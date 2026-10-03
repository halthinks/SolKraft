#!/usr/bin/env python3
"""Deterministic preflight and evidence-gate validator for DayQ Unreal libraries."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone


CANDIDATES = {
    "internal-control": {"ai_allowed": True, "package_required": False},
    "bulletforge": {"ai_allowed": False, "package_required": True},
    "easyballistics": {"ai_allowed": True, "package_required": True},
    "terminal-ballistics": {"ai_allowed": True, "package_required": True},
}

HARD_GATES = [
    "license",
    "ai_permission",
    "package_hash",
    "ue58_editor_build",
    "ue58_server_build",
    "smoke",
    "authority",
    "network_adversarial",
    "ballistics_fixtures",
    "performance",
    "dayq_adapter",
    "persistence_restart",
    "migration_removal",
    "security_supply_chain",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def find_ue58(explicit: str | None) -> Path | None:
    options = []
    if explicit:
        options.append(Path(explicit))
    env = os.environ.get("UE58_ROOT")
    if env:
        options.append(Path(env))
    options.extend([
        Path(r"C:\Program Files\Epic Games\UE_5.8"),
        Path(r"D:\Epic Games\UE_5.8"),
    ])
    for p in options:
        if (p / "Engine" / "Build" / "BatchFiles" / "Build.bat").exists():
            return p.resolve()
    return None


def find_msvc_x64() -> Path | None:
    """Find the x64 MSVC compiler the same way a normal VS/UBT install exposes it.

    `cl.exe` is often intentionally absent from a regular PowerShell PATH, so PATH
    alone is not valid evidence that Unreal lacks a compiler toolchain.
    """
    from_path = shutil.which("cl.exe")
    if from_path:
        return Path(from_path).resolve()

    installer = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / (
        "Microsoft Visual Studio/Installer/vswhere.exe"
    )
    installation_roots: list[Path] = []
    if installer.exists():
        try:
            result = subprocess.run(
                [
                    str(installer),
                    "-products",
                    "*",
                    "-requires",
                    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                    "-property",
                    "installationPath",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            installation_roots.extend(Path(line.strip()) for line in result.stdout.splitlines() if line.strip())
        except OSError:
            pass

    for root in installation_roots:
        tool_root = root / "VC/Tools/MSVC"
        if not tool_root.exists():
            continue
        versions = sorted((p for p in tool_root.iterdir() if p.is_dir()), reverse=True)
        for version in versions:
            compiler = version / "bin/Hostx64/x64/cl.exe"
            if compiler.exists():
                return compiler.resolve()
    return None


def candidate_package(root: Path, name: str) -> list[dict]:
    aliases = {
        "bulletforge": ("bulletforge", "bullet_forge"),
        "easyballistics": ("easyballistics", "easy_ballistics"),
        "terminal-ballistics": ("terminalballistics", "terminal_ballistics", "terminal-ballistics"),
    }[name]
    found = []
    if not root.exists():
        return found
    for p in root.rglob("*.uplugin"):
        low = str(p).lower().replace(" ", "")
        if any(a.replace("_", "").replace("-", "") in low.replace("_", "").replace("-", "") for a in aliases):
            found.append({"path": str(p.resolve()), "sha256": sha256_file(p)})
    return found


def preflight(args: argparse.Namespace) -> int:
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    ue = find_ue58(args.ue_root)
    compiler = find_msvc_x64()
    roots = [Path(p) for p in args.search_root]
    report = {
        "schema": 1,
        "created_at": now(),
        "host": {"platform": platform.platform(), "python": sys.version},
        "unreal_5_8_root": str(ue) if ue else None,
        "build_bat": str(ue / "Engine" / "Build" / "BatchFiles" / "Build.bat") if ue else None,
        "compiler": str(compiler) if compiler else None,
        "search_roots": [str(p.resolve()) for p in roots if p.exists()],
        "candidates": {},
    }
    for name, policy in CANDIDATES.items():
        packages = [] if name == "internal-control" else sum((candidate_package(r, name) for r in roots), [])
        if name == "internal-control":
            status = "ready-to-build" if ue and compiler else "blocked-environment"
        elif not policy["ai_allowed"]:
            status = "blocked-permission"
        elif not packages:
            status = "blocked-needs-acquisition"
        elif not ue:
            status = "blocked-environment"
        else:
            status = "ready-to-inspect"
        report["candidates"][name] = {
            "ai_allowed_public_baseline": policy["ai_allowed"],
            "packages": packages,
            "status": status,
        }
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


def evaluate(args: argparse.Namespace) -> int:
    evidence = Path(args.evidence)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    results = {"schema": 1, "created_at": now(), "candidates": {}}
    for name, policy in CANDIDATES.items():
        path = evidence / f"{name}.json"
        if not path.exists():
            disposition = "blocked-needs-acquisition" if policy["package_required"] else "blocked-environment"
            if not policy["ai_allowed"]:
                disposition = "blocked-permission"
            results["candidates"][name] = {"disposition": disposition, "missing": HARD_GATES}
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        gates = data.get("gates", {})
        missing = [g for g in HARD_GATES if gates.get(g) not in ("pass", "not-applicable")]
        requested = data.get("requested_disposition", "wrap")
        if missing:
            disposition = data.get("blocked_disposition", "reject")
        elif requested not in ("adopt", "wrap", "fork", "reject"):
            disposition = "reject"
        else:
            disposition = requested
        results["candidates"][name] = {
            "disposition": disposition,
            "missing_or_failed_gates": missing,
            "evidence_file": str(path.resolve()),
            "evidence_sha256": sha256_file(path),
        }
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("preflight")
    p.add_argument("--output", required=True)
    p.add_argument("--ue-root")
    p.add_argument("--search-root", action="append", default=[])
    p.set_defaults(func=preflight)
    e = sub.add_parser("evaluate")
    e.add_argument("--evidence", required=True)
    e.add_argument("--output", required=True)
    e.set_defaults(func=evaluate)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
