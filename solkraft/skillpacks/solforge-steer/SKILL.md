---
name: solforge-steer
description: Apply user corrections to scope or direction while preserving completed evidence and valid work.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Steer

Apply user corrections to scope or direction while preserving completed evidence and valid work.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Apply the latest user correction to scope, priority, or constraints. Determine which completed evidence remains valid and which dependent actions need revision. Continue from the first affected unverified action; preserve unrelated valid work and immediate stop controls.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
