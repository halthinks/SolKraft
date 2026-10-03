---
name: solforge-workflow-business-model
description: Build explicit assumptions, scenarios, sensitivities, and decision thresholds with auditable calculations.
---

# Model business economics

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the decision the model informs, the alternatives under comparison, the time horizon, and the acceptance criteria before building anything. Separate supplied inputs from assumptions; record every assumption with its basis — observed data, a cited source, an analogous business, or an explicit guess — and keep facts, inferences, and unknowns distinct. Reuse valid prior work rather than rebuilding equivalent stages.

Structure the model around drivers, not line items copied from a template: volume, price, conversion, retention, acquisition cost, delivery cost, and cash timing, composed into unit economics and then the period view. Build scenarios by varying specific drivers with stated reasons — a downside case that moves every input by an arbitrary percentage is not a scenario, it is decoration. Run sensitivity analysis to rank which assumptions actually swing the outcome, and derive decision thresholds from the structure: break-even volume, minimum runway, price floor, the assumption value at which the decision flips.

Verify the calculations are auditable: every output traceable to an input and a formula, units and time periods consistent, arithmetic independently re-derived on a sample of cells rather than trusted from the tool. A precise-looking projection resting on an unexamined assumption is weak evidence; label the confidence of each material input. Do not present a projection as an observed fact, and do not let a single-point estimate stand where a range is honest.

Report the assumption table with basis, scenario and sensitivity results ranked by impact, the thresholds that govern the decision, and unresolved limits. Use [research execution](../solforge-run-research/SKILL.md) when a material assumption needs sourced evidence beyond what was supplied.
