# DayQ Agent Systems — Complete Asset Catalog, Design-Prompt, and Production Handoff

## Energy realism routing override

Route all energy, fuel, refinery, generator, foundry and hydrogen asset jobs through `DAYQ_PLAYABLE_PLASTIC_TO_FUEL_PROGRESSION_HANDOFF_PROMPT.md` and `DAYQ_ENERGY_BOOTSTRAP_REALISM_DECISION.md`. Do not produce assets that imply a household printer and wheel forge can bootstrap gasoline refining, industrial foundry power or hydrogen-vessel manufacture.

Continue the primary DayQ task by creating the complete physical and digital asset-production layer for the 2058 agent infrastructure, training, autonomous research, AI-assisted design, tactical-companion, advanced exoskeleton, and pinnacle mech systems.

This is a prompt and handoff. Inspect the current DayQ workspace and its no-skip ledger before acting. Use workspace-relative conventions. Do not assume absolute paths. Do not modify, merge, delete, package, or reference the separate wave-surfing project.

The previously delivered agent-systems handoff remains authoritative for gameplay, progression, research, security, and tactical-companion behavior. This handoff supplies the missing complete item/design catalog and the skill route that prompts those items into production existence.

# User-locked outcome

Produce every physical part, device, machine, workstation, room kit, tool, consumable, interface, damaged variant, repair object, and gameplay data contract required to make the DayQ agent stack observable and buildable in the world.

The player must be able to understand the agent stack physically:

`scavenge components -> inspect provenance and condition -> transport -> clean/repair -> assemble racks and services -> restore an agent -> curate knowledge -> train and evaluate -> deploy into field hardware -> collect evidence -> research -> generate candidate designs -> prototype -> test -> qualify -> manufacture -> install in exos/mechs/drones/base systems -> repair, upgrade, capture, salvage, or lose`

Nothing important may exist only as a progress bar or invisible technology-tree icon.

# Skill architecture

Create one new DayQ-only native adapter skill:

`DAYQ_AGENT_SYSTEM_ASSET_CATALOG_AND_PROMPT_ROUTER_SKILL`

Native folder name:

`generate-dayq-agent-system-assets`

The new skill owns:

- complete agent-system asset catalog coverage;
- decomposition of a facility, machine, suit subsystem, or research capability into independently buildable assets and assemblies;
- stable catalog IDs, family IDs, variants, tiers, dependencies, interfaces, and completeness checks;
- selection of the correct prompt and production route for every catalog entry;
- generation of one `DAYQ_ASSET_FACTORY_JOB` seed per accepted asset or assembly;
- batch manifests, dependency ordering, shared-part reuse, asset-family consistency, and missing-item detection;
- family-level visual language and original 2058 DayQ design constraints;
- routing each item through the established skills without replacing them.

The new skill does **not** own:

- the general systemic asset contract;
- source rights or provider security;
- img2threejs implementation;
- Blender production;
- Unreal implementation;
- item identity;
- raw-material lots;
- recipes;
- inventory transactions;
- power, cooling, communications, weapon, armor, exo, mech, damage, persistence, or multiplayer truth.

Consume these existing skills as authoritative owners:

1. `$generate-dayq-systemic-asset-prompts`
   - Expands every minimal catalog entry into a 300–800 word canon-bound systemic production prompt.
2. `$build-dayq-systemic-asset-factory`
   - Owns immutable request-to-acceptance lineage, provenance, environmental classification, Blender/Unreal evidence, and final disposition.
3. `$produce-dayq-assets`
   - Owns reference reconstruction, img2threejs when suitable, Blender MCP promotion, inspection, repair, and export.
4. `$dayq-raw-materials-crafting-trees`
   - Owns sources, materials, processing, recipes, workstations, quality, repair, salvage, and progression DAGs.
5. `$dayq-unreal-mcp-production-validation`
   - Owns Unreal import, Data Assets, Actors/Components, interactions, replication, persistence, PIE, tests, and evidence.
6. `$dayq-physical-inventory-load-slots`
   - Owns mass, volume, shape, slots, containers, carry/load, handling, transport, and transfer.
7. `$build-dayq-agent-infrastructure`, `$train-dayq-agents`, `$orchestrate-dayq-agent-research`, `$design-dayq-with-agents`, `$secure-dayq-agent-systems`, and `$operate-dayq-tactical-companion-agents`
   - Own agent-system behavior and progression contracts.
8. Existing power, hydrogen, plastic refinement, communications/mesh/LoRa, drones, armor, weapons/ballistics, exoskeleton, mech, building, fire, repair, authority, persistence, and economy skills
   - Remain owners of their states and rules.

Do not create parallel versions of those systems. Add adapter records and foreign-key references.

# Required native skill structure

Create:

```text
generate-dayq-agent-system-assets/
  SKILL.md
  agents/openai.yaml
  references/AGENT_SYSTEM_ASSET_CATALOG.md
  references/ASSET_FAMILY_PROMPT_CONTRACTS.md
  references/ASSEMBLY_AND_INTERFACE_CONTRACTS.md
  references/PRODUCTION_ROUTE_MATRIX.md
  references/VALIDATION_MATRIX.md
  assets/DAYQ_AGENT_SYSTEM_ASSET_CATALOG.schema.json
  assets/DAYQ_AGENT_ASSET_BATCH_JOB.schema.json
  scripts/validate_agent_asset_catalog.py
  scripts/expand_agent_asset_batch.py
```

Keep `SKILL.md` concise. Its YAML frontmatter may contain only `name` and `description`. It must tell the agent exactly which references to read for catalog generation, prompt generation, production routing, assembly work, or validation.

`agents/openai.yaml` must contain a human-readable name, concise description, and default prompt that explicitly invokes `$generate-dayq-agent-system-assets`.

The validators must detect:

- duplicate IDs;
- missing dependencies;
- cycles where the ordinary build DAG must remain acyclic;
- orphan items;
- missing source/repair/salvage routes;
- unowned interfaces;
- references to nonexistent skills or schemas;
- asset families lacking variants, damage states, environmental classification, or evidence gates;
- assemblies whose required components cannot be produced, recovered, repaired, or substituted;
- outputs with no Unreal acceptance route.

# Universal catalog-entry contract

Every entry must define:

```yaml
asset_id: stable.dayq.id
family_id: stable.family.id
display_name: original DayQ name
category: enum
tier: T0|T1|T2|T3|T4|T5|T6
physical_or_digital: physical|digital|hybrid
common_or_original: common_baseline|recovered_2058|original_dayq|fictional_quantum
gameplay_purpose: []
owning_systems: []
required_skills: []
dimensions_and_mass_class: {}
material_regions: []
components: []
interfaces: []
mounts_and_sockets: []
power_heat_cooling_network: {}
inventory_and_transport: {}
environmental_applicability: {}
condition_states: []
damage_failure_modes: []
repair_reference: stable.id
salvage_reference: stable.id
recipe_reference: stable.id
source_route: enum
reference_needs: []
lod_collision_animation: {}
replication_class: configuration|state|event|cosmetic
persistence_fields: []
acceptance_gates: []
```

Every component/assembly interface must specify connector or mount class, power, data, coolant/fluid, structural load, bandwidth, security/trust, environmental sealing, compatibility tags, failure behavior, service access, and validation.

# Source and visual-baseline workflow

The intended use of web image search and img2threejs is explicit:

## Common objects

For ordinary real-world objects—racks, fans, pumps, tanks, server chassis, cables, workbenches, meters, tools, radios, printers, fire extinguishers, protective cases, keyboards, displays, cameras, ladders, carts, hoists, and similar items—use current web image search to establish a visual and construction baseline when a cleared local reference does not already exist.

