---
name: solforge-workflow-software-diagnose
description: "Diagnose crashes, errors, hangs, regressions, or unexpected software behavior; trace the failure to code and evidence before selecting a fix."
---

# Diagnose software behavior

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Capture expected versus observed behavior, the trigger, affected version or checkout, and the smallest available reproduction. Inspect the failing output and relevant code before selecting a cause. If reproduction is unavailable, keep the diagnosis provisional and identify the missing observation.

Trace the failure from the visible symptom to the owning boundary. Separate the initiating defect from downstream errors. Check relevant inputs, state transitions, configuration, dependencies, and recent changes; select probes that distinguish the leading hypotheses rather than collecting unrelated logs.

When a hypothesis is falsified, retain the observation and change the hypothesis. When a cause is supported, explain the causal chain and a focused correction. If repair is requested, demonstrate the failure with an appropriate regression check, apply the correction, and verify the original trigger plus affected neighboring behavior. Follow repository testing requirements.

Report cause, evidence, correction if performed, and remaining limits. Use [repository investigation](../solforge-codebase/SKILL.md) only when understanding the call or data path requires deeper exploration.
