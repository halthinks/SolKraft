# Constraint Reversal

Version: 1.1.0
Status: candidate

## Operating idea

Audit assumed limits and convert the right limitation into leverage.

## Applicability gate

1. Use only when one or more stated or observable constraints materially limit the solution space.
2. Treat a constraint as false-fixed or reversible only when evidence supports both its controlling effect and its mutability.
3. Exclude safety, legal, ethical, authority, and objective-defining constraints from reversal candidates.

## Sol execution contract

1. Inventory explicit and implicit constraints, cite their source or observation, and classify each as necessary, objective-bound, conventional, inherited, convenient, unsupported, reversible, or potentially useful.
2. For every proposed false-fixed constraint, show evidence that it materially controls the outcome, can be changed, and is not a safety, legal, ethical, authority, or objective-defining boundary.
3. Run a no-constraint discovery test before ideation; if no material reversible false-fixed constraint is evidenced, return `NO_REVERSIBLE_CONSTRAINT_FOUND` with the tested boundary and strongest conventional solution rather than forcing a reversal.
4. For supported candidates, compare preserve, remove, reverse, combine, exploit, and architectural-elimination mechanisms, translating speculative ideas back into explicit feasible conditions.
5. Test whether benefits survive reality, where costs and risks move, which dependencies are introduced, and whether necessary constraints can be restored without destroying the mechanism.
6. Return the evidenced false-fixed constraint, selected reversal, complete solution, feasibility evidence, introduced risks, restoration conditions, and strongest conventional alternative.

## Observable output contract

1. Constraint ledger with provenance, evidence, materiality, and classification.
2. No-constraint discovery test with an explicit result.
3. Reversal candidate table covering mechanism, feasibility, transferred cost, risk, and restoration.
4. Selected reversal plus conventional baseline, or a `NO_REVERSIBLE_CONSTRAINT_FOUND` packet.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
