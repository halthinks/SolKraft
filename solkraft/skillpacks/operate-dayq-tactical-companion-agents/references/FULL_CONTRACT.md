# DayQ 2058 Agent Training, Tactical Companions, Autonomous Research, Quantum Infrastructure, and AI-Assisted Design — Complete Handoff Prompt

Continue the existing DayQ design and implementation with trained agents and physical agent infrastructure as a first-class progression pillar.

This is a prompt and handoff for the primary DayQ task. Do not implement these skills in the source handoff workspace. Do not assume filesystem locations. Inspect the current DayQ workspace and use its established project-relative conventions.

Keep this work DayQ-only. Do not include, modify, merge, delete, or repurpose the separate wave-surfing project.

# User-locked canon and direction

The playable year is **2058**, twenty-eight years after the Hearthline/global cryptographic collapse.

The user has directed that software agents be a major gameplay and development domain.

Agents must:

- exist as recoverable, trainable, configurable, persistent capabilities rather than automatic menu bonuses;
- require models/checkpoints, knowledge, data, human demonstrations, evaluation, compute, memory, storage, networking, power, cooling, tools, sensors, and secure infrastructure;
- improve through explicit training and upgrading;
- specialize into useful disciplines;
- accelerate and optimize research, design, production, repair, logistics, defenses, drones, armor, exoskeletons, mechs, communications, power, water, medicine, agriculture, quantum systems, and other DayQ domains;
- unlock AI-assisted design branches including advanced additive manufacturing, 3D-printed game-defined weapon systems, honeycomb/cellular structures, advanced drones, advanced armor, new materials, robotics, and higher-tier quantum development;
- gain more capable planning, orchestration, self-evaluation, simulation, experiment, and auto-research loops when better infrastructure is installed;
- depend on infrastructure such as processors, accelerators, Quantum ASIC stacks, memory, storage, secure roots, interconnects, network services, power supplies, UPS/buffer systems, generators, hydrogen/fuel-cell systems, cooling, server racks, sensors, laboratories, printers, CNC/press/composite/ceramic/electronics facilities, and protected bases;
- remain vulnerable to poor training, bad data, compromised checkpoints, malicious documents, tool failures, sabotage, power instability, cooling failure, drift, overconfidence, weak evaluation, capture, theft, and hostile agents;
- create powerful late-game automation without making players, human specialists, field missions, experimentation, resource logistics, or judgment irrelevant.

These are locked creative requirements. Exact balance, timing, autonomy boundaries, and runtime architecture remain evidence-gated.

# Required six-skill architecture

Create and integrate these six coordinated native DayQ skills:

1. `DAYQ_AGENT_COMPUTE_POWER_COOLING_AND_QUANTUM_INFRASTRUCTURE_SKILL`
   - native folder: `build-dayq-agent-infrastructure`
2. `DAYQ_AGENT_TRAINING_CURRICULA_EVALUATION_AND_SPECIALIZATION_SKILL`
   - native folder: `train-dayq-agents`
3. `DAYQ_MULTI_AGENT_ORCHESTRATION_AUTORESEARCH_AND_DISCOVERY_SKILL`
   - native folder: `orchestrate-dayq-agent-research`
4. `DAYQ_AI_ASSISTED_DESIGN_SIMULATION_AND_MANUFACTURING_SKILL`
   - native folder: `design-dayq-with-agents`
5. `DAYQ_AGENT_SECURITY_TRUST_GOVERNANCE_AND_COUNTER_AGENT_SKILL`
   - native folder: `secure-dayq-agent-systems`
6. `DAYQ_EMBODIED_TACTICAL_COMPANION_AND_COMBAT_LEARNING_SKILL`
   - native folder: `operate-dayq-tactical-companion-agents`

Also integrate the separate production-support adapter defined by `DAYQ_AGENT_SYSTEMS_COMPLETE_ASSET_CATALOG_AND_PRODUCTION_HANDOFF_PROMPT.md`:

- `DAYQ_AGENT_SYSTEM_ASSET_CATALOG_AND_PROMPT_ROUTER_SKILL`
- native folder: `generate-dayq-agent-system-assets`

This adapter is not a seventh gameplay-system owner. It enumerates every required physical/digital asset and routes each entry through the existing systemic prompt generator, source/reference pipeline, img2threejs when suitable, Blender MCP production, raw-material/recipe owners, and Unreal MCP acceptance. Use it to prevent the six gameplay skills from leaving required machines, parts, rooms, tools, media, interfaces, repair objects, or suit hardware undefined.

Also integrate the four-system amendment defined by `DAYQ_EDGE_INTERFACE_MESH_COMMS_AGENTIC_CYBERWARFARE_AND_QUANTUM_BREACH_HANDOFF_PROMPT.md`:

- `operate-dayq-edge-interfaces`;
- `build-dayq-mesh-comms`;
- `conduct-dayq-cyber-operations`;
- `conduct-dayq-quantum-breaches`.

The Edge Interface is the player's persistent portable local-agent host and universal exo/mech/drone/infrastructure communications interface. All exos may consume its assistance through compatible hardware, while cyber and quantum effects remain abstract, server-authoritative, target-specific, costly, counterable, and isolated from real player networks. Software PQC and hardware-rooted PQC must remain distinct; certified on-chip roots close the direct quantum-cryptanalytic route.

Every skill must contain:

- `SKILL.md` with YAML frontmatter containing only `name` and `description`;
- `agents/openai.yaml` with matching display metadata and a default prompt naming its native `$skill-name`;
- directly linked references for full contracts and test matrices;
- an explicit dependency and ownership map;
- Unreal MCP guidance;
- multiplayer, persistence, migration, exploit, security, privacy, performance, and evidence gates;
- scripts only when deterministic graph, training, evaluation, research, infrastructure, economy, or evidence validation benefits;
- no auxiliary README or installation guide inside the native skill folder.

# Skill ownership

## Skill 1 — compute, power, cooling, and quantum infrastructure

Own:

- physical agent-compute infrastructure;
- CPUs, GPUs, NPUs, classical ASICs, memory, storage, networking, interconnects, server chassis/racks, power supplies, UPS/buffer systems, generators, hydrogen/fuel cells, cooling, filtration, environmental control, sensors, secure roots, consoles, and maintenance;
- fictional sovereign Quantum ASIC accelerators and their classical control stack;
- compute capacity, memory, bandwidth, storage, power quality, power draw, heat, cooling, reliability, redundancy, latency, secure execution, maintenance, and infrastructure progression;
- construction recipes, component compatibility, room/building requirements, workstations, repair, salvage, logistics, sabotage, hazards, and performance allocation;
- data-center/server-room layouts and physical base integration.

Do not own training outcomes, agent policy, research logic, design acceptance, or security decisions beyond the infrastructure state they consume.

## Skill 2 — training, curricula, evaluation, and specialization

Own:

- agent model/checkpoint identity and provenance;
- curricula;
- datasets;
- recovered archives;
- books/manuals/scientific literature;
- human demonstrations;
- field telemetry;
- simulation data;
- synthetic data;
- tool-use training;
- memory formation;
- fine-tuning/distillation/adaptation abstractions;
- domain competence;
- uncertainty calibration;
- evaluator suites;
- certification;
- drift detection;
- retraining;
- specialization and cross-domain transfer;
- trainer/specialist gameplay;
- training jobs, costs, failures, persistence, and progression.

Do not own compute allocation, research orchestration, manufacturing output, or security policy. Consume their interfaces.

## Skill 3 — multi-agent orchestration, auto-research, and discovery

Own:

- planner, decomposer, researcher, simulator, experimenter, critic, verifier, safety reviewer, fabrication coordinator, field analyst, archivist, and integrator roles;
- task graphs;
- planning horizons;
- parallelism;
- hypothesis generation;
- experiment selection;
- simulation queues;
- evidence gathering;
- independent criticism;
- uncertainty reduction;
- research milestones;
- auto-research loops;
- stopping rules;
- human approval gates;
- research failures and recovery;
- discovery provenance;
- reusable research knowledge;
- theory-to-prototype-to-field-feedback loops.

Do not directly create items, alter inventory, mutate manufacturing output, or authorize weapon use. Produce approved design/research artifacts through established owners.

## Skill 4 — AI-assisted design, simulation, and manufacturing

Own:

