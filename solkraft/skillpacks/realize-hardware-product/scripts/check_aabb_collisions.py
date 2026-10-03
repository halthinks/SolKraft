#!/usr/bin/env python3
"""Screen axis-aligned hardware envelopes for prohibited overlap/clearance."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


def axis_gap(a0: float, a1: float, b0: float, b1: float) -> float:
    if a1 < b0:
        return b0 - a1
    if b1 < a0:
        return a0 - b1
    return -min(a1, b1) + max(a0, b0)


def pair_result(a: dict, b: dict) -> dict:
    gaps = {
        axis: axis_gap(
            float(a["min_mm"][axis]),
            float(a["max_mm"][axis]),
            float(b["min_mm"][axis]),
            float(b["max_mm"][axis]),
        )
        for axis in ("x", "y", "z")
    }
    overlap = all(value <= 0 for value in gaps.values())
    clearance = 0.0 if overlap else math.sqrt(sum(max(value, 0.0) ** 2 for value in gaps.values()))
    return {"a": a["id"], "b": b["id"], "overlap": overlap, "axis_gap_mm": gaps, "clearance_mm": round(clearance, 3)}


def requested_pairs(data: dict) -> list[dict]:
    """Return an explicit pair matrix, or the legacy all-pairs matrix."""
    boxes = {box["id"]: box for box in data["boxes"]}
    requested = data.get("check_pairs")
    if requested is None:
        return [
            {"a": a["id"], "b": b["id"], "minimum_clearance_mm": 0.0}
            for a, b in itertools.combinations(data["boxes"], 2)
            if a.get("check", True) and b.get("check", True)
        ]

    output = []
    seen = set()
    for entry in requested:
        if isinstance(entry, list) and len(entry) == 2:
            item = {"a": entry[0], "b": entry[1], "minimum_clearance_mm": 0.0}
        elif isinstance(entry, dict):
            item = {
                "a": entry.get("a"),
                "b": entry.get("b"),
                "minimum_clearance_mm": float(entry.get("minimum_clearance_mm", 0.0)),
                "purpose": entry.get("purpose", ""),
            }
        else:
            raise ValueError(f"invalid check_pairs entry: {entry!r}")
        if item["a"] not in boxes or item["b"] not in boxes:
            raise ValueError(f"unknown box in check pair: {item['a']!r}, {item['b']!r}")
        key = tuple(sorted((item["a"], item["b"])))
        if key in seen:
            raise ValueError(f"duplicate check pair: {key}")
        seen.add(key)
        output.append(item)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    allowed = {tuple(sorted(pair)) for pair in data.get("allowed_overlap_pairs", [])}
    boxes = {box["id"]: box for box in data["boxes"]}
    checked = []
    violations = []
    for request in requested_pairs(data):
        a, b = boxes[request["a"]], boxes[request["b"]]
        pair = tuple(sorted((request["a"], request["b"])))
        result = pair_result(a, b)
        result["allowed"] = pair in allowed
        result["minimum_clearance_mm"] = request.get("minimum_clearance_mm", 0.0)
        result["purpose"] = request.get("purpose", "")
        result["clearance_violation"] = (
            not result["overlap"]
            and result["clearance_mm"] + 1e-9 < result["minimum_clearance_mm"]
        )
        checked.append(result)
        if (result["overlap"] and not result["allowed"]) or result["clearance_violation"]:
            violations.append(result)
    report = {
        "schema_version": "hardware-aabb-collision-report.v2",
        "datum": data["datum"],
        "result_class": "CAD_SCREEN_NOT_PHYSICAL_PROOF",
        "check_mode": "EXPLICIT_PAIRS" if data.get("check_pairs") is not None else "ALL_PAIRS_LEGACY",
        "checked_pair_count": len(checked),
        "violation_count": len(violations),
        "violations": violations,
        "pairs": checked,
    }
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
