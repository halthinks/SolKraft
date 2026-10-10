---
name: sol-merge-report
description: Compare candidate and target repositories for evidence-backed adoption, reuse, licensing, and integration decisions.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Sol Merge Report

Compare candidate and target repositories for evidence-backed adoption, reuse, licensing, and integration decisions.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Inspect the exact base, head, ancestry, changed contracts, and validation evidence. Explain integrated changes, unresolved conflicts, and remaining compatibility or verification gaps. A merged commit proves source integration; it does not prove deployment or product qualification.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