- conversion of approved research into versioned design candidates;
- geometry, topology, material, process, component, control, and assembly optimization abstractions;
- digital twins;
- virtual testing;
- design-space exploration;
- generative alternatives;
- manufacturability checks;
- tolerance and quality requirements;
- failure-mode review;
- toolpath/job abstraction;
- prototype work orders;
- measurement feedback;
- certification evidence;
- release, revision, rollback, and retirement of designs;
- agent-assisted designs for drones, armor, honeycomb/cellular structures, additive-manufactured parts, exos/mechs, utilities, electronics, and game-defined weapon systems.

Do not bypass the existing raw-material, recipe, manufacturing, inventory, weapons, armor, drone, exo, mech, building, damage, or validation owners. An agent design is not a crafted item and not production-ready until physical validation passes.

## Skill 5 — security, trust, governance, and counter-agent systems

Own:

- trust zones;
- model/checkpoint provenance;
- dataset provenance;
- tool permissions;
- sandboxing;
- secure roots;
- agent identity;
- delegation boundaries;
- approval policies;
- audit logs;
- anomaly detection;
- evaluation integrity;
- malicious/compromised agent states;
- data poisoning abstraction;
- prompt/document injection abstraction;
- checkpoint tampering;
- tool misuse;
- secret leakage;
- sabotage;
- model theft;
- quarantine;
- rollback;
- re-certification;
- hostile agent/counter-agent gameplay;
- safety and rules for weapon, defense-grid, drone, quantum, infrastructure, and strategic decisions.

Do not create a second clan-permission, post-quantum identity, communications-security, persistence, moderation, or anti-cheat owner. Extend them.

## Skill 6 — embodied tactical companion and combat learning

Own:

- the original DayQ tactical-companion fantasy inside top-tier exoskeletons and mech suits;
- a persistent named agent identity, voice/personality profile, pilot trust, doctrine, mission memory, certifications, and deployable checkpoint;
- suit-local perception fusion from authorized optics, acoustic sensors, radar, thermal systems, suit condition, maps, communications, drones, and squad data;
- target detection assistance, classification, uncertainty, track continuity, threat prioritization, range/wind/lead solution presentation, friendly/neutral protection, and pilot-facing warnings;
- route, cover, vertical-access, heat, power, ammunition, damage, retreat, recovery, and maintenance recommendations;
- after-action recording, combat-evidence curation, replay, debrief, training-credit calculation, and transfer into the base training/research stack;
- pilot-agent coordination, learned preferences, bounded adaptation, emergency assistance, degraded/offline behavior, and backup/restore rules;
- battlefield-derived design hypotheses for armor, sensors, countermeasures, weapons, ammunition interfaces, mobility, cooling, drones, and suit components;
- competitive fairness, counterplay, telemetry provenance, anti-farming, privacy, security, multiplayer authority, persistence, and validation for the companion loop.

Do not own weapon firing, hit determination, damage, inventory, suit assembly, sensor truth, agent training infrastructure, research approval, design acceptance, crafting, or fabrication. Consume those authoritative systems. The agent may propose and assist; it may not create hidden information, fire without the approved control doctrine, grant a finished schematic, or directly manufacture anything.

## Shared boundary

No skill may duplicate:

- item/component identity;
- inventory/crafting transactions;
- power/water/network state;
- model/checkpoint identity;
- agent identity;
- training job state;
- research job state;
- design revision identity;
- manufacturing work orders;
- weapon authorization;
- clan permissions;
- persistence journals;
- migrations.

The tactical-companion skill additionally composes around the existing exoskeleton, mech, weapon, ballistics, damage, drone, communications, traversal, AI, sensory-perception, multiplayer-authority, persistence, economy, crafting, and fabrication owners. It may add agent-specific records and interfaces, but it must not replace their state or rules.

# Science-fiction doctrine

## Agents are not magic

Agent capability derives from a complete stack:

`model architecture + weights/checkpoint + training corpus + domain memory + tool adapters + evaluator quality + orchestration + compute + memory + storage + interconnect + power + cooling + secure hardware + laboratory/fabrication access + real-world measurements + human direction`

Removing or degrading any part changes what the agent can do.

Do not use one abstract “AI level” as the sole source of capability.

## Quantum does not equal intelligence

Quantum hardware accelerates selected workloads. Classical systems still host agent cognition, memory, tools, coordination, persistence, and most simulation.

In DayQ, a **Quantum ASIC stack** is survivor shorthand for a rare integrated sovereign accelerator complex combining:

- specialized quantum/coherent processing tiles;
- classical error-correction and control ASICs;
- photonic/high-speed interconnects;
- trusted post-quantum roots;
- precision timing;
- cryogenic or advanced thermal support according to recovered technology tier;
- calibration sensors;
- classical scheduling/compiler services;
- secure memory and audit hardware.

This is fictional 2058 technology descended from the clandestine sovereign infrastructure that triggered the collapse. It must remain physical, scarce, power intensive, calibration sensitive, failure prone, and difficult to reproduce.

Quantum stacks may accelerate:

- constrained optimization;
- materials and molecular simulation abstractions;
- quantum-system design;
- route/schedule/resource optimization;
- uncertainty sampling;
- selected cryptographic/secure-system analysis;
- quantum sensor interpretation;
- large design-space branch search;
- error-correction research;
- suppression-field modeling.

They do not grant unlimited knowledge, perfect prediction, free decryption of post-quantum hardware, or spontaneous general intelligence.

# Agent progression

Use physical capability bands rather than character level.

## A0 — inert archives and broken assistants

- corrupted model shards;
- encrypted or locked checkpoints;
- damaged consumer assistants;
- appliance agents;
- manuals and offline corpora;
- partial embeddings/memory stores;
- old inference devices;
- unknown provenance;
- severe tool, context, and reliability limitations.

Players can inspect, recover, trade, quarantine, or destroy these assets.

## A1 — local assistant

- one repaired classical compute node;
- narrow recovered model;
- small curated corpus;
- local text/diagram interface;
- inventory/manual search;
- checklist generation;
- basic diagnosis suggestions;
- no autonomous tool execution by default;
- frequent uncertainty and verification needs.

This tier appears early and helps players understand the system.

## A2 — trained domain apprentice

- better compute/memory/storage;
- human demonstrations;
- tool adapters;
- domain curriculum;
- evaluator suite;
- bounded workbench access;
- persistent domain memory;
- repair, logistics, agriculture, medicine, construction, electronics, communications, drone, armor, or other specialization;
- supervised job decomposition and optimization.

An apprentice accelerates known work but rarely creates reliable new designs.

## A3 — certified specialist agent

- larger/repaired model or ensemble;
- high-quality domain data;
- simulator access;
- calibrated uncertainty;
- independent validation set;
- better tools;
- stable power/cooling;
- certified procedures;
- reliable scheduling and process optimization;
- bounded design modifications;
- explicit deployment envelope.

Multiple specializations may exist, but no agent is automatically expert in every domain.

## A4 — multi-agent research cell

- planner/decomposer;
- domain researchers;
- simulation agents;
- experiment designer;
- critic/red-team agent;
- safety/manufacturing reviewer;
- evidence archivist;
- integrator;
- parallel compute and queues;
- laboratory/fabrication interfaces;
- hypothesis → simulation → experiment → prototype → measurement → revision loop;
- human milestone approvals.

This tier unlocks genuine research and novel but bounded designs.

## A5 — sovereign research lattice

- redundant secure racks;
- high-speed interconnect;
- large model ensemble;
- persistent causal/world models;
- extensive validated archives;
- multiple physical laboratories;
- automated measurement;
- advanced fabrication;
- independent verification agents;
- secure supply-chain tracking;
- field telemetry;
- classical accelerator clusters;
- one or more recovered Quantum ASIC stacks;
- long-horizon portfolio planning;
- continuous but bounded auto-research.

This is a strategic clan asset comparable to an elite enclave, bunker, or mech industry.

## A6 — coherent discovery complex

This is a theoretical late-game DayQ system, not guaranteed production canon until prototyped and accepted.

It may combine:

- multiple sovereign research lattices;
- geographically separated secure compute;
- quantum/coherent accelerators;
- trusted physical roots;
- agent-to-agent proof/evidence exchange;
- automated replication of experiments across independent labs;
- formal design invariants;
- uncertainty-driven research allocation;
- live digital twins of bases, fleets, production, and environments;
- secure embodied agents operating drones/robots and test facilities;
- self-repairing orchestration that can replace failed agents without rewriting trust policy;
- strategic discovery portfolios spanning materials, energy, robotics, medicine, agriculture, communications, armor, quantum systems, and suppression.

A6 must still consume enormous power, cooling, components, time, specialists, secure sites, raw materials, experiments, and maintenance. It must have shutdown, isolation, audit, and human/clan governance.

# Original theoretical agentic unlocks

