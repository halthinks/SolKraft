#!/usr/bin/env python3
"""Validate generated SolForge audit packages against the semantic golden corpus."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_package import validate_package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_dir")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    cases = json.loads((root / "references" / "evaluation-corpus.json").read_text(encoding="utf-8"))["cases"]
    results_dir = Path(args.results_dir)
    failures = 0
    for case in cases:
        path = results_dir / f"{case['id']}.json"
        errors: list[str] = []
        if not path.exists():
            errors.append("missing result package")
        else:
            package = json.loads(path.read_text(encoding="utf-8"))
            errors.extend(validate_package(package, root))
            prompt = package.get("prompt", "").lower()
            for term in case["must_represent"]:
                if term.lower() not in prompt:
                    errors.append(f"missing golden semantic phrase: {term}")
            for term in case["must_not_include"]:
                if term.lower() in prompt:
                    errors.append(f"forbidden source leakage: {term}")
            actual_risks = set(package.get("intent_record", {}).get("risk_categories", []))
            expected_risks = set(case["expected_risk_categories"])
            if expected_risks:
                if not expected_risks.issubset(actual_risks):
                    errors.append(f"missing expected risks: {sorted(expected_risks-actual_risks)}")
            elif actual_risks:
                errors.append(f"unexpected risks: {sorted(actual_risks)}")
        if errors:
            failures += 1
            print(f"FAIL {case['id']}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {case['id']}")
    print(f"{len(cases)-failures}/{len(cases)} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
