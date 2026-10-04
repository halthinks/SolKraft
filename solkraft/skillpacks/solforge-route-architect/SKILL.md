---
name: solforge-route-architect
description: Compose a workflow graph with explicit inputs, dependencies, output checks, and conditional next steps.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

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
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
