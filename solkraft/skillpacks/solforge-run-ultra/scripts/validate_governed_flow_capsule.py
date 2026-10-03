#!/usr/bin/env python3
"""Validate every non-Strategy app-governed Ultra capsule shape.

Each flow has a closed schema and flow-specific authority/provenance checks.
Live execution still requires the owning app's state/approval/Goal checks; this
file validates immutable artifact identity and prevents capsules from falling
between protected skills.
"""

from __future__ import annotations

import json
import hashlib
import os
import sys
from pathlib import Path
from typing import Any, Callable

from validate_governed_capsule import (
    ValidationError,
    canonical,
    require_exact_keys,
    require_hash,
    sha256,
    verify_native_capability,
)


FLOW_KEYS: dict[str, set[str]] = {
    "prompt": {
        "schemaVersion", "runId", "request", "originalRequestHash",
        "promptOriginId", "promptTemplateId", "promptObjectiveReceiptSha256",
        "promptSelection", "promptSelectionHash", "promptSelectionReceiptSha256",
        "profile", "effort", "effortProfileHash", "hardenedPrompt",
        "hardenedPromptHash", "nativeUltraCapability", "authority", "capsuleHash",
    },
    "solforge-mvp-create": {
        "schemaVersion", "kind", "runId", "parentRunId", "originalIntent",
        "sourceResultHash", "profile", "nativeUltraCapability", "effort",
        "effortProfileHash", "hardenedPromptHash", "parentCapsule",
        "mvpDefinition", "mvpDefinitionHash", "definitionReceiptSha256",
        "creationReceiptSha256", "authority", "executionAuthorized", "capsuleHash",
    },
    "solforge-proposal": {
        "schemaVersion", "kind", "runId", "parentRunId", "originalIntent",
        "profile", "nativeUltraCapability", "effort", "effortProfileHash",
        "hardenedPromptHash", "parentCapsule", "codebaseResultHash",
        "evidenceLedgerHash", "proposalDirection", "executionContract",
        "selectionReceiptSha256", "creationReceiptSha256", "authority",
        "executionAuthorized", "permissionExpansionAuthorized", "capsuleHash",
    },
    "solforge-specialized-execution": {
        "schemaVersion", "kind", "runId", "parentRunId", "originalIntent",
        "profile", "nativeUltraCapability", "effort", "effortProfileHash",
        "parentCapsule", "proposalResultHash", "executionPlan", "runRoute",
        "executionContract", "selectionReceiptSha256", "creationReceiptSha256",
        "authority", "permissionExpansionAuthorized",
        "externalPublishingAuthorized", "capsuleHash",
    },
    "solforge-replacement-execution": {
        "schemaVersion", "kind", "runId", "parentRunId", "replacesCapsule",
        "sourceOutcomeHash", "sourceArtifacts", "originalIntent", "profile",
        "nativeUltraCapability", "effort", "effortProfileHash",
        "replacementSpecification", "proposalSummary", "executionContract",
        "userSteering", "selectionReceiptSha256", "creationReceiptSha256",
        "authority", "executionAuthorized", "capsuleHash",
    },
    "solforge-report-execution": {
        "schemaVersion", "kind", "runId", "originalIntent", "profile",
        "nativeUltraCapability", "effort", "effortProfileHash",
        "hardenedPromptHash", "sourceResultHash", "parentCapsule",
        "reportRequest", "authority", "executionAuthorized", "prohibitions",
        "capsuleHash",
    },
    "derived-workflow-route": {
        "schemaVersion", "kind", "runId", "request", "profile",
        "nativeUltraCapability", "effort", "effortProfileHash",
        "hardenedPromptHash", "promptRunResultHash", "parentCapsule",
        "routeConfiguration", "routeHash", "routeReceiptSha256", "authority",
        "inheritedRequirements", "capsuleHash",
    },
}


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} is required")
    return value


def parent_pointer(value: Any, label: str = "parent capsule") -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} pointer is required")
    expected = {"path", "hash"}
    if label == "replaced capsule":
        expected.add("resumable")
    require_exact_keys(value, expected, label)
    require_string(value.get("path"), f"{label} path")
    require_hash(value.get("hash"), f"{label} hash")
    if label == "replaced capsule" and value.get("resumable") is not False:
        raise ValidationError("replaced Ultra capsule may not be resumed")


def common(capsule: dict[str, Any], expected_subject: dict[str, Any] | None) -> None:
    if capsule.get("profile") != "ultra":
        raise ValidationError("governed flow capsule profile mismatch")
    require_string(capsule.get("runId"), "run id")
    require_string(capsule.get("originalIntent", capsule.get("request")), "intent")
    if sha256(capsule.get("effort")) != capsule.get("effortProfileHash"):
        raise ValidationError("governed flow effort hash mismatch")
    require_hash(capsule.get("effortProfileHash"), "effort profile hash")
    binding = capsule.get("nativeUltraCapability")
    if not isinstance(binding, dict) or binding.get("leaseSubject", {}).get("runId") != capsule["runId"]:
        raise ValidationError("native Ultra capability is not scoped to this run")
    if expected_subject is None:
        expected_subject = binding["leaseSubject"]
    secret = os.environ.get("SOLFORGE_NATIVE_ULTRA_ATTESTATION_SECRET", "").strip()
    if len(secret) < 32:
        raise ValidationError(
            "SOLFORGE_NATIVE_ULTRA_ATTESTATION_SECRET must contain at least 32 characters"
        )
    verify_native_capability(capsule, None, secret, expected_subject)


