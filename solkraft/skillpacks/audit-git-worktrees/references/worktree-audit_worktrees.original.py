from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("worktree-audit.json")


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def records() -> list[dict[str, str]]:
    raw = run("git", "worktree", "list", "--porcelain").stdout
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


def main() -> int:
    main_head = run("git", "rev-parse", "HEAD").stdout.strip()
    rows = []
    failures = []
    for item in records():
        path = Path(item["worktree"])
        exists = path.is_dir()
        status = run("git", "status", "--porcelain=v1", cwd=path) if exists else None
        head = run("git", "rev-parse", "HEAD", cwd=path) if exists else None
        ancestor = run("git", "merge-base", "--is-ancestor", (head.stdout.strip() if head else item.get("HEAD", "")), main_head)
        row = {
            "path": str(path),
            "exists": exists,
            "head": head.stdout.strip() if head and head.returncode == 0 else item.get("HEAD"),
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
    payload = {"schema_version": 1, "main_head": main_head, "summary": summary, "worktrees": rows, "failures": failures}
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
