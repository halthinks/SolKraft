---
name: solforge-codebase
description: "Understand how an existing repository works: trace behavior, architecture, ownership, and history at specific files and revisions."
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Investigate a repository

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Start with the question to answer and the exact checkout. Read applicable repository instructions and inspect local changes before proposing mutations. Search for the user-visible entrypoint, then trace callers, implementation, state, configuration, and tests across the relevant boundary. Expand only when those links require it; a focused question does not require an inventory of the entire repository.

Distinguish code that exists from code registered, called, reachable, and exercised. Check feature flags, generated files, alternate implementations, and error paths when they could change the answer. Use history to explain a specific behavior or regression, not as a substitute for inspecting current code.

For competing explanations, state the discriminating observation and collect it. Prefer a small reproduction or existing relevant test when it can resolve uncertainty. Inspection alone does not establish runtime behavior.

Answer with the finding, concrete file/function evidence, relevant dependency path, and unresolved uncertainty. If changes were requested, carry the evidence into implementation; otherwise deliver the investigation without starting a repair.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
