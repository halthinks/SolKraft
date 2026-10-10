---
name: solforge-research-mastery-loop
description: Coordinate codebase research and implementation in dependency order for a requested completion program.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Research Mastery Loop

Coordinate codebase research and implementation in dependency order for a requested completion program.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requested behavior, accepted scope, source identity, existing work, affected callers, and observable acceptance criteria. Inspect the relevant implementation and tests before choosing changes.

Order authorized changes by dependencies. Work in coherent units, preserving public contracts and state ownership. For behavior changes, reproduce the defect or add the required failing behavior test before implementation.

Verify each changed boundary with decisive checks, then inspect the actual user journey or artifact. Reuse still-valid evidence; repair failed acceptance rather than restarting completed stages.

Deliver the demonstrated result, exact verification commands and outcomes, and remaining blockers. No fixed iteration count, mandatory capsule, approval widget, or invented orchestration is required.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
