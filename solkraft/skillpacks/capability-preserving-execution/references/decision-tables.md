# Decision Tables

Use these tables when the correct orchestration choice is not already obvious. No row establishes authority or a maximum effort level.

## Batch, parallelize, or sequence

| Situation | Preferred execution | Reason |
|---|---|---|
| Independent known file reads or searches | Batch or parallelize | One synthesis pass without state conflict |
| Independent current-documentation queries | Batch or parallelize | Reduce repeated retrieval phases |
| Tests with isolated outputs and services | Parallelize | Reduce elapsed time safely |
| One result selects the next action | Sequence | Preserve the true dependency |
| Ordered or irreversible state changes | Sequence behind gates | Preserve ordering and recovery |
| Commands share a port, lock, cache, device, database, or build directory | Isolate or sequence | Avoid nondeterminism and corruption |
| Parallel output would obscure attribution | Sequence or improve attribution | Diagnosability is capability |
| Concurrency or rate limits are uncertain | Inspect first, then bound concurrency | Avoid partial failure and retry churn |

## Choose context breadth

| Evidence state | Action |
|---|---|
| Local symbol and callers are indexed | Read targeted ranges plus interfaces and tests |
| File-level invariants or macros affect meaning | Read the complete relevant file |
| Artifact is generated or minified | Find and inspect its source of truth |
| Failure depends on timing or ordering | Read the complete relevant trace window |
| Excerpt conflicts with observed behavior | Broaden across the adjacent layers |
| External fact may have changed | Retrieve a current authoritative source |
| Summary omits exact material values or wording | Reopen the primary evidence |

Choose the minimum context that preserves the decision, not the minimum token count.

## Choose validation breadth

| Change profile | Minimum posture |
|---|---|
| Tiny deterministic edit | Focused check and direct behavior inspection |
| Shared utility or public interface | Unit plus affected consumer or integration checks |
| Cross-cutting refactor | Characterization, focused checks, and broader suite or build |
| Schema or data migration | Compatibility, representative data, and recovery or rollback |
| Security, authorization, payment, or production-critical change | Negative tests and independent review |
| UI or interaction change | Static checks plus real browser or device inspection |
| Performance change | Correctness plus comparable before and after measurements |
| Flaky or nondeterministic area | Repeated or stress validation with retained evidence |

Expand validation whenever evidence, blast radius, or uncertainty requires it.

## Decide whether to delegate

Delegate only when policy permits it, the work can be bounded, and at least one benefit is material:

- independent domain expertise;
- parallel competing hypotheses;
- isolated implementation alternative;
- noisy evidence collection;
- independent adversarial review;
- separate nonconflicting module.

Keep work in the primary task when it is small, tightly coupled, dominated by shared context, dependent on the same mutable state, or costly to integrate.

## Escalation ladder

1. Recheck assumptions and the exact observation.
2. Improve the discriminating probe.
3. Broaden the relevant context.
4. Add instrumentation or a minimal reproduction.
5. Use a specialized tool or authoritative source.
6. Isolate competing approaches or hypotheses.
7. Seek independent adversarial review.
8. Reconsider the architecture.

Do not repeat the same low-information action at multiple levels.
