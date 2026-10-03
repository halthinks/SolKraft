#!/usr/bin/env python3
"""Validate the minimum evidence shape of a CAD-bound product realization."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


REQUIRED_MANIFEST_KEYS = {
    "schema",
    "revision",
    "status",
    "authority",
    "requirements",
    "geometry",
    "analysis",
    "presentation",
    "acceptance",
    "claims",
    "open_gates",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = root / "product-realization-manifest.json"
    if not manifest_path.is_file():
        errors.append("missing product-realization-manifest.json")
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_MANIFEST_KEYS - set(manifest))
        if missing:
            errors.append(f"manifest missing keys: {', '.join(missing)}")

    geometry = manifest.get("geometry", {})
    master_rel = geometry.get("master_assembly")
    if not master_rel:
        errors.append("manifest geometry.master_assembly is absent")
    else:
        master = root / master_rel
        if not master.is_file():
            errors.append(f"missing master assembly: {master_rel}")
        elif geometry.get("master_sha256", "").upper() != sha256(master):
            errors.append("master assembly SHA-256 does not match manifest")

    lineage_rel = manifest.get("presentation", {}).get("render_lineage")
    if not lineage_rel or not (root / lineage_rel).is_file():
        errors.append("missing render-lineage manifest")

    ledger_rel = manifest.get("acceptance", {}).get("ledger")
    if not ledger_rel or not (root / ledger_rel).is_file():
        errors.append("missing physical acceptance ledger")
    else:
        with (root / ledger_rel).open(newline="", encoding="utf-8-sig") as stream:
            rows = list(csv.DictReader(stream))
        if not rows:
            errors.append("physical acceptance ledger has no test rows")
        elif any(row.get("status") == "PASS" and not row.get("evidence_path") for row in rows):
            errors.append("physical acceptance PASS exists without evidence_path")

    if not manifest.get("open_gates"):
        warnings.append("no open gates recorded; verify that physical evidence is truly complete")
    if "production" in str(manifest.get("status", "")).lower() and manifest.get("open_gates"):
        errors.append("production status conflicts with open gates")

    result = {"root": str(root), "errors": errors, "warnings": warnings, "valid": not errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
