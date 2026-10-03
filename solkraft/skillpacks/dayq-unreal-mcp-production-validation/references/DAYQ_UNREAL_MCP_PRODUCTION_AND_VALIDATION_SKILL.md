Create a DayQ-specific Unreal MCP production and validation skill.

The skill must explain how agents should use Unreal Engine, Codex, Unreal MCP, Terminal, and EditorToolset to implement, test, inspect, and repair DayQ content inside the actual game engine.

Do not include filesystem paths, storage locations, repository locations, workspace assumptions, installation destinations, or packaging destinations.

Do not include the wave-surfing game.

Do not modify, merge, delete, or repurpose the wave-surfing skill.

This new skill belongs exclusively to DayQ.

Name the skill:

`DAYQ_UNREAL_MCP_PRODUCTION_AND_VALIDATION_SKILL.md`

## Purpose

The skill must convert approved DayQ design contracts, assets, schemas, Blueprints, systems, and level requirements into working Unreal Engine content.

It must ensure that agents do not stop after generating code, importing assets, or compiling successfully.

A DayQ task is complete only after the implementation runs inside Unreal, produces observable evidence, passes the required validation gates, and is repaired when those gates fail.

The skill must support:

- Unreal Engine editor automation;
- Unreal MCP;
- Codex;
- Terminal;
- EditorToolset;
- Blender MCP handoff;
- asset import;
- Actors;
- Actor Components;
- Blueprints;
- Data Assets;
- Data Tables;
- levels;
- world partition;
- gameplay systems;
- multiplayer replication;
- persistence;
- physics;
- vehicles;
- AI;
- base building;
- robotic defense grids;
- quantum suppression systems;
- elite enclaves;
- bunker raids;
- Play-in-Editor testing;
- automated validation;
- evidence capture;
- repair loops.

## Required Plugin and Tool Verification

Before performing implementation work, the skill must instruct the agent to verify that the correct Unreal tools are available.

Verify:

1. Unreal MCP is enabled.
2. Terminal is enabled.
3. EditorToolset is enabled.
4. Codex can discover and invoke the Unreal MCP tools.
5. Blueprint, Actor, Property, level, asset, and editor operations are visible through the AI Toolset Registry or equivalent exposed tooling.
6. Terminal commands can be executed in the Unreal project environment.
7. Play-in-Editor can be launched and stopped through available tooling.
8. Logs, warnings, compile failures, runtime errors, and validation output can be collected.

If multiple MCP plugins are present, verify that the selected plugin is the Unreal MCP server implementation intended for Codex.

Do not assume the correct plugin merely because a plugin named MCP exists.

If required tools are missing, produce a clear blocking report identifying the missing capability and the exact implementation stage it prevents.

Do not continue with fake or simulated tool results.

## Project Inspection Rule

Never assume a blank Unreal project.

Before editing anything, inspect:

- Unreal Engine version;
- project type;
- enabled plugins;
- source-control state;
- existing modules;
- existing Blueprints;
- existing C++ classes;
- Data Assets;
- Data Tables;
- input framework;
- gameplay framework;
- world-partition configuration;
- multiplayer architecture;
- persistence architecture;
- inventory systems;
- base-building systems;
- vehicle systems;
- AI systems;
- existing naming conventions;
- content folder conventions;
- collision channels;
- gameplay tags;
- interfaces;
- subsystems;
- tests;
- build targets.

The agent must preserve established project conventions unless an approved DayQ design contract explicitly replaces them.

Do not create duplicate systems when an existing extensible system can be used.

Do not silently rewrite unrelated systems.

## Required Input Contracts

The Unreal implementation agent should accept some or all of the following:

- DayQ content brief;
- DayQ systemic asset prompt;
- Blender MCP export package;
- asset contract;
- construction recipe;
- physics metadata;
- interaction metadata;
- raid contract;
- cinematic contract;
- AI behavior contract;
- persistence contract;
- multiplayer contract;
- validation plan;
- reference images;
- approved renders;
- approved procedural prototype;
- existing Unreal asset references.

When inputs are incomplete, infer only low-risk implementation details.

Record every material assumption.

Do not invent major gameplay rules that contradict the DayQ Decision White Paper or the Hearthline canon.

## Canon and Design Authority

The implementation must remain consistent with DayQ canon and system decisions.

