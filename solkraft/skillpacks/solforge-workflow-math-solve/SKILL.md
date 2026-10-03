---
name: solforge-workflow-math-solve
description: Develop a rigorous solution or derivation with checked assumptions, intermediate results, and explicit limits.
---

# Solve a mathematical problem

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact statement before computing: the definitions in force, hypotheses on every variable and parameter (domains, sign, regularity, convergence), allowed methods or tools, and the form of the expected answer — closed form, constructive procedure, bound, or numerical value with tolerance. Confirm the acceptance criteria; a correct answer to a misread problem is a failed task.

Classify the problem and reduce it to a structure with a known method before calculating. Carry the derivation in explicit steps, stating the condition that licenses each non-reversible transformation: dividing requires a nonvanishing quantity, squaring or substitution can introduce extraneous candidates, exchanging limits, sums, or integrals requires its convergence hypothesis. Keep intermediate results inspectable; when a path stalls, change representations rather than repeating the same manipulation.

Verify the result independently of the derivation that produced it. Back-substitute candidates into the original statement and discard extraneous roots. Test boundary and degenerate cases: zero or limiting parameters, n = 0, empty or unbounded domains. Cross-check by a second method, a magnitude estimate, or a numerical spot check against the analytic form. Numerical agreement at a few points is not proof of a general identity, and computer-algebra output is evidence only after its branch and domain assumptions match the problem's.

Report the solution with its derivation, the condition attached to each key step, the checks performed, and the explicit limits of validity — parameter ranges, undischarged assumptions, or cases left open. Use [math verification](../solforge-workflow-math-verify/SKILL.md) when the result needs a line-by-line audit of inferences and hidden assumptions beyond the solver's own checks.
