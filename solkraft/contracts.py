"""Compact skill contracts used as selection constraints.

Contracts describe a skill. They never grant execution authority. Missing or
unsupported metadata stays explicit so SolKraft cannot accidentally turn
unknown into safe.
"""
from __future__ import annotations

from .constraint_parser import excluded_effects


AUTH_ORDER = ("none", "read", "write-local", "network", "external-effect")
CONTRACT_STATUSES = ("declared", "legacy", "opaque", "unsupported", "invalid")
SUPPORTED_SCHEMA_MAJOR = 1


def _auth_rank(scope: str | None) -> int | None:
    if scope not in AUTH_ORDER:
        return None
    return AUTH_ORDER.index(scope)


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
    """Normalize graph or sidecar metadata into one compact contract view."""
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
    if isinstance(side, list) and not all(isinstance(item, str) and item for item in side):
        status = "invalid"
        side = None

    auth = node.get("auth_scope")
    if auth is None:
        authority = node.get("authority")
        if isinstance(authority, dict):
            auth = authority.get("legacy_scope")
    if auth is None and node.get("effect") is False:
        auth = "none"
    if auth is not None and auth not in AUTH_ORDER:
        status = "invalid"
        auth = None

    test = node.get("test_contract") or node.get("exit_evidence")
    verification = node.get("verification")
    if not test and isinstance(verification, dict):
        test = verification.get("description")
        if not test and verification.get("checks"):
            test = "Declarative verification checks are present."

    inputs = list(node.get("inputs") or [])
    outputs = list(node.get("outputs") or [])
    capabilities = []
    resources = []
    authority = node.get("authority")
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

    declared = status in {"declared", "legacy"}
    return {
        "status": status,
        "schema_version": schema_version,
        "contract_revision": node.get("contract_revision"),
        "inputs": inputs,
        "outputs": outputs,
        "side_effects": list(side) if side is not None else None,
        "auth_scope": auth,
        "capabilities": capabilities,
        "resources": resources,
        "test_contract": test,
        "declared": declared,
    }


def _rejection(skill: str, contract: dict, reasons: list[str]) -> dict:
    return {"id": skill, "reasons": reasons, "contract": contract}


def violates(contract: dict, excluded: set[str], allowed_auth: str | None) -> list[str]:
    reasons = []
    declared_effects = set(contract["side_effects"] or [])
    if declared_effects & excluded:
        reasons.append("side effect excluded: " + ", ".join(sorted(declared_effects & excluded)))
    if contract["side_effects"] is None and excluded:
        reasons.append("undeclared side effects conflict with an effect exclusion")
    allowed_rank = _auth_rank(allowed_auth)
    skill_rank = _auth_rank(contract["auth_scope"])
    if allowed_rank is not None and skill_rank is not None and skill_rank > allowed_rank:
        reasons.append(f"auth scope {contract['auth_scope']} exceeds {allowed_auth}")
    if allowed_rank is not None and contract["auth_scope"] is None:
        reasons.append("undeclared auth scope exceeds an explicit allowance")
    return reasons


def apply_contracts(
    result: dict,
    graph: dict,
    objective: str,
    allowed_auth: str | None = None,
) -> dict:
    """Filter conflicting skills and make route breakage explicit."""
    if allowed_auth is not None and allowed_auth not in AUTH_ORDER:
        raise ValueError("Unknown auth scope: " + str(allowed_auth))
    excluded = set(excluded_effects(objective))
    nodes = graph.get("nodes", {})
    rejected = []
    selected = []
    contracts = {}

    for skill in result.get("selected", []):
        contract = contract_from_node(nodes.get(skill, {}))
        reasons = violates(contract, excluded, allowed_auth)
        if reasons:
            rejected.append(_rejection(skill, contract, reasons))
            continue
        selected.append(skill)
        contracts[skill] = contract

    rejected_ids = {item["id"] for item in rejected}
    blocked_stages = []
    for stage in result.get("stages", []):
        before = list(stage.get("selected", []))
        stage["selected"] = [skill for skill in before if skill not in rejected_ids]
        removed = [skill for skill in before if skill in rejected_ids]
        if before and not stage["selected"] and removed:
            blocked_stages.append({
                "stage": stage.get("stage"),
                "text": stage.get("text"),
                "reason": "all selected skills rejected by contract constraints",
                "rejected": removed,
            })

    if "skills" in result:
        result["skills"] = [item for item in result["skills"] if item.get("id") in contracts]
    result["selected"] = selected
    result["contracts"] = contracts
    result["contract_rejections"] = rejected
    result["blocked_stages"] = blocked_stages
    result["excluded_effects"] = sorted(excluded)

    if blocked_stages or (rejected and not selected):
        result["selection_status"] = "partially_blocked" if selected else "blocked"
    else:
        result["selection_status"] = "matched" if selected else "abstained"
    result["execution_authorized"] = False
    return result
