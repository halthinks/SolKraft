#!/usr/bin/env python3
"""Exercise positive and adversarial cases for the multi registry validator."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_multi_registry import validate_registry  # noqa: E402


def valid_registry() -> dict:
    return {
        "profile": "multi",
        "capsule_sha256": "0" * 64,
        "real_agent_capability": {"verified": True, "evidence": "Codex collaboration agent listing"},
        "root_agent_id": "root",
        "requirement_ids": ["RQ-001", "RQ-002"],
        "agents": [
            {"agent_id": "root", "role": "integration and acceptance", "status": "running"},
            {"agent_id": "worker-a", "role": "independent implementation", "status": "completed"},
            {"agent_id": "worker-b", "role": "independent verification", "status": "completed"},
        ],
        "workstreams": [
            {
                "workstream_id": "implementation",
                "owner_agent_id": "worker-a",
                "task": "Implement bounded change",
                "requirement_ids": ["RQ-001"],
                "authorization_basis": "Validated capsule authorizes workspace writes",
                "resources": [{"resource": "src/feature.py", "access": "write"}],
                "status": "complete",
            },
            {
                "workstream_id": "verification",
                "owner_agent_id": "worker-b",
                "task": "Run independent acceptance tests",
                "requirement_ids": ["RQ-002"],
                "authorization_basis": "Validated capsule authorizes read-only verification",
                "resources": [{"resource": "tests/test_feature.py", "access": "read"}],
                "status": "complete",
            },
        ],
        "handoffs": [
            {
                "handoff_id": "H-001",
                "workstream_id": "implementation",
                "from_agent_id": "worker-a",
                "to_agent_id": "root",
                "task": "Implement bounded change",
                "scope": "src/feature.py only",
                "access_classification": "write",
                "authorization_basis": "RQ-001 and capsule write scope",
                "requirement_ids": ["RQ-001"],
                "commands_tools": ["apply_patch", "python -m pytest tests/test_feature.py"],
                "started_at": "2026-07-13T10:00:00Z",
                "completed_at": "2026-07-13T10:05:00Z",
                "status": "completed",
                "results": "Change implemented and focused test passed",
                "evidence": [{"kind": "test_result", "locator": "terminal:test-feature", "claim": "Focused test passed"}],
                "uncertainties": [],
                "next_safe_action": "Root inspect diff and rerun integrated verification",
            }
        ],
        "integrated_verification": {
            "performed_by_root": True,
            "evidence": ["terminal:integrated-tests"],
            "adversarial_audit": ["Requirement and unauthorized-scope audit passed"],
        },
    }


def expect_error(name: str, mutate, needle: str) -> None:
    case = copy.deepcopy(valid_registry())
    mutate(case)
    errors = validate_registry(case)
    if not any(needle in error for error in errors):
        raise AssertionError(f"{name}: expected {needle!r}, got {errors!r}")
    print(f"PASS reject {name}")


def main() -> int:
    errors = validate_registry(valid_registry())
    if errors:
        raise AssertionError(f"valid registry rejected: {errors!r}")
    print("PASS accept valid registry and evidence-bearing handoff")

    capsule = {
        "capsule_sha256": "0" * 64,
        "payload": {"requirements": [{"id": "RQ-001"}, {"id": "RQ-002"}]},
    }
    if validate_registry(valid_registry(), capsule):
        raise AssertionError("capsule-bound registry was rejected")
    print("PASS accept exact capsule binding")
    wrong_hash = valid_registry()
    wrong_hash["capsule_sha256"] = "1" * 64
    if not any("different capsule" in error for error in validate_registry(wrong_hash, capsule)):
        raise AssertionError("capsule hash mismatch was accepted")
    print("PASS reject capsule hash mismatch")
    wrong_requirements = valid_registry()
    wrong_requirements["requirement_ids"] = ["RQ-001"]
    if not any("exactly match" in error for error in validate_registry(wrong_requirements, capsule)):
        raise AssertionError("capsule requirement mismatch was accepted")
    print("PASS reject capsule requirement mismatch")

    expect_error(
        "duplicate ownership",
        lambda d: d["workstreams"][0]["resources"].append({"resource": "src/feature.py", "access": "write"}),
        "duplicate ownership declaration",
    )
    expect_error(
        "invalid requirement ID",
        lambda d: d["workstreams"][0]["requirement_ids"].append("RQ-999"),
        "invalid requirement IDs",
    )
    expect_error(
        "unsupported status",
        lambda d: d["agents"][1].update(status="imaginary"),
        "unsupported agent status",
    )
    expect_error(
        "missing evidence",
        lambda d: d["handoffs"][0].update(evidence=[]),
        "missing evidence",
    )
    expect_error(
        "unsupported summary evidence",
        lambda d: d["handoffs"][0].update(evidence=[{"kind": "summary", "locator": "agent", "claim": "done"}]),
        "unsupported summary",
    )

    def conflict(d: dict) -> None:
        d["workstreams"][1]["resources"] = [{"resource": "src/feature.py", "access": "write"}]

    expect_error("conflicting write ownership", conflict, "conflicting write ownership")
    print("PASS all multi profile self-tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
