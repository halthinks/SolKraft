# Independent Research and Mastery loop contract

Each outer cycle has separately inspectable sovereign worker records:

1. **Research plan** — produced only by `solforge-code-research` from repository evidence and reconstructed intent.
2. **Mastery plan** — produced only by `solforge-code-mastery` from its independent completeness and implementation analysis.
3. **Research execution and reinspection** — Research executes its own plan and repeats until convergence.
4. **Mastery execution and reinspection** — Mastery creates and executes its own plan only after Research convergence.

The loop skill schedules workers and preserves traceability. It must never rename itself as either source skill, make Mastery execute Research, combine their plans, discard a worker plan, or pass generic phase prose off as a completed plan.

The required phase order is:

1. `code_research`
2. `research_execution`
3. `research_focused_check_and_reinspect` (repeat 1-3 until convergence)
4. `code_mastery`
5. `mastery_execution`
6. `mastery_focused_check_and_reinspect` (repeat 4-6 until convergence)

Every stored phase names its responsible skill. Every action includes its concrete change, reason, observable result, decisive check, dependencies, and remaining uncertainty. Explicit constraints and landing effects remain in the accepted contract instead of being converted into repetitive non-action narration. The loop remains under one accepted Decision Program until direct user Pause or Stop, scope-changing user steering, or qualified closure. Goal state is irrelevant.

The program maintains a durable outstanding-finding ledger. A cycle cannot omit, rename away, or mark externally non-actionable a finding that the preceding execution left open. Research must provide fresh repository-tagged evidence for every authorized repository. Execution must disposition every current finding exactly once. Closed findings require an explicitly mapped observed file change and a passing focused check in the affected repository. The next cycle may add newly discovered findings, but it may not replace or erase carried findings.
