"""Generate typed Contract v1 sidecars from legacy graph metadata.

Generated sidecars are explicitly inferred and remain legacy-inferred. This tool
never overwrites an existing contract.yaml and never infers harmlessness from an
unknown or effectful graph node.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import yaml

from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, get_graph


ROOT = Path(__file__).resolve().parents[1]


def _binding_name(prefix: str, index: int, text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")[:40]
    return slug or f"{prefix}-{index}"


def _input_binding(index: int, text: str) -> dict:
    return {
        "name": _binding_name("input", index, text),
        "required": True,
        "source": "user",
        "description": text,
        "schema": {},
    }


def _output_binding(index: int, text: str) -> dict:
    return {
        "name": _binding_name("output", index, text),
        "description": text,
        "schema": {},
    }


def inferred_contract(skill_id: str, node: dict) -> dict | None:
    if node.get("effect") is not False:
        return None
    return {
        "schema_version": "1.0",
        "skill_id": skill_id,
        "contract_revision": 1,
        "inputs": [
            _input_binding(index, str(text))
            for index, text in enumerate(node.get("inputs") or [], 1)
        ],
        "outputs": [
            _output_binding(index, str(text))
            for index, text in enumerate(node.get("outputs") or [], 1)
        ],
        "effects": [],
        "authority": {
            "capabilities": [],
            "resources": [],
            "legacy_scope": "none",
        },
        "risk": {
            "external": False,
            "destructive": False,
            "open_world": False,
        },
        "verification": {
            "mode": "declarative",
            "description": node.get("exit_evidence") or "Legacy exit evidence must be reviewed.",
            "checks": [],
        },
        "provenance": {
            "migration": "legacy-graph",
            "inferred": True,
        },
        "extensions": {
            "legacy_graph": {
                "domain": node.get("domain"),
                "selection": node.get("selection"),
                "path": node.get("path"),
            }
        },
    }


def migrate(*, write: bool = False) -> dict:
    graph = get_graph()
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = {record.id: record for record in catalog.records()}
    report = {
        "schema": "solkraft/contracts-migration/v1",
        "write": write,
        "generated": [],
        "existing": [],
        "manual_required": [],
        "missing_catalog": [],
    }
    for skill_id, node in sorted(graph["nodes"].items()):
        record = records.get(skill_id)
        if record is None:
            report["missing_catalog"].append(skill_id)
            continue
        target = record.entrypoint.parent / "contract.yaml"
        if target.is_file():
            report["existing"].append(skill_id)
            continue
        candidate = inferred_contract(skill_id, node)
        if candidate is None:
            report["manual_required"].append({
                "skill": skill_id,
                "reason": "legacy graph does not prove effect:false",
            })
            continue
        report["generated"].append(skill_id)
        if write:
            target.write_text(
                yaml.safe_dump(candidate, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
    report["counts"] = {
        key: len(report[key])
        for key in ("generated", "existing", "manual_required", "missing_catalog")
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Create missing inferred sidecars.")
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "build" / "contracts-migration.json",
    )
    args = parser.parse_args()
    report = migrate(write=args.write)
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