Create original DayQ names and mechanics. Candidate unlocks include:

## Evidence Weave

Agents share claims only with source lineage, uncertainty, test state, and contradiction links. This reduces repeated mistakes and unlocks reliable cross-domain research.

## Skeptic Loop

Every proposal is attacked by an independent critic agent that does not share the proposer’s working memory. Disagreement creates tests rather than being averaged away.

## Causal Forge

Agents build causal models from controlled experiments and field telemetry, improving diagnosis and reducing correlation-driven design failures.

## Counterfactual Foundry

The system explores alternative materials, components, routes, and failure conditions in digital twins before consuming rare physical resources.

## Proof-Carrying Fabrication

Every released design includes machine-readable prerequisites, assumptions, material grades, tolerances, hazard controls, predicted failure envelope, test evidence, and rollback route. Workstations reject missing or incompatible proof packages.

## Embodied Replay

Drone, robot, exo, mech, workshop, and field telemetry becomes replayable training/evaluation evidence. Agents learn from real failures without automatically trusting every sensor.

## Adversarial Twin

A hostile evaluator attempts to break designs, schedules, permissions, and assumptions in simulation before release. It cannot alter production systems.

## Tool Genesis

Agents may propose new tool adapters or automation routines, but a sandbox, evaluator, code review, permission review, and live bounded test are required before activation.

## Context Federation

Specialist agents exchange compact verified knowledge packets rather than dumping unrestricted memory, improving scale while preserving domain boundaries and secrecy.

## Research Portfolio Mind

The lattice allocates compute, laboratory time, materials, and specialists across competing hypotheses based on expected information gain, strategic value, risk, and resource scarcity.

## Quantum Branch Search

A Quantum ASIC accelerates selected combinatorial or quantum-domain searches. Results remain hypotheses requiring classical verification and physical testing.

## Lattice Self-Healing

The orchestrator detects failed, drifting, compromised, or overloaded agents and transfers work to certified replacements while preserving immutable audit lineage and human policy.

## Sovereign Toolchain

The agent complex can operate entirely offline through locally hosted models, data, tools, simulators, manufacturing systems, and post-quantum-secured identity.

These unlocks must create observable gameplay, infrastructure, resource, risk, and validation differences—not decorative research-tree names.

# Agent identity and capability model

Every agent instance must define:

- persistent identity;
- model/checkpoint family and revision;
- architecture/capability class;
- parameter/capacity band abstraction;
- quantization/compression state where relevant;
- provenance;
- license/ownership abstraction where canonically relevant;
- trust/security state;
- domain competencies;
- tool competencies;
- planning horizon;
- context/memory capacity;
- persistent memory stores;
- uncertainty calibration;
- evaluator performance;
- autonomy class;
- allowed tools;
- allowed data;
- allowed networks;
- allowed workstations;
- allowed mission/domain scopes;
- latency;
- compute requirement;
- memory/storage requirement;
- power/heat profile;
- failure/drift history;
- training/certification history;
- owner/clan/permissions;
- deployment state;
- compromise/quarantine state.

Do not reduce all this to intelligence points.

# Infrastructure stack

## Compute

Support:

- salvaged consumer CPUs/GPUs/NPUs;
- workstation accelerators;
- server accelerators;
- industrial inference ASICs;
- robotics/control ASICs;
- secure compute modules;
- recovered enclave/bunker systems;
- classical control processors;
- Quantum ASIC/coherent accelerator tiles;
- heterogeneous scheduling.

Compute affects concurrency, model size/capability, context, simulation fidelity, training rate, research throughput, latency, and power/heat.

## Memory and storage

Support:

- volatile memory;
- accelerator memory;
- local solid-state storage;
- archival storage;
- redundant arrays;
- secure stores;
- dataset repositories;
- checkpoint stores;
- vector/knowledge stores;
- experiment/evidence archives;
- backup and immutable audit media;
- corruption, wear, capacity, bandwidth, and recovery.

Larger storage does not create better knowledge unless data is curated, indexed, compatible, and trusted.

## Interconnect and networking

Support:

- board/rack interconnect;
- base intranet;
- secure service network;
- storage network;
- laboratory control network;
- mesh/radio gateways for compact field telemetry;
- high-bandwidth local links;
- post-quantum-rooted trust;
- segmented/quarantined zones;
- offline operation;
- bandwidth, latency, congestion, partition, and compromise.

Do not place unrestricted agent control on public or untrusted networks.

## Power

Support:

- grid/microgrid input;
- generators;
- plastic-derived fuel generation;
- solar/wind/hydro where available;
- batteries;
- hydrogen/fuel-cell systems;
- UPS/buffer systems;
- conditioned power;
- redundant feeds;
- load priority;
- brownouts;
- overload;
- grounding/short/fire abstractions;
- consumption metering;
- shutdown and safe checkpoint.

Training, simulation, and quantum acceleration are interruptible high-load jobs. Bad power can corrupt work, damage hardware, or force rollback.

## Cooling and environment

Support:

- airflow;
- liquid cooling abstraction;
- heat exchangers;
- pumps/fans;
- filters;
- chilled/cold loops where tier-appropriate;
- cryogenic or exotic thermal support for sovereign quantum modules as fictional capability abstractions;
- humidity/dust control;
- leak detection;
- fire suppression;
- hot/cold aisle layout abstraction;
- heat rejection signature;
- maintenance;
- weather and contamination.

Heat must constrain sustained agent capability.

## Physical spaces

Buildable spaces include:

- recovered terminal nook;
- small server closet;
- electronics lab;
- agent training room;
- data archive;
- secure model vault;
- evaluation sandbox;
- simulation cluster;
- fabrication design office;
- robotics/drone integration lab;
- materials lab;
- additive-manufacturing cell;
- composite/ceramic/armor lab;
- quantum-control lab;
- cold/thermal plant;
- sovereign rack hall;
- hardened research bunker;
- field telemetry center;
- audit/command room;
- quarantine room;
- redundant backup site.

Rooms depend on structure, power, cooling, networking, security, fire response, repair access, operators, and supplies.

# Training lifecycle

Every training program follows:

1. define intended task/domain;
2. define prohibited scope and autonomy;
3. inspect base model/checkpoint provenance;
4. gather and classify training sources;
5. quarantine untrusted material;
6. curate curriculum;
7. collect human demonstrations and corrections;
8. bind tool/simulator interfaces;
9. reserve compute, memory, storage, power, cooling, and time;
10. train/adapt through abstract jobs;
11. run held-out evaluations;
12. run adversarial and failure evaluations;
13. measure uncertainty calibration;
14. inspect drift and regressions;
15. certify a bounded capability envelope;
16. deploy with permissions and monitoring;
17. collect field evidence;
18. retrain, revoke, quarantine, roll back, or expand certification.

Training is not consuming generic data points. Every dataset and demonstration has provenance, domain, quality, bias/coverage abstraction, freshness, contamination, security, and compatibility.

# Human trainer gameplay

Human specialists remain strategically important.

Players and recruited experts may:

- select curricula;
- annotate manuals and failures;
- demonstrate tasks;
- correct agent plans;
- classify uncertain examples;
- design evaluations;
- operate labs;
- certify procedures;
- resolve contradictions;
- authorize tools;
- investigate incidents;
- approve research milestones;
- teach local/faction practices;
- preserve tacit knowledge not contained in archives.

Losing a specialist can slow training, invalidate certification, or strand a research branch without deleting all prior knowledge.

# Auto-research lifecycle

Every research program defines:

- problem statement;
- desired capability;
- constraints;
- prohibited outcomes;
- known evidence;
- uncertainty;
- hypotheses;
- candidate simulations;
- physical experiment requirements;
- material/tool/workstation needs;
- compute/power/cooling budget;
- time horizon;
- safety/ethics/gameplay approval gates;
- evaluator/critic agents;
- success metrics;
- stopping conditions;
- failure/recovery;
- expected unlock;
- artifact lineage.

The loop is:

`question → evidence review → hypothesis portfolio → simulation → skeptical review → experiment plan → human approval → physical experiment/prototype → measurement → contradiction analysis → model update → independent verification → release candidate → manufacturing qualification → field evidence → revision`

Do not unlock technology from compute time alone. Research must consume appropriate measurements, materials, prototypes, specialists, and facilities.

# AI-assisted design domains

## Additive manufacturing

Agents can unlock:

- topology-optimized brackets;
- lightweight lattice/cellular structures;
- replacement housings;
- ducts/manifolds as safe fictional game components;
- jigs and fixtures;
- drone parts;
- exo/mech interfaces;
- medical/support items;
- electronics enclosures;
- molds/forms for later processes;
- repair patches;
- game-defined weapon components only through the direct build-file unlock route and the existing weapon/crafting/maintenance owners.

