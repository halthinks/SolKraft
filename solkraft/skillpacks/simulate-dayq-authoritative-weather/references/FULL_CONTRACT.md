# DayQ Authoritative Weather World Simulation — Complete Handoff Prompt

Status: **user-directed and decided; implementation evidence pending**
Owner: user, sole DayQ creative authority
Scope: DayQ only
Runtime target: Unreal Engine 5.8
Wave-surfing project: excluded and untouched

## Governing decision

DayQ weather is a **world simulation**, not a particle-effects manager.

One server-authoritative environmental-state system owns atmospheric conditions, fronts, terrain modification, precipitation, accumulation, wind and forecast truth. Survival, clothing, fire, structures, traversal, ballistics, sound, AI, wildlife, agriculture, water, power, machines, communications, sensors, vehicles, drones, bases and rendering consume that state through defined interfaces. None may invent a separate scalar for “how bad the storm is.”

The system has eight connected layers:

1. atmospheric model;
2. moving weather fronts;
3. terrain and built-environment effects;
4. precipitation and persistent accumulation;
5. thermal exchange;
6. wind as a physical system;
7. weather-driven world consequences;
8. uncertain forecasting and player information.

It operates at three resolutions:

- **near player:** detailed local sampling and physical/presentation interactions;
- **regional:** authoritative weather cells affecting settlements, AI, production and travel;
- **distant world:** low-frequency climate/front evolution and bounded offline catch-up.

## Player purpose

Weather must create readable preparation, route, timing, shelter, clothing, loadout, construction, power, logistics and combat decisions.

Players should be able to:

- see a front approaching and decide whether to leave, reroute, fortify or exploit it;
- understand why a ridge, valley, forest, street canyon or building interior feels different;
- prepare clothing, fuel, tools, vehicles, ropes, batteries, radios and shelter for expected conditions;
- exploit wind, fog, snow, rain, heat or cold tactically;
- suffer consequences that trace back to observable exposure rather than arbitrary debuffs;
- improve forecasting through instruments, radios, sensors, agents and settlement infrastructure without ever gaining perfect knowledge.

Weather reinforces DayQ's core loop:

`forecast -> prepare -> travel -> read changing conditions -> exploit or endure -> extract -> repair/dry/treat/rebuild -> improve weather intelligence and resilience`

## Explicit non-goals

Do not create:

- globally randomized weather presets that switch without spatial cause;
- Niagara, fog, sky, audio or material systems that own gameplay weather;
- separate temperature, wind, wetness or storm truth inside every consumer;
- a single global storm-severity percentage;
- per-particle network replication;
- full computational fluid dynamics across the 64 km² region;
- uniform snow depth, wind, temperature or precipitation across all terrain;
- constant survival-meter chores with no route, gear or shelter decision;
- deterministic perfect forecasts available from the UI;
- offline simulation capable of erasing a base through unstable or unbounded numerical catch-up;
- arbitrary weather damage that ignores materials, exposure, condition and construction;
- exact proprietary weather behavior copied from another game.

## Authoritative ownership

Create or extend one project-owned environmental subsystem. A provisional Unreal name is `UDayQEnvironmentSubsystem`; preserve a compatible existing owner if one already exists.

The environment owner supplies immutable/queryable samples and versioned events. Consumers own their consequences:

| State or consequence | Authoritative owner |
|---|---|
| Atmosphere, fronts, regional cells, local environmental sample | Environment |
| Character heat, exposure, disease and injury | Survival/health |
| Garment wetness, insulation, damage and drying | Clothing |
| Ignition, combustion, smoke and fire spread | Fire/combustion |
| Building ingress, drainage, roof load, damage and repair | Building/structures |
| Mud/snow/ice traversal and climbing consequences | Movement/traversal |
| Projectile wind response | Ballistics |
| Sound propagation and AI acoustic evidence | Proximity audio/AI hearing |
| Battery/generator/renewable efficiency and load | Power/energy |
| Machine faults, cooling and production delay | Manufacturing/crafting |
| Radio/sensor range and signal uncertainty | Communications/sensors |
| Crop, soil, wildlife and water consequences | Agriculture/ecology/water |
| Particles, clouds, sky, fog, wet materials and audio | Client presentation only |

Consumers may cache the last environment sample for bounded processing. They may not alter, reinterpret or persist a competing atmosphere/front state.

## Layer 1 — atmospheric model

