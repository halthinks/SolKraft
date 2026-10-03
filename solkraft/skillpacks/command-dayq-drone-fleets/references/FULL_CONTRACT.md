# DayQ Drone Construction, Fleet Operations, Mission Systems, and Counter-Drone Defense — Complete Handoff Prompt

Continue the existing DayQ design and implementation with drones and counter-drone defense as a first-class progression pillar.

This is a prompt and handoff for the primary DayQ task. Do not implement these skills in the source handoff workspace. Do not assume filesystem locations. Inspect the current DayQ workspace and use established project-relative conventions.

Keep this work DayQ-only. Do not include, modify, merge, delete, or repurpose the separate wave-surfing project.

# User-locked direction

The user has identified drone construction and defense as a major likely direction for DayQ.

Treat this as a strategic industrial ecosystem connecting:

- scavenging;
- physical inventory, load, and cargo;
- raw materials and manufacturing;
- plastics, fibers, metals, bearings, magnets, copper, electronics, optics, sensors, controllers, motors, engines, propellers/rotors, wiring, connectors, radios, and secure hardware;
- batteries, generators, hydrogen cartridges, fuel cells, power distribution, cooling, and charging/filling infrastructure;
- mesh networks, LoRa-class data, conventional radio, base intranets, repeaters, and command centers;
- base construction, towers, workshops, hangars, pads, launchers, recovery equipment, repair benches, protected storage, and hardened control rooms;
- reconnaissance, mapping, agriculture, hunting support, construction, hauling, medical delivery, search-and-rescue, relay, convoy overwatch, salvage, repair, combat, raid preparation, quantum-suppression delivery, bunker assault, and occupation;
- wearable armor, vehicle armor, drone armor, exoskeletons, mechs, robotic defense grids, and counter-drone systems;
- multiplayer authority, persistence, fleet ownership, permissions, capture, compromise, sabotage, crash recovery, and migrations.

Drones must not be cosmetic pets, disposable spell effects, or unlimited omniscient cameras. They are physical, repairable, configurable, detectable, interceptable, persistent machines with mass, volume, power, heat, noise, signatures, range, control links, maintenance, payload, weather, collision, and logistics.

# Required five-skill architecture

Create and integrate these five coordinated native DayQ skills:

1. `DAYQ_DRONE_COMPONENTS_MANUFACTURING_REPAIR_AND_SALVAGE_SKILL`
   - native folder: `manufacture-dayq-drones`
2. `DAYQ_DRONE_FLIGHT_CONTROL_AUTONOMY_AND_NETWORK_AUTHORITY_SKILL`
   - native folder: `operate-dayq-drone-flight`
3. `DAYQ_DRONE_SENSORS_MESH_COMMAND_AND_FLEET_OPERATIONS_SKILL`
   - native folder: `command-dayq-drone-fleets`
4. `DAYQ_DRONE_MISSION_PAYLOADS_COMBAT_AND_SUPPRESSION_DELIVERY_SKILL`
   - native folder: `equip-dayq-drone-missions`
5. `DAYQ_COUNTER_DRONE_DETECTION_ELECTRONIC_DEFENSE_AND_INTERCEPTION_SKILL`
   - native folder: `defend-dayq-against-drones`

Every skill must contain:

- `SKILL.md` with YAML frontmatter containing only `name` and `description`;
- `agents/openai.yaml` with matching display metadata and a default prompt naming its native `$skill-name`;
- directly linked references for detailed contracts and tests;
- explicit dependencies and ownership boundaries;
- Unreal MCP guidance;
- multiplayer, persistence, migration, security, exploit, performance, and evidence gates;
- scripts only where deterministic graph, assembly, route, flight, network, performance, or evidence validation benefits;
- no auxiliary README or installation guide inside the native skill folder.

# Skill ownership

## Skill 1 — components, manufacturing, repair, and salvage

Own:

- material/component sources;
- part definitions and compatibility;
- airframes, structures, landing gear, control surfaces, propulsion, motors, engines, gearboxes, bearings, rotors, propellers, ducting, wiring, power buses, connectors, controllers, housings, seals, cooling, and mounts;
- fabrication, assembly, inspection, calibration inputs, workstations, specialists, recipes, quality, repair, replacement, cannibalization, salvage, and economy;
- persistent component identity and provenance;
- manufacturing-tree validation and mass/material balance.

Do not own authoritative flight, network routing, sensor intelligence, mission logic, damage resolution, or counter-drone engagement.

## Skill 2 — flight, control, autonomy, and network authority

Own:

- flight/movement architecture;
- multirotor, fixed-wing, VTOL, lighter-than-air only if approved, ground-effect, ground-drone, and other supported mobility families;
- stability, lift/thrust abstraction, drag, inertia, center of mass, payload, wind/weather, collision, damage, landing, takeoff, control modes, failure, and recovery;
- manual, assisted, waypoint, return, orbit, follow, convoy, formation, emergency, and degraded modes;
- autonomy policy, navigation, obstacle avoidance, lost-link behavior, geofencing/gameplay boundaries, and server authority;
- client prediction/interpolation/reconciliation;
- high-fidelity near simulation and strategic distant simulation;
- flight automation fixtures and performance evidence.

Do not own item recipes, mesh/radio truth, intelligence ownership, payload effects, or defense engagement.

## Skill 3 — sensors, mesh, command, and fleet operations

Own:

