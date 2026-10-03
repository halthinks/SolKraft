---
name: solforge-workflow-merge-report
description: Inspect candidate and target repositories at real revisions, prove capabilities from implementation evidence, and recommend adoption across architecture, runtime, dependencies, evidence quality, licensing, and risk without mutating code.
---

# Report on repository adoption

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the candidate and target repositories at pinned revisions — record exact commits or tags, not branch names that can move — and the adoption question being asked: adopt a capability into the target, vendor a component, or decline. Capture the acceptance criteria the recommendation must satisfy and any scope limits (modules, platforms, dependency tiers). This is inspection work: do not modify either repository.

Prove each claimed capability from implementation evidence, not from its documentation. Trace the candidate's feature to entry points, call paths, tests, and build configuration; a README promise with no corresponding code, or dead code no path reaches, is not a capability. Then judge fit across the named dimensions: architecture (whether the candidate's structure composes with the target's or forces a redesign), runtime and dependencies (version ranges, platform assumptions, and transitive dependency weight), evidence quality (whether the candidate's own tests and CI actually exercise what would be adopted), and licensing (read the actual license and notice files and determine compatibility with the target's distribution model rather than assuming it).

Keep the comparison at equal footing: same revision discipline and inspection depth on both sides. Treat popularity metrics as context, never as capability evidence. Do not execute candidate code against the target environment as a "proof" — running code is an effect this report does not authorize. Mark what could not be inspected (private dependencies, generated code without sources, undocumented behavior) as an unknown rather than a pass.

Report the recommendation with its evidence chain: capability findings with file-level pointers, integration cost and risk, the license determination, and the explicit limits of the inspection. A well-supported "do not adopt" is a successful report. Read [sol-merge-report](../sol-merge-report/SKILL.md) when the comparison needs more method than this node carries; a completed equivalent assessment need not be repeated.
