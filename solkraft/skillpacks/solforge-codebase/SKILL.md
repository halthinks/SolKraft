---
name: solforge-codebase
description: "Understand how an existing repository works: trace behavior, architecture, ownership, and history at specific files and revisions."
---

# Investigate a repository

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Start with the question to answer and the exact checkout. Read applicable repository instructions and inspect local changes before proposing mutations. Search for the user-visible entrypoint, then trace callers, implementation, state, configuration, and tests across the relevant boundary. Expand only when those links require it; a focused question does not require an inventory of the entire repository.

Distinguish code that exists from code registered, called, reachable, and exercised. Check feature flags, generated files, alternate implementations, and error paths when they could change the answer. Use history to explain a specific behavior or regression, not as a substitute for inspecting current code.

For competing explanations, state the discriminating observation and collect it. Prefer a small reproduction or existing relevant test when it can resolve uncertainty. Inspection alone does not establish runtime behavior.

Answer with the finding, concrete file/function evidence, relevant dependency path, and unresolved uncertainty. If changes were requested, carry the evidence into implementation; otherwise deliver the investigation without starting a repair.

Read [legacy capability detail](references/capability-detail.md) only for an explicitly requested legacy work-bundle protocol.
