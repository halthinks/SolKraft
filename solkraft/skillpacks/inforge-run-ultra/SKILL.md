---
name: inforge-run-ultra
description: Execute a validated InForge Ultra execution capsule with verified native Ultra orchestration, explicit user authorization, hard cost and runtime ceilings, evidence-backed acceptance, and an emergency kill switch. Use only when the user explicitly invokes $inforge-run-ultra and supplies a current Ultra capsule; never substitute ordinary agents or higher reasoning for native Ultra.
---

# InForge Run Ultra

Execute only a validated Ultra capsule. Read `references/execution-policy.md` and `references/ultra-execution-policy.md` completely before acting.

## Required procedure

1. Run `python scripts/verify_bundle.py`, then `python scripts/validate_capsule.py <capsule.json> --profile ultra`. Reject bundle or capsule tampering, stale bound artifacts, profile mismatch, added authority, or missing requirements.
2. Verify that the current runtime actually exposes native Ultra orchestration. If it does not, stop with terminal state `blocked`; never substitute desktop subagents, simulated branches, or higher reasoning.
3. Run `python scripts/validate_ultra_budget.py <budget.json> --capsule <capsule.json>`. Require explicit user-authored Ultra authorization bound to the capsule and budget hashes. Never generate that authorization yourself.
4. Initialize the execution state with `scripts/execution_state.py`. Preserve the original request, capsule hash, requirements, scope, authorization boundaries, budgets, and terminal policy.
5. For high-consequence work, remain `awaiting_confirmation` until the user confirms the exact capsule scope, effects, rollback, and acceptance criteria. Bind confirmation to the capsule hash.
6. Execute through native Ultra within the approved elapsed-time, tool-call, round, agent, and cost ceilings. Stop immediately when any ceiling is reached. A higher ceiling requires a new user-authored extension bound to both old and new budget hashes.
7. Maintain approach, action, evidence, blocker, and budget ledgers. Do not treat subagent summaries as evidence without underlying artifacts.
8. Finish early when every acceptance criterion passes. Do not spend the remaining budget merely because it exists.
9. Run `python scripts/acceptance_audit.py <capsule.json> <state.json> --complete`. This is the only path to `complete`, and it requires evidence for every requirement with no unauthorized action, stale evidence, skipped required check, or exceeded budget.
10. Use only `complete`, `blocked`, or `declined` as ordinary terminal outcomes. Use `terminated` for emergency kill or a hard ceiling. Preserve the last safe state and report the exact resume condition.

## Kill switch

On user termination, capability loss, budget exhaustion, unsafe scope expansion, or control failure, stop native Ultra work immediately, record `terminated`, cancel pending work where the runtime permits, and perform no new mutations.

## Release testing

Routine skill tests are proof-only: validate schemas, budgets, capability-gate behavior, state transitions, and kill behavior without launching native Ultra. Native Ultra forward tests require separate explicit user authorization.
