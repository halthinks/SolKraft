#!/usr/bin/env python3
"""Check that a SolForge draft retains the source prompt's structural power."""

import argparse
import re
import sys


COMMON = [r"Current task statement", r"[Pp]artial progress does not count|[Pp]artial .* (?:is|are) insufficient", r"genuinely diverse portfolio|substantially different", r"registry of approach families", r"mark that route as blocked|mark .* blocked", r"several incompatible|multiple incompatible", r"adversarial", r"concrete (?:lemmas|constructions|equations|artifacts|diffs|tests|evidence|outputs)", r"Do not return merely because|Do not stop merely because", r"Return only when", r"Public search|public web|external search"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("single", "multi", "ultra"), required=True)
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()
    text = open(args.path, encoding="utf-8").read() if args.path else sys.stdin.read()
    if not text.strip(): parser.error("draft must not be empty")
    missing = [pattern for pattern in COMMON if not re.search(pattern, text)]
    if args.mode == "single" and re.search(r"launch(?:ing)? (?:new )?agents|concurrent agents", text, re.I): missing.append("single mode must not claim agent launches")
    if args.mode == "multi" and not re.search(r"Codex desktop|desktop agents|subagents", text, re.I): missing.append("multi mode must identify real desktop orchestration")
    if args.mode == "ultra" and not (re.search(r"native Ultra", text, re.I) and re.search(r"if .*not|unavailable|does not", text, re.I)): missing.append("ultra mode must contain a native-Ultra capability gate")
    if missing:
        for item in missing: print(f"MISSING: {item}", file=sys.stderr)
        return 1
    print("Transposition structure is present.")
    return 0


if __name__ == "__main__": raise SystemExit(main())
