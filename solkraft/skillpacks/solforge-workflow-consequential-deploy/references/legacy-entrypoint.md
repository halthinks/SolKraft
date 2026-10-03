---
name: solforge-workflow-consequential-deploy
description: "Execute only the selected deploy effect, preserve exact request provenance, and return effect evidence. Use the Deploy a release workflow alone or combine it with any other compatible capability."
---

# SolForge Workflow: Consequential Deploy

Execute only the selected deploy effect, preserve exact request provenance, and return effect evidence.

## Native workflow

- Domain: `general`
- Action family: `deploy`
- Environment: `available_external_system`
- Typical outputs: `deployment_evidence_record`.
- Suggested starting skill: `$solforge-build`

1. Translate the objective and supplied inputs into concrete work for this workflow.
2. Load the suggested starting skill and any other useful native skills. The suggestion is not exclusive.
3. Inspect dependencies and group independent work into safe parallel waves when useful.
4. Execute with real tools and preserve unrelated user work.
5. Verify every material output and state any unsupported or incomplete claim plainly.
6. Return the result directly; do not substitute a routing artifact for the requested outcome.

## Effect-time behavior

This workflow can create an external or destructive effect. Use it only when the current user request names the exact action and target, and follow ordinary host safeguards at effect time.

## Composition behavior

- This workflow may run alone, alongside other workflows, or as part of an include-all route.
- Add, remove, reorder, repeat, or parallelize compatible capabilities as the objective requires.
- Apply direct user Pause, Resume, and Stop instructions immediately.
