---
name: solforge-run-comparison
description: Compare repositories, products, architectures, or evidence sets using symmetric criteria and sources.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

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
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
