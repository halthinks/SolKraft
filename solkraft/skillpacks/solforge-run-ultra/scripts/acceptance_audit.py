#!/usr/bin/env python3
"""Perform the sole completion gate for SolForge Run Ultra."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_capsule import ValidationError, load_validate, requires_confirmation
from validate_ultra_budget import (
    budget_hash,
    canonical_sha,
    forward_control_errors,
    load_budget,
    validate as validate_budget,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capsule")
    parser.add_argument("budget")
    parser.add_argument("state")
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--proof-only-fixture", action="store_true")
    parser.add_argument("--validation-time", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-config-sha256", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-kill-switch", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        capsule = load_validate(args.capsule, require_confirmation=True)
        budget = load_budget(args.budget)
        state_path = Path(args.state)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        validation = {
            "proof_only_fixture": args.proof_only_fixture,
            "control_mode": "safe_exit",
            "current_time": args.validation_time,
            "runtime_config_sha256": args.runtime_config_sha256,
            "runtime_kill_switch": args.runtime_kill_switch,
        }
        errors = validate_budget(budget, capsule, state, **validation)
        drift = forward_control_errors(
            budget,
            proof_only_fixture=args.proof_only_fixture,
            current_time=args.validation_time,
            runtime_config_sha256=args.runtime_config_sha256,
            runtime_kill_switch=args.runtime_kill_switch,
        )
        if state.get("capsule_sha256") != capsule["capsule_sha256"]:
            errors.append("state/capsule hash mismatch")
        if state.get("budget_sha256") != budget_hash(budget):
            errors.append("state/budget hash mismatch")
        capability_hash = budget.get("capability_attestation", {}).get("attestation_sha256")
        if state.get("capability_attestation_sha256") != capability_hash:
            errors.append("state/capability attestation mismatch")
        if state.get("provider_verification_receipt_sha256") != budget.get(
            "capability_attestation", {}
        ).get("verification_receipt_sha256"):
            errors.append("state/provider verification receipt mismatch")
        if state.get("authorization_receipt_sha256") != budget.get("authorization", {}).get(
            "receipt_sha256"
        ):
            errors.append("state/user authorization receipt mismatch")
        if state.get("status") != "adversarial_audit":
            errors.append("state must be adversarial_audit")
        usage = state.get("usage", {})
        if usage.get("agents", 0) < 2:
            errors.append("Ultra audit requires at least two verified native Ultra agents")
        if state.get("violations"):
            errors.append("execution ledger contains rejected authority/scope/budget actions")
        actions = state.get("actions", [])
        if not actions:
            errors.append("no bounded Ultra action evidence exists")
        if any(action.get("status") != "closed" for action in actions):
            errors.append("open action remains")

        kill = state.get("kill_switch", {})
        if kill.get("armed") is not True:
            errors.append("kill switch is not armed")
        if kill.get("invoked") is True:
            errors.append("terminated Ultra work cannot pass acceptance")

        ledger = state.get("lease_ledger", {})
        if ledger.get("active_lease") is not None:
            errors.append("active lease must be checkpointed before acceptance")
        entries = ledger.get("entries", []) if isinstance(ledger, dict) else []
        checkpointed = [row for row in entries if isinstance(row, dict) and row.get("event") == "checkpointed"]
        if not checkpointed:
            errors.append("lease ledger has no checkpointed bounded unit")
        closed_action_ids = {action.get("id") for action in actions if action.get("status") == "closed"}
        ledger_action_ids = {
            action_id
            for row in checkpointed
            for action_id in row.get("action_ids", [])
        }
        if ledger_action_ids != closed_action_ids:
            errors.append("checkpointed lease actions do not match the action ledger")

        approaches = state.get("approaches", {})
        if not approaches:
            errors.append("approach registry is empty")
        elif not any(row.get("status") in {"accepted", "integrated"} for row in approaches.values()):
            errors.append("no approach was accepted or integrated")
        expected = {row["id"] for row in capsule["payload"]["requirements"]}
        actual = set(state.get("evidence", {}))
        if actual != expected:
            errors.append("evidence requirement set mismatch")
        for requirement_id in sorted(expected):
            records = state.get("evidence", {}).get(requirement_id, [])
            if not any(
                row.get("result") == "passed"
                and str(row.get("locator", "")).strip()
                and str(row.get("method", "")).strip()
                for row in records
            ):
                errors.append(f"missing passed evidence for {requirement_id}")
        if requires_confirmation(capsule) and capsule["confirmation"] is None:
            errors.append("required confirmation absent")
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(
            f"PASS: all {len(expected)} requirements have accepted evidence; "
            "immutable capability receipts, authority, budget, and lease controls are clean; "
            "any live-control drift is bound to the audit receipt"
        )
        if args.complete:
            precompletion_hash = canonical_sha({key: value for key, value in state.items() if key != "audit_receipt"})
            state["audit_receipt"] = {
                "result": "passed",
                "capsule_sha256": capsule["capsule_sha256"],
                "budget_sha256": budget_hash(budget),
                "capability_attestation_sha256": capability_hash,
                "provider_verification_receipt_sha256": budget["capability_attestation"]["verification_receipt_sha256"],
                "authorization_receipt_sha256": budget["authorization"]["receipt_sha256"],
                "lease_ledger_head_sha256": ledger["head_sha256"],
                "precompletion_state_sha256": precompletion_hash,
                "requirement_ids": sorted(expected),
                "forward_control_drift_at_completion": sorted(set(drift)),
            }
            state["status"] = "complete"
            state["events"].append({
                "sequence": len(state["events"]) + 1,
                "kind": "acceptance_complete",
                "detail": capsule["capsule_sha256"],
            })
            temporary = Path(str(state_path) + ".tmp")
            temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            os.replace(temporary, state_path)
            print("PASS: terminal state complete")
        return 0
    except (ValidationError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
