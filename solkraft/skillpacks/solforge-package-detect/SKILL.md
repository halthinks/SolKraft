---
name: solforge-package-detect
description: Inspect a repository for runtimes, entrypoints, build systems, dependencies, and packaging options.
---

# SolForge Package Detect

Inspect a repository for runtimes, entrypoints, build systems, dependencies, and packaging options.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Inspect existing manifests, lockfiles, build definitions, entrypoints, and release artifacts before choosing a packaging strategy. Distinguish declared dependencies from installed tools and runnable outputs. Return the detected formats, reproducible commands, target requirements, and actual gaps; discovery alone does not authorize packaging changes.
