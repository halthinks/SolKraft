---
name: solforge-workflow-launcher-package-matrix
description: Build reproducible native, runtime-bundled, container, and ecosystem artifacts without overstating platform support.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Build the launcher package matrix

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requested targets before building: platform and architecture pairs, package formats (native installers, runtime-bundled applications, container images, ecosystem packages for npm, pip, Homebrew, winget, or similar registries), signing and notarization obligations, and the acceptance criteria per target. Read the existing build configuration, lockfiles, and CI definitions before adding packaging infrastructure; scale the matrix to what was asked rather than every conceivable target.

Build each artifact from a clean checkout with a pinned toolchain, and record the exact command, toolchain versions, and source revision per artifact. Decide per target whether the runtime is bundled or resolved at install time, and confirm a bundled artifact actually carries its dependencies rather than silently resolving them from the build host. For container targets, build per-architecture images and assemble the multi-arch manifest instead of tagging a single-arch build as universal. Apply signing and notarization where the platform requires it and record the credential basis used.

Verify claims, not just builds. Install and launch each artifact on its claimed target, or document the closest equivalent environment actually exercised; a successful compile or a green CI badge is not evidence the package works. For reproducibility, rebuild from the same revision and compare digests, or name the specific nondeterministic inputs (embedded timestamps, ambient toolchains, network-fetched dependencies) that prevent a match. Do not list a platform as supported because compilation succeeded without a launch check, and do not present an artifact built on a developer machine with ambient state as reproducible.

Return the matrix of artifact, target, build command, digest, and verification status, with unbuilt or unverified targets stated plainly as such. Use [package build](../solforge-package-build/SKILL.md) when a target needs the underlying per-platform build procedure beyond this matrix.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
