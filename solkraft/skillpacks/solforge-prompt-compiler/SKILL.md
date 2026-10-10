---
name: solforge-prompt-compiler
description: Compile an objective, selected workflows, inputs, constraints, and acceptance criteria into an execution prompt.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Prompt Compiler

Compile an objective, selected workflows, inputs, constraints, and acceptance criteria into an execution prompt.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Translate the request into a concise executable instruction with the actual objective, inputs, constraints, acceptance checks, and available capabilities. Preserve exclusions and distinguish source material from instructions. Validate that the result adds no invented tools, authority, or mandatory protocol.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
