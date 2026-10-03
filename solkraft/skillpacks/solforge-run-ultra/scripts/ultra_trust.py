#!/usr/bin/env python3
"""Cryptographic trust primitives for SolForge Ultra control contracts.

Production verification uses two independently configured HMAC-SHA256 trust
roots: one for the native-Ultra provider and one for the user's authorization
service.  The fixed keys in this module are deliberately restricted to the
explicit proof-only fixture mode; they are public test data, not trust roots.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Mapping


PRODUCTION_MODE = "production"
PROOF_ONLY_MODE = "proof_only_fixture"
HMAC_ALGORITHM = "hmac-sha256"
PROOF_HMAC_ALGORITHM = "proof-only-hmac-sha256"

PROOF_ONLY_PROVIDER_KEY_ID = "solforge-proof-only-provider-v1"
PROOF_ONLY_USER_KEY_ID = "solforge-proof-only-user-v1"
PROOF_ONLY_PROVIDER_SECRET = b"solforge-public-proof-only-provider-key-v1"
PROOF_ONLY_USER_SECRET = b"solforge-public-proof-only-user-auth-key-v1"
PROOF_ONLY_RUNTIME_CONFIG_SHA256 = hashlib.sha256(
    b"solforge-proof-only-runtime-config-v1"
).hexdigest()

PROVIDER_KEY_ID_ENV = "SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_ID"
PROVIDER_SECRET_ENV = "SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_SECRET"
USER_KEY_ID_ENV = "SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_ID"
USER_SECRET_ENV = "SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_SECRET"
RUNTIME_CONFIG_ENV = "SOLFORGE_ULTRA_RUNTIME_CONFIG_SHA256"
RUNTIME_KILL_ENV = "SOLFORGE_ULTRA_KILL_SWITCH"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_sha(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def hmac_signature(secret: bytes, value: object) -> str:
    return hmac.new(secret, canonical_bytes(value), hashlib.sha256).hexdigest()


def capability_signature_payload(attestation: Mapping[str, object]) -> dict:
    return {
        key: attestation.get(key)
        for key in (
            "schema_version",
            "capability",
            "verified",
            "provider",
            "proof_id",
            "issued_at",
            "expires_at",
            "max_agents",
            "runtime_config_sha256",
            "signature_algorithm",
            "key_id",
        )
    }


def capability_verification_receipt(attestation: Mapping[str, object]) -> str:
    payload = capability_signature_payload(attestation)
    return canonical_sha(
        {
            "schema_version": "1.0.0",
            "kind": "solforge.native_ultra.provider_verification",
            "payload_sha256": canonical_sha(payload),
            "signature_algorithm": attestation.get("signature_algorithm"),
            "key_id": attestation.get("key_id"),
            "signature": attestation.get("signature"),
        }
    )


def authorization_signature_payload(
    authorization: Mapping[str, object], *, kind: str
) -> dict:
    if kind == "authorization":
        fields = (
            "authorized_by",
            "confirmation_text",
            "confirmed_at",
            "capsule_sha256",
            "budget_sha256",
            "signature_algorithm",
            "key_id",
        )
    elif kind == "extension":
        fields = (
            "old_budget_sha256",
            "new_budget_sha256",
            "reason",
            "authorized_by",
            "confirmation_text",
            "confirmed_at",
            "signature_algorithm",
            "key_id",
        )
    else:
        raise ValueError(f"unsupported authorization receipt kind: {kind}")
    return {key: authorization.get(key) for key in fields}


def authorization_verification_receipt(
    authorization: Mapping[str, object], *, kind: str
) -> str:
    payload = authorization_signature_payload(authorization, kind=kind)
    receipt_kind = (
        "solforge.native_ultra.user_authorization"
        if kind == "authorization"
        else "solforge.native_ultra.user_budget_extension"
    )
    return canonical_sha(
        {
            "schema_version": "1.0.0",
            "kind": receipt_kind,
            "payload_sha256": canonical_sha(payload),
            "signature_algorithm": authorization.get("signature_algorithm"),
            "key_id": authorization.get("key_id"),
            "signature": authorization.get("signature"),
        }
    )


def _production_root(id_env: str, secret_env: str, label: str) -> tuple[str, bytes, list[str]]:
    errors: list[str] = []
    key_id = os.environ.get(id_env, "").strip()
    secret_text = os.environ.get(secret_env, "")
    secret = secret_text.encode("utf-8")
    if not key_id:
        errors.append(f"{label} trust-root ID is not configured")
    if len(secret) < 32:
        errors.append(f"{label} trust-root secret must contain at least 32 UTF-8 bytes")
    return key_id, secret, errors


def _root_for(mode: str, purpose: str, proof_only_fixture: bool) -> tuple[str, bytes, str, list[str]]:
    errors: list[str] = []
    if mode == PROOF_ONLY_MODE:
        if not proof_only_fixture:
            return "", b"", PROOF_HMAC_ALGORITHM, [
                "proof-only fixture contract requires the explicit proof-only fixture gate"
            ]
        if os.environ.get("SOLFORGE_ENV", "").strip().lower() in {
            "prod",
            "production",
            "live",
        }:
            return "", b"", PROOF_HMAC_ALGORITHM, [
                "proof-only fixture mode is forbidden in a production environment"
            ]
        if purpose == "provider":
            return (
                PROOF_ONLY_PROVIDER_KEY_ID,
                PROOF_ONLY_PROVIDER_SECRET,
                PROOF_HMAC_ALGORITHM,
                errors,
            )
        return (
            PROOF_ONLY_USER_KEY_ID,
            PROOF_ONLY_USER_SECRET,
            PROOF_HMAC_ALGORITHM,
            errors,
        )
    if mode != PRODUCTION_MODE:
        return "", b"", HMAC_ALGORITHM, ["unsupported Ultra validation_mode"]
    if proof_only_fixture:
        errors.append("proof-only fixture gate cannot validate a production contract")
    if purpose == "provider":
        key_id, secret, root_errors = _production_root(
            PROVIDER_KEY_ID_ENV, PROVIDER_SECRET_ENV, "provider"
        )
    else:
        key_id, secret, root_errors = _production_root(
            USER_KEY_ID_ENV, USER_SECRET_ENV, "user authorization"
        )
    return key_id, secret, HMAC_ALGORITHM, errors + root_errors


def verify_capability_receipt(
    attestation: Mapping[str, object], *, mode: str, proof_only_fixture: bool
) -> list[str]:
    key_id, secret, algorithm, errors = _root_for(
        mode, "provider", proof_only_fixture
    )
    if attestation.get("signature_algorithm") != algorithm:
        errors.append("capability signature algorithm is not permitted for this validation mode")
    if attestation.get("key_id") != key_id:
        errors.append("capability key_id does not match the configured provider trust root")
    signature = attestation.get("signature")
    if not isinstance(signature, str) or len(signature) != 64:
        errors.append("capability signature must be a lowercase HMAC-SHA256 digest")
    elif secret:
        expected = hmac_signature(secret, capability_signature_payload(attestation))
        if not hmac.compare_digest(signature, expected):
            errors.append("capability HMAC verification failed")
    receipt = attestation.get("verification_receipt_sha256")
    expected_receipt = capability_verification_receipt(attestation)
    if not isinstance(receipt, str) or not hmac.compare_digest(receipt, expected_receipt):
        errors.append("capability verification receipt mismatch")
    return errors


def verify_user_receipt(
    authorization: Mapping[str, object], *, mode: str, proof_only_fixture: bool, kind: str
) -> list[str]:
    key_id, secret, algorithm, errors = _root_for(mode, "user", proof_only_fixture)
    label = "authorization" if kind == "authorization" else "budget extension"
    if authorization.get("signature_algorithm") != algorithm:
        errors.append(f"{label} signature algorithm is not permitted for this validation mode")
    if authorization.get("key_id") != key_id:
        errors.append(f"{label} key_id does not match the configured user trust root")
    signature = authorization.get("signature")
    if not isinstance(signature, str) or len(signature) != 64:
        errors.append(f"{label} signature must be a lowercase HMAC-SHA256 digest")
    elif secret:
        expected = hmac_signature(
            secret, authorization_signature_payload(authorization, kind=kind)
        )
        if not hmac.compare_digest(signature, expected):
            errors.append(f"{label} HMAC verification failed")
    receipt = authorization.get("receipt_sha256")
    expected_receipt = authorization_verification_receipt(authorization, kind=kind)
    if not isinstance(receipt, str) or not hmac.compare_digest(receipt, expected_receipt):
        errors.append(f"{label} verification receipt mismatch")
    return errors
