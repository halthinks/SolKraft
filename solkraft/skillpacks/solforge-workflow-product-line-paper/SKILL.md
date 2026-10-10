---
name: solforge-workflow-product-line-paper
description: Turn a selected, traceable plan into synchronized product-family industrial renders, BOM and power ledgers, a polished DOCX, and a visually verified PDF without drifting from locked decisions.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Produce a visual product-line paper

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish which plan is selected and locked: the variants in the product family, the locked decisions and evidence each specification value traces to, the required deliverables (renders, BOM ledger, power ledger, DOCX, PDF), and the acceptance criteria. Confirm traceability before generating anything; an unselected or contradictory plan is a blocker to resolve, not a gap to fill by invention.

Derive the variant matrix from the locked plan and generate the industrial renders per variant with consistent viewpoint, scale, lighting, and branding across the family, so differences between variants read as design differences rather than rendering artifacts. Build the BOM and power ledgers from the same locked decisions the renders depict: every line item traces to the plan, totals recompute from line items, and no render shows a part, connector, or rating the ledgers do not carry. When a specification value lacks evidence, flag it as an assumption instead of silently choosing a plausible number.

Assemble the DOCX with the family overview, per-variant sections, renders, and ledgers in a stable order, then export the PDF from the final DOCX rather than a parallel source. Verify visually: inspect every rendered page for layout breaks, clipped images, orphaned headings, and overflowing ledger columns, and cross-check each render against its variant's ledger entries. A page-count match or a spot check of one page is not visual verification, and a ledger total typed in rather than recomputed is weak evidence.

Return the DOCX and PDF paths, the variant matrix, assumption-flagged values, and what was visually verified. Read [solforge-product-line-paper](../solforge-product-line-paper/SKILL.md) when the underlying render-and-ledger procedure is needed; a completed equivalent stage need not be repeated.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