Require:

1. multi-view or complementary references where hidden geometry matters;
2. scale cues and manufacturer-neutral construction analysis;
3. provider, creator, URL, retrieval time, license, modification/redistribution rights, attribution, and content hash;
4. quarantine and no execution of embedded scripts;
5. a detail inventory and source-suitability decision;
6. img2threejs only for suitable hard-surface/modular prototypes;
7. Blender MCP for final topology, UVs, material regions, LODs, collision, moving parts, damage/repair states, sockets, metadata, and export;
8. Unreal MCP for gameplay acceptance.

The common reference forms a **baseline**, not the final DayQ asset. Customize it with canonical age, repair history, faction modifications, component swaps, compatible 2058 systems, environmental exposure, gameplay interfaces, and material states.

## Original and futuristic objects

For Quantum ASIC stacks, sovereign accelerators, advanced companion cores, coherent control hardware, post-quantum trust devices, tactical-agent interfaces, advanced mech sensor suites, and other original 2058 technology:

- use a reference board containing lawful generic examples of adjacent real technologies;
- extract functional visual principles rather than copying a specific product;
- design original DayQ silhouettes, component hierarchy, service access, thermal solution, cables, shielding, indicators, wear, and faction modifications;
- clearly label fictional performance and technology;
- validate physical support needs: size, power, heat, cooling, vibration, calibration, maintenance, and transport;
- reject floating holographic magic, unexplained energy sources, ornamental greebling without function, and quantum hardware that looks or behaves like an ordinary glowing box.

## Route selection

Use exactly one declared route per job:

- `img2threejs_then_blender` for suitable common hard-surface/modular objects;
- `direct_blender` for original geometry, exact interfaces, or multi-part engineering assets;
- `licensed_source_then_blender` for cleared source models;
- `generated_source_then_blender` for generated candidates requiring full provenance/similarity/topology review;
- `dedicated_character_or_organic_pipeline` only when organic assets are genuinely required.

No reference image, generated mesh, procedural prototype, `.blend`, or import counts as completion without live Unreal evidence.

# Universal production-prompt template

For every catalog entry, invoke `$generate-dayq-systemic-asset-prompts` and produce one cohesive imperative prompt using this structure:

> Create `[asset name and variant]` for DayQ in 2058 as `[gameplay function and assembly role]`. Establish plausible real or explicitly fictional dimensions, mass, construction, material regions, capacity, ratings, interfaces, operating envelope, power draw, heat output, cooling demand, bandwidth, storage, latency, hazards, and service clearance. Describe its pre-collapse origin or original DayQ manufacturing history, its survival through the first fifteen days, day-thirty fragmentation, the three-year assault, and its condition and ownership twenty-eight years later when those facts are relevant. Separate every inspectable, moving, removable, repairable, replaceable, calibratable, and breakable component. Define structural mounts, power/data/cooling/fluid connectors, inventory and tool interactions, access panels, pivots, sockets, collision zones, damage zones, navigation blockers, audio/VFX emitters, and trust boundaries. Make its condition affect its actual gameplay outputs rather than appearance alone. Define all applicable dry, wet, dusty, muddy, contaminated, corroded, overheated, burned, frozen, damaged, repaired, improvised, faction-modified, powered, unpowered, degraded, quarantined, calibrated, and failed states with persistent consequences. Connect acquisition, raw materials, substitutions, processing, workstations, tools, specialists, power, build stages, quality, repair, salvage, transport, theft, sabotage, ownership, multiplayer authority, persistence, crash recovery, and migration to existing DayQ systems. Produce a hero mesh, appropriate LOD chain, collision, material instances, animations or moving states, named sockets, metadata, debug overlays, and validation renders. Route common visual baselines through cleared references and img2threejs when suitable; promote all accepted assets through Blender MCP and Unreal MCP. Require automated tests and a live PIE/dedicated-server route proving scale, interaction, interfaces, state transitions, environmental response, repair, replication, persistence, performance, and assembly compatibility. End with a complete `DAYQ_ASSET_FACTORY_JOB` seed and do not claim acceptance without hashed Blender and live Unreal evidence.

Replace every bracket and general statement with object-specific requirements. Never emit the template unchanged as an asset prompt.

# Complete required asset catalog

The following is the minimum catalog. The implementation task may add required dependencies, but may not silently omit an entry. Reuse shared parts through assemblies and variants instead of duplicating meshes and identities.

## A. Recovered knowledge, model, and training media

Generate prompts and jobs for:

- printed technical manual, field manual, textbook, maintenance binder, lab notebook, wiring diagram folio, calibration certificate, and damaged/annotated variants;
- optical archive disc and rugged archive case;
- solid-state archive module;
- encrypted data cartridge;
- model checkpoint cartridge;
- training dataset cartridge;
- evaluator-suite cartridge;
- doctrine package;
- signed firmware module;
- secure key/token module;
- removable memory brick;
- archival tape cartridge and tape library magazine;
- recovered personal assistant device;
- damaged sovereign research terminal;
- portable field-data recorder;
- suit mission-data recorder;
- tamper-evident evidence module;
- quarantine storage container;
- offline transfer case/data-diode kit;
- write blocker and media-imaging station;
- document scanner, overhead book scanner, camera copy stand, microphone capture kit, and human-demonstration recording rig.

Each data-bearing object needs provenance, capacity, interface, encryption/trust state, corruption, partial readability, contamination, physical damage, duplication policy, ingestion/quarantine workflow, and persistent hash/lineage.

## B. Operator terminals and everyday computing

- rugged handheld agent terminal;
- tablet terminal;
- laptop workstation;
- repairable desktop workstation;
- thin client;
- rack console/KVM;
- keyboard, pointing device, trackball, controller, rugged touch panel, stylus;
- flat display, rugged display, curved operations display, low-power e-ink status panel;
- projection unit only where physically justified;
- headset, throat microphone, boom microphone, speaker, haptic belt, warning beacon;
- portable diagnostic console;
- field programmer;
- secure enrollment terminal;
- training/debrief console;
- research visualization table;
- fabrication review console;
- server-room wallboard;
- base operations command desk;
- cable, adapter, dock, charger, protective case, stand, and mounting variants.

## C. Classical compute boards and modules

- salvaged CPU board;
- workstation motherboard;
- server motherboard;
- GPU accelerator card;
- NPU/AI accelerator card;
- FPGA card;
- classical ASIC accelerator;
- storage controller;
- network interface card;
- high-speed interconnect card;
- trusted-platform/post-quantum root module;
- HSM/security module;
- time-synchronization card;
- sensor-fusion processor;
- deterministic safety controller;
- actuator-control board;
- baseboard-management controller;
- power-management controller;
- debug/programming header module;
- expansion backplane;
- mezzanine board;
- memory DIMM family;
- persistent-memory module;
- removable rugged compute blade;
- low-power edge-agent module;
- suit-local hardened agent module;
- drone-agent compute module;
- robot-defense compute module;
- degraded, counterfeit, contaminated, overclocked, repaired, faction-modified, trusted, untrusted, and revoked states.

Board prompts must expose chips, heat spreaders, sockets, connectors, retention hardware, shielding, indicators, service access, firmware identity, trust state, cooling contact, power envelope, failure regions, and ESD handling.

## D. Servers, chassis, racks, and compute assemblies

