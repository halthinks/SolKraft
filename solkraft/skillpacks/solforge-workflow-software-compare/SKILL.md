---
name: solforge-workflow-software-compare
description: Inspect implementations symmetrically against explicit criteria, evidence parity, and decision sensitivity.
---

# Compare software implementations

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the decision the comparison must inform, the named alternatives pinned to specific revisions or versions, and the explicit criteria before inspecting any candidate — criteria written after seeing results rationalize rather than evaluate. Where the request implies weighting across correctness, performance, complexity, dependency surface, license, maintenance burden, or portability, record it; unstated weights hide the actual decision.

Apply every criterion symmetrically. Run candidates against the same workload, harness, configuration, and environment, and inspect actual source or observed behavior rather than README or marketing claims. Benchmarks measured on different machines, build flags, or datasets are not comparable evidence — rerun them under parity or state the asymmetry as a finding. Measure realistic load and failure modes, not microbenchmarks tuned to flatter one candidate; comparing one candidate's documentation against another's source is evidence asymmetry, not analysis.

Distinguish functional equivalence from non-functional difference: two implementations can produce identical outputs yet differ sharply in complexity, error handling, dependency risk, or operational cost. Then test decision sensitivity — identify which criteria dominate the ranking and whether the outcome flips under plausible changes in weights or workload. A ranking that inverts under small weight changes is a tie with stated conditions, not a winner.

Report the criteria, the evidence per candidate per criterion with its provenance, the recommendation with its sensitivity, and unresolved gaps where parity could not be achieved. Use [comparison execution](../solforge-run-comparison/SKILL.md) when the underlying comparison method needs more procedure than this stage supplies.
