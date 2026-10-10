---
name: solforge-workflow-math-counterexample
description: Stress the statement across boundary cases, constructions, computation, and known obstruction families.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Falsify a mathematical statement

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Fix the exact statement first: its quantifier structure, hypotheses, the class of objects it ranges over, and what counts as a refutation — an object satisfying every hypothesis while violating the conclusion. Note the definitional conventions in force (whether zero is natural, whether graphs are simple), since a counterexample under one convention may be excluded under another. If the statement is ambiguous, resolve the ambiguity or attack the strongest reasonable reading and say which.

Probe the places where such statements characteristically break: degenerate and boundary inputs (empty, singleton, zero, coincident points), extremal parameter values, small cases against asymptotic claims, and the weakening of each hypothesis in turn. Apply known obstruction families for the domain — nowhere-differentiable constructions against regularity claims, non-compact or infinite-dimensional examples against finite intuition, parity and integrality obstructions, and classic named counterexamples whose hypotheses the statement resembles. When hand constructions stall, search computationally: enumerate small instances, run randomized or solver-assisted search, and optimize against the conclusion on a search space large enough to be meaningful.

Verify every candidate before reporting it: recheck that it satisfies each hypothesis exactly as stated and that the conclusion genuinely fails, recomputing with exact arithmetic where floating point could manufacture the violation. A candidate that quietly violates one hypothesis is not a counterexample; a numerical violation inside rounding error is not a counterexample; a refutation of a misquoted or strengthened version refutes nothing. Equally, failing to find one is not a proof — report the space actually searched, not a verdict the search cannot support.

Report the verified counterexample with its construction and hypothesis check, or the falsification search actually performed: cases and families covered, computational bounds reached, and where the statement survived. Use [solforge-run-research](../solforge-run-research/SKILL.md) when locating prior counterexamples or the domain's known obstruction families requires a tracked literature search.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