Each design must match printer/process capability, feedstock, orientation/support abstraction, tolerances, post-processing, inspection, fatigue, heat, environment, and load.

## Honeycomb and cellular structures

Agents may design:

- lightweight cores;
- armor backing/core structures;
- drone panels;
- vehicle/exo/mech panels;
- impact absorbers;
- thermal structures;
- filters;
- structural sandwich panels;
- deployable base components.

Performance depends on material, cell architecture abstraction, defects, bonding, face sheets, load direction, manufacturing resolution, damage, moisture, heat, and repair. A honeycomb label is not a protection or strength guarantee.

## Advanced drones

Agents may improve:

- airframe topology;
- propulsion efficiency;
- load distribution;
- control tuning;
- navigation;
- sensor fusion;
- communications;
- swarm/fleet scheduling;
- armor;
- payload integration;
- repairability;
- manufacturing consistency;
- counter-drone systems.

All results use the five drone skills and live Unreal flight/network/evidence gates.

## Armor and materials

Agents may explore:

- layer ordering;
- ceramic/fiber/resin systems;
- honeycomb/cellular backings;
- vehicle/drone/exo/mech panels;
- weight/protection tradeoffs;
- multi-hit damage mitigation;
- repairable modules;
- manufacturing quality.

All results use the five armor skills and vendor-neutral ballistics evidence. No real-world armor recipe is produced.

## Game-defined additive-manufactured weapons

Agents may repair recovered build files or unlock original DayQ weapon-family recipes only as fictional game content.

The player-facing route is locked:

`find build file -> load it or repair damaged data -> recipe unlocks -> gather listed materials/core -> manufacture the gun -> use it immediately`.

There is no separate player-facing gun inspection, proof test, range approval, prototype certification, production approval, candidate rejection, or release gate. Developer QA remains required evidence, but it is never a player activity or crafting prerequisite.

Require:

- server-authoritative weapon, ammunition, recipe-unlock, crafting, inventory, and persistence systems;
- fictionalized material/process definitions and approved game balance;
- direct recipe unlock after a complete build file is loaded or repaired;
- ordinary crafting consumption through the existing manufacturing owner;
- immediate usable-weapon output after a successful authoritative craft;
- routing to the existing DayQ wear, dirt, fouling, lubrication, cleaning, field-stripping, repair, part-replacement, familiarity, handling, and malfunction systems;
- provenance and persistent identity;
- a project-owned `IBallisticsBackend` boundary with no vendor types in serialized state;
- Unreal testing as developer evidence rather than an in-world approval loop.

Do not generate real firearm CAD, dimensions, tolerances, chamber/barrel specifications, material recipes, printer parameters, ammunition construction, or step-by-step real fabrication instructions.

## Quantum development

Agents may research:

- Quantum ASIC control;
- error-correction abstractions;
- calibration;
- thermal/cold systems;
- photonic/interconnect components;
- secure roots;
- quantum sensor systems;
- suppression-field modeling;
- post-quantum hardware integration;
- recovered sovereign network interfaces;
- new accelerator schedules and algorithms.

Every branch requires captured hardware, measurements, facilities, specialists, power/cooling, and physical experiments. No universal decryption or magical quantum unlock.

# Agent research tree topology

Use intersecting branches:

- compute and memory;
- storage and knowledge;
- power and cooling;
- networking and secure roots;
- model recovery and training;
- evaluation and uncertainty;
- tool use and automation;
- simulation and digital twins;
- scientific discovery;
- materials and manufacturing;
- communications and networks;
- drones and robotics;
- armor and structures;
- weapons and defenses;
- medicine and biology;
- agriculture and ecology;
- energy and utilities;
- exoskeletons and mechs;
- quantum systems and suppression;
- governance, security, and counter-agent capability.

Knowledge permits an attempt. Infrastructure, materials, tools, specialists, experiments, and evidence make the unlock reliable.

# Agent job economics

Every training/research/design job consumes:

- compute time;
- memory/storage allocation;
- power;
- cooling capacity;
- operator/specialist attention;
- datasets/knowledge access;
- laboratory time;
- simulation capacity;
- materials and prototypes when physical evidence is needed;
- tool wear;
- maintenance;
- security/audit resources;
- opportunity cost from other jobs.

Model solo, four-person, twelve-person, and organized-large-clan progression. Prevent large-clan runaway through contested rare hardware, power/cooling, specialist scarcity, physical experiments, maintenance, security burden, diminishing returns, parallel verification needs, and attack/capture risk—not arbitrary research caps.

# Agent failure and uncertainty

Support:

- hallucinated or unsupported claims;
- overconfidence;
- underconfidence;
- bad decomposition;
- tool misuse;
- simulation mismatch;
- stale knowledge;
- conflicting corpora;
- corrupted memory;
- dataset poisoning abstraction;
- malicious instruction/document injection abstraction;
- checkpoint tampering;
- evaluator leakage/overfitting;
- reward/proxy gaming abstraction;
- catastrophic forgetting;
- domain transfer failure;
- automation cascade;
- fabrication mismatch;
- sensor error;
- field distribution shift;
- power interruption;
- cooling degradation;
- hardware error;
- network partition;
- compromised secure root;
- hostile agent deception;
- stolen designs;
- unauthorized autonomy.

Failures must be observable through evidence gaps, contradictions, anomalous behavior, tests, telemetry, component state, and audit—not opaque random punishment.

# Trust and governance

Use autonomy classes:

- `advisory`: may recommend only;
- `drafting`: may create candidate plans/designs;
- `sandboxed-tool`: may use approved tools in isolation;
- `supervised-execution`: may execute bounded jobs with human confirmation;
- `certified-autonomy`: may run previously certified routines within strict envelope;
- `strategic-orchestration`: may allocate approved resources within a portfolio but cannot change core policy;
- `quarantined`: no operational tool access;
- `revoked`: disabled pending investigation or destruction.

High-risk domains require stronger gates:

- weapons;
- autonomous defense;
- drones;
- quantum suppression;
- post-quantum identity;
- base utilities;
- medical treatment;
- model/training infrastructure;
- security/permissions;
- mech control;
- strategic research.

Agents may not rewrite their own trust roots, permissions, audit policy, weapon authorization, clan governance, or release criteria.

# Factions and world consequences

Agent infrastructure creates new faction identities and conflicts:

- archive keepers;
- human craft guilds suspicious of automation;
- agent trainers;
- model salvagers;
- secure-hardware clans;
- autonomous enclave remnants;
- bunker research societies;
- hostile captured-agent operators;
- open-knowledge settlements;
- tightly controlled sovereign labs;
- factions trading datasets, evaluations, tool adapters, checkpoints, secure chips, compute time, and research results.

Agent ownership creates political questions:

- who controls training data;
- who approves dangerous research;
- who receives productivity gains;
- whether agents can be copied;
- whether recovered agents carry old loyalties;
- how clans verify designs;
- how settlements respond to labor displacement;
- how secrets and public knowledge spread;
- whether a captured lattice is destroyed, isolated, negotiated with, retrained, or occupied.

Keep agents as systems with behavior, identity, history, and trust state without asserting real-world sentience conclusions as fact.

# Pinnacle tactical-companion loop

The pinnacle DayQ PvP build is not merely a powerful mech suit. It is a coupled system:

`pilot + persistent tactical companion + exo/mech chassis + sensors + communications + weapons + field evidence + base compute/training + research agents + fabrication stack`

The desired emotional arc is that the player and companion survive together, learn each other's methods, return with hard-won evidence, and use that evidence to make the clan's next physical build meaningfully better. A veteran agent should feel recognizable, valuable, and difficult to replace without becoming an invisible aim bot or a permanent unbeatable stat advantage.

Use an original DayQ identity and terminology for this system. “Jarvis-like” describes conversational presence and integrated assistance only; do not copy another franchise's name, voice, personality, interface, dialogue, art direction, or lore.

## Tactical-companion operating modes

Support explicit modes with different authority, bandwidth, power, heat, latency, and risk:

