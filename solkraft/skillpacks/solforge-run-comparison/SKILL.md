---
name: solforge-run-comparison
description: Compare repositories, products, architectures, or evidence sets using symmetric criteria and sources.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Run Comparison

Compare repositories, products, architectures, or evidence sets using symmetric criteria and sources.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Choose comparable candidates and criteria tied to the actual decision. Run the same relevant checks under recorded conditions, preserve failures and tradeoffs, and explain whether differences are material. Separate measured results from inferred suitability.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
