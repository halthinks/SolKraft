---
name: solforge-prompt-multi
description: Write a coordinated multi-agent execution prompt with ownership, dependencies, handoffs, and integration checks.
---

# SolForge Prompt Multi

Write a coordinated multi-agent execution prompt with ownership, dependencies, handoffs, and integration checks.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Read [capability detail](references/capability-detail.md) when the requested scope needs the full domain-specific criteria. Legacy runtime steps in that reference apply only to an explicitly requested legacy protocol.

Apply this procedure directly within the current task. Reuse valid inputs and completed work; read a linked method only when it adds missing guidance. Return the requested result. Consult the [router](../solforge/SKILL.md) only if the next useful workflow is unclear.

Prompt generation produces a prompt; it does not execute that prompt or authorize agents.
