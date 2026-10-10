---
name: solforge-workflow-consequential-purchase
description: Carry out an explicitly authorized purchase action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Execute an authorized purchase

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact purchase the user authorized: the specific item, vendor or checkout, quantity, price or spending limit, payment instrument, and delivery or account destination. Selecting this workflow grants no effect; before acting, confirm that authorization in the current request names this action and this target — an earlier "go ahead," a graph edge, or an include-all route is not purchase authorization. If the target, price, or instrument is ambiguous or has drifted from what was approved, stop and reconfirm rather than inferring.

Confirm reversibility and blast radius before committing: whether the order can be cancelled or refunded, whether the charge recurs, and which balance, card, or subscription the payment binds. Where a review step exists — cart summary, order confirmation screen, quoted total — inspect it against the authorized terms before final submission, and prefer the least-privileged payment path that satisfies the request. Record the authorization evidence: the user's words, the agreed terms, and the pre-purchase summary you checked.

After submitting, verify the actual effect rather than the attempt. Capture the order confirmation, transaction identifier, charged amount, and the resulting state of the account or delivery target, and reconcile them against the authorized terms. A screenshot of a filled cart is not evidence of purchase, and a bare success message without a verifiable confirmation is weak evidence. If the outcome is uncertain — timeout, ambiguous error, possible duplicate submission — reconcile through the merchant's order history or account statement before any retry; a blind resubmit is a second irreversible effect.

Report the authorization basis, the exact action taken, observed confirmation and charge evidence, any deviation from the authorized terms, and the reversal path (cancellation or refund). If the purchase failed or was declined, report that plainly without inventing an order. Use [result validation](../solforge-result-validator/SKILL.md) for acceptance beyond the purchase evidence record itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