Represent the world as versioned regional weather cells over climate regions and elevation bands. Each cell contains at minimum:

```yaml
cell_id: stable_guid
revision: integer
simulation_time_utc: timestamp
center_world_m: [x, y]
horizontal_extent_m: [x, y]
representative_elevation_m: number
air_temperature_c: number
relative_humidity_fraction: number
pressure_hpa: number
wind_velocity_mps: [east, north, vertical]
gust_velocity_mps: [east, north, vertical]
cloud_cover_fraction: number
cloud_base_m: number
precipitation_type: none|rain|snow|sleet|hail|freezing_rain|mixed
precipitation_rate_mm_per_hr: number
visibility_m: number
solar_input_fraction: number
front_refs: []
forecast_uncertainty: map
deterministic_seed: integer
```

Temperature, humidity, pressure, wind, cloud, precipitation and visibility vary by region, elevation, season and time. Exact cell size and cadence remain evidence-driven.

Use physically motivated bounded relationships rather than a full numerical weather-prediction model. Conservation-like constraints, pressure gradients, moisture availability, terrain and front state must prevent impossible discontinuities.

## Layer 2 — moving weather fronts

Fronts are persistent world entities, not timers.

```yaml
front_id: stable_guid
front_type: cold|warm|occluded|stationary|convective_line|other
revision: integer
position_and_shape: versioned_geometry
velocity_mps: [east, north]
pressure_gradient: number
temperature_delta_c: number
moisture_delta: number
wind_shift: map
instability: number
precipitation_potential: number
growth_state: developing|mature|weakening|dissipated
created_at: timestamp
```

Fronts advect across regional cells, interact with terrain and available moisture, change pressure and wind, form or intensify precipitation, and dissipate gradually. Players may observe the approach through cloud movement, pressure fall, temperature change, wind shift, animal behavior, radio reports and sensors.

The server owns front evolution. Clients receive relevant sampled state and forecast products, not unrestricted hidden future truth.

## Layer 3 — terrain and built-environment effects

The environment subsystem combines regional cell state with authoritative static/dynamic modifiers:

- elevation lapse and exposure;
- mountain lifting, rain shadow and ridge wind;
- valley cold-air/fog pooling;
- forest wind shelter, humidity retention and shade;
- urban heat retention and street-canyon wind;
- rooftop/high-rise exposure;
- large-building wind shadow and tunnel effects;
- water-body temperature/humidity moderation;
- underground thermal stability;
- doors, windows, roofs, insulation, ventilation and structural breaches;
- player-built walls, windbreaks, drainage, heaters and fires.

Use precomputed terrain descriptors plus bounded dynamic modifiers. Do not attempt per-frame fluid simulation around every object.

Local sample contract:

```yaml
sample_time: timestamp
world_position_m: [x, y, z]
source_cell_id: stable_guid
source_revision: integer
air_temperature_c: number
humidity_fraction: number
pressure_hpa: number
mean_wind_mps: vector
gust_mps: vector
precipitation_type: enum
precipitation_rate_mm_per_hr: number
visibility_m: number
solar_input_fraction: number
shelter_fraction: number
rain_exposure_fraction: number
sky_exposure_fraction: number
terrain_surface_state_ref: stable_id
confidence: number
```

## Layer 4 — precipitation and persistent accumulation

Rain, snow, sleet, hail and freezing rain create persistent world state.

Track accumulation at a resolution appropriate to gameplay surfaces and strategic cells:

- liquid water depth and drainage state;
- soil saturation and mud class;
- snow water equivalent, approximate depth and compaction;
- drifting/exposure modifier;
- surface ice and refreeze risk;
- roof or platform snow/ice load;
- doorway, road, stair, ladder, roof and equipment obstruction;
- last authoritative update and bounded offline catch-up.

Accumulation changes:

- traction, speed, stamina and fall risk;
- footstep and vehicle sound;
- visibility, concealment and tracking;
- vehicle mobility and fuel consumption;
- climbing anchors, ropes, ladders and roof access;
- carried-object stability and hauling;
- door/road/vent/drain blockage;
- buried caches, resources and construction markers;
- structural load, leakage, corrosion and collapse risk;
- water availability and contamination transport.

Snow and mud visuals are projections of this state. A material mask or Niagara effect may not create or erase authoritative accumulation.

## Layer 5 — thermal simulation

