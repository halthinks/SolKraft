---
name: solforge-workflow-engineering-prototype
description: Create a requested prototype or design artifact with simulation, test, rollback, and release boundaries.
---

# Prototype an engineering design

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requirements the prototype must demonstrate, the operating envelope (loads, tolerances, interfaces, environment), the materials, processes, and tools actually available, and the acceptance criteria with their measurement methods. Confirm which claims the prototype is expected to settle and which remain model-only; a build that omits its decisive question wastes the effort.

Choose the cheapest artifact that exercises the governing risk: an analytical model or simulation when geometry and physics are well characterized, a bench rig or coupon when a single interface or failure mode dominates, and a full prototype only when interaction between subsystems is the unknown. Fix interfaces and datum references before fabricating, and freeze one configuration per test so results attribute to the change made. Keep the rollback path explicit: version the design files, preserve the last-known-good configuration, and confirm any fabrication, purchase, or hardware effect is reversible or separately authorized before executing it.

Verify against evidence, not intent. Run simulations with stated boundary conditions and a mesh or convergence check before trusting their outputs, then test the physical artifact under the same load cases and compare measured against predicted values. Record instruments and calibration state, configuration and revision tested, and environmental conditions. A simulation that agrees only with itself is not validation; a measurement with unknown sensor error, an unrecorded configuration, or a result from a different build than the one being claimed is weak evidence. Do not extrapolate one passing bench result into a rated capability.

Report what was built, the exact configuration tested, measured versus predicted results, deviations and their likely causes, and the release boundary: which claims are now evidence-backed, which remain assumptions, and what the next iteration must settle. Use [engineering verification](../solforge-workflow-engineering-verify/SKILL.md) for systematic testing of requirements, tolerances, and failure modes beyond the prototype's own checks.
