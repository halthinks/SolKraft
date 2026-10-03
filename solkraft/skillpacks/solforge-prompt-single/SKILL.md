---
name: solforge-prompt-single
description: Write a single-agent execution prompt preserving the objective, required inputs, and acceptance evidence.
---

# SolForge Prompt Single

Write a single-agent execution prompt preserving the objective, required inputs, and acceptance evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Preserve the exact downstream objective, required inputs, exclusions, authority, tools, and observable acceptance conditions. Resolve material contradictions before compiling instructions.

Write a portable prompt with dependency-ordered stages, relevant skills, evidence requirements, failure recovery, and stop conditions. For multi-agent prompts, define real ownership boundaries, handoffs, integration, and host capability prerequisites.

Check the complete prompt against every user requirement, available capability, and effect boundary. Avoid equivalent skill stacks, invented tools, fictional agent counts, or model-tier guarantees.

Return the requested prompt format. Prompt generation does not execute the downstream task, spawn agents, or grant new authority.
