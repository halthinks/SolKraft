#!/usr/bin/env python3
"""Proof-only tests for Ultra capability, budget, lease, and kill controls."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True

from validate_capsule import canonical_hash, validate as validate_capsule
from validate_ultra_budget import (
    attestation_hash,
    budget_hash,
    forward_control_errors,
    validate,
)
from ultra_trust import (
    HMAC_ALGORITHM,
    PROOF_HMAC_ALGORITHM,
    PROOF_ONLY_MODE,
    PROOF_ONLY_PROVIDER_KEY_ID,
    PROOF_ONLY_PROVIDER_SECRET,
    PROOF_ONLY_RUNTIME_CONFIG_SHA256,
    PROOF_ONLY_USER_KEY_ID,
    PROOF_ONLY_USER_SECRET,
    PRODUCTION_MODE,
    authorization_signature_payload,
    authorization_verification_receipt,
    capability_signature_payload,
    capability_verification_receipt,
    hmac_signature,
)


ROOT = Path(__file__).resolve().parent
HEX_A = "a" * 64
HEX_B = "b" * 64
HEX_C = "c" * 64


def valid_capsule() -> dict:
    capsule = {
        "schema_version": "1.0.0",
        "profile": "ultra",
        "capsule_id": "proof-only-ultra",
        "payload": {
            "original_request": "inspect the proof fixture with python",
            "structured_intent": {
                "objective": "Verify the proof-only Ultra control path.",
                "inputs": [],
                "constraints": [],
                "deliverables": ["proof receipt"],
                "acceptance_criteria": ["control path passes"],
                "authorization_boundaries": [],
            },
            "hardened_prompt": "Verify controls without launching Ultra.",
            "solforge_provenance": "profile=ultra; execution_boundary=transpose_only",
            "requirements": [{"id": "REQ-1", "text": "control path passes"}],
            "scope": {"in_scope": [str(ROOT)], "out_of_scope": []},
            "authorization": {
                "allowed_actions": ["inspect"],
                "prohibited_actions": [],
                "allowed_tools": ["python"],
                "permission_evidence": [
                    {"permission": "inspect", "basis": "user_explicit", "evidence": "inspect"},
                    {"permission": "python", "basis": "user_explicit", "evidence": "python"},
                ],
                "mutation_allowed": False,
                "external_side_effects_allowed": False,
            },
            "risks": {"categories": [], "high_consequence": False},
            "budgets": {
                "max_elapsed_seconds": 60,
                "max_tool_calls": 10,
                "max_rounds": 2,
                "max_agents": 2,
                "max_cost_usd": 1.0,
            },
            "retry_limit": 1,
            "source_artifacts": [],
        },
        "capsule_sha256": "0" * 64,
        "confirmation": None,
    }
    capsule["capsule_sha256"] = canonical_hash(capsule)
    validate_capsule(capsule)
    return capsule


def sign_capability(capability: dict, secret: bytes) -> None:
    capability["signature"] = hmac_signature(secret, capability_signature_payload(capability))
    capability["verification_receipt_sha256"] = capability_verification_receipt(capability)
    capability["attestation_sha256"] = attestation_hash(capability)


def sign_authorization(authorization: dict, secret: bytes, *, kind: str) -> None:
    authorization["signature"] = hmac_signature(
        secret, authorization_signature_payload(authorization, kind=kind)
    )
    authorization["receipt_sha256"] = authorization_verification_receipt(
        authorization, kind=kind
    )


def valid_budget(
    capsule: dict,
    max_rounds: int = 2,
    *,
    mode: str = PROOF_ONLY_MODE,
    issued: datetime | None = None,
    provider_key_id: str = PROOF_ONLY_PROVIDER_KEY_ID,
    provider_secret: bytes = PROOF_ONLY_PROVIDER_SECRET,
    user_key_id: str = PROOF_ONLY_USER_KEY_ID,
    user_secret: bytes = PROOF_ONLY_USER_SECRET,
    runtime_config_sha256: str = PROOF_ONLY_RUNTIME_CONFIG_SHA256,
) -> dict:
    issued = issued or datetime.now(timezone.utc).replace(microsecond=0)
    algorithm = PROOF_HMAC_ALGORITHM if mode == PROOF_ONLY_MODE else HMAC_ALGORITHM
    capability = {
        "schema_version": "1.0.0",
        "capability": "native_ultra",
        "verified": True,
        "provider": "proof-only-runtime" if mode == PROOF_ONLY_MODE else "test-production-runtime",
        "proof_id": "proof-only-capability" if mode == PROOF_ONLY_MODE else "production-capability",
        "issued_at": issued.isoformat().replace("+00:00", "Z"),
        "expires_at": (issued + timedelta(hours=1)).isoformat().replace("+00:00", "Z"),
        "max_agents": 2,
        "runtime_config_sha256": runtime_config_sha256,
        "signature_algorithm": algorithm,
        "key_id": provider_key_id,
        "signature": "0" * 64,
        "verification_receipt_sha256": "0" * 64,
        "attestation_sha256": "0" * 64,
    }
    sign_capability(capability, provider_secret)
    budget = {
        "schema_version": "1.0.0",
        "validation_mode": mode,
        "capsule_sha256": capsule["capsule_sha256"],
        "capability_attestation": capability,
        "limits": {
            "max_elapsed_seconds": 60,
            "max_tool_calls": 10,
            "max_rounds": max_rounds,
            "max_agents": 2,
            "max_cost_usd": 1.0,
        },
        "kill_switch": {
            "armed": True,
            "controller": "user",
            "mechanism": "terminate",
            "authority_expansion_allowed": False,
            "activation_receipt_sha256": HEX_B,
        },
        "lease_policy": {
            "max_active_leases": 1,
            "bounded_units_per_lease": 1,
            "checkpoint_before_reacquire": True,
            "sha256_chain_required": True,
            "receipt_sha256": HEX_C,
        },
        "authorization": {
            "authorized_by": "user",
            "confirmation_text": "I authorize this bounded proof-only Ultra control test.",
            "confirmed_at": issued.isoformat().replace("+00:00", "Z"),
            "capsule_sha256": capsule["capsule_sha256"],
            "budget_sha256": "0" * 64,
            "signature_algorithm": algorithm,
            "key_id": user_key_id,
            "signature": "0" * 64,
            "receipt_sha256": "0" * 64,
        },
    }
    budget["authorization"]["budget_sha256"] = budget_hash(budget)
    sign_authorization(budget["authorization"], user_secret, kind="authorization")
    return budget


def require_failure(
    name: str,
    budget: dict,
    capsule: dict,
    state: dict | None = None,
    **validation,
) -> None:
    if not validate(budget, capsule, state, **validation):
        raise AssertionError(f"{name} unexpectedly passed")


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if result.returncode != expect:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expect}: {' '.join(args)}\n"
            f"stdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


def lifecycle_proof(capsule: dict, budget: dict, directory: Path) -> None:
    capsule_path = directory / "capsule.json"
    budget_path = directory / "budget.json"
    state_path = directory / "state.json"
    capsule_path.write_text(json.dumps(capsule, indent=4) + "\n", encoding="utf-8")
    budget_path.write_text(json.dumps(budget, indent=2) + "\n", encoding="utf-8")
    common = [str(capsule_path), str(budget_path), str(state_path), "--proof-only-fixture"]
    run("execution_state.py", "init", *common)
    run("execution_state.py", "transition", *common, "ready")
    run("execution_state.py", "transition", *common, "executing")
    run("execution_state.py", "approach", *common, "proof", "control", "accepted", "--evidence", "selftest")
    run("execution_state.py", "lease-open", *common, "lease-1", "--unit", "one proof-only action")
    run("execution_state.py", "lease-open", *common, "lease-2", "--unit", "forbidden parallel action", expect=1)
    run(
        "execution_state.py", "action", *common, "lease-1", "action-1", "inspect", str(ROOT),
        "--requirement-id", "REQ-1", "--tool", "python", "--expected", "controls pass",
        "--actual", "controls passed", "--evidence", "selftest receipt", "--tools", "1",
        "--rounds", "1", "--agents", "2",
    )
    run("execution_state.py", "lease-close", *common, "lease-1", "--checkpoint-sha256", HEX_A)
    run("execution_state.py", "evidence", *common, "REQ-1", "selftest_ultra.py", "proof-only subprocess", "passed")
    run("execution_state.py", "transition", *common, "verifying")
    run("execution_state.py", "transition", *common, "adversarial_audit")
    run(
        "validate_ultra_budget.py",
        str(budget_path),
        "--capsule",
        str(capsule_path),
        "--usage",
        str(state_path),
        "--proof-only-fixture",
    )
    run("acceptance_audit.py", *common, "--complete")
    completed = json.loads(state_path.read_text(encoding="utf-8"))
    assert completed["status"] == "complete"
    assert completed["usage"]["agents"] == 2
    assert completed["audit_receipt"]["budget_sha256"] == budget_hash(budget)
    assert completed["audit_receipt"]["lease_ledger_head_sha256"] == completed["lease_ledger"]["head_sha256"]

    killed_state = directory / "killed-state.json"
    killed_common = [
        str(capsule_path),
        str(budget_path),
        str(killed_state),
        "--proof-only-fixture",
    ]
    run("execution_state.py", "init", *killed_common)
    run("execution_state.py", "transition", *killed_common, "ready")
    run("execution_state.py", "transition", *killed_common, "executing")
    run("execution_state.py", "lease-open", *killed_common, "kill-lease", "--unit", "pending proof")
    run("execution_state.py", "kill", *killed_common, "--reason", "proof-only user kill")
    killed = json.loads(killed_state.read_text(encoding="utf-8"))
    assert killed["status"] == "terminated"
    assert killed["kill_switch"]["invoked"] is True
    assert killed["lease_ledger"]["active_lease"] is None
    run("acceptance_audit.py", *killed_common, expect=1)


def safe_exit_drift_proof(capsule: dict, directory: Path) -> None:
    issued = datetime.now(timezone.utc).replace(microsecond=0)
    valid_time = (issued + timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
    drift_time = (issued + timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    budget = valid_budget(capsule, issued=issued)
    capsule_path = directory / "drift-capsule.json"
    budget_path = directory / "drift-budget.json"
    state_path = directory / "drift-state.json"
    capsule_path.write_text(json.dumps(capsule, indent=2) + "\n", encoding="utf-8")
    budget_path.write_text(json.dumps(budget, indent=2) + "\n", encoding="utf-8")

    def common(path: Path, when: str, *, drift: bool = False) -> list[str]:
        result = [
            str(capsule_path),
            str(budget_path),
            str(path),
            "--proof-only-fixture",
            "--validation-time",
            when,
        ]
        if drift:
            result.extend(
                [
                    "--runtime-config-sha256",
                    HEX_A,
                    "--runtime-kill-switch",
                    "disarmed",
                ]
            )
        return result

    live = common(state_path, valid_time)
    drift = common(state_path, drift_time, drift=True)
    expired_init_path = directory / "expired-init-state.json"
    run(
        "execution_state.py",
        "init",
        *common(expired_init_path, drift_time, drift=True),
        expect=1,
    )
    run("execution_state.py", "init", *live)
    run("execution_state.py", "transition", *live, "ready")
    run("execution_state.py", "transition", *live, "executing")
    run(
        "execution_state.py",
        "approach",
        *live,
        "safe-exit",
        "control",
        "accepted",
        "--evidence",
        "pre-drift approach receipt",
    )
    run("execution_state.py", "lease-open", *live, "lease-drift", "--unit", "bounded action")

    # Expiry, runtime configuration drift, and a disarmed live kill gate block
    # every operation that could start, resume, acquire, or derive more work.
    run("execution_state.py", "lease-open", *drift, "lease-new", "--unit", "forbidden", expect=1)
    run(
        "execution_state.py",
        "approach",
        *drift,
        "derived-after-drift",
        "forbidden",
        "candidate",
        expect=1,
    )

    # Recording an already-completed bounded action/evidence and checkpointing
    # the lease remain available, as do final verification and acceptance.
    run(
        "execution_state.py",
        "action",
        *drift,
        "lease-drift",
        "action-drift",
        "inspect",
        str(ROOT),
        "--requirement-id",
        "REQ-1",
        "--tool",
        "python",
        "--expected",
        "controls pass",
        "--actual",
        "completed before drift was observed",
        "--evidence",
        "sealed completion receipt",
        "--tools",
        "1",
        "--rounds",
        "1",
        "--agents",
        "2",
    )
    run(
        "execution_state.py",
        "evidence",
        *drift,
        "REQ-1",
        "safe-exit receipt",
        "proof-only adversarial subprocess",
        "passed",
    )
    run(
        "execution_state.py",
        "proposal",
        *drift,
        "proposal-safe-exit",
        "--summary",
        "Preserve the completed proof and request a newly authorized capability before more work.",
        "--evidence",
        "observed expiry, runtime-config drift, and disarmed kill gate",
    )
    run(
        "execution_state.py",
        "lease-close",
        *drift,
        "lease-drift",
        "--checkpoint-sha256",
        HEX_B,
    )
    run("execution_state.py", "transition", *drift, "verifying")
    run("execution_state.py", "transition", *drift, "adversarial_audit")
    run("acceptance_audit.py", *drift, "--complete")
    completed = json.loads(state_path.read_text(encoding="utf-8"))
    assert completed["status"] == "complete"
    assert completed["proposals"][0]["id"] == "proposal-safe-exit"
    observed = completed["audit_receipt"]["forward_control_drift_at_completion"]
    assert any("expired" in row for row in observed)
    assert any("configuration has drifted" in row for row in observed)
    assert any("kill switch is not armed" in row for row in observed)

    # A paused/abandoned lease may be checkpointed without claiming an action.
    paused_path = directory / "paused-state.json"
    paused_live = common(paused_path, valid_time)
    paused_drift = common(paused_path, drift_time, drift=True)
    run("execution_state.py", "init", *paused_live)
    run("execution_state.py", "transition", *paused_live, "ready")
    run("execution_state.py", "transition", *paused_live, "executing")
    run("execution_state.py", "lease-open", *paused_live, "lease-pause", "--unit", "not started")
    run(
        "execution_state.py",
        "lease-close",
        *paused_drift,
        "lease-pause",
        "--checkpoint-sha256",
        HEX_C,
        "--abandoned-reason",
        "live controls drifted before the bounded action started",
    )
    run("execution_state.py", "transition", *paused_drift, "declined", "--reason", "user declined continuation")

    # Kill must remain available even with an active lease and all live gates bad.
    killed_path = directory / "drift-killed-state.json"
    killed_live = common(killed_path, valid_time)
    killed_drift = common(killed_path, drift_time, drift=True)
    run("execution_state.py", "init", *killed_live)
    run("execution_state.py", "transition", *killed_live, "ready")
    run("execution_state.py", "transition", *killed_live, "executing")
    run("execution_state.py", "lease-open", *killed_live, "lease-kill", "--unit", "pending")
    run("execution_state.py", "kill", *killed_drift, "--reason", "control drift emergency stop")
    killed = json.loads(killed_path.read_text(encoding="utf-8"))
    assert killed["status"] == "terminated"
    assert killed["kill_switch"]["invoked"] is True

    # A state that has not started cannot cross the execution boundary after drift.
    resume_path = directory / "resume-state.json"
    resume_live = common(resume_path, valid_time)
    resume_drift = common(resume_path, drift_time, drift=True)
    run("execution_state.py", "init", *resume_live)
    run("execution_state.py", "transition", *resume_live, "ready")
    run("execution_state.py", "transition", *resume_drift, "executing", expect=1)


def main() -> int:
    capsule = valid_capsule()
    good = valid_budget(capsule)
    proof = {"proof_only_fixture": True}
    assert validate(good, capsule, **proof) == []
    require_failure("proof fixture accepted without explicit gate", good, capsule)
    bad = copy.deepcopy(good)
    bad["capability_attestation"]["verified"] = False
    require_failure("missing capability", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["capability_attestation"]["attestation_sha256"] = HEX_A
    require_failure("tampered attestation", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["capability_attestation"]["signature"] = HEX_A
    bad["capability_attestation"]["verification_receipt_sha256"] = (
        capability_verification_receipt(bad["capability_attestation"])
    )
    bad["capability_attestation"]["attestation_sha256"] = attestation_hash(
        bad["capability_attestation"]
    )
    require_failure("fabricated capability signature and self-hashes", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["authorization"]["signature"] = HEX_B
    bad["authorization"]["receipt_sha256"] = authorization_verification_receipt(
        bad["authorization"], kind="authorization"
    )
    require_failure("fabricated user authorization receipt", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["limits"]["max_agents"] = 1
    require_failure("single agent", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["kill_switch"]["armed"] = False
    require_failure("disarmed sealed kill switch", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["lease_policy"]["max_active_leases"] = 2
    require_failure("parallel leases", bad, capsule, **proof)
    bad = copy.deepcopy(good)
    bad["capsule_sha256"] = HEX_A
    require_failure("tampered canonical capsule binding", bad, capsule, **proof)
    require_failure("over budget", good, capsule, {"elapsed_seconds": 61}, **proof)

    with patch.dict(os.environ, {"SOLFORGE_ENV": "production"}, clear=False):
        require_failure("proof fixture enabled in production", good, capsule, **proof)

    provider_secret = b"P" * 32
    user_secret = b"U" * 32
    provider_key_id = "test-production-provider"
    user_key_id = "test-production-user"
    production = valid_budget(
        capsule,
        mode=PRODUCTION_MODE,
        provider_key_id=provider_key_id,
        provider_secret=provider_secret,
        user_key_id=user_key_id,
        user_secret=user_secret,
        runtime_config_sha256=HEX_C,
    )
    production_env = {
        "SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_ID": provider_key_id,
        "SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_SECRET": provider_secret.decode("ascii"),
        "SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_ID": user_key_id,
        "SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_SECRET": user_secret.decode("ascii"),
        "SOLFORGE_ULTRA_RUNTIME_CONFIG_SHA256": HEX_C,
        "SOLFORGE_ULTRA_KILL_SWITCH": "armed",
    }
    with patch.dict(os.environ, production_env, clear=False):
        assert validate(production, capsule) == []
        require_failure(
            "production contract accepted with proof-only gate",
            production,
            capsule,
            proof_only_fixture=True,
        )
        bad = copy.deepcopy(production)
        bad["capability_attestation"]["signature"] = HEX_A
        bad["capability_attestation"]["verification_receipt_sha256"] = (
            capability_verification_receipt(bad["capability_attestation"])
        )
        bad["capability_attestation"]["attestation_sha256"] = attestation_hash(
            bad["capability_attestation"]
        )
        require_failure("production fabricated provider receipt", bad, capsule)
        bad = copy.deepcopy(production)
        bad["authorization"]["signature"] = HEX_B
        bad["authorization"]["receipt_sha256"] = authorization_verification_receipt(
            bad["authorization"], kind="authorization"
        )
        require_failure("production fabricated user receipt", bad, capsule)
        bad = copy.deepcopy(production)
        bad["capability_attestation"]["key_id"] = user_key_id
        sign_capability(bad["capability_attestation"], user_secret)
        require_failure("provider capability signed by user trust root", bad, capsule)
        drift = forward_control_errors(
            production,
            runtime_config_sha256=None,
            runtime_kill_switch=None,
        )
        assert drift == []

    extended = valid_budget(capsule, max_rounds=1)
    old_hash = budget_hash(extended)
    extended["limits"]["max_rounds"] = 2
    new_hash = budget_hash(extended)
    extended["authorization"]["budget_sha256"] = new_hash
    sign_authorization(extended["authorization"], PROOF_ONLY_USER_SECRET, kind="authorization")
    extended["extension"] = {
        "old_budget_sha256": old_hash,
        "new_budget_sha256": new_hash,
        "reason": "User approved one additional proof-only round.",
        "authorized_by": "user",
        "confirmation_text": "I approve the stated bounded extension.",
        "confirmed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "signature_algorithm": PROOF_HMAC_ALGORITHM,
        "key_id": PROOF_ONLY_USER_KEY_ID,
        "signature": "0" * 64,
        "receipt_sha256": "0" * 64,
    }
    sign_authorization(extended["extension"], PROOF_ONLY_USER_SECRET, kind="extension")
    assert validate(extended, capsule, **proof) == []
    bad = copy.deepcopy(extended)
    bad["extension"]["confirmation_text"] = ""
    require_failure("invalid extension", bad, capsule, **proof)

    with tempfile.TemporaryDirectory(prefix="solforge-ultra-proof-") as temporary:
        directory = Path(temporary)
        lifecycle_proof(capsule, good, directory)
        safe_exit_drift_proof(capsule, directory)
    print(
        "PASS: production HMAC trust rejection, proof-only controls, safe-exit drift, "
        "and lifecycle verified; no native Ultra work was launched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
