# DayQ Agent-Designed Printed Weapon Contract

## Purpose

DayQ contains thirty original weapon families whose frames, housings, furniture, controls, magazines, mounts, interfaces, and selected non-pressure-bearing components may be additively manufactured. Their existence connects build files found as valuable loot, trained agents, Glentech fabrication, material reclamation, field experience, gunsmithing, asset production, authentic handling, maintenance, and persistent clan industry.

"Printed weapon" is a progression category, not a promise that a household printer creates a complete firearm. Each family declares recovered or manufactured functional cores, material grades, printer capability and direct integration with the existing firearm wear, cleaning, maintenance and repair loop. The game never exposes actionable real-world fabrication specifications.

## What each fabrication tier really produces

- **P1-P2:** rebuild kits. Print stocks, grips, outer chassis, simple sights, magazine bodies, carriers, covers and workshop aids around a recovered working barrel/action/fire-control core.
- **P3:** standardized hybrid weapons. Add durable housings, circuit interfaces, improved magazines and modular furniture, but retain a recovered functional core.
- **P4:** structural metal production. Manufacture correct-tier receiver structures, controls and feed parts while using a recovered or P4-compatible barrel/locking core.
- **P5:** multi-material production. Produce stronger, lighter and sensor-ready structures; critical cores remain separate recipe components.
- **P6-P7:** advanced clan and sovereign production. Manufacture nearly the complete platform from high-grade material lots while still requiring critical cores, ammunition and service support.

This keeps early additive manufacturing useful immediately without pretending a home polymer printer can safely replace every part of a firearm.

## Existing owners and adapters

| Concern | Existing owner | This skill contributes |
|---|---|---|
| Weapon operation and ballistics | `operate-dayq-authentic-weapons` | family configuration and runtime interfaces |
| Field stripping and maintenance | firearm-maintenance suite | component hierarchy, service states, familiarity hooks |
| Item identity and transactions | authoritative inventory | stable design/component/weapon references only |
| Recipes and jobs | crafting/manufacturing owners | abstract gates and versioned work-order input |
| Printer/foundry capability | `build-dayq-glentech-fabrication` | R/F/P/G/M requirements, material grades and crafting jobs |
| Agent training | `train-dayq-agents` | competency and training prerequisites |
| Research and design | agent research/design owners | candidate lineage and design hypotheses |
| Player skill | `progress-dayq-player-skills` | gunsmith/operator practice evidence adapters |
| Assets | systemic asset factory | Blender/Unreal work orders and acceptance evidence |
| Authority/persistence | existing runtime owners | server-owned recipe unlocks, revisions, journals and migrations |

Never replace these owners.

## Playable unlock loop

1. Find a weapon build file in the world. It is a real loot item stored on a data chip, workshop drive, Edge Interface, printer cartridge, base server or captured clan terminal.
2. Bring it home or copy it through an owned terminal. Before import, another player can steal the physical carrier. After import, the player chooses a personal-agent library or an explicitly shared clan library.
3. If the file is complete, loading it reveals the required printer, materials, functional core, tools and skills and immediately unlocks the recipe.
4. If the file is damaged, the player assigns an agent repair job. When the file reaches complete data, its recipe unlocks immediately.
5. Gather the physical materials and components and manufacture a persistent weapon through the existing crafting system.
6. The weapon is immediately usable. Its material grade, functional-core condition, machine condition and agent assistance establish its starting condition and reliability.
7. From that point forward, existing firearm mechanics own fouling, lubrication, dirt, water, heat, wear, malfunctions, cleaning, field stripping, repair, part replacement and familiarity.
8. After meaningful use and maintenance history, the agent may offer optional variant recipes. Choosing one unlocks another craftable design; it does not impose a certification sequence.
9. High-tier agents can eventually design an original family, but crafting it still requires its listed materials, machines and functional core.

The base unlock is deliberately easy to understand: **find file -> bring it home -> agent reads or repairs it -> recipe unlocks -> manufacture and use the gun -> maintain it through the existing system**.

### Build-file conditions

- **Complete:** loads immediately and unlocks the recipe.
- **Damaged:** shows a readable completeness percentage and requires a bounded agent repair job. Repair time, compute and failure risk scale with missing data.
- **Encrypted:** requires the specified agent skill and compute tier before it behaves like a complete or damaged file. It is a progression gate, not a hacking minigame.

Duplicate files remain useful: trade them, share them, or consume an extra copy to improve a damaged file's completeness. Do not turn duplicates into arbitrary research currency.

### Direct crafting rule

