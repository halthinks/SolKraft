# Counterfactual World

Version: 1.1.0
Status: candidate

## Operating idea

Stress the solution across alternate worlds and extract what survives.

## Applicability gate

1. Use only for a materially costly, durable, or difficult-to-reverse decision that may change under uncertainty.
2. Require at least one decisive dependency with evidence-supported alternatives, bounds, or sensitivity ranges.
3. Route away when the decision is cheap, reversible, or demonstrably insensitive to plausible changes.

## Sol execution contract

1. Bind the common objective, constraints, decision, and acceptance basis, then identify only dependencies whose variation could change the preferred decision.
2. Select two to four coherent counterfactual worlds, each changing a decisive assumption supported by supplied evidence, observed alternatives, or credible bounds; do not generate a generic scenario catalog.
3. If credible world facts or bounds are insufficient, replace narrative worlds with sensitivity analysis over explicit variables and ranges, and label the result as sensitivity rather than scenario evidence.
4. Solve the same decision within each selected world or range, preserving common objective constraints, and compare outcomes, regret, option value, and adaptation cost.
5. Identify invariants, thresholds where the preferred solution changes, fragile dependencies, reversible decisions, lock-in, invalidation signals, and migration triggers.
6. Synthesize a robust core with explicit adaptations and state the smallest evidence-supported change that destroys its value, including survival, migration, warning, or honest scope.

## Observable output contract

1. Decisive-assumption and dependency ledger with evidence or ranges.
2. Two to four world cards, or an explicitly labeled sensitivity grid.
3. Cross-world decision matrix with thresholds, regret, adaptation cost, and invalidation signals.
4. Robust core with migration triggers and the smallest value-destroying change.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
