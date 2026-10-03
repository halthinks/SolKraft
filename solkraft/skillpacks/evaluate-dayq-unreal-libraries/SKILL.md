---
name: evaluate-dayq-unreal-libraries
description: Evaluate Unreal libraries for DayQ adoption using source, licensing, compatibility, and runtime evidence.
---

# Evaluate DayQ Unreal Libraries

Own the evaluation. Return tested dispositions and evidence, not instructions for another task to repeat the work.

Read [evaluation-contract.md](references/evaluation-contract.md), [dayq-adapter-contract.md](references/dayq-adapter-contract.md), and [candidate-baseline.md](references/candidate-baseline.md) before testing.

## Workflow

1. Inspect the target Unreal version, build tools, candidate packages, entitlements, licenses, AI-use terms, source access, platforms, and current DayQ ownership boundaries.
2. Work in an isolated bakeoff project. Never add an unaccepted candidate to production DayQ.
3. Run `scripts/bakeoff.py preflight` to create a machine-readable environment report.
4. Stop before opening candidate source when its license or AI-use terms prohibit agent inspection. Record `blocked-permission`; do not infer permission from possession.
5. Create one DayQ-owned adapter interface. Candidate types must not enter persistent schemas, inventory identity, damage, weapon instances, or gameplay-facing data.
6. Establish the internal solver as the control. Run identical fixtures for every accessible candidate.
7. Use `scripts/run_unreal_bakeoff.ps1` to compile editor and dedicated-server targets in the exact target engine version and run the common automation suite. Then run PIE, packaged/dedicated-server, latency/loss, authority, persistence, crash-recovery, security, performance, and upgrade/removal tests.
8. Capture commands, versions, hashes, logs, test data, profiles, screenshots/video when applicable, and failures. Missing evidence is a failed gate, not a favorable score.
9. Run `scripts/bakeoff.py evaluate` to validate evidence and render dispositions.
10. Choose exactly one result per candidate: `adopt`, `wrap`, `fork`, `reject`, `blocked-needs-acquisition`, `blocked-permission`, or `blocked-environment`.
11. Hand the signed evidence report and adapter recommendation to the primary DayQ task. That task imports only the selected adapter and accepted dependency.

## Required comparisons

For firearm ballistics always compare:

- DayQ internal control;
- BulletForge, only after written AI-use permission permits agent inspection;
- EasyBallistics when lawfully acquired;
- Terminal Ballistics when lawfully acquired, using DayQ-owned networking;
- any stronger current candidate discovered from primary/vendor evidence.

Measure external trajectory and time of flight, wind/environment response, energy, penetration, ricochet, material continuation, projectile throughput, allocations, server CPU, client CPU, memory, bandwidth, RPC count, prediction/correction, rewind abuse, muzzle validity, duplicated requests, 30/60/120 Hz behavior, 0/50/100/200 ms RTT, jitter, loss, concurrent shooters, persistence, restart, migration, packaging, and removal.

Do not claim DayZ or Reforger parity. Translate observable qualities into original measurable DayQ targets.

## Authority

The server owns fire authorization, ammunition/chamber mutation, muzzle validation, projectile truth, hit validation, damage/wound application, persistence, and anti-duplication. Client prediction may improve presentation but cannot create authoritative shots or hits.

## Completion

Complete only when every accessible candidate has live evidence and every inaccessible candidate has an exact blocker with the acquisition or permission needed. Distinguish `not tested` from `failed`. Never call a vendor listing a test result.

Report exact paths, hashes, Unreal version, package versions, licenses, commands, tests, metrics, defects, dispositions, and the safe handoff boundary.
