"""Contract-v1 schema helpers.

The JSON Schema is the portable source of truth. These helpers implement the
small amount of validation SolKraft needs without executing skill content.
"""
from __future__ import annotations

import json
from pathlib import Path


CONTRACT_SCHEMA_VERSION = "1.0"
SUPPORTED_SCHEMA_MAJOR = 1
SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "skill-contract-v1.json"
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


def validate_v1_document(data: object, *, expected_skill_id: str | None = None) -> list[str]:
    """Return deterministic structural validation errors for a v1 sidecar."""
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

    for field in ("inputs", "outputs", "effects"):
        value = data.get(field, [])
        if not isinstance(value, list):
            errors.append(f"{field} must be a list")

    effects = data.get("effects", [])
    if isinstance(effects, list) and not all(isinstance(item, str) and item for item in effects):
        errors.append("effects entries must be non-empty strings")

    authority = data.get("authority", {})
    if not isinstance(authority, dict):
        errors.append("authority must be a mapping")
    else:
        for field in ("capabilities", "resources"):
            value = authority.get(field, [])
            if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
                errors.append(f"authority.{field} must be a list of non-empty strings")
        legacy_scope = authority.get("legacy_scope")
        if legacy_scope is not None and legacy_scope not in {
            "none", "read", "write-local", "network", "external-effect"
        }:
            errors.append("authority.legacy_scope is invalid")

    for field in ("risk", "verification", "provenance", "extensions"):
        value = data.get(field, {})
        if not isinstance(value, dict):
            errors.append(f"{field} must be a mapping")

    verification = data.get("verification", {})
    if isinstance(verification, dict):
        checks = verification.get("checks", [])
        if not isinstance(checks, list):
            errors.append("verification.checks must be a list")

    return errors
