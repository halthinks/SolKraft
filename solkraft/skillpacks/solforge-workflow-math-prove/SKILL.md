---
name: solforge-workflow-math-prove
description: Construct and audit a proof using independent approaches, lemma tracking, and adversarial counterexample checks.
---

# Prove a mathematical statement

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact statement, the definitions in force, the permitted methods and accepted background theorems, and the acceptance standard — full rigor versus an argued sketch, and the intended audience. Pin down ambiguous quantifiers, hypotheses, and domains before proving anything. If the statement as given is false or underdetermined, report that with a counterexample or missing hypothesis rather than silently proving a weakened or strengthened variant.

Choose the strategy from the statement's shape: induction for claims over naturals or recursively built structures, contradiction or contraposition when the negation gives more to work with, explicit construction for existence claims, and case analysis only when the cases are demonstrably exhaustive. Decompose into named lemmas, track which results each lemma depends on, and prove lemmas before the arguments that cite them. Then attempt at least one genuinely independent check of the conclusion — a second proof strategy, direct computation on representative or extremal instances, or derivation from a known theorem — and reconcile any disagreement; two write-ups that share one unproven lemma are not independent evidence.

Audit the finished argument adversarially. Probe boundary and degenerate cases the hypotheses allow — empty structures, n = 0, zero divisors, coincident points, divergence at the limit — and actively search for counterexamples to each lemma, not only to the headline claim. A step justified as "clearly" or "obviously," a cited theorem whose side conditions go unchecked, a case split with an unexamined overlap, or verification limited to the example that motivated the conjecture is weak evidence. Numeric or symbolic computation over finitely many instances corroborates but does not prove a universal claim unless the reduction to those instances is itself proven.

Report the proof or proof program, the status of every lemma, the independent checks applied and their outcomes, and any remaining gap, extra assumption, or excluded case stated plainly. Use [proof verification](../solforge-workflow-math-verify/SKILL.md) for a dedicated audit of a finished argument or when a found gap needs a bounded repair.
