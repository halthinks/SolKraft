#!/usr/bin/env python3
"""Sequence the six finished hardware skills against one product root."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STAGES = [
    "authority",
    "select",
    "preserve",
    "build_matrix",
    "realize",
    "cad_bind",
]

CLOSURE = [
    "CONCEPT",
    "SOURCE_BOUND",
    "DIGITAL_CLOSED",
    "FIRST_ARTICLE_READY",
    "PHYSICALLY_VERIFIED",
]

SKILL_SCRIPTS = {
    "select": ("select-and-validate-hardware-parts", "scripts/validate_part_decision.py"),
    "preserve": ("preserve-engineering-selections", "scripts/validate_selection_register.py"),
    "build_matrix": ("build-selected-hardware-product", "scripts/build_closure_matrix.py"),
    "realize": ("realize-hardware-product", "scripts/validate_realization.py"),
    "cad_bind": ("realize-cad-bound-product", "scripts/validate_realization.py"),
}

TEMPLATE_MANIFEST = {
    "schema_version": "hardware-realization-manifest.v1",
    "product": "",
    "revision": "",
    "closure_level": "CONCEPT",
    "root_datum": "PENDING",
    "authority": {
        "product_lock": "PENDING",
        "software_contracts": [],
        "user_journey": "PENDING",
    },
    "requirements": [],
    "components": [],
    "interfaces": [],
    "geometry": {
        "master_assembly": "PENDING",
        "custom_part_exports": [],
        "supplier_geometry": [],
        "overall_envelope_mm": {"x": None, "y": None, "z": None},
        "dimensionally_closed": False,
    },
    "analysis": {
        "collision_report": "PENDING",
        "balance_report": "PENDING",
        "power_report": "PENDING",
        "thermal_report": "PENDING",
        "pcb_status": "PENDING",
    },
    "presentation": {
        "render_lineage": "PENDING",
        "released_renders": [],
        "geometry_unchanged_for_presentation": False,
    },
    "acceptance": {
        "ledger": "PENDING",
        "required_test_ids": [],
        "executed_test_ids": [],
        "raw_evidence": [],
    },
    "claims": {
        "supported": [],
        "prohibited_until_evidence": [
            "fabrication-ready",
            "measured",
            "production-ready",
            "pcb-generation release",
        ],
    },
    "open_gates": [
        "Write requirements and hard gates before selecting parts",
        "Do not use unfinished pcb-generation as fabrication evidence",
    ],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def default_skills_root(script: Path) -> Path:
    here = script.resolve().parent
    if here.parent.name == "hardware-product-pipeline":
        return here.parent.parent
    return Path.home() / ".codex" / "skills"


def skill_script(skills_root: Path, stage: str) -> Path:
    folder, rel = SKILL_SCRIPTS[stage]
    return skills_root / folder / rel


def run_py(script: Path, args: list[str]) -> dict:
    if not script.is_file():
        return {"ok": False, "exit": 127, "stdout": "", "stderr": f"missing {script}"}
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "ok": proc.returncode == 0,
        "exit": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def init_root(root: Path, product: str, profile: str, revision: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name in ("authority", "decisions", "geometry", "analysis", "acceptance", "presentation"):
        (root / name).mkdir(exist_ok=True)
    write_json(
        root / "pipeline.json",
        {
            "schema": "hardware-product-pipeline.v1",
            "product": product,
            "profile": profile,
            "revision": revision,
            "claimed_stage": "authority",
            "claimed_closure": "CONCEPT",
            "skills": [
                "evidence-bound-product-pipeline",
                "select-and-validate-hardware-parts",
                "preserve-engineering-selections",
                "build-selected-hardware-product",
                "realize-hardware-product",
                "realize-cad-bound-product",
            ],
            "blocked_hooks": [
                {
                    "skill": "pcb-generation",
                    "reason": "unfinished; not fabrication or manufacturer evidence",
                }
            ],
        },
    )
    write_json(
        root / "authority" / "decision-log.json",
        {"schema": "authority-decision-log.v1", "entries": []},
    )
    write_json(
        root / "authority" / "evidence-index.json",
        {"schema": "authority-evidence-index.v1", "items": []},
    )
    write_json(
        root / "requirements.json",
        {
            "schema": "hardware-requirements.v1",
            "product": product,
            "profile": profile,
            "revision": revision,
            "requirements": [],
            "hard_gates": [],
            "electronic_domains": [],
        },
    )
    write_json(
        root / "selection-register.json",
        {
            "schema": "selection-register.v1",
            "product": product,
            "profile": profile,
            "revision": revision,
            "selections": [],
        },
    )
    manifest = json.loads(json.dumps(TEMPLATE_MANIFEST))
    manifest["product"] = product
    manifest["revision"] = revision
    write_json(root / "product-realization-manifest.json", manifest)
    write_json(
        root / "pipeline-status.json",
        {
            "schema": "hardware-product-pipeline-status.v1",
            "product": product,
            "revision": revision,
            "checked_at": utc_now(),
            "supported_stage": None,
            "supported_closure": "CONCEPT",
            "note": "initialized empty; init is not a selection or a build",
            "checks": [],
        },
    )


def collect_decisions(root: Path) -> list[Path]:
    folder = root / "decisions"
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.json") if p.is_file())


def check_root(root: Path, skills_root: Path) -> dict:
    root = root.resolve()
    checks = []
    pipeline = read_json(root / "pipeline.json") if (root / "pipeline.json").is_file() else {}

    authority_ok = (root / "authority" / "decision-log.json").is_file() and (
        root / "requirements.json"
    ).is_file()
    reqs = []
    if (root / "requirements.json").is_file():
        reqs = read_json(root / "requirements.json").get("requirements", [])
    checks.append(
        {
            "stage": "authority",
            "skill": "evidence-bound-product-pipeline",
            "ok": authority_ok and bool(reqs),
            "detail": "requirements present" if reqs else "requirements.json has no requirements yet",
        }
    )

    decisions = collect_decisions(root)
    select_script = skill_script(skills_root, "select")
    select_ok = True
    select_details = []
    if not decisions:
        select_ok = False
        select_details.append("no decisions/*.json")
    for decision in decisions:
        result = run_py(select_script, [str(decision)])
        select_ok = select_ok and result["ok"]
        select_details.append(
            f"{decision.name}: {'PASS' if result['ok'] else 'FAIL'} {(result['stdout'] or result['stderr']).strip()}"
        )
    checks.append(
        {
            "stage": "select",
            "skill": "select-and-validate-hardware-parts",
            "ok": select_ok,
            "detail": " | ".join(select_details),
        }
    )

    register = root / "selection-register.json"
    preserve_result = {"ok": False, "stdout": "missing selection-register.json", "stderr": ""}
    if register.is_file():
        preserve_result = run_py(skill_script(skills_root, "preserve"), [str(register)])
        rows = read_json(register).get("selections", [])
        if not rows:
            preserve_result = {
                "ok": False,
                "stdout": preserve_result.get("stdout", ""),
                "stderr": "selection-register.json has no selections",
            }
    checks.append(
        {
            "stage": "preserve",
            "skill": "preserve-engineering-selections",
            "ok": preserve_result["ok"],
            "detail": (preserve_result["stdout"] or preserve_result["stderr"]).strip(),
        }
    )

    matrix = root / "build-closure-matrix.json"
    matrix_ok = False
    matrix_detail = "missing build-closure-matrix.json"
    if register.is_file():
        generated = run_py(
            skill_script(skills_root, "build_matrix"),
            [str(register), "--output", str(matrix)],
        )
        if generated["ok"] and matrix.is_file():
            data = read_json(matrix)
            summary = data.get("summary", {})
            rows = data.get("rows", [])
            matrix_ok = bool(rows)
            matrix_detail = (
                f"selections={summary.get('selections')} "
                f"closed={summary.get('closed_cells')} "
                f"open={summary.get('open_cells')}"
            )
            if not rows:
                matrix_detail = "matrix has no selection rows"
        else:
            matrix_detail = (generated["stdout"] or generated["stderr"]).strip()
    checks.append(
        {
            "stage": "build_matrix",
            "skill": "build-selected-hardware-product",
            "ok": matrix_ok,
            "detail": matrix_detail,
        }
    )

    manifest = root / "product-realization-manifest.json"
    realize_result = {"ok": False, "stdout": "missing product-realization-manifest.json", "stderr": ""}
    claimed_closure = "CONCEPT"
    if manifest.is_file():
        realize_result = run_py(
            skill_script(skills_root, "realize"),
            [str(manifest), "--root", str(root)],
        )
        claimed_closure = read_json(manifest).get("closure_level", "CONCEPT")
        if claimed_closure not in CLOSURE:
            claimed_closure = "CONCEPT"
    checks.append(
        {
            "stage": "realize",
            "skill": "realize-hardware-product",
            "ok": realize_result["ok"],
            "detail": (realize_result["stdout"] or realize_result["stderr"]).strip(),
        }
    )

    cad_result = run_py(skill_script(skills_root, "cad_bind"), [str(root)])
    checks.append(
        {
            "stage": "cad_bind",
            "skill": "realize-cad-bound-product",
            "ok": cad_result["ok"],
            "detail": (cad_result["stdout"] or cad_result["stderr"]).strip(),
        }
    )

    supported_stage = None
    for check in checks:
        if check["ok"]:
            supported_stage = check["stage"]
        else:
            break

    supported_closure = "CONCEPT"
    if supported_stage in {"realize", "cad_bind"} and realize_result["ok"]:
        supported_closure = claimed_closure
    elif supported_stage == "build_matrix":
        supported_closure = "CONCEPT"
    elif supported_stage in {"select", "preserve"}:
        supported_closure = "SOURCE_BOUND" if supported_stage == "preserve" and select_ok else "CONCEPT"

    status = {
        "schema": "hardware-product-pipeline-status.v1",
        "product": pipeline.get("product"),
        "profile": pipeline.get("profile"),
        "revision": pipeline.get("revision"),
        "checked_at": utc_now(),
        "claimed_stage": pipeline.get("claimed_stage"),
        "claimed_closure": pipeline.get("claimed_closure") or claimed_closure,
        "supported_stage": supported_stage,
        "supported_closure": supported_closure,
        "text_to_pcb": {
            "usable_as_release_evidence": False,
            "reason": "unfinished skill; board factory hook only",
        },
        "checks": checks,
        "next": next_action(checks),
    }
    write_json(root / "pipeline-status.json", status)
    return status


def next_action(checks: list[dict]) -> str:
    for check in checks:
        if not check["ok"]:
            return f"close {check['stage']} ({check['skill']}): {check['detail']}"
    return "all six stage checks passed; promote only to the supported closure"


def print_status(status: dict) -> None:
    print(
        json.dumps(
            {
                "product": status.get("product"),
                "supported_stage": status.get("supported_stage"),
                "supported_closure": status.get("supported_closure"),
                "claimed_stage": status.get("claimed_stage"),
                "claimed_closure": status.get("claimed_closure"),
                "next": status.get("next"),
                "text_to_pcb_release_evidence": False,
                "checks": [
                    {
                        "stage": c["stage"],
                        "ok": c["ok"],
                        "skill": c["skill"],
                    }
                    for c in status.get("checks", [])
                ],
            },
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the six-skill hardware product pipeline.")
    parser.add_argument("command", choices=("init", "check", "status"))
    parser.add_argument("product_root", type=Path)
    parser.add_argument("--product", default="UNNAMED")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--revision", default="A")
    parser.add_argument("--skills-root", type=Path)
    args = parser.parse_args()
    skills_root = (args.skills_root or default_skills_root(Path(__file__))).resolve()
    root = args.product_root

    if args.command == "init":
        init_root(root, args.product, args.profile, args.revision)
        status = check_root(root, skills_root)
        print_status(status)
        return 0
    if args.command == "status":
        path = root / "pipeline-status.json"
        if not path.is_file():
            print("missing pipeline-status.json; run check", file=sys.stderr)
            return 1
        print_status(read_json(path))
        return 0
    status = check_root(root, skills_root)
    print_status(status)
    return 0 if status.get("supported_stage") else 1


if __name__ == "__main__":
    raise SystemExit(main())
