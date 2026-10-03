#!/usr/bin/env python3
"""Verify the versioned SolForge bundle against references/manifest.json."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(root: Path) -> list[str]:
    manifest_path = root / "references" / "manifest.json"
    if not manifest_path.exists():
        return ["missing references/manifest.json"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for relative, expected in manifest.get("files", {}).items():
        path = root / relative
        if not path.exists():
            errors.append(f"missing {relative}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"hash mismatch {relative}: expected {expected}, got {actual}")
    source = manifest.get("files", {}).get("references/source-prompt.md")
    contract = manifest.get("files", {}).get("references/transposition-contract.md")
    if manifest.get("source_sha256") != source:
        errors.append("source_sha256 does not match source file entry")
    if manifest.get("contract_sha256") != contract:
        errors.append("contract_sha256 does not match contract file entry")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = verify(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("SolForge bundle hashes verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
