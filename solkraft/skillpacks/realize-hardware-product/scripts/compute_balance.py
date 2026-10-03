#!/usr/bin/env python3
"""Compute mass and center of gravity for named hardware configurations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compute(data: dict) -> dict:
    by_id = {item["id"]: item for item in data["components"]}
    results = []
    for cfg in data["configurations"]:
        ids = cfg["include"]
        missing = sorted(set(ids) - set(by_id))
        if missing:
            raise ValueError(f"{cfg['id']}: unknown components: {missing}")
        parts = [by_id[item_id] for item_id in ids]
        total = sum(float(p["mass_g"]) for p in parts)
        if total <= 0:
            raise ValueError(f"{cfg['id']}: total mass must be positive")
        cg = {
            axis: sum(float(p["mass_g"]) * float(p["cg_mm"][axis]) for p in parts) / total
            for axis in ("x", "y", "z")
        }
        results.append(
            {
                "id": cfg["id"],
                "description": cfg.get("description", ""),
                "component_ids": ids,
                "total_mass_g": round(total, 3),
                "cg_mm": {axis: round(value, 3) for axis, value in cg.items()},
                "evidence_mix": sorted({p.get("evidence_class", "UNKNOWN") for p in parts}),
            }
        )
    return {
        "schema_version": "hardware-balance-report.v1",
        "datum": data["datum"],
        "result_class": "CALCULATED_NOT_MEASURED",
        "configurations": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = compute(load(args.input))
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
