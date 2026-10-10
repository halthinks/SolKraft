---
name: solforge-workflow-data-visualize
description: Build evidence-linked charts and an explanatory narrative matched to audience and decision use.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Visualize data for a decision

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the analysis question the visual must answer, the decision it supports, the audience, and the acceptance criteria before choosing any chart form. Confirm the dataset's grain, metric definitions, units, time zone, and coverage window, and inspect the actual data — row counts, types, null and duplicate rates, ranges, and outliers — rather than trusting a schema or a sample head. If the supplied data cannot support the requested comparison at the stated grain, say so and identify what is missing instead of charting around the gap.

Select each chart from the comparison being made: trends over time as lines, distributions as histograms or box plots, ranked comparisons as bars, relationships as scatter plots, and part-to-whole only when parts sum to a meaningful total. Give each chart one message, aggregate at the stated grain, and handle missing values, duplicates, and outliers by an explicit stated rule. Keep axes honest: a truncated or dual axis only when labeled and justified, shared scales across comparable panels, log scale only when named, and color encodings that survive grayscale and common color-vision deficiency. Every plotted mark must trace back to a query or transformation of the source data that can be re-run.

Verify the numbers behind the pixels: recompute spot-checked aggregates with independent queries against the source and compare them to the plotted values, then confirm labels, units, legends, and time ranges against the data actually used. A chart that renders is not evidence that its numbers are correct; do not smooth, interpolate, or filter silently, and do not present a dashboard spec or static mock as a verified deliverable without rendering it against the real data. Distinguish data-quality limits (gaps, skew, small samples) from visualization choices in the accompanying narrative, and keep claims, inferences, and unknowns distinct.

Report the deliverables produced (visual_analysis, dashboard_spec), the source and grain used, the verification checks performed, and any unresolved data limits. Use [report writing](../solforge-run-report-write/SKILL.md) when the visuals must be delivered inside a reviewed report or a requested export.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