- single-board improvised assistant node;
- rugged field-compute case;
- tower workstation;
- 1U/2U/4U server chassis variants;
- GPU accelerator chassis;
- storage server;
- training server;
- simulation server;
- evaluator server;
- orchestration/controller server;
- security/audit server;
- checkpoint vault server;
- tactical-companion deployment server;
- digital-twin server;
- fabrication scheduler server;
- full-height rack, half rack, wall rack, shock-isolated mobile rack;
- rack rails, cable-management arms, blanking panels, fan trays, dust filters, lockable doors, side panels, anchoring kit;
- rack PDU, metered PDU, intelligent breaker panel, bus bar, patch panel, fiber tray, network switch, console drawer;
- cluster backplane/interconnect fabric;
- A1 assistant closet assembly;
- A2 training rack assembly;
- A3 certified specialist cluster;
- A4 multi-agent research cell cluster;
- A5 sovereign research lattice;
- A6 coherent discovery complex as a proposed/tested late-game assembly, not established reality.

Each assembly must define floor loading, clearance, airflow, sound, heat, power, grounding, fire control, filtration, security, access, maintenance, transport, construction stages, partial operation, redundancy, and sabotage points.

## E. Sovereign Quantum ASIC and coherent accelerator hardware

- fictional quantum/coherent processing tile;
- Quantum ASIC control board;
- error-correction ASIC board;
- waveform/control electronics;
- precision timing oscillator and timing distribution module;
- photonic interconnect module;
- optical transceiver;
- cryogenic interface/control unit where required by tier;
- advanced room-temperature coherent module where supported by recovered fiction;
- calibration source;
- calibration sensor array;
- magnetic/electromagnetic shielding enclosure;
- vibration-isolation cradle;
- vacuum/cryogenic service interface where applicable;
- thermal-control manifold;
- trusted post-quantum root module;
- secure memory/audit module;
- classical scheduling/compiler controller;
- sovereign accelerator blade;
- multi-blade coherent chassis;
- timing rack;
- calibration rack;
- control rack;
- shielded quantum cabinet;
- Quantum ASIC stack assembly;
- branch-search accelerator assembly;
- quantum sensor-analysis assembly;
- suppression-field simulation assembly;
- damaged enclave/bunker recovered variants;
- counterfeit, miscalibrated, poisoned-firmware, shield-breached, thermally unstable, revoked, repaired, and qualified states.

Every prompt must distinguish fictional functions from present technology. Require classical controllers, power conditioning, cooling, timing, calibration, shielding, secure roots, and maintenance. Never render a generic glowing cube as the entire system.

## F. Storage, memory, checkpoint, and archive infrastructure

- SSD, HDD, archival tape, optical archive, rugged removable storage, persistent-memory variants;
- hot storage array;
- checkpoint repository;
- read-only doctrine repository;
- immutable audit store;
- evidence-ingestion store;
- quarantine store;
- training-data lake appliance;
- research artifact repository;
- backup appliance;
- offline cold-vault case;
- tape library;
- drive sled, caddy, cable, controller, enclosure, lock, seal, and label components;
- base master checkpoint vault;
- suit checkpoint loading dock;
- checkpoint transfer cradle;
- secure erase/sanitize station;
- recovery/imaging station;
- corrupted, degraded, partially readable, rebuilt, mirrored, stale-backup, revoked, captured, and restored states.

## G. Networking, mesh, LoRa, and agent communications

- copper and fiber cable families;
- rugged patch cables;
- connectors, couplers, splices, termination panels, reels, conduit, cable trays, weatherproof junction boxes;
- Ethernet switch, managed switch, router, firewall, gateway, network tap, data diode, protocol bridge;
- fiber switch and optical patch panel;
- Wi-Fi access point and directional link;
- mesh radio node;
- LoRa endpoint;
- LoRa gateway;
- portable relay;
- mast-mounted base relay;
- directional antenna, omnidirectional antenna, panel antenna, dish, mast, guy kit, grounding/lightning kit;
- secure base radio;
- portable radio;
- vehicle radio;
- exo/mech radio;
- drone datalink;
- tactical-companion encrypted link;
- time-sync node;
- network monitoring appliance;
- spectrum analyzer and field-strength meter;
- jamming/spoofing detector;
- authenticated squad-mesh module;
- disconnected field cache;
- damaged, jammed, spoofed, misconfigured, compromised, encrypted, degraded, weathered, and repaired states.

Compose with the existing communications skill. The asset prompt owns geometry and physical interfaces; communications remains authoritative over range, propagation, spectrum, encryption, routing, and voice/data behavior.

## H. Power generation, storage, conditioning, and distribution

- municipal-hardening gasoline generator family: small suitcase/inverter, construction-frame, towable municipal, stationary backup and pump/generator variants sourced from public works, emergency services, schools/shelters, clinics, water sites, municipal depots and public-safety communications locations;
- salvaged petroleum generator variants with intact, deployed, stripped, corroded, fuel-fouled, wiring-looted, alternator-damaged, overloaded, repaired, faction-held, transport-secured and operating states;
- plastic-derived fuel compatible generator variant owned by the energy tree;
- SG0 battery-powered bootstrap setup linking a damaged P1 printer, Edge Interface/basic agent and early plastic-conversion controls;
- SG1 linear Stirling generator assembled from frame/body, hot/cold assemblies, piston/displacer cylinder, linear alternator, mechanical families, reclaimed-petro burner, nitrogen service, regulator/protection and P1-printed housings/adapters/ducts/jigs/guards;
- SG2 workshop Stirling, SG3 modular generator bank, SG4 cogeneration plant and SG5 strategic heat-engine variants with visibly increasing heat exchange, alternator, cooling, control, service and grid equipment;
- nitrogen source/cylinder, service connection and depleted/leaking/contaminated states owned by the energy system;
- SG1 build-option visuals for portable, durable, fuel-tolerant and higher-output configurations generated from shared modular parts rather than unique bespoke meshes;
- idle, cranking/starting, cycling, loaded, overloaded, fuel-starved, dirty-burner, low-working-gas, weak-alternator, rubbing/knocking, overheated, unstable-output, damaged, repaired and upgraded states;
- RF1 Field Plastic Fuel Refinery with prepared-plastic input, internal processing presentation, crude-burner-oil output for SG1, residue/waste output, field-repair and fouled-maintenance states;
- RF1-RF4 single-job refinery family from `DAYQ_PLAYABLE_PLASTIC_TO_FUEL_PROGRESSION_HANDOFF_PROMPT.md`: Field Plastic Fuel Refinery, Workshop Plastic Fuel Refinery, Stabilized Fuel Refinery and Clan Fuel Works, plus RF5 depot/network assets. Internal reduction, conversion, cleanup and finishing appear within each refinery asset rather than as mandatory separate production stations;
- legacy and synthetic-gasoline containers across field, workshop, stabilized and industrial quality grades, with clean, contaminated, degraded, leaking, secured, connected and depleted states;
- alternator, starter, radiator, fuel tank, filters, belts, mounts, exhaust, control panel, outlets, grounding components;
- solar panel, frame, tracker, charge controller, combiner, disconnect;
- wind turbine, mast, brake, controller;
- micro-hydro generator where regionally valid;
- grid-tie and islanding inverter;
- transformer;
- rectifier;
- DC converter;
- power supply unit families;
- hot-swap server PSU;
- UPS;
- flywheel/buffer system;
- conventional battery bank;
- forklift and warehouse-vehicle traction packs, trays, chargers, contactors, fuses, connectors, cables and handling fixtures;
- telecom backup-cabinet modules, rectifiers, distribution, monitoring boards, protection gear, environmental cabinets and cooling;
- UPS and data-center rack modules, cabinets, UPS power stages, bypass gear, PDUs, breakers, monitoring controllers, busbars and cooling parts;
- solar-storage modules, inverters, charge controllers, combiners, disconnects, panel interfaces, weatherproof enclosures and monitoring systems;
- rare original-fiction residential wall-storage pack families for fortified solar homes and elite residential microgrids, including intact jackpot, empty mount, stripped, burned, flooded, management-locked, thermally suspect, isolated, extracted, transport-cradled, repaired and installed states;
- residential wall-pack raid assets: protected energy room, disconnect/isolation interaction, access panel, inverter/BMS, lifting and carry interfaces, cart/exoskeleton/vehicle restraints, clues in ordinary houses and persistent extraction/ownership markers;
- electric/hybrid vehicle traction modules, auxiliary packs, inverter, DC conversion, contactors, service disconnect, cooling hardware, wiring and charge interfaces;
- hospital emergency-storage modules, central UPS cabinets, generator-start batteries, portable medical packs, conditioned-power hardware, isolation equipment and service carts;
- industrial-robot and Battle Circuit packs, swap modules, high-rate buffers, chargers, BMS boards, contactors, motor controllers, test fixtures and damaged/improvised variants;
- utility/substation control-power banks and heavy-equipment/marine storage as additional source families;
- every industrial bootstrap battery family requires distinct intact, depleted, mismatched, corroded, flooded, impact-damaged, overheated, management-locked, protection-bypassed, repaired, recertified, installed, disconnected, extracted, transport-secured and salvage-only states, plus source-specific handling and interaction assets;
- futuristic hydrogen battery/fuel-cell module owned by the established energy skill;
- forged/recovered hydrogen cylinder variants, regulator, valve, relief device, manifold, leak sensor, cabinet, ventilation, and transport cradle;
- F2 Cylinder Forge Upgrade with installed, operating, damaged, repaired and upgraded states, plus early heavy and later improved manufactured metal hydrogen-cylinder variants;
- electrolyzer, water treatment feed, gas separator, dryer, compressor abstraction, safe storage and control assembly;
- rack PDU, busbar, breaker, fuse, disconnect, grounding rod, bonding strap, cable, plug, socket, junction box;
- power-quality analyzer;
- load bank;
- emergency lighting and shutdown system;
- low-voltage, brownout, surge, harmonic/noisy, grounded/ungrounded, overloaded, leaking, overheated, isolated, repaired, and sabotaged states.

