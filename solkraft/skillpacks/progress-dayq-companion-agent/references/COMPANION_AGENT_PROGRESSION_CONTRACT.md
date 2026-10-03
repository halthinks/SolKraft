# DayQ Companion Agent Progression, Conversation, and Combat Voice Contract

## Core fantasy

The player's named companion grows from a fragile local assistant into a trusted field partner, research specialist, weapons designer, and eventually a suit-local tactical intelligence. The relationship is interactive: the player talks with the agent, reviews what it learned, chooses its doctrine and specialties, hears timely battlefield guidance, and brings signed field evidence home to improve the next certified revision.

The agent remains physical and bounded by its checkpoint, Edge Interface, sensors, compute, memory, radios, power, cooling, tools, infrastructure, training, evaluation, permissions and trust state.

## Separate axes

Never collapse progression into one AI level.

- A0-A6: physical/organizational capability band.
- Branch rank: learned competency in one skill branch.
- Certification: permission to perform a bounded role.
- Doctrine: player-selected behavior and priorities.
- Trust: provenance, integrity and deployment state.
- Field bond: pilot-agent coordination and familiarity.
- Equipment envelope: actual sensors, actuators, compute, radios and tools.

## Seven skill branches

1. **Fieldcraft:** terrain reading, navigation, cover, vertical routes, weather risk, extraction and uncertainty-aware scouting.
2. **Combat Sense:** authoritative sensor fusion, threat prioritization, stance/support advice, target reacquisition timing, suppression awareness and retreat decisions.
3. **Weaponsmith:** diagnosis, maintenance coaching, configuration analysis, failure pattern recognition and agent-designed weapon candidate quality.
4. **Fabrication:** salvage substitution, process planning, metrology, machine scheduling, quality evidence and repairability.
5. **Research:** evidence curation, hypothesis formation, counterfactual simulation, independent criticism and experimental design.
6. **Command and Signal:** radio discipline, channel support, concise reports, squad coordination, translation, authentication warnings and contested-network behavior.
7. **Suit and Drone Integration:** power/heat/load prediction, sensor management, drone tasking, exo/mech coordination, damaged-mode assistance and recovery.

Each branch has six ranks, C0-C5. C0 is untrained. C1-C3 are broadly attainable. C4 requires an A3 certified specialist and advanced infrastructure. C5 requires an A4+ research/training cell, a branch mastery evaluation, physical tools and a signed checkpoint revision. Rank never grants unavailable hardware, hidden information, items, authority, or free designs.

Every node must change something the player can see or do. Store:

- the action the player gains;
- the information or option the agent adds;
- the outcome used to test whether it helped;
- the cost, uncertainty or opportunity tradeoff;
- the owning system that remains authoritative.

Do not grant invisible percentage bonuses such as extra damage, perfect aim, generic crafting speed or a global research multiplier.

## Advancement loop

1. Server-authoritative gameplay records signed evidence episodes with novelty, difficulty, stakes, outcome, contribution, sensor provenance, counterplay and integrity flags.
2. The Edge Interface summarizes candidate lessons without changing permanent capability.
3. During a safe conversation, the companion explains what it observed, how certain it is, and which two or three branch choices are available.
4. The player selects a doctrine or skill direction. Choices must have visible benefits, opportunity costs and later cross-training routes.
5. A secured base training job reserves checkpoint, dataset, compute, memory, power, cooling, time, trainer, evaluator and backup.
6. Held-out tests may pass, fail, expose overfitting or create a remediation plan.
7. Certification signs a new immutable revision. Deployment is transactional and rollback-safe.
8. Field use measures benefit and counterplay. A failed result remains useful only when it produces diagnosed, novel evidence.

The conversation is the progression screen. The player should be able to ask: "What did you learn?", "What will this unlock?", "What will it cost?", "What are you less certain about?" and "What do I give up by choosing it?" The agent answers with concrete gameplay changes from the node definition.

Reject duplicate episodes, staged kills, low-risk repetition, AFK time, replayed telemetry, alt-account farming, client-authored awards and evidence from sensors the agent did not possess.

## Conversation UI

The Edge Interface and suit UI provide:

