---
name: simulate-dayq-authoritative-weather
description: Implement DayQ’s authoritative weather simulation, local samples, persistence, and presentation adapters.
---

# DayQ Authoritative Weather

Build weather as causal world state. Never replace it with presets, particles, a global storm scalar, or consumer-owned weather values.

Read [FULL_CONTRACT.md](references/FULL_CONTRACT.md) completely before changing weather behavior. Read [INTEGRATION.md](references/INTEGRATION.md) before connecting a consumer or persistence path.

## Workflow

1. Inspect existing environment, survival, clothing, fire, structures, traversal, ballistics, audio/AI hearing, power, manufacturing, communications, water/ecology, vehicle, drone, authority, replication, and persistence owners.
2. Preserve one environment owner for atmosphere, fronts, regional cells, local samples, accumulation, simulation time, and forecast products. Extend a compatible owner instead of creating another.
3. Define versioned cells, fronts, samples, accumulations, forecasts, seeds, revisions, timestamps, uncertainty, and bounded catch-up through project schemas/data.
4. Implement the smallest complete causal slice: move one front, produce terrain-localized samples, feed at least one existing consumer through an adapter, and persist through the project journal.
5. Add consumers only through explicit sampled-state interfaces. Each consumer retains authority over its consequence and must record which environment sample caused it.
6. Keep World Partition, Niagara, sky/fog/materials, Sound Attenuation, and MetaSounds in streaming or presentation roles. They never own gameplay truth.
7. Compile in Unreal 5.8, run automation, run PIE, exercise the observable route, capture logs/images/video/state, repair failures, and rerun regression tests.
8. Expand through the mandatory technical spikes: moving fronts; terrain localization; rain/mud/drying; snow/ice/obstruction; thermal coupling; vector-wind consumers; cross-system coherence; uncertain forecasts; deterministic unload/restart/catch-up; two clients; and representative density/performance.
9. Update the no-skip ledger with exact evidence. Only `passed` evidence closes a gate.

## Ownership rules

- Environment owns weather truth, not outcomes in other systems.
- Existing persistence owns storage, journaling, revisions, migrations, corruption quarantine, rollback, and crash recovery.
- Clients interpolate presentation and may never author temperature, wind, precipitation, accumulation, forecast correctness, or damage-causing exposure.
- Numerical cell sizes, cadences, coefficients, thresholds, and optimization strategies remain evidence-gated variables.
- Do not touch or merge the wave-surfing project.

## Completion contract

Do not claim completion from clouds, precipitation VFX, materials, compilation, or an empty-map benchmark. Completion requires one moving authoritative front that crosses terrain, persists and catches up deterministically, feeds all required consumers coherently, remains explainable to players, survives multiplayer/restart/migration/fault tests, and meets representative performance budgets.

Report inspected owners, retained boundaries, state/data contracts, C++/Blueprint/data/level changes, consumer adapters, tests and evidence, performance results, failures/repairs, and every remaining gate.
