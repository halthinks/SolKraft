# DayQ weather integration boundary

The environment owner supplies immutable or queryable versioned samples and events. It never directly applies consumer consequences.

| Input or outcome | Authoritative owner |
|---|---|
| Atmosphere, fronts, cells, local samples, accumulation, forecasts | Environment |
| Core temperature, exposure, disease, injury | Survival and health |
| Garment wetness, insulation, damage, drying | Clothing |
| Ignition, combustion, smoke, spread | Fire and combustion |
| Ingress, drainage, roof load, structure damage | Building and structures |
| Mud, snow, ice, climbing and hauling effects | Movement and traversal |
| Projectile wind response | Ballistics |
| Acoustic propagation and AI evidence | Proximity audio and AI hearing |
| Generation, storage efficiency and loads | Power and energy |
| Machine cooling, faults and job delay | Manufacturing and crafting |
| Link quality and sensor uncertainty | Communications and sensors |
| Runoff, soil, wildlife, crops and water consequences | Water, agriculture and ecology |
| Sky, fog, particles, materials and weather audio | Client presentation |

Use the existing persistence subsystem for cell/front/accumulation/forecast entities. Require stable IDs, expected revisions, idempotency keys, atomic journal writes, schema versions, quarantine, tombstones, migrations, rollback, last-simulated time, and bounded deterministic catch-up. Never create a weather-specific save file or trust a client sample.

The first bounded implementation slice is `WX-001`: one seeded front crossing four Blackglass terrain contexts, deterministic local samples, a survival exposure adapter, one existing-journal persistence entity, restart digest equality, and focused Unreal automation. PIE presentation, two-client replication, accumulation, broader consumers, World Partition catch-up, and representative performance remain separate gates until evidenced.
