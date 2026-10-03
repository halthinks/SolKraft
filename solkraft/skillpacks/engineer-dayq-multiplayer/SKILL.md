---
name: engineer-dayq-multiplayer
description: Design or implement DayQ multiplayer authority, networking, persistence, and server behavior.
---

# DayQ Multiplayer Engineering

Prefer authoritative, observable, recoverable state over client trust and hidden editor behavior.

Read [multiplayer-contract.md](references/multiplayer-contract.md) and the relevant system sheet before changing architecture.

## Workflow

1. Define authoritative owner, state schema, identity, update cadence, relevance, and persistence boundary.
2. Define client prediction, interpolation, reconciliation, rollback limits, and degraded-network behavior.
3. Make item transfers and construction changes transactional and idempotent.
4. Persist stable identifiers, versions, checksums, and audit events needed for recovery and anti-duplication.
5. Implement restart recovery, interrupted-action recovery, migrations, and corruption quarantine.
6. Load-test realistic world distributions, not only empty-server actor counts.
7. Inject latency, jitter, loss, duplication, reordering, disconnects, and crash faults.
8. Record server tick, CPU, memory, bandwidth, database writes, recovery time, and integrity failures.

## Rules

- Never trust client inventory, damage, crafting completion, placement legality, or loot ownership.
- Keep distant AI and bases in cheaper simulation tiers with deterministic promotion.
- Design anti-cheat as layered detection, authority, auditability, and moderation evidence—not secrecy alone.
- Treat every migration as reversible until post-migration verification passes.

## Output

Deliver architecture records, schemas, implementation, fault tests, capacity evidence, pass/fail results, and remediation.
