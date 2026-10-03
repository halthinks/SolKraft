#!/usr/bin/env python3
"""Create and maintain a structured deep-research dossier."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path


SOURCE_FIELDS = ["id", "title", "url", "type", "quality", "relevance", "date_accessed", "note"]
CLAIM_FIELDS = ["id", "claim", "status", "confidence", "evidence", "note"]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "research"


def ensure_csv(path: Path, fields: list[str]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()


def read_rows(path: Path, fields: list[str]) -> list[dict[str, str]]:
    ensure_csv(path, fields)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def workspace_from_args(args: argparse.Namespace) -> Path:
    workspace = Path(getattr(args, "workspace", ".")).expanduser().resolve()
    return workspace


def manifest_path(workspace: Path) -> Path:
    return workspace / "dossier.json"


def load_manifest(workspace: Path) -> dict[str, str]:
    path = manifest_path(workspace)
    if not path.exists():
        raise SystemExit(f"No dossier found at {workspace}. Run init first or pass --workspace.")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return "\n".join(lines)


def command_init(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else root / f"{date.today().isoformat()}-{slugify(args.topic)}"
    workspace.mkdir(parents=True, exist_ok=True)

    manifest = {
        "topic": args.topic,
        "created": date.today().isoformat(),
        "question": args.question or args.topic,
        "decision": args.decision or "",
    }
    with manifest_path(workspace).open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")

    ensure_csv(workspace / "sources.csv", SOURCE_FIELDS)
    ensure_csv(workspace / "claims.csv", CLAIM_FIELDS)
    (workspace / "notes.md").write_text(f"# Notes\n\nTopic: {args.topic}\n", encoding="utf-8")
    render_report(workspace)
    print(workspace)


def command_add_source(args: argparse.Namespace) -> None:
    workspace = workspace_from_args(args)
    load_manifest(workspace)
    path = workspace / "sources.csv"
    rows = read_rows(path, SOURCE_FIELDS)
    source_id = args.id
    if any(row["id"] == source_id for row in rows):
        raise SystemExit(f"Source id already exists: {source_id}")
    rows.append(
        {
            "id": source_id,
            "title": args.title,
            "url": args.url,
            "type": args.type,
            "quality": args.quality,
            "relevance": args.relevance,
            "date_accessed": args.date_accessed or date.today().isoformat(),
            "note": args.note or "",
        }
    )
    write_rows(path, SOURCE_FIELDS, rows)
    print(f"added source {source_id}")


def command_add_claim(args: argparse.Namespace) -> None:
    workspace = workspace_from_args(args)
    load_manifest(workspace)
    path = workspace / "claims.csv"
    rows = read_rows(path, CLAIM_FIELDS)
    claim_id = args.id or f"C{len(rows) + 1}"
    if any(row["id"] == claim_id for row in rows):
        raise SystemExit(f"Claim id already exists: {claim_id}")
    rows.append(
        {
            "id": claim_id,
            "claim": args.claim,
            "status": args.status,
            "confidence": args.confidence,
            "evidence": args.evidence,
            "note": args.note or "",
        }
    )
    write_rows(path, CLAIM_FIELDS, rows)
    print(f"added claim {claim_id}")


def render_report(workspace: Path) -> None:
    manifest = load_manifest(workspace)
    sources = read_rows(workspace / "sources.csv", SOURCE_FIELDS)
    claims = read_rows(workspace / "claims.csv", CLAIM_FIELDS)

    source_rows = [
        [row["id"], row["title"], row["type"], row["quality"], row["relevance"], row["note"]]
        for row in sources
    ]
    claim_rows = [
        [row["id"], row["claim"], row["status"], row["confidence"], row["evidence"], row["note"]]
        for row in claims
    ]

    report = f"""# Deep Research Dossier: {manifest["topic"]}

## Executive Answer

- Replace this section with the concise answer after research.

## Scope And Method

- Research question: {manifest.get("question", manifest["topic"])}
- Decision this supports: {manifest.get("decision", "")}
- Date researched: {date.today().isoformat()}
- Dossier workspace: `{workspace}`

## Source Ledger

{markdown_table(["ID", "Source", "Type", "Quality", "Relevance", "Why it matters"], source_rows) if source_rows else "_No sources recorded yet._"}

## Claim Matrix

{markdown_table(["ID", "Claim", "Status", "Confidence", "Evidence", "Notes"], claim_rows) if claim_rows else "_No claims recorded yet._"}

## Findings

Group findings by theme. Separate facts from inferences.

## Contradictions And Gaps

List conflicts, missing data, failed searches, and unknowns.

## Local Repo Impact

Tie findings back to local files, code, docs, model artifacts, or tests.

## Recommendations

Rank next actions by impact and confidence.

## Appendix

Add search queries, local commands, benchmark notes, and short compliant quotes.
"""
    (workspace / "report.md").write_text(report, encoding="utf-8")


def command_render(args: argparse.Namespace) -> None:
    workspace = workspace_from_args(args)
    render_report(workspace)
    print(workspace / "report.md")


def command_status(args: argparse.Namespace) -> None:
    workspace = workspace_from_args(args)
    manifest = load_manifest(workspace)
    sources = read_rows(workspace / "sources.csv", SOURCE_FIELDS)
    claims = read_rows(workspace / "claims.csv", CLAIM_FIELDS)
    supported = sum(1 for row in claims if row["status"] == "supported")
    print(f"topic: {manifest['topic']}")
    print(f"workspace: {workspace}")
    print(f"sources: {len(sources)}")
    print(f"claims: {len(claims)} ({supported} supported)")
    print(f"report: {workspace / 'report.md'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a dossier workspace")
    init.add_argument("--topic", required=True)
    init.add_argument("--question")
    init.add_argument("--decision")
    init.add_argument("--root", default="research")
    init.add_argument("--workspace")
    init.set_defaults(func=command_init)

    source = sub.add_parser("add-source", help="Record a source")
    source.add_argument("--workspace", default=".")
    source.add_argument("--id", required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--type", default="web")
    source.add_argument("--quality", choices=["low", "medium", "high"], default="medium")
    source.add_argument("--relevance", choices=["low", "medium", "high"], default="medium")
    source.add_argument("--date-accessed")
    source.add_argument("--note")
    source.set_defaults(func=command_add_source)

    claim = sub.add_parser("add-claim", help="Record a claim and evidence IDs")
    claim.add_argument("--workspace", default=".")
    claim.add_argument("--id")
    claim.add_argument("--claim", required=True)
    claim.add_argument("--status", choices=["supported", "mixed", "unsupported", "speculative"], default="supported")
    claim.add_argument("--confidence", choices=["low", "medium", "high"], default="medium")
    claim.add_argument("--evidence", required=True)
    claim.add_argument("--note")
    claim.set_defaults(func=command_add_claim)

    render = sub.add_parser("render", help="Render report.md from ledger files")
    render.add_argument("--workspace", default=".")
    render.set_defaults(func=command_render)

    status = sub.add_parser("status", help="Show dossier status")
    status.add_argument("--workspace", default=".")
    status.set_defaults(func=command_status)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
