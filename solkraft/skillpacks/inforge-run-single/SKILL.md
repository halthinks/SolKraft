---
name: inforge-run-single
description: Execute a validated, hash-bound InForge Single execution capsule with one Codex agent. Use when a user explicitly asks to run or execute an output from $inforge-single and the work needs integrity checks, scope and authorization enforcement, risk confirmation, budgets, evidence-backed acceptance, and truthful terminal status without subagents.
---

# InForge Run Single

Execute only a capsule conforming to [references/execution-capsule.schema.json](references/execution-capsule.schema.json). Read [references/execution-policy.md](references/execution-policy.md) before acting.

## Workflow

1. Run `python scripts/verify_bundle.py`, then `python scripts/validate_capsule.py <capsule.json> --check-sources`. Stop on any error. Never repair the bundle or capsule during execution.
2. Run `python scripts/execution_state.py init <capsule.json> <state.json>`. Treat the state file as the execution ledger.
3. Perform capability preflight. Record unavailable tools, credentials, inputs, or permissions as blockers; never pretend capability exists.
4. If state is `awaiting_confirmation`, call the InForge Approval plugin tool `inforge_request_approval`. Pass the exact capsule hash, ID, profile, objective, scope, authorized mutations, external effects, acceptance criteria, prohibitions, and rollback. Also pass (a) a plain-language approval summary stating exactly what the button authorizes and (b) an ordered approval journey built only from observable completed checkpoints and their concrete evidence: bundle verification, capsule validation, capability preflight, scope/effect review, and the final pending user decision. Never expose or invent private chain-of-thought. Stop while its widget is pending. Do not ask the user to copy or retype an attestation sentence.
   - Accept only the widget-generated follow-up containing `APPROVE` or `DENY`, the exact capsule hash, and a receipt SHA-256.
   - On `APPROVE`, add `{"author":"user","capsule_sha256":"<exact hash>","confirmed":true,"statement":"Approved via InForge Approval; receipt <exact receipt SHA-256>."}` to the capsule, revalidate it, and initialize a fresh state.
   - On `Deny`, do not alter the capsule or any target source. Transition the ledger to `declined` and stop.
   - If `inforge_request_approval` is unavailable, remain at `awaiting_confirmation` and report that the InForge Approval plugin must be loaded. Do not substitute a prose confirmation gate.
   - InForge Approval is workflow authorization and remains independent of the host sandbox approval policy.
5. Transition through `ready` and `executing`. Use one agent only. Do not spawn, simulate, or claim subagents. Maintain materially distinct approaches with `execution_state.py approach`.
6. Before each action, use `execution_state.py action` to enforce scope, authorization, and all ceilings. Record actual elapsed time, tool calls, rounds, agent count, and cost. Never perform an action rejected by the script. For a long lane, use a checkpoint-aware runner that atomically records every completed unit; a launch or schedule record is not completion evidence.
7. Record evidence for requirements with `execution_state.py evidence`. Evidence must identify a concrete artifact, result, or observation and its verification method.
8. Transition to `verifying`, run proportional tests, then transition to `adversarial_audit`. Compare every requirement, acceptance criterion, prohibition, mutation, failure, and claim with current evidence.
9. Run `python scripts/acceptance_audit.py <capsule.json> <state.json> --complete`. This is the only path to `complete`.

## Safe pause and outage recovery

- Request cooperative pause at the lane boundary, wait for the lane checkpoint to report `paused`, then run `python scripts/execution_state.py pause <capsule.json> <state.json> --reason <reason> --checkpoint <checkpoint.json>`.
- While the ledger is `paused`, perform no new tool calls, mutations, tests, or agent work for that run.
- Resume only with `python scripts/execution_state.py resume <capsule.json> <state.json> --reason <reason>`. Resume revalidates the approved capsule, bound sources, and exact checkpoint hash.
- If an intentionally regenerated checkpoint must replace the paused checkpoint, use `rebind-pause` with the new path and a concrete validation reason. This stays paused and preserves both hashes; it is never a shortcut around resume validation.
- After an outage, inspect the durable checkpoint and artifacts first. Continue from the first uncheckpointed unit; never infer that an in-flight unit passed.
- If the checkpoint or approved inputs changed, remain paused or transition to `blocked`; do not silently restart from an untrusted state.

Use `blocked` only for a genuine external dependency or unavailable capability, `declined` for policy or authorization conflict, and `terminated` for emergency stop. Do not call partial progress complete. Revalidate and request new confirmation after any material scope or authorization change.

## Controls

- Bind execution to the capsule hash and InForge provenance.
- Preserve unrelated work and capture pre-mutation state and rollback evidence.
- Enforce elapsed-time, tool-call, round, agent, cost, and retry ceilings. Never increase a ceiling without a new capsule.
- Keep an approach registry with `candidate`, `active`, `blocked`, `falsified`, `superseded`, `integrated`, or `accepted` status.
- Stop when acceptance passes; do not manufacture work to consume a budget.
- Return only `complete`, `blocked`, `declined`, or emergency `terminated`, with requirement-level evidence or the exact blocker.
