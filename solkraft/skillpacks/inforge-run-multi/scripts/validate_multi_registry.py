#!/usr/bin/env python3
"""Validate an InForge Run Multi registry without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from validate_capsule import ValidationError, load_validate
AGENT_STATUSES = {"running", "idle", "completed", "blocked", "failed", "interrupted"}
WORK_STATUSES = {"pending", "active", "blocked", "failed", "complete", "integrated"}
HANDOFF_STATUSES = {"completed", "blocked", "failed"}
EVIDENCE_KINDS = {"command_output", "diff", "test_result", "artifact", "tool_result"}


def _nonempty(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def _unique(values: list[object], label: str, errors: list[str]) -> None:
    if len(values) != len(set(values)):
        errors.append(f"duplicate {label}")


def _datetime(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{label} must be an ISO-8601 timestamp")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO-8601 timestamp")


def validate_registry(data: object, capsule: dict | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry must be a JSON object"]
    if data.get("profile") != "multi":
        errors.append("profile must be multi")
    capsule_hash = data.get("capsule_sha256")
    _nonempty(capsule_hash, "capsule_sha256", errors)
    if capsule is not None and capsule_hash != capsule.get("capsule_sha256"):
        errors.append("registry is bound to a different capsule")

    capability = data.get("real_agent_capability")
    if not isinstance(capability, dict) or capability.get("verified") is not True:
        errors.append("real Codex desktop agent capability must be verified")
    else:
        _nonempty(capability.get("evidence"), "real_agent_capability.evidence", errors)

    requirements = data.get("requirement_ids")
    if not isinstance(requirements, list) or not requirements:
        errors.append("requirement_ids must be a non-empty list")
        requirements = []
    else:
        for rid in requirements:
            if not isinstance(rid, str) or not rid.strip() or any(ch.isspace() for ch in rid):
                errors.append(f"invalid requirement ID: {rid!r}")
        _unique(requirements, "requirement IDs", errors)
    requirement_set = set(requirements)
    if capsule is not None:
        capsule_requirements = {row["id"] for row in capsule["payload"]["requirements"]}
        if requirement_set != capsule_requirements:
            errors.append("registry requirement IDs do not exactly match the capsule")

    agents = data.get("agents")
    if not isinstance(agents, list) or len(agents) < 2:
        errors.append("agents must contain the root and at least one real worker")
        agents = []
    agent_ids: list[object] = []
    for i, agent in enumerate(agents):
        if not isinstance(agent, dict):
            errors.append(f"agents[{i}] must be an object")
            continue
        aid = agent.get("agent_id")
        _nonempty(aid, f"agents[{i}].agent_id", errors)
        agent_ids.append(aid)
        if agent.get("status") not in AGENT_STATUSES:
            errors.append(f"unsupported agent status: {agent.get('status')!r}")
    _unique(agent_ids, "agent IDs", errors)
    agent_set = set(agent_ids)
    root = data.get("root_agent_id")
    if root not in agent_set:
        errors.append("root_agent_id must identify a registered agent")

    workstreams = data.get("workstreams")
    if not isinstance(workstreams, list) or not workstreams:
        errors.append("workstreams must be a non-empty list")
        workstreams = []
    workstream_ids: list[object] = []
    ownership: dict[str, tuple[object, str]] = {}
    for i, work in enumerate(workstreams):
        if not isinstance(work, dict):
            errors.append(f"workstreams[{i}] must be an object")
            continue
        wid = work.get("workstream_id")
        _nonempty(wid, f"workstreams[{i}].workstream_id", errors)
        workstream_ids.append(wid)
        owner = work.get("owner_agent_id")
        if owner not in agent_set:
            errors.append(f"workstream {wid!r} has an unknown owner")
        if work.get("status") not in WORK_STATUSES:
            errors.append(f"unsupported workstream status: {work.get('status')!r}")
        refs = work.get("requirement_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"workstream {wid!r} requires requirement IDs")
        else:
            unknown = set(refs) - requirement_set
            if unknown:
                errors.append(f"workstream {wid!r} has invalid requirement IDs: {sorted(unknown)}")
        _nonempty(work.get("authorization_basis"), f"workstream {wid!r} authorization_basis", errors)
        resources = work.get("resources")
        if not isinstance(resources, list) or not resources:
            errors.append(f"workstream {wid!r} requires resources")
            continue
        for resource in resources:
            if not isinstance(resource, dict):
                errors.append(f"workstream {wid!r} has an invalid resource")
                continue
            path = resource.get("resource")
            access = resource.get("access")
            _nonempty(path, f"workstream {wid!r} resource", errors)
            if access not in {"read", "write"}:
                errors.append(f"workstream {wid!r} has unsupported resource access: {access!r}")
                continue
            if not isinstance(path, str) or not path.strip():
                continue
            key = path.strip().casefold()
            if key in ownership:
                previous_owner, previous_access = ownership[key]
                if owner == previous_owner:
                    errors.append(f"duplicate ownership declaration for resource {path!r}")
                elif access == "write" or previous_access == "write":
                    errors.append(f"conflicting write ownership for resource {path!r}")
            else:
                ownership[key] = (owner, access)
    _unique(workstream_ids, "workstream ownership", errors)
    workstream_set = set(workstream_ids)

    handoffs = data.get("handoffs")
    if not isinstance(handoffs, list):
        errors.append("handoffs must be a list")
        handoffs = []
    handoff_ids: list[object] = []
    for i, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            errors.append(f"handoffs[{i}] must be an object")
            continue
        hid = handoff.get("handoff_id")
        _nonempty(hid, f"handoffs[{i}].handoff_id", errors)
        handoff_ids.append(hid)
        if handoff.get("workstream_id") not in workstream_set:
            errors.append(f"handoff {hid!r} references an unknown workstream")
        for field in ("from_agent_id", "to_agent_id"):
            if handoff.get(field) not in agent_set:
                errors.append(f"handoff {hid!r} has unknown {field}")
        for field in ("task", "scope", "authorization_basis", "results", "next_safe_action"):
            _nonempty(handoff.get(field), f"handoff {hid!r} {field}", errors)
        if handoff.get("access_classification") not in {"read", "write", "mixed"}:
            errors.append(f"handoff {hid!r} has unsupported access classification")
        if handoff.get("status") not in HANDOFF_STATUSES:
            errors.append(f"unsupported handoff status: {handoff.get('status')!r}")
        refs = handoff.get("requirement_ids")
        if not isinstance(refs, list) or not refs or set(refs) - requirement_set:
            errors.append(f"handoff {hid!r} has invalid requirement IDs")
        commands = handoff.get("commands_tools")
        if not isinstance(commands, list) or not commands or not all(isinstance(x, str) and x.strip() for x in commands):
            errors.append(f"handoff {hid!r} must record commands or tools")
        _datetime(handoff.get("started_at"), f"handoff {hid!r} started_at", errors)
        _datetime(handoff.get("completed_at"), f"handoff {hid!r} completed_at", errors)
        evidence = handoff.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"handoff {hid!r} is missing evidence")
        else:
            for item in evidence:
                if not isinstance(item, dict) or item.get("kind") not in EVIDENCE_KINDS:
                    errors.append(f"handoff {hid!r} contains unsupported summary or evidence kind")
                    continue
                _nonempty(item.get("locator"), f"handoff {hid!r} evidence locator", errors)
                _nonempty(item.get("claim"), f"handoff {hid!r} evidence claim", errors)
        if not isinstance(handoff.get("uncertainties"), list):
            errors.append(f"handoff {hid!r} uncertainties must be a list")
    _unique(handoff_ids, "handoff IDs", errors)

    verification = data.get("integrated_verification")
    if not isinstance(verification, dict):
        errors.append("integrated_verification must be an object")
    elif verification.get("performed_by_root") is True:
        if not verification.get("evidence"):
            errors.append("root integrated verification requires evidence")
        if not verification.get("adversarial_audit"):
            errors.append("root integrated verification requires an adversarial audit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--capsule", type=Path, required=True)
    args = parser.parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
        capsule = load_validate(args.capsule)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_registry(data, capsule)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: valid InForge Run Multi registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
