# Validation contract

## Release-candidate cohorts

Hardcore survival players, base builders, PvP players, cooperative PvE players, clan leaders, survival newcomers, and logistics/crafting players.

Observe confusion, boredom, exploits, ignored systems, natural cooperation, base-defense value, gear-loss tolerance, and whether clan progression creates pride or chores.

## Technical spikes

Run a spike when its subsystem enters the active playable route and presents unresolved technical risk—not as blanket preflight. Release coverage includes persistent world, build-piece scale, replication/destruction, offline persistence, networked vehicles, distant AI, defense grids, drones, bunker interiors, world streaming, authoritative inventory, anti-duplication, crash recovery, migrations, and anti-cheat.

## Invocation tiers

- Routine implementation: do not invoke this full contract; compile and smoke-play through `$run-dayq-autopilot`.
- Subsystem milestone: validate only the changed mechanic and its direct neighbors.
- Integration milestone: add affected authority, persistence, fault, and performance paths.
- Release candidate: run the complete cohort, spike, regression, performance, and evidence program.

## Validation record fields

ID, requirement, build, configuration, environment, dataset, method, threshold, raw evidence, result, defects, severity, remediation, regression impact, reviewer, timestamp, and ledger link.

Statuses are `not-started`, `specified`, `implemented`, `testing`, `passed`, `failed`, `deferred`, `blocked`, and `reopened`. Only `passed` closes a milestone or release requirement. `Deferred` is valid for noncritical work outside the active gate.
