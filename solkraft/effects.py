"""Namespaced side-effect identifiers used by Contract v1 and route policy."""
from __future__ import annotations

import re


LEGACY_EFFECT_ALIASES = {
    "merge": "repo.merge",
    "publish": "artifact.publish",
    "deploy": "deployment.release",
    "send": "messaging.send",
    "purchase": "billing.purchase",
    "fabricate": "fabrication.create",
    "delete": "fs.delete",
    "revoke": "identity.revoke",
    "rotate": "secret.rotate",
    "push": "repo.push",
}

EFFECT_ATTRIBUTES = {
    "repo.merge": {"mutation": True, "external": True, "destructive": False, "reversible": True},
    "artifact.publish": {"mutation": True, "external": True, "destructive": False, "reversible": True},
    "deployment.release": {"mutation": True, "external": True, "destructive": False, "reversible": True},
    "messaging.send": {"mutation": True, "external": True, "destructive": False, "reversible": False},
    "billing.purchase": {"mutation": True, "external": True, "destructive": False, "reversible": False},
    "fabrication.create": {"mutation": True, "external": True, "destructive": False, "reversible": False},
    "fs.delete": {"mutation": True, "external": False, "destructive": True, "reversible": False},
    "identity.revoke": {"mutation": True, "external": True, "destructive": True, "reversible": True},
    "secret.rotate": {"mutation": True, "external": True, "destructive": False, "reversible": True},
    "repo.push": {"mutation": True, "external": True, "destructive": False, "reversible": True},
}

EFFECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")


def normalize_effect(effect: str) -> str:
    value = effect.strip().casefold()
    return LEGACY_EFFECT_ALIASES.get(value, value)


def normalize_effects(effects) -> list[str]:
    seen = set()
    result = []
    for effect in effects or ():
        if not isinstance(effect, str) or not effect.strip():
            continue
        normalized = normalize_effect(effect)
        if normalized not in seen:
            result.append(normalized)
            seen.add(normalized)
    return result


def effect_matches(pattern: str, effect: str) -> bool:
    pattern = normalize_effect(pattern)
    effect = normalize_effect(effect)
    if pattern.endswith(".*"):
        return effect.startswith(pattern[:-1])
    return pattern == effect


def validate_effect_id(effect: str) -> bool:
    return bool(EFFECT_ID_RE.fullmatch(normalize_effect(effect)))


def effect_attributes(effect: str) -> dict:
    return dict(EFFECT_ATTRIBUTES.get(normalize_effect(effect), {}))
