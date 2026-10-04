---
name: solforge-workflow-writing-review
description: "Review or revise supplied writing for logic, clarity, structure, consistency, and evidential support while preserving the intended meaning."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Review and revise writing

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the piece's audience, purpose, and format, the acceptance criteria for the review, and the permitted scope of revision — audit only, line edits, or restructuring. Distinguish what the author must decide (argument, emphasis, claims) from what the reviewer may fix (grammar, consistency, clarity). Read the whole piece before judging any part; a passage that looks redundant often carries a later section.

Audit the argument before the prose. State the thesis as the draft actually presents it, then check each section against it: does every section advance the purpose, does each material claim carry support, and do citations resolve and say what the draft attributes to them. Look for contrary evidence the draft omits, hedges that hide an unsupported claim, and structure that buries the point the audience came for. Only then work line-level: clarity, consistent terminology and voice, and transitions.

Preserve intended meaning as a hard constraint. A revision that strengthens, weakens, or narrows a claim is an error, not an improvement; flag it for the author instead of making it silently. Do not report personal style preference as a defect, and do not mark a claim supported because the prose sounds confident — support means a source or reasoning you inspected. Flag what you cannot verify rather than passing it silently.

For revision, apply the agreed changes, then reread the corrected draft against the audit: every accepted issue resolved, no new errors introduced, meaning intact. Return the editorial audit with issues located and severity-ordered, the revision plan, and the revised text when requested, stating plainly which flagged items remain unresolved. Use [writing fact-check](../solforge-workflow-writing-factcheck/SKILL.md) when flagged claims need independent source verification beyond what the review can inspect.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
