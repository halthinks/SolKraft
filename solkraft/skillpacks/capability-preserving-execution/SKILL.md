---
name: capability-preserving-execution
description: Orchestrate substantial multi-step coding, debugging, research, migration, and validation work with dependency-aware waves, selective recovery, and evidence-based completion while preserving capability. Use when a task spans multiple tools, files, systems, hypotheses, implementation stages, or validation layers. Do not use for simple explanations, rewrites, calculations, or tiny isolated edits unless explicitly invoked. Yield to specialized skills and repository workflows.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Capability-Preserving Execution

## Purpose

Reduce avoidable model/tool round trips, repeated context processing, redundant reads, and low-information retries without reducing correctness, coverage, safety, insight, validation strength, or completion probability.

Optimize waste, not work.

## Preserve capability and authority

- Follow system, safety, user, repository, environment, and specialized-skill instructions first.
- Treat this skill as orchestration guidance, never as execution authority.
- Preserve every tool, source, test, hypothesis, interface, and specialist needed for the outcome.
- Never impose fixed limits on reasoning, tools, agents, searches, files, tests, or validation.
- Prefer the more capable path whenever an optimization could materially weaken the result.
- Keep Pause, Stop, approval, permission, production, and destructive-action boundaries authoritative.

### Escape from a harmful optimization

Suspend or relax this skill's efficiency defaults immediately when they block necessary discovery, reasoning, implementation, debugging, recovery, or validation.

No additional permission is needed to relax this skill's own defaults. This escape hatch does not expand authority, waive approvals, permit external or destructive actions, authorize delegation against active policy, or override a governing workflow.

## Run the adaptive loop

### 1. Frame

Establish the requested outcome, observable acceptance criteria, constraints, prohibited changes, affected boundaries, risk, reversibility, and evidence that must be observed directly.

Resolve ordinary ambiguity from evidence and established conventions. Ask only when a material product, policy, authority, or irreversible choice cannot be inferred safely.

### 2. Map

Maintain a compact working ledger of:

- governing instructions and acceptance criteria;
- relevant architecture, paths, contracts, and current evidence;
- hypotheses and material uncertainty;
- changed state and completed checks;
- unresolved dependencies and the next unblocked frontier.

Distinguish read-only work from state changes and identify ordering, shared-state, rate-limit, and isolation constraints.

### 3. Wave

Collect the presently known, useful, safely independent operations at the current dependency frontier.

Batch or parallelize only when operations:

- do not depend on one another's output;
- do not mutate or contend for the same state;
- remain individually attributable and diagnosable;
- can fail independently without obscuring recovery.

Sequence work when a result determines the next action, state changes are ordered, a safety gate must pass, resources conflict, or parallel output would weaken diagnosis.

### 4. Synthesize

Preserve successful results, separate facts from interpretations, update the ledger, rank remaining hypotheses, and select the smallest next probe set that can resolve material uncertainty.

Retry only failed or inconclusive operations unless a shared precondition invalidated the whole wave.

### 5. Act

Inspect enough surrounding context to understand callers, interfaces, invariants, tests, configuration, generated-file boundaries, and compatibility expectations.

Apply coherent architecture-aware edits. Update affected tests, types, schemas, fixtures, configuration, and documentation together when required. Avoid unrelated refactors and inspect the complete diff.

### 6. Verify

Use evidence proportional to risk:

1. nearest syntax, format, type, schema, or static checks;
2. focused unit or component tests;
3. affected integration or end-to-end checks;
4. required broader suite, build, packaging, migration, or deployment checks;
5. direct inspection of the real output or behavior.

After a repair, rerun checks invalidated by that repair. For visual work inspect the rendering; for APIs exercise success and failure paths; for performance compare equivalent before/after measurements; for migrations verify compatibility and recovery.

### 7. Escalate or finish

Escalate capability instead of repeating low-yield actions. Broaden context, improve probes, add instrumentation, use a better tool or authoritative source, isolate alternatives, or add an independent review when evidence conflicts or progress stalls.

Finish only when the requested outcome is delivered and the definition of done is satisfied.

## Preserve context and observability

- Prefer targeted searches, indexes, structured output, diffs, and relevant ranges.
- Read complete files, traces, logs, or additional sources whenever excerpts could hide material semantics.
- Reuse evidence only while its source state remains unchanged and current.
- Do not build opaque compound commands merely to reduce call count.
- Keep intent, working directory, output, exit status, and errors attributable.
- Do not suppress failures unless absence is intentionally treated and recorded as data.

Repeat an operation when state changed, earlier evidence was incomplete, evidence conflicts, or repetition is itself the test. Do not repeat it for reassurance alone.

## Delegate only for a concrete benefit

Use subagents only when higher-priority instructions permit them and bounded delegation adds specialization, independent hypotheses, isolated implementation, adversarial review, or meaningful elapsed-time savings.

Define the objective, authoritative inputs, scope, allowed tools and writes, evidence contract, completion criteria, and conflict-avoidance mechanism. Keep shared mutable state isolated and integrate and validate the whole result in the primary task.

## Definition of done

Before finalizing:

- satisfy or explicitly account for every material acceptance criterion;
- run relevant checks and inspect real behavior where applicable;
- review the coherent diff or system change;
- test likely edge cases and failure boundaries;
- perform one adversarial pass for stale evidence, hidden dependencies, regressions, unsafe assumptions, and omitted validation;
- repair defects found and rerun affected checks;
- state material uncertainty, skipped checks, and environmental limits honestly.

Report the delivered outcome, important changes, observed validation, direct inspection evidence, and remaining material risk. Never claim completion from plans, code inspection, queued work, or packaging checks alone when the real result can be exercised.

## Load references only when needed

- Read [decision-tables.md](references/decision-tables.md) when batching, context, validation breadth, or delegation is ambiguous.
- Read [playbooks.md](references/playbooks.md) for task-specific execution patterns.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
