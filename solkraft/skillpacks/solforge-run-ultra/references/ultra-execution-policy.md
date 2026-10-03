# Ultra execution policy

Native Ultra is a capability, not a label. Execution is forbidden until a fresh runtime capability attestation proves at least two native Ultra agents and a user-authored authorization binds the canonical capsule plus the complete control contract.

## Environment boundary

Proof-only termination is a development cost-control mechanism for CI, smoke, self-test, and routine skill-validation contexts only. Never apply it to production or a real user-authorized Ultra run. Production executes the complete approved capsule within its verified capability, explicit budget, checkpoint, kill-switch, and acceptance controls.

The budget contract declares exactly one `validation_mode`: `production` or `proof_only_fixture`. Production is the default trust boundary. A proof fixture is accepted only with the runner's explicit `--proof-only-fixture` gate and is rejected whenever `SOLFORGE_ENV` identifies a production/live environment. Its public fixed keys are test data and can never authenticate production work.

## Production trust roots

Production validation requires two independently configured HMAC-SHA256 roots:

- provider capability: `SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_ID` and `SOLFORGE_ULTRA_PROVIDER_TRUST_ROOT_SECRET`;
- user authorization: `SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_ID` and `SOLFORGE_ULTRA_USER_AUTH_TRUST_ROOT_SECRET`.

Each secret must contain at least 32 UTF-8 bytes. The provider signature covers the complete capability payload, including issuance, expiry, capacity, provider proof ID, and runtime-configuration hash. The user signature covers the exact capsule and complete Ultra budget hash; budget extensions receive a separate user signature over both old and new hashes. The keyed signature and its deterministic verification receipt must both pass. A nonempty string, ordinary self-hash, caller claim, wrong-root signature, or recomputed receipt around a fabricated signature is not evidence.

Before new production work, `SOLFORGE_ULTRA_RUNTIME_CONFIG_SHA256` must equal the provider-attested configuration and `SOLFORGE_ULTRA_KILL_SWITCH` must equal `armed`. These live values are gates, not sources of authority.

## Required hard ceilings

- `max_elapsed_seconds`
- `max_tool_calls`
- `max_rounds`
- `max_agents`
- `max_cost_usd`

Every ceiling must be finite and nonnegative; counts and elapsed time must be positive, and `max_agents` must be at least two. The approved budget-contract hash covers the canonical capsule hash, capability-attestation hash, ceilings, armed kill switch, and one-unit lease policy.

Every newly issued governed execution lease also binds a finite per-unit reservation for completion units, elapsed seconds, tool calls, rounds, and retries. Provider usage verification enforces every delta against both that reservation and the cumulative run ceiling. If a provider/control loss prevents accounting, recovery may debit only the reservation already signed into that lost lease; a legacy or malformed lease without a trustworthy reservation is recovery-ineligible. No retry, recovery, or capsule continuation resets a counter.

For app-governed execution, the provider budget is only the immutable outer limit. Each accepted run also carries a canonical inner `runBudget`, `runBudgetHash`, and `runBudgetBasisHash`. A verified accepted completion-unit estimate supplies Low `1`, Medium `3`, High `8`, or Extra's disclosed hard maximum; an Ultra topology increment is included only when an actual accepted source contract supplies and hashes it. Every result is clamped to provider capacity. When no trustworthy estimate exists, use the provider maximum and record the exact fallback reason instead of inventing a low cap. Execution leases, provider usage, checkpoints, continuations, and acceptance bind the inner hashes. Cumulative usage crosses same-program capsule boundaries, so continuation never refreshes or silently raises capacity.

## Authorization

The authorization record must contain the canonical capsule SHA-256, complete budget-contract SHA-256, user-authored confirmation text, confirmation time, and `authorized_by: user`. The executing agent must not manufacture or infer authorization. Reformatting the capsule file cannot change this identity.

## Kill switch and execution leases

Before execution, preserve evidence that the user-controlled kill switch is armed and cannot expand authority. Every native dispatch must use the sole active lease, record exactly one bounded action, and close through a SHA-256-bound checkpoint before reacquisition. Acceptance requires a valid predecessor chain, no active lease, exact checkpoint-to-action coverage, and an armed, uninvoked kill switch. Kill invocation terminates the run and closes any active lease without authorizing cleanup effects.

## Extensions

An extension must preserve the old budget hash, name the new budget hash, state the exact increases and reason, and contain new user-authored confirmation. Never silently roll unused capacity between capsules.

## Termination

Stop immediately on capability loss, any exceeded ceiling, unsafe scope change, missing confirmation, or invalid/stale evidence. System/provider termination does not authorize cleanup mutations unless they were already explicitly included in the confirmed rollback plan. User-directed Stop is a separate controlled suspension: app-only Stop freezes dispatch, a provider checkpoint and workspace fingerprint establish `user_stopped`, and only app-only Resume may issue a fresh lease.

An unaccounted lease is permanently non-resumable and non-acceptable. For provider, control, or capability loss, the run may expose `recovery_pending` only when a last-good zero-work/start boundary or provider checkpoint proves the exact approved plan, capsule, configuration, budget, provider head, cumulative counters, signed per-axis lease reservation, server projection, and all mutation-capable workspace fingerprints. The lost lease, results, phase receipts, and event range remain append-only quarantine evidence. The app-only manual `continue_ultra_from_last_good` decision may start a new lease from that boundary after exact workspace restoration is independently visible and current capability is reverified; it never revives the lost lease. A late provider termination receipt may replace conservative reservation debit with its verified cumulative counters while the run remains pending manual Continue. Loss after a user Stop request but before its provider checkpoint follows this quarantine path; it cannot become `user_stopped` and cannot use user Resume.

## Safe exit after live-control drift

Capability or execution-lease expiry forbids all work under the expired lease. A historical bootstrap lease may be replaced before approval display/recording, initial Start, Resume, or child derivation only through a signed live renewal: reverify historical signer evidence, exact immutable authority, unchanged configuration/provider budget/run budget/basis/full mode, armed kill gate, and current provider capacity, then issue one fresh capability/execution lease. Resume additionally preserves cumulative counters/agents and the provider-receipt head and binds the old/new capability lease hashes into the event chain. This is renewal, never a budget reset. Non-trust-root runtime-configuration/budget drift or a disarmed live kill gate forbids renewal, initialization/start, transition or resume into execution, lease acquisition, new approach derivation, and any other new native dispatch. It does not erase already granted authority or prevent control-plane safety operations. While all immutable hashes, HMAC receipts, capsule/budget bindings, scope, ceilings, and ledger chains still verify against the exact retained signer roots, the runner must continue to allow:

- kill/termination;
- completed or explicitly abandoned lease checkpoint/close (safe pause);
- decline or deny transitions;
- final verification, adversarial audit, acceptance/finish, and non-executing proposals;
- recording an already-completed bounded action and its evidence.

Every safe-exit operation records the observed drift. It must never be interpreted as permission to start another action, reacquire a lease, derive a new route, resume execution, clean up outside the approved rollback plan, or expand authority. Acceptance may finish already-completed work after drift and must bind the drift list into its audit receipt.

Safe exit is not a key-recovery bypass. Loss of the configured attestation or provider-usage verification root fails closed. Trust-root rotation remains acceptable only through an explicitly governed verification-key ring that retains the exact stored key ID and old verification material; the current implementation therefore guarantees safe exit across expiry, budget/configuration, and kill-gate drift while those roots remain available, not across arbitrary secret replacement.
