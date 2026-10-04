---
name: solforge-workflow-business-market
description: Build a source-verifiable market and segment view with competitors, demand evidence, and unresolved gaps.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Build the market view

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the decision this market view must support, the target segment and geography, the time horizon, and the economic assumptions the requester already holds. Fix the market boundary and its taxonomy before collecting numbers: which products, buyers, and substitutes count as inside, and which adjacent categories are explicitly excluded. Record the acceptance criteria for the market_landscape and opportunity_brief so completeness is judged against them, not against volume of material gathered.

Size the market from at least two independent directions — a bottom-up build from buyer counts, usage rates, and observed prices, and a top-down decomposition of industry figures — and reconcile the two rather than averaging away a divergence; the gap usually exposes a definitional error. Map competitors from primary evidence: actual pricing pages, product documentation, customer reviews, and filings, not their own positioning statements. Gather demand evidence from observable behavior such as search trends, community discussion, job postings, and sales or waitlist data where accessible. Date-stamp every source, since market figures decay quickly.

Verify every material claim against a source that can actually be inspected; a figure cited through an aggregator or blog roundup without the underlying report is unverified. Anti-patterns that invalidate this deliverable: presenting a top-down-only estimate as market truth, treating a competitor's claimed traction as measured demand, quoting one segment's growth rate for the whole market, and silently widening the market boundary to reach an impressive total. Keep facts, inferences from those facts, and open unknowns visibly separated; a gap that cannot be closed with available sources is reported as a gap, not papered over.

Report the market_landscape with segment definitions, sizing ranges and their derivation, the competitor map with evidence per claim, and the opportunity_brief stating where demand evidence is strong, weak, or absent. State the staleness window of the sources and which assumptions most strongly drive the conclusion. Use [research execution](../solforge-run-research/SKILL.md) when source tracking, contradiction handling, or reproducible searches need the full underlying procedure.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
