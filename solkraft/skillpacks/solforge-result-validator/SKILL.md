---
name: solforge-result-validator
description: "Check that a deliverable actually meets the requested outcome using inspected artifacts and observed behavior. Use before consequential completion claims."
---

# Validate the requested result

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Translate the user's actual request into observable acceptance conditions. Include supplied constraints and required inputs; do not add a new product scope. Bind each material completion claim to the exact file, revision, artifact, environment, or output that was inspected.

Evaluate evidence at the level of the claim: source inspection establishes code presence; execution establishes observed behavior; integration requires exercising the relevant boundary. Local tests do not establish deployment, installation, physical performance, or production readiness. For a document, inspect its actual contents and supporting sources; for a visual deliverable, inspect the rendered result.

Look specifically for omitted requirements, stale evidence after edits, mocks standing in for required dependencies, inaccessible outputs, and tests that cannot distinguish success from the original defect. Reuse valid checks rather than repeat them for ceremony. Independence means challenging the proposed conclusion with evidence; it does not require spawning an agent.

If a gap is fixable within the authorized task, resolve it and repeat only the affected validation. Otherwise state the unmet condition and the evidence or external action needed. Report completion only to the extent demonstrated, with remaining limitations alongside the affected claim.
