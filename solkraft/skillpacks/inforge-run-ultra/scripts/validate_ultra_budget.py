#!/usr/bin/env python3
"""Validate bounded Ultra authorization without launching Ultra."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


FIELDS = ("max_elapsed_seconds", "max_tool_calls", "max_rounds", "max_agents", "max_cost_usd")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def limits_hash(limits: dict) -> str:
    return sha_bytes(json.dumps(limits, sort_keys=True, separators=(",", ":")).encode())


def validate(budget: dict, capsule_bytes: bytes, usage: dict | None = None) -> list[str]:
    errors: list[str] = []
    capsule_sha = sha_bytes(capsule_bytes)
    if budget.get("capsule_sha256") != capsule_sha:
        errors.append("capsule_sha256 mismatch")
    if budget.get("native_ultra_verified") is not True:
        errors.append("native Ultra capability is not verified")
    limits = budget.get("limits")
    if not isinstance(limits, dict) or set(limits) != set(FIELDS):
        errors.append("all and only required hard ceilings must be present")
        limits = {}
    for field in FIELDS:
        value = limits.get(field)
        if field == "max_cost_usd":
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"{field} must be finite and nonnegative")
        elif not isinstance(value, int) or isinstance(value, bool) or value < 1:
            errors.append(f"{field} must be a positive integer")
    auth = budget.get("authorization")
    expected_budget_sha = limits_hash(limits) if limits else ""
    if not isinstance(auth, dict):
        errors.append("user Ultra authorization is required")
        auth = {}
    if auth.get("authorized_by") != "user" or not str(auth.get("confirmation_text", "")).strip():
        errors.append("authorization must contain user-authored confirmation")
    if not str(auth.get("confirmed_at", "")).strip():
        errors.append("authorization timestamp is required")
    if auth.get("capsule_sha256") != capsule_sha:
        errors.append("authorization is not bound to capsule")
    if auth.get("budget_sha256") != expected_budget_sha:
        errors.append("authorization is not bound to current limits")
    extension = budget.get("extension")
    if extension is not None:
        if not isinstance(extension, dict):
            errors.append("extension must be an object")
        else:
            if extension.get("new_budget_sha256") != expected_budget_sha:
                errors.append("extension new budget hash mismatch")
            if not str(extension.get("old_budget_sha256", "")).strip() or extension.get("old_budget_sha256") == expected_budget_sha:
                errors.append("extension must bind a distinct old budget hash")
            if extension.get("authorized_by") != "user" or not str(extension.get("confirmation_text", "")).strip():
                errors.append("budget extension requires new user confirmation")
            if not str(extension.get("reason", "")).strip():
                errors.append("budget extension reason is required")
    if usage is not None and limits:
        mapping = {
            "elapsed_seconds": "max_elapsed_seconds",
            "tool_calls": "max_tool_calls",
            "rounds": "max_rounds",
            "agents": "max_agents",
            "cost_usd": "max_cost_usd",
        }
        for used_field, limit_field in mapping.items():
            used = usage.get(used_field, 0)
            if not isinstance(used, (int, float)) or used < 0:
                errors.append(f"invalid usage {used_field}")
            elif used > limits[limit_field]:
                errors.append(f"hard ceiling exceeded: {used_field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("budget")
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--usage")
    args = parser.parse_args()
    budget = json.loads(Path(args.budget).read_text(encoding="utf-8"))
    capsule_bytes = Path(args.capsule).read_bytes()
    usage = json.loads(Path(args.usage).read_text(encoding="utf-8")) if args.usage else None
    errors = validate(budget, capsule_bytes, usage)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Ultra budget authorization is valid; no Ultra execution was launched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