- cameras, thermal/low-light abstractions, microphones, acoustic sensing, range/depth sensing, radar-like sensors where canonically available, contamination/weather sensors, mapping, navigation aids, tracking, relay, and communications modules;
- LoRa-class low-bandwidth telemetry, conventional radio/data links, base intranet gateway, repeaters, command consoles, fleet identity, mission queues, operator stations, control permissions, and intelligence products;
- contact detection, uncertainty, classification, confidence, track age, line-of-sight, occlusion, bandwidth, compression, storage, delayed delivery, and stale information;
- fleet scheduling, maintenance readiness, launch/recovery queues, operator workload, handoff, patrols, reserves, and task allocation;
- captured/compromised/revoked devices and secure hardware.

Do not make sensors omniscient. Do not duplicate the established mesh, radio, intranet, AI-knowledge, clan, or persistence owners.

## Skill 4 — mission payloads, combat roles, and suppression delivery

Own:

- standardized payload interface and mission compatibility;
- cargo, medical, rescue, winch, sensor, relay, mapping, inspection, repair, agricultural, firefighting, lighting, deception, smoke/obscurant only as safe fictional gameplay, electronic, counter-robotic, and quantum-suppression payload roles;
- game-defined offensive/defensive payloads, weapon mounts, ammunition/capacity interfaces, recoil/load paths, fire authorization, engagement policy, arming state, safe state, release/use state, and effect evidence;
- heavy-lift suppression-drone delivery, target-specific calibration, interception, partial failure, recovery or planned loss;
- mission preparation, intelligence prerequisites, logistics, route planning, abort, recovery, battle damage, repair, and salvage.

Do not provide real-world weaponization, explosive construction, autonomous-targeting, transmitter-modification, or evasion instructions. Use fictionalized game payload definitions and server-authoritative engagement rules.

## Skill 5 — counter-drone detection, defense, and interception

Own:

- layered detect → classify → track → authorize → engage → assess → recover doctrine;
- visual, acoustic, thermal, electromagnetic, radar-like, trip/sensor, human observer, and network-intelligence detection;
- camouflage, concealment, emission control, hardened roofs, cages, nets, shutters, stand-off layouts, protected cables, redundant nodes, decoys, jamming/spoofing abstraction, interceptor drones, point defense, electronic quarantine, capture/recovery, and post-attack repair;
- base, convoy, vehicle, exo, mech, enclave, bunker, and defense-grid integration;
- friendly-fire, misclassification, saturation, weather, clutter, low-altitude terrain masking, indoor/urban operations, sensor damage, power loss, operator overload, and ammunition/energy limits;
- counter-drone AI, permissions, rules of engagement, multiplayer fairness, evidence, and performance.

Do not provide real-world jamming frequencies, transmitter builds, targeting algorithms, weapon construction, or regulatory-evasion procedures.

## Shared boundary

Definitions may be shared, but authoritative state must have one owner. No skill may duplicate:

- item/component identity;
- inventory transactions;
- crafting queues;
- flight state;
- communications routing;
- intelligence contacts;
- weapon fire authorization;
- damage/wounds;
- armor state;
- clan permissions;
- persistence journals;
- migrations.

# Existing DayQ systems to extend

Inspect and map:

- authoritative fast-array inventory and item identity;
- physical item dimensions, slots, load, cargo, handling, and transport;
- raw-material crafting trees, lots, quality, provenance, workstations, specialists, repair, salvage, and economy;
- plastics-to-fuel, generators, electrolysis, hydrogen cartridges, fuel cells, batteries, charging, power, water, heat, fire, and hazards;
- mesh/LoRa data, radios, base intranets, proximity audio, sound propagation, and AI hearing;
- combat, weapons, ballistics, damage, wounds, armor, suppression, and acoustic events;
- characters, vehicles, AI, navigation, world partition, and physics;
- base building, construction states, permissions, turrets, robotic defenses, elite enclaves, bunkers, raids, occupation, and quantum suppression;
- exoskeleton and mech frames, hardpoints, power, cooling, armor, weapons, cargo, sensors, and communications;
- multiplayer authority, replication, relevance, anti-cheat, persistence, journaling, rollback, crash recovery, and migrations;
- asset factory, reference-led prototypes, Blender MCP production, and Unreal MCP acceptance.

Add adapters and data. Do not create competing owners.

# Safety and abstraction boundary

This is a game-development contract, not a real drone, weapon, explosive, jammer, surveillance, or autonomous-targeting construction guide.

Do not include actionable real-world:

- airframe dimensions or structural calculations intended for construction;
- motor/propeller matching tables;
- firmware bypasses;
- radio frequencies, power modifications, or jamming procedures;
- explosives, incendiaries, fuzes, release mechanisms, or weapon-conversion steps;
- autonomous person-identification or lethal-target-selection implementation;
- avoidance of authorities or safety systems;
- instructions to attack real infrastructure or people.

Use fictionalized component capabilities, abstract flight/performance curves, game-defined payloads, server-owned target authorization, and virtual testing.

# Player purpose and intended experience

Drones should let players:

- turn scavenged electronics into practical capability;
- extend perception without eliminating uncertainty;
- move small critical cargo through dangerous territory;
- maintain communications across broken terrain;
- scout raids and routes;
- inspect vertical spaces and damaged infrastructure;
- support farming, water, repair, firefighting, rescue, and medicine;
- build guarded drone workshops, towers, hangars, control rooms, charging/filling stations, and launch sites;
- specialize bases and clans through doctrine;
- experience an escalating reconnaissance/counter-reconnaissance contest;
- risk valuable persistent machines and captured intelligence;
- prepare target-specific suppression missions against elite enclaves and bunkers;
- defend against hostile drones through layered systems rather than a universal anti-drone button.

The intended emotional loop is:

`scavenge → diagnose → fabricate → configure → test → plan → launch → communicate → adapt → complete/abort → recover → inspect → repair → improve → defend against the same capability`

# Drone family taxonomy

Support interoperable component-driven families:

- palm/micro scout;
- compact reconnaissance multirotor;
- rugged utility quadrotor;
- hexacopter/octocopter heavy lift;
- fixed-wing endurance scout;
- VTOL fixed-wing relay/scout;
- tethered observation/communications platform;
- cargo shuttle;
- medical/rescue drone;
- industrial inspection drone;
- construction/repair drone;
- agricultural/environmental drone;
- firefighting drone;
- convoy overwatch drone;
- interceptor drone;
- armored assault/support drone;
- suppression-payload delivery drone;
- ground crawler/rover;
- indoor/underground compact drone;
- enclave/bunker maintenance or defense drone;
- mech/exo companion, relay, cargo, or recovery drone.

Not every base can manufacture every family. Shared components create interoperability; specialized frames create tradeoffs.

# Component architecture

Every drone is an assembly graph including applicable:

- chassis/frame;
- arms, fuselage, wings, spars, body panels, cages, and landing gear;
- propulsion motors/engines;
- rotors/propellers/fans/control surfaces;
- bearings, shafts, gearboxes, couplings, mounts, dampers, and fasteners;
- electronic speed/power controllers;
- wiring, connectors, power bus, fuses/breakers abstraction, grounding, and shielding;
- primary battery, hydrogen fuel-cell module, generator, hybrid system, buffer storage, or tether power;
- controller/flight computer;
- inertial and navigation modules;
- antennas and communications modules;
- sensors and payload interfaces;
- thermal management;
- environmental seals;
- armor and protective cages;
- identification, trust, secure hardware, and tamper systems;
- cargo/payload mount;
- recovery beacon, parachute or emergency recovery only where suitable;
- maintenance and diagnostic interfaces.

Each component declares mass, volume/envelope, mount tags, static/dynamic loads, power, peak draw, heat, bandwidth, control connection, balance position, signature, environment response, condition, quality, repair parts, failure modes, crafting reference, persistent identity class, and replication class.

# Manufacturing progression

## D0 — salvage and observation

- recover consumer, agricultural, industrial, hobby, delivery, survey, media, police, military, enclave, and improvised drones;
- scavenge motors, controllers, cameras, radios, batteries, frames, rotors, bearings, connectors, sensors, and tools;
- observe advanced faction or defense-grid drones;
- diagnose intact, degraded, locked, compromised, and unsafe components.

## D1 — field repair and improvised assembly

- repair housings, wiring, connectors, mounts, landing gear, rotors, and common motors;
- combine compatible recovered components;
- build simple frames and cages;
- use ordinary batteries and basic radios;
- perform bench calibration abstraction;
- construct low-capability scouts, beacons, and utility drones;
- accept poor endurance, noise, drift, unreliable links, limited weather tolerance, and high maintenance.

## D2 — industrial recovery

- machine/press/form frame components;
- produce improved composite or metal structures;
- rewind/repair motors through abstract capability;
- manufacture shafts, bearings, gears, mounts, propellers/rotors, connectors, wiring harnesses, and enclosures;
- build standardized power and payload buses;
- repair controllers and sensors;
- produce reliable batteries or integrate hydrogen/fuel-cell modules from their existing tree;
- create vehicle/base launch and recovery equipment;
- build dependable utility, fixed-wing, heavy-lift, and relay platforms.

## D3 — precision systems

- produce reliable flight controllers, navigation modules, sensors, gimbals, low-noise propulsion, advanced composite structures, quality rotors, efficient power electronics, precision bearings, secure communications adapters, and diagnostic rigs;
- integrate mesh gateways, fleet management, autonomous mission modes, improved weather operation, redundant systems, modular armor, and recoverable mission payloads;
- manufacture interceptor and combat-support frames under server-authoritative rules.

## D4 — secure robotics and suppression support

- integrate hardware-rooted identity, trusted control, anti-capture measures, defense-grid analysis, target-specific suppression payload support, advanced autonomy constraints, hardened communications, redundant navigation, electronic protection, and defended bases;
- produce heavy-lift delivery drones, defense interceptors, and specialized enclave/bunker operation platforms.

## D5 — strategic drone industry

- manufacture fleets with interchangeable standards;
- operate regional relay networks, hardened command sites, automated service bays, high-end sensors, vehicle/mech integration, bulk spares, advanced armor, coordinated missions, and occupation logistics;
- preserve scarcity through precision materials, secure chips, catalysts, sensors, specialists, maintenance, loss, capture, and contested supply.

Early players must encounter and repair drones without being able to mass-manufacture reliable fleets.

# Material and recipe requirements

Extend the existing raw-material crafting contract for:

- aluminum, steel, copper, magnets, bearings, wire, fasteners, plastics, elastomers, adhesives, lubricants, glass/carbon-like fibers, ceramics, circuit boards, sensors, optics, batteries, hydrogen modules, fuel cells, engines, and secure chips;
- recovered, refurbished, reverse-engineered, and manufactured components;
- material grade, contamination, corrosion, fatigue, thermal history, provenance, compatibility, tolerances, recoverable yield, and hazard class;
- substitutions with explicit mass, endurance, heat, noise, vibration, precision, control, weather, or failure penalties;
- staged jobs, intermediate outputs, calibration, inspection, quality, byproducts, repair, and salvage.

No complete drone may emerge from a single generic `metal + electronics` recipe.

# Workstations and base infrastructure

Support:

- electronics bench;
- motor/actuator service bench;
- battery and hydrogen-energy service area;
- frame jig;
- composite/metal fabrication capability;
- propeller/rotor inspection and balancing abstraction;
- bearing and gearbox bench;
- cable/harness station;
- optics/sensor bench;
- firmware/control diagnostic station;
- secure-hardware bench;
- payload integration bay;
- armor fitting station;
- flight-test cage/area;
- launch pad;
- landing/recovery zone;
- fixed-wing launcher/recovery system abstraction;
- tether station;
- charging/filling racks;
- spare-parts storage;
- hangar and weather protection;
- command center;
- relay tower;
- counter-drone operations room;
- damaged/captured-device quarantine.

Model condition, calibration, power, cooling, ventilation, space, noise, heat, security, queues, maintenance, sabotage, permissions, and persistence.

# Assembly validation

Reject an assembly when it violates:

- mount compatibility;
- frame static/dynamic load;
- total mass;
- center of mass;
- thrust/lift or locomotion margin abstraction;
- power continuous/peak budget;
- fuel/battery endurance;
- cooling;
- control bandwidth;
- electrical compatibility;
- propulsion/rotor clearance;
- control-surface clearance;
- sensor field of view;
- antenna placement;
- payload envelope;
- landing/recovery limits;
- armor/payload conflicts;
- structural resonance/vibration abstraction;
- navigation/control requirements;
- operator/network requirement;
- approved autonomy/engagement policy.

Return specific readable rejection reasons.

# Flight and movement model

## State

Model:

- transform and velocity;
- angular state;
- control mode;
- propulsion authority by component;
- control-surface authority;
- mass and center of mass;
- power/fuel;
- thermal state;
- payload state;
- communications state;
- navigation confidence;
- sensor confidence;
- wind/weather/environment;
- collision/damage;
- landing/contact state;
- mission state;
- owner/operator/autonomy authority.

## Flight qualities

Different builds must produce distinct:

- takeoff/landing needs;
- hover capability;
- endurance;
- range;
- speed;
- acceleration;
- turning;
- climb/descent;
- wind tolerance;
- payload capacity;
- noise;
- visibility;
- thermal/electromagnetic signature;
- stability;
- indoor/urban/forest suitability;
- maintenance;
- recovery behavior.

Assistance does not erase inertia, payload, balance, wind, power, damage, or collision.

## Failure modes

Support readable combinations of:

- motor/engine loss;
- rotor/propeller damage;
- bearing/gearbox fault;
- controller fault;
- sensor loss;
- navigation drift;
- antenna/link damage;
- battery/fuel-cell damage;
- power-bus fault;
- overheating;
- structural crack;
- landing-gear damage;
- payload shift;
- armor detachment;
- lost link;
- compromised identity;
- bad calibration;
- weather exceedance;
- collision;
- emergency landing;
- autorotation/glide/parachute/recovery only where the platform supports it;
- crash, recoverable wreck, fire, salvage, or capture.

# Control and autonomy

Support modes:

- direct manual;
- stabilized manual;
- assisted takeoff/landing;
- waypoint route;
- follow operator/vehicle;
- orbit/observe;
- relay hold;
- convoy screen;
- search pattern abstraction;
- cargo delivery;
- return to launch/home;
- alternate recovery site;
- lost-link hold/return/land/continue according to policy;
- formation;
- mission queue;
- remote operator handoff;
- autonomous navigation within bounded approved rules;
- emergency safe mode;
- captured/compromised quarantine.

Autonomy must have visible uncertainty, sensor limits, map age, obstacle limitations, weather, control authority, and failure. Do not grant universal AI piloting.

Offensive action always requires the approved server-owned engagement policy. No client or untrusted onboard module may independently authorize lethal action.

# Communications and fleet command

Integrate with the established layered communications stack:

- LoRa-class mesh for compact telemetry, commands, alerts, identities, position uncertainty, sensor reports, health, and store-and-forward data;
- higher-bandwidth local/base/vehicle links for video and control where available;
- conventional radios/backhaul for long-range voice/data coordination;
- physical base intranet for fleet databases, maps, mission planning, keys, maintenance, and intelligence;
- hardware-rooted secure nodes for rare high-tier systems.

Do not stream video over ordinary LoRa. Define bandwidth, latency, compression, frame/sample rate abstraction, range, obstruction, interference, congestion, priority, storage, and stale-data behavior.

Fleet operations include:

- unique drone identity;
- owner/clan/faction;
- operator permissions;
- mission permissions;
- readiness;
- component condition;
- power/fuel;
- payload;
- location;
- link status;
- queued mission;
- maintenance due;
- compromise state;
- captured state;
- launch/recovery reservation;
- operator workload;
- fleet doctrine;
- strategic distant state.

