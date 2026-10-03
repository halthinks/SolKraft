# Decision contract

## Dependency order

1. Product identity.
2. Player-experience contract and core loop.
3. Death, persistence, and multiplayer structure.
4. Combat and survival.
5. Building and economy.
6. AI, factions, map, and progression.
7. Technical architecture.
8. Vertical slice and playtest revisions.
9. Product, platform, and legal conclusions.

## Required record

```yaml
id: stable-kebab-id
question: what must be decided
status: proposed|testing|decided|rejected|reopened
owner: authority role or user
dependency_milestone: upstream decision or evidence gate
evidence_method: direction|analysis|prototype|simulation|playtest|research
evidence_required: []
options:
  - id: option-a
    description: materially distinct choice
    benefits: []
    costs: []
recommendation: option-id
decision: option-id-or-null
rationale: concise causal explanation
consequences: []
acceptance_criteria: []
reopen_when: []
artifacts_to_update: []
```

Product identity must explicitly answer camera, realism, PvP/PvE, server population, clan size, map size, platforms, commercial model, resets, session length, audience, visual tone, and rating. Score the three baseline concepts—Hardcore Survival, Accessible Clan Survival, and Strategic Survival MMO—against appeal, uniqueness, development cost, technical risk, content burden, monetization compatibility, and team capability before selecting one primary identity.
