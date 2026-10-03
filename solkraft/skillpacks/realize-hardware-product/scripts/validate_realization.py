#!/usr/bin/env python3
"""Validate closure claims in a hardware realization manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


LEVELS = ["CONCEPT", "SOURCE_BOUND", "DIGITAL_CLOSED", "FIRST_ARTICLE_READY", "PHYSICALLY_VERIFIED"]
PENDING = {None, "", "PENDING", "TBD", "UNKNOWN"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_ok(root: Path, value: object) -> bool:
    return isinstance(value, str) and value not in PENDING and (root / value).is_file()


def validate(data: dict, root: Path) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "product", "revision", "closure_level", "authority", "requirements", "components", "interfaces", "geometry", "analysis", "acceptance", "claims", "open_gates"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    level = data.get("closure_level")
    if level not in LEVELS:
        errors.append(f"invalid closure_level: {level!r}")
        return errors
    index = LEVELS.index(level)

    if index >= 1:
        critical = [c for c in data.get("components", []) if c.get("critical", True)]
        if not critical:
            errors.append("SOURCE_BOUND requires critical components")
        for component in critical:
            label = component.get("id", "<unnamed>")
            for key in ("manufacturer", "model", "selection_state", "source_url", "evidence_class"):
                if component.get(key) in PENDING:
                    errors.append(f"{label}: missing source-bound {key}")
            if component.get("selection_state") == "SELECTED" and component.get("order_path") in PENDING:
                errors.append(f"{label}: selected part lacks order_path")
            local = component.get("local_source")
            expected = component.get("sha256")
            if local not in PENDING:
                local_path = root / str(local)
                if not local_path.is_file():
                    errors.append(f"{label}: local_source not found: {local}")
                elif expected not in PENDING and sha256(local_path).lower() != str(expected).lower():
                    errors.append(f"{label}: SHA-256 mismatch: {local}")

    if index >= 2:
        geometry = data.get("geometry", {})
        if geometry.get("dimensionally_closed") is not True:
            errors.append("DIGITAL_CLOSED requires geometry.dimensionally_closed=true")
        if not path_ok(root, geometry.get("master_assembly")):
            errors.append("DIGITAL_CLOSED requires an existing master_assembly")
        envelope = geometry.get("overall_envelope_mm", {})
        for axis in ("x", "y", "z"):
            value = envelope.get(axis)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"DIGITAL_CLOSED requires positive overall envelope {axis}")
        for key in ("collision_report", "balance_report", "power_report", "thermal_report", "pcb_status"):
            value = data.get("analysis", {}).get(key)
            if key == "pcb_status":
                if value in PENDING:
                    errors.append("DIGITAL_CLOSED requires explicit pcb_status")
            elif not path_ok(root, value):
                errors.append(f"DIGITAL_CLOSED requires existing analysis.{key}")
        if not data.get("interfaces"):
            errors.append("DIGITAL_CLOSED requires interface records")

    if index >= 3:
        acceptance = data.get("acceptance", {})
        if not path_ok(root, acceptance.get("ledger")):
            errors.append("FIRST_ARTICLE_READY requires an acceptance ledger")
        if not acceptance.get("required_test_ids"):
            errors.append("FIRST_ARTICLE_READY requires required_test_ids")

    if index >= 4:
        acceptance = data.get("acceptance", {})
        required = set(acceptance.get("required_test_ids", []))
        executed = set(acceptance.get("executed_test_ids", []))
        if required - executed:
            errors.append(f"PHYSICALLY_VERIFIED missing executed tests: {sorted(required - executed)}")
        if not acceptance.get("raw_evidence"):
            errors.append("PHYSICALLY_VERIFIED requires raw_evidence")
        for record in acceptance.get("raw_evidence", []):
            for key in ("test_id", "article_id", "operator", "date", "instrument_id", "artifact", "sha256", "result"):
                if record.get(key) in PENDING:
                    errors.append(f"physical evidence record missing {key}: {record.get('test_id', '<unnamed>')}")
            artifact = record.get("artifact")
            if artifact not in PENDING and not path_ok(root, artifact):
                errors.append(f"physical evidence artifact missing: {artifact}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    root = (args.root or args.manifest.parent).resolve()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate(data, root)
    report = {"manifest": str(args.manifest), "root": str(root), "valid": not errors, "errors": errors}
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