Do not generate unsafe real-world hydrogen construction instructions. Model the gameplay chain, certified components, hazards, inspection, and fictionalized production abstractions.

## I. Cooling, air handling, and environmental control

- chassis fan, rack fan tray, blower, intake and exhaust duct;
- heat sink, heat spreader, cold plate, thermal pad, thermal compound;
- liquid-cooling pump, reservoir, manifold, hose, quick disconnect, valve, flow meter, filter, leak detector;
- radiator, dry cooler, evaporative cooler, chiller, heat exchanger;
- phase-change buffer module;
- room air handler;
- dust prefilter, fine filter, chemical filter, radiological filter, spare filter cassette;
- dehumidifier, humidifier, condensate drain;
- room temperature/humidity/particulate sensor;
- smoke/heat detector;
- oxygen and gas sensor;
- cryogenic plant abstractions and service tools where required;
- shielded cooling distribution unit;
- portable emergency cooling cart;
- server-room thermal containment panels;
- clogged, leaking, cavitating, frozen, contaminated, corroded, overheated, repaired, bypassed, and miscalibrated states.

## J. Security, trust, quarantine, and counter-agent hardware

- secure root module;
- HSM;
- biometric reader;
- token/card reader;
- physical key switch;
- tamper switch;
- seal and evidence label;
- secure enclosure;
- lockable rack/cage;
- checkpoint vault;
- air-gap transfer station;
- one-way data diode;
- quarantine compute box;
- sandbox rack;
- forensic workstation;
- audit recorder;
- anomaly monitoring display;
- revocation console;
- credential enrollment kit;
- secure backup case;
- Faraday/shielded case;
- shredding/destruction station abstraction;
- guarded network boundary cabinet;
- compromised, tampered, bypassed, spoofed, revoked, locked, quarantined, under-review, and recertified states.

## K. Training, evaluation, simulation, and debrief equipment

- human demonstration workstation;
- video/audio/sensor capture rig;
- motion-capture camera and marker/markerless reference kit;
- haptic controller and training manipulators;
- exoskeleton training harness;
- suit cockpit simulator;
- driving/flight/drone simulation controls;
- target and sensor simulator;
- environmental simulation chamber abstraction;
- network/communications simulator;
- synthetic workload server;
- evaluator server;
- benchmark cartridge;
- held-out test vault;
- adversarial test appliance;
- replay workstation;
- after-action debrief table;
- multi-display operations wall;
- trainer headset and console;
- calibration props and test fixtures;
- instrumented dummy/load rig;
- telemetry ingestion dock;
- field evidence reader;
- signed checkpoint deployment dock;
- failed, outdated, contaminated, poisoned-data, miscalibrated, incomplete, certified, and quarantined states.

## L. Research laboratory and metrology equipment

- electronics bench;
- ESD mat, grounding strap, storage bins, fume extraction;
- soldering station;
- hot-air rework station;
- microscope;
- magnifier lamp;
- oscilloscope;
- multimeter;
- logic analyzer;
- bench power supply;
- signal generator;
- spectrum analyzer;
- network analyzer abstraction;
- thermal camera;
- vibration sensor;
- load cell;
- strain gauge kit;
- material test coupons;
- dimensional metrology tools;
- calipers, micrometer, gauge blocks, indicators;
- surface plate;
- optical inspection station;
- materials microscope abstraction;
- environmental test enclosure;
- thermal cycling chamber abstraction;
- dust/water ingress test fixture;
- drop/impact test fixture;
- armor/ballistics test instrumentation owned by the armor/weapons evaluation systems;
- drone thrust stand;
- motor/actuator dynamometer;
- battery/fuel-cell cycler;
- sensor calibration tunnel/room;
- shielded RF test area;
- quantum calibration bench;
- sample storage, chemical cabinet, fire cabinet, PPE station;
- calibration-expired, damaged, contaminated, improvised, repaired, and certified variants.

## M. Fabrication and prototype equipment

