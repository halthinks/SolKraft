---
name: solforge-workflow-software-test
description: "Design and run software tests when behavior, a fix, or a regression needs verification; select checks proportional to the affected behavior."
---

# Verify software behavior

Use this procedure for repository release gates, pre-merge checks, and CI verification, including preparation of a draft pull request. The PR state does not make the work prose drafting. If the requested output is specifically its title, description, or body, use the appropriate writing skill instead.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Derive checks from the requested behavior, affected boundaries, and plausible failure modes. Inspect existing test commands and fixtures before adding infrastructure. Choose the smallest meaningful unit, integration, or end-to-end check that observes the behavior; a test mirroring implementation statements is weak evidence.

For a defect, reproduce the original failure before the fix when feasible. For a new behavior, assert an externally meaningful result. Follow repository red/green requirements. Include relevant error handling, boundary inputs, state transitions, and compatibility cases when the change could affect them; avoid unrelated exhaustive suites.

Run against the intended checkout, configuration, and artifact. Record the actual command, result, and relevant environment. Distinguish product failures from setup failures, skipped checks, and flaky results. Do not silently rerun a failure until it passes or present a mock as evidence for an untested real dependency.

After a change, rerun invalidated checks. Broaden testing when public boundaries, integration risk, failures, or repository requirements justify it. For visible behavior, inspect the real interface when tests do not establish the requested outcome.

Return verified behavior, failures or untested limits, and reproduction details. Create a test-plan or report file only when requested or required by the repository. Use [result validation](../solforge-result-validator/SKILL.md) for acceptance beyond the software tests themselves.
