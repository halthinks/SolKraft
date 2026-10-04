---
name: solforge-mvp
description: Define and deliver a bounded working MVP or vertical slice with acceptance evidence and explicit exclusions.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge MVP

Define and deliver a bounded working MVP or vertical slice with acceptance evidence and explicit exclusions.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Define the smallest usable outcome with explicit users, critical journey, acceptance evidence, and deferred features. Identify dependencies that must actually work for that journey. Return the requested scope or decision; implementing it requires an implementation request.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