The environment publishes exposure inputs; existing survival, clothing, building, fire, machine and power owners calculate their own heat state.

Thermal inputs include:

- air and radiant temperature;
- mean wind and gusts;
- humidity;
- precipitation and immersion;
- solar exposure;
- shelter and insulation;
- surface contact temperature;
- activity/exertion;
- fire, machinery, batteries and generator heat;
- wetness and evaporation;
- injuries, illness and circulation impairment.

Use bounded heat-flow approximations at sensible cadences. Distinguish dry sheltered cold from wet wind-exposed cold. Do not reduce thermal consequences to ambient temperature alone.

Buildings and rooms require an inspectable thermal envelope: internal temperature, insulation effectiveness, air exchange, openings, moisture, heat sources, occupancy and thermal mass abstraction. A closed but damaged room must behave differently from an intact insulated shelter.

## Layer 6 — wind as a physical system

Wind is a vector field sampled from regional state plus terrain/building modifiers and bounded gust events.

Consumers include:

- projectile drift and time-of-flight effects;
- smoke, fire spread and ember transport;
- sound propagation and masking;
- scent and airborne contamination;
- loose debris and carried-object stability;
- climbing, rope work, ladders, cranes and temporary structures;
- aircraft, drones and airborne payloads;
- wind generation;
- exposed-character balance and thermal loss;
- snow drifting and rain exposure.

Each consumer maps the vector through its own physical rules. Wind does not directly grant generic accuracy, stealth or movement debuffs.

## Layer 7 — weather-driven world consequences

Required consumer interfaces include:

- AI work schedules, shelter seeking, patrol routes, travel and risk tolerance;
- settlement labor and production scheduling;
- crops, soil moisture, irrigation and harvest risk;
- wildlife feeding, migration, shelter and tracks;
- water collection, runoff, flooding, freezing and contamination;
- solar/wind generation and battery temperature behavior;
- generator fuel use, starting reliability and cooling;
- Stirling heat rejection and useful waste heat;
- machine efficiency, overheating, freezing, corrosion and breakdown;
- construction time, cure/dry conditions and worker exposure;
- hauling, roads, vehicles and vertical logistics;
- structures, roofs, temporary works and drainage;
- mesh/radio links, optical/acoustic sensors and visibility;
- wound, respiratory, infection, fatigue and sleep risk.

All consequences must cite a sampled environmental state and consumer rule. Telemetry must be able to answer which weather input caused a failure.

## Layer 8 — forecasting and player information

Players learn weather through an evidence ladder:

1. direct observation: clouds, wind, temperature, visibility, precipitation and animal/NPC behavior;
2. simple instruments: thermometer, barometer, wind indicator, rain/snow gauge;
3. radio reports and settlement observations;
4. portable sensors and Edge Interface logging;
5. base weather station and regional mesh observations;
6. trained agent forecast using historical and current data;
7. restored strategic weather infrastructure where canonically plausible.

Forecasts are versioned information products with issue time, valid window, covered region, predicted ranges, confidence, provenance and model/sensor condition. Accuracy depends on observation density, sensor quality, communications, front stability, terrain, lead time and agent capability.

Never expose the authoritative future seed or exact front path to the client. Forecast uncertainty must be real, bounded and explainable rather than arbitrary lying.

## Three-resolution simulation

### Near-player

Use local samples for characters, projectiles, ropes, drones, fires, exposed machines, sound, debris and traversed surfaces. Run detailed client presentation: Niagara precipitation/debris, local fog, wet/snow/ice materials, wind audio, sky/cloud response and camera effects. Gameplay truth remains server-owned.

### Regional

Weather cells update authoritative settlements, AI plans, production, agriculture, power, travel routes, water and strategic accumulation. Use event-driven/batched updates and relevance projections for connected clients.

### Distant world

Advance fronts, climate/season baselines, cell trends and strategic consequences at a lower cadence. Offline catch-up must be deterministic, bounded, versioned and capped against runaway damage. When a region becomes relevant, refine from the authoritative coarse state without rerolling it.

## Multiplayer, replication and persistence

The server owns:

- cell/front identity, time, seeds, state and revisions;
- terrain/dynamic modifiers that affect gameplay;
- accumulation and strategic environmental consequences;
- forecast products and information access;
- environmental events delivered to consumers.

