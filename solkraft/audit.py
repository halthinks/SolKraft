"""Deterministic audit receipts for route and verification decisions."""
from __future__ import annotations

import hashlib
import json


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def route_audit_event(result: dict) -> dict:
    contracts = {}
    for skill, decision in (result.get("contract_decisions") or {}).items():
        contracts[skill] = {
            "status": decision.get("contract_status"),
            "trust": decision.get("trust"),
            "contract_digest": decision.get("contract_digest"),
            "entrypoint_digest": decision.get("entrypoint_digest"),
        }
    payload = {
        "objective": result.get("objective"),
        "selected": list(result.get("selected") or []),
        "selection_status": result.get("selection_status"),
        "policy": result.get("route_policy"),
        "contracts": contracts,
        "required_capabilities": list(result.get("required_capabilities") or []),
        "required_resources": list(result.get("required_resources") or []),
        "blocked_stages": list(result.get("blocked_stages") or []),
    }
    return {
        "schema": "solkraft/audit/route/v1",
        "digest": digest(payload),
        "payload": payload,
        "execution_authorized": False,
    }


def verification_audit_event(skill_id: str, verification: dict) -> dict:
    evidence = verification.get("evidence") or {}
    payload = {
        "skill_id": skill_id,
        "state": verification.get("state"),
        "passed": verification.get("passed"),
        "contract_digest": evidence.get("contract_digest"),
        "entrypoint_digest": evidence.get("entrypoint_digest"),
        "evidence_digest": evidence.get("evidence_digest"),
        "checks": verification.get("checks") or [],
    }
    return {
        "schema": "solkraft/audit/verification/v1",
        "digest": digest(payload),
        "payload": payload,
    }
