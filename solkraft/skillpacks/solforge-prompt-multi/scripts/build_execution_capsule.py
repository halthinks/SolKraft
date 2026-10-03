#!/usr/bin/env python3
"""Build a hash-bound SolForge execution capsule from a validated audit package."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_package import validate_package

PROFILE = "multi"


def canonical_hash(capsule: dict) -> str:
    immutable = {k: v for k, v in capsule.items() if k not in {"capsule_sha256", "confirmation"}}
    raw = json.dumps(immutable, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_package")
    parser.add_argument("original_request_file")
    parser.add_argument("authority_file")
    parser.add_argument("output")
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    audit = json.loads(Path(args.audit_package).read_text(encoding="utf-8"))
    errors = validate_package(audit, skill_root)
    if errors:
        for error in errors:
            print(f"ERROR: audit package: {error}", file=sys.stderr)
        return 1
    if audit.get("profile") != PROFILE:
        print(f"ERROR: audit profile must be {PROFILE}", file=sys.stderr)
        return 1
    original_request = Path(args.original_request_file).read_text(encoding="utf-8").strip()
    if not original_request:
        print("ERROR: original request must be nonempty", file=sys.stderr)
        return 1
    authority = json.loads(Path(args.authority_file).read_text(encoding="utf-8"))
    expected = {"capsule_id", "scope", "authorization", "budgets", "retry_limit", "source_artifacts"}
    if set(authority) != expected:
        print(f"ERROR: authority keys must be {sorted(expected)}", file=sys.stderr)
        return 1
    artifacts = []
    for source in authority["source_artifacts"]:
        path = Path(source)
        if not path.is_file():
            print(f"ERROR: source artifact missing: {path}", file=sys.stderr)
            return 1
        artifacts.append({"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    record = audit["intent_record"]
    requirement_rows = []
    for field in ("constraints", "deliverables", "acceptance_criteria", "unacceptable_partial_outcomes"):
        requirement_rows.extend({"id": row["id"], "text": row["text"]} for row in record[field])
    provenance = audit["prompt"].rstrip().splitlines()[-1]
    capsule = {
        "schema_version": "1.0.0",
        "profile": PROFILE,
        "capsule_id": authority["capsule_id"],
        "payload": {
            "original_request": original_request,
            "structured_intent": {
                "objective": record["objective"],
                "inputs": list(record["inputs"]),
                "constraints": [row["text"] for row in record["constraints"]],
                "deliverables": [row["text"] for row in record["deliverables"]],
                "acceptance_criteria": [row["text"] for row in record["acceptance_criteria"]],
                "authorization_boundaries": list(record["authorization_boundaries"]),
            },
            "hardened_prompt": audit["prompt"],
            "solforge_provenance": provenance,
            "requirements": requirement_rows,
            "scope": authority["scope"],
            "authorization": authority["authorization"],
            "risks": {"categories": list(record["risk_categories"]), "high_consequence": record["high_consequence"]},
            "budgets": authority["budgets"],
            "retry_limit": authority["retry_limit"],
            "source_artifacts": artifacts,
        },
        "capsule_sha256": "0" * 64,
        "confirmation": None,
    }
    capsule["capsule_sha256"] = canonical_hash(capsule)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Execution capsule written: {output}")
    print(f"capsule_sha256={capsule['capsule_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
