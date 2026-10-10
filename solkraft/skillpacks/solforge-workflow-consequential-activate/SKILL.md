---
name: solforge-workflow-consequential-activate
description: Carry out an explicitly authorized activate action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Activate an authorized target

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact activate action and its exact target: the service, feature flag, account, schedule, subscription, or integration being enabled, identified precisely (resource ID, account, flag name, environment) rather than as a class of thing. Selection of this workflow grants no effect; before acting, confirm explicit user authorization for this action on this target, and record what was authorized, by whom, and when. Authorization for a different target, a staging activation, or an earlier similar request does not transfer; if the target, scope, or authorization is ambiguous, resolve that first.

Capture the pre-state and assess reversibility and blast radius before enabling. Record the current off or disabled state so the target can be restored, and confirm the prerequisites activation assumes — credentials, billing, dependencies — are actually in place. Trace what activation turns on downstream: jobs that run, traffic that flows, features users immediately see. Distinguish a reversible toggle from an activation that commits state, such as starting billing or provisioning non-deletable resources; if the effect is irreversible, say so and get that acknowledged in the authorization.

Execute through the real control plane — the actual API, console, CLI, or scheduler — never by simulating or announcing it. Then observe the effect on the exact target: query its state directly, confirm it reports active, and exercise one real behavior the activation was meant to enable. An accepted API response or a checked console box is not evidence of the effect; a scheduled job is active when it is confirmed scheduled or has run, not when the schedule was saved. Reconcile any uncertain outcome — timeout, ambiguous status, partial activation — before any retry, because retrying an already-applied activation can double-provision or double-bill.

Return an activation evidence record: the authorization evidence, exact target identifier, pre- and post-state observations, the verification performed, and rollback status or remaining limits. If activation exposes a defect that requires changing code or configuration before the target can safely stay live, use [SolForge Build](../solforge-build/SKILL.md) for the correction, then re-obtain authorization for the reattempt.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