Replicate relevance-filtered cell samples, front observations, forecast products and significant accumulation changes. Clients interpolate presentation but may not report temperature, wind, precipitation, accumulation, forecast correctness or damage-causing exposure.

Persist:

- climate/season state and simulation clock;
- front identities and evolution state;
- regional cell state/revisions/seeds;
- persistent accumulation where gameplay-relevant;
- dynamic terrain/building modifiers;
- issued forecasts when player knowledge must survive restart;
- last-simulated time and bounded catch-up version.

Use the existing DayQ atomic journaling, corruption quarantine, migrations, tombstones, revisions and idempotent transactions. Do not create a weather save system.

Test late join, reconnect, stale observations, reordered updates, server restart during front movement/accumulation, world-partition unload/reload, migration, corrupted cell/front state, simultaneous structure/weather changes and deterministic catch-up.

## Exploits and mitigations

Prevent:

- relogging or crossing cell boundaries to reroll weather;
- client-forged favorable samples;
- forecast seed extraction;
- shelter-volume overlap granting impossible protection;
- stacking windbreaks or heaters beyond physical limits;
- unloading a region to avoid weather damage;
- pausing production/decay clocks through disconnect;
- duplicated water/snow resources;
- accumulation toggles that trap players without an escape/recovery route;
- weather stations granting perfect map-wide intelligence;
- denial-of-service through unbounded weather queries, particles or surface state.

## Unreal Engine 5.8 implementation guidance

Inspect the existing project before adding owners. Prefer:

- authoritative C++ world/environment subsystem for cells, fronts, samples, time, persistence and queries;
- versioned Data Assets/Tables for climates, seasons, terrain modifiers, precipitation families and consumer curves;
- spatial indexing compatible with World Partition rather than one Actor per tiny weather sample;
- double-precision world positions where large-world calculations require them;
- interfaces/events for consumers rather than cross-system direct mutation;
- Niagara Data Channels or equivalent for efficient client presentation driven by sampled gameplay state;
- material parameter collections, render targets, virtual textures or bounded surface masks only after a measured accumulation spike;
- MetaSounds, attenuation, occlusion, filters, Audio Volumes and reverb as consumers of environment samples;
- significance, pooling, culling and scalable quality bands for precipitation/debris/audio.

