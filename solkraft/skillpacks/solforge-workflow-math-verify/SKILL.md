---
name: solforge-workflow-math-verify
description: Check every inference, dependency, edge case, and hidden assumption; isolate gaps and propose bounded repairs.
---

# Verify or repair a proof

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact claim under audit: its statement, hypotheses, the definitions in force, and the methods or axioms allowed, plus whether the task is a full audit or a check of specific steps. Reconstruct the argument from the source rather than trusting a summary; when the proof invokes external results, confirm what those results actually assert and under which hypotheses. Note what closure is requested — a verified proof, a located gap, or a repaired theorem each end differently.

Step through the argument inference by inference, checking that each line follows from cited premises, definitions, or earlier steps. Interrogate dependencies: every invoked lemma must have its hypotheses discharged in this context, not merely in general. Probe the edge cases an argument tends to exclude silently — zero denominators, empty or degenerate configurations, boundary points, quantifier order, and hidden regularity assumptions such as finiteness, continuity, or well-definedness. Where a step is load-bearing but unjustified, attempt a counterexample at exactly that step; a targeted numeric or symbolic check falsifies faster than rereading.

Distinguish a fatal flaw from a fillable gap, and locate each at a specific step with the missing justification named. A true conclusion is not evidence the argument is valid; a step that restates or tacitly assumes the claim is circular reasoning, not a gap. Do not rescue a proof by silently adding hypotheses — a bounded repair strengthens hypotheses, restricts the claim's scope, or replaces a step, and states exactly what changed.

Report the verdict per inference or section, each located gap with its justification debt, and any repair with its effect on the theorem's scope. Mark steps accepted only under unverified external assumptions. Use [research execution](../solforge-run-research/SKILL.md) when closing a gap requires locating a supporting result in the literature.
