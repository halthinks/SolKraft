"""Declarative contract verification over externally supplied evidence.

Core SolKraft never executes a command from a contract. Verification consumes
structured evidence and evaluates a small, explicit check vocabulary.
"""
from __future__ import annotations

from .evidence import normalize_evidence
from .effects import normalize_effects


SUPPORTED_CHECKS = {
    "artifact_exists",
    "field_present",
    "field_equals",
    "check_equals",
    "observed_effects_subset",
}


def _field_get(fields: dict, path: str):
    current = fields
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _check_artifact_exists(check: dict, evidence: dict):
    name = check.get("artifact") or check.get("name")
    if not isinstance(name, str) or not name:
        return False, "artifact_exists requires artifact"
    names = {item.get("name") for item in evidence["artifacts"]}
    return name in names, f"artifact {name!r} was not present"


def _check_field_present(check: dict, evidence: dict):
    field = check.get("field")
    if not isinstance(field, str) or not field:
        return False, "field_present requires field"
    present, _ = _field_get(evidence["fields"], field)
    return present, f"field {field!r} was not present"


def _check_field_equals(check: dict, evidence: dict):
    field = check.get("field")
    if not isinstance(field, str) or not field:
        return False, "field_equals requires field"
    present, actual = _field_get(evidence["fields"], field)
    if not present:
        return False, f"field {field!r} was not present"
    expected = check.get("expected")
    return actual == expected, f"field {field!r} did not equal expected value"


def _check_check_equals(check: dict, evidence: dict):
    key = check.get("check")
    if not isinstance(key, str) or not key:
        return False, "check_equals requires check"
    if key not in evidence["checks"]:
        return False, f"host check {key!r} was not present"
    expected = check.get("expected", True)
    return evidence["checks"][key] == expected, f"host check {key!r} did not match"


def _check_observed_effects_subset(check: dict, evidence: dict, contract: dict):
    allowed = set(normalize_effects(contract.get("side_effects") or []))
    observed = set(evidence["observed_effects"])
    unexpected = sorted(observed - allowed)
    return not unexpected, (
        "unexpected observed effects: " + ", ".join(unexpected)
        if unexpected else ""
    )


def verify_contract(contract: dict, evidence: object) -> dict:
    normalized, errors = normalize_evidence(evidence)
    if errors:
        return {
            "state": "verification-failed",
            "passed": False,
            "errors": errors,
            "checks": [],
            "evidence": normalized,
        }

    binding_errors = []
    if normalized["contract_digest"] != contract.get("contract_digest"):
        binding_errors.append("evidence contract digest does not match selected contract")
    if normalized["entrypoint_digest"] != contract.get("entrypoint_digest"):
        binding_errors.append("evidence entrypoint digest does not match selected procedure")
    if binding_errors:
        return {
            "state": "verification-failed",
            "passed": False,
            "errors": binding_errors,
            "checks": [],
            "evidence": normalized,
        }

    verification = contract.get("verification") or {}
    checks = verification.get("checks") or []
    if not checks:
        return {
            "state": "executed-unverified",
            "passed": False,
            "errors": [],
            "checks": [],
            "evidence": normalized,
        }

    results = []
    for check in checks:
        check_type = check.get("type")
        if check_type not in SUPPORTED_CHECKS:
            results.append({
                "id": check.get("id"),
                "type": check_type,
                "passed": False,
                "reason": f"unsupported declarative check type: {check_type}",
            })
            continue

        if check_type == "artifact_exists":
            passed, reason = _check_artifact_exists(check, normalized)
        elif check_type == "field_present":
            passed, reason = _check_field_present(check, normalized)
        elif check_type == "field_equals":
            passed, reason = _check_field_equals(check, normalized)
        elif check_type == "check_equals":
            passed, reason = _check_check_equals(check, normalized)
        else:
            passed, reason = _check_observed_effects_subset(check, normalized, contract)

        results.append({
            "id": check.get("id"),
            "type": check_type,
            "passed": passed,
            "reason": "" if passed else reason,
        })

    passed = bool(results) and all(item["passed"] for item in results)
    return {
        "state": "verified" if passed else "verification-failed",
        "passed": passed,
        "errors": [],
        "checks": results,
        "evidence": normalized,
    }
