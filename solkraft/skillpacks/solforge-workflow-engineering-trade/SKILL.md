---
name: solforge-workflow-engineering-trade
description: Compare design alternatives with common constraints, models, evidence, sensitivity, and risks.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Run a design trade study

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the alternatives in scope, the decision the study feeds, and the shared constraints and interfaces every candidate must satisfy before scoring anything. Derive criteria from the stated requirements and acceptance criteria, with units and a source for each; separate hard constraints that eliminate candidates from preferences that merely rank them. Eliminate infeasible alternatives first so they cannot distort the weights later.

Score each alternative against the same criteria from the same kind of evidence — measured data, a stated model, a cited vendor figure, or a flagged estimate — and record which basis supports each score. Normalize only within a criterion; never collapse unlike units onto one scale without a stated conversion. Weighted sums are decision aids, not measurements: a ranking difference smaller than the uncertainty of the underlying scores is a tie, and precision beyond the evidence is theater.

Run sensitivity on the weights and on the load-bearing assumptions. A recommendation that flips when one weight moves within its plausible range is not stable; report the flip point instead of hiding it. Record per-alternative risks and the evidence that would change the ranking. Do not tune weights after seeing the outcome, and do not drop a disfavored alternative's strongest criterion from the record.

Return the trade study and decision record: criteria with sources, scores with their evidence basis, sensitivity results, the recommended alternative with its margin, and open risks. Use [run comparison](../solforge-run-comparison/SKILL.md) when the comparison extends to repositories, products, or evidence sets beyond design candidates.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