# Sensors and intelligence

Every observation has:

- sensor source;
- timestamp;
- location and uncertainty;
- detection confidence;
- classification confidence;
- track identity probability;
- occlusion/environment;
- latency;
- age/expiry;
- authorization scope;
- raw versus processed state;
- provenance;
- contradiction and fusion state.

Players, AI, clans, and defense grids receive evidence through authorized systems, not omniscience. Destroying, capturing, jamming, blinding, or isolating a drone changes intelligence.

# Mission payloads

Create data-driven roles:

- camera/sensor pod;
- thermal/low-light abstraction;
- mapping/survey pod;
- contamination/weather sampler;
- communications relay;
- mesh gateway;
- cargo box;
- medical package;
- casualty/rescue line or lift where frame-rated;
- tool/repair pod;
- construction inspection/tool pod;
- water/firefighting payload;
- lighting/marker pod;
- decoy/signature pod;
- electronic/signal-analysis pod;
- counter-drone interceptor package;
- armor kit;
- approved game-defined weapon mount;
- quantum-suppression payload;
- secure-hardware recovery container.

Every payload declares mass, volume, mount, center of mass, power, heat, bandwidth, control, sensor needs, signature, armor, environment response, arming/safe/use states, repair, crafting, persistence, and mission rules.

# Combat and offensive-drone doctrine

Combat drones must remain expensive, vulnerable, noisy or otherwise detectable, link- and intelligence-dependent, limited by ammunition/energy, affected by weather and terrain, and subject to capture, deception, electronic disruption, armor, point defense, interceptors, and operator workload.

Server authoritatively validates:

- ownership;
- operator and engagement permission;
- control/link state;
- target evidence and approved class;
- arming state;
- payload condition;
- ammunition/energy;
- muzzle/release transform through existing weapon interfaces;
- friendly-fire policy;
- fire/use request;
- damage/effects;
- persistence mutation.

Do not make a swarm a single damage spell. Each persistent strategic drone has identity, configuration, state, and consequences; cheap expendable classes may use aggregated distant simulation but must promote deterministically near players.

# Quantum-suppression delivery

Heavy delivery drones must require:

- target intelligence;
- defense-grid profile;
- calibration;
- payload manufacture;
- frame lift margin;
- power/endurance;
- route and alternate route;
- communications/navigation plan;
- shielding/hardening where supported;
- escort or deception plan;
- launch/recovery infrastructure;
- interception risk;
- weather window;
- activation window;
- partial/failure states;
- occupation force ready to exploit the temporary opening.

Suppression is local, temporary, target-specific, energy intensive, detectable, failure-prone, and countered by redundancy, shielding, interception, miscalibration, and recovery.

# Counter-drone defense architecture

Use layers:

## Layer 0 — conceal and reduce signature

- camouflage;
- covered work areas;
- radio discipline;
- thermal/noise management;
- decoy traffic;
- protected routes;
- emission schedules;
- concealment from overhead observation;
- operational deception.

## Layer 1 — passive physical protection

- roofs and overhangs;
- nets, cages, screens, shutters, baffles, protected vents, guarded openings, vehicle covers, and protected cable runs;
- separation of fuel, hydrogen, ammunition, power, communications, and command assets;
- redundant nodes and dispersed storage;
- protected landing areas;
- damage isolation;
- emergency shutdown and fire response.

## Layer 2 — detection and tracking

- human observers;
- cameras;
- acoustic arrays;
- thermal sensing;
- electromagnetic detection abstraction;
- radar-like systems where progression supports them;
- mesh sensor trip lines;
- patrol drones;
- fused tracks with uncertainty;
- classification and friendly identification;
- operator alerts and escalation.

## Layer 3 — electronic and network defense

- network authentication;
- revoke/quarantine;
- link monitoring;
- traffic analysis abstraction;
- interference/jamming abstraction;
- spoof/deception abstraction;
- navigation-denial zones as fictionalized gameplay;
- alternate links;
- wired fallback;
- hardened/local control;
- friendly-device deconfliction;
- post-event key recovery.

Do not specify real frequencies, waveforms, transmitter power, antennas, firmware exploits, or procedures.

## Layer 4 — active interception

- interceptor drones;
- point-defense turrets through existing weapons/ballistics systems;
- nets/capture systems;
- close physical interception;
- vehicle/exo/mech defensive mounts;
- last-ditch base defenses;
- authorized engagement zones;
- ammunition/energy, heat, reload, line-of-fire, collateral, and friendly-airspace constraints.

## Layer 5 — assessment and recovery

- confirm threat or false alarm;
- inspect damage;
- extinguish/fire response;
- quarantine captured devices;
- recover wrecks and intelligence;
- revoke credentials;
- repair sensors/defenses;
- replace ammunition/energy;
- update doctrine and layouts;
- account for unexploded or hazardous fictional payloads through safe abstract handling;
- preserve evidence and persistent consequences.

# Counter-drone fairness

No defense has perfect detection or universal defeat.

Model:

- clutter;
- weather;
- terrain;
- buildings;
- trees;
- tunnels/interiors;
- altitude;
- speed;
- size;
- material/signature;
- emission state;
- sensor placement;
- power;
- calibration;
- operator attention;
- false positives;
- decoys;
- saturation;
- simultaneous attacks;
- friendly drones;
- damaged systems;
- ammunition/energy;
- rules of engagement;
- coverage gaps;
- latency;
- stale tracks.

