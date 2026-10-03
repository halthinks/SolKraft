#!/usr/bin/env python3
"""Maintain a hash-bound SolForge Ultra execution and single-lease ledger."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_capsule import ValidationError, load_validate, requires_confirmation
from validate_ultra_budget import (
    ZERO_HASH,
    budget_hash,
    canonical_sha,
    forward_control_errors,
    load_budget,
    validate as validate_budget,
)


TRANSITIONS = {
    "preflight": {"awaiting_confirmation", "ready", "blocked", "declined"},
    "awaiting_confirmation": {"ready", "blocked", "declined"},
    "ready": {"executing", "blocked", "declined"},
    "executing": {"verifying", "blocked", "declined"},
    "verifying": {"executing", "adversarial_audit", "blocked", "declined"},
    "adversarial_audit": {"executing", "verifying", "blocked", "declined"},
    "complete": set(),
    "blocked": set(),
    "declined": set(),
    "terminated": set(),
}
APPROACH_STATUSES = {"candidate", "active", "blocked", "falsified", "superseded", "integrated", "accepted"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def event(state, kind, detail):
    state["events"].append({"sequence": len(state["events"]) + 1, "kind": kind, "detail": detail})


def lease_event(state, lease_id, kind, **detail):
    ledger = state["lease_ledger"]
    row = {
        "sequence": len(ledger["entries"]) + 1,
        "previous_sha256": ledger["head_sha256"],
        "lease_id": lease_id,
        "event": kind,
        **detail,
    }
    row["entry_sha256"] = canonical_sha(row)
    ledger["entries"].append(row)
    ledger["head_sha256"] = row["entry_sha256"]


def validation_options(args, control_mode):
    return {
        "proof_only_fixture": args.proof_only_fixture,
        "control_mode": control_mode,
        "current_time": args.validation_time,
        "runtime_config_sha256": args.runtime_config_sha256,
        "runtime_kill_switch": args.runtime_kill_switch,
    }


def get(capsule_path, budget_path, state_path, **validation):
    capsule = load_validate(capsule_path)
    budget = load_budget(budget_path)
    state = read(state_path)
    errors = validate_budget(budget, capsule, state, **validation)
    if errors:
        raise ValidationError("; ".join(errors))
    drift = []
    if validation.get("control_mode") == "safe_exit":
        drift = forward_control_errors(
            budget,
            proof_only_fixture=validation.get("proof_only_fixture", False),
            current_time=validation.get("current_time"),
            runtime_config_sha256=validation.get("runtime_config_sha256"),
            runtime_kill_switch=validation.get("runtime_kill_switch"),
        )
    return capsule, budget, state, drift


def record_control_drift(state, command, drift):
    if not drift:
        return
    observation = {"command": command, "reasons": sorted(set(drift))}
    if observation not in state["control_drift"]:
        state["control_drift"].append(observation)
        event(state, "safe_exit_control_drift", observation)


def over(capsule, budget, usage):
    checks = {
        "elapsed_seconds": budget["limits"]["max_elapsed_seconds"],
        "tool_calls": budget["limits"]["max_tool_calls"],
        "rounds": budget["limits"]["max_rounds"],
        "agents": budget["limits"]["max_agents"],
        "cost_usd": budget["limits"]["max_cost_usd"],
    }
    exceeded = [key for key, maximum in checks.items() if usage[key] > maximum]
    if usage["retries"] > capsule["payload"]["retry_limit"]:
        exceeded.append("retries")
    return exceeded


def contained(target, roots):
    normalized_target = os.path.normcase(os.path.abspath(os.path.expanduser(target)))
    for root in roots:
        normalized_root = os.path.normcase(os.path.abspath(os.path.expanduser(root)))
        try:
            if os.path.commonpath([normalized_target, normalized_root]) == normalized_root:
                return True
        except ValueError:
            pass
        if target == root or target.startswith(root.rstrip("/") + "/"):
            return True
    return False


def add_common(parser):
    parser.add_argument("capsule")
    parser.add_argument("budget")
    parser.add_argument("state")
    parser.add_argument("--proof-only-fixture", action="store_true")
    parser.add_argument("--validation-time", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-config-sha256", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-kill-switch", help=argparse.SUPPRESS)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    command = sub.add_parser("init")
    add_common(command)
    command = sub.add_parser("transition")
    add_common(command)
    command.add_argument("to")
    command.add_argument("--reason", default="")
    command = sub.add_parser("approach")
    add_common(command)
    command.add_argument("id")
    command.add_argument("family")
    command.add_argument("status", choices=sorted(APPROACH_STATUSES))
    command.add_argument("--hypothesis", default="")
    command.add_argument("--evidence", default="")
    command.add_argument("--blocker", default="")
    command = sub.add_parser("lease-open")
    add_common(command)
    command.add_argument("lease_id")
    command.add_argument("--unit", required=True)
    command = sub.add_parser("lease-close")
    add_common(command)
    command.add_argument("lease_id")
    command.add_argument("--checkpoint-sha256", required=True)
    command.add_argument("--abandoned-reason", default="")
    command = sub.add_parser("kill")
    add_common(command)
    command.add_argument("--reason", required=True)
    command = sub.add_parser("action")
    add_common(command)
    command.add_argument("lease_id")
    command.add_argument("action_id")
    command.add_argument("kind")
    command.add_argument("target")
    command.add_argument("--requirement-id", action="append", required=True)
    command.add_argument("--tool", required=True)
    command.add_argument("--expected", required=True)
    command.add_argument("--actual", required=True)
    command.add_argument("--evidence", required=True)
    command.add_argument("--rollback", default="not_applicable")
    command.add_argument("--mutation", action="store_true")
    command.add_argument("--external", action="store_true")
    command.add_argument("--elapsed", type=float, default=0)
    command.add_argument("--tools", type=int, default=1)
    command.add_argument("--rounds", type=int, default=0)
    command.add_argument("--agents", type=int, default=2)
    command.add_argument("--cost", type=float, default=0)
    command.add_argument("--retry", action="store_true")
    command = sub.add_parser("evidence")
    add_common(command)
    command.add_argument("requirement_id")
    command.add_argument("locator")
    command.add_argument("method")
    command.add_argument("result", choices=["passed", "failed", "blocked"])
    command = sub.add_parser("proposal")
    add_common(command)
    command.add_argument("proposal_id")
    command.add_argument("--summary", required=True)
    command.add_argument("--evidence", required=True)
    args = parser.parse_args()

    try:
        if args.cmd == "init":
            capsule = load_validate(args.capsule)
            budget = load_budget(args.budget)
            errors = validate_budget(
                budget,
                capsule,
                **validation_options(args, "forward"),
            )
            if errors:
                raise ValidationError("; ".join(errors))
            status = "awaiting_confirmation" if requires_confirmation(capsule) and capsule["confirmation"] is None else "preflight"
            state = {
                "schema_version": "1.1.0",
                "capsule_sha256": capsule["capsule_sha256"],
                "budget_sha256": budget_hash(budget),
                "capability_attestation_sha256": budget["capability_attestation"]["attestation_sha256"],
                "provider_verification_receipt_sha256": budget["capability_attestation"]["verification_receipt_sha256"],
                "authorization_receipt_sha256": budget["authorization"]["receipt_sha256"],
                "validation_mode": budget["validation_mode"],
                "status": status,
                "created_unix": int(time.time()),
                "usage": {"elapsed_seconds": 0, "tool_calls": 0, "rounds": 0, "agents": 0, "cost_usd": 0, "retries": 0},
                "kill_switch": {
                    "armed": True,
                    "invoked": False,
                    "activation_receipt_sha256": budget["kill_switch"]["activation_receipt_sha256"],
                    "invocation": None,
                },
                "lease_ledger": {"policy_receipt_sha256": budget["lease_policy"]["receipt_sha256"], "active_lease": None, "entries": [], "head_sha256": ZERO_HASH},
                "approaches": {},
                "actions": [],
                "evidence": {row["id"]: [] for row in capsule["payload"]["requirements"]},
                "proposals": [],
                "violations": [],
                "control_drift": [],
                "events": [],
                "audit_receipt": None,
            }
            event(state, "initialized", status)
            write(args.state, state)
            print(f"PASS: initialized {status} with hash-bound Ultra controls")
            return 0

        safe_transitions = {"verifying", "adversarial_audit", "blocked", "declined"}
        safe_exit = args.cmd in {"kill", "lease-close", "action", "evidence", "proposal"} or (
            args.cmd == "transition" and args.to in safe_transitions
        )
        capsule, budget, state, drift = get(
            args.capsule,
            args.budget,
            args.state,
            **validation_options(args, "safe_exit" if safe_exit else "forward"),
        )
        if safe_exit:
            record_control_drift(state, args.cmd, drift)
        if args.cmd == "kill":
            if state["status"] in {"complete", "blocked", "declined", "terminated"}:
                return fail("terminal state is immutable")
            if not args.reason.strip():
                return fail("kill requires a reason")
            active = state["lease_ledger"]["active_lease"]
            if active:
                lease_event(state, active["lease_id"], "terminated", reason=args.reason, action_ids=list(active["action_ids"]))
                state["lease_ledger"]["active_lease"] = None
            state["kill_switch"]["invoked"] = True
            state["kill_switch"]["invocation"] = {"reason": args.reason, "recorded_unix": int(time.time())}
            old = state["status"]
            state["status"] = "terminated"
            event(state, "kill_switch_invoked", {"from": old, "reason": args.reason})
            write(args.state, state)
            print("PASS: kill switch invoked; state terminated")
            return 0

        if state["status"] in {"complete", "blocked", "declined", "terminated"}:
            return fail("terminal state is immutable")

        if args.cmd == "transition":
            if args.to == "complete":
                return fail("complete is reserved for acceptance_audit.py --complete")
            if args.to == "terminated":
                return fail("terminated is reserved for the kill command")
            if args.to not in TRANSITIONS.get(state["status"], set()):
                return fail(f"invalid transition {state['status']} -> {args.to}")
            if args.to == "ready":
                load_validate(args.capsule, require_confirmation=True)
                if state["status"] not in {"preflight", "awaiting_confirmation"}:
                    return fail("ready requires preflight")
            if args.to in {"blocked", "declined"} and not args.reason.strip():
                return fail("terminal transition requires a reason")
            if state["lease_ledger"]["active_lease"] is not None and args.to != "executing":
                return fail("checkpoint or terminate the active lease before transition")
            old = state["status"]
            state["status"] = args.to
            event(state, "transition", {"from": old, "to": args.to, "reason": args.reason})
            write(args.state, state)
            print(f"PASS: {old} -> {args.to}")
            return 0

        if args.cmd == "approach":
            state["approaches"][args.id] = {
                "family": args.family, "status": args.status, "hypothesis": args.hypothesis,
                "evidence": args.evidence, "blocker": args.blocker,
            }
            event(state, "approach", args.id)
            write(args.state, state)
            print("PASS: approach recorded")
            return 0

        if args.cmd == "lease-open":
            if state["status"] != "executing":
                return fail("lease acquisition requires executing state")
            if state["lease_ledger"]["active_lease"] is not None:
                return fail("only one active Ultra lease is permitted")
            if not args.lease_id.strip() or not args.unit.strip():
                return fail("lease ID and bounded unit must be nonempty")
            if any(row.get("lease_id") == args.lease_id for row in state["lease_ledger"]["entries"]):
                return fail("lease IDs cannot be reused")
            active = {"lease_id": args.lease_id, "unit": args.unit, "action_ids": [], "acquired_unix": int(time.time())}
            state["lease_ledger"]["active_lease"] = active
            lease_event(state, args.lease_id, "acquired", unit=args.unit)
            event(state, "lease_acquired", args.lease_id)
            write(args.state, state)
            print("PASS: one bounded Ultra lease acquired")
            return 0

        if args.cmd == "lease-close":
            active = state["lease_ledger"]["active_lease"]
            if not active or active.get("lease_id") != args.lease_id:
                return fail("lease ID is not active")
            if len(active["action_ids"]) > 1:
                return fail("a lease may contain at most one bounded action before checkpoint")
            if not active["action_ids"] and not args.abandoned_reason.strip():
                return fail("an empty lease requires --abandoned-reason for a safe pause")
            if active["action_ids"] and args.abandoned_reason.strip():
                return fail("a completed lease cannot be marked abandoned")
            if len(args.checkpoint_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in args.checkpoint_sha256):
                return fail("checkpoint SHA-256 must be lowercase hexadecimal")
            detail = {
                "checkpoint_sha256": args.checkpoint_sha256,
                "action_ids": list(active["action_ids"]),
                "disposition": "completed" if active["action_ids"] else "abandoned",
            }
            if not active["action_ids"]:
                detail["abandoned_reason"] = args.abandoned_reason.strip()
            lease_event(state, args.lease_id, "checkpointed", **detail)
            state["lease_ledger"]["active_lease"] = None
            event(state, "lease_checkpointed", args.lease_id)
            write(args.state, state)
            print("PASS: bounded Ultra lease checkpointed")
            return 0

        if args.cmd == "action":
            if state["status"] != "executing":
                return fail("actions require executing state")
            load_validate(args.capsule, require_confirmation=True)
            active = state["lease_ledger"]["active_lease"]
            if not active or active.get("lease_id") != args.lease_id:
                return fail("action requires the matching active lease")
            if active["action_ids"]:
                return fail("one bounded action is permitted per lease")
            authorization = capsule["payload"]["authorization"]
            scope = capsule["payload"]["scope"]
            violations = []
            valid_requirement_ids = {row["id"] for row in capsule["payload"]["requirements"]}
            if any(requirement_id not in valid_requirement_ids for requirement_id in args.requirement_id):
                violations.append("unknown requirement id")
            if args.kind not in authorization["allowed_actions"] or args.kind in authorization["prohibited_actions"]:
                violations.append("unauthorized action kind")
            if args.tool not in authorization["allowed_tools"]:
                violations.append("unauthorized tool")
            if not contained(args.target, scope["in_scope"]) or contained(args.target, scope["out_of_scope"]):
                violations.append("target outside authorized scope")
            if args.mutation and not authorization["mutation_allowed"]:
                violations.append("mutation not authorized")
            if args.external and not authorization["external_side_effects_allowed"]:
                violations.append("external effect not authorized")
            if (args.mutation or args.external) and (not args.rollback.strip() or args.rollback == "not_applicable"):
                violations.append("mutation/external action requires rollback or recovery evidence")
            increments = (args.elapsed, args.tools, args.rounds, args.agents, args.cost)
            if any(not math.isfinite(value) or value < 0 for value in increments):
                violations.append("usage increments must be finite and nonnegative")
            if args.agents < 2:
                violations.append("native Ultra execution requires at least two verified agents")
            if args.retry and not any(
                row.get("status") in {"blocked", "falsified"} and (row.get("hypothesis") or row.get("blocker"))
                for row in state["approaches"].values()
            ):
                violations.append("retry requires a recorded blocked/falsified approach and new mechanism")
            proposed = dict(state["usage"])
            proposed["elapsed_seconds"] += args.elapsed
            proposed["tool_calls"] += args.tools
            proposed["rounds"] += args.rounds
            proposed["agents"] = max(proposed["agents"], args.agents)
            proposed["cost_usd"] += args.cost
            proposed["retries"] += int(args.retry)
            exceeded = over(capsule, budget, proposed)
            if exceeded:
                violations.append("budget exceeded: " + ", ".join(exceeded))
            if violations:
                state["violations"].append({"action_id": args.action_id, "violations": violations})
                event(state, "action_rejected", args.action_id)
                write(args.state, state)
                return fail("; ".join(violations))
            state["usage"] = proposed
            state["actions"].append({
                "id": args.action_id, "lease_id": args.lease_id, "requirement_ids": args.requirement_id,
                "kind": args.kind, "target": args.target, "tool": args.tool, "mutation": args.mutation,
                "external": args.external, "expected": args.expected, "actual": args.actual,
                "evidence": args.evidence, "rollback": args.rollback, "status": "closed",
            })
            active["action_ids"].append(args.action_id)
            event(state, "action", args.action_id)
            write(args.state, state)
            print("PASS: one bounded action recorded within Ultra authority and budgets")
            return 0

        if args.cmd == "evidence":
            if args.requirement_id not in state["evidence"]:
                return fail("unknown requirement id")
            if not args.locator.strip() or not args.method.strip():
                return fail("evidence locator and method must be nonempty")
            state["evidence"][args.requirement_id].append({"locator": args.locator, "method": args.method, "result": args.result})
            event(state, "evidence", args.requirement_id)
            write(args.state, state)
            print("PASS: evidence recorded")
            return 0

        if args.cmd == "proposal":
            if not args.proposal_id.strip() or not args.summary.strip() or not args.evidence.strip():
                return fail("proposal ID, summary, and evidence must be nonempty")
            if any(row.get("id") == args.proposal_id for row in state["proposals"]):
                return fail("proposal IDs cannot be reused")
            proposal = {
                "sequence": len(state["proposals"]) + 1,
                "id": args.proposal_id,
                "summary": args.summary,
                "evidence": args.evidence,
            }
            proposal["proposal_sha256"] = canonical_sha(proposal)
            state["proposals"].append(proposal)
            event(state, "safe_exit_proposal", args.proposal_id)
            write(args.state, state)
            print("PASS: non-executing proposal recorded without expanding authority")
            return 0
    except (ValidationError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