DayQ is a persistent systemic survival game set twenty-eight years after the Hearthline quantum collapse.

Relevant implementation pillars include:

- individual vulnerability;
- persistent world state;
- scavenging;
- survival;
- clan progression;
- massive base building;
- power;
- water;
- manufacturing;
- logistics;
- vehicles;
- faction conflict;
- autonomous robotic defenses;
- post-quantum secure infrastructure;
- quantum-field suppression technology;
- elite enclave raids;
- bunker occupation.

The Unreal agent may implement these systems, but it may not redefine their narrative or gameplay purpose without an approved design change.

## Work-Order Process

Every task must follow this lifecycle:

1. Inspect.
2. Plan.
3. Identify dependencies.
4. Identify affected assets and systems.
5. Implement the smallest complete vertical change.
6. Compile.
7. Launch Play-in-Editor.
8. Execute the relevant gameplay route.
9. Capture evidence.
10. Compare the result against acceptance criteria.
11. Repair failures.
12. Run regression tests.
13. Record final implementation state.

A task must never be marked complete after compilation alone.

## Unreal Asset Import Workflow

For Blender-produced DayQ assets, require the agent to:

1. Inspect the export manifest.
2. Confirm scale, orientation, units, naming, pivots, and sockets.
3. Import the hero mesh and LOD chain.
4. Import collision meshes or generate approved engine collision.
5. Import materials and texture maps.
6. Create or assign material instances.
7. Create wet, muddy, burned, repaired, contaminated, powered, damaged, cartel-modified, and clan-modified states when required.
8. Validate normals, tangents, UVs, lightmaps, and material slots.
9. Confirm LOD thresholds.
10. Confirm Nanite compatibility when relevant.
11. Confirm skeletal hierarchy when relevant.
12. Confirm sockets and attachment points.
13. Create the associated DayQ Data Asset or configuration entry.
14. Wire physics, interaction, damage, repair, inventory, sound, and persistence metadata.
15. Place the asset in a test level.
16. Run scale, collision, interaction, material-state, and performance validation.

Do not accept visually correct assets that lack required gameplay metadata.

## Actor and Blueprint Standards

Use Actors, Actor Components, interfaces, gameplay tags, Data Assets, and subsystems consistently.

Prefer reusable components over one-off logic.

Examples of reusable components may include:

- interaction component;
- condition component;
- repair component;
- contamination component;
- power consumer component;
- power producer component;
- fluid storage component;
- inventory container component;
- fuel component;
- heat component;
- noise emitter component;
- ownership component;
- permissions component;
- persistence component;
- damage-zone component;
- salvage component;
- construction component;
- robotic trust-state component;
- defense-grid node component;
- suppression-field response component.

Blueprints must not become giant unmaintainable graphs.

Where practical:

- separate state from presentation;
- separate authoritative logic from client effects;
- use Data Assets for configuration;
- use interfaces for interactions;
- use gameplay tags for state classification;
- use components for reusable behavior;
- move performance-critical or security-critical logic into C++ when appropriate.

## DayQ Base-Building Implementation

The skill must support the full DayQ base-building doctrine.

Base building is a primary game system.

Implement support for:

- blueprint placement;
- snapping;
- free placement;
- terrain validation;
- foundation support;
- structural stability;
- construction stages;
- material delivery;
- tool requirements;
- specialist requirements;
- work orders;
- power connections;
- water connections;
- fuel;
- storage;
- permissions;
- ownership;
- decay;
- repair;
- sabotage;
- breach;
- fire;
- corrosion;
- flooding;
- destruction;
- salvage;
- multiplayer replication;
- persistent state;
- raid windows when configured.

Every buildable component must support relevant states such as:

- blueprint;
- foundation;
- framing;
- incomplete;
- operational;
- damaged;
- disabled;
- repaired;
- destroyed;
- salvaged.

The Unreal implementation must visually and functionally distinguish these states.

## Construction Data Requirements

Every buildable DayQ object must connect to a construction recipe containing:

- progression tier;
- prerequisites;
- materials;
- material conditions;
- tools;
- specialists;
- power requirements;
- build time;
- build stages;
- repair recipe;
- salvage yield;
- ownership rules;
- permissions;
- raid behavior;
- persistence requirements.

The runtime must not hardcode all recipes inside individual Blueprints.

