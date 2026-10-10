---
name: solforge-workflow-whitepaper-to-readme
description: Convert an evidence-rich report into a progressive-disclosure README package with source-bound claims, verified commands and links, preserved user scope boundaries, supporting docs, and a compression ledger.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Convert a whitepaper into a repository README

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the source report and its evidence base, the target audience and purpose, the repository the README will live in, and the user's acceptance criteria and scope boundaries before writing. Read the source closely enough to know which claims its evidence actually supports and which are aspiration, roadmap, or marketing, and to find its stated limitations — a README that drops them misrepresents the system. Confirm what the user excludes from disclosure, such as credentials, internal infrastructure, or unreleased detail, and treat those boundaries as constraints on every section.

Structure for progressive disclosure: a short statement of what the project does and for whom, a quickstart a newcomer can actually run, then pointers into supporting docs that carry the architecture, evidence, and detail the README compresses out. Bind each material claim to specific evidence in the source; where the source itself is unverified, say so or drop the claim rather than launder it through the summary. Run every install, build, and run command you print, in the environment the README targets, and fetch every link. Move overflow detail into the supporting docs instead of lengthening the README, and keep a compression ledger recording what was condensed or omitted, where it went, and why, so the conversion stays auditable.

Verify the package against the source, not against its own prose: each claim traces to evidence, each command was observed to work, each link resolves, and each limitation and scope boundary survives. A command copied from the source without running it is an untested command, not a verified one; a claim supported only by another summary is weak evidence; a fluent README that loses a stated limitation is a failed conversion, not a successful one.

Report the package contents, the commands and links verified and how, the compression ledger, and any claims left unsupported or scoped out. Use [solforge-readme](../solforge-readme/SKILL.md) when the underlying README composition method is needed beyond this conversion procedure.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
