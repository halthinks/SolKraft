"""Load optional contract.yaml sidecars without loading SKILL.md bodies."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from .contract_schema import schema_major, validate_v1_document, SUPPORTED_SCHEMA_MAJOR
from .contracts import contract_from_node
from .effects import normalize_effects


MAX_CONTRACT_BYTES = 64_000


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _entrypoint_digest(entrypoint: Path) -> str | None:
    try:
        return _digest(entrypoint.read_bytes())
    except OSError:
        return None


def _state(status: str, *, schema_version=None, errors=(), entrypoint_digest=None) -> dict:
    result = contract_from_node({
        "contract_status": status,
        "schema_version": schema_version,
        "entrypoint_digest": entrypoint_digest,
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
    sidecar = entrypoint.parent / "contract.yaml"
    entry_digest = _entrypoint_digest(entrypoint)
    if not sidecar.is_file():
        source = dict(legacy_node or {})
        source["entrypoint_digest"] = entry_digest
        result = contract_from_node(source)
        result["validation_errors"] = []
        result["source"] = "legacy-graph" if legacy_node else "none"
        result["contract_digest"] = None
        return result

    try:
        if sidecar.stat().st_size > MAX_CONTRACT_BYTES:
            return _state(
                "invalid",
                errors=["contract.yaml exceeds size limit"],
                entrypoint_digest=entry_digest,
            )
        data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return _state(
            "invalid",
            errors=[f"contract.yaml could not be parsed: {exc}"],
            entrypoint_digest=entry_digest,
        )

    if not isinstance(data, dict):
        return _state(
            "invalid",
            errors=["contract must be a mapping"],
            entrypoint_digest=entry_digest,
        )

    version = data.get("schema_version")
    major = schema_major(version)
    if major is None:
        return _state(
            "invalid",
            schema_version=version,
            errors=["schema_version is invalid"],
            entrypoint_digest=entry_digest,
        )
    if major != SUPPORTED_SCHEMA_MAJOR:
        return _state(
            "unsupported",
            schema_version=version,
            entrypoint_digest=entry_digest,
        )

    errors = validate_v1_document(data, expected_skill_id=expected_skill_id)
    if errors:
        return _state(
            "invalid",
            schema_version=version,
            errors=errors,
            entrypoint_digest=entry_digest,
        )

    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    contract_digest = _digest(canonical.encode("utf-8"))

    normalized = dict(data)
    provenance = data.get("provenance") or {}
    normalized["contract_status"] = (
        "legacy" if provenance.get("inferred") is True else "declared"
    )
    normalized["side_effects"] = normalize_effects(data.get("effects") or [])
    authority = data.get("authority") or {}
    normalized["auth_scope"] = authority.get("legacy_scope")
    normalized["entrypoint_digest"] = entry_digest
    normalized["contract_digest"] = contract_digest
    verification = data.get("verification") or {}
    normalized["test_contract"] = (
        verification.get("description")
        or ("Declarative verification checks are present." if verification.get("checks") else None)
    )
    result = contract_from_node(normalized)
    result["validation_errors"] = []
    result["source"] = "sidecar"
    result["verification"] = verification
    result["risk"] = dict(data.get("risk") or {})
    result["provenance"] = dict(data.get("provenance") or {})
    result["extensions"] = dict(data.get("extensions") or {})
    return result
