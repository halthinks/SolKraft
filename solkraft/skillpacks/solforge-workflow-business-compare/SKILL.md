---
name: solforge-workflow-business-compare
description: Compare named alternatives using explicit criteria, evidence parity, sensitivity, and decision implications.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Compare business alternatives

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the decision the comparison must serve, the named alternatives (including status quo or do-nothing where relevant), the evaluation criteria with their weights, and the planning horizon before collecting evidence. Derive criteria from the decision maker's constraints — budget, time to value, switching cost, regulatory exposure, strategic fit — not from vendor feature lists. When criteria arrive from a stakeholder with a preferred outcome, surface that before scoring; a weighting reverse-engineered to crown a preselected option is not a comparison.

Gather evidence to parity: each alternative gets the same depth of sourcing, the same cost basis, and the same vintage of data. Price on total cost of ownership — licensing, implementation, migration, training, and exit cost — not list price. Normalize qualitative claims to observable support: reference customers, contract terms, published roadmaps, and audited financials outweigh marketing copy and analyst placements. Record what could not be verified for each option; an evidence gap on one alternative is a finding to report, not a silent tiebreaker against it.

Score each option against the criteria in a visible scorecard, then stress the result: vary the two or three most load-bearing weights and assumptions until the ranking flips, and record those break-even points. A recommendation that survives only a narrow band of assumptions is fragile and must say so. Separate decisive differentiators from noise, and name the conditions under which the second-ranked option would win.

Report the scorecard with per-criterion evidence, the sensitivity results, explicit decision implications, and unresolved gaps. Use [run comparison](../solforge-run-comparison/SKILL.md) when the underlying comparison procedure is missing or the alternatives span evidence sets beyond business options.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
