"""Contract-v1 schema helpers."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .effects import validate_effect_id


CONTRACT_SCHEMA_VERSION = "1.0"
SUPPORTED_SCHEMA_MAJOR = 1
SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "skill-contract-v1.json"
CAPABILITY_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")
TOP_LEVEL_FIELDS = {
    "schema_version",
    "skill_id",
    "contract_revision",
    "inputs",
    "outputs",
    "effects",
    "authority",
    "risk",
    "verification",
    "fixtures",
    "provenance",
    "extensions",
}


def schema_major(value) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        head = value.strip().split(".", 1)[0]
        if head.isdigit():
            return int(head)
    return None


def load_contract_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_bindings(name: str, value, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{name} must be a list")
        return
    seen = set()
    for index, item in enumerate(value):
        prefix = f"{name}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        allowed = {"name", "required", "description", "sensitive", "source", "schema"}
        unknown = sorted(set(item) - allowed)
        if unknown:
            errors.append(f"{prefix} has unknown fields: " + ", ".join(unknown))
        binding_name = item.get("name")
        if not isinstance(binding_name, str) or not binding_name:
            errors.append(f"{prefix}.name must be a non-empty string")
        elif binding_name in seen:
            errors.append(f"{name} contains duplicate name {binding_name}")
        else:
            seen.add(binding_name)
        if not isinstance(item.get("schema"), dict):
            errors.append(f"{prefix}.schema must be an object")
        for flag in ("required", "sensitive"):
            if flag in item and not isinstance(item[flag], bool):
                errors.append(f"{prefix}.{flag} must be a boolean")
        if "source" in item and item["source"] not in {
            "user", "context", "artifact", "skill-output", "host"
        }:
            errors.append(f"{prefix}.source is invalid")


def validate_v1_document(data: object, *, expected_skill_id: str | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["contract must be a mapping"]

    errors = []
    unknown = sorted(set(data) - TOP_LEVEL_FIELDS)
    if unknown:
        errors.append("unknown top-level fields: " + ", ".join(unknown))

    if schema_major(data.get("schema_version")) != SUPPORTED_SCHEMA_MAJOR:
        errors.append("schema_version must use major version 1")

    skill_id = data.get("skill_id")
    if not isinstance(skill_id, str) or not skill_id.strip():
        errors.append("skill_id must be a non-empty string")
    elif expected_skill_id and skill_id != expected_skill_id:
        errors.append(f"skill_id {skill_id!r} does not match {expected_skill_id!r}")

    revision = data.get("contract_revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        errors.append("contract_revision must be an integer >= 1")

    _validate_bindings("inputs", data.get("inputs", []), errors)
    _validate_bindings("outputs", data.get("outputs", []), errors)

    effects = data.get("effects", [])
    if not isinstance(effects, list):
        errors.append("effects must be a list")
    else:
        if all(isinstance(item, str) for item in effects) and len(set(effects)) != len(effects):
            errors.append("effects must not contain duplicates")
        for effect in effects:
            if not isinstance(effect, str) or not validate_effect_id(effect):
                errors.append(f"invalid namespaced effect: {effect!r}")

    authority = data.get("authority", {})
    if not isinstance(authority, dict):
        errors.append("authority must be a mapping")
    else:
        unknown_authority = sorted(set(authority) - {"capabilities", "resources", "legacy_scope"})
        if unknown_authority:
            errors.append("authority has unknown fields: " + ", ".join(unknown_authority))
        capabilities = authority.get("capabilities", [])
        if not isinstance(capabilities, list):
            errors.append("authority.capabilities must be a list")
        else:
            if all(isinstance(item, str) for item in capabilities) and len(set(capabilities)) != len(capabilities):
                errors.append("authority.capabilities must not contain duplicates")
            for capability in capabilities:
                if not isinstance(capability, str) or not CAPABILITY_RE.fullmatch(capability):
                    errors.append(f"invalid capability: {capability!r}")
        resources = authority.get("resources", [])
        if not isinstance(resources, list) or not all(
            isinstance(item, str) and item for item in resources
        ):
            errors.append("authority.resources must be a list of non-empty strings")
        legacy_scope = authority.get("legacy_scope")
        if legacy_scope is not None and legacy_scope not in {
            "none", "read", "write-local", "network", "external-effect"
        }:
            errors.append("authority.legacy_scope is invalid")

    risk = data.get("risk", {})
    if not isinstance(risk, dict):
        errors.append("risk must be a mapping")
    else:
        allowed_risk = {"external", "destructive", "idempotent", "reversible", "open_world"}
        unknown_risk = sorted(set(risk) - allowed_risk)
        if unknown_risk:
            errors.append("risk has unknown fields: " + ", ".join(unknown_risk))
        for key, value in risk.items():
            if key in allowed_risk and not isinstance(value, bool):
                errors.append(f"risk.{key} must be a boolean")

    verification = data.get("verification", {})
    if not isinstance(verification, dict):
        errors.append("verification must be a mapping")
    else:
        unknown_verification = sorted(set(verification) - {"description", "mode", "checks"})
        if unknown_verification:
            errors.append("verification has unknown fields: " + ", ".join(unknown_verification))
        if verification.get("mode") not in {None, "declarative"}:
            errors.append("verification.mode must be declarative")
        checks = verification.get("checks", [])
        if not isinstance(checks, list):
            errors.append("verification.checks must be a list")
        else:
            seen_checks = set()
            for index, check in enumerate(checks):
                if not isinstance(check, dict):
                    errors.append(f"verification.checks[{index}] must be an object")
                    continue
                check_id = check.get("id")
                check_type = check.get("type")
                if not isinstance(check_id, str) or not check_id:
                    errors.append(f"verification.checks[{index}].id must be a non-empty string")
                elif check_id in seen_checks:
                    errors.append(f"duplicate verification check id {check_id}")
                else:
                    seen_checks.add(check_id)
                if not isinstance(check_type, str) or not check_type:
                    errors.append(f"verification.checks[{index}].type must be a non-empty string")

    fixtures = data.get("fixtures", {})
    if not isinstance(fixtures, dict):
        errors.append("fixtures must be a mapping")
    else:
        unknown_fixtures = sorted(set(fixtures) - {"selection", "policy"})
        if unknown_fixtures:
            errors.append("fixtures has unknown fields: " + ", ".join(unknown_fixtures))

        selection = fixtures.get("selection", [])
        if not isinstance(selection, list):
            errors.append("fixtures.selection must be a list")
        else:
            seen_fixture_ids = set()
            for index, fixture in enumerate(selection):
                prefix = f"fixtures.selection[{index}]"
                if not isinstance(fixture, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                unknown = sorted(set(fixture) - {
                    "id", "objective", "expected_selected", "context", "policy", "max_skills"
                })
                if unknown:
                    errors.append(f"{prefix} has unknown fields: " + ", ".join(unknown))
                fixture_id = fixture.get("id")
                if not isinstance(fixture_id, str) or not fixture_id:
                    errors.append(f"{prefix}.id must be a non-empty string")
                elif fixture_id in seen_fixture_ids:
                    errors.append(f"duplicate fixture id {fixture_id}")
                else:
                    seen_fixture_ids.add(fixture_id)
                if not isinstance(fixture.get("objective"), str) or not fixture.get("objective", "").strip():
                    errors.append(f"{prefix}.objective must be a non-empty string")
                expected = fixture.get("expected_selected")
                if not isinstance(expected, list) or not all(isinstance(item, str) and item for item in expected):
                    errors.append(f"{prefix}.expected_selected must be a list of skill IDs")
                if "context" in fixture and not isinstance(fixture["context"], dict):
                    errors.append(f"{prefix}.context must be a mapping")
                if "policy" in fixture and not isinstance(fixture["policy"], dict):
                    errors.append(f"{prefix}.policy must be a mapping")
                if "max_skills" in fixture and (
                    not isinstance(fixture["max_skills"], int)
                    or isinstance(fixture["max_skills"], bool)
                    or not 1 <= fixture["max_skills"] <= 50
                ):
                    errors.append(f"{prefix}.max_skills must be an integer from 1 to 50")

        policy_fixtures = fixtures.get("policy", [])
        if not isinstance(policy_fixtures, list):
            errors.append("fixtures.policy must be a list")
        else:
            seen_policy_ids = set()
            for index, fixture in enumerate(policy_fixtures):
                prefix = f"fixtures.policy[{index}]"
                if not isinstance(fixture, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                unknown = sorted(set(fixture) - {
                    "id", "objective", "policy", "expected_status", "reason_contains"
                })
                if unknown:
                    errors.append(f"{prefix} has unknown fields: " + ", ".join(unknown))
                fixture_id = fixture.get("id")
                if not isinstance(fixture_id, str) or not fixture_id:
                    errors.append(f"{prefix}.id must be a non-empty string")
                elif fixture_id in seen_policy_ids:
                    errors.append(f"duplicate fixture id {fixture_id}")
                else:
                    seen_policy_ids.add(fixture_id)
                if "objective" in fixture and (
                    not isinstance(fixture["objective"], str) or not fixture["objective"].strip()
                ):
                    errors.append(f"{prefix}.objective must be a non-empty string")
                if not isinstance(fixture.get("policy"), dict):
                    errors.append(f"{prefix}.policy must be a mapping")
                if fixture.get("expected_status") not in {
                    "allowed", "denied", "opaque", "legacy-warning"
                }:
                    errors.append(f"{prefix}.expected_status is invalid")
                if "reason_contains" in fixture and (
                    not isinstance(fixture["reason_contains"], str) or not fixture["reason_contains"]
                ):
                    errors.append(f"{prefix}.reason_contains must be a non-empty string")

    for field in ("provenance", "extensions"):
        if not isinstance(data.get(field, {}), dict):
            errors.append(f"{field} must be a mapping")

    return errors
