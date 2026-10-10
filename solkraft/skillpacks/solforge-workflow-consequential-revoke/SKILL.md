---
name: solforge-workflow-consequential-revoke
description: Carry out an explicitly authorized revoke action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Revoke a credential or access grant

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact target: the specific credential, key, token, session, or grant identifier; the principal it belongs to; and the system that enforces it. Then verify explicit effect authorization — the current request must name this revoke action and this target; a selection-graph edge, an include-all route, or a general cleanup instruction grants no effect. If the target is ambiguous (several tokens for one principal, similarly named keys), resolve its identity from the system's own listing before acting rather than guessing.

Confirm reversibility and blast radius before the call. Determine whether revocation is reversible (a disable that can be re-enabled) or final (key destruction, certificate revocation), whether it takes effect immediately or only after cached tokens expire, and what depends on the credential — running automation, deployed services, other sessions for the same principal. Prefer the reversible form when the system offers one and the request allows it, and revoke the minimum scope authorized rather than the principal's entire access.

Execute the revoke once against the exact target, then verify the effect from the enforcing system's own state rather than from the API's success response: attempt an operation with the revoked credential and observe the denial, or list the grant and confirm it is absent or marked revoked. An acknowledgment without an observed denial is weak evidence, a cached or offline rejection is not proof of server-side revocation, and revoking one token does not establish that the principal's other tokens or live sessions are invalid. Never retry an uncertain outcome without first reconciling whether the first attempt already took effect.

Record a revocation evidence record: who authorized the action, the exact target, the time, the call made, and the observed post-revocation denial. Report what was revoked, the supporting evidence, residual access still held by the principal, and any follow-on. Use [rotate](../solforge-workflow-consequential-rotate/SKILL.md) when a replacement credential must be issued — that is a separate effect requiring its own authorization.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
