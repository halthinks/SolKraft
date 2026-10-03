---
name: solforge-workflow-data-analyze
description: Execute a reproducible analysis with grain, definitions, assumptions, uncertainty, and decision implications.
---

# Analyze data reproducibly

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the analysis question, the dataset and its grain — what one row represents — the metric definitions, filters and time windows in scope, and the acceptance criteria. Inspect the actual source before computing: schema, sample rows, row counts, key uniqueness, and freshness. If the data cannot answer the question at the requested grain, say so and identify the missing source or aggregation rather than producing a confident-looking proxy.

Profile before aggregating: distributions, missingness, duplicates, outliers, and category coverage at the raw grain. Compute at the lowest grain first, then aggregate, recording every transformation and filter with row counts before and after so a dropped segment is visible rather than silent. Choose methods proportional to the question — summary, comparison, or trend — and check the assumptions each carries: correct denominators, population coverage, independence of observations, and whether a comparison group is actually comparable. Keep correlation and causation distinct unless the design supports the stronger claim.

Verify the headline numbers before reporting them. Recompute at least the load-bearing figure with an independent query or path, and reconcile aggregates against known totals or prior reports; a result that cannot be recomputed from the recorded steps is not a finding. State uncertainty honestly: sample size, sensitivity to definition and window choices, and plausible alternative explanations. Named anti-patterns: aggregates over silently dropped nulls, percentage changes on tiny bases, cherry-picked date windows, and p-hacked slices presented as the original question.

Report the question, data window and grain, metric definitions, method, results with uncertainty, limitations, and the decision implications — keeping facts, inferences, and recommendations distinct. Deliver the reproducible notebook or script alongside the report when requested. Use [data validation](../solforge-workflow-data-validate/SKILL.md) when source quality itself is unverified and the conclusions would rest on it.