- **Dormant/transport:** encrypted checkpoint carried but not running.
- **Base resident:** uses the base compute lattice for training, research, simulation, and fabrication support.
- **Suit resident:** runs on local hardened compute with bounded memory and tools.
- **Distributed:** local reflex/safety processes remain in the suit while higher reasoning uses an authenticated base or squad mesh when connectivity permits.
- **Disconnected:** works from cached maps, local sensors, local doctrine, and last certified checkpoint; no remote knowledge appears magically.
- **Degraded:** sensor, compute, memory, power, cooling, or trust damage reduces specific capabilities.
- **Quarantined:** can be inspected but cannot operate tools, command devices, update models, or export learned artifacts.
- **Emergency:** performs only approved safety actions such as fall arrest, fire suppression, actuator stabilization, collision avoidance, pilot extraction assistance, and distress transmission.

Loss of communications must alter behavior rather than merely hiding voice lines. Loss of the base link stops remote simulation and shared intelligence. Damage to suit compute may increase latency, reduce track count, narrow models, disable speech, or force deterministic emergency control.

## Companion capability domains

Model distinct, trainable domains rather than one universal companion level:

- perception and sensor fusion;
- target classification and uncertainty calibration;
- track continuity and reacquisition;
- squad coordination and communications discipline;
- ballistics-solution assistance;
- counter-drone and robotic-defense analysis;
- armor and damage diagnosis;
- mobility, climbing, balance, and route planning;
- heat, power, ammunition, and maintenance management;
- electronic-signature and emissions control;
- tactical prediction and adversary-doctrine recognition;
- pilot workload management;
- casualty and rescue assistance;
- after-action reconstruction;
- research-evidence curation;
- design-domain specializations.

Each domain requires its own training evidence, evaluator score, confidence calibration, certification, decay/drift rules, compute/memory cost, and tool permissions.

## Pilot-facing interaction

The companion may communicate through:

- directional voice;
- HUD annotations;
- uncertainty bands;
- prioritized warnings;
- haptic cues;
- map and route overlays;
- suit-status summaries;
- proposed target tracks;
- requested confirmations;
- post-battle debriefs;
- base-lab design reviews.

Allow players to configure verbosity, terminology, warning priority, risk tolerance within doctrine limits, accessibility presentation, and whether noncritical observations are spoken or visual. Preserve essential safety/friendly-fire warnings.

The relationship model may remember useful preferences and shared history, but it must not manipulate the player, impersonate real people, fabricate emotions as proof of sentience, or conceal material uncertainty. Personality affects presentation and cooperation—not hidden combat power.

## Target acquisition and tracking rules

The agent can make sensor-rich combat feel advanced without providing cheats.

Require:

- a real authoritative sensor source for every observation;
- line of sight, field of view, range, resolution, refresh rate, occlusion, weather, smoke, foliage, lighting, emissions, and sensor damage where relevant;
- observation age and uncertainty;
- classification confidence and false-positive/false-negative behavior;
- server-authoritative track creation, fusion, sharing, decay, reacquisition, and deletion;
- explicit distinction between detected, suspected, classified, identified, ranged, tracked, and firing-solution states;
- latency and bandwidth costs for squad/base/drone sharing;
- jamming, spoofing, decoys, camouflage, thermal management, terrain masking, emissions control, sensor destruction, and network partition as counterplay;
- pilot confirmation for lethal target designation unless a separately approved doctrine explicitly permits a bounded defensive action;
- no knowledge of players, inventories, health, positions, intentions, or identities that the authorized sensor and intelligence systems could not infer.

The companion may recommend aim corrections, lead, holdover, zero, target priority, weapon suitability, armor-facing, and exposure timing. The authoritative weapon and ballistics systems own the shot, recoil, projectile, hit, penetration, damage, condition, malfunction, and ammunition result.

Do not implement perfect lock-on, cursor adhesion, recoil cancellation, automatic head selection, automatic weak-point omniscience, target persistence through unexplained occlusion, or server-hidden information disclosure.

## Pilot-agent combat learning

Combat experience may improve the agent, but raw kills or time connected are not training currency.

Capture versioned **combat evidence episodes** containing only authoritative and policy-approved data:

- encounter ID and context class;
- participating pilot, suit, agent, and model versions;
- terrain, verticality, weather, visibility, sensor and network conditions;
- enemy/contact classes known after adjudication;
- observations and their uncertainty at decision time;
- recommendations made, accepted, rejected, or ignored;
- pilot actions and timing;
- weapon, ammunition, armor, mobility, heat, power, and damage states;
- outcomes, near misses, component failures, friendly-fire risks, retreat/recovery, and survival;
- contradictions between prediction and outcome;
- evidence provenance, integrity, consent/privacy class, and anti-tamper signature.

Convert episodes into learning only through:

1. authoritative capture;
2. integrity and anti-farming review;
3. privacy/redaction policy;
4. encounter diversity scoring;
5. uncertainty and contradiction extraction;
6. base debrief with pilot annotations;
7. replay or counterfactual simulation;
8. independent evaluator/critic review;
9. bounded training or memory update;
10. regression against held-out scenarios;
11. certification;
12. deployment as a new signed checkpoint or doctrine revision.

The fielded agent never silently rewrites its own authoritative combat policy during a match. It may create temporary episodic memory and candidate lessons, but permanent capability changes occur through the secured training pipeline.

Reward diverse, high-information survival and correction:

- encountering a new countermeasure;
- discovering a model error;
- successfully identifying uncertainty;
- coordinating across sensor types;
- surviving damaged or disconnected operation;
- detecting a spoof or decoy;
- observing armor, heat, mobility, weapon, or drone failure under controlled provenance;
- completing objectives with lower collateral damage, ammunition use, exposure, or component loss;
- validating a prediction through repeated independent evidence.

Do not reward arranged kill trading, repeated helpless targets, disposable alt accounts, spawn camping, identical scripted encounters, friendly damage, or unverifiable client telemetry.

## Battlefield-to-base innovation loop

The complete loop is:

`PvP/PvE operation → signed evidence episodes → debrief → curated dataset → replay/counterfactual simulation → training/evaluation → certified agent revision → research hypothesis → digital design candidates → virtual tests → physical prototype → range/lab test → manufacturing qualification → new component/recipe revision → field deployment → new evidence`

Battlefield learning can unlock **questions, hypotheses, parameter envelopes, or design candidates**. It cannot directly unlock a finished item merely because the pilot accumulated kills.

Examples:

- repeated joint penetrations can generate a revised armor-coverage hypothesis;
- thermal saturation can motivate radiator placement, heat-sink, duty-cycle, or doctrine candidates;
- track loss in smoke can produce multisensor or drone-placement research;
- recoil-induced structural drift can produce hardpoint, bracing, stabilization, or fire-control candidates;
- vertical ambush evidence can improve route-risk models and climber-suit sensor placement;
- counter-drone engagements can produce new antenna, sensor, armor, interceptor, or swarm-doctrine candidates;
- ammunition and magazine failures can create interface, feed, storage, inspection, or maintenance candidates;
- pilot overload can drive display, warning-priority, automation, or haptic-interface redesign.

Every candidate still consumes research time, compute, electricity, cooling, specialist labor, test capacity, raw materials, tools, prototypes, and destructive validation. The established design, crafting, weapon, armor, drone, exo, mech, and fabrication owners decide whether the candidate becomes a released revision.

## Agent inheritance, backup, loss, and capture

Persist separately:

- base master checkpoint;
- suit-deployed signed checkpoint;
- episodic mission memory;
- pending unreviewed evidence;
- curated training evidence;
- certified long-term memory;
- pilot relationship/preferences;
- tool permissions and doctrine;
- research/design contributions;
- backup generation and timestamp.

If a suit is destroyed, captured, disconnected, rolled back, or recovered, resolve each layer explicitly. A recent base backup may preserve the agent but lose unreturned mission experience. A captured local checkpoint may expose doctrine or evidence only to the degree allowed by hardware damage, encryption, trusted roots, extraction tools, and security gameplay. Never duplicate an agent by replaying a save, reconnecting during transfer, or restoring both source and destination.

Permit expensive forked specialists only through an explicit lineage operation with compute, training, certification, identity, memory, and trust consequences. A fork is not the same person/agent instance and cannot inherit unique field evidence twice.

## Progression and pinnacle builds

Companion access should begin before pinnacle mechs, but capability and embodiment scale:

- **T0 recovered advisory fragment:** base console, manuals, diagnostics, unreliable answers;
- **T1 personal field assistant:** radio/handheld mapping, inventory and maintenance aid;
- **T2 exoskeleton copilot:** load, balance, route, power, sensor, and safety assistance;
- **T3 combat exo tactical companion:** bounded sensor fusion, track proposals, squad communications, debrief, and battle evidence;
- **T4 specialist suit agent:** certified doctrine, drone coordination, electronic countermeasure analysis, design-domain expertise;
- **T5 mech integrated combat partner:** redundant local compute, multi-sensor fusion, damage control, weapon/suit orchestration, pilot workload management, and high-value field research;
- **T6 sovereign battle-research agent:** a rare late-game companion linked to a mature Quantum ASIC/base research lattice, able to coordinate specialized research cells and produce superior candidates while remaining evidence-, resource-, and certification-gated.

