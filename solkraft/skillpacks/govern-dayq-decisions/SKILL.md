---
name: govern-dayq-decisions
description: Record and reconcile DayQ design decisions, locked intent, ownership, and dependencies.
---

# DayQ Decision Governance

Turn open questions into explicit, traceable decisions. Never silently decide canon or merge incompatible product identities.

Read [decision-contract.md](references/decision-contract.md). For canon-sensitive decisions also read `../direct-dayq-content/references/dayq-canon.md`.

## Workflow

1. Resolve the DayQ workspace root from `DAYQ_ROOT` or the nearest current-directory ancestor containing `docs/DAYQ_REQUIREMENTS_LEDGER.md` and `dayq/skills`. Locate the requirement at `$DAYQ_ROOT/docs/DAYQ_REQUIREMENTS_LEDGER.md` when available.
2. Identify upstream dependencies and refuse to lock a downstream assumption before its required parent decision.
3. Generate materially distinct options. Include the current recommendation and a credible alternative.
4. Select the evidence method: creative direction, systems analysis, prototype, simulation, playtest, or current primary-source research.
5. Recommend one option using explicit criteria. Do not average incompatible concepts into an undefined hybrid.
6. Record owner, milestone, evidence, options, decision, rationale, consequences, acceptance criteria, status, and reopening conditions.
7. Propagate the decision to affected system sheets, schemas, prototypes, models, and tests.
8. Reopen a decision when later evidence violates its acceptance criteria; preserve the earlier record.

## Rules

- Treat user declarations as authoritative creative decisions unless they conflict or require feasibility proof.
- Separate a provisional default from a tested decision.
- Do not mark implementation-dependent questions `passed` from prose alone.
- Exclude staffing and budget from creative scoring unless they materially change feasibility; still record platform, service, certification, and legal constraints.
- Keep fictional geopolitical and elite actors publishable; preserve causal specificity without relying on living real people as villains.

## Output

Write a decision record conforming to the reference contract, update the ledger status, and list downstream artifacts that must change.
