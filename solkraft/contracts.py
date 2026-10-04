"""Compact skill contracts used as selection constraints.

A contract is metadata: inputs, side effects, auth scope, and a test contract.
It is never loaded as a procedure and never grants execution authority.
Undeclared skills stay selectable but are marked opaque. Declared conflicts
are rejected before the host fetches a SKILL.md body.
"""
from __future__ import annotations

import re


EFFECTS = (
    "merge", "publish", "deploy", "send", "purchase",
    "fabricate", "delete", "revoke", "rotate", "push",
)
# Ordered from least to most authority. A route may allow a scope and every
# scope below it. External effects are never implied by a lower scope.
AUTH_ORDER = ("none", "read", "write-local", "network", "external-effect")
_EFFECT_FORMS = {
    "merge": r"merg(?:e|ing|ed)?",
    "publish": r"publish(?:ing|ed|es)?",
    "deploy": r"deploy(?:ing|ed|s)?",
    "send": r"send|sending|sent",
    "purchase": r"purchas(?:e|ing|ed)",
    "fabricate": r"fabricat(?:e|ing|ed|ion)?",
    "delete": r"delet(?:e|ing|ed)",
    "revoke": r"revok(?:e|ing|ed)",
    "rotate": r"rotat(?:e|ing|ed)",
    "push": r"push(?:ing|ed|es)?",
}


def excluded_effects(objective: str) -> list[str]:
    """Return effects the objective explicitly forbids. Quotes stay inert."""
    visible = re.sub(r"```[\s\S]*?```|`[^`\n]*`|\"[^\"\n]*\"|'[^'\n]*'", " ", objective.casefold())
    found = []
    for effect, form in _EFFECT_FORMS.items():
        pattern = rf"\b(?:do not|don't|dont|without|never|skip|avoid)\b[^.;\n]{{0,70}}\b(?:{form})\b"
        match = re.search(pattern, visible)
        if match:
            found.append((match.start(), effect))
    return [effect for _, effect in sorted(found)]


def _auth_rank(scope: str | None) -> int | None:
    if scope not in AUTH_ORDER:
        return None
    return AUTH_ORDER.index(scope)


def contract_from_node(node: dict) -> dict:
    """Read a contract from graph metadata. Missing fields stay undeclared."""
    side = node.get("side_effects")
    if side is None and node.get("effect") is False:
        side = []
    if isinstance(side, str):
        side = [side]
    auth = node.get("auth_scope")
    if auth is None and node.get("effect") is False:
        auth = "none"
    test = node.get("test_contract") or node.get("exit_evidence")
    inputs = list(node.get("inputs") or [])
    declared = side is not None and auth in AUTH_ORDER and bool(test)
    return {
        "inputs": inputs,
        "side_effects": list(side) if side is not None else None,
        "auth_scope": auth if auth in AUTH_ORDER else None,
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
    if contract["auth_scope"] == "external-effect" and excluded:
        reasons.append("external-effect scope conflicts with an effect exclusion")
    if contract["side_effects"] is None and excluded:
        reasons.append("undeclared side effects conflict with an effect exclusion")
    allowed_rank = _auth_rank(allowed_auth)
    skill_rank = _auth_rank(contract["auth_scope"])
    if allowed_rank is not None and skill_rank is not None and skill_rank > allowed_rank:
        reasons.append(f"auth scope {contract['auth_scope']} exceeds {allowed_auth}")
    if allowed_rank is not None and contract["auth_scope"] is None:
        reasons.append("undeclared auth scope exceeds an explicit allowance")
    return reasons


def apply_contracts(result: dict, graph: dict, objective: str, allowed_auth: str | None = None) -> dict:
    """Drop selected skills whose declared contract conflicts with the request.

    The composer still chooses order and method. This pass only removes skills
    that cannot legally sit on the route, and attaches the test contract so the
    host can verify a stage without loading the procedure body.
    """
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
    for stage in result.get("stages", []):
        stage["selected"] = [skill for skill in stage.get("selected", []) if skill not in rejected_ids]
    if "skills" in result:
        result["skills"] = [item for item in result["skills"] if item.get("id") in contracts]
    result["selected"] = selected
    result["contracts"] = contracts
    result["contract_rejections"] = rejected
    result["excluded_effects"] = sorted(excluded)
    result["selection_status"] = "matched" if selected else "abstained"
    result["execution_authorized"] = False
    return result
