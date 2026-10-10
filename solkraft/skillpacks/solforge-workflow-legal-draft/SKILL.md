---
name: solforge-workflow-legal-draft
description: Produce a clearly scoped draft with user scope references, assumptions, review gates, and non-advice boundaries.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Draft legal and policy documents

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the document's purpose and type (policy, agreement, notice, clause set), the parties and audience, the governing jurisdiction and effective date, the controlling sources supplied or already identified, and the user's scope and acceptance criteria. Keep user-supplied facts, assumptions you introduce, and open questions as three distinct lists before drafting; where a controlling source is missing, flag it rather than inventing authority.

Draft from the sources, not from genre memory. Define terms once and use them consistently; structure clauses so obligations, rights, conditions, and exceptions are separable. Distinguish what the source mandates, what it permits as a default, and what is a drafting choice, and mark each drafting choice so the reviewer can see where judgment entered. Use explicit placeholders like [PARTY NAME] or [EFFECTIVE DATE] for facts not supplied; never fill a placeholder with a plausible-looking invention. Scope every provision to the stated jurisdiction and date, and say where the rule is uncertain, split, or changing.

Verify the draft as a document: every legal or factual claim traces to an inspected source, every defined term is used, every cross-reference and section number resolves, and every placeholder is visible rather than silently resolved. A clause copied from a template but presented as tailored is weak evidence of fit; so is a disclaimer standing in for a claim that was never checked. The draft is a work product for review, not legal advice and not an executable instrument — signing, filing, sending, or publishing it is a separate action requiring its own authorization.

Return the draft with its scope statement, the fact and assumption lists, the open questions routed for qualified professional review, and the claims you could not support. Use [legal research](../solforge-workflow-legal-research/SKILL.md) when the controlling sources or authority hierarchy are not yet established well enough to draft against.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Validation evidence and limits: see repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