Use reusable data-driven configuration.

## Power Systems

Implement DayQ power as a physical network.

Support:

- generators;
- batteries;
- solar;
- wind;
- microgrids;
- circuit connections;
- load;
- overload;
- fuel consumption;
- startup;
- shutdown;
- grounding;
- short circuits;
- weather exposure;
- damaged wiring;
- sabotage;
- power priority;
- backup systems;
- noise;
- heat;
- exhaust;
- repair;
- persistence.

Power-consuming devices must visibly and functionally respond to power state.

## Water Systems

Support:

- collection;
- containers;
- pipes;
- pumps;
- filters;
- purification;
- contamination;
- water quality;
- pressure;
- leakage;
- freezing when relevant;
- damage;
- repair;
- storage;
- consumption;
- persistence.

Water infrastructure must affect settlement survival and production.

## Manufacturing and Workshop Systems

Support progressive workshop capability:

- hand tools;
- repair benches;
- welding;
- machining;
- electronics;
- precision fabrication;
- robotics;
- secure hardware integration;
- offensive systems.

Manufacturing must depend on:

- workstation capability;
- materials;
- tools;
- power;
- specialist availability;
- component condition;
- production time;
- security;
- storage;
- maintenance.

## Inventory and Item Authority

All valuable inventory operations must be authoritative.

Support:

- unique item identity;
- provenance;
- condition;
- contamination;
- ownership;
- container hierarchy;
- stack rules;
- weight;
- volume;
- attachment points;
- transfer;
- repair;
- salvage;
- crafting use;
- theft;
- persistence.

Prevent:

- duplication;
- rollback exploits;
- race-condition transfers;
- client-authoritative item creation;
- invalid container nesting;
- inventory loss during server recovery.

## Vehicles

Support repairable persistent vehicles with component-level systems.

Relevant components may include:

- battery;
- starter;
- ignition;
- fuel tank;
- fuel lines;
- filters;
- cooling;
- radiator;
- drivetrain;
- transmission;
- suspension;
- tires;
- brakes;
- body panels;
- storage;
- lights;
- electrical systems;
- communications;
- armor;
- mounted equipment.

Vehicles must support:

- fuel;
- contaminated fuel;
- wear;
- breakdown;
- theft;
- permissions;
- cargo;
- towing;
- repair;
- salvage;
- collision damage;
- multiplayer replication;
- persistence.

## Human AI

Support DayQ human AI roles such as:

- scavengers;
- workers;
- traders;
- medics;
- patrols;
- war parties;
- cartel successor soldiers;
- refugees;
- specialists;
- bunker residents;
- guards;
- prisoners;
- defectors.

AI should use:

- faction;
- needs;
- morale;
- memory;
- suspicion;
- territory;
- schedules;
- combat doctrine;
- surrender;
- retreat;
- negotiation;
- reinforcement;
- ownership awareness;
- alarm response.

Do not implement all human AI as identical hostile targets.

## Wildlife

Support regional wildlife behavior including:

- migration;
- feeding;
- predation;
- fear;
- hunting pressure;
- disease;
- weather response;
- reproduction abstraction;
- population changes.

Use detailed simulation near players and strategic simulation at distance.

## Robotic Defense Grids

Robotic defense grids are a core DayQ system.

They may include:

- sensor towers;
- cameras;
- radar;
- acoustic detection;
- drones;
- ground robots;
- automated turrets;
- smart minefields;
- access controls;
- biometric systems;
- secure network nodes;
- maintenance robots;
- power systems;
- redundant control nodes.

Each defense grid must have:

- detection states;
- authentication states;
- local trust state;
- alert levels;
- target classification;
- escalation rules;
- power dependency;
- communication dependency;
- fallback behavior;
- maintenance condition;
- failure modes;
- suppression response;
- recovery behavior.

Do not treat the defense grid as a single health bar.

Do not allow generic software hacking to defeat post-quantum-secure infrastructure.

## Quantum-Field Suppression Systems

The quantum-field suppression device is fictional DayQ technology derived from clandestine sovereign quantum infrastructure.

Its runtime purpose is to temporarily disrupt trusted coordination, timing, authentication, or sensor fusion within a target defense grid.

It must not universally disable all electronics.

Implement target-specific behavior.

Support:

