# DayQ use-based progression contract

## Tier semantics

- T0: ordinary survivor baseline with proper gear.
- T1-T5: connected, universally visible and cross-trainable action unlocks.
- T6: hidden native-only ultimate; requires T5, an origin mastery trial, equipment/resources, and server authorization.

Initial tiers are derived from permanent origin: four native trees at T1 and twelve foreign trees at T0. Shared maximum is T5. Native maximum is T6.

## Evidence contract

Every award contains a stable evidence ID, character, tree/domain, activity, challenge, novelty/context tags, tools/assists, contribution, quality/outcome, risk/cost, optional instruction source, repetition bucket, integrity flags, and awarded practice. Duplicate evidence is idempotently ignored. Server-measured activity is authoritative.

Reduce or reject identical low-risk repetitions, AFK movement, free craft/recycle loops, friendly damage, kill trading, harmless treatment loops, password spam, fake agent jobs, inventory-transfer spam, or safe-room macros. Legitimate failure may teach only when it has stakes and produces a diagnosed new mistake.

## Grants and owners

Nodes unlock actions, recipes, handling, modifications, or tactical options. They reference bounded owner interfaces and do not write underlying state. T6 is powerful but remains constrained by gear, ammunition, tools, power, condition, supplies, time, exposure, and counterplay.

Found firearm field/operator/maintenance manuals use the same grant boundary without becoming a skill-tree tier. A server-authorized readable study records one stable manual-instance/character/weapon-family evidence transaction and grants the family service-knowledge tag idempotently. Progression does not alter weapon condition directly: the weapon owner consumes the grant as a non-stacking one-third avoidable-wear multiplier, while existing maintenance/crafting consumes it as one-third repair and cleaning duration. Duplicate copies, aliases, client requests, rollback and migration cannot stack or replay the grant.

## Persistence and security

The server owns origin, evidence, practice totals, tiers, choices, prerequisites, grants, and respecialization. Use stable transaction IDs and revisions. On projection, remove every unauthorized T6 field before serialization. On import/migration, recompute T6 eligibility from permanent origin; never trust legacy client visibility or grant flags.

Death retention remains configurable until the death owner locks exact familiarity decay. Do not silently decide it.

## Verification matrix

Verify 4 origins x 16 initial tiers, universal T5 reachability, native T6 success, all foreign T6 rejections, duplicate evidence, low-risk rejection, valid varied evidence, reconnect/restart/migration/rollback, simultaneous grants, death during choice, clan/defection invariance, and no required core objective depending on T6.
