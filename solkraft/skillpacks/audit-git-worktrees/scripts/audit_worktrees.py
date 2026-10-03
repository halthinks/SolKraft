from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def records(root: Path) -> list[dict[str, str]]:
    raw = run("git", "worktree", "list", "--porcelain", cwd=root).stdout
    result: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in raw.splitlines() + [""]:
        if not line:
            if current:
                result.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return result


def audit(root: Path) -> tuple[dict[str, object], list[str]]:
    root_probe = run("git", "rev-parse", "--show-toplevel", cwd=root)
    if root_probe.returncode != 0:
        raise RuntimeError(
            f"not a readable Git repository: {root}: {root_probe.stderr.strip()}"
        )
    canonical_root = Path(root_probe.stdout.strip()).resolve()
    main_head_probe = run("git", "rev-parse", "HEAD", cwd=canonical_root)
    if main_head_probe.returncode != 0:
        raise RuntimeError(
            f"cannot resolve canonical HEAD: {canonical_root}: {main_head_probe.stderr.strip()}"
        )
    main_head = main_head_probe.stdout.strip()
    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for item in records(canonical_root):
        path = Path(item["worktree"])
        exists = path.is_dir()
        status = run("git", "status", "--porcelain=v1", cwd=path) if exists else None
        head = run("git", "rev-parse", "HEAD", cwd=path) if exists else None
        head_value = head.stdout.strip() if head and head.returncode == 0 else item.get("HEAD", "")
        ancestor = run(
            "git", "merge-base", "--is-ancestor", head_value, main_head,
            cwd=canonical_root,
        )
        row = {
            "path": str(path),
            "exists": exists,
            "head": head_value or None,
            "branch": item.get("branch"),
            "detached": "detached" in item,
            "locked": item.get("locked"),
            "prunable": item.get("prunable"),
            "status_rows": len(status.stdout.splitlines()) if status and status.returncode == 0 else None,
            "status_sample": status.stdout.splitlines()[:20] if status else [],
            "head_is_ancestor_of_main": ancestor.returncode == 0,
        }
        if not exists or status is None or status.returncode != 0:
            failures.append(f"unreadable:{path}")
        rows.append(row)
    summary = {
        "registered": len(rows),
        "existing": sum(1 for row in rows if row["exists"]),
        "clean": sum(1 for row in rows if row["status_rows"] == 0),
        "dirty": sum(1 for row in rows if isinstance(row["status_rows"], int) and row["status_rows"] > 0),
        "merged_or_ancestor": sum(1 for row in rows if row["head_is_ancestor_of_main"]),
        "not_ancestor": sum(1 for row in rows if not row["head_is_ancestor_of_main"]),
    }
    payload: dict[str, object] = {
        "schema_version": 1,
        "main_head": main_head,
        "summary": summary,
        "worktrees": rows,
        "failures": failures,
    }
    return payload, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only evidence-bound audit of registered Git worktrees."
    )
    parser.add_argument("--repo", required=True, type=Path, help="Canonical Git repository root.")
    parser.add_argument("--output", required=True, type=Path, help="Audit JSON output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload, failures = audit(args.repo.resolve())
    except Exception as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, sort_keys=True))
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"summary": payload["summary"], "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
