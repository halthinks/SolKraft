---
name: solforge-build
description: Implement requested features, bug fixes, automation, or local artifacts; use when changing working code and verifying the result.
---

# SolForge Build

Implement requested features, bug fixes, automation, or local artifacts; use when changing working code and verifying the result.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requested behavior, accepted scope, source identity, existing work, affected callers, and observable acceptance criteria. Inspect the relevant implementation and tests before choosing changes.

Order authorized changes by dependencies. Work in coherent units, preserving public contracts and state ownership. For behavior changes, reproduce the defect or add the required failing behavior test before implementation.

Verify each changed boundary with decisive checks, then inspect the actual user journey or artifact. Reuse still-valid evidence; repair failed acceptance rather than restarting completed stages.

Deliver the demonstrated result, exact verification commands and outcomes, and remaining blockers. No fixed iteration count, mandatory capsule, approval widget, or invented orchestration is required.
