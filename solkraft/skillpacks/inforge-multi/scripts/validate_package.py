#!/usr/bin/env python3
"""Validate an InForge private audit package and its final transposed prompt."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from verify_bundle import verify


GATE = "Before performing any state-changing or externally consequential action, present the transposed scope, deliverables, acceptance criteria, and irreversible or external effects to the user and obtain explicit confirmation."
RISK_CATEGORIES = {
    "destructive_or_irreversible",
    "external_side_effect",
    "production_or_deployment",
    "security_or_privileged_access",
    "credentials_or_sensitive_data",
    "financial_commitment",
    "legal_medical_financial_reliance",
    "broad_scope_state_change",
}
AUTH_BASES = {"user_explicit", "higher_priority_policy", "derived_nonexpansive", "not_applicable"}
FEASIBILITY_STATUSES = {"verified", "assumption", "unknown"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def id_objects(record: dict, field: str, errors: list[str]) -> list[dict]:
    value = record.get(field)
    if not isinstance(value, list):
        errors.append(f"intent_record.{field} must be a list")
        return []
    seen: set[str] = set()
    result: list[dict] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict) or not nonempty(item.get("id")) or not nonempty(item.get("text")):
            errors.append(f"intent_record.{field}[{index}] must have nonempty id and text")
            continue
        if item["id"] in seen:
            errors.append(f"duplicate requirement id {item['id']}")
        seen.add(item["id"])
        result.append(item)
    return result


def expected_provenance(manifest: dict) -> str:
    return (
        "InForge provenance: "
        f"profile={manifest['profile']}; "
        f"control_version={manifest['control_version']}; "
        f"source_version={manifest['source_version']}; "
        f"source_sha256={manifest['source_sha256']}; "
        f"contract_sha256={manifest['contract_sha256']}; "
        "execution_boundary=transpose_only"
    )


def validate_package(package: dict, root: Path) -> list[str]:
    errors = verify(root)
    manifest = json.loads((root / "references" / "manifest.json").read_text(encoding="utf-8"))

    for field in ("profile", "control_version", "source_version", "source_sha256", "contract_sha256"):
        if package.get(field) != manifest.get(field):
            errors.append(f"{field} must match manifest")
    if package.get("execution_boundary") != "transpose_only":
        errors.append("execution_boundary must be transpose_only")

    prompt = package.get("prompt")
    if not nonempty(prompt):
        errors.append("prompt must be nonempty")
        prompt = ""

    record = package.get("intent_record")
    if not isinstance(record, dict):
        errors.append("intent_record must be an object")
        record = {}
    if not nonempty(record.get("objective")):
        errors.append("intent_record.objective must be nonempty")
    for field in ("scope", "inputs", "assumptions", "authorization_boundaries"):
        value = record.get(field)
        if not isinstance(value, list) or any(not nonempty(x) for x in value):
            errors.append(f"intent_record.{field} must be a list of nonempty strings")
    if not nonempty(record.get("search_policy")):
        errors.append("intent_record.search_policy must be nonempty")

    requirement_objects: list[dict] = []
    for field in ("constraints", "deliverables", "acceptance_criteria", "unacceptable_partial_outcomes"):
        requirement_objects.extend(id_objects(record, field, errors))
    requirement_ids = {item["id"] for item in requirement_objects}

    roles = package.get("role_map")
    if not isinstance(roles, list):
        errors.append("role_map must be a list")
        roles = []
    by_role: dict[str, dict] = {}
    covered: set[str] = set()
    for index, role in enumerate(roles):
        if not isinstance(role, dict) or not nonempty(role.get("source_role_id")):
            errors.append(f"role_map[{index}] missing source_role_id")
            continue
        role_id = role["source_role_id"]
        if role_id in by_role:
            errors.append(f"duplicate source role {role_id}")
        by_role[role_id] = role
        status = role.get("status")
        if status not in ("mapped", "not_applicable"):
            errors.append(f"{role_id} has invalid status")
        if role.get("authorization_basis") not in AUTH_BASES:
            errors.append(f"{role_id} has invalid authorization_basis")
        if not nonempty(role.get("source_function")):
            errors.append(f"{role_id} missing source_function")
        if not nonempty(role.get("feasibility_basis")):
            errors.append(f"{role_id} missing feasibility_basis")
        if not nonempty(role.get("search_policy_basis")):
            errors.append(f"{role_id} missing search_policy_basis")
        ids = role.get("requirement_ids")
        if not isinstance(ids, list) or any(x not in requirement_ids for x in ids):
            errors.append(f"{role_id} has invalid requirement_ids")
        else:
            covered.update(ids)
        if status == "mapped":
            evidence = role.get("prompt_evidence")
            if not nonempty(role.get("task_expression")) or not nonempty(evidence):
                errors.append(f"{role_id} mapped role needs task_expression and prompt_evidence")
            elif evidence not in prompt:
                errors.append(f"{role_id} prompt_evidence not found exactly in prompt")
        elif not nonempty(role.get("justification")):
            errors.append(f"{role_id} not_applicable role needs justification")

    expected_roles = set(manifest.get("required_role_ids", []))
    actual_roles = set(by_role)
    if actual_roles != expected_roles:
        errors.append(f"role coverage mismatch: missing={sorted(expected_roles-actual_roles)} extra={sorted(actual_roles-expected_roles)}")
    if covered != requirement_ids:
        errors.append(f"requirement coverage mismatch: uncovered={sorted(requirement_ids-covered)}")

    omitted = package.get("omitted_requirement_ids")
    if omitted != []:
        errors.append("omitted_requirement_ids must be an empty list")
    added = package.get("added_permissions")
    if added != []:
        errors.append("added_permissions must be an empty list")

    claims = package.get("feasibility_claims")
    if not isinstance(claims, list):
        errors.append("feasibility_claims must be a list")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict) or not nonempty(claim.get("claim")) or not nonempty(claim.get("basis")) or claim.get("status") not in FEASIBILITY_STATUSES:
                errors.append(f"feasibility_claims[{index}] is invalid")

    risks = record.get("risk_categories")
    if not isinstance(risks, list) or any(risk not in RISK_CATEGORIES for risk in risks) or len(set(risks or [])) != len(risks or []):
        errors.append("intent_record.risk_categories is invalid")
        risks = []
    high = bool(risks)
    if record.get("high_consequence") is not high:
        errors.append("high_consequence must equal whether risk_categories is nonempty")
    if record.get("confirmation_required") is not high:
        errors.append("confirmation_required must equal high_consequence")
    if high and GATE not in prompt:
        errors.append("high-consequence prompt is missing the exact confirmation gate")
    if not high and GATE in prompt:
        errors.append("low-consequence prompt must not include the confirmation gate")

    provenance = expected_provenance(manifest)
    if not prompt.rstrip().endswith(provenance):
        errors.append("prompt must end with exact manifest-derived provenance")

    structural = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_transposition.py"), "--mode", manifest["profile"]],
        input=prompt,
        text=True,
        capture_output=True,
    )
    if structural.returncode:
        errors.append("structural validation failed: " + structural.stderr.strip().replace("\n", "; "))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    package = json.loads(Path(args.package).read_text(encoding="utf-8"))
    errors = validate_package(package, root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("InForge audit package is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
