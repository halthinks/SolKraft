---
name: solforge-route-architect
description: Compose a workflow graph with explicit inputs, dependencies, output checks, and conditional next steps.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Route Architect

Compose a workflow graph with explicit inputs, dependencies, output checks, and conditional next steps.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Compose only procedures needed for the requested deliverable. Order them by input dependencies, identify reusable completed evidence, and explain ambiguous stage selection with its trigger. Graph edges are recommendations; they do not dispatch tools or grant authority.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
