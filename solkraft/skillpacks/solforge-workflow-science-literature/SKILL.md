---
name: solforge-workflow-science-literature
description: Run a reproducible source search, evidence table, disagreement analysis, and gap map.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Review the scientific literature

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Pin down the exact question before searching: the phenomenon or hypothesis at issue, population and conditions in scope, date range and field boundaries, and the acceptance criteria — what coverage would justify stating a consensus, a contested point, or an unknown. Write inclusion and exclusion criteria explicitly so screening decisions are reviewable rather than impressionistic.

Make the search reproducible. Record each database or index queried (PubMed, Crossref, OpenAlex, Semantic Scholar, arXiv, or whatever the host actually reaches), the exact query strings, filters, and the date run. Deduplicate results, screen titles and abstracts against the criteria, and log exclusion reasons at full-text stage. Snowball from reference lists and citing papers of the strongest sources; stop when new searches return only already-known work, and say so.

Extract per-source evidence into a table: the specific claim, method, sample or effect size, conditions, peer-review or preprint status, and whether you inspected full text or only the abstract. For disagreements, separate genuine contradictions from artifacts of different populations, measures, or definitions, and check retraction and replication status before treating a result as settled. The gap map distinguishes never-studied questions from studied-but-null or underpowered ones.

Treat citation count as a locator, not a quality signal. A claim traceable only to a secondary summary, a review's paraphrase, or model memory is weak evidence — verify the primary source exists and says what is attributed to it; do not present an inspected abstract as full-text reading, and mark paywalled or inaccessible sources as unverified. A selection of only supporting studies is advocacy, not a map.

Return the question and criteria, the search record (queries, dates, hit counts), the evidence table, disagreement analysis, gap map, and unresolved limits. Use [run research](../solforge-run-research/SKILL.md) when the question extends beyond the published record into new data or experiment execution.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
