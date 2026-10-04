"""Interface contract for any future executable verifier adapter.

Core SolKraft deliberately provides no subprocess runner here.
"""
from __future__ import annotations

from dataclasses import dataclass


CORE_EXECUTABLE_VERIFIERS_ENABLED = False


@dataclass(frozen=True)
class SandboxRequirements:
    timeout_seconds: int = 60
    network: bool = False
    inherit_secrets: bool = False
    max_output_bytes: int = 1_000_000
    max_processes: int = 8
    read_only_mounts: tuple[str, ...] = ()
    writable_mounts: tuple[str, ...] = ()

    def public(self) -> dict:
        return {
            "timeout_seconds": self.timeout_seconds,
            "network": self.network,
            "inherit_secrets": self.inherit_secrets,
            "max_output_bytes": self.max_output_bytes,
            "max_processes": self.max_processes,
            "read_only_mounts": list(self.read_only_mounts),
            "writable_mounts": list(self.writable_mounts),
        }


DEFAULT_VERIFIER_SANDBOX = SandboxRequirements()


def validate_adapter_manifest(value: object) -> list[str]:
    """Validate a host adapter declaration; never execute the adapter."""
    if not isinstance(value, dict):
        return ["sandbox adapter manifest must be an object"]
    errors = []
    if value.get("network", False):
        errors.append("verifier sandbox network must default to disabled")
    if value.get("inherit_secrets", False):
        errors.append("verifier sandbox must not inherit host secrets")
    timeout = value.get("timeout_seconds", 60)
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 600:
        errors.append("timeout_seconds must be between 1 and 600")
    output = value.get("max_output_bytes", 1_000_000)
    if not isinstance(output, int) or isinstance(output, bool) or not 1 <= output <= 10_000_000:
        errors.append("max_output_bytes must be between 1 and 10000000")
    processes = value.get("max_processes", 8)
    if not isinstance(processes, int) or isinstance(processes, bool) or not 1 <= processes <= 64:
        errors.append("max_processes must be between 1 and 64")
    writable = value.get("writable_mounts", [])
    readonly = value.get("read_only_mounts", [])
    if not isinstance(writable, list) or not isinstance(readonly, list):
        errors.append("sandbox mounts must be lists")
    return errors
