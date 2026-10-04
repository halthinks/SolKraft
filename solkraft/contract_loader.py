"""Load optional contract.yaml sidecars without loading SKILL.md bodies."""
from __future__ import annotations

from pathlib import Path

import yaml

from .contract_schema import schema_major, validate_v1_document, SUPPORTED_SCHEMA_MAJOR
from .contracts import contract_from_node


MAX_CONTRACT_BYTES = 64_000


def _state(status: str, *, schema_version=None, errors=()) -> dict:
    result = contract_from_node({
        "contract_status": status,
        "schema_version": schema_version,
    })
    result["validation_errors"] = list(errors)
    result["source"] = "sidecar"
    return result


def load_skill_contract(
    entrypoint: Path,
    *,
    legacy_node: dict | None = None,
    expected_skill_id: str | None = None,
) -> dict:
    """Load contract.yaml next to an entrypoint or normalize legacy metadata."""
    sidecar = entrypoint.parent / "contract.yaml"
    if not sidecar.is_file():
        result = contract_from_node(legacy_node)
        result["validation_errors"] = []
        result["source"] = "legacy-graph" if legacy_node else "none"
        return result

    try:
        if sidecar.stat().st_size > MAX_CONTRACT_BYTES:
            return _state("invalid", errors=["contract.yaml exceeds size limit"])
        data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return _state("invalid", errors=[f"contract.yaml could not be parsed: {exc}"])

    if not isinstance(data, dict):
        return _state("invalid", errors=["contract must be a mapping"])

    version = data.get("schema_version")
    major = schema_major(version)
    if major is None:
        return _state("invalid", schema_version=version, errors=["schema_version is invalid"])
    if major != SUPPORTED_SCHEMA_MAJOR:
        return _state("unsupported", schema_version=version)

    errors = validate_v1_document(data, expected_skill_id=expected_skill_id)
    if errors:
        return _state("invalid", schema_version=version, errors=errors)

    normalized = dict(data)
    normalized["contract_status"] = "declared"
    normalized["side_effects"] = list(data.get("effects") or [])
    authority = data.get("authority") or {}
    normalized["auth_scope"] = authority.get("legacy_scope")
    verification = data.get("verification") or {}
    normalized["test_contract"] = (
        verification.get("description")
        or ("Declarative verification checks are present." if verification.get("checks") else None)
    )
    result = contract_from_node(normalized)
    result["validation_errors"] = []
    result["source"] = "sidecar"
    return result
