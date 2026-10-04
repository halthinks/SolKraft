"""Structured route policy for contract-aware skill selection.

Policy constrains selection. It never grants runtime authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from .capabilities import (
    LEGACY_AUTH_SCOPES,
    CapabilityGrant,
    legacy_scope_allows,
    missing_capabilities,
    missing_resources,
    normalize_grant,
)
from .constraint_parser import excluded_effects
from .contracts import contract_from_node
from .effects import effect_matches, normalize_effects


CONTRACT_MODES = {"legacy", "warn", "strict", "hardened"}


@dataclass(frozen=True)
class RoutePolicy:
    denied_effects: tuple[str, ...] = ()
    grant: CapabilityGrant | None = None
    legacy_auth_scope: str | None = None
    contract_mode: str = "legacy"

    @property
    def granted_capabilities(self):
        return self.grant.capabilities if self.grant else None

    @property
    def granted_resources(self):
        return self.grant.resources if self.grant else None

    def public(self) -> dict:
        return {
            "denied_effects": list(self.denied_effects),
            "grant": self.grant.public() if self.grant else None,
            "granted_capabilities": (
                sorted(self.grant.capabilities) if self.grant else None
            ),
            "granted_resources": (
                sorted(self.grant.resources) if self.grant else None
            ),
            "legacy_auth_scope": self.legacy_auth_scope,
            "contract_mode": self.contract_mode,
        }


def _flat_grant(value: dict) -> CapabilityGrant | None:
    capabilities = value.get("granted_capabilities")
    resources = value.get("granted_resources")
    if capabilities is None and resources is None:
        return None
    capabilities = capabilities or []
    resources = resources or []
    if not isinstance(capabilities, list) or not all(
        isinstance(item, str) and item for item in capabilities
    ):
        raise ValueError("policy.granted_capabilities must be a list of strings")
    if not isinstance(resources, list) or not all(
        isinstance(item, str) and item for item in resources
    ):
        raise ValueError("policy.granted_resources must be a list of strings")
    return CapabilityGrant(
        capabilities=frozenset(capabilities),
        resources=frozenset(resources),
    )


def normalize_policy(policy: dict | RoutePolicy | None, objective: str) -> RoutePolicy:
    if isinstance(policy, RoutePolicy):
        base = policy
    else:
        value = policy or {}
        if not isinstance(value, dict):
            raise ValueError("policy must be an object")
        mode = value.get("contract_mode", "legacy")
        if mode not in CONTRACT_MODES:
            raise ValueError("policy.contract_mode must be legacy, warn, strict, or hardened")
        legacy_auth = value.get("legacy_auth_scope")
        if legacy_auth is not None and legacy_auth not in LEGACY_AUTH_SCOPES:
            raise ValueError("policy.legacy_auth_scope is invalid")
        denied = value.get("denied_effects", [])
        if not isinstance(denied, list) or not all(
            isinstance(item, str) and item for item in denied
        ):
            raise ValueError("policy.denied_effects must be a list of strings")

        explicit_grant = normalize_grant(value.get("grant"))
        flat_grant = _flat_grant(value)
        if explicit_grant and flat_grant:
            explicit_grant = CapabilityGrant(
                capabilities=frozenset(
                    set(explicit_grant.capabilities) | set(flat_grant.capabilities)
                ),
                resources=frozenset(
                    set(explicit_grant.resources) | set(flat_grant.resources)
                ),
                grant_id=explicit_grant.grant_id,
                identity=explicit_grant.identity,
                expires_at=explicit_grant.expires_at,
            )
        grant = explicit_grant or flat_grant
        base = RoutePolicy(
            denied_effects=tuple(normalize_effects(denied)),
            grant=grant,
            legacy_auth_scope=legacy_auth,
            contract_mode=mode,
        )

    inferred = normalize_effects(excluded_effects(objective))
    denied = tuple(dict.fromkeys([*base.denied_effects, *inferred]))
    return RoutePolicy(
        denied_effects=denied,
        grant=base.grant,
        legacy_auth_scope=base.legacy_auth_scope,
        contract_mode=base.contract_mode,
    )


def evaluate_contract(contract: dict, policy: RoutePolicy) -> dict:
    reasons = []
    effects = contract.get("side_effects")
    status = contract.get("status", "opaque")

    if status in {"invalid", "unsupported"}:
        reasons.append(f"contract status {status}")
    elif status == "opaque" and policy.contract_mode in {"strict", "hardened"}:
        reasons.append(f"opaque contract rejected by {policy.contract_mode} policy")

    if effects is None and policy.denied_effects:
        reasons.append("undeclared side effects conflict with denied effects")
    else:
        for effect in effects or []:
            for denied in policy.denied_effects:
                if effect_matches(denied, effect):
                    reasons.append(f"effect {effect} denied by policy {denied}")
                    break

    required_capabilities = set(contract.get("capabilities") or [])
    required_resources = set(contract.get("resources") or [])
    if policy.grant is not None:
        if policy.grant.expired():
            reasons.append("host grant expired")
        missing_caps = missing_capabilities(
            required_capabilities, policy.grant.capabilities
        )
        missing_res = missing_resources(
            required_resources, policy.grant.resources
        )
        if missing_caps:
            reasons.append("capabilities not granted: " + ", ".join(missing_caps))
        if missing_res:
            reasons.append("resources not granted: " + ", ".join(missing_res))

    # Scalar auth is compatibility-only. Declared Contract v1 skills are
    # governed by capability/resource sets and never by the legacy ladder.
    if policy.legacy_auth_scope is not None and status == "legacy":
        required_scope = contract.get("auth_scope")
        if not legacy_scope_allows(policy.legacy_auth_scope, required_scope):
            reasons.append(
                f"legacy auth scope {required_scope} is not allowed by {policy.legacy_auth_scope}"
            )

    decision_status = "denied" if reasons else "allowed"
    if not reasons and status == "opaque":
        decision_status = "opaque"
    elif not reasons and status == "legacy" and policy.contract_mode in {"warn", "hardened"}:
        decision_status = "legacy-warning"

    return {
        "status": decision_status,
        "contract_status": status,
        "reasons": reasons,
        "effects": list(effects) if effects is not None else None,
        "capabilities": sorted(required_capabilities),
        "resources": sorted(required_resources),
        "grant_checked": policy.grant is not None,
        "grant_id": policy.grant.grant_id if policy.grant else None,
        "trust": dict(contract.get("trust") or {}),
        "contract_digest": contract.get("contract_digest"),
        "entrypoint_digest": contract.get("entrypoint_digest"),
    }


def evaluate_graph(graph: dict, objective: str, policy: dict | RoutePolicy | None = None):
    normalized = normalize_policy(policy, objective)
    decisions = {}
    for skill, node in graph.get("nodes", {}).items():
        decisions[skill] = evaluate_contract(contract_from_node(node), normalized)
    return normalized, decisions
