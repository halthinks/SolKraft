# SolForge Run Ultra execution policy

## Authority

The capsule is the maximum authority, not a suggestion. User confirmation may activate authorized high-risk work but cannot add scope, permissions, tools, targets, or budget. A material change requires a newly forged and hashed capsule.

## Integrity

Compute `capsule_sha256` as lowercase SHA-256 of the UTF-8, compact, key-sorted JSON serialization of every top-level field except `capsule_sha256` and `confirmation`. Confirmation is an attestation over that hash. With `--check-sources`, each source artifact must exist and match its recorded SHA-256.

The Ultra control contract additionally requires cryptographic provider and user receipts. Ordinary SHA-256 proves content identity, not signer identity. Production therefore verifies both receipts with configured HMAC trust roots before initialization, start/resume, lease acquisition, or derivation. Proof-only fixed keys are permitted only behind the explicit fixture gate and are never production authority.

## Confirmation

Require confirmation when `risks.high_consequence` is true or when mutations or external side effects are authorized. Accept only a confirmation object with `author: "user"`, the exact capsule hash, `confirmed: true`, and a nonempty statement. Agent-authored, inferred, stale, or hash-mismatched confirmation is invalid.

## State and budgets

Use only these states: `preflight`, `awaiting_confirmation`, `ready`, `executing`, `verifying`, `adversarial_audit`, `complete`, `blocked`, `declined`, `terminated`. All counters are cumulative. Enforce maximum elapsed seconds, tool calls, rounds, agents, cost, and retries before action. `max_agents` must be at least two and no greater than the capsule ceiling or verified native Ultra capacity.

Bind state to the canonical capsule SHA-256, complete budget-contract SHA-256, native capability-attestation SHA-256, armed user kill-switch receipt, and single-active-lease policy. A native dispatch requires a matching active lease. Each lease permits exactly one bounded action, must be recorded in a SHA-256 predecessor chain, and must close with a checkpoint receipt before another lease is acquired. Raw capsule file bytes are never the capsule identity.

## Scope and evidence

An action target must equal or be contained by an `in_scope` path or resource. It must not match `out_of_scope`, its action kind must appear in `allowed_actions` and not in `prohibited_actions`, and its tool must appear in `allowed_tools`. Every action records served requirement IDs, target, tool, expected and actual results, evidence, and rollback or recovery. Mutations and external effects additionally require their authorization booleans, confirmation, and a nonempty rollback or recovery method.

Every requirement needs at least one concrete evidence record with a nonempty locator and verification result `passed`. Completion also requires at least two verified agent identities under the portable state-ledger protocol, no open action or active lease, exact action-to-checkpoint coverage, no exceeded budget, no unauthorized scope, an armed and uninvoked kill switch, and a passed audit receipt bound to the capsule, complete budget contract, capability attestation, lease-ledger head, and final state.

## Retries and terminal states

Retry only after recording a materially new hypothesis or mechanism. Stop at `retry_limit`. Finish as `complete` only through acceptance audit, `blocked` for an external dependency, `declined` for policy/authorization conflict, or `terminated` for emergency stop. Never convert absence of evidence into success.

Expiry or live runtime-control drift closes the forward-execution gate but not the safe-exit control plane. Kill, decline, completed/abandoned checkpoints, non-executing proposals, final audit, and recording evidence for an already-completed bounded action remain available while every immutable binding and keyed receipt still passes. No safe-exit command may acquire, dispatch, retry, resume, mutate, or derive more work.