- hand-tool bench;
- drill press;
- bandsaw;
- grinder;
- welding station;
- lathe;
- mill;
- CNC mill/lathe abstraction;
- sheet-metal brake;
- shear;
- hydraulic press;
- forging press;
- furnace/heat-treatment system abstraction;
- F0 camp hearth with stones/firebrick, small grate, hand tools and crude heated-part states;
- F1 wheel/brake-drum forge using a vehicle wheel, brake drum, grill/fire bowl or similar body; hair dryer, vehicle/HVAC/shop blower or hand-crank fan; metal air pipe; common forge material; ingot mold and handling tool;
- F1 manual-bellows alternative using leather/heavy cloth, sticks/boards, rope/bindings and air pipe, including manual pumping or assigned-worker interaction;
- alternative F1 grill, stove, heater, kiln-shell, steel-basin, school/shop forge and clan-fabricated forge bodies;
- F2 enclosed crucible furnace assembled from recovered heater/kiln/industrial shell, refractory, controlled air/heat module, crucible, molds, sensors and handling gear;
- F2 Cylinder Forge Upgrade shown as a visible upgrade to the existing forging station rather than a separate unrelated crafting bench;
- F3 recovered/rebuilt electric or induction furnace with power electronics, heating/coil assembly, controls, cooling, sensors and graded-feedstock output;
- F4 controlled alloy foundry kit with material separation, multiple furnace processes, molds, heat treatment, handling, testing and contamination-control equipment;
- F5 heavy foundry with large furnace, forging press, casting/ingot line, cranes/handling, inspection and vehicle/exo/mech-scale feedstock production;
- R2 controlled foundry with improved enclosure, powered air/heat control, interchangeable material-handling modules, molds, waste/slag capture abstraction and repeatable ingot stations;
- R3 materials lab with material identification, contamination testing, grading, polymer drying/compounding and conductor preparation equipment;
- R4/R5 precision-reclamation equipment for advanced alloy, copper, silver/gold-bearing concentrate, ceramic, composite and strategic feedstock abstractions;
- separate ferrous, light-alloy, copper/conductor, mixed precious-metal concentrate, silver/gold micro-ingot, polymer flake, polymer pellet/rod/spool/brick and electronic-substrate feedstock assets;
- P0 ruined/partial Glentech machine;
- P1 Home Polymer printer;
- P2 Reinforced Fabricator with engineering-polymer/composite modules;
- P3 Circuit Cell with PCB, conductor, placement, joining and inspection modules;
- P4 Metaljet Foundry using fictional sealed melt/filter/precision-jet deposition onto an actively supercooled build plate;
- P5 Multi-Material Works as a coordinated cell rather than a magic desktop box;
- P6 Heavy Systems Foundry with large chamber, heavy power/cooling, handling, machining and inspection equipment;
- P7 Sovereign Integration Cell with adapters for captured secure/quantum seed hardware;
- separate upgrade kits for chamber, motion, toolhead, controller, power bus, active cooling, filtration, atmosphere abstraction, safety, material handling, metrology and post-processing;
- ceramic printer/press abstraction;
- composite layup table;
- vacuum bagging/infusion system abstraction;
- honeycomb/cellular structure printer/forming fixtures;
- curing oven/autoclave abstraction;
- electronics pick-and-place/reflow line abstraction;
- wire/cable fabrication bench;
- optics bench;
- clean electronics enclosure;
- parts washer;
- ultrasonic cleaner;
- paint/coating booth;
- shot/blast cleaning cabinet;
- metrology/quality station;
- non-destructive inspection station abstraction;
- prototype quarantine cage;
- destructive-test scrap bins;
- tool holders, fixtures, jigs, dies, molds, build plates, feedstock spools/powders, resin containers, ceramic feed, composite fabric, fasteners, bearings, seals, wire, connectors, lubricants, coolants, cleaning consumables;
- worn, uncalibrated, contaminated, power-starved, damaged, repaired, upgraded, and certified states.

These assets must remain compatible with the existing crafting tree. Do not provide actionable real-world firearm or dangerous chemical/hydrogen manufacturing instructions.

## N. Tactical-companion personal and suit hardware

- personal agent identity/token module;
- hardened agent core;
- local inference accelerator;
- deterministic safety controller;
- secure memory/checkpoint module;
- mission evidence recorder;
- suit sensor-fusion computer;
- power-conditioning module;
- thermal spreader/cold plate;
- shock/vibration cradle;
- shielded enclosure;
- trusted boot module;
- encrypted base/squad mesh module;
- voice/audio processor;
- pilot microphone and speakers;
- haptic cue controller;
- HUD/display interface module;
- cockpit status panel;
- physical confirmation control;
- emergency override and release control;
- agent deployment dock;
- agent backup/transfer cradle;
- diagnostic port and authorized tool;
- quarantine mode indicator;
- compromised/tampered/heat-damaged/memory-damaged/sensor-starved/network-isolated/degraded/repaired/recertified variants.

## O. Exoskeleton agent-integration parts

- head/helmet sensor mount;
- chest compute enclosure;
- spine cable/data trunk;
- hip controller mount;
- arm/leg actuator interface modules;
- joint-state sensors;
- inertial measurement unit;
- foot pressure/contact sensors;
- load cells;
- power-bus interface;
- battery/fuel-cell interface;
- cooling loop interface;
- communications antenna mount;
- camera/thermal/acoustic sensor pods;
- climbing-route sensor module;
- weapon-state data interface owned by weapons;
- drone-control interface;
- evidence recorder;
- emergency limp-home controller;
- manual fallback controller;
- removable companion core cradle;
- service rack, charging stand, calibration frame, fit harness, diagnostic cable set;
- scout, climber, carry, rescue, evasive, combat, and industrial variants.

## P. Pinnacle mech tactical-companion integration

- redundant companion compute bay;
- cockpit-local agent core;
- secondary safety controller;
- armored checkpoint vault;
- sensor-fusion backplane;
- high-bandwidth optical data ring;
- sensor mast computer;
- panoramic optical camera array;
- thermal sensor array;
- acoustic localization array;
- radar/sensing module where canonically supported;
- laser/rangefinding module abstraction;
- navigation and terrain-mapping computer;
- fire-control advisory computer;
- friendly/neutral identification module;
- electronic-support and jamming-detection module;
- counter-drone coordination module;
- squad mesh and base uplink;
- drone-bay control node;
- weapons-interface gateway;
- armor/damage-control computer;
- actuator-health monitoring network;
- power/thermal/ammunition management console;
- cockpit voice, HUD, haptic, and confirmation controls;
- emergency fire suppression and pilot-extraction assistance controller;
- removable mission recorder;
- service, backup, deployment, calibration, and quarantine docks;
- light/scout, urban climber, shield/breacher, fire-support, anti-mech, anti-robotic, command/drone-control, rescue/engineering, and endurance variants.

All sensor and fire-control prompts must enforce authoritative sensing, uncertainty, occlusion, latency, damage, jamming, spoofing, decoys, counterplay, and advisory-by-default lethal authority.

## Q. Field sensors, targeting aids, and test targets

- visible camera family;
- low-light camera;
- thermal camera;
- depth/range sensor abstraction;
- radar module where supported;
- acoustic microphone array;
- vibration/seismic sensor;
- chemical/radiological sensor;
- weather station;
- wind/pressure/temperature sensors;
- inertial/navigation sensors;
- target-designation display/controller;
- range card and physical map aids;
- sensor calibration targets;
- thermal target;
- radar reflector;
- acoustic calibration source;
- moving test target;
- drone target;
- armored test silhouette;
- smoke/occlusion test equipment;
- decoy and spoofing test modules;
- jamming simulator abstraction;
- sensor covers, lenses, windows, wipers, heaters, mounts, cables, and protective housings;
- dirty, scratched, fogged, misaligned, overheated, jammed, spoofed, damaged, repaired, and calibrated states.

## R. Agent-assisted drone parts

- drone agent compute module;
- flight controller;
- deterministic safety controller;
- navigation sensor suite;
- optical/thermal/acoustic payloads;
- communications/datalink module;
- mesh relay payload;
- companion coordination module;
- mission recorder;
- swappable storage;
- battery/fuel-cell/power modules;
- thermal management;
- payload hardpoint;
- suppression payload interface;
- armor panel interfaces;
- countermeasure dispenser abstraction;
- recovery beacon;
- field programming/diagnostic kit;
- launch rack, charging rack, repair cradle, calibration stand, transport case;
- scout, relay, cargo, interceptor, decoy, mapping, recovery, defense, and heavy-lift variants.

Use the existing drone construction/operations/defense skills for flight and combat truth.

## S. Maintenance, repair, calibration, and recovery tools