The pinnacle PvP setup is a highly customized mech plus a veteran, trusted, properly certified tactical companion and the clan infrastructure capable of sustaining both. It must remain vulnerable to logistics interruption, compute/cooling failure, checkpoint theft, jamming, deception, sensor damage, pilot error, ammunition limits, heat, terrain, anti-mech weapons, maintenance debt, and coordinated opponents.

## PvP economy and anti-snowball rules

Model progression for solo, four-person, twelve-person, and organized-large-clan cohorts.

Use diminishing information value for repeated encounter classes. Require diversity across opponents, equipment, ranges, environments, tactics, sensor conditions, and failure cases. Cap the amount of unreviewed evidence that can be banked. Charge compute, energy, cooling, specialist time, evaluator capacity, and test materials for every durable improvement.

Veteran agents should primarily improve prediction quality, uncertainty, coordination, adaptation speed, design search, and efficient use of existing systems—not stack unlimited raw accuracy or damage bonuses.

Create catch-up and counterplay through:

- recoverable general curricula;
- tradable or stealable nonpersonal research;
- alliance research agreements;
- public/recovered benchmark suites;
- diminishing returns;
- domain specialization tradeoffs;
- operating and recertification costs;
- evidence decay when environments or enemy technology change;
- adversarial counter-doctrine;
- captured telemetry and reverse engineering;
- destruction/capture risk for deployed hardware;
- strict limits on transferring unique pilot-agent coordination.

Run exploit scenarios for kill trading, bot/alt farming, staged sensor spoofing, disconnect preservation, duplicate checkpoint restore, replay submission, fabricated client telemetry, private-server boosting, low-risk repetitive farming, clan telemetry monopolies, and deliberate poisoning of shared datasets.

## Tactical companion data contract

Create versioned schemas at minimum for:

```yaml
tactical_companion:
  agent_id: stable_unique_id
  lineage_id: stable_id
  display_identity: original_dayq_identity
  model_checkpoint_id: stable_id
  doctrine_version: version
  certifications: []
  domain_capabilities: {}
  uncertainty_calibration: {}
  pilot_links: []
  relationship_preferences: {}
  tool_permissions: []
  sensor_permissions: []
  weapon_authority_policy: advisory_by_default
  suit_compatibility: []
  local_compute_requirements: {}
  memory_budget: {}
  power_heat_bandwidth_costs: {}
  security_state: trusted|degraded|quarantined|revoked
  backup_generation: integer
  persistence_version: version

combat_evidence_episode:
  episode_id: stable_unique_id
  server_match_id: stable_id
  agent_checkpoint_id: stable_id
  pilot_id: stable_id
  suit_configuration_hash: hash
  start_end_time: {}
  context_class: stable_id
  environment_tags: []
  authoritative_observations: []
  recommendations_and_responses: []
  state_timeline_reference: stable_id
  outcomes: []
  contradictions: []
  novelty_score: number
  integrity_status: pending|verified|rejected|quarantined
  privacy_class: enum
  anti_farm_flags: []
  signature: hash_or_signature

agent_design_insight:
  insight_id: stable_unique_id
  contributing_episode_ids: []
  agent_checkpoint_id: stable_id
  domain: armor|weapon|sensor|drone|mobility|thermal|power|comms|quantum|other
  observed_failure_or_opportunity: stable_description
  hypothesis: stable_description
  confidence_and_uncertainty: {}
  proposed_tests: []
  owning_system: stable_id
  research_program_id: stable_id
  status: proposed|testing|supported|rejected|superseded
  design_candidate_ids: []
  provenance: []
```

Use stable IDs, idempotency keys, revision hashes, audit records, save-version migrations, and ownership boundaries. Do not persist high-frequency raw sensor streams directly in ordinary save records; store bounded evidence summaries and references according to the telemetry architecture and privacy policy.

## Unreal MCP implementation guidance for the companion

Inspect the existing DayQ agent, exo, mech, GAS, AI perception, weapon, ballistics, damage, team, drone, communications, inventory, crafting, persistence, replay, telemetry, UI, audio, voice, networking, and anti-cheat systems before creating anything.

Prefer data-driven composition:

- tactical-companion definition Data Assets;
- certification/doctrine Data Assets;
- suit-agent interface components;
- authoritative sensor-track subsystem;
- advisory/notification subsystem;
- evidence capture and debrief subsystem;
- training/research handoff records;
- signed checkpoint and transfer transactions;
- explicit gameplay tags for mode, trust, certification, sensor state, track state, and authority;
- deterministic or bounded server-approved decision logic for live PvP-critical outcomes.

Do not put the entire companion in one Blueprint graph. Separate presentation, dialogue, local prediction, authoritative perception, evidence recording, persistence, training, and design-research handoff.

Default the shipped player-facing tactical behavior to deterministic/data-driven systems that do not require a live external AI service. Any live generative dialogue or reasoning service is a separate explicit product decision with privacy, latency, moderation, platform, cost, availability, security, competitive-integrity, and offline fallback gates. It must never own authoritative perception, aiming, firing, damage, inventory, crafting, progression, or persistence.

## Companion validation gates

The sixth skill is accepted only when:

1. the companion feels present and useful through voice/UI/behavior without copying another franchise;
2. every target track is explainable from authoritative sensors and decays correctly;
3. jamming, spoofing, concealment, network loss, sensor damage, and heat/power loss provide observable counterplay;
4. the agent never fires, damages, reveals, or persists information outside its approved authority;
5. combat evidence cannot be forged, replayed, duplicated, or cheaply farmed;
6. durable learning requires base review, training, held-out evaluation, certification, and a signed revision;
7. battlefield evidence produces hypotheses/design candidates rather than free finished blueprints;
8. every released component still passes owning-system simulation, prototype, physical test, crafting, balance, and manufacturing gates;
9. agent backup, transfer, capture, destruction, quarantine, fork, and restore remain duplication-safe and crash-safe;
10. pilot-agent history persists without creating uncapped raw combat bonuses;
11. solo and small-group players retain viable paths while large clans gain breadth and throughput rather than exclusive invulnerability;
12. late join, disconnect, reconnect, server restart, journal replay, rollback, migration, network partition, and suit capture preserve authoritative state;
13. representative exo/mech battles meet server frame, client frame, memory, AI, sensor, audio, telemetry, persistence, and bandwidth budgets;
14. automated tests and live multi-client PIE evidence cover both successful assistance and every major failure/degraded state;
15. the full field-evidence-to-certified-design-to-physical-prototype-to-redeployment loop is demonstrated end to end.

# Data contracts

Create versioned data equivalent to:

```yaml
agent_model_definition:
  model_id: stable_id
  family: stable_id
  revision: version
  architecture_class: enum
  capability_band: enum
  provenance_ref: stable_or_persistent_id
  required_compute_tags: []
  memory_storage_requirements: map
  supported_tool_protocols: []
  base_domain_capabilities: map
  security_requirements: []
  known_limitations: []

agent_instance:
  agent_id: persistent_guid
  model_definition_id: stable_id
  checkpoint_id: persistent_guid
  owner_id: entity
  permissions_ref: stable_id
  autonomy_class: enum
  domain_competencies: map
  tool_competencies: map
  uncertainty_calibration: map
  memory_store_refs: []
  allowed_tool_refs: []
  allowed_network_refs: []
  training_history_refs: []
  certification_refs: []
  drift_state: enum
  trust_state: trusted|restricted|suspected|quarantined|revoked
  deployment_state: enum
  infrastructure_assignment_ref: optional
  persistence_revision: integer

agent_infrastructure_node:
  node_id: persistent_guid
  component_instance_ids: []
  compute_capacity: map
  memory_capacity: map
  storage_capacity: map
  interconnect_capacity: map
  power_requirement: map
  cooling_requirement: map
  secure_root_refs: []
  quantum_accelerator_refs: []
  condition_by_component: map
  owner_id: entity
  permissions_ref: stable_id
  network_zone: enum
  current_allocations: []
  persistence_revision: integer

agent_training_job:
  job_id: persistent_guid
  agent_or_checkpoint_ref: guid
  curriculum_revision: stable_id
  dataset_refs: []
  demonstration_refs: []
  tool_refs: []
  evaluator_refs: []
  infrastructure_reservations: []
  power_cooling_reservations: map
  specialist_assignments: []
  current_stage: enum
  progress: normalized
  interruption_history: []
  output_checkpoint_ref: optional_guid
  evaluation_result_refs: []
  journal_revision: integer

agent_research_program:
  program_id: persistent_guid
  owner_scope: entity
  problem_definition_ref: stable_id
  constraints_ref: stable_id
  assigned_agent_ids: []
  orchestration_graph_ref: persistent_data
  hypothesis_refs: []
  simulation_job_refs: []
  experiment_job_refs: []
  prototype_job_refs: []
  evidence_refs: []
  critic_verifier_refs: []
  resource_reservations: []
  user_approval_gates: []
  uncertainty_state: map
  current_stage: enum
  unlock_candidate_refs: []
  journal_revision: integer

agent_design_artifact:
  design_id: persistent_guid
  family_id: stable_id
  revision: version
  originating_program_id: guid
  agent_author_refs: []
  human_approver_refs: []
  assumptions: []
  material_recipe_refs: []
  process_capability_refs: []
  geometry_or_schema_ref: secure_artifact
  simulation_evidence_refs: []
  physical_test_refs: []
  failure_envelope_ref: stable_id
  manufacturability_state: enum
  certification_state: draft|sandbox|prototype|qualified|released|rejected|retired
  security_classification: enum
  artifact_hash: hash
  persistence_revision: integer
```

