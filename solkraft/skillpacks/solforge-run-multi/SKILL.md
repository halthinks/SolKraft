---
name: solforge-run-multi
description: Execute an authorized multi-agent plan with bounded ownership, handoffs, and root integration.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Run Multi

Execute an authorized multi-agent plan with bounded ownership, handoffs, and root integration.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.


Apply this procedure directly within the current task. Reuse valid inputs and completed work; read a linked method only when it adds missing guidance. Return the requested result. Consult the [router](../solforge/SKILL.md) only if the next useful workflow is unclear.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
