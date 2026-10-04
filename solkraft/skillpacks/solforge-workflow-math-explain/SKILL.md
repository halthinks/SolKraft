---
name: solforge-workflow-math-explain
description: Produce a level-appropriate explanation with intuition, formal steps, examples, diagrams, and limitations.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Explain a mathematical result

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact statement to be explained, its assumptions, the audience's level and prerequisites, and any constraints on notation or allowed methods. Pin down definitions before prose: an explanation built on an ambiguous term fails regardless of style. Determine what the reader must be able to do afterward — reconstruct the argument, apply the method, or recognize when it fails — since that decides depth, not the writer's preference.

Order the explanation motivation before mechanism. Give the intuition that makes the result plausible, state it formally, then develop the argument in steps the intended reader can actually follow, naming each non-obvious inference and the hypothesis it consumes. Choose examples that carry weight: one generic case, one boundary or degenerate case, and one non-example showing where the hypotheses are essential. Include a diagram only when it conveys structure the text cannot, and keep notation consistent from first use to last.

Verify the explanation, not just its polish. Recompute every worked example independently, check each cited fact against a source or derivation, and audit that no step silently uses a stronger assumption than stated. Named anti-patterns: an example covering only the trivial case is weak evidence of understanding; a plausible heuristic presented as the reason a theorem holds is not a proof; a numerical check does not establish a general statement; "clearly" marking the step that actually needs justification hides the gap. Distinguish intuition, proof, and conjecture explicitly.

Return the explanation with its assumed level, verified examples, and stated limitations or open subtleties. Use [report production](../solforge-run-report-write/SKILL.md) when the explanation must be assembled, reviewed, and exported as a larger document beyond the explanation itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
