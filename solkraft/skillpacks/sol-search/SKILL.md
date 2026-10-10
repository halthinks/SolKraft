---
name: sol-search
description: "Find current facts, primary sources, and contrary evidence for research, comparisons, technical questions, or claim checks. Use when an answer needs sourced evidence."
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Sol Search

Answer the user's exact research question in the current task using native browsing and file tools. This is a general research workflow; it does not require or call SolForge MCP, widgets, or capsules.

Preserve every supplied source, repository, file, and scope constraint. Investigate material claims using primary evidence; inspect relevant implementation when a repository is in scope. Distinguish fact, inference, recommendation, and unknown. Track source versions, contrary evidence, uncertainty, and what each source can establish. Research alone authorizes no implementation or external effects, and no delegation without the user's explicit request.

For substantial research, comparisons, repository studies, or consequential claims, read [the research contract](references/research-contract.md). Keep its full source/claim ledger and applicable challenge audits. A simple factual lookup needs the relevant source and a bounded answer, not an elaborate report.

Lead with the answer and place citations near supported claims. Explain decision implications, limitations, and decisive missing evidence. Deliver in chat unless files were requested. Finish when required inputs are accounted for and material conclusions are supported or explicitly uncertain.

When the user also requests implementation, analysis, or a durable report, pass the research evidence to the matching [SolForge workflow](../solforge/SKILL.md). This handoff uses native skills; it never changes the research-only authority boundary or implicitly starts another phase.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
