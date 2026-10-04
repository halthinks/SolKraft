---
name: solforge-prompt-multi
description: Write a coordinated multi-agent execution prompt with ownership, dependencies, handoffs, and integration checks.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Prompt Multi

Write a coordinated multi-agent execution prompt with ownership, dependencies, handoffs, and integration checks.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Preserve the exact downstream objective, required inputs, exclusions, authority, tools, and observable acceptance conditions. Resolve material contradictions before compiling instructions.

Write a portable prompt with dependency-ordered stages, relevant skills, evidence requirements, failure recovery, and stop conditions. For multi-agent prompts, define real ownership boundaries, handoffs, integration, and host capability prerequisites.

Check the complete prompt against every user requirement, available capability, and effect boundary. Avoid equivalent skill stacks, invented tools, fictional agent counts, or model-tier guarantees.

Return the requested prompt format. Prompt generation does not execute the downstream task, spawn agents, or grant new authority.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
