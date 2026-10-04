---
name: solforge-workflow-data-validate
description: "Check a dataset for missing values, duplicates, inconsistent types, leakage, and other quality defects before relying on its results."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Validate a dataset before relying on it

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish what one row represents (the grain), the declared schema, the metric definitions in use, and the analysis question the data must answer, plus the user's scope and acceptance criteria. Record provenance for each source: where it came from, when it was extracted, and what transformations were already applied. Validate the actual data, not a description or sample of it.

Profile before judging. Compare row counts and key cardinality against expectations; measure missingness per column and distinguish structural gaps from extraction errors; check for duplicate keys at the declared grain, inconsistent types and units across partitions, out-of-range or implausible values against domain knowledge, and broken referential integrity across joined tables. For data feeding a model or decision, check leakage: fields that could not have been known at decision time, future-dated values, and identifiers spuriously correlated with the target. Recompute reported aggregates and derived metrics from source rows rather than trusting the totals.

Distinguish defects from legitimate properties of the domain: a zero may be real, an outlier may be the signal, and a missing value may carry meaning. Quantify each defect — affected rows, columns, and share — and judge materiality against the analysis question instead of applying blanket rules. A passing schema check is not evidence the values are correct, and validating a convenience sample is not evidence about the whole dataset. Never silently coerce, impute, or drop rows and present the result as the original data; record every transformation applied.

Report defects by severity and materiality, provenance and leakage findings, which checks ran and which could not (and why), and whether the data supports the intended use. Validation identifies and characterizes defects; it does not repair them without authorization. Use [research execution](../solforge-run-research/SKILL.md) when tracing a defect's origin requires source or lineage investigation beyond the dataset itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
