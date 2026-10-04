---
name: solforge-workflow-business-model
description: Build explicit assumptions, scenarios, sensitivities, and decision thresholds with auditable calculations.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Model business economics

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the decision the model informs, the alternatives under comparison, the time horizon, and the acceptance criteria before building anything. Separate supplied inputs from assumptions; record every assumption with its basis — observed data, a cited source, an analogous business, or an explicit guess — and keep facts, inferences, and unknowns distinct. Reuse valid prior work rather than rebuilding equivalent stages.

Structure the model around drivers, not line items copied from a template: volume, price, conversion, retention, acquisition cost, delivery cost, and cash timing, composed into unit economics and then the period view. Build scenarios by varying specific drivers with stated reasons — a downside case that moves every input by an arbitrary percentage is not a scenario, it is decoration. Run sensitivity analysis to rank which assumptions actually swing the outcome, and derive decision thresholds from the structure: break-even volume, minimum runway, price floor, the assumption value at which the decision flips.

Verify the calculations are auditable: every output traceable to an input and a formula, units and time periods consistent, arithmetic independently re-derived on a sample of cells rather than trusted from the tool. A precise-looking projection resting on an unexamined assumption is weak evidence; label the confidence of each material input. Do not present a projection as an observed fact, and do not let a single-point estimate stand where a range is honest.

Report the assumption table with basis, scenario and sensitivity results ranked by impact, the thresholds that govern the decision, and unresolved limits. Use [research execution](../solforge-run-research/SKILL.md) when a material assumption needs sourced evidence beyond what was supplied.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
