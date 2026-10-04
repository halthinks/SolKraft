---
name: solforge-workflow-consequential-send
description: Carry out an explicitly authorized send action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Execute an authorized send

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact action, the exact target, and the payload before anything is transmitted: the recipient address, channel, or endpoint resolved from an authoritative source rather than autocomplete or a prior thread, and the final content as the recipient will see it, including attachments and links. Confirm that explicit authorization covers this action and this target. Selection of this workflow grants no effect, and authorization for one send does not extend to a different recipient, a modified payload, or a repeated send; widen the request only through the authorizer.

Confirm reversibility and blast radius before acting. A delivered email, message, or webhook generally cannot be recalled, so the pre-send review carries the weight a post-hoc check cannot: re-read the payload for correctness, tone, and unintended recipients (reply-all, stale distribution lists, lookalike addresses), and use a draft, preview, or dry-run mode when the channel offers one. Record the evidence of authorization — who granted it, when, and its scope — so the send is traceable to a decision rather than an inference.

Perform exactly the authorized send, then verify the resulting effect from the channel's own signals. Capture delivery evidence such as a message ID, timestamp, and provider acceptance response, and distinguish acceptance from actual delivery or receipt; a queued message, a saved draft, or a silent API response is not proof the send happened. If the outcome is ambiguous — a timeout, an unclear error, a dropped connection — reconcile whether the first attempt landed before retrying, since a blind retry produces duplicates.

Report the action performed, the exact target, the authorization evidence, and the observed effect, with any unreconciled uncertainty stated plainly. Use [result validation](../solforge-result-validator/SKILL.md) when the delivery claim needs acceptance beyond the observed send evidence itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
