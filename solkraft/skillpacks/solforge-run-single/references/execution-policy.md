# SolForge Run Single execution policy

## Authority

The capsule is the maximum authority, not a suggestion. User confirmation may activate authorized high-risk work but cannot add scope, permissions, tools, targets, or budget. A material change requires a newly forged and hashed capsule.

## Integrity

Compute `capsule_sha256` as lowercase SHA-256 of the UTF-8, compact, key-sorted JSON serialization of every top-level field except `capsule_sha256` and `confirmation`. Confirmation is an attestation over that hash. With `--check-sources`, each source artifact must exist and match its recorded SHA-256.

## Confirmation

Require confirmation when `risks.high_consequence` is true or when mutations or external side effects are authorized. Accept only a confirmation object with `author: "user"`, the exact capsule hash, `confirmed: true`, and a nonempty statement. Agent-authored, inferred, stale, or hash-mismatched confirmation is invalid.

Use the SolForge Approval plugin's `solforge_request_approval` widget with `Approve scoped mutations` and `Deny`. Accept only its hash-bound receipt and widget-generated user follow-up. A denial never mutates the capsule or target source and terminates the run as `declined`. Do not require the user to copy a generated sentence and do not fall back to a prose gate when the plugin is unavailable. Remain at `awaiting_confirmation` until the plugin is loaded.

SolForge Approval is workflow authorization independent of Codex runtime permissions. Sandbox, network, MCP, connector, and out-of-workspace actions remain subject to the host's separate policy when applicable.

## State and budgets

Use only these states: `preflight`, `awaiting_confirmation`, `ready`, `executing`, `verifying`, `adversarial_audit`, `paused`, `complete`, `blocked`, `declined`, `terminated`. All counters are cumulative. Enforce maximum elapsed seconds, tool calls, rounds, agents, cost, and retries before action. `max_agents` must equal 1.

## Interruption safety and pause

Long-running lanes must write an atomic, hashable checkpoint after every independently verifiable unit. Never mark a scheduled or started lane closed merely because it was launched. A completed action requires its terminal result and evidence; interrupted work remains non-complete.

Honor a safe pause only at a checkpoint boundary with no open or unrecovered action. `execution_state.py pause` binds the ledger to the exact checkpoint path and SHA-256 and records the state to resume. While paused, perform no new actions or mutations. `execution_state.py resume` must revalidate the capsule, confirmation, source artifacts, and checkpoint hash before restoring the prior active state. A missing, changed, stale, or differently ordered checkpoint fails closed and requires explicit revalidation rather than inferred continuation.

When a checkpoint is intentionally regenerated while the ledger remains paused, use `execution_state.py rebind-pause` only after independently validating the replacement. Rebind remains paused, records the old and new hashes plus the reason, and grants no execution authority. Resume still performs the full validation gate afterward.

On process loss or host outage, reconstruct state only from the capsule, execution ledger, atomic lane checkpoint, and concrete artifacts. Never reconstruct authorization or completion from chat history. Rerun at most the last uncheckpointed unit; preserve the completed prefix and all nonpassing evidence.

## Scope and evidence

An action target must equal or be contained by an `in_scope` path or resource. It must not match `out_of_scope`, its action kind must appear in `allowed_actions` and not in `prohibited_actions`, and its tool must appear in `allowed_tools`. Every action records served requirement IDs, target, tool, expected and actual results, evidence, and rollback or recovery. Mutations and external effects additionally require their authorization booleans, confirmation, and a nonempty rollback or recovery method.

Every requirement needs at least one concrete evidence record with a nonempty locator and verification result `passed`. Completion also requires no open actions, no exceeded budget, no unauthorized scope, and a passed audit receipt bound to both the capsule and final state.

## Retries and terminal states

Retry only after recording a materially new hypothesis or mechanism. Stop at `retry_limit`. Finish as `complete` only through acceptance audit, `blocked` for an external dependency, `declined` for policy/authorization conflict, or `terminated` for emergency stop. Never convert absence of evidence into success.