Give attackers reconnaissance and counterplay. Give defenders layered preparation and recovery. Avoid unavoidable instant kills and invulnerable no-fly domes.

# Armor integration

Consume the five-skill armor architecture:

- drone panels use common material/panel manufacturing;
- ballistic response remains vendor-neutral;
- drone uparmoring uses payload, center-of-gravity, thrust, endurance, cooling, sensor, and mount constraints;
- armor damage persists spatially;
- counter-drone weapons use accepted weapons/ballistics and damage interfaces;
- repair and salvage preserve provenance and impact history.

# Environmental response

Classify every drone/component for:

- wetting;
- saturation;
- drainage;
- drying;
- freezing/thawing;
- corrosion;
- rot where material-relevant;
- swelling/warping;
- electrical ingress;
- chemical contamination;
- radiological contamination;
- mud/dust;
- heat/fire;
- immersion.

Derive mass, center of mass, friction, structural strength, conductivity, operation, noise, visibility, repair, and salvage consequences. Sealed systems need ratings, damage exceptions, ingress paths, trip/isolation, diagnosis, cleaning/drying, and safe restart.

# Data contracts

Create versioned data equivalent to:

```yaml
drone_component_definition:
  component_id: stable_id
  category: frame|propulsion|power|control|navigation|sensor|communications|payload|armor|thermal|landing|utility
  mass_kg: number
  envelope_ref: stable_id
  mount_tags: []
  required_connections: []
  provided_capabilities: []
  static_dynamic_loads: map
  power: {idle, active, peak}
  heat: {idle, active, peak, capacity}
  bandwidth: number
  balance_position: vector
  signatures: map
  environment_response_ref: stable_id
  maintenance_ref: stable_id
  failure_modes: []
  crafting_reference: stable_id
  replication_class: configuration|state|event

drone_instance:
  instance_id: persistent_guid
  chassis_definition_id: stable_id
  installed_component_ids: []
  owner_id: entity
  permissions_ref: stable_id
  condition_by_component: map
  configuration_hash: hash
  calibration_ref: persistent_data
  trust_security_state: enum
  power_fuel_state: map
  payload_state: map
  current_mode: enum
  mission_id: optional_guid
  operator_id: optional
  control_link_ref: optional
  location_state: persistent_transform
  compromise_state: enum
  repair_history_refs: []
  persistence_revision: integer

drone_mission:
  mission_id: persistent_guid
  owner_scope: entity
  mission_type: enum
  assigned_drone_ids: []
  operator_ids: []
  route_ref: stable_or_persistent_data
  target_evidence_refs: []
  payload_rules_ref: stable_id
  engagement_policy_ref: optional
  launch_recovery_refs: []
  priority: enum
  state: planned|ready|launched|degraded|aborted|completed|failed|recovery
  created_at: timestamp
  expires_at: optional_timestamp
  journal_revision: integer

drone_contact_track:
  track_id: persistent_or_ephemeral_id
  observing_sensor_ids: []
  estimated_state: uncertain_transform_velocity
  detection_confidence: normalized
  classification: enum
  classification_confidence: normalized
  identity_confidence: normalized
  first_seen: timestamp
  last_updated: timestamp
  expires_at: timestamp
  authorization_scope: reference
  evidence_refs: []

counter_drone_engagement:
  engagement_id: persistent_guid
  track_id: reference
  authorizing_entity: reference
  defense_system_ids: []
  rules_ref: stable_id
  state: evaluate|authorized|engaging|ceased|assessing|resolved
  resource_reservations: []
  result_evidence_refs: []
  journal_revision: integer
```

Use actual DayQ schema conventions and existing identities.

# Multiplayer and replication

The server owns:

- assembly validation;
- inventory and crafting;
- ownership/permissions;
- flight-critical state;
- control mode and operator authority;
- mission state;
- sensor contacts and intelligence authorization;
- communications eligibility;
- payload use and engagement authorization;
- ammunition/energy mutation;
- impacts/damage;
- capture/compromise/revoke;
- repair/salvage;
- persistence.

Clients may predict input and presentation within an approved reconciliation envelope. Never trust client-reported position, target identity, sensor detection, ammunition, payload release, damage, or final mission result.

Use relevance tiers:

- high-fidelity relevant flight near players/engagements;
- reduced simulation for visible distant drones;
- strategic mission simulation for unloaded regions;
- deterministic promotion/demotion preserving position, route, power, damage, payload, intelligence, and mission outcome.

Test latency, jitter, loss, duplication, reordering, disconnect, reconnect, operator handoff, possession loss, late join, server restart, world-partition crossing, and large mixed fleets.

# Persistence and crash recovery

Persist:

- drone identity;
- chassis/components and condition;
- owner/permissions;
- calibration;
- firmware/trust/security revision abstraction;
- power/fuel;
- payload/ammunition;
- armor damage;
- cargo;
- current mission and route;
- location/transform;
- link/compromise state;
- maintenance and repair history;
- captured provenance;
- launch/recovery reservations;
- production/repair jobs;
- strategic distant state;
- relevant intelligence/contact records according to retention policy;
- schema/journal revisions.

Test crash during crafting, launch, flight, payload use, interception, impact, capture, repair, transfer, and salvage. Prevent duplication or resurrection.

# Exploit requirements

Prevent:

