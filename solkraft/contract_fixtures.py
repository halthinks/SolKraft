"""Executable Contract v1 fixtures.

Fixtures are compact contract assertions. They exercise the production router
and contract-policy evaluator but never execute a skill or grant authority.
"""
from __future__ import annotations

from .contract_policy import evaluate_contract, normalize_policy
from .routing import route_request


def run_contract_fixtures(catalog, skill_id: str, contract: dict) -> dict:
    fixtures = contract.get("fixtures") or {}
    selection = fixtures.get("selection") or []
    policy = fixtures.get("policy") or []
    results = []

    for fixture in selection:
        objective = fixture["objective"]
        expected = fixture["expected_selected"]
        try:
            routed = route_request(
                catalog,
                objective,
                max_skills=fixture.get("max_skills", 50),
                context=fixture.get("context"),
                policy=fixture.get("policy"),
            )
            passed = (
                routed.get("selected") == expected
                and routed.get("execution_authorized") is False
            )
            results.append({
                "id": fixture["id"],
                "kind": "selection",
                "passed": passed,
                "expected_selected": expected,
                "actual_selected": routed.get("selected"),
                "execution_authorized": routed.get("execution_authorized"),
            })
        except Exception as exc:
            results.append({
                "id": fixture["id"],
                "kind": "selection",
                "passed": False,
                "expected_selected": expected,
                "actual_selected": None,
                "execution_authorized": None,
                "error": f"{type(exc).__name__}: {exc}",
            })

    for fixture in policy:
        objective = fixture.get("objective") or "Evaluate contract policy."
        expected_status = fixture["expected_status"]
        needle = fixture.get("reason_contains")
        try:
            normalized = normalize_policy(fixture.get("policy"), objective)
            decision = evaluate_contract(contract, normalized)
            reason_ok = (
                True if not needle
                else any(needle in reason for reason in decision.get("reasons") or [])
            )
            passed = decision.get("status") == expected_status and reason_ok
            results.append({
                "id": fixture["id"],
                "kind": "policy",
                "passed": passed,
                "expected_status": expected_status,
                "actual_status": decision.get("status"),
                "reason_contains": needle,
                "reasons": decision.get("reasons") or [],
            })
        except Exception as exc:
            results.append({
                "id": fixture["id"],
                "kind": "policy",
                "passed": False,
                "expected_status": expected_status,
                "actual_status": None,
                "reason_contains": needle,
                "reasons": [],
                "error": f"{type(exc).__name__}: {exc}",
            })

    return {
        "skill_id": skill_id,
        "total": len(results),
        "passed": sum(1 for item in results if item["passed"]),
        "failed": sum(1 for item in results if not item["passed"]),
        "results": results,
    }
