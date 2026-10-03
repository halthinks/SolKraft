#!/usr/bin/env python3
"""Proof-only tests for Ultra gating, budgets, extensions, and termination."""

from __future__ import annotations

import hashlib
import json
from validate_ultra_budget import limits_hash, validate


CAPSULE = b'{"profile":"ultra","execution_boundary":"transpose_only"}'
CAPSULE_SHA = hashlib.sha256(CAPSULE).hexdigest()


def valid_budget() -> dict:
    limits = {
        "max_elapsed_seconds": 60,
        "max_tool_calls": 10,
        "max_rounds": 2,
        "max_agents": 2,
        "max_cost_usd": 1.0,
    }
    return {
        "capsule_sha256": CAPSULE_SHA,
        "native_ultra_verified": True,
        "limits": limits,
        "authorization": {
            "authorized_by": "user",
            "confirmation_text": "I authorize this bounded Ultra execution.",
            "confirmed_at": "2026-07-13T00:00:00Z",
            "capsule_sha256": CAPSULE_SHA,
            "budget_sha256": limits_hash(limits),
        },
    }


def require_failure(name: str, budget: dict, usage: dict | None = None) -> None:
    if not validate(budget, CAPSULE, usage):
        raise AssertionError(f"{name} unexpectedly passed")


def main() -> int:
    good = valid_budget()
    assert validate(good, CAPSULE) == []
    bad = valid_budget(); bad["native_ultra_verified"] = False
    require_failure("missing capability", bad)
    bad = valid_budget(); bad.pop("authorization")
    require_failure("missing authorization", bad)
    bad = valid_budget(); bad["capsule_sha256"] = "0" * 64
    require_failure("tampered capsule binding", bad)
    bad = valid_budget(); bad["limits"]["max_rounds"] = 0
    require_failure("unbounded/invalid limit", bad)
    require_failure("over budget", good, {"elapsed_seconds": 61})
    extended = valid_budget()
    old_hash = limits_hash(extended["limits"])
    extended["limits"]["max_rounds"] = 3
    new_hash = limits_hash(extended["limits"])
    extended["authorization"]["budget_sha256"] = new_hash
    extended["extension"] = {
        "old_budget_sha256": old_hash,
        "new_budget_sha256": new_hash,
        "reason": "User approved one additional round.",
        "authorized_by": "user",
        "confirmation_text": "I approve the stated budget extension.",
    }
    assert validate(extended, CAPSULE) == []
    bad = json.loads(json.dumps(extended)); bad["extension"]["confirmation_text"] = ""
    require_failure("invalid extension", bad)
    terminated = {"state": "terminated", "reason": "user kill", "pending_actions": []}
    assert terminated["state"] == "terminated" and not terminated["pending_actions"]
    print("PASS: Ultra proof-only controls; native Ultra was not launched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
