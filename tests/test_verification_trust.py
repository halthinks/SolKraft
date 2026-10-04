import inspect

from solkraft.audit import route_audit_event, verification_audit_event
from solkraft.contract_verify import verify_contract
from solkraft.sandbox import (
    CORE_EXECUTABLE_VERIFIERS_ENABLED,
    DEFAULT_VERIFIER_SANDBOX,
    validate_adapter_manifest,
)
from solkraft.trust import resolve_trust
import solkraft.sandbox as sandbox_module


def _contract():
    return {
        "status": "declared",
        "contract_digest": "sha256:contract",
        "entrypoint_digest": "sha256:entry",
        "side_effects": ["repo.push"],
        "verification": {
            "mode": "declarative",
            "checks": [
                {"id": "receipt", "type": "artifact_exists", "artifact": "receipt"},
                {"id": "healthy", "type": "check_equals", "check": "healthy", "expected": True},
                {"id": "effects", "type": "observed_effects_subset"},
            ],
        },
    }


def _evidence(**changes):
    value = {
        "skill_id": "demo",
        "contract_digest": "sha256:contract",
        "entrypoint_digest": "sha256:entry",
        "artifacts": [{"name": "receipt", "sha256": "abc"}],
        "observed_effects": ["repo.push"],
        "fields": {},
        "checks": {"healthy": True},
        "host_receipt": "host-1",
    }
    value.update(changes)
    return value


def test_declarative_verifier_passes_from_evidence_only():
    result = verify_contract(_contract(), _evidence())
    assert result["state"] == "verified"
    assert result["passed"] is True
    assert all(item["passed"] for item in result["checks"])


def test_digest_drift_fails_verification():
    result = verify_contract(
        _contract(),
        _evidence(entrypoint_digest="sha256:changed"),
    )
    assert result["state"] == "verification-failed"
    assert "entrypoint digest" in result["errors"][0]


def test_contract_without_checks_is_executed_unverified():
    contract = _contract()
    contract["verification"] = {"mode": "declarative", "checks": []}
    result = verify_contract(contract, _evidence())
    assert result["state"] == "executed-unverified"
    assert result["passed"] is False


def test_unsupported_check_fails_safely():
    contract = _contract()
    contract["verification"]["checks"] = [{"id": "x", "type": "shell"}]
    result = verify_contract(contract, _evidence())
    assert result["state"] == "verification-failed"
    assert "unsupported declarative check type" in result["checks"][0]["reason"]


def test_skill_authored_provenance_cannot_self_elevate_trust():
    contract = {
        "status": "declared",
        "contract_digest": "sha256:c",
        "entrypoint_digest": "sha256:e",
        "provenance": {"trust": "bundled-reviewed", "reviewer": "self"},
    }
    resolved = resolve_trust("demo", contract, registry={})
    assert resolved["state"] == "local-unreviewed"
    assert resolved["trusted"] is False


def test_external_digest_binding_grants_and_drift_revokes_trust():
    contract = {
        "status": "declared",
        "contract_digest": "sha256:c",
        "entrypoint_digest": "sha256:e",
    }
    registry = {
        "demo": {
            "state": "bundled-reviewed",
            "contract_digest": "sha256:c",
            "entrypoint_digest": "sha256:e",
            "reviewer": "maintainer",
            "revision": 1,
        }
    }
    trusted = resolve_trust("demo", contract, registry=registry)
    assert trusted["state"] == "bundled-reviewed"
    assert trusted["trusted"] is True

    changed = dict(contract, entrypoint_digest="sha256:changed")
    revoked = resolve_trust("demo", changed, registry=registry)
    assert revoked["state"] == "local-unreviewed"
    assert revoked["trusted"] is False


def test_legacy_metadata_is_never_reviewed_by_inference():
    resolved = resolve_trust("demo", {"status": "legacy"}, registry={})
    assert resolved["state"] == "legacy-inferred"
    assert resolved["trusted"] is False


def test_audit_receipts_are_deterministic():
    route = {
        "objective": "Inspect it",
        "selected": ["demo"],
        "selection_status": "matched",
        "route_policy": {"contract_mode": "strict"},
        "contract_decisions": {
            "demo": {
                "contract_status": "declared",
                "trust": {"state": "local-unreviewed"},
                "contract_digest": "sha256:c",
                "entrypoint_digest": "sha256:e",
            }
        },
        "required_capabilities": ["repo.read"],
        "required_resources": ["repo:demo"],
        "blocked_stages": [],
    }
    assert route_audit_event(route)["digest"] == route_audit_event(route)["digest"]

    verified = verify_contract(_contract(), _evidence())
    event = verification_audit_event("demo", verified)
    assert event["payload"]["state"] == "verified"
    assert event["payload"]["evidence_digest"].startswith("sha256:")


def test_core_sandbox_defines_requirements_but_has_no_executor():
    assert CORE_EXECUTABLE_VERIFIERS_ENABLED is False
    assert DEFAULT_VERIFIER_SANDBOX.network is False
    assert DEFAULT_VERIFIER_SANDBOX.inherit_secrets is False
    assert "subprocess" not in inspect.getsource(sandbox_module)
    errors = validate_adapter_manifest({
        "network": True,
        "inherit_secrets": True,
        "timeout_seconds": 601,
    })
    assert len(errors) == 3
