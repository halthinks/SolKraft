---
name: validate-dayq-game
description: Validate DayQ milestone or release acceptance through gameplay, regressions, performance, and playtest evidence.
---

# DayQ Game Validation

Close milestone and release requirements with evidence. Never convert an unrun test into a pass. For routine edits, return to `$run-dayq-autopilot` and use compile plus a focused smoke route.

Read [validation-contract.md](references/validation-contract.md) and the acceptance criteria for the target system.

## Workflow

1. Identify the exact ledger item and required evidence type.
2. Freeze build, configuration, dataset, route, hardware/network profile, and threshold.
3. Run the smallest test that can falsify the claim.
4. Capture raw logs, metrics, screenshots/video, state snapshots, crashes, and tester observations.
5. Compare against the threshold; mark pass or fail without narrative softening.
6. File the highest-impact failure, repair it, and rerun only the affected focused regression suites.
7. Preserve failed evidence and link the final result.
8. Audit adjacent ledger items for invalidated decisions.

## Human playtesting

Prepare protocols and telemetry for all required cohorts. Agent simulation may test instructions and defects but cannot replace real human evidence for confusion, boredom, cooperation, pride, frustration, or loss tolerance.

## Output

Produce a validation record containing provenance, method, raw evidence links, result, defects, remediation, regressions, and ledger status.
