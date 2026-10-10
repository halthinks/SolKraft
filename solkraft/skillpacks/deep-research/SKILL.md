---
name: deep-research
description: Use when the user asks for deep research, literature review, source-backed analysis, technical due diligence, market or policy research, model/dataset/paper investigation, repo-connected research, or a cited report with evidence, uncertainty, and recommendations.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Deep Research

## Overview

Use this skill to turn open-ended research into a traceable dossier. The output must separate sourced facts, reasoned inferences, uncertainty, and recommendations.

## Workflow

1. Scope the question: identify the decision the research should support, audience, constraints, and required freshness. Ask at most one clarifying question if scope is ambiguous; otherwise proceed with stated assumptions.
2. Create a dossier workspace with `scripts/research_dossier.py init --topic "<topic>"`.
3. Gather sources using the best available tools. Browse for current information, use primary sources for technical claims, and prefer papers, official docs, standards, datasets, code repos, and maintainer documentation over summaries.
4. Record every material source with `add-source`. Include title, URL/path, source type, date, quality, relevance, and a short note.
5. Build a claim matrix with `add-claim`. Each important conclusion needs evidence IDs and a confidence level. Mark unsupported or speculative claims clearly.
6. Synthesize findings into the generated `report.md`: executive answer, evidence table, contradictions, uncertainty, repo impact, and next actions.
7. Verify the report before finalizing: source links work or local files exist, direct quotes are short, claims point to evidence IDs, and recommendations do not overstate the evidence.

## Source Standards

- Technical implementation claims: use official docs, upstream repos, issue threads from maintainers, release notes, standards, or papers.
- ML research claims: use papers, dataset cards, model cards, benchmark code, upstream training code, and reproducible evaluation artifacts.
- Market/legal/medical/financial/current claims: browse current sources and include dates.
- Local-code claims: cite absolute local paths and line numbers when useful.
- Do not cite low-quality summaries as primary evidence when a primary source exists.

## Tool

Run the bundled helper from this skill directory:

```powershell
& '<python.exe>' scripts\research_dossier.py init --topic "WiFi CSI pose estimation for RuView"
& '<python.exe>' scripts\research_dossier.py add-source --id S1 --title "Paper title" --url "https://..." --type paper --quality high --relevance high --note "Why it matters"
& '<python.exe>' scripts\research_dossier.py add-claim --claim "Claim text" --evidence S1,S2 --confidence medium --status supported --note "Boundary conditions"
& '<python.exe>' scripts\research_dossier.py status
& '<python.exe>' scripts\research_dossier.py render
```

Use the absolute Python path when `python` is not on PATH. On this machine that is commonly `<configured-path>`.

## Report Shape

Use `references/report-template.md` for the final structure. Keep the final answer concise, but leave the full dossier on disk when the research is substantial.

## Common Mistakes

- Treating a vendor blog or secondary explainer as the source of truth when a paper, docs page, or repo exists.
- Mixing facts with inferences. Label inferences explicitly.
- Overclaiming model performance from a dataset or paper without matching hardware, environment, and evaluation setup.
- Omitting negative evidence, contradictions, failed searches, or limits.
- Finishing without a claim matrix.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
