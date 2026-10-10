---
name: brainstorming
description: Explore product requirements and design alternatives when the user requests design help or material design decisions remain unresolved.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Brainstorming Ideas Into Designs

Develop a design that resolves the user's material product choices and is concrete enough to implement.

Use existing project context and stated requirements. Ask only for missing decisions that materially affect the result; present alternatives when the tradeoff matters. For routine choices within an authorized implementation, use judgment and continue.

Describe the outcome, component boundaries, data flow, failure behavior, and acceptance criteria at the level the task needs. Keep unrelated refactoring out of scope. For a large project, identify dependencies and a coherent first deliverable while preserving the overall objective.

If the user requested design only, deliver the design and stop before implementation. If implementation is already authorized, continue after resolving material decisions; this skill does not add a separate approval gate for every design section. Preserve any review checkpoints explicitly required by the user or repository.

Save a reusable spec when requested or when the implementation needs a durable handoff. The default location is `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`; follow project conventions or a user-selected path. Commit only within the user's authorized Git workflow.

Use a visual when it clarifies a real design decision. For the optional browser companion, obtain any required consent and read [visual-companion.md](visual-companion.md) before starting it.

Use the writing-plans skill when an implementation plan would resolve dependencies or the user asks for one. Do not force a separate planning phase for a fully specified small change.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
