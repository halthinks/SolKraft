# Evaluation contract

## Gates

Every candidate must have evidence for:

1. lawful acquisition and archived license;
2. explicit AI-assisted inspection/modification permission when agents are used;
3. complete package hash and source-access classification;
4. exact Unreal 5.8 editor build;
5. exact Unreal 5.8 dedicated-server build;
6. plugin load and smoke test;
7. deterministic fixture corpus;
8. server authority and adversarial RPC tests;
9. latency, jitter, loss, correction, and rewind tests;
10. trajectory, impact, penetration, ricochet, and continuation accuracy;
11. projectile concurrency and sustained-fire performance;
12. DayQ inventory, chamber, magazine, damage, wound, audio, and material adapters;
13. persistence, restart, journal replay, schema migration, and rollback safety;
14. target-platform packaging;
15. dependency, telemetry, security, and supply-chain audit;
16. maintainability, documentation, update history, and support evidence;
17. removal/upgrade proof with no vendor types in authoritative saved data;
18. captured logs, metrics, commands, build IDs, and defect reruns.

## Standard fixtures

- Distances: 10 m, 100 m, 300 m, and an approved long-range case.
- Environment: no wind control plus crosswind, density, temperature, and humidity cases appropriate to the accepted fidelity tier.
- Materials: glass, wood, soil, masonry, sheet metal, armor, vehicle structure, robotic structure, and body layers.
- Impacts: normal, oblique, multi-layer, ricochet, penetration, stop, and retained-projectile cases.
- Fire: semi-auto, burst, and sustained automatic fire from one and many shooters.
- Network: 0/50/100/200 ms RTT; bounded jitter/loss; moving targets; cover transitions; invalid muzzle; replayed/duplicated requests; high-ping abuse.
- Lifecycle: save/load, disconnect/reconnect, server restart, journal replay, migration, candidate removal, and Unreal minor-version rebuild.

Use versioned JSON fixtures and tolerances. Do not tune separate fixtures to favor candidates.

## Dispositions

- `adopt`: candidate passes all gates and can be used substantially as designed behind DayQ interfaces.
- `wrap`: candidate passes but must remain isolated behind an adapter.
- `fork`: source and license permit modification, the fork passes, and DayQ accepts maintenance ownership.
- `reject`: tested evidence fails one or more non-negotiable gates or the value does not justify risk.
- `blocked-needs-acquisition`: package or entitlement is absent.
- `blocked-permission`: license, AI-use, commercial, source, or platform permission is unresolved.
- `blocked-environment`: required engine, compiler, platform SDK, account-backed service, or hardware is unavailable.

Never average away a failed authority, licensing, persistence, security, or removal gate.
