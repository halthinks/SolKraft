from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("audit_worktrees.py")


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def require_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise AssertionError(f"{label} failed: {result.stdout}\n{result.stderr}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="audit-git-worktrees-") as raw:
        temp = Path(raw)
        repo = temp / "repo"
        peer = temp / "peer"
        output_a = temp / "audit-a.json"
        output_b = temp / "audit-b.json"
        repo.mkdir()
        require_ok(run("git", "init", cwd=repo), "git init")
        require_ok(run("git", "config", "user.name", "Audit Selftest", cwd=repo), "git user.name")
        require_ok(run("git", "config", "user.email", "audit@example.invalid", cwd=repo), "git user.email")
        (repo / "base.txt").write_text("base\n", encoding="utf-8", newline="\n")
        require_ok(run("git", "add", "base.txt", cwd=repo), "git add")
        require_ok(run("git", "commit", "-m", "base", cwd=repo), "base commit")
        require_ok(run("git", "worktree", "add", "-b", "audit-peer", str(peer), cwd=repo), "worktree add")
        (peer / "peer.txt").write_text("peer\n", encoding="utf-8", newline="\n")
        require_ok(run("git", "add", "peer.txt", cwd=peer), "peer add")
        require_ok(run("git", "commit", "-m", "peer", cwd=peer), "peer commit")
        (peer / "dirty.txt").write_text("dirty\n", encoding="utf-8", newline="\n")

        first = run(
            sys.executable, "-B", str(SCRIPT), "--repo", str(repo), "--output", str(output_a), cwd=temp
        )
        require_ok(first, "first audit")
        second = run(
            sys.executable, "-B", str(SCRIPT), "--repo", str(repo), "--output", str(output_b), cwd=temp
        )
        require_ok(second, "second audit")
        payload = json.loads(output_a.read_text(encoding="utf-8"))
        assert output_a.read_bytes() == output_b.read_bytes()
        assert set(payload) == {"schema_version", "main_head", "summary", "worktrees", "failures"}
        assert payload["schema_version"] == 1
        assert payload["failures"] == []
        assert payload["summary"] == {
            "registered": 2,
            "existing": 2,
            "clean": 1,
            "dirty": 1,
            "merged_or_ancestor": 1,
            "not_ancestor": 1,
        }
        peer_rows = [row for row in payload["worktrees"] if Path(row["path"]) == peer]
        assert len(peer_rows) == 1
        peer_row = peer_rows[0]
        assert peer_row["status_rows"] == 1
        assert peer_row["status_sample"] == ["?? dirty.txt"]
        assert peer_row["head_is_ancestor_of_main"] is False
        print(json.dumps({"status": "pass", "summary": payload["summary"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
