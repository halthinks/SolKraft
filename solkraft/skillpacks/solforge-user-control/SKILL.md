---
name: solforge-user-control
description: Apply user Pause, Resume, Stop, and scope corrections during active work.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge User Control

Apply user Pause, Resume, Stop, and scope corrections during active work.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Treat Pause, Stop, Resume, exclusions, and scope corrections as direct user controls. Stop new dispatch after Pause or Stop, preserve recoverable state, and explain the current boundary. Resume only after the user requests it; approval for one target or effect never grants another.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
