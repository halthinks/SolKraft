# SolForge Run Single execution policy

## Authority

The capsule is the maximum authority, not a suggestion. User confirmation may activate authorized high-risk work but cannot add scope, permissions, tools, targets, or budget. A material change requires a newly forged and hashed capsule.

## Integrity

Compute `capsule_sha256` as lowercase SHA-256 of the UTF-8, compact, key-sorted JSON serialization of every top-level field except `capsule_sha256` and `confirmation`. Confirmation is an attestation over that hash. With `--check-sources`, each source artifact must exist and match its recorded SHA-256.

## Confirmation

Require confirmation when `risks.high_consequence` is true or when mutations or external side effects are authorized. Accept only a confirmation object with `author: "user"`, the exact capsule hash, `confirmed: true`, and a nonempty statement. Agent-authored, inferred, stale, or hash-mismatched confirmation is invalid.

## State and budgets

Use only these states: `preflight`, `awaiting_confirmation`, `ready`, `executing`, `verifying`, `adversarial_audit`, `complete`, `blocked`, `declined`, `terminated`. All counters are cumulative. Enforce maximum elapsed seconds, tool calls, rounds, agents, cost, and retries before action. `max_agents` must be positive and no greater than verified desktop capacity.

## Scope and evidence

An action target must equal or be contained by an `in_scope` path or resource. It must not match `out_of_scope`, its action kind must appear in `allowed_actions` and not in `prohibited_actions`, and its tool must appear in `allowed_tools`. Every action records served requirement IDs, target, tool, expected and actual results, evidence, and rollback or recovery. Mutations and external effects additionally require their authorization booleans, confirmation, and a nonempty rollback or recovery method.

Every requirement needs at least one concrete evidence record with a nonempty locator and verification result `passed`. Completion also requires no open actions, no exceeded budget, no unauthorized scope, and a passed audit receipt bound to both the capsule and final state.

## Retries and terminal states

Retry only after recording a materially new hypothesis or mechanism. Stop at `retry_limit`. Finish as `complete` only through acceptance audit, `blocked` for an external dependency, `declined` for policy/authorization conflict, or `terminated` for emergency stop. Never convert absence of evidence into success.
