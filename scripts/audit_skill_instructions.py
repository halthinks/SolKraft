#!/usr/bin/env python3
"""Audit bundled skill instructions for broken references and stale execution assumptions."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "solkraft" / "skillpacks"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_RE = re.compile(r"`([^`\n]+)`")
HOST_RUNTIME_PATTERNS = (
    ("codex", re.compile(r"\bCodex\b")),
    ("claude-code", re.compile(r"\bClaude Code\b")),
)
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|coming soon)\b", re.I)

def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            clean = target.split("#", 1)[0]
            if not clean or re.match(r"^(?:https?:|mailto:|#)", clean):
                continue
            resolved = (skill.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{skill.relative_to(ROOT)}: reference escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{skill.relative_to(ROOT)}: missing reference: {target}")
        for label, pattern in HOST_RUNTIME_PATTERNS:
            if pattern.search(text):
                warnings.append(f"{skill.relative_to(ROOT)}: named runtime wording: {label}")
        if PLACEHOLDER_RE.search(text):
            warnings.append(f"{skill.relative_to(ROOT)}: unresolved TODO/TBD/coming-soon wording")
        for code in CODE_RE.findall(text):
            if "<path-to-skill>" in code:
                continue
            if re.search(r"(?:^|\s)(?:python3?|bash|sh)\s+scripts/[^\s]+", code):
                script_path = re.search(r"(?:python3?|bash|sh)\s+(scripts/[^\s]+)", code)
                if script_path and not (skill.parent / script_path.group(1)).exists():
                    failures.append(
                        f"{skill.relative_to(ROOT)}: command references missing {script_path.group(1)}"
                    )
    print(f"skills={len(skills)} failures={len(failures)} warnings={len(warnings)}")
    for row in failures:
        print("FAIL", row)
    for row in warnings:
        print("WARN", row)
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
