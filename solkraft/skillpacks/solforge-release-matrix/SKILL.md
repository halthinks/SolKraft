---
name: solforge-release-matrix
description: Reconcile platform artifacts, signing, provenance, update support, and release-readiness evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Release Matrix

Reconcile platform artifacts, signing, provenance, update support, and release-readiness evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Build a target-by-target matrix of artifact identity, build result, installation or launch result, compatibility, and unresolved release gates. Keep missing, failed, and passed checks distinct. Promote a target only on evidence for that exact artifact and environment.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