- a persistent name, voice, identity, trust and current revision;
- text and optional speech input routed through bounded intents;
- a conversation timeline separating memory, hypothesis, advice, command request and confirmed action;
- evidence cards with source, age, uncertainty, contradictions and privacy scope;
- skill-tree view with prerequisites, costs, alternatives and owner effects;
- training proposal comparison and player confirmation;
- doctrine controls for verbosity, risk tolerance, engagement, privacy, squad sharing, interruption and emergency priority;
- after-action debrief with scrubbed timeline, mistakes, successes, counterfactuals and research leads;
- damaged/offline fallback and deterministic authored dialogue when no generative service is approved.

Core gameplay must not depend on a cloud model. A deterministic structured-intent and authored/parameterized response system is the baseline. Any runtime generative service requires a separate user decision and privacy, moderation, latency, cost, platform, offline and security evidence.

## Audible combat guidance

Voice events are short, interruptible, evidence-bound and priority-queued:

- emergency: immediate physical danger, catastrophic suit state, friendly-fire risk;
- critical: confirmed threat, power/heat failure, weapon obstruction, lost support;
- tactical: uncertain track, cover/route option, reload or maintenance concern, drone/sensor change;
- advisory: weather, fatigue, logistics, objective or formation suggestion;
- debrief-only: hypotheses, long explanations, skill proposals and design insights.

Every event carries stable ID, category, priority, source observations, confidence, age, expiration, required permissions, audience/channel, cooldown, dedupe key, interruption rule, caption, spatial/radio treatment and acknowledgment state. Stale or contradicted events must expire or be corrected audibly. Other players hear only what the channel and physical audio rules authorize.

Limit ordinary combat callouts to information that changes an immediate decision. Repeated contact updates collapse into one corrected message. Low-priority advice waits behind weapon sounds, player speech and emergency warnings. Players can independently tune tactical verbosity, noncritical callouts, captions and voice volume without changing authoritative outcomes.

The agent may advise on a target or firing solution but may not invent observations, see through occlusion, cancel recoil, aim/fire autonomously without a separately approved doctrine, or bypass the weapon owner.

## Weapon-design loop

Combat and maintenance episodes may produce design insights such as ergonomic conflict, contamination weakness, optic retention issue, repair bottleneck, excessive carried burden or unreliable component behavior. A Weaponsmith/Research companion can convert these into variant choices. The player chooses a direction, the agent completes its design job, and the resulting recipe uses the ordinary crafting and maintenance systems.

The companion's progression improves diagnosis, uncertainty calibration, option quality, test selection and integration. It does not linearly increase damage or accuracy and does not print a gun from nothing.

For weapon design, the playable ranks are:

- C0-C1: read manuals and recognize obvious maintenance conditions;
- C2: rank likely stoppage causes;
- C3: repair damaged build files;
- C4: offer competing variants based on real use and maintenance;
- C5: manage a clan weapon family, shared parts and recalls.

## Authority and persistence

The server owns agent identity, revision, branch ranks, certifications, doctrine, evidence, field bond, proposals, training jobs, evaluation, grants, deployment, backup, capture, quarantine, revoke and migration. Clients display permitted projections and request actions. They cannot award evidence, edit ranks, forge dialogue outcomes, reveal protected T6-like data, or install revisions.

Persist stable IDs and revisions for agent, checkpoint, branch node, evidence episode, conversation, choice, training job, evaluation, certification, deployment and rollback. Test restart at every irreversible edge, lost acknowledgment, duplicate requests, simultaneous choices, late join, capture, theft, quarantine, restore, schema migration and tombstone rejection.

## Unreal implementation guidance

Use Data Assets/Tables for branch/node/dialogue/voice definitions; persistent records for instances and evidence; C++ for authoritative validation, jobs, grants, transactions and projection; UI/Blueprint for conversation, tree, evidence cards, subtitles and voice presentation. Integrate with Edge Interface, Enhanced Input, audio/MetaSounds, voice-chat abstraction, sensor observations, exo/mech, weapons, research, player progression and existing persistence through adapters.

Validate deterministic dialogue fallback, menu/controller accessibility, captions, volume/verbosity controls, hearing-accessibility cues, noisy-combat intelligibility, event priority/deduplication, two clients receiving only authorized messages, network loss, restart, anti-farming, performance and human comprehension. Capture logs, screenshots, video, state dumps and observed defects. Design prose is not runtime proof.

## Acceptance gates

Accept only when progression is evidence-driven and physical, every branch maps to existing gameplay owners, dialogue choices have real tradeoffs, combat voice uses only authorized observations, field learning cannot self-modify permanently, signed training/revision transactions survive failure, counterplay remains intact, and live Unreal/multiplayer/persistence evidence exists for the implemented slice.
