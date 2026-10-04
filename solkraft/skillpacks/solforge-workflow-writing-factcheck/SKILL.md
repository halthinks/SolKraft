---
name: solforge-workflow-writing-factcheck
description: "Verify factual claims and citations in supplied writing; identify unsupported, outdated, or overstated statements and provide supported corrections."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Fact-check written claims

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the text under review, its audience and purpose, the scope of the check (all material claims, flagged passages, or citations only), and whether the result is a verdict ledger, a corrected draft, or both. Identify which claims are material — those a reader would rely on or that carry consequence if wrong — and note the date the writing treats as "current," since prices, versions, statistics, and roles go stale.

Extract the checkable claims: specific numbers, dates, names, quotations, causal or comparative assertions, and every statement carrying a citation. Skip pure opinion and clearly hedged framing. Verify each claim against the most authoritative available source — primary documents over aggregators, publisher records over summaries — and prefer sources independent of the claim's origin. For cited claims, open the cited source itself and confirm it actually contains the claim; a citation whose source does not support the statement is an unsupported claim, not a verified one. Check quotations verbatim, including ellipses and context that changes meaning.

Classify each claim: supported, contradicted, outdated, overstated, unsupported, or unverifiable with available sources. Overstated covers accurate cores wrapped in stronger language than the evidence bears ("proven" for "suggested," "all" for "most"). A correction must itself be supported; do not replace one unverified figure with another. Do not treat search-result snippets as evidence — read the source. Do not silently rewrite disputed claims in the draft; flag them so the author decides. Label unverifiable claims plainly rather than manufacturing confidence, and record what observation would settle them.

Return a claim-by-claim ledger with verdict, evidence, and source for each material claim, plus the corrected draft if requested with every change traceable to a verdict. State coverage limits: claims not checked, sources unavailable, and checks that expired against live data. Use [research execution](../solforge-run-research/SKILL.md) when settling a claim requires open-ended source discovery beyond the supplied material.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
