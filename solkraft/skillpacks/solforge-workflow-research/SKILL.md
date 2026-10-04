---
name: solforge-workflow-research
description: Extend the prompt result through source-backed research, claim-evidence mapping, contradiction analysis, and explicit uncertainty.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Extend a result with source-backed research

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact question or claims to extend, the supplied evidence, the scope (domains, depth, recency), and the requested deliverable — evidence brief, research synthesis, or decision analysis — plus what finding would settle the question. Decompose the objective into individually checkable claims before searching; an unfalsifiable prompt yields an unfalsifiable brief.

Prefer primary sources (papers, filings, standards, official documentation, raw data) over aggregators, and record provenance for every source: locator, publisher, date, and the specific passage relied on. Search for disconfirming evidence with the same effort as confirming evidence, checking dates and applicability for time-sensitive claims. Weigh sources by authority, independence, and method rather than by how well they support the emerging answer.

Map each claim to its supporting and contradicting evidence. Resolve contradictions through source quality, recency, and scope, or carry them as explicitly unresolved. Keep facts, inferences, and unknowns distinct, and attach confidence and freshness to each claim. A claim resting on an uncited secondary summary or on model recollection is weak evidence; an absence of search results is not evidence of absence; do not silently drop a source because it contradicts the preferred conclusion, and do not present a quotation the source passage does not contain.

Report the deliverable with claims mapped to evidence, per-claim confidence, unresolved contradictions, and coverage gaps. Reuse valid prior research rather than repeating it. Use [solforge-research](../solforge-research/SKILL.md) when the underlying evidence-gathering procedure needs deeper guidance.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
