---
name: solforge-workflow-consequential-rotate
description: Carry out an explicitly authorized rotate action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Rotate a credential or secret

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the explicit authorization first: it must name this rotate action and this exact target — the specific key, token, certificate, or secret and the system, account, or environment it belongs to. Selection grants no effect, and authorization for one credential or environment does not extend to another. Identify every consumer of the current value — services, pipelines, configuration stores, local files — and capture how the target authenticates today, so the post-rotation check is defined before anything changes.

Confirm reversibility and blast radius before acting: whether the provider supports an overlap period with two live values, how fast revocation propagates, which consumers fail if the old value dies early, and the exact rollback path if the swap fails midway. Where overlap is supported, stage and distribute the replacement before invalidating the old value; where it is not, sequence the swap to minimize the dead window with rollback ready. Perform the rotation once, against the authorized target only.

Verify the resulting effect, not just the mechanics. A newly generated secret is not a rotation until consumers authenticate with it: make a real authenticated call using the new value, and where retirement is required, confirm the old value is actually rejected. A stored-but-unused value, a success response from the provider console, or a planned follow-up is not evidence of effect. If the outcome is uncertain, reconcile which value is live before any retry — a blind retry can invalidate the value consumers just picked up.

Record the rotation evidence: the authorized target and the basis of authorization, the observed old and new value states, consumers confirmed on the new value, any consumer still on the old value with its cutover plan, and rollback status. Use [build](../solforge-build/SKILL.md) when the replacement credential, rotation automation, or consumer configuration must be created or changed before the rotation can proceed.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
