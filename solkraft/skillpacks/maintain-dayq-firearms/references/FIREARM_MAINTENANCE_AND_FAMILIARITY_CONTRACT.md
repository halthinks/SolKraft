# DayQ Firearm Maintenance and Familiarity Contract

## Ownership

- Inventory owns stable weapon, magazine, ammunition, component, tool, supply and manufactured-part identities and transfers.
- The weapon owner owns action state, compatibility, component effects, condition, fouling, lubrication, temperature, contamination, stoppages, field-strip eligibility, functional checks and handling outputs.
- Crafting/repair owns reservation, conservation, fabrication and repair transactions.
- Progression owns evidence, practice, tiers, grants and anti-grind policy.
- Animation owns presentation only.
- The server and persistence journal own commits, revisions, recovery, tombstones and migration.

## Physical maintenance state

Persist weapon ID/profile version, maintenance-session ID/revision, safety/selector/action/feed/chamber state, attached and removed component IDs, component transforms or maintenance-surface slots, hand occupancy, tools, reserved supplies, fouling by region, lubrication by region, corrosion/contamination, heat, wear, diagnosed/hidden faults, active manipulation node, applied work, pauses, interruption cause, reassembly validity, function-check status and audit history.

The weapon cannot fire while its required operating set is incomplete. A removed component is a real inventory or maintenance-surface identity, not an animation-only duplicate. No component may exist simultaneously in the weapon and on the mat.

## Field-strip state machine

Use data-driven states such as `secured`, `unloaded_verified`, `strip_ready`, `disassembly_active`, `inspection`, `cleaning`, `repair_pending`, `reassembly_active`, `function_check`, `serviceable`, and `incomplete`. Family profiles supply the ordered manipulation graph and part relationships from lawful technical references. Store abstract node keys rather than instructional prose.

Each node specifies authoritative prerequisites, occupied hands, required support/surface, eligible tools, start/end component ownership, progress, interruption behavior, animation event key, sound event key, and failure outcome. Server state advances only after validated animation/event timing and transaction checks. Clients may predict hand motion, never part ownership or condition changes.

## Cost and quality

Cleaning consumes bounded supply charges according to fouling, contaminants, weapon family, method, skill and workspace. Repair consumes material/part/tool durability and time according to damaged region and chosen outcome. Field improvisation may restore limited function with reliability, precision, wear or service-life tradeoffs. Full restoration requires the appropriate bench, fabrication and metrology capability.

Replacement parts use family compatibility classes, not scavenger-hunt serial numbers. Printable or machinable outputs require an existing recipe, capable printer/machine, eligible material, finishing, quality inspection and installation. Critical parts may require higher printer, forge/foundry, heat-treatment or metrology tiers; the gameplay exposes capability requirements without providing real manufacturing instructions.

## Familiarity model

Maintain distinct server-owned records:

- `weapon_family_familiarity`: transferable operation knowledge for a mechanism/family;
- `weapon_instance_familiarity`: knowledge of one weapon's controls, balance, zero, quirks and repairs;
- `maintenance_mastery`: diagnosis, strip/reassembly and repair proficiency by mechanism class;
- `marksmanship_practice`: stance/support/breath/recoil and sight-use experience by handling class and optic class.

Evidence includes stable ID, weapon and family, instance, activity, context, risk, challenge, weapon condition, optic/support, outcome quality, faults diagnosed, assists, duration, repetition bucket and integrity flags. Diminishing returns apply to identical low-risk repetitions. Field-strip count is recorded but never grants mastery alone.

Familiarity may affect bounded curves for manipulation duration, diagnosis confidence, part-placement error, reassembly validation, ready transition, optic presentation alignment, initial sway envelope, time to stable sight picture and post-movement/post-shot sway recovery. It never alters projectile truth, intrinsic dispersion, ammunition, damage, penetration or hit validation and never tracks targets.

## Found field manuals

Field, operator and maintenance manuals are physical inventory items with stable identity, condition and provenance. A readable manual is mapped to one supported DayQ weapon family/model and maintenance profile. The first server-authorized study commits one idempotent progression knowledge grant for that character and family; the manual is not consumed and may remain valuable physical clan/trade loot. Item ownership does not become progression ownership.

The user-locked grant is exact and non-stacking:

- `effective_durability_multiplier = 3.0` and `service_interval_multiplier = 3.0` are one shared effect, implemented once as `avoidable_wear_accumulation_multiplier = 1/3`; never apply both multipliers independently or produce 9x service life;
- `repair_speed_multiplier = 3.0`, implemented as authoritative repair-duration multiplier `1/3`;
- `cleaning_speed_multiplier = 3.0`, implemented as authoritative cleaning-duration multiplier `1/3`.

The weapon owner applies wear, maintenance/crafting applies service durations and costs, progression owns the manual-knowledge grant, inventory owns the manual item, and persistence owns the journal/migration. The grant is family/model specific and cannot change projectile truth, damage, penetration, intrinsic accuracy, hit authority, target tracking or ammunition. Duplicate study, aliases, reconnect, rollback and migration must remain idempotent. UI and animation expose abstract DayQ service knowledge only, never real operational or manufacturing instructions.

## Target acquisition and sway

Compute sight-settle state from weapon mass/balance/length, optic mass/height/eye relief, stance, movement history, support, breathing, fatigue, pain, injury, cold, suppression, carried load, clothing, exo assistance, family familiarity, instance familiarity and marksmanship practice. Separate:

1. raise/presentation time;
2. eye-to-sight alignment;
3. initial sway envelope;
4. stabilization/settle time;
5. continuous breathing/postural sway;
6. recoil recovery;
7. movement/turn recovery.

Expose each term in debug telemetry. Skilled characters settle faster and more consistently but do not receive hidden aim snapping or perfect stillness.

## Animation and assets

Every supported firearm production master requires separated field-strip components, interior surfaces visible during normal stripping, component pivots/constraints, hand/contact sockets, maintenance-mat slots, inspection/material masks, fouling/wet/mud/corrosion/wear states, first-person high-detail geometry, third-person proxy/LOD strategy, and animation compatibility metadata.

Create authored first-person sequences for clearing/unloading, family-specific disassembly, laying parts out, inspection, cleaning, repair substitution, lubrication, reassembly, function check and interruption recovery. Use procedural alignment and IK for variation, not to conceal incorrect part relationships. No instant montage may skip authoritative work.

## Multiplayer, persistence and abuse

Server-authorize session start, eligibility, unload/clear, part removal/installation, supplies, repair, condition, function check and progression. Test duplicate/reordered requests, stale revisions, two players touching one surface, theft during maintenance, moving/destroying the surface, damage, death, disconnect, late join, restart, injected crash, lost acknowledgment, rollback, migration and tombstone resurrection.

Recovery must produce a valid old or new state: never duplicated parts, consumed supplies without committed work, repaired weapons without costs, or assembled weapons missing their authoritative component identities.

## Required proof

Require focused automation, a live first-person PIE route, visual inspection of part transforms and hand contacts, two-client authority/observation, persistence/restart and crash matrix, familiarity anti-grind tests, target-settle telemetry, representative performance, and video evidence of novice-versus-expert presentation without projectile or damage differences. The route must also find and study a physical family manual, prove a single non-stacking grant, measure one-third avoidable wear accumulation and one-third repair/cleaning durations, and reject wrong-family, unreadable, duplicate and client-forged grants.
