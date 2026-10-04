"""Resolve contract trust from external digest-bound bindings."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


TRUST_STATES = (
    "bundled-reviewed",
    "signed",
    "operator-trusted",
    "local-unreviewed",
    "legacy-inferred",
    "opaque",
    "invalid",
)
TRUSTED_STATES = {"bundled-reviewed", "signed", "operator-trusted"}
REGISTRY_PATH = Path(__file__).resolve().parent / "trust-bindings.json"


@lru_cache(maxsize=1)
def load_trust_bindings() -> dict:
    if not REGISTRY_PATH.is_file():
        return {}
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return data.get("bindings", {}) if isinstance(data, dict) else {}


def resolve_trust(
    skill_id: str,
    contract: dict,
    *,
    registry: dict | None = None,
) -> dict:
    """Resolve trust. Skill-authored provenance cannot elevate this result."""
    status = contract.get("status")
    if status in {"invalid", "unsupported"}:
        return {"state": "invalid", "trusted": False, "reason": f"contract status {status}"}
    if status == "opaque":
        return {"state": "opaque", "trusted": False, "reason": "no usable contract declaration"}
    if status == "legacy":
        return {
            "state": "legacy-inferred",
            "trusted": False,
            "reason": "metadata inferred from legacy graph or migration",
        }

    registry = registry if registry is not None else load_trust_bindings()
    binding = registry.get(skill_id) if isinstance(registry, dict) else None
    if not isinstance(binding, dict):
        return {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "no external digest-bound trust binding",
        }

    state = binding.get("state")
    if state not in TRUSTED_STATES:
        return {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "external binding does not grant a recognized trusted state",
        }

    if binding.get("contract_digest") != contract.get("contract_digest"):
        return {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "trusted contract digest does not match",
        }
    if binding.get("entrypoint_digest") != contract.get("entrypoint_digest"):
        return {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "trusted procedure digest does not match",
        }

    return {
        "state": state,
        "trusted": True,
        "reason": "external digest-bound trust binding matched",
        "reviewer": binding.get("reviewer"),
        "binding_revision": binding.get("revision"),
    }