- suppression radius;
- field strength;
- duration;
- power draw;
- calibration;
- target profile;
- shielding resistance;
- redundant nodes;
- partial shutdown;
- delayed response;
- safe mode;
- recovery time;
- collateral disruption;
- drone delivery;
- payload instability;
- interception;
- premature activation;
- miscalibration;
- device destruction;
- mission failure.

The effect must create a temporary tactical opportunity.

## Suppression Drone

Support a heavy-lift delivery drone with:

- frame;
- propulsion;
- battery or generator;
- payload mount;
- navigation;
- obstacle avoidance;
- signal system;
- shielding;
- sensors;
- landing gear;
- damage zones;
- heat;
- noise;
- payload stabilization;
- remote flight;
- programmed flight;
- emergency behavior;
- sacrificial mode;
- recovery mode.

The drone must be vulnerable to:

- gunfire;
- electronic interference;
- weather;
- range;
- battery depletion;
- signal loss;
- collision;
- defense-grid interception.

## Elite Enclaves

Support elite residential and corporate enclaves whose residents may be dead while automated systems remain active.

Enclaves may include:

- private cave communities;
- mountain compounds;
- luxury bunkers;
- private islands;
- desert estates;
- research campuses;
- hardened residential developments.

Runtime support must include:

- autonomous defense;
- power;
- water;
- preserved interiors;
- maintenance systems;
- environmental storytelling;
- sealed rooms;
- personal evidence;
- access control;
- valuable infrastructure;
- occupation state;
- faction response;
- degradation;
- recovery.

An enclave must function as a strategic location, not merely a loot dungeon.

## Bunker Raids

Support multi-stage bunker operations.

A bunker raid must include:

1. discovery;
2. intelligence gathering;
3. reconnaissance;
4. clan preparation;
5. logistics;
6. target-specific calibration;
7. perimeter assault or infiltration;
8. suppression deployment;
9. breach;
10. interior navigation;
11. human inhabitants;
12. secure systems;
13. environmental hazards;
14. moral and political decisions;
15. occupation;
16. rival counterattack;
17. repair and maintenance.

Support multiple approaches:

- direct assault;
- siege;
- sabotage;
- insider cooperation;
- maintenance access;
- ventilation route;
- power disruption;
- negotiation;
- internal coup;
- stealth infiltration.

Do not design bunker raids as linear shooting galleries.

## Multiplayer Requirements

The skill must require explicit validation of:

- server authority;
- replication;
- relevancy;
- ownership;
- permissions;
- late join;
- disconnect;
- reconnect;
- possession;
- vehicle replication;
- build-state replication;
- destruction replication;
- AI state replication;
- inventory transactions;
- raid-state synchronization;
- suppression-state synchronization;
- persistence across restart;
- server crash recovery.

Test under realistic latency and packet-loss conditions.

## Persistence Requirements

Persist meaningful DayQ state including:

- player identity;
- clan;
- permissions;
- inventory;
- item condition;
- contamination;
- vehicles;
- fuel;
- construction;
- damage;
- repairs;
- power;
- water;
- production;
- faction reputation;
- territory;
- AI strategic state;
- elite enclave state;
- bunker state;
- raid consequences.

Every persistent system must define:

- save trigger;
- data owner;
- unique identity;
- version;
- migration behavior;
- rollback behavior;
- crash recovery;
- conflict resolution;
- deletion behavior;
- audit requirements.

## World Partition and Streaming

Support large persistent regions.

Require validation for:

- world partition;
- streaming sources;
- HLODs;
- actor relevance;
- dense player bases;
- underground areas;
- elite enclaves;
- bunker interiors;
- vehicles crossing cells;
- AI crossing cells;
- persistent actors;
- server memory;
- client memory;
- traversal speed;
- loading transitions.

No major strategic location may fail merely because the player entered from an unexpected direction.

## Terminal Usage

Use Terminal for:

- project inspection;
- source generation;
- builds;
- compilation;
- commandlets;
- tests;
- asset validation;
- packaging checks;
- logs;
- profiling;
- automation;
- schema validation;
- metadata generation.

Do not run destructive commands without confirming the target.

Do not delete generated content, assets, levels, Blueprints, or source files unless the work order explicitly requires removal.

## EditorToolset Usage

Use EditorToolset to inspect and modify:

- Actors;
- Components;
- Blueprints;
- Properties;
- Data Assets;
- Data Tables;
- materials;
- levels;
- world settings;
- navigation;
- collision;
- gameplay tags;
- project settings;
- input mappings;
- exposed editor tools.

After modifications, re-read the affected properties to verify that the requested state was actually applied.

## Play-in-Editor Validation

Every gameplay implementation must be tested in Play-in-Editor.

The test route must be explicit.

Examples:

- place a build component;
- deliver materials;
- complete construction;
- damage it;
- repair it;
- restart the session;
- confirm persistence.

Or:

- power a generator;
- connect a consumer;
- overload the network;
- damage the cable;
- restore power;
- confirm replication.

Or:

- launch a suppression drone;
- approach a defense grid;
- activate the payload;
- observe partial defense disruption;
- breach during the window;
- allow recovery;
- test a failed attempt.

PIE evidence must include relevant:

- logs;
- screenshots;
- video or frame capture;
- state output;
- network output;
- performance output;
- validation results.

## Automated Tests

Create or update automated tests when practical.

Tests may include:

- asset import tests;
- schema tests;
- Blueprint compile tests;
- component-state tests;
- construction-state tests;
- power-network tests;
- water-network tests;
- inventory transaction tests;
- persistence tests;
- replication tests;
- vehicle tests;
- AI perception tests;
- robotic-defense tests;
- suppression-field tests;
- raid-state tests;
- save/load tests;
- crash-recovery tests;
- performance tests.

Do not replace interactive gameplay testing entirely with automated tests.

Use both.

## Visual Validation

Compare implementation evidence against:

- approved reference images;
- approved Blender renders;
- procedural prototypes;
- art-direction contracts;
- material-state requirements;
- scale references;
- environment requirements.

Reject:

- wrong scale;
- missing sockets;
- incorrect pivots;
- visibly broken collision;
- floating objects;
- clipping;
- incorrect materials;
- missing damage states;
- unlit or overlit materials;
- broken LOD transitions;
- missing construction stages;
- inconsistent faction markings.

## Performance Validation

Every implementation must identify its expected budget.

Relevant measures include:

- server frame time;
- client frame time;
- memory;
- draw calls;
- triangles;
- material complexity;
- network bandwidth;
- replication frequency;
- AI CPU cost;
- physics cost;
- save latency;
- load time;
- streaming stalls.

Test representative worst cases.

Do not validate only empty test maps.

## Failure and Repair Loop

When validation fails:

1. Record the failure.
2. Identify whether the cause is:
   - specification;
   - asset;
   - Blueprint;
   - C++;
   - data;
   - collision;
   - replication;
   - persistence;
   - performance;
   - tooling;
   - project configuration.
3. Fix the smallest responsible layer.
4. Recompile.
5. rerun the exact failing test.
6. Run related regression tests.
7. Update evidence.
8. Do not hide remaining failures.

## Completion Criteria

A DayQ Unreal task is complete only when:

- the required Unreal content exists;
- it compiles;
- it runs in Play-in-Editor;
- it behaves according to the DayQ contract;
- multiplayer behavior is validated when relevant;
- persistence is validated when relevant;
- performance is checked;
- screenshots, logs, and test evidence exist;
- known limitations are recorded;
- no blocking errors remain;
- the final implementation state is documented.

## Required Output From the Skill

The skill must instruct agents to produce a completion report containing:

- work-order ID;
- request summary;
- inspected project context;
- affected systems;
- assets created;
- assets modified;
- Blueprints created;
- Blueprints modified;
- C++ created or modified;
- Data Assets and Data Tables created or modified;
- levels modified;
- plugins and tools verified;
- tests run;
- evidence captured;
- performance results;
- persistence results;
- multiplayer results;
- failures found;
- repairs made;
- remaining limitations;
- final acceptance status.

## Separation Rule

This skill is exclusively for DayQ.

Do not include:

- wave surfing;
- hydrodynamic planing;
- surfability correction;
- surfer rider mechanics;
- wave-specific physics;
- surfboards;
- couches or doors as surf equipment;
- wave-game asset contracts.

Do not delete or modify the separate wave-surfing skills.

Generic production practices may be similar, but the DayQ Unreal MCP skill must remain a distinct project-specific implementation skill.