Use actual DayQ conventions. Never store vendor/runtime model types in authoritative game schemas.

# Multiplayer and persistence

The server authoritatively owns:

- agent/model/checkpoint identity;
- infrastructure components and allocation;
- training/research/design jobs;
- dataset/tool permissions;
- resource reservations and consumption;
- progression unlocks;
- design release state;
- manufacturing handoff;
- trust/quarantine/revoke state;
- ownership, capture, theft, transfer, and destruction;
- audit events;
- persistence and migration.

Clients may request jobs and display authorized progress/results. They may not report completion, create checkpoints/designs, forge competence, alter autonomy, bypass evaluations, duplicate weights/data, or reveal protected artifacts.

Persist all unique assets, jobs, histories, evidence references, infrastructure condition, allocations, power/cooling state, approvals, trust state, designs, and schema revisions.

Test late join, simultaneous job requests, disconnect, transfer/capture, server restart during training/research/fabrication, journal replay, rollback, migration, corrupted artifacts, revoked agents, destroyed racks, network partition, power loss, and recovery from backup.

# Runtime architecture boundary

DayQ’s player-facing agent system does not require live external AI services.

Default to a deterministic/data-driven gameplay simulation of:

- agent capabilities;
- research graphs;
- training/evaluation;
- generated design alternatives;
- uncertainty;
- job progress;
- failures;
- unlocks;
- dialogue/presentation.

If the project proposes real runtime generative models or external services, treat that as a separate user decision requiring:

- privacy;
- moderation;
- service availability;
- latency;
- cost;
- platform certification;
- age rating;
- abuse controls;
- prompt/data security;
- deterministic fallback;
- offline behavior;
- content provenance;
- licensing;
- model updates;
- telemetry;
- retention;
- player consent.

Do not make core gameplay dependent on an unapproved cloud service.

Developer agents used to build DayQ remain separate from simulated in-world agents. Do not let an in-world agent access developer tools, source control, local machines, credentials, or production services.

# Unreal MCP implementation guidance

Use the existing DayQ Unreal MCP production and validation skill.

Before editing:

1. verify Unreal MCP, Terminal, EditorToolset, build, PIE, dedicated server, tests, logs, and profiling;
2. inspect current project systems and authority;
3. map ownership, schemas, migrations, and decisions;
4. update the requirements/no-skip ledger;
5. define a bounded vertical work order;
6. implement the smallest complete agent loop;
7. compile, run automated tests, launch PIE/multiplayer, capture evidence, repair, and regress.

Prefer:

- versioned Data Assets/Tables for definitions;
- persistent instance records for agents, checkpoints, infrastructure, jobs, and designs;
- project-owned subsystems for agent infrastructure, training, research orchestration, design artifacts, and trust/audit;
- adapters to inventory, crafting, power, cooling, networks, tools, manufacturing, drones, armor, weapons, exos, mechs, and quantum systems;
- C++ for authoritative jobs, transaction integrity, graph validation, persistence boundaries, permissions, and large-scale simulation;
- Blueprints/UI for presentation and assembly without client-owned authoritative truth;
- strategic/offline job simulation with deterministic elapsed-time bounds;
- debug views for capability, resources, task graphs, uncertainty, evaluations, contradictions, approvals, security, power, cooling, and provenance.

# Security and exploit requirements

Prevent:

- client-created agents/checkpoints/designs;
- duplicated model weights, datasets, secure hardware, research outputs, or unlocks;
- cancel/refund training duplication;
- restarting to reroll outcomes without consuming state;
- clock manipulation of offline research;
- forged evaluation results;
- evaluator leakage making every training pass;
- unauthorized tool/network/workstation access;
- agent privilege escalation;
- agent rewriting trust or weapon policy;
- copying protected artifacts without time/storage/hardware consequences;
- prompt/document injection directly changing authority;
- data poisoning without detectable provenance paths;
- compromised agent silently reentering trusted service;
- infinite recursive task spawning;
- unbounded queues or compute denial of service;
- free auto-research without power/material/lab cost;
- AI designs bypassing manufacturing or safety validation;
- impossible material/design unlocks;
- external service secrets in logs/assets;
- developer-agent access from in-world systems;
- rollback restoring consumed resources while keeping results;
- large-clan snowball without contested inputs, upkeep, and attack surface.

# Performance model

Do not simulate every token or neural operation.

Budget:

- active agent conversations/tasks;
- background jobs;
- research graph nodes;
- simulation queues;
- infrastructure allocations;
- UI updates;
- audit events;
- persistence writes;
- offline advancement;
- strategic faction agent systems;
- multiplayer relevance;
- design artifacts;
- telemetry and debugging.

Use event-driven or scheduled job simulation. Replicate authorized state changes, not internal thought traces. Store compact evidence/provenance, not unrestricted hidden reasoning.

# Required integrated vertical slice

Build and validate this route:

1. A player recovers a damaged pre-collapse assistant, fragmented checkpoint, manuals, storage device, accelerator card, power supply, cooling parts, and uncertain datasets.
2. Physical inventory enforces mass, volume, fragility, contamination, power, cooling, security, and transport.
3. The player builds a small server closet with power, UPS/buffer, cooling, network isolation, console, storage, and fire response.
4. The agent starts as A1 advisory-only and can search trusted manuals while clearly reporting uncertainty.
5. A human technician curates data and demonstrations to train an A2 repair apprentice.
6. Training reserves compute, memory, storage, power, cooling, time, specialist attention, and evaluator capacity.
7. A held-out evaluation catches at least one bad procedure, triggering retraining rather than a free unlock.
8. The trained agent accelerates a known repair/crafting workflow without creating resources or bypassing workstation capability.
9. The clan builds better racks, accelerators, storage, interconnect, power, cooling, secure roots, simulation, and laboratory infrastructure.
10. Multiple specialist agents form an A4 research cell with planner, researcher, simulator, critic, safety reviewer, archivist, and integrator roles.
11. The cell researches a honeycomb/cellular drone or armor panel through hypothesis, simulation, independent criticism, physical prototype, measurement, revision, and qualification.
12. A design with impressive simulated performance fails physical testing because of a manufacturing or material mismatch; evidence drives revision.
13. An approved design becomes a versioned manufacturing recipe/work order and produces a real persistent item through existing crafting systems.
14. The cell creates an improved drone component that passes assembly, flight, multiplayer, repair, and persistence tests.
15. The cell recovers or creates an original game-defined weapon build file; loading or repairing the complete file unlocks its recipe, existing crafting produces an immediately usable weapon when listed requirements are met, and existing maintenance owns the item thereafter without a separate player-facing approval loop.
16. The clan captures a damaged Quantum ASIC/control module from an enclave or bunker operation.
17. Specialists restore power, cooling, timing, secure root, calibration, and classical control around the module.
18. Quantum Branch Search accelerates one approved optimization/research workload but returns hypotheses requiring classical and physical validation.
19. The research lattice advances suppression, drone, armor, materials, energy, or quantum capability without universal decryption or magic.
20. An untrusted recovered dataset attempts an abstract poisoning/injection event. Provenance, sandbox, critic, anomaly, and quarantine systems expose and contain it.
21. A compromised agent is revoked while jobs transfer to certified replacements with preserved audit lineage.
22. Rival players attempt theft/capture/sabotage of racks, checkpoints, archives, power, cooling, and network links.
23. Multiple clients submit, approve, monitor, interrupt, and recover jobs under latency and packet loss.
24. The server restarts during training, research, simulation, design release, infrastructure failure, and fabrication handoff.
25. Journal replay, rollback, backups, and migrations preserve correct agents, resources, jobs, evidence, permissions, unlocks, and artifact lineage without duplication.
26. Representative settlement, clan, enclave, and bunker agent loads meet server, memory, bandwidth, save, and offline-simulation budgets.
27. The player deploys a certified tactical companion into a combat exoskeleton and verifies its named identity, doctrine, sensor permissions, tool permissions, checkpoint, and base backup.
28. In a live multi-client combat route, the companion fuses only authoritative suit, squad, drone, and communications observations into uncertain target tracks.
29. Opponents break or mislead tracks through occlusion, smoke, camouflage, jamming, spoofing, decoys, sensor damage, network partition, and emissions control.
30. The companion advises on target priority, lead/hold, cover, vertical routes, heat, ammunition, power, damage, and retreat while the weapon and ballistics owners remain authoritative.
31. The pilot and companion survive a novel engagement, return signed evidence, and complete an interactive after-action debrief.
32. Anti-farming checks reject replayed, duplicated, staged, low-diversity, client-forged, and alt-account evidence.
33. Curated evidence drives replay, counterfactual simulation, bounded training, held-out evaluation, certification, and a signed companion checkpoint revision.
34. A verified field failure produces an armor, sensor, weapon-interface, drone, cooling, mobility, or communications design hypothesis—not a free blueprint.
35. Research agents convert the hypothesis into competing design candidates; the owning system selects tests and rejects at least one attractive but invalid design.
36. A surviving candidate passes virtual, physical, manufacturing, crafting, multiplayer, and persistence gates before becoming a released component revision.
37. The revised companion and component return to an advanced exo or mech battle, producing measurable benefit and new counterplay without hidden information or autonomous lethal authority.
38. Destroy, capture, disconnect, quarantine, restore, and migrate the suit/agent while proving backup generations, episodic evidence, ownership, checkpoint lineage, and inventories cannot duplicate.

