---
name: solforge-workflow-data-model
description: Build and validate a transparent model with baselines, holdouts, sensitivity, drift, and limitations.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Model data

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the analysis question, the dataset and its grain, the target and metric definitions, and the acceptance criteria before fitting anything. Inspect the actual data — row counts, ranges, missingness, key distributions, and time coverage — rather than trusting a schema or a sample of head rows. Confirm the split unit matches the prediction unit: if you forecast per customer per week, leakage check, split, and score at that grain.

Fit a simple baseline first (naive persistence, historical mean, or a linear model) and require every candidate model to beat it on the same held-out data. Choose the split to match deployment: random splits only for exchangeable rows, time-ordered splits with an embargo for forecasting, group splits when entities repeat. Keep the final holdout untouched until selection is done; a model tuned against the holdout has no honest evaluation left. Check for leakage by tracing every feature's availability at prediction time — a feature derived from the outcome or from future rows invalidates the result no matter how good the score looks.

Report performance with the metric tied to the decision, plus sensitivity: how the result moves across hyperparameter choices, segments, and reasonable data perturbations. For forecasts, give intervals, not point values alone. Check drift between training and serving distributions, and state the range where the model should not be trusted. A single aggregate metric is weak evidence — show per-segment or per-horizon breakdowns where failure would concentrate, and do not present cross-validation scores as evidence about future data when the split was random over time.

Deliver the model package with its training data version, features, parameters, and scores so the result is reproducible. Report what was verified, the margin over baseline, known limitations, and where the model degrades. Use [data validation](../solforge-workflow-data-validate/SKILL.md) first when the input dataset's quality has not been established.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
