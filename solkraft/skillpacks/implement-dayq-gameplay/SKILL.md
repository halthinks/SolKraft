---
name: implement-dayq-gameplay
description: Implement approved DayQ gameplay systems and their runtime interfaces.
---

# DayQ Gameplay Implementation

Build the smallest complete playable change, launch it, collect evidence, and repair the highest-impact failure.

Read [gameplay-proof-contract.md](references/gameplay-proof-contract.md), the relevant system sheets, and the canon when content is involved.

## Loop

1. Translate the request into one observable player behavior and a focused smoke route.
2. Inspect only the runtime owners, inputs, authority, save state, and tests touched by the change.
3. Implement one vertical mechanic across state, simulation, feedback, networking, persistence, and failure recovery.
4. Add debug visualization or telemetry only when it shortens implementation or diagnosis.
5. Compile and launch; execute the shortest representative gameplay route.
6. Capture the command and result; add one representative log or screenshot only at a milestone.
7. Repair a crash, build failure, data-loss risk, authority exploit, or current-route blocker.
8. Defer other defects and continue. Run focused adjacent regressions at subsystem milestones.

## Rules

- Keep the server authoritative for damage, inventory, movement-critical state, and item transfer in multiplayer builds.
- Make wounds, contamination, equipment state, and treatment legible through more than UI meters.
- Combine or remove survival pressures that produce maintenance without decisions.
- Tune against tactical readability, not only time-to-kill averages.
- Preserve degraded and interrupted states across save/load and reconnect.

## Output

Deliver source changes and a playable route. Report what changed, what is playable, deferred defects, and the next milestone. Add tuning datasets, evidence packages, and ledger links only when their milestone requires them.
