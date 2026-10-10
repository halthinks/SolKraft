---
name: solforge-finalize
description: Deliver completed work with its verification evidence, remaining limits, and requested handoff artifacts.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Finalize

Deliver completed work with its verification evidence, remaining limits, and requested handoff artifacts.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Reconcile the requested outcome against actual files, executed checks, and repository state. Verify that the handoff identifies the exact revision or artifact, explains how to use it, and separates completed work from blockers. Deliver the requested result without inventing publication, deployment, or qualification evidence.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
