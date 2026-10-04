"""Compact skill contract normalization.

The module intentionally contains no route filtering. Admissibility belongs to
contract_policy and route_validation; this file only normalizes declarations.
"""
from __future__ import annotations

from .capabilities import LEGACY_AUTH_SCOPES
from .effects import normalize_effects


CONTRACT_STATUSES = ("declared", "legacy", "opaque", "unsupported", "invalid")
SUPPORTED_SCHEMA_MAJOR = 1


def _schema_major(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        head = value.strip().split(".", 1)[0]
        if head.isdigit():
            return int(head)
    return None


def contract_from_node(node: dict | None) -> dict:
    node = node if isinstance(node, dict) else {}
    forced_status = node.get("contract_status")
    if forced_status not in CONTRACT_STATUSES:
        forced_status = None

    schema_version = node.get("schema_version")
    major = _schema_major(schema_version)
    if schema_version is not None and major is None:
        status = "invalid"
    elif major is not None and major != SUPPORTED_SCHEMA_MAJOR:
        status = "unsupported"
    else:
        status = forced_status

    side = node.get("side_effects")
    if side is None and "effects" in node:
        side = node.get("effects")
    if side is None and node.get("effect") is False:
        side = []
    if isinstance(side, str):
        side = [side]
    if side is not None and not isinstance(side, list):
        status = "invalid"
        side = None
    if isinstance(side, list):
        if not all(isinstance(item, str) and item for item in side):
            status = "invalid"
            side = None
        else:
            side = normalize_effects(side)

    auth = node.get("auth_scope")
    authority = node.get("authority")
    if auth is None and isinstance(authority, dict):
        auth = authority.get("legacy_scope")
    if auth is None and node.get("effect") is False and forced_status != "declared":
        auth = "none"
    if auth is not None and auth not in LEGACY_AUTH_SCOPES:
        status = "invalid"
        auth = None

    test = node.get("test_contract") or node.get("exit_evidence")
    verification = node.get("verification")
    if not test and isinstance(verification, dict):
        test = verification.get("description")
        if not test and verification.get("checks"):
            test = "Declarative verification checks are present."

    capabilities = []
    resources = []
    if isinstance(authority, dict):
        capabilities = list(authority.get("capabilities") or [])
        resources = list(authority.get("resources") or [])

    if status is None:
        explicit_contract = any(
            key in node for key in (
                "schema_version", "side_effects", "effects", "auth_scope",
                "test_contract", "verification", "authority",
            )
        )
        legacy_contract = any(key in node for key in ("effect", "exit_evidence"))
        if explicit_contract:
            status = "declared"
        elif legacy_contract:
            status = "legacy"
        else:
            status = "opaque"

    return {
        "status": status,
        "schema_version": schema_version,
        "contract_revision": node.get("contract_revision"),
        "inputs": list(node.get("inputs") or []),
        "outputs": list(node.get("outputs") or []),
        "side_effects": list(side) if side is not None else None,
        "auth_scope": auth,
        "capabilities": capabilities,
        "resources": resources,
        "test_contract": test,
        "verification": dict(verification) if isinstance(verification, dict) else {},
        "risk": dict(node.get("risk") or {}) if isinstance(node.get("risk"), dict) else {},
        "provenance": dict(node.get("provenance") or {}) if isinstance(node.get("provenance"), dict) else {},
        "trust": dict(node.get("trust") or {}) if isinstance(node.get("trust"), dict) else {},
        "contract_digest": node.get("contract_digest"),
        "entrypoint_digest": node.get("entrypoint_digest"),
        "declared": status in {"declared", "legacy"},
    }
