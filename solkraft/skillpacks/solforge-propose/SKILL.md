---
name: solforge-propose
description: Turn research or a codebase audit into a concrete implementation proposal with scoped changes and verification.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Propose

Turn research or a codebase audit into a concrete implementation proposal with scoped changes and verification.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Identify the current user outcome, work stage, required inputs, valid completed evidence, unresolved decisions, and available host tools. Preserve explicit exclusions and the latest user correction.

Select one primary procedure per stage, with support only for distinct constraints. Order work by dependencies, retain mandatory contracts and contrary evidence, and identify capability or authority gaps rather than inventing them.

Challenge the proposed route or result with concrete missing requirements, stale evidence, failure modes, and unnecessary work. Replan only affected dependencies; use delegation only when separately authorized and useful.

Return the requested route, proposal, context, review, or correction and continue already authorized work. Pause and Stop end new task dispatch; Resume begins at the first unverified unit. No widget cursor or extra confirmation ceremony is required.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