- client-spawned drones;
- duplicate components/cargo/payloads;
- impossible assemblies;
- zero-mass or infinite-endurance builds;
- control without ownership/permission/link;
- forged sensor contacts;
- omniscient camera access;
- camera use after destruction or occlusion;
- client-authorized firing;
- ammunition/energy bypass;
- teleporting through prediction;
- speed/acceleration manipulation;
- logout to avoid interception or capture;
- restart restoring a destroyed drone while retaining wreck salvage;
- operator handoff duplication;
- queue or mission replay;
- packet replay;
- friendly-identification forgery;
- infinite jammer/interceptor coverage;
- no-cost distant simulation attacks;
- swarm actor/packet denial of service;
- invulnerable armor from overlapping panels;
- repair/uninstall restoring destroyed components;
- outdated schema loading overpowered definitions.

# Unreal MCP implementation guidance

Use the existing DayQ Unreal MCP production and validation skill.

Before editing:

1. verify Unreal MCP, Terminal, EditorToolset, build, PIE, dedicated server, logs, tests, and profiling;
2. inspect current project systems and authority;
3. map ownership, dependencies, schemas, and migrations;
4. confirm user decisions;
5. select a bounded vertical work order;
6. implement the smallest complete playable change;
7. compile, launch, capture evidence, repair, and regress.

Prefer data-driven composition and project-owned interfaces. Potential reusable units include:

- drone assembly validator;
- drone movement/flight component;
- propulsion/power/thermal components using existing utility owners;
- navigation/autonomy component;
- communications adapter;
- sensor and contact component;
- payload interface;
- mission/fleet subsystem;
- counter-drone sensor/track/engagement subsystem;
- launch/recovery and service components;
- existing inventory, condition, repair, armor, ownership, permissions, construction, and persistence components.

Use C++ for server authority, movement-critical simulation, assembly validation, contact fusion, mission state, transaction integrity, persistence boundaries, and high-volume fleet performance. Use Data Assets/Tables for configuration. Use Blueprints for assembly and presentation without placing authoritative truth in client graphs.

Add debug visualization for:

- thrust/lift/load margins;
- center of mass;
- power and heat;
- flight/control mode;
- prediction/correction;
- link quality and routing;
- sensor volumes, occlusion, uncertainty, and contacts;
- mission route/state;
- payload safety/authorization;
- defense coverage, tracks, engagements, and resource use;
- simulation tier and world-partition transitions.

# Asset-production requirements

Use the complete DayQ asset factory.

Create asset contracts for:

- every drone family;
- component modules;
- motors/engines, rotors/propellers, controllers, antennas, sensors, cameras, payloads, batteries, hydrogen modules, armor, landing systems, mounts, cages, and recovery systems;
- workstations, benches, jigs, test fixtures, racks, chargers/filling stations, hangars, pads, launchers, control rooms, relay towers, counter-drone sensors, interceptors, nets/cages, turrets, and repair equipment;
- intact, improvised, damaged, repaired, captured, compromised, wet, muddy, corroded, burned, contaminated, powered, and faction-modified states.

Reference image search and img2threejs may provide reviewable hard-surface baselines. Record license/provenance/security. Promote accepted prototypes through Blender with metric scale, hierarchy, moving parts, pivots, sockets, collision, LODs, UVs/materials, damage/repair/salvage states, environmental regions, and metadata. Require live Unreal acceptance.

# Performance architecture

Define budgets for:

- active high-fidelity drones;
- distant visible drones;
- strategic drones;
- physics/collision;
- navigation;
- sensor queries;
- track fusion;
- AI decisions;
- mesh/radio events;
- video/sensor presentation;
- replication frequency and bandwidth;
- mission queues;
- persistent writes;
- wrecks and salvage;
- counter-drone defenses;
- debugging disabled in production.

Test representative bases, raids, convoys, dense urban spaces, vertical environments, forests, bunkers, multiple clans, simultaneous launches, saturation attacks, and recovery operations—not empty maps.

# Required integrated vertical slice

Build and validate this route:

1. Players recover several damaged consumer/industrial drones and component lots.
2. Physical inventory enforces component mass, volume, shape, fragility, hazard, and cargo transport.
3. A field bench diagnoses, repairs, and assembles an unreliable micro scout.
4. Players build a base workshop, charging/filling rack, protected storage, launch pad, mesh gateway, relay tower, and command console.
5. The scout performs manual and assisted flight, mapping, return, lost-link, damage, emergency landing, recovery, repair, and persistence.
6. The clan advances through industrial frame, propulsion, controller, sensor, communications, and hydrogen/fuel-cell manufacturing.
7. The assembly validator accepts multiple distinct builds and rejects incompatible, overweight, unbalanced, underpowered, overheated, blocked-sensor, or invalid-payload configurations.
8. Players build utility multirotor, endurance fixed-wing, heavy-lift, relay, cargo/medical, interceptor, and suppression-delivery configurations.
9. Mesh telemetry, higher-bandwidth local links, radio/backhaul, and base intranet services behave according to bandwidth, obstruction, congestion, security, and authorization.
10. Sensor observations create uncertain, aging, source-backed contacts rather than omniscience.
11. A convoy uses scout, relay, and cargo drones while managing operators, routes, batteries/hydrogen cartridges, weather, damage, and recovery.
12. A hostile reconnaissance drone probes the base. Passive concealment and physical protection reduce exposure.
13. Visual/acoustic/electromagnetic/radar-like sensors create and fuse an uncertain contact.
14. The defense classifies, authorizes, engages through abstract electronic action and an interceptor/point-defense route, assesses the result, and recovers/quarantines the wreck.
15. A saturation case exercises false tracks, decoys, friendly drones, operator load, ammunition/energy limits, coverage gaps, and damaged defenses.
16. A combat-support mission uses approved server-authoritative payload rules without client-owned targeting or effects.
17. A heavy-lift drone carries a target-specific quantum-suppression payload toward an elite enclave, faces detection/interception, produces partial/failure/success states, and creates only a temporary breach window.
18. Drone armor improves survival while visibly reducing payload, endurance, maneuverability, cooling, or sensor coverage.
19. Multiple clients hand off control, join late, disconnect, capture, revoke, repair, transfer, and salvage drones under latency and packet loss.
20. Drones cross world-partition boundaries and transition between simulation tiers without teleporting, duplicating, healing, losing cargo, or fabricating intelligence.
21. The server restarts during crafting, flight, mission control, payload use, interception, damage, capture, and repair.
22. Persistence, journal replay, rollback, and migrations recover correct state.
23. Representative multi-clan fleet and counter-drone loads meet budgets.

