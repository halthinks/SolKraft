# Portability contract

Preserve a tested behavioral baseline before changing platform boundaries. Record every coupling by component, kind, source platform, target platform, and evidence.

| State | Meaning |
|---|---|
| `verified` | Real target executed the accepted behavioral suite |
| `buildable` | Target artifact built; runtime behavior is not yet fully verified |
| `adapter_required` | Shared behavior is viable after explicit platform abstraction |
| `redesign_required` | UI, lifecycle, storage, permissions, interaction, or system model must change |
| `unsupported` | No bounded truthful route exists with current constraints |

Prefer shared core plus narrow adapters when behavior is portable. Prefer platform shells when user experience or lifecycle differs. Use compatibility runtimes only when their operational dependency and limitations are acceptable. Every claim must state the exact OS, architecture, runtime, evidence tier, and known gaps.

## Executable bindings

Compilation requires the complete verified Blender `finalActionGoal` and a cryptographically intact accepted route receipt. Each target binds one `selectedStrategyId`; a result using a different route is rejected. `topChoices` shows three options while `allChoices` preserves every Advanced route.

Evidence kinds are allowlisted and every passed record requires a SHA-256. Buildable or verified targets require behavior baseline, adapter contract, cross-build, rollback, and compatibility-report evidence; verified additionally requires real-target evidence. Unknown result fields and unauthorized commit, push, publication, store, device-farm, hosting, or deployment claims fail closed.
