---
name: solforge-workflow-business-diligence
description: Test the investment or operating thesis against source quality, red flags, counterevidence, and uncertainty.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Stress-test an investment or operating thesis

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

State the thesis in falsifiable form before testing it: the decision at stake (invest, acquire, partner, extend credit, continue operating), the claims the decision depends on, and what evidence would change the answer. Establish the supplied materials — deck, data room, financials, contracts, customer references, management interviews — and the depth the timeline permits. Scale the diligence to the exposure: a small pilot warrants checks proportional to it, not a full acquisition workup.

Triangulate every material claim. Separate primary sources (audited financials, filings, raw usage or transaction data, direct customer calls) from the company's own narrative, and corroborate each load-bearing claim with at least one independent source or mark it unverified. For a revenue thesis, test concentration, churn, deferred revenue, one-time items, and whether bookings were pulled forward; for unit economics, recompute margins from raw inputs rather than accepting blended figures; for market claims, check sizing against independent data rather than the deck's top-down arithmetic. Follow inconsistencies: numbers that differ between the deck and the data room, metrics whose definitions shift between periods, and questions management answers with anecdotes instead of records.

Actively hunt counterevidence rather than cataloging confirmations. A finding sourced only to company-supplied material is weak evidence; absence of discovered red flags is not absence of risk — state what was not inspectable (unaudited periods, withheld contracts, unreachable references) as a limit on the conclusion, not as clearance. Keep facts, inferences, and unknowns distinct, and do not upgrade a plausible explanation into a verified one without the supporting record.

Report the verdict on each claim as supported, undermined, or unresolved, with the evidence behind it; a risk register ranked by severity and likelihood; and the specific evidence that would change the conclusion. Use [run research](../solforge-run-research/SKILL.md) when the diligence plan needs reproducible source tracking or deeper evidence gathering beyond the supplied materials.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
