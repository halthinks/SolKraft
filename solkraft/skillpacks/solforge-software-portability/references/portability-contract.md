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

## Verification bindings

Identify the source baseline, chosen strategy, target, build configuration, exact artifact, and decisive acceptance checks. Attach concrete build and runtime evidence to each claimed target. A route receipt, Blender finalActionGoal, or external registry is not required.

Buildable and verified status must cite the corresponding observed results. Preserve rollback and compatibility boundaries; publication, store submission, device-farm use, or deployment requires the applicable task authority.
