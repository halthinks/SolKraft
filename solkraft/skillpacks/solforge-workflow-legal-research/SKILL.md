---
name: solforge-workflow-legal-research
description: Map controlling sources, source authority hierarchy, interpretations, uncertainty, and jurisdictional limits.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Research a legal question

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Frame the question before searching: the jurisdiction whose law controls, the governing domain (statutory, regulatory, common law, constitutional), the as-of date that matters, and the user's scope boundaries and acceptance criteria. Legal answers are jurisdiction- and time-bound; if the jurisdiction or date is missing, resolve it by targeted inquiry or state the assumption explicitly.

Orient with secondary sources (treatises, practice guides, law review articles) to find the terminology and leading authorities, then work in primary law. Rank sources by authority: constitutions, statutes, and regulations control over case law; within case law, binding precedent from the governing jurisdiction and court level outweighs persuasive authority from other jurisdictions, and holdings outweigh dicta. Trace each statutory claim to the current codified text and each case claim to the opinion itself. Check the subsequent history of every case relied on — whether it has been overruled, abrogated by statute, or distinguished — and note where circuits or jurisdictions split.

Verify every material proposition against the source it is cited to, with a pinpoint citation. A secondary source's summary of a holding is weak evidence of what the court actually decided; an unverified citation is no evidence at all — confirm that each cited authority exists and supports the proposition attributed to it. Do not present an open question as settled law, a plurality or dissent as controlling, or agency guidance as binding when its status is contested. Keep established law, reasonable inference, and genuine uncertainty as separate categories.

Report a research memo: the question as scoped, the controlling authority ranked by jurisdiction and weight, conflicting interpretations and splits, the points that remain uncertain or undecided, and the jurisdictional limits of every conclusion. Name what was searched and what remains unchecked. Use [run research](../solforge-run-research/SKILL.md) when the collection itself needs reproducible search tracking across many databases beyond this authority mapping.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
