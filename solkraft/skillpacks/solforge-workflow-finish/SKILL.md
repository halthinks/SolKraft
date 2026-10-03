---
name: solforge-workflow-finish
description: Explicitly accept the completed result as the final deliverable without creating another execution or report work bundle.
---

# Accept the completed result

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the original objective, the acceptance criteria in effect, and which deliverable is being accepted. Identify the result's final form and location — the file, artifact, deployed state, or message the user will actually use — and distinguish it from scratch copies, intermediates, and work-in-progress. Reuse verification evidence that is still valid for the current artifact; a completed check need not be repeated, but evidence gathered against an older build or earlier draft does not cover the result being accepted now.

Inspect the actual deliverable before accepting it. Spot-check its material claims against the acceptance criteria: open the produced file, run the key command, or exercise the primary behavior rather than trusting a prior summary that the work passed. Confirm nothing in scope was silently dropped — an item skipped because it was hard is an open limit, not a completed item — and that unrelated user work and existing state were preserved. A plan, a queued action, or a summary of intent is not the deliverable; accept only what demonstrably exists.

Acceptance is a decision, not another stage of work. Do not manufacture a new execution, report, or packaging bundle as a condition of finishing, and do not re-run verification whose results already cover this artifact. If inspection reveals a real gap, name it and either resolve it within the current scope or carry it as an explicit limit — do not widen the task or route into a new workflow just to avoid stating the gap.

Report what was accepted, the evidence inspected, and any remaining limits or unsupported claims. Use [finalize](../solforge-finalize/SKILL.md) when the deliverable still needs its verification evidence assembled or requested handoff artifacts produced before acceptance.
