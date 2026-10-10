---
name: solforge-workflow-science-analysis
description: Apply a reproducible analysis plan with assumptions, sensitivity checks, uncertainty, and contrary evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Analyze scientific evidence

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the question or hypothesis, the data and papers actually supplied, the conditions under which they were produced, and the acceptance criteria. Decide before touching results whether the analysis is confirmatory, testing a stated hypothesis against a plan, or exploratory, searching for structure; label the outputs accordingly. Record provenance: where each dataset came from, how it was filtered, and what was excluded and why.

Write the analysis plan before running it: the estimand, the method, the assumptions it requires, and which observations would falsify it. Fit the primary analysis, then probe it — sensitivity to model specification, priors or hyperparameters, outlier and inclusion choices, and alternative reasonable codings of the variables. Quantify uncertainty with intervals and effect sizes, not point estimates and p-values alone, and correct for multiple comparisons when searching. When the conclusion depends on a fragile choice, report the range of defensible answers rather than the most favorable one.

Seek contrary evidence deliberately: run the control or negative case, check subgroup consistency, and test the assumptions instead of presuming them. An analysis selected because it reached significance is weak evidence; tuning preprocessing until the result appears and reporting only the final pipeline hides the garden of forking paths; intervals computed after data-dependent model selection understate real uncertainty; correlation in observational data is not a causal effect. Make the work reproducible: record the code, package versions, seeds, and data identifiers behind every number, and rerun the pipeline end-to-end from the raw inputs before reporting.

Report the claim, supporting evidence, uncertainty, sensitivity results, and contrary evidence found, keeping facts, inferences, and unknowns distinct; state plainly what the analysis does not establish. Deliver the analysis package and results memo the request expects. Use the [build workflow](../solforge-build/SKILL.md) when the analysis requires implementing or repairing the code, pipeline, or artifacts it depends on.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
