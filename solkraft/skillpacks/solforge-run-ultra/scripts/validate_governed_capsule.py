#!/usr/bin/env python3
"""Validate an app-governed SolForge Ultra wrapper capsule.

This validator is intentionally separate from ``validate_capsule.py``.  The
portable Ultra protocol and the app-governed MCP protocol have different,
immutable schemas and different runtime ledgers; accepting one as the other
would create an authority bypass.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any


HASH = re.compile(r"^[a-f0-9]{64}$")
KINDS = {
    "solforge-strategy-ultra": "strategy",
    "solforge-code-research-ultra": "code-research",
}
COMMON_SEQUENCE = [
    "start_run",
    "record_ultra_provider_usage",
    "record_run_outcome",
    "record_acceptance",
]
CODE_RESEARCH_RESULT_SEQUENCE = [
    "solforge_validate_code_research_result",
    "solforge_record_code_research_result",
    "record_run_outcome",
    "record_acceptance",
]


class ValidationError(ValueError):
    """A fail-closed governed capsule validation error."""


def js_number(value: int | float) -> str:
    """Render the ordinary finite JSON numbers emitted by JSON.stringify.

    Governed capsules use integer counters and conventional decimal scoring
    values.  This covers that complete emitted domain and rejects non-finite
    values instead of guessing at an identity.
    """

    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise ValidationError("non-finite number is forbidden")
    if value == 0:
        return "0"
    if value.is_integer() and abs(value) < 1e21:
        return str(int(value))
    rendered = repr(value).lower()
    if "e" in rendered:
        mantissa, exponent = rendered.split("e", 1)
        sign = ""
        if exponent.startswith(("+", "-")):
            sign, exponent = exponent[0], exponent[1:]
        exponent = exponent.lstrip("0") or "0"
        numeric_exponent = int((sign or "+") + exponent)
        # JSON.stringify uses fixed notation in [1e-6, 1e21).
        if -6 <= numeric_exponent < 21:
            fixed = format(value, ".15f").rstrip("0").rstrip(".")
            return fixed
        return f"{mantissa}e{sign}{exponent}"
    return rendered


def canonical(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return js_number(value)
    if isinstance(value, list):
        return "[" + ",".join(canonical(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValidationError("object keys must be strings")
        # Node's canonicalizers use String.localeCompare.  Governed schema
        # keys are ASCII; its default ICU ordering is case-insensitive first
        # with lowercase before uppercase for otherwise equal keys.
        ordered_keys = sorted(
            value,
            key=lambda key: (
                key.casefold(),
                tuple(0 if char.islower() else 1 if char.isupper() else 0 for char in key),
                key,
            ),
        )
        return "{" + ",".join(
            f"{json.dumps(key, ensure_ascii=False)}:{canonical(value[key])}"
            for key in ordered_keys
        ) + "}"
    raise ValidationError(f"unsupported JSON value: {type(value).__name__}")


def sha256(value: Any) -> str:
    raw = value if isinstance(value, str) else canonical(value)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def require_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or not HASH.fullmatch(value):
        raise ValidationError(f"{label} must be a lowercase SHA-256")
    return value


def require_exact_keys(value: dict[str, Any], required: set[str], label: str) -> None:
    missing = sorted(required - set(value))
    if missing:
        raise ValidationError(f"{label} is missing: {', '.join(missing)}")
    extras = sorted(set(value) - required)
    if extras:
        raise ValidationError(f"{label} contains unknown fields: {', '.join(extras)}")


def verify_source_receipt(capsule: dict[str, Any], source_kind: str) -> None:
    source = capsule["governedSource"]
    receipt = capsule["sourceReceipt"]
    if not isinstance(source, dict) or not isinstance(receipt, dict):
        raise ValidationError("governed source and source receipt must be objects")
    if source.get("kind") != source_kind:
        raise ValidationError("governed source kind mismatch")
    source_hash = require_hash(source.get("receiptSha256"), "source receipt hash")
    declared_hash = require_hash(receipt.get("receiptSha256"), "source receipt declaration")
    if source_hash != declared_hash:
        raise ValidationError("governed source receipt mismatch")
    unsigned = dict(receipt)
    unsigned.pop("receiptSha256", None)
    if sha256(unsigned) != source_hash:
        raise ValidationError("source acceptance receipt integrity mismatch")
    if receipt.get("executionAuthorized") is not True:
        raise ValidationError("source acceptance did not authorize execution")
    if source.get("graphHash") != receipt.get("graphHash"):
        raise ValidationError("source graph binding mismatch")
    if source.get("acceptedContractHash") != receipt.get("acceptedContractHash"):
        raise ValidationError("source contract binding mismatch")
    require_hash(source.get("graphHash"), "source graph hash")
    require_hash(source.get("acceptedContractHash"), "source contract hash")
    if source_kind == "strategy":
        if sha256(capsule["contract"]) != source["acceptedContractHash"]:
            raise ValidationError("Strategy contract payload is not the accepted contract")
    else:
        if capsule["contract"].get("planHash") != source["acceptedContractHash"]:
            raise ValidationError("Code Research plan is not the accepted contract")


RUN_BUDGET_CEILINGS = {
    "maximumCompletionUnits",
    "maximumElapsedSeconds",
    "maximumToolCalls",
    "maximumRounds",
    "maximumRetries",
    "maximumAgents",
}


def verify_run_budget(binding: dict[str, Any], provider_budget: dict[str, Any]) -> None:
    run_budget = binding.get("runBudget")
    basis = binding.get("runBudgetBasis")
    required_run_budget = {
        "schemaVersion", "kind", "currency", *RUN_BUDGET_CEILINGS,
        "overageAllowed", "cumulativeAcrossContinuations", "basisHash",
        "authorityExpansionAuthorized",
    }
    required_basis = {
        "schemaVersion", "kind", "source", "effortId",
        "completionUnitEstimate", "completionUnitEstimateHash",
        "topologyIncrementContract", "topologyIncrementContractHash",
        "topologyIncrementUnits", "requestedMaximumCompletionUnits",
        "environmentMaximumCompletionUnits", "priorMaximumCompletionUnits",
        "clampedMaximumCompletionUnits", "inheritedFromRunBudgetHash",
        "fallbackReason", "cumulativeAcrossContinuations",
        "authorityExpansionAuthorized",
    }
    require_exact_keys(run_budget, required_run_budget, "native Ultra run budget")
    require_exact_keys(basis, required_basis, "native Ultra run budget basis")
    run_budget_hash = require_hash(binding.get("runBudgetHash"), "native Ultra run budget hash")
    basis_hash = require_hash(binding.get("runBudgetBasisHash"), "native Ultra run budget basis hash")
    if sha256(run_budget) != run_budget_hash or sha256(basis) != basis_hash:
        raise ValidationError("native Ultra run budget hash mismatch")
    if run_budget.get("basisHash") != basis_hash:
        raise ValidationError("native Ultra run budget is detached from its basis")
    if (
        run_budget.get("schemaVersion") != "1.0"
        or run_budget.get("kind") != "solforge-ultra-run-budget-v1"
        or run_budget.get("currency") != provider_budget.get("currency")
        or run_budget.get("overageAllowed") is not False
        or run_budget.get("cumulativeAcrossContinuations") is not True
        or run_budget.get("authorityExpansionAuthorized") is not False
        or basis.get("schemaVersion") != "1.0"
        or basis.get("kind") != "solforge-ultra-run-budget-basis"
        or basis.get("cumulativeAcrossContinuations") is not True
        or basis.get("authorityExpansionAuthorized") is not False
    ):
        raise ValidationError("native Ultra run budget contract is invalid")
    for key in RUN_BUDGET_CEILINGS:
        if not isinstance(run_budget.get(key), int) or run_budget[key] < 0:
            raise ValidationError(f"native Ultra run budget {key} is invalid")
        if run_budget[key] > provider_budget[key]:
            raise ValidationError(f"native Ultra run budget {key} exceeds provider capacity")
    if run_budget["maximumAgents"] < 2:
        raise ValidationError("native Ultra run budget requires at least two agents")
    for key in ("maximumCompletionUnits", "maximumElapsedSeconds", "maximumToolCalls", "maximumRounds"):
        if run_budget[key] < 1:
            raise ValidationError(f"native Ultra run budget {key} must be positive")
    for key in (
        "requestedMaximumCompletionUnits", "environmentMaximumCompletionUnits",
        "clampedMaximumCompletionUnits", "topologyIncrementUnits",
    ):
        if not isinstance(basis.get(key), int) or basis[key] < 0:
            raise ValidationError(f"native Ultra run budget basis {key} is invalid")
    prior_maximum = basis.get("priorMaximumCompletionUnits")
    if prior_maximum is not None and (
        not isinstance(prior_maximum, int) or prior_maximum < 1
    ):
        raise ValidationError("native Ultra prior run budget ceiling is invalid")
    if basis.get("inheritedFromRunBudgetHash") is not None:
        require_hash(basis["inheritedFromRunBudgetHash"], "inherited run budget hash")
    expected_clamp = min(
        basis["requestedMaximumCompletionUnits"],
        basis["environmentMaximumCompletionUnits"],
        prior_maximum or basis["environmentMaximumCompletionUnits"],
    )
    if (
        basis["environmentMaximumCompletionUnits"]
        != provider_budget["maximumCompletionUnits"]
        or basis["clampedMaximumCompletionUnits"] != expected_clamp
        or run_budget["maximumCompletionUnits"] != expected_clamp
    ):
        raise ValidationError("native Ultra run budget clamp was rebound")

    increment = basis.get("topologyIncrementContract")
    if increment is not None:
        require_exact_keys(
            increment,
            {
                "schemaVersion", "kind", "units", "sourceContractHash",
                "authorityExpansionAuthorized", "contractHash",
            },
            "Ultra topology increment contract",
        )
        unsigned_increment = dict(increment)
        increment_hash = require_hash(
            unsigned_increment.pop("contractHash", None),
            "Ultra topology increment contract hash",
        )
        if (
            sha256(unsigned_increment) != increment_hash
            or increment.get("schemaVersion") != "1.0"
            or increment.get("kind")
            != "solforge-ultra-topology-completion-unit-increment"
            or not isinstance(increment.get("units"), int)
            or increment["units"] < 0
            or increment.get("authorityExpansionAuthorized") is not False
        ):
            raise ValidationError("Ultra topology increment contract is invalid")
        require_hash(increment.get("sourceContractHash"), "topology increment source contract")
    if (
        basis.get("topologyIncrementContractHash")
        != (increment.get("contractHash") if increment else None)
        or basis.get("topologyIncrementUnits")
        != (increment.get("units") if increment else 0)
    ):
        raise ValidationError("Ultra topology increment binding mismatch")

    if basis.get("source") == "accepted_completion_unit_contract":
        estimate = basis.get("completionUnitEstimate")
        if not isinstance(estimate, dict):
            raise ValidationError("accepted completion-unit estimate is missing")
        estimate_hash = require_hash(estimate.get("estimateHash"), "completion-unit estimate hash")
        unsigned_estimate = dict(estimate)
        unsigned_estimate.pop("estimateHash", None)
        if (
            sha256(unsigned_estimate) != estimate_hash
            or estimate.get("schemaVersion") != "1.0"
            or estimate.get("policyVersion") != "solforge-completion-units-v1"
            or basis.get("completionUnitEstimateHash") != estimate_hash
            or basis.get("effortId") != estimate.get("effortId")
            or basis.get("fallbackReason") is not None
            or not isinstance(estimate.get("maximumUnits"), int)
            or basis["requestedMaximumCompletionUnits"]
            != estimate["maximumUnits"] + basis["topologyIncrementUnits"]
        ):
            raise ValidationError("accepted completion-unit estimate was rebound")
    elif (
        basis.get("source") != "environment_hard_max_fallback"
        or basis.get("completionUnitEstimate") is not None
        or basis.get("completionUnitEstimateHash") is not None
        or basis.get("effortId") is not None
        or increment is not None
        or basis.get("topologyIncrementContractHash") is not None
        or basis.get("topologyIncrementUnits") != 0
        or not isinstance(basis.get("fallbackReason"), str)
        or not basis["fallbackReason"].strip()
        or basis["requestedMaximumCompletionUnits"]
        != provider_budget["maximumCompletionUnits"]
    ):
        raise ValidationError("native Ultra run budget fallback is invalid")


def verify_native_capability(
    capsule: dict[str, Any],
    source_kind: str | None,
    attestation_secret: str,
    expected_subject: dict[str, Any] | None = None,
) -> None:
    binding = capsule["nativeUltraCapability"]
    if not isinstance(binding, dict):
        raise ValidationError("native Ultra binding must be an object")
    require_exact_keys(
        binding,
        {
            "schemaVersion",
            "provider",
            "hostId",
            "maxAgents",
            "executionMode",
            "configHash",
            "budget",
            "budgetHash",
            "runBudget",
            "runBudgetHash",
            "runBudgetBasis",
            "runBudgetBasisHash",
            "leaseSubject",
            "initialLease",
            "initialLeaseHash",
            "initialLeaseExpiresAt",
            "leaseTtlSeconds",
            "providerUsageProtocol",
            "providerUsageKeyId",
            "killSwitchRequired",
            "userAcceptanceRequired",
            "authorityExpansionAuthorized",
        },
        "native Ultra binding",
    )
    if binding.get("schemaVersion") != "solforge-native-ultra-v1":
        raise ValidationError("native Ultra capability schema mismatch")
    if binding.get("executionMode") != "full_approved_capsule":
        raise ValidationError("governed Ultra requires full-approved-capsule mode")
    if not isinstance(binding.get("maxAgents"), int) or binding["maxAgents"] < 2:
        raise ValidationError("governed Ultra requires at least two native agents")
    if binding.get("providerUsageProtocol") != "solforge-ultra-usage-v1":
        raise ValidationError("provider usage protocol mismatch")
    if (
        binding.get("killSwitchRequired") is not True
        or binding.get("userAcceptanceRequired") is not True
        or binding.get("authorityExpansionAuthorized") is not False
    ):
        raise ValidationError("native Ultra safety flags are invalid")

    budget = binding.get("budget")
    if not isinstance(budget, dict) or sha256(budget) != binding.get("budgetHash"):
        raise ValidationError("native Ultra budget hash mismatch")
    require_hash(binding.get("budgetHash"), "native Ultra budget hash")
    required_budget = {
        "schemaVersion",
        "currency",
        "maximumCompletionUnits",
        "maximumElapsedSeconds",
        "maximumToolCalls",
        "maximumRounds",
        "maximumRetries",
        "maximumAgents",
        "overageAllowed",
        "authorityExpansionAuthorized",
    }
    require_exact_keys(budget, required_budget, "native Ultra budget")
    if budget.get("schemaVersion") != "1.0" or budget.get("currency") != "completion_units":
        raise ValidationError("native Ultra budget schema or currency mismatch")
    for key in required_budget - {"schemaVersion", "currency", "overageAllowed", "authorityExpansionAuthorized"}:
        if not isinstance(budget[key], int) or budget[key] < 0:
            raise ValidationError(f"native Ultra budget {key} must be finite and nonnegative")
    if budget["maximumAgents"] < 2 or budget["maximumAgents"] > binding["maxAgents"]:
        raise ValidationError("native Ultra agent ceiling exceeds capability")
    if budget.get("overageAllowed") is not False or budget.get("authorityExpansionAuthorized") is not False:
        raise ValidationError("native Ultra budget may not allow overage or authority expansion")
    verify_run_budget(binding, budget)
    increment = binding["runBudgetBasis"].get("topologyIncrementContract")
    if increment is not None:
        accepted_increment_source = None
        for owner in (capsule.get("contract"), capsule.get("completionRoute")):
            if isinstance(owner, dict) and isinstance(
                owner.get("ultraTopologyCompletionUnitIncrement"), dict
            ):
                accepted_increment_source = owner["ultraTopologyCompletionUnitIncrement"]
                break
        if (
            accepted_increment_source is None
            or sha256(accepted_increment_source)
            != increment.get("sourceContractHash")
        ):
            raise ValidationError(
                "Ultra topology increment is not bound to the accepted source contract"
            )

    subject = binding.get("leaseSubject")
    if not isinstance(subject, dict):
        raise ValidationError("native Ultra lease subject is missing")
    if expected_subject is None:
        source = capsule["governedSource"]
        expected_subject = {
            "purpose": f"{source_kind}-governed-ultra-run",
            "runId": capsule["runId"],
            "sourceId": source["id"],
            "sourceReceiptSha256": source["receiptSha256"],
        }
    if canonical(subject) != canonical(expected_subject):
        raise ValidationError("native Ultra capability was rebound to another subject")

    lease = binding.get("initialLease")
    if not isinstance(lease, dict):
        raise ValidationError("initial native Ultra lease is missing")
    lease_hash = require_hash(lease.get("leaseHash"), "initial native Ultra lease hash")
    unsigned_lease = {
        key: value for key, value in lease.items() if key not in {"leaseHash", "signature"}
    }
    if sha256(unsigned_lease) != lease_hash or binding.get("initialLeaseHash") != lease_hash:
        raise ValidationError("initial native Ultra lease integrity mismatch")
    expected_signature = hmac.new(
        attestation_secret.encode("utf-8"), lease_hash.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    signature = lease.get("signature")
    if not isinstance(signature, str) or not hmac.compare_digest(expected_signature, signature):
        raise ValidationError("initial native Ultra lease signer proof mismatch")
    if lease.get("subjectHash") != sha256(subject):
        raise ValidationError("initial native Ultra lease subject mismatch")
    for field in ("provider", "hostId", "maxAgents", "executionMode", "configHash", "budgetHash"):
        if lease.get(field) != binding.get(field):
            raise ValidationError(f"initial native Ultra lease {field} mismatch")
    if lease.get("expiresAt") != binding.get("initialLeaseExpiresAt"):
        raise ValidationError("initial native Ultra lease expiry mismatch")
    require_hash(binding.get("configHash"), "native Ultra configuration hash")
    require_hash(binding.get("providerUsageKeyId"), "provider usage key id")


def validate(path: Path) -> dict[str, Any]:
    try:
        capsule = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read governed capsule: {exc}") from exc
    if not isinstance(capsule, dict):
        raise ValidationError("governed capsule must be a JSON object")
    if "schema_version" in capsule or "capsule_sha256" in capsule:
        raise ValidationError("portable and governed capsule protocols may not be mixed")
    require_exact_keys(
        capsule,
        {
            "schemaVersion",
            "kind",
            "runId",
            "originalIntent",
            "profile",
            "nativeUltraCapability",
            "effort",
            "effortProfileHash",
            "governedSource",
            "sourceReceipt",
            "graph",
            "contract",
            "completionRoute",
            "effects",
            "authority",
            "executionContract",
            "workflowRoute",
            "acceptanceSequence",
            "executionAuthorized",
            "authorityExpansionAuthorized",
            "capsuleHash",
        },
        "governed Ultra capsule",
    )
    if capsule.get("schemaVersion") != "2.0":
        raise ValidationError("governed Ultra capsule schema mismatch")
    source_kind = KINDS.get(capsule.get("kind"))
    if source_kind is None:
        raise ValidationError("unsupported governed Ultra capsule kind")
    if capsule.get("profile") != "ultra":
        raise ValidationError("governed Ultra capsule profile mismatch")
    if not isinstance(capsule.get("runId"), str) or not capsule["runId"]:
        raise ValidationError("governed Ultra run id is missing")
    if not isinstance(capsule.get("originalIntent"), str) or not capsule["originalIntent"].strip():
        raise ValidationError("governed Ultra intent is missing")
    if capsule.get("executionAuthorized") is not True or capsule.get("authorityExpansionAuthorized") is not False:
        raise ValidationError("governed Ultra execution/authority flags are invalid")
    unsigned = dict(capsule)
    declared_hash = require_hash(unsigned.pop("capsuleHash", None), "governed capsule hash")
    if sha256(unsigned) != declared_hash:
        raise ValidationError("governed Ultra capsule integrity mismatch")
    if sha256(capsule.get("effort")) != capsule.get("effortProfileHash"):
        raise ValidationError("governed Ultra effort profile hash mismatch")
    require_hash(capsule.get("effortProfileHash"), "effort profile hash")
    if capsule.get("acceptanceSequence") != COMMON_SEQUENCE:
        raise ValidationError("governed Ultra acceptance sequence mismatch")

    route = capsule.get("workflowRoute")
    if not isinstance(route, dict) or route.get("skillId") != "solforge-run-ultra":
        raise ValidationError("governed capsule is not routed to Run Ultra")
    if route.get("routeId") != f"{source_kind}_ultra":
        raise ValidationError("governed Ultra workflow route mismatch")
    require_hash(route.get("routeHash"), "governed Ultra route hash")

    verify_source_receipt(capsule, source_kind)
    secret = os.environ.get("SOLFORGE_NATIVE_ULTRA_ATTESTATION_SECRET", "").strip()
    if len(secret) < 32:
        raise ValidationError(
            "SOLFORGE_NATIVE_ULTRA_ATTESTATION_SECRET must contain at least 32 characters"
        )
    verify_native_capability(capsule, source_kind, secret)

    if source_kind == "code-research":
        route_sequence = capsule.get("completionRoute", {}).get("resultSequence")
        required_tools = capsule.get("executionContract", {}).get("requiredResultTools")
        if route_sequence != CODE_RESEARCH_RESULT_SEQUENCE:
            raise ValidationError("Code Research governed result sequence mismatch")
        if required_tools != CODE_RESEARCH_RESULT_SEQUENCE[:2]:
            raise ValidationError("Code Research governed result tools mismatch")
        if capsule.get("executionContract", {}).get("resultMustPrecedeRunOutcome") is not True:
            raise ValidationError("Code Research result must precede run outcome")

    return {
        "valid": True,
        "protocol": "app_governed_mcp",
        "kind": capsule["kind"],
        "runId": capsule["runId"],
        "capsuleHash": declared_hash,
        "sourceReceiptSha256": capsule["governedSource"]["receiptSha256"],
        "effortProfileHash": capsule["effortProfileHash"],
        "providerBudgetHash": capsule["nativeUltraCapability"]["budgetHash"],
        "runBudgetHash": capsule["nativeUltraCapability"]["runBudgetHash"],
        "runBudgetBasisHash": capsule["nativeUltraCapability"]["runBudgetBasisHash"],
        "providerUsageProtocol": capsule["nativeUltraCapability"]["providerUsageProtocol"],
        "authorityExpansionAuthorized": False,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_governed_capsule.py <governed-capsule.json>", file=sys.stderr)
        return 2
    try:
        result = validate(Path(argv[1]).resolve())
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
