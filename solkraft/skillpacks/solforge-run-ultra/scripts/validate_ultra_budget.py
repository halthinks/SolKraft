#!/usr/bin/env python3
"""Validate hash-bound Ultra capability, budget, kill-switch, and lease evidence.

It verifies production trust or an explicitly gated proof fixture and never
launches native Ultra work.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_capsule import ValidationError, load_validate
from ultra_trust import (
    PRODUCTION_MODE,
    PROOF_ONLY_MODE,
    PROOF_ONLY_RUNTIME_CONFIG_SHA256,
    RUNTIME_CONFIG_ENV,
    RUNTIME_KILL_ENV,
    canonical_sha,
    verify_capability_receipt,
    verify_user_receipt,
)


FIELDS = ("max_elapsed_seconds", "max_tool_calls", "max_rounds", "max_agents", "max_cost_usd")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ZERO_HASH = "0" * 64


def attestation_hash(attestation: dict) -> str:
    return canonical_sha({k: v for k, v in attestation.items() if k != "attestation_sha256"})


def budget_hash(budget: dict) -> str:
    attestation = budget.get("capability_attestation", {})
    core = {
        "schema_version": budget.get("schema_version"),
        "validation_mode": budget.get("validation_mode"),
        "capsule_sha256": budget.get("capsule_sha256"),
        "capability_attestation_sha256": attestation.get("attestation_sha256"),
        "limits": budget.get("limits"),
        "kill_switch": budget.get("kill_switch"),
        "lease_policy": budget.get("lease_policy"),
    }
    return canonical_sha(core)


def _timestamp(value: object, name: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{name} is required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{name} must be an ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{name} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _exact_keys(value: object, expected: set[str], name: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{name} must be an object")
        return {}
    if set(value) != expected:
        errors.append(f"{name} keys mismatch")
    return value


def _hex(value: object) -> bool:
    return isinstance(value, str) and HEX64.fullmatch(value) is not None


def _validation_time(value: datetime | str | None, errors: list[str]) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            errors.append("validation time must include a timezone")
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    parsed = _timestamp(value, "validation time", errors)
    return parsed or datetime.now(timezone.utc)


def forward_control_errors(
    budget: dict,
    *,
    proof_only_fixture: bool = False,
    current_time: datetime | str | None = None,
    runtime_config_sha256: str | None = None,
    runtime_kill_switch: str | None = None,
) -> list[str]:
    """Return only live-control failures that forbid new Ultra work.

    These failures deliberately do not invalidate safe-exit operations. Static
    hashes, signatures, state bindings, and ledger integrity remain mandatory.
    Runtime overrides exist only for explicitly gated proof fixtures.
    """

    errors: list[str] = []
    mode = budget.get("validation_mode")
    if mode == PROOF_ONLY_MODE:
        if not proof_only_fixture:
            return ["proof-only fixture contract requires the explicit proof-only fixture gate"]
        expected_config = (
            runtime_config_sha256
            if runtime_config_sha256 is not None
            else PROOF_ONLY_RUNTIME_CONFIG_SHA256
        )
        kill_state = runtime_kill_switch if runtime_kill_switch is not None else "armed"
    else:
        if runtime_config_sha256 is not None or runtime_kill_switch is not None:
            errors.append("runtime control overrides are forbidden for production validation")
        expected_config = os.environ.get(RUNTIME_CONFIG_ENV, "").strip()
        kill_state = os.environ.get(RUNTIME_KILL_ENV, "").strip().lower()
        if not _hex(expected_config):
            errors.append("production runtime configuration hash is not configured")
    capability = budget.get("capability_attestation", {})
    now = _validation_time(current_time, errors)
    issued_errors: list[str] = []
    issued = _timestamp(capability.get("issued_at"), "capability issued_at", issued_errors)
    expires = _timestamp(capability.get("expires_at"), "capability expires_at", issued_errors)
    if issued and now < issued:
        errors.append("native Ultra capability attestation is not yet valid")
    if expires and expires <= now:
        errors.append("native Ultra capability attestation has expired")
    if capability.get("runtime_config_sha256") != expected_config:
        errors.append("native Ultra runtime configuration has drifted from the attestation")
    if kill_state != "armed":
        errors.append("native Ultra runtime kill switch is not armed")
    return errors


def validate_lease_ledger(state: dict, budget: dict) -> list[str]:
    """Verify the state-side single-lease SHA chain and control bindings."""
    errors: list[str] = []
    if state.get("capsule_sha256") != budget.get("capsule_sha256"):
        errors.append("state capsule binding mismatch")
    if state.get("budget_sha256") != budget_hash(budget):
        errors.append("state budget binding mismatch")
    expected_capability = budget.get("capability_attestation", {}).get("attestation_sha256")
    if state.get("capability_attestation_sha256") != expected_capability:
        errors.append("state capability binding mismatch")
    if state.get("validation_mode") != budget.get("validation_mode"):
        errors.append("state validation-mode binding mismatch")
    expected_provider_receipt = budget.get("capability_attestation", {}).get(
        "verification_receipt_sha256"
    )
    if state.get("provider_verification_receipt_sha256") != expected_provider_receipt:
        errors.append("state provider-verification receipt binding mismatch")
    expected_authorization_receipt = budget.get("authorization", {}).get("receipt_sha256")
    if state.get("authorization_receipt_sha256") != expected_authorization_receipt:
        errors.append("state user-authorization receipt binding mismatch")

    kill = state.get("kill_switch")
    if not isinstance(kill, dict):
        errors.append("state kill-switch evidence is missing")
    else:
        if kill.get("armed") is not True:
            errors.append("state kill switch is not armed")
        if kill.get("activation_receipt_sha256") != budget.get("kill_switch", {}).get("activation_receipt_sha256"):
            errors.append("state kill-switch receipt mismatch")
        if kill.get("invoked") is True and state.get("status") != "terminated":
            errors.append("invoked kill switch requires terminated state")

    ledger = state.get("lease_ledger")
    if not isinstance(ledger, dict):
        return errors + ["lease ledger evidence is missing"]
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        return errors + ["lease ledger entries must be a list"]
    previous = ZERO_HASH
    open_ids: set[str] = set()
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"lease ledger entry {index} must be an object")
            continue
        claimed = entry.get("entry_sha256")
        immutable = {k: v for k, v in entry.items() if k != "entry_sha256"}
        if entry.get("sequence") != index:
            errors.append(f"lease ledger sequence mismatch at {index}")
        if entry.get("previous_sha256") != previous:
            errors.append(f"lease ledger predecessor mismatch at {index}")
        computed = canonical_sha(immutable)
        if claimed != computed:
            errors.append(f"lease ledger hash mismatch at {index}")
        previous = computed
        lease_id = entry.get("lease_id")
        event = entry.get("event")
        if not isinstance(lease_id, str) or not lease_id.strip():
            errors.append(f"lease ledger lease_id missing at {index}")
        elif event == "acquired":
            if open_ids:
                errors.append("more than one active lease appears in the ledger")
            if lease_id in open_ids:
                errors.append(f"duplicate lease acquisition: {lease_id}")
            open_ids.add(lease_id)
        elif event in {"checkpointed", "terminated"}:
            if lease_id not in open_ids:
                errors.append(f"lease closed without acquisition: {lease_id}")
            else:
                open_ids.remove(lease_id)
            if event == "checkpointed":
                if not _hex(entry.get("checkpoint_sha256")):
                    errors.append(f"checkpoint receipt missing for lease {lease_id}")
                action_ids = entry.get("action_ids")
                disposition = entry.get("disposition")
                if not isinstance(action_ids, list) or len(action_ids) > 1:
                    errors.append(f"lease {lease_id} may contain at most one bounded action")
                elif len(action_ids) == 1 and disposition != "completed":
                    errors.append(f"completed lease {lease_id} has invalid disposition")
                elif len(action_ids) == 0 and (
                    disposition != "abandoned"
                    or not str(entry.get("abandoned_reason", "")).strip()
                ):
                    errors.append(f"empty lease {lease_id} requires an abandoned checkpoint reason")
        else:
            errors.append(f"invalid lease event at {index}")
    if ledger.get("head_sha256") != previous:
        errors.append("lease ledger head mismatch")
    active = ledger.get("active_lease")
    active_id = active.get("lease_id") if isinstance(active, dict) else None
    if set([active_id] if active_id else []) != open_ids:
        errors.append("active lease does not match the lease ledger")
    if len(open_ids) > budget.get("lease_policy", {}).get("max_active_leases", 0):
        errors.append("active lease ceiling exceeded")

    proposals = state.get("proposals")
    if not isinstance(proposals, list):
        errors.append("proposal ledger is missing")
    else:
        for index, proposal in enumerate(proposals, 1):
            if not isinstance(proposal, dict):
                errors.append(f"proposal ledger entry {index} must be an object")
                continue
            claimed = proposal.get("proposal_sha256")
            immutable = {key: value for key, value in proposal.items() if key != "proposal_sha256"}
            if proposal.get("sequence") != index:
                errors.append(f"proposal ledger sequence mismatch at {index}")
            if not str(proposal.get("id", "")).strip():
                errors.append(f"proposal ID missing at {index}")
            if not str(proposal.get("summary", "")).strip() or not str(
                proposal.get("evidence", "")
            ).strip():
                errors.append(f"proposal summary/evidence missing at {index}")
            if claimed != canonical_sha(immutable):
                errors.append(f"proposal ledger hash mismatch at {index}")
    return errors


def validate(
    budget: dict,
    capsule: dict,
    usage: dict | None = None,
    *,
    proof_only_fixture: bool = False,
    control_mode: str = "forward",
    current_time: datetime | str | None = None,
    runtime_config_sha256: str | None = None,
    runtime_kill_switch: str | None = None,
) -> list[str]:
    errors: list[str] = []
    required_top = {
        "schema_version", "validation_mode", "capsule_sha256", "capability_attestation", "limits",
        "kill_switch", "lease_policy", "authorization",
    }
    allowed_top = required_top | {"extension"}
    if not isinstance(budget, dict):
        return ["budget contract must be an object"]
    if not required_top <= set(budget) or not set(budget) <= allowed_top:
        errors.append("budget contract keys mismatch")
    if budget.get("schema_version") != "1.0.0":
        errors.append("unsupported budget schema_version")
    mode = budget.get("validation_mode")
    if mode not in {PRODUCTION_MODE, PROOF_ONLY_MODE}:
        errors.append("unsupported Ultra validation_mode")
    if control_mode not in {"forward", "safe_exit"}:
        errors.append("control_mode must be forward or safe_exit")
    capsule_sha = capsule.get("capsule_sha256")
    if budget.get("capsule_sha256") != capsule_sha:
        errors.append("capsule_sha256 mismatch")

    capability = _exact_keys(
        budget.get("capability_attestation"),
        {"schema_version", "capability", "verified", "provider", "proof_id", "issued_at", "expires_at", "max_agents", "runtime_config_sha256", "signature_algorithm", "key_id", "signature", "verification_receipt_sha256", "attestation_sha256"},
        "capability_attestation",
        errors,
    )
    if capability:
        if capability.get("schema_version") != "1.0.0":
            errors.append("unsupported capability attestation schema_version")
        if capability.get("capability") != "native_ultra" or capability.get("verified") is not True:
            errors.append("native Ultra capability is not verified")
        if not str(capability.get("provider", "")).strip() or not str(capability.get("proof_id", "")).strip():
            errors.append("capability provider and proof_id are required")
        if not str(capability.get("signature_algorithm", "")).strip() or not str(capability.get("signature", "")).strip():
            errors.append("signed capability evidence is required")
        if not str(capability.get("key_id", "")).strip():
            errors.append("capability trust-root key_id is required")
        if not _hex(capability.get("runtime_config_sha256")):
            errors.append("capability runtime configuration hash is invalid")
        if not _hex(capability.get("verification_receipt_sha256")):
            errors.append("capability verification receipt is invalid")
        if capability.get("attestation_sha256") != attestation_hash(capability):
            errors.append("capability attestation hash mismatch")
        errors.extend(
            verify_capability_receipt(
                capability,
                mode=mode,
                proof_only_fixture=proof_only_fixture,
            )
        )
        issued = _timestamp(capability.get("issued_at"), "capability issued_at", errors)
        expires = _timestamp(capability.get("expires_at"), "capability expires_at", errors)
        if issued and expires and expires <= issued:
            errors.append("capability expiry must follow issuance")
        if not isinstance(capability.get("max_agents"), int) or isinstance(capability.get("max_agents"), bool) or capability.get("max_agents", 0) < 2:
            errors.append("capability must attest at least two native Ultra agents")

    limits = _exact_keys(budget.get("limits"), set(FIELDS), "limits", errors)
    capsule_limits = capsule.get("payload", {}).get("budgets", {})
    for field in FIELDS:
        value = limits.get(field)
        if field == "max_cost_usd":
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
                errors.append(f"{field} must be finite and nonnegative")
        elif not isinstance(value, int) or isinstance(value, bool) or value < 1:
            errors.append(f"{field} must be a positive integer")
        if field in limits and field in capsule_limits and isinstance(value, (int, float)) and value > capsule_limits[field]:
            errors.append(f"{field} exceeds the capsule ceiling")
    if isinstance(limits.get("max_agents"), int) and limits.get("max_agents", 0) < 2:
        errors.append("Ultra budget must authorize at least two native Ultra agents")
    if capability and isinstance(limits.get("max_agents"), int) and limits["max_agents"] > capability.get("max_agents", 0):
        errors.append("max_agents exceeds verified native Ultra capacity")

    kill = _exact_keys(
        budget.get("kill_switch"),
        {"armed", "controller", "mechanism", "authority_expansion_allowed", "activation_receipt_sha256"},
        "kill_switch",
        errors,
    )
    if kill:
        if kill.get("armed") is not True or kill.get("controller") != "user":
            errors.append("user-controlled kill switch must be armed")
        if kill.get("mechanism") not in {"terminate", "cancel"}:
            errors.append("kill-switch mechanism must be terminate or cancel")
        if kill.get("authority_expansion_allowed") is not False:
            errors.append("kill switch cannot expand authority")
        if not _hex(kill.get("activation_receipt_sha256")):
            errors.append("kill-switch activation receipt is invalid")

    lease = _exact_keys(
        budget.get("lease_policy"),
        {"max_active_leases", "bounded_units_per_lease", "checkpoint_before_reacquire", "sha256_chain_required", "receipt_sha256"},
        "lease_policy",
        errors,
    )
    if lease:
        if lease.get("max_active_leases") != 1 or lease.get("bounded_units_per_lease") != 1:
            errors.append("Ultra requires one active lease and one bounded unit per lease")
        if lease.get("checkpoint_before_reacquire") is not True or lease.get("sha256_chain_required") is not True:
            errors.append("lease policy must require checkpoint and SHA-256 chaining")
        if not _hex(lease.get("receipt_sha256")):
            errors.append("lease-policy receipt is invalid")

    auth = _exact_keys(
        budget.get("authorization"),
        {"authorized_by", "confirmation_text", "confirmed_at", "capsule_sha256", "budget_sha256", "signature_algorithm", "key_id", "signature", "receipt_sha256"},
        "authorization",
        errors,
    )
    expected_budget_sha = budget_hash(budget)
    if auth:
        if auth.get("authorized_by") != "user" or not str(auth.get("confirmation_text", "")).strip():
            errors.append("authorization must contain user-authored confirmation")
        _timestamp(auth.get("confirmed_at"), "authorization confirmed_at", errors)
        if auth.get("capsule_sha256") != capsule_sha:
            errors.append("authorization is not bound to capsule")
        if auth.get("budget_sha256") != expected_budget_sha:
            errors.append("authorization is not bound to the complete Ultra control contract")
        errors.extend(
            verify_user_receipt(
                auth,
                mode=mode,
                proof_only_fixture=proof_only_fixture,
                kind="authorization",
            )
        )

    extension = budget.get("extension")
    if extension is not None:
        extension = _exact_keys(
            extension,
            {"old_budget_sha256", "new_budget_sha256", "reason", "authorized_by", "confirmation_text", "confirmed_at", "signature_algorithm", "key_id", "signature", "receipt_sha256"},
            "extension",
            errors,
        )
        if extension:
            if extension.get("new_budget_sha256") != expected_budget_sha:
                errors.append("extension new budget hash mismatch")
            if not _hex(extension.get("old_budget_sha256")) or extension.get("old_budget_sha256") == expected_budget_sha:
                errors.append("extension must bind a distinct old budget hash")
            if extension.get("authorized_by") != "user" or not str(extension.get("confirmation_text", "")).strip():
                errors.append("budget extension requires new user confirmation")
            if not str(extension.get("reason", "")).strip():
                errors.append("budget extension reason is required")
            _timestamp(extension.get("confirmed_at"), "extension confirmed_at", errors)
            errors.extend(
                verify_user_receipt(
                    extension,
                    mode=mode,
                    proof_only_fixture=proof_only_fixture,
                    kind="extension",
                )
            )

    if control_mode == "forward":
        errors.extend(
            forward_control_errors(
                budget,
                proof_only_fixture=proof_only_fixture,
                current_time=current_time,
                runtime_config_sha256=runtime_config_sha256,
                runtime_kill_switch=runtime_kill_switch,
            )
        )
    elif not proof_only_fixture and (
        runtime_config_sha256 is not None or runtime_kill_switch is not None
    ):
        errors.append("runtime control overrides are forbidden for production validation")

    if usage is not None and limits:
        state = usage if "usage" in usage else {"usage": usage}
        counters = state.get("usage", {})
        mapping = {
            "elapsed_seconds": "max_elapsed_seconds", "tool_calls": "max_tool_calls",
            "rounds": "max_rounds", "agents": "max_agents", "cost_usd": "max_cost_usd",
        }
        for used_field, limit_field in mapping.items():
            used = counters.get(used_field, 0)
            if not isinstance(used, (int, float)) or isinstance(used, bool) or not math.isfinite(used) or used < 0:
                errors.append(f"invalid usage {used_field}")
            elif used > limits[limit_field]:
                errors.append(f"hard ceiling exceeded: {used_field}")
        if "usage" in usage:
            errors.extend(validate_lease_ledger(usage, budget))
    return errors


def load_budget(path: str | Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read Ultra budget contract: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("budget")
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--usage")
    parser.add_argument(
        "--proof-only-fixture",
        action="store_true",
        help="accept only an explicitly labeled proof-only fixture contract",
    )
    parser.add_argument(
        "--safe-exit",
        action="store_true",
        help="verify immutable controls while allowing expiry/config/kill drift",
    )
    parser.add_argument("--validation-time", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-config-sha256", help=argparse.SUPPRESS)
    parser.add_argument("--runtime-kill-switch", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        capsule = load_validate(args.capsule)
        budget = load_budget(args.budget)
        usage = json.loads(Path(args.usage).read_text(encoding="utf-8")) if args.usage else None
        if (
            args.validation_time is not None
            or args.runtime_config_sha256 is not None
            or args.runtime_kill_switch is not None
        ) and not args.proof_only_fixture:
            raise ValidationError("runtime validation overrides require --proof-only-fixture")
        errors = validate(
            budget,
            capsule,
            usage,
            proof_only_fixture=args.proof_only_fixture,
            control_mode="safe_exit" if args.safe_exit else "forward",
            current_time=args.validation_time,
            runtime_config_sha256=args.runtime_config_sha256,
            runtime_kill_switch=args.runtime_kill_switch,
        )
    except (ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    mode = budget.get("validation_mode")
    gate = "safe-exit" if args.safe_exit else "forward"
    print(
        f"PASS: {mode} Ultra provider/user receipts, budget, kill-switch, and lease "
        f"controls are valid for {gate}; no Ultra execution was launched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
