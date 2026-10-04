"""Capability and resource requirements for advisory route evaluation.

These structures describe what a route would require from a host. They do not
grant runtime authority and they are never treated as execution credentials.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re


CAPABILITY_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")

LEGACY_AUTH_SCOPES = ("none", "read", "write-local", "network", "external-effect")
LEGACY_SCOPE_ALLOW = {
    "none": frozenset({"none"}),
    "read": frozenset({"none", "read"}),
    "write-local": frozenset({"none", "read", "write-local"}),
    "network": frozenset({"none", "read", "write-local", "network"}),
    "external-effect": frozenset(LEGACY_AUTH_SCOPES),
}


def legacy_scope_allows(allowed: str | None, required: str | None) -> bool:
    """Compatibility adapter for pre-v1 scalar auth metadata only."""
    if allowed is None:
        return True
    if allowed not in LEGACY_SCOPE_ALLOW:
        raise ValueError("unknown legacy auth scope: " + str(allowed))
    if required is None:
        return False
    return required in LEGACY_SCOPE_ALLOW[allowed]


def _matches(pattern: str, value: str, *, separator: str) -> bool:
    if pattern == value:
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    if pattern.endswith(separator + "*"):
        return value.startswith(pattern[: -1])
    return False


def capability_matches(grant: str, required: str) -> bool:
    return _matches(grant, required, separator=".")


def resource_matches(grant: str, required: str) -> bool:
    return _matches(grant, required, separator=":")


def missing_capabilities(required, granted) -> list[str]:
    granted = tuple(granted or ())
    return sorted(
        requirement
        for requirement in set(required or ())
        if not any(capability_matches(item, requirement) for item in granted)
    )


def missing_resources(required, granted) -> list[str]:
    granted = tuple(granted or ())
    return sorted(
        requirement
        for requirement in set(required or ())
        if not any(resource_matches(item, requirement) for item in granted)
    )


@dataclass(frozen=True)
class CapabilityGrant:
    """A host-supplied advisory snapshot of currently available authority."""

    capabilities: frozenset[str]
    resources: frozenset[str]
    grant_id: str | None = None
    identity: str | None = None
    expires_at: str | None = None

    def public(self) -> dict:
        return {
            "grant_id": self.grant_id,
            "identity": self.identity,
            "expires_at": self.expires_at,
            "capabilities": sorted(self.capabilities),
            "resources": sorted(self.resources),
        }

    def expired(self, *, now: datetime | None = None) -> bool:
        if not self.expires_at:
            return False
        try:
            instant = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        except ValueError:
            return True
        now = now or datetime.now(timezone.utc)
        if instant.tzinfo is None:
            instant = instant.replace(tzinfo=timezone.utc)
        return instant <= now.astimezone(timezone.utc)


def normalize_grant(value: dict | CapabilityGrant | None) -> CapabilityGrant | None:
    if value is None:
        return None
    if isinstance(value, CapabilityGrant):
        return value
    if not isinstance(value, dict):
        raise ValueError("policy.grant must be an object")

    capabilities = value.get("capabilities", [])
    resources = value.get("resources", [])
    if not isinstance(capabilities, list) or not all(
        isinstance(item, str) and item for item in capabilities
    ):
        raise ValueError("policy.grant.capabilities must be a list of strings")
    if not isinstance(resources, list) or not all(
        isinstance(item, str) and item for item in resources
    ):
        raise ValueError("policy.grant.resources must be a list of strings")

    for item in capabilities:
        wildcard_base = item[:-2] if item.endswith(".*") else item
        if "*" not in item and not CAPABILITY_RE.fullmatch(item):
            raise ValueError(f"invalid granted capability: {item}")
        if item.endswith(".*") and not CAPABILITY_RE.fullmatch(wildcard_base + ".x"):
            raise ValueError(f"invalid granted capability pattern: {item}")

    return CapabilityGrant(
        capabilities=frozenset(capabilities),
        resources=frozenset(resources),
        grant_id=value.get("grant_id"),
        identity=value.get("identity"),
        expires_at=value.get("expires_at"),
    )
