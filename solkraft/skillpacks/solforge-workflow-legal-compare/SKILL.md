---
name: solforge-workflow-legal-compare
description: Compare rules, implementation, evidence, risks, and applicability without flattening jurisdictional differences.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Compare jurisdictions and policies

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact question being compared, the jurisdictions or policy instruments in scope, the effective date for each, and the user's purpose and acceptance criteria. Comparison is meaningless without a fixed unit: hold the question constant and answer it separately for each side before synthesizing. Confirm which sources are controlling — constitution, statute, regulation, case law, agency guidance, or contractual text — and pin each claim to a specific provision and date, not to a general impression of how the system works.

For each jurisdiction, work the authority hierarchy in order and distinguish the rule on the books from its implementation: enforcement practice, published interpretations, and open litigation often diverge from the text. Check effective dates, pending amendments, transitional rules, and preemption or supremacy questions before treating a provision as current. Where legal traditions differ — common-law versus civil-law reasoning, mandatory rules versus default rules, registration versus use-based rights — preserve the structural difference instead of forcing both sides into one template. Apply identical criteria to every side; asymmetric scrutiny is the most common way a comparison quietly becomes advocacy.

Verify every material claim against a primary or clearly attributed source. A summary, blog post, or model recollection is not evidence of the rule; when only secondary coverage is available, mark the claim unverified rather than launder it into fact. "No source found" is not "no rule exists" — state the search performed and the residual gap. Do not flatten genuine conflicts into false equivalence, and do not present the comparison as legal advice; flag the questions that require qualified counsel in the relevant jurisdiction.

Report the comparison with each side's rule, its source and effective date, the material differences and their practical consequences, and the risks or applicability limits of acting on the result. State unresolved conflicts and evidence gaps plainly. Use [the comparison method](../solforge-run-comparison/SKILL.md) when the task needs its symmetric-criteria procedure beyond the legal sourcing discipline here.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
