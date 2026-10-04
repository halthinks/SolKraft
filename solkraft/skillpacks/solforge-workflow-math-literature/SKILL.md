---
name: solforge-workflow-math-literature
description: Map related results, equivalent formulations, known techniques, and unresolved gaps with source provenance.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Map the mathematical literature

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Pin down the exact statement in scope — its hypotheses, definitions, and the class of objects or methods the user cares about — plus the acceptance criteria for the map: breadth versus depth, era, and whether equivalent formulations, techniques, or open problems are the priority. Resolve ambiguous terminology against the user's field before searching; the same name often denotes different theorems across subfields, and a map built on a misread term is wrong from the root.

Anchor the map on primary sources actually inspected, not on surveys or other papers' introductions. For each result record the precise statement with its hypotheses, the proving technique, and a citable location (theorem or section). Separate strengthenings, special cases, and genuine generalizations from cosmetic restatements; verify claimed equivalences at the statement level, because a formulation that quietly drops a side condition is not equivalent. Catalog the standard proof techniques with their hypotheses, typical obstructions, and where each breaks down, and distinguish attributed results from folklore.

Keep provenance honest. A citation taken from an abstract, a survey, or another paper's summary without inspecting the source is weak evidence and must be marked as such. Absence of a result from your search is not evidence that none exists — state the search coverage instead of claiming novelty. Surface contradictions between sources and statements you could not verify rather than smoothing them over.

Report the literature map with per-claim provenance, a synthesis of the technique landscape, the unresolved gaps stated as explicit open statements with conjectured and proved kept distinct, and the items that remain unverified or rest on secondary reporting. Scale depth to the request. Use [research execution](../solforge-run-research/SKILL.md) when the task needs broader source tracking, reproducible searches, or contradiction handling beyond the mathematical reading.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