def validate_prompt(capsule: dict[str, Any]) -> None:
    if capsule.get("schemaVersion") != "1.3" or "kind" in capsule:
        raise ValidationError("Prompt Ultra capsule discriminator mismatch")
    if capsule.get("authority") != "user-request-only":
        raise ValidationError("Prompt Ultra authority expanded")
    if sha256(capsule.get("request")) != capsule.get("originalRequestHash"):
        raise ValidationError("Prompt Ultra original request hash mismatch")
    if sha256(capsule.get("promptSelection")) != capsule.get("promptSelectionHash"):
        raise ValidationError("Prompt Ultra selection hash mismatch")
    if capsule.get("promptSelection", {}).get("profile") != "ultra":
        raise ValidationError("Prompt Ultra selection profile mismatch")
    if sha256(capsule.get("hardenedPrompt")) != capsule.get("hardenedPromptHash"):
        raise ValidationError("Prompt Ultra hardened prompt hash mismatch")
    for key in (
        "promptObjectiveReceiptSha256", "promptSelectionReceiptSha256",
        "originalRequestHash", "promptSelectionHash", "hardenedPromptHash",
    ):
        require_hash(capsule.get(key), key)
    common(capsule, None)


def derived_subject(capsule: dict[str, Any], purpose: str) -> dict[str, Any]:
    return {
        "purpose": purpose,
        "runId": capsule["runId"],
        "parentRunId": capsule["parentRunId"],
    }


def validate_mvp(capsule: dict[str, Any]) -> None:
    if capsule.get("authority") != "create-new-local-mvp-repository-only" or capsule.get("executionAuthorized") is not False:
        raise ValidationError("MVP capsule authority expanded or pre-authorized execution")
    parent_pointer(capsule.get("parentCapsule"))
    if sha256(capsule.get("mvpDefinition")) != capsule.get("mvpDefinitionHash"):
        raise ValidationError("MVP definition hash mismatch")
    for key in ("sourceResultHash", "mvpDefinitionHash", "definitionReceiptSha256", "creationReceiptSha256", "hardenedPromptHash"):
        require_hash(capsule.get(key), key)
    common(capsule, derived_subject(capsule, "derived-mvp-run"))


def validate_proposal(capsule: dict[str, Any]) -> None:
    if (
        capsule.get("authority") != "proposal-production-only"
        or capsule.get("executionAuthorized") is not False
        or capsule.get("permissionExpansionAuthorized") is not False
    ):
        raise ValidationError("Proposal capsule authority expanded or pre-authorized execution")
    parent_pointer(capsule.get("parentCapsule"))
    if canonical(capsule.get("executionContract")) != canonical(capsule.get("proposalDirection", {}).get("executionContract")):
        raise ValidationError("Proposal execution contract mismatch")
    for key in ("codebaseResultHash", "evidenceLedgerHash", "selectionReceiptSha256", "creationReceiptSha256", "hardenedPromptHash"):
        require_hash(capsule.get(key), key)
    common(capsule, derived_subject(capsule, "derived-proposal-run"))


def validate_specialized(capsule: dict[str, Any]) -> None:
    if (
        capsule.get("authority") != "execute-exact-approved-plan-only"
        or capsule.get("permissionExpansionAuthorized") is not False
        or capsule.get("externalPublishingAuthorized") is not False
    ):
        raise ValidationError("specialized execution authority expanded")
    parent_pointer(capsule.get("parentCapsule"))
    if canonical(capsule.get("executionContract")) != canonical(capsule.get("runRoute", {}).get("executionContract")):
        raise ValidationError("specialized execution contract mismatch")
    route = capsule.get("runRoute")
    if not isinstance(route, dict) or route.get("skillId") not in {
        "solforge-run-research", "solforge-run-refactor", "solforge-run-comparison",
        "solforge-run-report-write", "solforge-run-ultra",
    }:
        raise ValidationError("specialized Ultra route is not protected")
    plan = capsule.get("executionPlan")
    require_exact_keys(plan, {"path", "hash"}, "execution plan")
    plan_path = Path(require_string(plan.get("path"), "execution plan path"))
    plan_hash = require_hash(plan.get("hash"), "execution plan hash")
    if not plan_path.is_file() or hashlib.sha256(plan_path.read_bytes()).hexdigest() != plan_hash:
        raise ValidationError("specialized execution plan file hash mismatch")
    for key in ("proposalResultHash", "selectionReceiptSha256", "creationReceiptSha256"):
        require_hash(capsule.get(key), key)
    common(capsule, derived_subject(capsule, "derived-specialized-run"))