- general mechanic tool kit;
- electronics tool kit;
- ESD kit;
- cable/connector tool kit;
- fiber termination/inspection kit;
- network diagnostic kit;
- power diagnostic kit;
- cooling-loop service kit;
- leak detection kit;
- thermal-interface service kit;
- rack installation kit;
- lifting handles and server lift;
- hand cart, pallet jack, engine hoist, gantry crane, chain hoist, sling, rack dolly;
- board cleaning kit;
- corrosion removal kit;
- filter service kit;
- fire cleanup kit;
- media recovery kit;
- checkpoint imaging kit;
- trusted firmware programmer;
- calibration kit families;
- exo diagnostic kit;
- mech service cart;
- drone repair kit;
- sensor alignment kit;
- torque, alignment, electrical, optical, thermal, pressure, and flow instruments;
- worn, missing-piece, contaminated, uncalibrated, damaged, improvised, repaired, and complete states.

## T. Consumables, spares, and material lots

- fasteners, rails, brackets, cable ties, labels, seals, tamper labels;
- wire, cable, fiber, connectors, terminals, fuses, breakers;
- solder, flux, braid, wick, heat-shrink, insulation;
- thermal paste, pads, coolant, filters, lubricants, cleaning fluids;
- fan, pump, bearing, seal, valve, regulator, hose, quick-disconnect spares;
- battery cells/modules and approved hydrogen/fuel-cell consumables;
- storage drives, memory modules, controller cards, optical transceivers;
- printer feedstock, build plates, tooling, cutting inserts, abrasives;
- resins, fibers, ceramic feed, metal stock, sheet, plate, bar, tube;
- PPE, gloves, masks, respirator filters, eye/ear protection;
- fire-extinguisher agent containers and fire blankets;
- desiccant, corrosion inhibitor, sealed bags, rugged cases;
- calibration standards and test coupons;
- provenance, grade, contamination, condition, expiration, compatibility, quantity, mass, volume, storage, and salvage variants.

Do not collapse unlike stock into generic `electronics`, `metal`, or `chemicals` where grade changes outcome.

## U. Rooms, structures, furniture, and base services

- scavenged assistant closet;
- secure server room;
- rack row and hot/cold aisle kit;
- power room;
- battery/hydrogen safe room;
- cooling plant room;
- network operations room;
- archive vault;
- checkpoint vault;
- quarantine room;
- electronics lab;
- training/debrief room;
- simulation room;
- research lab;
- metrology lab;
- additive manufacturing room;
- machine shop;
- composite/ceramic shop;
- drone bay;
- exoskeleton service bay;
- mech service/fabrication bay;
- secure design review room;
- evidence ingestion room;
- fire-rated partition, door, window, floor, ceiling, cable penetration, ventilation penetration, drainage, grounding, shielding, access-control, lighting, camera, alarm, suppression, and signage modules;
- workbench, lab table, desk, rack, shelf, cabinet, locker, parts bin, tool chest, stool, chair, monitor arm, cable tray, pallet, cage, cart, crane, platform, catwalk, ladder, service pit, guardrail;
- blueprint, framing, incomplete, operational, damaged, flooded, burned, contaminated, breached, repaired, upgraded, occupied, captured, and salvaged states.

Integrate with building, structural, permissions, power, fire, water, ventilation, traversal, multiplayer, and persistence owners.

## V. Safety, fire, environmental, and incident-response assets

- smoke detector;
- heat detector;
- gas/hydrogen detector;
- coolant/leak detector;
- water-ingress detector;
- fire alarm panel;
- emergency-stop station;
- emergency lighting;
- extinguisher families;
- fire blanket;
- suppression nozzle/tank/control abstraction;
- spill kit;
- absorbent materials;
- eyewash and first-aid station;
- respirator/PPE cabinet;
- grounding and lightning protection;
- ventilation damper;
- emergency exhaust fan;
- isolation switch;
- battery/hydrogen venting and safe enclosure;
- damaged, discharged, expired, obstructed, unpowered, bypassed, sabotaged, inspected, serviced, and active states.

## W. Loot, damaged, faction, captured, and salvage variants

For every family, define controlled variants rather than duplicating arbitrary assets:

- factory/pre-collapse;
- abandoned but sealed;
- exposed/weathered;
- cartel-successor modified;
- militia/clan repaired;
- elite-enclave maintained;
- bunker/sovereign secured;
- improvised field repair;
- stripped/cannibalized;
- burned;
- flooded/wet;
- corroded;
- contaminated;
- impact/ballistic damaged where relevant;
- tampered/compromised;
- counterfeit;
- untrusted firmware;
- partially functional;
- calibrated/certified;
- recertified;
- destroyed salvage.

Use modular state meshes, material instances, decals, removed components, exposed sockets, and metadata rather than making every state a wholly unrelated hero mesh.

## X. Edge Interface, mesh-comms, and cyber-operation assets

Generate prompts and asset-factory jobs for:

- complete Edge Interface device families from damaged recovered unit through clan-built and sovereign hardened variants;
- replaceable enclosure, frame, environmental seals, screen, digitizer, physical controls, haptic module, speaker, microphone, camera, thermal sensor, battery, power-management board, local accelerator, memory, storage, trusted-root, evidence recorder, antenna, shielding, cooling and port boards;
- short-range mesh radio module;
- LoRa-derived low-rate radio module;
- higher-bandwidth local radio module;
- gateway, peer relay, store-and-forward module, portable repeater, mast relay and base gateway;
- directional, omnidirectional, wearable, exo, vehicle, drone and base antennas;
- NFC/RFID, infrared, optical, wired serial/service, GPIO/tool and fictionalized authorized field-interface modules;
- Dolphin-class modular field cyber interface with original DayQ construction and no copied commercial-device identity;
- rugged keyboard/controller, docking cradle, exo dock, mech dock, drone dock, vehicle dock, base-console dock, evidence dock, checkpoint dock, charging stand and repair jig;
- hardware privacy/mute, transmit, confirmation, emergency, quarantine, wipe and disconnect controls;
- channel-status, link-quality, trust, key, alert, scan, target-profile and breach-package interface assets;
- secure key/token cartridge, channel enrollment token, revocation token, captured-device isolation bag/case and forensic adapter;
- cyber reconnaissance kit, authorized diagnostic probe, network test module, protocol adapter, spectrum/link analyzer, signal-direction aid, service cable and target-fingerprint evidence cartridge;
- defensive gateway, segmented controller, data diode, secure boot module, hardware root, biometric controller, lock controller, alarm controller, incident recorder and quarantine appliance;
- fictional Quantum Breach Package cartridge/module, execution controller, hydrogen-cell power-bank interface, quantum-stack link, cooling/power reservation indicators and spent/invalidated physical states;
- like-new, refurbished, field repaired, wet, corroded, cracked-screen, broken-port, weak-radio, damaged-antenna, battery-swollen, storage-corrupted, compromised, spoofed, quarantined, wiped, captured, revoked, repaired, recertified and destroyed-salvage variants.

Compose with `DAYQ_EDGE_INTERFACE_MESH_COMMS_AGENTIC_CYBERWARFARE_AND_QUANTUM_BREACH_HANDOFF_PROMPT.md`. Physical assets expose modules and states; communications, cyber, quantum, lock/gate, hydrogen, authority and persistence systems own their behavior and transactions.

## Y. Glentech universal manufacturing and standardized component assets

Compose with `DAYQ_ROOT_COMPONENTS_STANDARDIZED_SALVAGE_AND_GLENTECH_ADDITIVE_MANUFACTURING_HANDOFF_PROMPT.md` and generate prompts/jobs for:

