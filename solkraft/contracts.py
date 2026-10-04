"""Skill contracts are the facts used to choose a skill.

A usable contract states four things: inputs, side effects, auth scope, and a
test contract. Automatic selection ignores a skill that does not state them.
An explicit request can still name that skill, and the route marks it
undeclared. This module never runs a skill.
"""
from __future__ import annotations

import re


EFFECTS = (
    "merge", "publish", "deploy", "send", "purchase",
    "fabricate", "delete", "revoke", "rotate", "push",
)
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
    """Return effects the request text says not to do. Quoted text is ignored."""
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


def _as_list(value) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) and item.strip() for item in value):
        return None
    return [item.strip() for item in value]


def contract_from_declaration(raw: dict | None) -> dict:
    """Build a contract only from fields a skill actually stated."""
    raw = raw or {}
    inputs = _as_list(raw.get("inputs"))
    side = _as_list(raw.get("side_effects"))
    auth = raw.get("auth_scope")
    test = raw.get("test_contract")
    if not isinstance(test, str) or not test.strip():
        test = None
    else:
        test = " ".join(test.split())
    declared = inputs is not None and side is not None and auth in AUTH_ORDER and test is not None
    return {
        "inputs": inputs or [],
        "side_effects": side,
        "auth_scope": auth if auth in AUTH_ORDER else None,
        "test_contract": test,
        "declared": declared,
    }


def contract_from_node(node: dict) -> dict:
    """Read a stated contract. A read-only graph node already states the four facts."""
    stated = {
        "inputs": node.get("inputs"),
        "side_effects": node.get("side_effects"),
        "auth_scope": node.get("auth_scope"),
        "test_contract": node.get("test_contract") or node.get("exit_evidence"),
    }
    if stated["side_effects"] is None and node.get("effect") is False:
        stated["side_effects"] = []
    if stated["auth_scope"] is None and node.get("effect") is False:
        stated["auth_scope"] = "none"
    return contract_from_declaration(stated)


def merge_contract(node: dict, frontmatter: dict | None) -> dict:
    """Frontmatter wins. Graph fields fill only what the skill did not state."""
    base = contract_from_node(node)
    stated = contract_from_declaration(frontmatter)
    if not frontmatter:
        return base
    merged = {
        "inputs": frontmatter.get("inputs", base["inputs"]),
        "side_effects": frontmatter.get("side_effects", base["side_effects"]),
        "auth_scope": frontmatter.get("auth_scope", base["auth_scope"]),
        "test_contract": frontmatter.get("test_contract", base["test_contract"]),
    }
    return contract_from_declaration(merged)


def violates(contract: dict, excluded: set[str], allowed_auth: str | None) -> list[str]:
    reasons = []
    if not contract["declared"]:
        reasons.append("skill did not state inputs, side effects, auth scope, and a test contract")
        return reasons
    declared_effects = set(contract["side_effects"] or [])
    if declared_effects & excluded:
        reasons.append("request says not to " + ", ".join(sorted(declared_effects & excluded)))
    allowed_rank = _auth_rank(allowed_auth)
    skill_rank = _auth_rank(contract["auth_scope"])
    if allowed_rank is not None and skill_rank is not None and skill_rank > allowed_rank:
        reasons.append(f"auth scope {contract['auth_scope']} is above {allowed_auth}")
    return reasons


def apply_contracts(result: dict, graph: dict, objective: str, allowed_auth: str | None = None,
                    frontmatter: dict | None = None, explicit: tuple | list = ()) -> dict:
    """Keep automatic picks only when the skill stated a usable contract."""
    if allowed_auth is not None and allowed_auth not in AUTH_ORDER:
        raise ValueError("Unknown auth scope: " + str(allowed_auth))
    excluded = set(excluded_effects(objective))
    nodes = graph.get("nodes", {})
    frontmatter = frontmatter or {}
    explicit_ids = set(explicit)
    rejected = []
    selected = []
    contracts = {}
    for skill in result.get("selected", []):
        contract = merge_contract(nodes.get(skill, {}), frontmatter.get(skill))
        reasons = violates(contract, excluded, allowed_auth)
        if reasons and skill not in explicit_ids:
            rejected.append({"id": skill, "reasons": reasons, "contract": contract})
            continue
        if reasons and skill in explicit_ids:
            contract = {**contract, "explicit_undeclared": True}
        selected.append(skill)
        contracts[skill] = contract
    rejected_ids = {item["id"] for item in rejected}
    for stage in result.get("stages", []):
        stage["selected"] = [skill for skill in stage.get("selected", []) if skill not in rejected_ids]
    result["selected"] = selected
    result["contracts"] = contracts
    result["contract_rejections"] = rejected
    result["excluded_effects"] = sorted(excluded)
    result["selection_status"] = "matched" if selected else "abstained"
    result["execution_authorized"] = False
    return result
