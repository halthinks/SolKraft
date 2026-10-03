---
name: solforge-user-control
description: Apply user Pause, Resume, Stop, and scope corrections during active work.
---

# SolForge User Control

Apply user Pause, Resume, Stop, and scope corrections during active work.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Treat Pause, Stop, Resume, exclusions, and scope corrections as direct user controls. Stop new dispatch after Pause or Stop, preserve recoverable state, and explain the current boundary. Resume only after the user requests it; approval for one target or effect never grants another.
