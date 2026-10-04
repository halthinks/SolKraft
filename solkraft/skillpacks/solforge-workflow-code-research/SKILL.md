---
name: solforge-workflow-code-research
description: "Router-selected SolForge workflow node: audit a whole codebase or ecosystem for intended architecture, hidden capabilities, inconsistencies, and completion gaps, producing the code research package."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Audit a codebase for intended design and completion gaps

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish scope: the repositories and checkouts in bounds; what "complete" means here (requirements, shipped API surface, design documents, contracts implied by callers and tests); and which outputs the request names among the code research package, design envelope, completion gap matrix, and remediation master plan. Treat intended design as a claim to reconstruct from evidence: docs state intent, exported interfaces and wiring reveal it, tests show what was expected to work. Scale breadth to the request; a bounded question does not need exhaustive coverage.

Reconstruct the architecture from real import and call graphs, not directory layout or README structure; dead code, orphan modules, and stale entry points mislead. Inventory hidden capabilities: features implemented but undocumented, unexposed, or behind flags, and seams where the design anticipated extension. Label each finding explicit in the sources or inferred from usage. For the underlying method, read [solforge-code-research](../solforge-code-research/SKILL.md) when it supplies missing procedure; a completed equivalent stage need not be repeated.

Find inconsistencies and gaps by confronting intended design against actual behavior: contracts that implementations violate, documented features without working call paths, integrations abandoned mid-wiring, duplicated subsystems that diverged. Classify each finding by evidence — observed in code or execution, inferred from structure, or unresolved — and by consequence, not file count. A finding quoted from a docstring without checking the code it describes is weak evidence; a count of TODO markers is not a completion matrix. Do not infer "broken" from "unused" until callers and configuration are searched; run the code paths you can when a behavior claim is material.

Compile from verified findings: the design envelope as the evidence-supported end state, the gap matrix with each gap tied to its blocking dependencies, and the remediation plan ordered so no step assumes an unverified earlier step. Do not execute remediation; the audit defines gaps and acceptance evidence, it does not authorize changes. Report what was audited, what each material claim rests on, and what remains unverifiable. When remediation is authorized, hand the gaps and acceptance evidence to [code mastery](../solforge-code-mastery/SKILL.md).

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