def validate_replacement(capsule: dict[str, Any]) -> None:
    if capsule.get("authority") != "replacement-capsule-created-not-execution-approved" or capsule.get("executionAuthorized") is not False:
        raise ValidationError("replacement capsule authority expanded or pre-authorized execution")
    parent_pointer(capsule.get("replacesCapsule"), "replaced capsule")
    for key in ("sourceOutcomeHash", "selectionReceiptSha256", "creationReceiptSha256"):
        require_hash(capsule.get(key), key)
    if not isinstance(capsule.get("sourceArtifacts"), list):
        raise ValidationError("replacement source artifact ledger is missing")
    common(capsule, derived_subject(capsule, "derived-replacement-run"))


def validate_report(capsule: dict[str, Any]) -> None:
    if capsule.get("authority") != "produce-the-approved-report-artifacts-only" or capsule.get("executionAuthorized") is not False:
        raise ValidationError("report capsule authority expanded or pre-authorized execution")
    parent_pointer(capsule.get("parentCapsule"))
    prohibitions = capsule.get("prohibitions")
    if not isinstance(prohibitions, list) or len(prohibitions) < 4 or not all(isinstance(item, str) and item for item in prohibitions):
        raise ValidationError("report capsule prohibitions are incomplete")
    request = capsule.get("reportRequest")
    if not isinstance(request, dict):
        raise ValidationError("report request is missing")
    for key in ("sourceResultHash", "hardenedPromptHash"):
        require_hash(capsule.get(key), key)
    for key in ("configurationHash", "configurationReceiptSha256", "sourceResultHash"):
        require_hash(request.get(key), f"report request {key}")
    if request.get("sourceResultHash") != capsule.get("sourceResultHash"):
        raise ValidationError("report source result binding mismatch")
    common(capsule, None)


def validate_derived_workflow(capsule: dict[str, Any]) -> None:
    if capsule.get("schemaVersion") != "1.2":
        raise ValidationError("derived workflow capsule schema mismatch")
    if (
        capsule.get("authority") != "user-request-only"
        or capsule.get("inheritedRequirements") != "preserved-without-reduction"
    ):
        raise ValidationError("derived workflow authority or requirements expanded")
    parent_pointer(capsule.get("parentCapsule"))
    if sha256(capsule.get("routeConfiguration")) != capsule.get("routeHash"):
        raise ValidationError("derived workflow route hash mismatch")
    route = capsule.get("routeConfiguration")
    if not isinstance(route, dict) or route.get("routeId") not in {
        "solforge_plugin_development", "codebase", "code_research", "research",
        "implementation", "report",
    }:
        raise ValidationError("derived workflow route is unsupported")
    for key in (
        "hardenedPromptHash", "promptRunResultHash", "routeHash",
        "routeReceiptSha256",
    ):
        require_hash(capsule.get(key), key)
    common(capsule, None)


VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {
    "prompt": validate_prompt,
    "solforge-mvp-create": validate_mvp,
    "solforge-proposal": validate_proposal,
    "solforge-specialized-execution": validate_specialized,
    "solforge-replacement-execution": validate_replacement,
    "solforge-report-execution": validate_report,
    "derived-workflow-route": validate_derived_workflow,
}


def validate(path: Path) -> dict[str, Any]:
    try:
        capsule = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read governed flow capsule: {exc}") from exc
    if not isinstance(capsule, dict) or "schema_version" in capsule or "capsule_sha256" in capsule:
        raise ValidationError("portable and governed capsule protocols may not be mixed")
    flow = "prompt" if capsule.get("schemaVersion") == "1.3" and "kind" not in capsule else capsule.get("kind")
    validator = VALIDATORS.get(flow)
    if validator is None or capsule.get("schemaVersion") not in {"1.2", "1.3", "2.0"}:
        raise ValidationError("unsupported governed Ultra flow capsule")
    require_exact_keys(capsule, FLOW_KEYS[flow], f"{flow} capsule")
    declared_hash = require_hash(capsule.get("capsuleHash"), "governed flow capsule hash")
    unsigned = dict(capsule)
    unsigned.pop("capsuleHash", None)
    if sha256(unsigned) != declared_hash:
        raise ValidationError("governed flow capsule integrity mismatch")
    validator(capsule)
    return {
        "valid": True,
        "protocol": "app_governed_mcp",
        "flow": flow,
        "runId": capsule["runId"],
        "capsuleHash": declared_hash,
        "providerBudgetHash": capsule["nativeUltraCapability"]["budgetHash"],
        "runBudgetHash": capsule["nativeUltraCapability"]["runBudgetHash"],
        "runBudgetBasisHash": capsule["nativeUltraCapability"]["runBudgetBasisHash"],
        "authorityExpansionAuthorized": False,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_governed_flow_capsule.py <capsule.json>", file=sys.stderr)
        return 2
    try:
        output = validate(Path(argv[1]).resolve())
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