- twelve root-material families in representative raw, processed, packaged, contaminated, degraded and certified forms;
- twenty-four standardized part families across common, technical, precision, secure and sovereign bands;
- household, school, garage, Battle Circuit, field-repaired, clan-foundry, industrial and sovereign-adapted Glentech machine variants;
- R0-R5 reclamation assets including sorted salvage, cleaning/preparation stations, salvage forge, controlled foundry, materials lab and strategic-material qualification equipment;
- ferrous ingots/billets, light-alloy ingots, copper stock, conductor micro-ingots, mixed precious-metal concentrate, qualified silver/gold micro-ingots and their molds, labeled storage, contaminated, cracked, mixed-grade and certified variants;
- polymer flake, pellets, rods, spools, standardized feedstock bricks, drying/compounding equipment and separated polymer-family storage;
- P0-P7 distinct printer/cell models with visibly increasing chamber, toolhead, power, cooling, filtration, feedstock, electronics, metrology, material-handling and service infrastructure;
- Thermal-Gradient Jet Deposition assets: sealed ingot cassette, melt/metering unit, filter, replaceable jet head, actively supercooled build plate, cooling loop, oxidation-control abstraction, thermal cameras, shielding/interlocks, waste capture and post-processing fixtures;
- machine frame, enclosure, motion system, rails, bearings, drives, bed, chamber, tool changer, feedstock handling, controller, compute, storage, display, camera, sensors, ventilation, filtration, fire response, waste capture and service panels;
- polymer, elastomer, resin, fiber/composite, ceramic, conductive, dielectric, PCB, pick-and-place, reflow, wiring, metal, subtractive, inspection, curing and printed-electronics/microfabrication modules;
- feedstock cartridges, spools, powders/pastes as safe abstractions, plates, stock, inserts, calibration targets, test coupons, filters, cleaning and process consumables;
- deconstruction benches, sorting bins, cleaning/testing stations, recyclers, material identifiers and salvage containers;
- child-machine kit, printed controller package, open firmware/design archive, trusted machine identity and calibration certificate;
- damaged, stripped, worn, contaminated, wet, corroded, burned, miscalibrated, compromised-firmware, repaired, reproduced, upgraded and certified states.

Every tier change must be visually meaningful. Do not reuse one printer or furnace mesh with only a different tier label. For the early forge, show the chosen body, powered blower or manual bellows, air pipe and basic operating states. Keep detailed component simulation focused on printers and advanced production equipment rather than every internal forge part.

The asset prompt must distinguish visible shared parts from data-level grades and ratings. Do not create hundreds of nearly identical loose-part meshes. Use modular representative geometry, stacked/containerized presentations, metadata, shared materials and assembly state changes.

# Assembly catalog

In addition to individual assets, generate assembly prompts and validation jobs for:

1. T0 scavenged data-recovery bench.
2. T1 local assistant workstation.
3. T1 secure archive and quarantine corner.
4. T2 agent training rack.
5. T2 exoskeleton copilot deployment station.
6. T2 field evidence ingestion and debrief station.
7. T3 certified specialist-agent cluster.
8. T3 electronics and sensor calibration lab.
9. T3 combat-exo tactical-companion suite.
10. T3 drone-agent design and flight-test cell.
11. T4 multi-agent research cell.
12. T4 AI-assisted additive/honeycomb design lab.
13. T4 secure robotics fabrication cell.
14. T4 tactical-companion training and adversarial evaluation range.
15. T4 sovereign checkpoint vault and deployment service.
16. T5 mech tactical-companion compute/sensor suite.
17. T5 mech battle-evidence/debrief/research loop.
18. T5 full agent-supported mech fabrication and service bay.
19. T5 captured enclave Quantum ASIC restoration lab.
20. T5 sovereign research lattice.
21. T6 coherent discovery complex, retained as proposed/testing until evidence supports implementation.

Each assembly prompt must include:

- bill of materials and component references;
- room/structure and clearance;
- construction stages;
- transport/lifting requirements;
- power, heat, cooling, network, storage, security, and fire budgets;
- interfaces and compatibility;
- operators/specialists;
- partial/degraded operation;
- hazards and sabotage points;
- maintenance access;
- repair and salvage;
- multiplayer permissions and queues;
- persistent state and crash recovery;
- visual state changes as the assembly becomes operational;
- live end-to-end gameplay test.

# Family-specific prompt rules

## Electronics and compute prompt rule

Name boards, chips, connectors, storage, shielding, cooling contact, retention, indicators, service tools, firmware/trust identity, ESD risk, power rails, heat, failure zones, and replacement process. Condition must affect stability, throughput, latency, memory errors, bandwidth, power, heat, and trust—not only texture wear.

## Rack and room prompt rule

Specify standard dimensions or declared original standards, rail/mount compatibility, floor load, anchoring, cable routing, airflow direction, blanking, filter access, power distribution, grounding, fire separation, door swing, maintenance clearance, noise, heat, lighting, security, navigation, construction stages, and damaged/partial operation.

## Power prompt rule

Specify voltage/current class, input/output curve, conversion losses, power quality, peak/sustained load, protection, grounding, heat, fuel/energy source, startup/shutdown, isolation, overload, short, ingress, repair, and safe restart. Integrate with the authoritative energy model.

## Cooling prompt rule

Specify heat-transfer role, capacity range, flow/air path, pumps/fans, filters, fluid, pressure, temperature, condensate, leak paths, freeze state, clogging, noise, power, controls, alarms, service procedure, and degraded output.

## Security prompt rule

Specify physical root, identity, keys/tokens, tamper boundaries, tool permissions, audit, failure state, capture, quarantine, revocation, repair/recertification, and what is physically exposed. Do not use an unbreakable magic lock.

## Training/research prompt rule

Specify what evidence enters, who approves it, compute/time/power/cooling consumed, evaluator/tool connections, intermediate artifacts, failure and contradiction states, physical operator actions, UI feedback, persistence, and output lineage. Do not represent training as a single glowing progress bar.

## Tactical-companion prompt rule

Specify original identity presentation, local compute, checkpoint/memory storage, sensor and tool permissions, power/heat/bandwidth, suit mounting, voice/HUD/haptics, pilot confirmation, degraded/offline/emergency/quarantine behavior, evidence recording, backup/transfer/capture, and authoritative multiplayer rules. Visual design must communicate capability and damage without implying unexplained omniscience.

## Quantum prompt rule

Specify the classical control stack, timing, shielding, interconnect, cooling, calibration, trusted root, service access, specialist tools, power, failure, and fictional workload. Label fictional capability. No generic magic cube and no universal decryption.

# Design-family visual direction

Create a coherent visual language across tiers:

- **T0–T1:** recognizable salvaged consumer, industrial, telecom, lab, military-surplus, and enterprise hardware; mismatched repairs; exposed adapters; written labels; scarce environmental sealing.
- **T2–T3:** standardized clan frames, repaired racks, modular panels, color-coded services, field-service clearances, guarded cables, printed replacement brackets, practical warning systems.
- **T4:** secure robotics and research infrastructure with redundant buses, shielded enclosures, disciplined cable routing, calibrated sensors, evidence labels, service documentation, and higher material quality.
- **T5:** rare sovereign/enclave/bunker hardware integrated with clan-manufactured adapters; dense but functional; advanced thermal, optical, trusted, and sensor systems; visible logistical burden.
- **T6:** original DayQ coherent research technology whose visual complexity derives from timing, shielding, interconnect, calibration, cooling, power, and service—not decorative luminescence.

Create faction variants through repair doctrine, materials, connectors, labeling, security, weathering, and component selection. Do not reduce factions to paint colors.

# Raw-material, repair, and salvage requirements

Every craftable or repairable entry must trace:

`source -> extraction/recovery -> transport -> sorting -> cleaning -> processing -> part -> assembly -> calibration -> certification -> field use -> diagnosis -> repair/replacement -> salvage`

