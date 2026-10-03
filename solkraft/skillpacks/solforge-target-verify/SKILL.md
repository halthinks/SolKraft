---
name: solforge-target-verify
description: Verify exact platform artifacts while distinguishing cross-build, emulator, simulator, and real-target evidence.
---

# SolForge Target Verify

Verify exact platform artifacts while distinguishing cross-build, emulator, simulator, and real-target evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Define the source and requested target platform, architecture, versions, exact artifact, and meaning of compatibility. Establish baseline behavior and inspect OS APIs, native dependencies, paths, permissions, processes, lifecycle, and packaging.

Classify concrete coupling points and choose a narrow adapter, shared core, platform shell, or bounded redesign. Preserve existing behavior and public interfaces while changing the requested boundary.

Build with the actual target toolchain and run relevant checks on each available target. Record command, configuration, artifact hash, environment, and observed results; distinguish source inspection, cross-build, emulator, and real-target execution.

Report verified, buildable, adapter-required, redesign-required, unsupported, or unknown status per target, together with remaining checks and rollback. Do not inherit another target result or require a retired route receipt.
