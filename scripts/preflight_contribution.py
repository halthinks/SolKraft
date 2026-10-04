"""Build a reusable pre-PR evidence bundle for one skill contribution.

Usage:
    python -m scripts.preflight_contribution contributions/<skill>.json

This runs the canonical full contribution gate. It does not introduce a second
acceptance path; it packages the receipts and built artifacts produced by
scripts.check_contribution --full.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_artifact(source: Path, target_root: Path, relative: str) -> dict | None:
    if not source.is_file():
        return None
    target = target_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {
        "path": relative.replace("\\", "/"),
        "sha256": sha256(target),
        "bytes": target.stat().st_size,
    }


def build_bundle(manifest: Path) -> dict:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    skill = data.get("skill")
    if not isinstance(skill, str) or not skill:
        raise ValueError("Contribution manifest must contain a non-empty skill.")

    target = ROOT / "build" / "preflight" / skill
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    inventory = []
    candidates = [
        (manifest, "candidate/contribution.json"),
        (ROOT / "solkraft" / "skillpacks" / skill / "SKILL.md", "candidate/SKILL.md"),
        (ROOT / "solkraft" / "skillpacks" / skill / "contract.yaml", "candidate/contract.yaml"),
        (ROOT / "build" / "contributions" / "latest.json", "receipts/contribution.json"),
        (ROOT / "build" / "local-ci.json", "receipts/local-ci.json"),
        (ROOT / "scripts" / "results-routing-100000.json", "receipts/routing-100000.json"),
        (ROOT / "build" / "contracts-migration.json", "receipts/contracts-migration.json"),
        (ROOT / "build" / "contract-index.json", "receipts/contract-index.json"),
        (ROOT / "docs" / "downloads" / "solkraft-plugin.zip", "artifacts/solkraft-plugin.zip"),
    ]
    for source, relative in candidates:
        item = copy_artifact(source, target, relative)
        if item:
            inventory.append(item)

    for wheel in sorted((ROOT / "dist").glob("solkraft-*.whl")):
        item = copy_artifact(wheel, target, "artifacts/" + wheel.name)
        if item:
            inventory.append(item)

    contribution_receipt = ROOT / "build" / "contributions" / "latest.json"
    contribution = (
        json.loads(contribution_receipt.read_text(encoding="utf-8"))
        if contribution_receipt.is_file() else {}
    )
    local_receipt = ROOT / "build" / "local-ci.json"
    local = (
        json.loads(local_receipt.read_text(encoding="utf-8"))
        if local_receipt.is_file() else {}
    )

    summary = {
        "schema": "solkraft/contribution-preflight/v1",
        "skill": skill,
        "status": "passed" if (
            contribution.get("status") == "passed"
            and local.get("status") == "passed"
        ) else "failed",
        "manifest_sha256": sha256(manifest),
        "source_sha256": contribution.get("source_sha256"),
        "contribution_status": contribution.get("status"),
        "local_ci_status": local.get("status"),
        "routing_total": (contribution.get("full_regression") or {}).get("total"),
        "routing_passed": (contribution.get("full_regression") or {}).get("passed"),
        "artifacts": inventory,
    }
    (target / "preflight.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    archive = ROOT / "build" / "preflight" / f"{skill}-preflight.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(target.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(target).as_posix())
    summary["bundle"] = {
        "path": archive.relative_to(ROOT).as_posix(),
        "sha256": sha256(archive),
        "bytes": archive.stat().st_size,
    }
    (target / "preflight.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--variants", type=int, default=25)
    args = parser.parse_args()
    if not args.manifest.is_file():
        parser.error("manifest does not exist")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.check_contribution",
            str(args.manifest),
            "--full",
            "--variants",
            str(args.variants),
        ],
        cwd=ROOT,
        check=True,
    )
    summary = build_bundle(args.manifest)
    if summary["status"] != "passed":
        raise SystemExit("Full contribution gate did not produce passing receipts.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
