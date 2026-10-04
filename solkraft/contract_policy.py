"""Structured route policy for contract-aware skill selection.

Policy constrains selection. It never grants runtime authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from .constraint_parser import excluded_effects
from .contracts import AUTH_ORDER, contract_from_node
from .effects import effect_matches, normalize_effects


CONTRACT_MODES = {"legacy", "warn", "strict"}


@dataclass(frozen=True)
class RoutePolicy:
    denied_effects: tuple[str, ...] = ()
    granted_capabilities: frozenset[str] | None = None
    legacy_auth_scope: str | None = None
    contract_mode: str = "legacy"

    def public(self) -> dict:
        return {
            "denied_effects": list(self.denied_effects),
            "granted_capabilities": (
                sorted(self.granted_capabilities)
                if self.granted_capabilities is not None else None
            ),
            "legacy_auth_scope": self.legacy_auth_scope,
            "contract_mode": self.contract_mode,
        }


def _auth_rank(scope: str | None) -> int | None:
    if scope not in AUTH_ORDER:
        return None
    return AUTH_ORDER.index(scope)


def normalize_policy(policy: dict | RoutePolicy | None, objective: str) -> RoutePolicy:
    if isinstance(policy, RoutePolicy):
        base = policy
    else:
        value = policy or {}
        if not isinstance(value, dict):
            raise ValueError("policy must be an object")
        mode = value.get("contract_mode", "legacy")
        if mode not in CONTRACT_MODES:
            raise ValueError("policy.contract_mode must be legacy, warn, or strict")
        legacy_auth = value.get("legacy_auth_scope")
        if legacy_auth is not None and legacy_auth not in AUTH_ORDER:
            raise ValueError("policy.legacy_auth_scope is invalid")
        grants = value.get("granted_capabilities")
        if grants is not None:
            if not isinstance(grants, list) or not all(
                isinstance(item, str) and item for item in grants
            ):
                raise ValueError("policy.granted_capabilities must be a list of strings")
            grants = frozenset(grants)
        denied = value.get("denied_effects", [])
        if not isinstance(denied, list) or not all(
            isinstance(item, str) and item for item in denied
        ):
            raise ValueError("policy.denied_effects must be a list of strings")
        base = RoutePolicy(
            denied_effects=tuple(normalize_effects(denied)),
            granted_capabilities=grants,
            legacy_auth_scope=legacy_auth,
            contract_mode=mode,
        )

    inferred = normalize_effects(excluded_effects(objective))
    denied = tuple(dict.fromkeys([*base.denied_effects, *inferred]))
    return RoutePolicy(
        denied_effects=denied,
        granted_capabilities=base.granted_capabilities,
        legacy_auth_scope=base.legacy_auth_scope,
        contract_mode=base.contract_mode,
    )


def evaluate_contract(contract: dict, policy: RoutePolicy) -> dict:
    reasons = []
    effects = contract.get("side_effects")
    status = contract.get("status", "opaque")

    if status in {"invalid", "unsupported"}:
        reasons.append(f"contract status {status}")
    elif status == "opaque" and policy.contract_mode == "strict":
        reasons.append("opaque contract rejected by strict policy")

    if effects is None and policy.denied_effects:
        reasons.append("undeclared side effects conflict with denied effects")
    else:
        for effect in effects or []:
            for denied in policy.denied_effects:
                if effect_matches(denied, effect):
                    reasons.append(f"effect {effect} denied by policy {denied}")
                    break

    required = set(contract.get("capabilities") or [])
    if policy.granted_capabilities is not None:
        missing = sorted(required - policy.granted_capabilities)
        if missing:
            reasons.append("capabilities not granted: " + ", ".join(missing))

    allowed_rank = _auth_rank(policy.legacy_auth_scope)
    skill_rank = _auth_rank(contract.get("auth_scope"))
    if allowed_rank is not None:
        if skill_rank is None:
            reasons.append("undeclared legacy auth scope exceeds explicit allowance")
        elif skill_rank > allowed_rank:
            reasons.append(
                f"auth scope {contract.get('auth_scope')} exceeds {policy.legacy_auth_scope}"
            )

    decision_status = "denied" if reasons else "allowed"
    if not reasons and status == "opaque":
        decision_status = "opaque"
    elif not reasons and status == "legacy" and policy.contract_mode == "warn":
        decision_status = "legacy-warning"

    return {
        "status": decision_status,
        "contract_status": status,
        "reasons": reasons,
        "effects": list(effects) if effects is not None else None,
        "capabilities": sorted(required),
        "resources": list(contract.get("resources") or []),
        "contract_digest": contract.get("contract_digest"),
        "entrypoint_digest": contract.get("entrypoint_digest"),
    }


def evaluate_graph(graph: dict, objective: str, policy: dict | RoutePolicy | None = None):
    normalized = normalize_policy(policy, objective)
    decisions = {}
    for skill, node in graph.get("nodes", {}).items():
        decisions[skill] = evaluate_contract(contract_from_node(node), normalized)
    return normalized, decisions
