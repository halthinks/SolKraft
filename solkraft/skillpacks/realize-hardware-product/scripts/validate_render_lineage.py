#!/usr/bin/env python3
"""Validate that released presentation renders remain bound to CAD authority."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PENDING = {None, "", "PENDING", "TBD", "UNKNOWN"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_file(root: Path, record: dict, label: str, errors: list[str]) -> Path | None:
    value = record.get("path")
    expected = record.get("sha256")
    if value in PENDING:
        errors.append(f"{label}: missing path")
        return None
    path = root / str(value)
    if not path.is_file():
        errors.append(f"{label}: file not found: {value}")
        return None
    if expected in PENDING:
        errors.append(f"{label}: missing SHA-256")
    elif sha256(path).lower() != str(expected).lower():
        errors.append(f"{label}: SHA-256 mismatch: {value}")
    return path


def validate(data: dict, root: Path) -> list[str]:
    errors: list[str] = []
    for key in (
        "schema_version",
        "product",
        "revision",
        "geometry_authority",
        "render_pipeline",
        "render_inputs",
        "renders",
        "visual_review",
        "claim_boundary",
    ):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    authority = data.get("geometry_authority", {})
    checked_file(root, authority, "geometry authority", errors)
    authority_hash = authority.get("sha256")

    pipeline = data.get("render_pipeline", {})
    for key in ("software", "script", "mesh_export_report", "method"):
        if pipeline.get(key) in PENDING:
            errors.append(f"render pipeline missing {key}")
    for key in ("script", "mesh_export_report"):
        value = pipeline.get(key)
        if value not in PENDING and not (root / str(value)).is_file():
            errors.append(f"render pipeline file not found: {value}")

    inputs = data.get("render_inputs", [])
    if not isinstance(inputs, list) or not inputs:
        errors.append("at least one render input is required")
    else:
        for index, record in enumerate(inputs):
            checked_file(root, record, f"render input {index}", errors)

    renders = data.get("renders", [])
    if not isinstance(renders, list) or not renders:
        errors.append("at least one released render is required")
    else:
        for index, record in enumerate(renders):
            checked_file(root, record, f"render {index}", errors)
            if record.get("view") in PENDING:
                errors.append(f"render {index}: missing view")
            if record.get("geometry_modified_for_presentation") is not False:
                errors.append(f"render {index}: geometry_modified_for_presentation must be false")
            if str(record.get("geometry_authority_sha256", "")).lower() != str(authority_hash).lower():
                errors.append(f"render {index}: geometry authority hash does not match")

    review = data.get("visual_review", {})
    for key in ("reviewer", "date", "result", "notes"):
        if review.get(key) in PENDING:
            errors.append(f"visual review missing {key}")
    if data.get("claim_boundary") in PENDING:
        errors.append("missing render claim boundary")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("lineage", type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    root = (args.root or args.lineage.parent).resolve()
    data = json.loads(args.lineage.read_text(encoding="utf-8"))
    errors = validate(data, root)
    report = {
        "lineage": str(args.lineage),
        "root": str(root),
        "valid": not errors,
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
