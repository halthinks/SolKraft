---
name: using-superpowers
description: Route an explicitly requested Superpowers workflow to the relevant design, implementation, debugging, or review skill.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Superpowers Workflow Routing

Use this router for an explicitly requested Superpowers workflow. A bounded subagent should follow its assigned task rather than loading this router.

Select the skill that changes how the current task should be handled:

- Unresolved product design: `brainstorming`.
- A requested or dependency-heavy implementation plan: `writing-plans`.
- An existing plan: `executing-plans`; use `subagent-driven-development` only when delegation is authorized and useful.
- An unresolved defect: `systematic-debugging`.
- Requested or repository-required TDD: `test-driven-development`.
- Review feedback: `receiving-code-review`; requested independent review: `requesting-code-review`.
- Missing evidence for a completion claim: `verification-before-completion`.
- Branch integration: `finishing-a-development-branch`; required isolation: `using-git-worktrees`.
- Skill maintenance: `writing-skills`.

Read the selected skill, then only references needed by the task. Do not load skills merely because a keyword overlaps, force a workflow before ordinary answers, or repeat evidence for reassurance.

Use the environment's supported skill-loading mechanism. For an actual tool-name mismatch, consult [Codex mappings](references/codex-tools.md) or [Copilot mappings](references/copilot-tools.md) as appropriate.

Follow the host instruction hierarchy, user scope, and repository contracts. Skills do not override system or developer instructions, grant external-action permission, authorize delegation, or add approval steps to work already authorized.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