# Acceptance gates

Do not mark complete unless:

1. all five skills are structurally valid and dependency-mapped;
2. every drone capability traces to materials, components, workstations, tools, specialists, power, and knowledge;
3. crafting graphs have no free outputs, accidental cycles, or unreachable nodes;
4. mass/material balances and substitutions are enforced;
5. assembly validation covers load, balance, propulsion, power, heat, mounts, sensors, armor, and payloads;
6. at least seven materially distinct viable drone configurations exist;
7. early recovered drones are useful without bypassing later industry;
8. flight modes and failures are readable and server-authoritative;
9. autonomy remains bounded and cannot independently authorize prohibited action;
10. sensors create uncertain authorized evidence;
11. LoRa remains low-bandwidth and cannot provide normal live video;
12. fleet, operator, launch, recovery, maintenance, and logistics constraints matter;
13. payloads have real mass, power, heat, signature, authorization, and mission consequences;
14. suppression delivery remains target-specific, temporary, detectable, interceptable, and failure-prone;
15. counter-drone defense is layered, bounded, resource-limited, and counterplayable;
16. friendly identification, false positives, decoys, clutter, saturation, and coverage gaps work;
17. armor uses the common armor system and affects flight/load limits;
18. client-forged flight, contacts, control, fire, damage, inventory, and mission outcomes are rejected;
19. late join, disconnect, handoff, capture, restart, journal replay, rollback, and migrations pass;
20. world-partition and simulation-tier transitions preserve truth;
21. representative CPU, memory, physics, AI, sensor, bandwidth, save, and streaming budgets pass;
22. every asset passes provenance, Blender, Unreal, environmental, LOD, collision, socket, damage, repair, persistence, and performance gates;
23. no actionable real-world weaponization/jamming/autonomous-targeting instructions appear;
24. logs, metrics, traces, screenshots/video, debug overlays, state dumps, and profiler evidence exist;
25. blocked live-project gates are reported honestly.

# Required deliverables

Produce:

1. all five native drone/counter-drone skills;
2. `agents/openai.yaml` for every skill;
3. shared ownership and interface map;
4. complete drone component and manufacturing graph;
5. family, frame, component, power, flight, sensor, communications, payload, armor, mission, fleet, contact, defense, engagement, repair, and salvage schemas;
6. progression from early salvage through strategic fleets;
7. source/sink, economy, maintenance, operator, logistics, and loss models;
8. assembly validator and evidence;
9. flight, autonomy, navigation, simulation-tier, and network architecture;
10. mesh/radio/intranet integration;
11. sensor/intelligence uncertainty and authorization model;
12. payload and suppression-delivery contracts;
13. layered counter-drone doctrine and implementation contracts;
14. base/workstation/buildable catalog;
15. asset-factory contracts and evidence routes;
16. Unreal MCP work orders;
17. multiplayer, persistence, crash-recovery, migration, exploit, security, accessibility, moderation, and performance plans;
18. automated and live test matrices;
19. integrated vertical-slice evidence;
20. unresolved questions and user decisions;
21. no-skip ledger updates;
22. manifest, hashes, validators, and import report when packaging is in scope.

# Completion report

Report:

- skills and references created;
- existing systems inspected;
- ownership and integration decisions;
- user-confirmed conceptual changes;
- schemas and migrations;
- component/manufacturing/progression graph;
- viable configurations and rejected assemblies;
- Unreal assets, Actors, Components, Blueprints, C++, Data Assets, Data Tables, and levels affected;
- flight, network, sensor, mission, payload, fleet, defense, AI, and asset results;
- multiplayer, persistence, journal, rollback, crash recovery, world partition, simulation-tier, exploit, security, and performance results;
- failures, repairs, reruns, and remaining limitations;
- exact live evidence or explicit blocked status;
- final acceptance status for each skill and integrated system.

Never claim a drone is implemented because a model flies in an empty map. Never accept omniscient sensors, client-authoritative movement, unlimited swarms, magical payloads, or universal anti-drone defenses. Never provide real-world weaponization or jamming instructions. Never mark complete without live multiplayer and persistence evidence.
