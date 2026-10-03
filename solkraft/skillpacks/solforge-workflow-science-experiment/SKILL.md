---
name: solforge-workflow-science-experiment
description: Specify methods, controls, measurements, power assumptions, risks, and verification before execution.
---

# Design a scientific experiment

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the hypothesis or research question in falsifiable form, the primary outcome and endpoint, the acceptance criteria, and the real constraints: available instruments and their precision, samples or subjects, budget and time, safety and ethics limits. If the hypothesis lacks a stated prediction and falsifier, resolve that before designing around it; do not retrofit a hypothesis to data already observed.

Choose the design that isolates the claimed effect: comparison structure (parallel groups, within-subject, factorial), randomization and allocation concealment where applicable, and the controls that rule out the leading confounders — negative and positive controls, blinding of who measures, matched conditions. Specify the measurement plan concretely: instrument and calibration, units, sampling frequency, handling of missing or out-of-range values. State the power assumptions explicitly — expected effect size, variance estimate and its source, alpha, target power — and derive the sample size; a sample size justified only by convention or a pilot's observed effect is weak evidence. Pre-register the analysis: primary test, covariates, stopping rule, and what counts as confirmation versus refutation.

Assess risks to validity and to the work itself: confounds the design cannot rule out, instrument drift, selection effects, and safety or ethics constraints on execution. Distinguish the confirmatory analysis from exploratory follow-up; unplanned subgroup claims and data-dependent stopping without correction are not confirmation. Where feasible, validate the protocol with a dry run or pilot on the measurement path only, and record any deviations from the written protocol rather than silently revising it.

Return the experimental protocol and methods plan with power assumptions, risks, and verification steps, noting unresolved limits. Use [hypothesis derivation](../solforge-workflow-science-hypothesis/SKILL.md) when the prediction or its falsifiers are not yet established.
