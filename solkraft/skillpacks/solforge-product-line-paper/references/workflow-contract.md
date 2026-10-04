<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Visual Product-Line Paper Workflow Contract

## Source authority

The accepted plan is the immutable source of truth. Bind its absolute path,
actual byte SHA-256, and acceptance reference before generating the execution
directive. Re-read and re-hash it at finalization.

Locked decisions are preserved verbatim in original order. Assign
`LOCK-001`, `LOCK-002`, and so on. Structure may be added around a decision,
but a synonym, shortened paraphrase, renamed concept, or visually convenient
substitute does not replace it.

## Product-family and view manifests

Each family member has a stable ID, exact name, plan references, and role. Each
required view has a stable ID, purpose, framing, and one or more family-member
IDs. A family lineup may cover several members; each member must also have at
least one individually attributable render.

## Canonical derived data

Create these machine-readable artifacts before final document acceptance:

- canonical content manifest;
- render manifest;
- BOM ledger;
- power/runtime ledger;
- locked-decision traceability manifest.

The content manifest controls terminology, family IDs, component IDs, facts,
estimates, assumptions, captions, and paper structure. DOCX and PDF artifacts
must record its exact SHA-256.

## Industrial renders

Use `$imagegen` built-in mode. Issue one call per distinct asset or variant.
Use the `product-mockup` taxonomy unless the accepted plan explicitly requires
another style. Keep a shared style anchor across the family: camera language,
lighting, backdrop, material vocabulary, scale cues, and negative constraints.

Every final render must be a project-bound PNG with:

- artifact hash and dimensions;
- exact prompt and prompt SHA-256;
- required-view and family-member bindings;
- source-plan and locked-decision references;
- inspection status for subject, family consistency, composition, text,
  invariants, and avoid-list compliance.

Generated imagery is illustrative evidence, never proof of engineering
feasibility, compliance, dimensions, performance, or manufacturing readiness.

## BOM and power

Every family member has at least one BOM item and one power/runtime budget.
Each BOM item records quantity, unit, sourcing/price basis, estimate status,
evidence, and affected family members.

Each power budget records named loads and duty cycles. For a battery budget:

`average_load_w = sum(load_w * duty_cycle)`

`usable_energy_wh = capacity_wh * conversion_efficiency * (1 - reserve_fraction)`

`runtime_h = usable_energy_wh / average_load_w`

Finalization checks these equations within numeric tolerance. Mains and passive
budgets require an explicit reason that runtime is not applicable.

## Paper package

Required sections:

- executive summary;
- accepted-plan authority and locked decisions;
- product-family overview;
- visual language and render gallery;
- family-member specifications;
- system and interface architecture;
- BOM and cost;
- power and runtime;
- user experience;
- manufacturing and serviceability;
- validation and evidence;
- risks, assumptions, and unresolved gaps;
- traceability appendix.

Create a polished DOCX with `$documents`, then render and inspect every page.
Create or export the final PDF, then use `$pdf` to render and inspect every PDF
page independently. The final package must contain the DOCX, PDF, five
machine-readable manifests/ledgers above, final render PNGs, and QA page PNGs.

## Acceptance

Before delivery, verify:

1. accepted-plan identity and prompt identity;
2. locked-decision coverage;
3. product-family and required-view coverage;
4. render file bytes, PNG dimensions, prompts, and inspections;
5. BOM evidence and power arithmetic;
6. required paper sections;
7. canonical manifest bindings for DOCX and PDF;
8. contiguous, individually clean DOCX and PDF page QA;
9. artifact bytes and hashes;
10. semantic-preservation and cross-artifact synchronization audits.

Bind the final report claims and inspections to the actual delivered artifact bytes. Revalidate changed outputs.
