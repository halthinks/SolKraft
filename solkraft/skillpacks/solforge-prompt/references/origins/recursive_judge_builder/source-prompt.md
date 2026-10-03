# Recursive Judge-and-Builder

Version: 1.1.0
Status: candidate

## Operating idea

Define the evaluation system, build, judge, reconstruct, and repeat.

## Applicability gate

1. Use this origin only when quality depends on evaluating materially different candidates against a knowable standard; do not use it for a fixed mechanical answer or unbounded ideation.
2. Require a fixed evaluation constitution plus inspectable candidate evidence, or verified authority and inputs to produce candidate evidence, before assigning scores or verdicts.
3. If the rubric, candidate, or material evidence is missing, return a judge design and deferred evidence request; never invent observations, scores, test results, or candidate capability.
4. Bound the search to the baseline plus at most two materially distinct candidate branches, one adversarial evidence review, and one final adjudication unless the user explicitly authorizes a different finite bound.

## Observable output contract

1. A fixed evaluation constitution with hard gates, weighted criteria where justified, evidence requirements, and rejection conditions.
2. A bounded candidate registry containing the baseline and no more than two materially distinct alternatives by default.
3. A candidate-to-evidence ledger that distinguishes observed, supplied, proposed, missing, and contradicted evidence.
4. Per-candidate judgments with criterion results, uncertainty, disqualifiers, and strongest counterargument.
5. A bounded recursion trace covering one adversarial review, any material reconstruction, and final adjudication.
6. A supported verdict or an explicit deferred verdict with the minimum missing evidence.

## Sol execution contract

1. Apply the applicability gate first. Freeze a constitution containing non-negotiable validity, quality criteria, evidence requirements, adversarial tests, rejection conditions, and the finite candidate and review bounds before building or judging.
2. Register the supplied baseline and create at most two materially distinct alternatives only when authority and inputs permit; keep candidate generation separate from evidence evaluation and do not let a builder self-certify observations.
3. Judge every candidate against the same constitution using only supplied or actually observed evidence; record missing and contradicted evidence and defer any score or verdict that the evidence cannot support.
4. Use one adversarial evidence branch to test boundary cases, scale limits, implementation failures, and strongest objections; reconstruct only foundations whose change can materially improve a failed criterion.
5. Perform one final adjudication against the unchanged constitution, preserve disagreement and uncertainty, and stop at the declared bound even if further iteration could be imagined.
6. Return the constitution, candidate registry, evidence ledger, bounded recursion trace, material changes, and supported or deferred verdict; never lower criteria, fabricate evidence, or claim convergence from self-evaluation alone.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
