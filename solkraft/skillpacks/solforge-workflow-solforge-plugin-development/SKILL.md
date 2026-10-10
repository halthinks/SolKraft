---
name: solforge-workflow-solforge-plugin-development
description: Change, test, package, install, and verify the SolForge plugin product or one of its owned skills through the repository's native development workflow.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Develop the SolForge plugin

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish which surface the change targets — an owned skill's instructions and metadata, the routing catalog, packaging, or the plugin runtime itself — plus the repository checkout, the acceptance criteria, and whether installation into the live host is in scope. Work against the repository's own documented development workflow and its existing test, packaging, and install commands; do not invent parallel tooling when the repository already provides it.

Make the change in source, not in the installed copy, and keep it scoped to the requested behavior. When editing a skill, keep its frontmatter and linked reference paths stable unless the change explicitly renames them, and update any routing metadata whose description no longer matches the changed behavior. For runtime changes, trace the affected entry point and lifecycle before editing. Follow the repository's test requirements and run the checks that observe the changed behavior rather than the ones that merely compile it.

A source-only change is not a release. Package through the repository's packaging path, install through the official local install route, then validate the installed artifact: frontmatter parses, discovery and routing resolve to the new version, and the callable behavior reflects the change. Do not present a passing source-tree test as evidence the installed plugin works, do not edit the installed copy and claim the repository is updated, and do not treat a full host restart as a substitute for reload evidence. Preserve existing sessions on their verified versions and route new work to the new release; legacy transport steps apply only to an explicitly requested legacy protocol.

Report the change, the exact commands and install route used, validation results for the installed artifact, and any surface left unverified. Use [plugin development](../solforge-plugin-development/SKILL.md) when the underlying method supplies procedure this workflow omits.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