Once the recipe and its physical requirements are satisfied, the existing crafting transaction produces a usable weapon. Do not place another weapon-approval activity between crafting and use. The existing firearm-maintenance owner supplies all ongoing condition, cleaning, wear, malfunction, field-strip and repair gameplay.

## Progression rules

- A0-A1 agents can read complete low-tier build files and explain what the player still needs.
- A2 apprentices can repair damaged low-tier files and adapt known families under supervision.
- A3 specialists can unlock bounded variant recipes for known weapon families.
- A4 research cells can create genuinely new families from physical constraints, simulation, field history and independent criticism.
- A5 sovereign lattices can optimize multi-material, sensor, exo, and clan-scale platforms.
- A6 remains theoretical and evidence-gated; it does not bypass manufacturing requirements or the existing firearm systems.
- Combat experience creates useful weapon experience: handling problems, failures, repair history, optic issues and role-specific needs. It never generates a blueprint by kill count.
- A complete found build file unlocks the base recipe. It does not provide the printer, materials, components, power or player skill needed to build it.
- Higher P capability is necessary but never sufficient. R/F/G/M, materials, functional cores, power, tools, specialists and agent competencies gate crafting.
- Every revision carries costs and tradeoffs: mass, bulk, balance, heat, service life, contamination tolerance, recoil recovery, maintenance burden, noise, signature, ammunition compatibility, reliability, repairability, and production burden.

## Playability rules

- Every family must answer two questions in plain language: **why would I carry this?** and **why would I leave it at home?**
- Higher production tier does not mean universally better. Preserve viable early weapons through simplicity, dirt tolerance, low ammunition consumption and easy repair.
- Keep ammunition, magazines, donor cores, cleaning supplies and carried mass meaningful. A gun is not balanced only by damage.
- Use the six-value handling profile for comparison: ready speed, recoil burden, unsupported sway burden, heat burden, dirt tolerance and maintenance burden.
- Let configuration move mass, balance and service burden rather than silently adding bonuses.
- Make automatic fire a tactical choice with heat, ammunition, sound and wear costs.
- Never hide failure behind a flat random jam percentage. Derive it from family, core quality, magazine/ammunition condition, dirt, lubrication, heat, damage and maintenance.
- Late-game difficulty comes from acquiring build files, facilities, cores, material grades and contested resources—not repetitive approval chores.

## Family data contract

Each family includes:

- stable ID, name, role, platform class, originality statement, progression band, rarity and canonical source;
- recovered design-seed categories and minimum evidence quality;
- A-band and agent competency nodes;
- R/F/P/G/M gates plus power, cooling, metrology, workstation and specialist gates;
- abstract component groups, donor constraints, material classes and process modules;
- gameplay strengths, weaknesses, handling envelope, service burden and counterplay;
- ammunition role, operating system, fire modes, target carried mass and feed class;
- exact scope of what the current printer manufactures and which functional core remains required;
- a distinct player-choice statement, maintenance-profile reference and physical wear drivers;
- maintenance hierarchy, action/animation requirements and familiarity links;
- optic, muzzle, sling, hand, exo/mech and inventory interfaces;
- asset route, material states, LODs, collisions, sockets, pivots and debug geometry;
- direct recipe-unlock rule and integration with existing crafting and maintenance owners;
- multiplayer, persistence, migration and exploit tests.

## Unreal implementation guidance

Use versioned Data Assets for family/revision definitions and persistent instance records for weapons/components. Add project-owned adapter interfaces; do not let vendor types or Blueprint-only graphs become authoritative truth. C++ should own build-file state, recipe grants, crafting transactions and persistence. UI/Blueprint may present build files, design choices, weapon parts and workshop assembly.

Developer QA still requires schema validation, recipe-graph checks, asset import, separated-part animation, two independent clients, latency/loss, restart during file repair/crafting, replay rejection, migration, performance, screenshots, video, logs and human playtesting. This verifies the software; it does not add another player activity to weapon crafting.

## Safety and originality

Use original fictional family designs and abstract game data. Do not supply real firearm CAD, dimensions for pressure-bearing parts, chamber geometry, tolerances, toolpaths, printer settings, ammunition construction, conversion methods, or assembly directions that enable real weapon manufacture. Reference real objects only for lawful visual and gameplay study; never copy protected assets or proprietary tuning.

## Acceptance gates

Accept implementation only when the selected family has coherent lineage, physical gates, an authoritative crafting transaction, owner adapters, asset evidence, maintenance integration, multiplayer/persistence evidence, gameplay tradeoffs and no operational fabrication content. Leave every unverified runtime claim open.