# Acceptance gates

Do not mark complete unless:

1. all six skills are structurally valid and dependency-mapped;
2. the 2058 agent direction is recorded as user-decided canon;
3. exact autonomy/pacing/runtime questions remain labeled proposed/testing until evidenced;
4. agent capability derives from physical stack and training, not one magic level;
5. quantum accelerators remain specialized, scarce, bounded, and physically supported;
6. early agents are useful without bypassing later infrastructure;
7. curricula, demonstrations, datasets, tools, evaluators, and certifications produce distinct outcomes;
8. training and research consume compute, power, cooling, time, specialists, and physical evidence;
9. agents accelerate established work without creating free materials or ignoring workstations;
10. multi-agent research includes independent criticism, uncertainty, tests, and stopping rules;
11. auto-research cannot unlock technology from elapsed time alone;
12. non-weapon AI-assisted designs remain drafts until their owning validation gates pass, while agent-printed weapon build files follow the locked direct-unlock route and still require developer/runtime evidence without adding a player-facing approval activity;
13. honeycomb, drones, armor, weapons, and quantum designs use their existing authoritative systems;
14. no real-world weapon CAD or fabrication instruction appears;
15. security covers provenance, sandboxing, tools, permissions, poisoning, injection, tampering, theft, quarantine, and rollback;
16. agents cannot rewrite core trust, weapon, governance, or audit policies;
17. client-forged agents, jobs, results, designs, resources, and unlocks are rejected;
18. late join, disconnect, concurrent jobs, capture, restart, journal replay, rollback, and migrations pass;
19. infrastructure damage, power loss, cooling loss, and network partition create coherent degraded/recovery states;
20. agent systems do not make player judgment, specialists, field missions, logistics, or experimentation irrelevant;
21. representative performance budgets pass;
22. live Unreal logs, metrics, screenshots/video, state dumps, graph traces, evidence lineage, and profiler captures exist;
23. untested live-project gates are reported blocked;
24. no external runtime AI service is introduced without an explicit user decision and full platform/privacy/security evidence.
25. the tactical companion is a persistent original DayQ identity and not a copied franchise character;
26. target acquisition and tracking use explainable authoritative sensors, uncertainty, decay, and counterplay;
27. PvP combat learning cannot be reduced to kills, elapsed time, alt farming, or replayed telemetry;
28. durable agent improvements require debrief, training, held-out evaluation, certification, and signed deployment;
29. field learning produces evidence and design candidates, while owning systems retain weapon, armor, drone, exo, mech, crafting, and fabrication authority;
30. veteran agents improve coordination and design quality without uncapped accuracy, damage, or hidden-information bonuses;
31. the pinnacle mech-plus-agent loop remains constrained by power, cooling, sensors, communications, ammunition, logistics, damage, security, terrain, and opposing counter-doctrine;
32. the complete PvP-evidence-to-base-research-to-physical-upgrade-to-field-validation loop passes live multi-client tests.

# Required evidence baseline

Use current sources to ground risk and distinguish science fiction from present reality:

- NIST AI Risk Management Framework: <https://www.nist.gov/itl/ai-risk-management-framework>.
- NIST Generative AI Profile and testing/evaluation/verification/validation resources: <https://airc.nist.gov/>.
- DARPA FoundSci explored skeptical, uncertainty-aware agentic scientific discovery: <https://www.darpa.mil/research/programs/foundation-models-for-scientific-discovery>.
- DOE Quantum Information Science distinguishes quantum computing, sensing, simulation, and networking: <https://www.energy.gov/topics/quantum-information-science>.
- NIST post-quantum cryptography standards concern classical algorithms intended to resist quantum attacks and must not be confused with quantum computers themselves: <https://csrc.nist.gov/Projects/post-quantum-cryptography>.

Recheck current primary sources during implementation. Label DayQ-specific Quantum ASICs, coherent agent architecture, and 2058 capabilities as fiction.

# Required deliverables

Produce:

1. all six native DayQ agent-system skills;
2. `agents/openai.yaml` for every skill;
3. a decision record for agentic progression and theoretical A6 status;
4. shared ownership/interface map;
5. agent, model, checkpoint, dataset, memory, tool, evaluator, certification, infrastructure, training-job, research-program, design-artifact, tactical-companion, combat-evidence, agent-design-insight, security, audit, and unlock schemas;
6. compute/power/cooling/network/quantum infrastructure tree;
7. agent training and specialization tree;
8. multi-agent orchestration and auto-research graph;
9. AI-assisted design and manufacturing contracts;
10. trust, security, governance, hostile-agent, quarantine, rollback, and incident contracts;
11. progression/economy simulations for solo, four-person, twelve-person, and organized-large-clan cohorts;
12. base rooms, workstations, components, tools, assets, environmental states, repair, and salvage catalog;
13. integrations for drones, armor, communications, energy, weapons, ballistics, exos, mechs, tactical companions, combat evidence, defense grids, suppression, enclaves, and bunkers;
14. Unreal MCP work orders;
15. multiplayer, persistence, journaling, crash recovery, migration, exploit, privacy, security, accessibility, and performance plans;
16. automated and live test matrices;
17. integrated vertical-slice evidence;
18. unresolved questions and user decisions;
19. requirements/no-skip ledger updates;
20. manifest, hashes, validators, and import report when packaging is in scope.

# Completion report

Report:

- skills and references created;
- decisions recorded;
- existing systems inspected;
- ownership and integration decisions;
- infrastructure and progression graphs;
- schemas and migrations;
- agent/training/research/design/security/tactical-companion implementation;
- Unreal assets, Actors, Components, Blueprints, C++, Data Assets, Data Tables, UI, and levels affected;
- training, evaluation, tactical-companion, target-tracking, combat-evidence, anti-farming, auto-research, design, fabrication, security, and quantum-accelerator results;
- multiplayer, persistence, journal, rollback, crash recovery, exploit, privacy, security, and performance results;
- failures, repairs, reruns, and remaining limitations;
- exact live evidence or explicit blocked status;
- final acceptance status for every skill and integrated system.

Never claim an agent is capable because a progress bar completed. Never let agents create free knowledge, materials, designs, or authority. Never treat quantum as magic. Never release an AI design without evidence. Never let in-world agents access developer systems. Never mark complete without live multiplayer, persistence, security, and physical-loop proof.
