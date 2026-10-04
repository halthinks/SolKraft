<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Representation Shift

Version: 1.1.0
Status: candidate

## Operating idea

Search for a formulation where the hard part becomes natural or disappears.

## Applicability gate

1. Use this origin only when the current representation may be the material source of difficulty and the task has an inspectable baseline, objective, and success criteria.
2. Treat the identity baseline as an eligible candidate that may remain best; a shift is not required merely because this origin was selected.
3. Define the invariants, information that must be preserved, mapping direction, and equivalence evidence before preferring an alternate representation.
4. If equivalence or mapped-back validation cannot be established from supplied or observed evidence, return conditional alternatives and the missing proof obligations; never invent invariants or proof.

## Observable output contract

1. An explicit identity baseline with current performance, failure, or complexity evidence.
2. A material invariant and preservation ledger defining what every eligible representation must retain.
3. A bounded set of alternate representations with forward and reverse mappings, information loss, and newly natural operations.
4. A comparison matrix that includes the identity baseline and uses the same material success criteria for every candidate.
5. Identity, equivalence, and mapped-back proof statuses labeled evidenced, conditional, unverified, contradicted, or blocked.
6. A selected representation or no-shift verdict, with mapped-back validation and the strongest rejected alternative.

## Sol execution contract

1. Apply the applicability gate first. Record the current representation as the identity baseline, its observed difficulty, the task objective, and material success criteria; retain it as a candidate throughout evaluation.
2. Identify only evidence-supported hidden structure and define the invariants and information that every eligible representation must preserve before proposing a shift.
3. Construct a bounded set of materially different representations—structural, geometric, algebraic, state-transition, optimization, probabilistic, dual, compressed, expanded, or adjacent-field only where relevant.
4. For each candidate, including the identity baseline, provide the forward and reverse mapping, information loss, newly visible invariants, operations made natural, assumptions introduced, and proof status.
5. Select only when observed or derivable evidence shows a material improvement under the same criteria; prefer the identity baseline when alternatives add novelty without proven reduction, and combine representations only through precise interfaces.
6. Derive and map back the result, validate preservation and equivalence, attack introduced assumptions, and return a conditional or no-shift verdict when proof is unavailable; never claim a representation shift succeeded from plausibility alone.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
