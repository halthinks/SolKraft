"""Portable contract metadata import/export.

Portable documents carry declarations only. Import never creates trust,
credentials, runtime grants, or execution authorization.
"""
from __future__ import annotations

import copy
import json

from .contract_schema import validate_v1_document
from .contract_verify import SUPPORTED_CHECKS


PORTABLE_SCHEMA = "solkraft/portable-contract/v1"


def export_portable_contract(entry: dict) -> dict:
    """Export compact contract metadata without a SKILL.md body."""
    return {
        "schema": PORTABLE_SCHEMA,
        "skill_id": entry.get("id") or entry.get("skill_id"),
        "contract": {
            "schema_version": entry.get("schema_version") or "1.0",
            "skill_id": entry.get("id") or entry.get("skill_id"),
            "contract_revision": entry.get("contract_revision") or 1,
            "inputs": copy.deepcopy(entry.get("inputs") or []),
            "outputs": copy.deepcopy(entry.get("outputs") or []),
            "effects": copy.deepcopy(entry.get("effects") or []),
            "authority": {
                "capabilities": copy.deepcopy(entry.get("capabilities") or []),
                "resources": copy.deepcopy(entry.get("resources") or []),
            },
            "risk": copy.deepcopy(entry.get("risk") or {}),
            "verification": copy.deepcopy(entry.get("verification") or {}),
            "provenance": {
                **copy.deepcopy(entry.get("provenance") or {}),
                "portable_export": True,
            },
            "extensions": {
                "solkraft_export": {
                    "source_status": entry.get("status"),
                    "source_trust": (entry.get("trust") or {}).get("state"),
                    "contract_digest": entry.get("contract_digest"),
                    "entrypoint_digest": entry.get("entrypoint_digest"),
                }
            },
        },
        "authority_granted": False,
        "execution_authorized": False,
    }


def import_portable_contract(document: object) -> dict:
    """Validate portable metadata and return an untrusted declaration."""
    if not isinstance(document, dict):
        raise ValueError("portable contract must be an object")
    if document.get("schema") != PORTABLE_SCHEMA:
        raise ValueError("unsupported portable contract schema")
    contract = copy.deepcopy(document.get("contract"))
    errors = validate_v1_document(contract)
    if errors:
        raise ValueError("; ".join(errors))
    verification = contract.get("verification") or {}
    unsupported = [
        check.get("type")
        for check in verification.get("checks") or []
        if isinstance(check, dict) and check.get("type") not in SUPPORTED_CHECKS
    ]
    if unsupported:
        raise ValueError("unsupported verification types: " + ", ".join(map(str, unsupported)))
    provenance = dict(contract.get("provenance") or {})
    provenance["portable_import"] = True
    contract["provenance"] = provenance
    return {
        "contract": contract,
        "contract_status": "declared",
        "trust": {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "portable import is a declaration, not a trust grant",
        },
        "authority_granted": False,
        "execution_authorized": False,
    }


def dumps_portable_contract(entry: dict) -> str:
    return json.dumps(export_portable_contract(entry), indent=2, ensure_ascii=False) + "\n"
