---
name: solforge-independent-challenger
description: Challenge consequential plans or results for missing evidence, unsupported assumptions, and untested failure modes.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Independent Challenger

Challenge consequential plans or results for missing evidence, unsupported assumptions, and untested failure modes.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Identify the strongest consequential claim in the proposed result. Seek a concrete counterexample, violated invariant, missing boundary case, or conflicting source. Reproduce the failure when tools permit, then report its consequence and the smallest corrective action. A clean review states the searched boundary and remaining uncertainty.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
