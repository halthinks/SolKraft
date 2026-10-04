"""Structured evidence supplied by an external execution host."""
from __future__ import annotations

import hashlib
import json

from .effects import normalize_effects


RESULT_STATES = (
    "selected",
    "blocked",
    "executed-unverified",
    "verified",
    "verification-failed",
)


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def evidence_digest(evidence: dict) -> str:
    return "sha256:" + hashlib.sha256(
        canonical_json(evidence).encode("utf-8")
    ).hexdigest()


def normalize_evidence(evidence: object) -> tuple[dict, list[str]]:
    """Normalize host evidence without reading files or executing anything."""
    if not isinstance(evidence, dict):
        return {}, ["evidence must be an object"]

    errors = []
    skill_id = evidence.get("skill_id")
    if not isinstance(skill_id, str) or not skill_id:
        errors.append("evidence.skill_id must be a non-empty string")

    contract_digest = evidence.get("contract_digest")
    if not isinstance(contract_digest, str) or not contract_digest.startswith("sha256:"):
        errors.append("evidence.contract_digest must be a sha256 digest")

    entrypoint_digest = evidence.get("entrypoint_digest")
    if not isinstance(entrypoint_digest, str) or not entrypoint_digest.startswith("sha256:"):
        errors.append("evidence.entrypoint_digest must be a sha256 digest")

    artifacts = evidence.get("artifacts", [])
    normalized_artifacts = []
    if not isinstance(artifacts, list):
        errors.append("evidence.artifacts must be a list")
    else:
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"evidence.artifacts[{index}] must be an object")
                continue
            name = artifact.get("name")
            if not isinstance(name, str) or not name:
                errors.append(f"evidence.artifacts[{index}].name must be a non-empty string")
                continue
            normalized_artifacts.append(dict(artifact))

    observed_effects = evidence.get("observed_effects", [])
    if not isinstance(observed_effects, list) or not all(
        isinstance(item, str) and item for item in observed_effects
    ):
        errors.append("evidence.observed_effects must be a list of strings")
        observed_effects = []

    fields = evidence.get("fields", {})
    if not isinstance(fields, dict):
        errors.append("evidence.fields must be an object")
        fields = {}

    checks = evidence.get("checks", {})
    if not isinstance(checks, dict):
        errors.append("evidence.checks must be an object")
        checks = {}

    normalized = {
        "skill_id": skill_id,
        "contract_digest": contract_digest,
        "entrypoint_digest": entrypoint_digest,
        "artifacts": normalized_artifacts,
        "observed_effects": normalize_effects(observed_effects),
        "fields": dict(fields),
        "checks": dict(checks),
        "host_receipt": evidence.get("host_receipt"),
    }
    normalized["evidence_digest"] = evidence_digest(normalized)
    return normalized, errors
