---
name: solforge-workflow-business-strategy
description: Translate evidence into options, tradeoffs, sequencing, metrics, risks, and a decision-ready recommendation.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Develop a business strategy

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the actual decision being requested, who decides, the time horizon, and the constraints that bound it: budget, capacity, commitments already made, and what the requester has ruled in or out. Inventory the supplied evidence and judge its provenance and recency before building on it; separate verified facts from assumptions and identify which assumptions are load-bearing. If the decision framing is ambiguous, resolve it with the requester rather than guessing at scope.

Generate a real option set, including the do-nothing baseline, and fix the evaluation criteria — weighted against the stated objectives — before scoring anything. Work the economics concretely: cost, benefit, and cash or unit impact where relevant, plus sensitivity of the option ranking to the load-bearing assumptions; a ranking that flips under plausible assumption changes must say so. Sequence the recommended path by dependency and reversibility: front-load cheap, reversible steps that buy information, stage irreversible commitments behind decision points, and name the trigger conditions that would change the path. Attach metrics with baselines and targets to each phase, and build a risk register specific to this decision with likelihood, impact, and mitigation — a risk list any strategy in the domain could carry is not evidence of analysis.

Verify every material claim against its source. A recommendation that merely restates the requester's preferred option is advocacy, not strategy; a projection without a stated assumption chain is decoration. Stress-test the recommendation against the intake constraints and against the objections a skeptical decision-maker would raise first. Keep options, tradeoffs, and uncertainties distinct from the recommendation itself so the decision stays the requester's.

Report the recommendation, the options considered and why each was set aside, the assumption chain behind the economics, the sequencing with its triggers and metrics, the top risks, and the open unknowns that would change the answer. Use [structured comparison](../solforge-run-comparison/SKILL.md) when the options need symmetric evaluation against shared criteria and sources.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
