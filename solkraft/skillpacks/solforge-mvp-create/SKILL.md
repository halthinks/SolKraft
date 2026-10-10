---
name: solforge-mvp-create
description: Turn a product brief, research result, or selected plan into a working vertical slice with a PRD and architecture.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge MVP Create

Turn a product brief, research result, or selected plan into a working vertical slice with a PRD and architecture.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Implement the agreed critical user journey end to end with real inputs and outputs. Preserve existing interfaces, make the minimal necessary dependency changes, and verify the journey in its intended runtime. Report missing integrations as gaps instead of presenting placeholders as a working MVP.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
