<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Execution Playbooks

Adapt these patterns to the governing workflow. Omit irrelevant steps and add any work required by the mission.

## Repository implementation

1. Extract the behavior change, acceptance criteria, protected scope, and repository rules.
2. Locate implementation owners, callers, contracts, tests, schemas, configuration, and generated boundaries.
3. Group safe independent discovery into one evidence wave.
4. Choose the smallest architecture-consistent design and edit implementation and affected tests coherently.
5. Inspect the complete diff.
6. Run focused checks, affected integration checks, required build or packaging checks, and the actual behavior.
7. Perform an adversarial pass before declaring completion.

Do not assume the first matching file owns the complete subsystem.

## Debugging and incident diagnosis

1. Reproduce or directly observe the failure and retain the exact error, inputs, environment, and expected behavior.
2. Separate symptoms from causes and retain all materially plausible hypotheses.
3. Batch independent probes that discriminate among hypotheses: logs, traces, configuration, code paths, recent changes, minimal reproductions, and dependency health.
4. Fix the root cause at the correct layer and add regression coverage or observability when practical.
5. Confirm the original failure is gone, exercise adjacent failure paths, and check for silent degradation.
6. Record containment, rollback, or recovery status when the work affects a live incident.

## Refactor or migration

1. Inventory modules, consumers, contracts, schemas, configuration, tooling, tests, deployment boundaries, compatibility requirements, and ordering constraints.
2. Capture baseline behavior with characterization tests, outputs, snapshots, benchmarks, or contract checks.
3. Partition work into independently verifiable stages.
4. Use adapters or compatibility phases when risk warrants them.
5. Validate each stage before irreversible progression.
6. Remove temporary compatibility only after every consumer has migrated and recovery evidence is sufficient.

## Performance optimization

1. Define workload, hardware, environment, metric, and required invariants.
2. Measure and profile before changing anything.
3. Change the causal mechanism with attribution preserved.
4. Measure afterward under comparable conditions.
5. Check correctness, tail behavior, memory, reliability, and regression risk.

Do not infer a performance improvement from design prose, micro-tests, or proxy metrics.

## Research and technical decisions

1. Define the decision, timeframe, constraints, and evidence standard.
2. Distinguish stable facts from facts that require current verification.
3. Retrieve primary or authoritative sources in safe independent waves.
4. Reconcile versions, terminology, and disagreement; label inference explicitly.
5. Tie the recommendation to constraints, tradeoffs, failure modes, uncertainty, and validation steps.

Continue only while missing evidence could materially change the decision.

## Data analysis

1. Define grain, population, units, windows, and metric formulas.
2. Inspect schema and source provenance.
3. Profile missingness, duplicates, outliers, join cardinality, and temporal coverage.
4. Reconcile totals against an independent source or invariant when available.
5. Keep raw, transformed, and presentation layers distinct and reproducible.
6. Validate displayed tables and charts against underlying values.

## Frontend and visual work

1. Inspect the existing design system and responsive conventions.
2. Implement requested states, interactions, accessibility, loading, empty, and error behavior.
3. Run static and focused functional checks.
4. Inspect the real rendering at representative sizes and content lengths.
5. Check console, network, keyboard, focus, and failure behavior.
6. Repair visible defects and inspect again.

## API or integration work

1. Inspect both sides of the contract.
2. Account for authentication, authorization, idempotency, pagination, timeouts, retries, rate limits, and error mapping as applicable.
3. Exercise representative success, client-error, server-error, malformed-input, and safe-failure paths.
4. Sequence state-changing requests unless ordering and idempotency are proven.
5. Confirm observability at the affected boundary.

## Multi-agent work

1. Confirm delegation is allowed and materially useful.
2. Give each worker non-overlapping scope, authoritative inputs, allowed writes, an evidence contract, and completion criteria.
3. Isolate worktrees or mutable state where needed.
4. Require concise findings, patches, commands, and validation evidence rather than transcript dumps.
5. Reconcile assumptions, integrate changes, run cross-boundary checks, and complete the final adversarial review centrally.
