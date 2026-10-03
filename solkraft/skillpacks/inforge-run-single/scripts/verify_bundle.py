#!/usr/bin/env python3
"""Verify an InForge runner bundle against its tamper-evident manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    manifest_path = root / "references" / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: missing references/manifest.json", file=sys.stderr)
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid manifest: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    for relative, expected in manifest.get("files", {}).items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
        elif digest(path) != expected:
            errors.append(f"hash mismatch {relative}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"InForge runner bundle verified: {manifest.get('profile', 'unknown')}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
