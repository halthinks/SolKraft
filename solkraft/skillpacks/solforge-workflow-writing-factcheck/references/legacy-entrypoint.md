---
name: solforge-workflow-writing-factcheck
description: "Verify material claims against authoritative sources and expose unsupported, stale, or disputed statements. Use the Fact-check claims workflow alone or combine it with any other compatible capability."
---

# SolForge Workflow: Writing Factcheck

Verify material claims against authoritative sources and expose unsupported, stale, or disputed statements.

## Native workflow

- Domain: `writing`
- Action family: `verify`
- Environment: `available_tools_and_sources`
- Typical outputs: `fact_check_ledger`, `corrected_draft`.
- Suggested starting skill: `$solforge-run-research`

1. Translate the objective and supplied inputs into concrete work for this workflow.
2. Load the suggested starting skill and any other useful native skills. The suggestion is not exclusive.
3. Inspect dependencies and group independent work into safe parallel waves when useful.
4. Execute with real tools and preserve unrelated user work.
5. Verify every material output and state any unsupported or incomplete claim plainly.
6. Return the result directly; do not substitute a routing artifact for the requested outcome.

## Composition behavior

- This workflow may run alone, alongside other workflows, or as part of an include-all route.
- Add, remove, reorder, repeat, or parallelize compatible capabilities as the objective requires.
- Apply direct user Pause, Resume, and Stop instructions immediately.
