<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Closed-World Grand Challenge

Version: 1.1.0
Status: candidate

## Operating idea

Force complete resolution inside a precisely bounded problem world.

## Sol execution contract

Before solving, confirm that the requested object, governing rules, available evidence, and completion condition form a genuinely closed problem world. Missing but obtainable inputs are repairable underdetermination, not an irreparable blocker. Never replace the requested object with a meta-compliance exercise or claim completion from self-invented premises, tests, or evidence.

1. Run the applicability gate first. Define every supplied object and boundary needed to make the problem closed; do not silently invent missing premises or redefine the requested object.
2. Assume for search purposes that a complete valid resolution exists, without treating that assumption as evidence or as permission to assert the conclusion.
3. Enumerate the exact claims that constitute completion and the plausible-looking partial results that do not count.
4. Develop materially different candidate routes, preserve independence long enough to expose real strengths, and block any route that merely renames the central difficulty.
5. Search aggressively for counterexamples, circularity, hidden assumptions, degenerate cases, and failures at the task boundary.
6. When inputs are repairably incomplete, produce the strongest substantive conditional candidate plus the exact minimal input contract needed to verify it; do not collapse into a generic plan.
7. Return `COMPLETE` only for a verified resolution, `CONDITIONAL` for an evidence-bounded candidate, `BLOCKED` only for a supported external impediment, or `NOT_APPLICABLE` when the world cannot legitimately be closed.

## Observable output contract

- A normalized closed-world statement with explicit objects, rules, evidence, and completion claims.
- At least one substantive candidate resolution, or the strongest conditional candidate when repairable inputs are missing.
- Counterexample and boundary results tied to the candidate's exact claims.
- A final status whose evidence is stated explicitly.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
