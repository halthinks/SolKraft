---
name: solforge-context-curator
description: Select the requirements, sources, skills, and evidence needed at the current stage of substantial work.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Context Curator

Select the requirements, sources, skills, and evidence needed at the current stage of substantial work.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Keep the smallest sufficient working context: the latest request, mandatory contracts, relevant source boundaries, decisions already made, and evidence still needed. Mark stale observations and unresolved dependencies. Retrieve deeper references only when the next action needs them; preserve this compact context across continuation.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