[World Partition](https://dev.epicgames.com/documentation/unreal-engine/world-partition-in-unreal-engine) is the streaming foundation, not the weather solver. [Niagara Data Channels](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-channels-in-niagara-for-unreal-engine) can efficiently distribute data to visual simulations, but Niagara never owns gameplay state. [Unreal Audio attenuation and occlusion](https://dev.epicgames.com/documentation/unreal-engine/sound-attenuation-in-unreal-engine) and [MetaSounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-reference-guide-in-unreal-engine) render weather-aware audio while the DayQ acoustic owner retains propagation truth.

## Required technical spikes

1. Moving front crosses several regional cells with no state discontinuity or client reroll.
2. Mountain/valley/forest/urban modifiers produce different local samples from one regional cell.
3. Rain becomes puddling/mud/runoff and later dries through deterministic state.
4. Snow accumulates, compacts, drifts, obstructs a route and persists through restart.
5. Freezing rain creates ice affecting traversal, vehicles and structures.
6. Character clothing/thermal response distinguishes sheltered dry cold from wet windy cold.
7. Wind changes projectile, smoke/fire, sound, climbing and drone outcomes through owner adapters.
8. Weather changes power, machine, AI, agriculture, wildlife, water and logistics schedules without parallel storm values.
9. Forecasts improve with instruments/stations/mesh/agents but remain uncertain and provenance-bound.
10. World Partition unload/reload and 24-hour bounded catch-up reproduce the same digest.
11. Two clients observe consistent authoritative state while receiving appropriate local presentation.
12. Representative 60-player/AI/base density meets server, client, network, memory, save and streaming budgets.

## Integrated vertical slice

Build one forecastable front crossing a valley settlement, forest route, exposed high-rise district and elevated industrial target:

1. Player observes pressure fall, cloud movement and wind shift.
2. Simple instruments provide a coarse forecast with visible uncertainty.
3. Player selects route, clothing, pack, fuel, battery, radio, rope and vehicle strategy.
4. Rain begins on one side of the region and advances spatially.
5. Valley fog reduces visibility while forest shelter reduces wind/rain exposure.
6. Rooftop wind makes vertical traversal and drone use dangerous.
7. Wet clothing, wind and exertion drive explainable thermal consequences.
8. Rain affects sound, tracks, fire, solar output, roads and machine operation.
9. Temperature falls; water/mud transitions toward ice/snow where conditions support it.
10. Accumulation changes a road, doorway or roof load and forces a new decision.
11. AI changes work and travel plans using the same regional state.
12. Player reaches shelter, dries equipment and uses Stirling waste heat while managing thermal signature.
13. Save/restart/unload/reload preserves front and accumulation state.
14. A later upgraded station/agent forecast is better but not perfect.

## Acceptance gates

Reject completion unless:

1. one authoritative state produces every consumer's weather input;
2. fronts move spatially and change gradually;
3. terrain/elevation/buildings create inspectable local differences;
4. precipitation accumulation persists and changes gameplay;
5. thermal consequences use exposure, clothing, wetness, wind, activity and shelter;
6. wind is vector-based and reaches all required consumers through owner interfaces;
7. AI, power, machines, water, wildlife, agriculture, structures, communications and logistics respond coherently;
8. forecasts expose uncertainty and never leak hidden future truth;
9. near/regional/distant simulation refines without reroll or discontinuity;
10. multiplayer authority, late join, restart, migration, corruption and catch-up tests pass;
11. players can identify the approaching hazard and make a preparation decision;
12. weather creates choices rather than repetitive maintenance;
13. worst-case performance budgets pass with measured evidence;
14. screenshots/video/logs show the same authoritative event across gameplay and presentation.

## Governance record

```yaml
id: authoritative-weather-world-simulation
question: Does DayQ use disconnected weather effects or one authoritative multi-resolution atmosphere/front/terrain/accumulation simulation consumed by all systems?
status: decided
owner: user
dependency_milestone: product identity, world scale, persistence, survival, clothing, fire, power, traversal and multiplayer authority
evidence_method: explicit user direction + systems analysis + UE 5.8 prototype + multiplayer/persistence/performance tests
evidence_required:
  - moving-front vertical slice
  - terrain-localization proof
  - accumulation and thermal proof
  - consumer integration matrix
  - two-client/restart/catch-up evidence
  - representative performance evidence
options:
  - id: disconnected-effects
    description: independent visual weather presets and system-local storm scalars
    benefits: [fast presentation prototype]
    costs: [contradictory state, weak persistence, exploits, impossible systemic causality]
  - id: authoritative-world-weather
    description: one multi-resolution authoritative environmental system supplies versioned samples and events to all consumers
    benefits: [causal gameplay, persistence, forecasting, cross-system consistency, scalable simulation]
    costs: [requires shared interfaces, spatial simulation, persistence and performance proof]
recommendation: authoritative-world-weather
decision: authoritative-world-weather
rationale: Weather must change the world and player decisions without allowing visual, survival, AI, audio or production systems to invent contradictory storms.
consequences:
  - eight-layer model is locked
  - near/regional/distant resolution architecture is locked
  - environment owner is singular
  - Niagara/audio/materials are presentation consumers
  - every system consequence must trace to an authoritative sample
  - forecasts remain uncertain information products
acceptance_criteria:
  - all fourteen acceptance gates pass
reopen_when:
  - user changes direction
  - measured performance disproves a resolution/cadence choice; only that implementation choice reopens
artifacts_to_update:
  - weather/environment system sheet
  - survival, clothing, fire, power, water, building, traversal, ballistics, audio, AI, wildlife, agriculture, vehicles, drones, communications, crafting and persistence sheets
  - environmental catalog/schema and consumer interface contract
  - Blackglass world/vertical-slice plan
  - technical-spike registry, work orders and no-skip ledger
```

## Required completion report

Report:

- inspected owners and conflicts;
- environment/front/accumulation contracts;
- every consumer adapter and retained authority;
- cells/cadences/resolution choices and evidence;
- assets, C++, Blueprints, data and levels changed;
- tests, PIE route, logs, screenshots and video;
- multiplayer, persistence, catch-up and migration results;
- server/client/network/memory/save/streaming performance;
- failures, repairs, unresolved evidence and exact remaining gates.

Do not declare completion from cloud particles, a day/night sky, snowfall materials, a compiling Blueprint or an empty-map benchmark. Completion requires a moving authoritative front whose state persists, changes multiple systems coherently, remains explainable to players, survives multiplayer/restart, and meets representative performance budgets.
