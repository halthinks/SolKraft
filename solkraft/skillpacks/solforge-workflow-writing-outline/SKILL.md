---
name: solforge-workflow-writing-outline
description: Create a source-aware argument and section architecture matched to audience, purpose, and evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Outline a document

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish audience, purpose, format, and length before structuring anything: a decision memo, a literature review, and a product proposal fail in different ways. Inventory the supplied sources and record what each can actually support, plus the acceptance criteria — what the finished document must let the reader decide or do. Scale section count and depth to the length; a two-page brief does not need a chapter hierarchy.

Derive the argument before the sections. State the central claim in one sentence, then the subordinate claims the reader must accept in order, and only then name sections. Assign each section its job in the argument — establish context, present evidence, handle the strongest objection, draw the conclusion — and the specific sources or data it will cite. Order by reader need, not by source order: an outline that mirrors the sequence the sources were read in is a filing system, not an argument. Allocate a rough word or space budget per section so no section silently absorbs half the document.

Verify the outline as a machine for producing the document: every section carries a claim with named evidence or an explicit gap marker, every supplied source that bears on the thesis has a home, and transitions follow the dependency of claims. Flag claims with no supporting source instead of writing them in as settled. Anti-patterns: topic-label headings with no claim ("Background", "Analysis") that give the drafter nothing to assert; evidence assigned to a section it does not support because it was convenient; a conclusion section promising findings the evidence plan cannot deliver.

Report the outline with per-section purpose, claim, evidence assignments, and word budget, plus unresolved evidence gaps and any places where the available sources do not support the requested angle. Use [drafting](../solforge-workflow-writing-draft/SKILL.md) when the approved outline must become the document itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