Require material grades, lot condition, contamination, provenance, accepted substitutions, substitution penalties, workstations, tool capability, specialists, power quality, environment, stages, interruptions, failure, byproducts, quality rules, repair recipe, and salvage rule.

Examples of meaningful dependencies include:

- scrap steel/aluminum/copper -> sorted/cleaned stock -> sheet/bar/wire -> brackets, racks, busbars, cases, heat sinks;
- recovered boards -> inspection/cleaning/rework -> verified chips/controllers/connectors -> compute modules;
- glass/optics/electronics -> sensor modules;
- polymer feedstock and recovered plastic refinement -> housings, cable insulation, ducts, fixtures, additive parts;
- silica/ceramic/composite chains -> insulation, substrates, armor-adjacent enclosures, thermal/electrical parts;
- water, electrolyzer, certified pressure hardware, controls, safe storage -> hydrogen/fuel-cell energy chain;
- filters, pumps, fans, radiators, tubing, valves, sensors -> cooling and clean-air chains;
- trusted recovered roots, inspected secure boards, controlled firmware, secure workstations -> trusted compute;
- precision timing, photonics, advanced controllers, shielding, cooling, calibration -> Quantum ASIC stack.

Knowledge unlocks permission to attempt a build. It does not replace matter, machines, power, expertise, tolerances, inspection, or certification.

# Batch-generation workflow

For each catalog family:

1. Inspect current DayQ items, recipes, assets, schemas, skills, and owners.
2. Reuse existing stable identities where compatible.
3. Create or update catalog entries.
4. Expand assemblies into components and shared parts.
5. Topologically sort dependencies.
6. Decide `common_baseline`, `recovered_2058`, `original_dayq`, or `fictional_quantum`.
7. Choose a lawful source/reference route.
8. Invoke `$generate-dayq-systemic-asset-prompts` for each entry.
9. Create the asset-factory job seed.
10. Create the crafting/repair/salvage references through the existing owner.
11. Batch only independent jobs with shared visual-contract inputs locked.
12. Run img2threejs for suitable hard-surface prototypes.
13. Promote accepted prototypes or approved references through Blender MCP.
14. Integrate each item or assembly through Unreal MCP.
15. Validate interfaces in the full assembly, not only in an empty asset viewer.
16. Record failures, repairs, hashes, and final dispositions.
17. Update the no-skip ledger.

Never generate hundreds of visually isolated props without first locking shared dimensions, connector standards, rack units, cable families, mounting systems, material libraries, state conventions, and gameplay metadata.

# Completeness and acceptance gates

Do not mark this handoff complete unless:

1. the new native skill and all required references/assets/scripts validate;
2. every minimum catalog entry has a stable ID, family, tier, owner, route, dependency, repair/salvage reference, and acceptance route;
3. every assembly resolves to obtainable components and services;
4. no ordinary build-DAG cycles or orphan dependencies remain;
5. common objects use cleared baseline references where helpful and are canonically customized;
6. original/futuristic objects remain original DayQ designs with plausible support systems;
7. every external reference has rights, provenance, hash, quarantine, and intended-use records;
8. environmental channels are explicitly classified for every family;
9. every prompt replaces generic statements with item-specific observable requirements;
10. every physical object has dimensions, mass, material regions, components, interfaces, states, damage, repair, transport, collision, LOD, and metadata appropriate to its role;
11. every digital-bearing object has capacity, interface, provenance, trust, corruption, ingestion, identity, hash/lineage, and persistence;
12. every powered object has power, heat, cooling, grounding/protection, fault, ingress, isolation, repair, and safe-restart behavior;
13. every craftable object traces to raw materials, workstations, tools, specialists, power, stages, quality, failure, repair, and salvage;
14. every agent/companion/quantum object respects training, certification, trust, sensor, authority, security, and evidence boundaries;
15. no real-world weapon CAD, dangerous chemical recipe, or unsafe pressure/hydrogen construction instruction is generated;
16. img2threejs assets pass every locked visual stage when that route is selected;
17. Blender assets pass scale, topology, UV, materials, LOD, collision, sockets, pivots, state, damage, repair, naming, and export gates;
18. Unreal assets pass interaction, assembly, environment, collision, replication, persistence, migration, crash-recovery, performance, and live gameplay gates;
19. partial assemblies and degraded states remain understandable and playable;
20. large-clan throughput does not create free or irreversible technology monopolies without upkeep, exposure, capture, sabotage, and counterplay;
21. asset generation is traceable from request through hashes and evidence;
22. blocked live gates are reported honestly rather than inferred from prose or compilation.

# Required integrated proof route

Demonstrate at least this connected route:

1. Recover a damaged assistant, archive media, server components, power/cooling parts, and manuals.
2. Transport them under physical inventory constraints.
3. Search/select cleared common-object visual references.
4. Generate systemic prompts and asset-factory jobs.
5. Reconstruct suitable baseline props through img2threejs.
6. Produce and repair the full assets in Blender.
7. Import and validate them in Unreal.
8. Build a T1 assistant workstation from traceable materials and repaired components.
9. Add secure storage, networking, power, cooling, fire response, and quarantine.
10. Restore, train, evaluate, and certify an agent using physical terminals, media, racks, and tools.
11. Build an exoskeleton companion module and deployment station.
12. Deploy the companion, collect signed field evidence, and return it to the debrief station.
13. Upgrade to an A4 research/design/fabrication cell.
14. Generate and physically test a cellular drone, armor-adjacent, cooling, sensor, or mech component candidate.
15. Reject at least one simulated design through physical evidence.
16. Qualify and manufacture a surviving revision.
17. Integrate a veteran companion into a pinnacle mech sensor/compute suite.
18. Validate target assistance, jamming/counterplay, damage, power/cooling degradation, checkpoint backup, capture, repair, persistence, and multiplayer authority.
19. Recover and restore one Quantum ASIC stack component without treating it as magic.
20. Restart/crash/migrate during asset jobs, training, research, fabrication, suit deployment, evidence transfer, and repair while proving no duplication.

# Required deliverables

Produce:

1. the new native skill with `agents/openai.yaml`;
2. complete catalog reference;
3. family prompt contracts;
4. assembly/interface contracts;
5. route matrix;
6. validation matrix;
7. catalog and batch-job schemas;
8. validated catalog and batch-expansion scripts;
9. stable-ID catalog manifest covering every minimum entry;
10. dependency and assembly graphs;
11. one complete production prompt and job seed per catalog entry;
12. source/reference/provenance plans;
13. raw-material/recipe/repair/salvage references;
14. shared connector, mount, rack, cable, material, state, and metadata standards;
15. Blender and Unreal work orders;
16. automated and live test matrices;
17. integrated proof evidence;
18. overlap/ownership map against existing DayQ systems;
19. no-skip-ledger updates;
20. manifest, validators, hashes, unresolved questions, blocked gates, and final acceptance report.

# Completion report

Report:

- exact skill and catalog artifacts created;
- catalog totals by family, tier, route, and disposition;
- existing identities reused and conflicts reconciled;
- source/reference decisions and provenance;
- prompts and job seeds generated;
- shared assemblies and interface standards;
- crafting/repair/salvage dependencies;
- img2threejs, Blender, and Unreal evidence;
- replication, persistence, migration, crash-recovery, performance, and exploit results;
- missing, failed, rejected, waived, or blocked entries with reasons;
- final acceptance status.

Do not say “all assets are designed” when only a list exists. Do not say “production ready” when prompts or meshes exist but Unreal gameplay evidence does not. Do not let an image substitute for simulation. Do not let a fictional technology avoid physical support. Do not let an agent produce free designs or items. Preserve one traceable lineage from every catalog requirement to the accepted DayQ asset.
