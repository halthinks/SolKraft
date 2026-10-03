---
name: solforge-workflow-software-native-port
description: Port shared behavior through explicit native platform adapters and verified target builds.
---

# Port software to native platforms

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the shared behavior to be ported, the exact target platforms (operating system, architecture, toolchain versions), and the acceptance criteria — typically that each target produces the same observable behavior, not merely a compiling artifact. Inventory the existing platform seams: filesystem, process spawning, UI, storage, permissions, lifecycle, and any conditional-compilation already present. Identify which differences are essential to the platform and which are incidental, and reuse existing adapters and completed port stages rather than repeating them.

Define or extend an explicit adapter interface at each seam, keep the shared logic free of platform assumptions (path separators, line endings, endianness, locale, process models), and place every platform-specific implementation behind the adapter. Decide dispatch deliberately — compile-time selection per target versus runtime detection — and resist conditional-compilation sprawl, which hides untested combinations. Build each target with its actual native toolchain, not a cross-check on the host alone.

Verify behavior per target, not per build. A green compile or a test pass on one operating system is not evidence of parity on another; run the behavior checks that exercise each adapter on the real target, and do not present a mock or shim of a platform API as evidence for behavior on that platform. Where the same input produces legitimately different output per target, record the difference as intentional with its reason; treat unexplained differences as port defects. Follow repository build and test requirements and rerun invalidated checks after adapter changes.

Report the ported adapters, per-target build commands and toolchains, verified behavior with its evidence, intentional divergences, and any target that remains unbuilt or unverified. Use [platform adapter](../solforge-platform-adapter/SKILL.md) for the underlying adapter implementation detail when the port needs it.
