---
name: solforge-workflow-software-target-verify
description: Build and verify exact target artifacts with explicit cross-build, emulator, simulator, and real-target evidence tiers.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Verify software on its exact target

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact target tuple — operating system and version, CPU architecture, ABI and libc, and device class where relevant — plus the identity of the artifact under claim and the evidence tier the request accepts. Pin down what "works on X" must mean: launch, a specific user journey, or performance within bounds. Record the toolchain, flags, and pinned dependencies used for each target build, and hash the produced artifact so later runs can prove they exercised the same bytes.

Build with the target's real toolchain configuration, then escalate through evidence tiers in order. Cross-build success plus static checks — binary format, linked libraries, exported symbols — proves the artifact loads for the target and nothing more. An emulator such as QEMU user-mode or an Android emulator exercises the target ISA and ABI but masks timing, syscall, and driver differences. A simulator is weaker still: an iOS Simulator pass runs host-architecture code and is not device evidence. A real-target run on the actual OS and hardware closes the gap; when hardware is unavailable, state plainly which tier the evidence stops at.

Do not present a clean cross-compile as runtime evidence, a simulator pass as device support, or a rerun of a rebuilt artifact as evidence about the shipped one — compare checksums. Distinguish target failures from harness, emulator, and environment failures, and record the actual command, output, and environment for each tier rather than a bare pass.

Report per target: tier reached, artifact hashes, commands and environments, observed behavior against the acceptance criteria, and the unsupported targets or unverified tiers. Use [cross-platform target verification](../solforge-target-verify/SKILL.md) when the underlying tier procedure is missing; a completed equivalent stage need not be repeated.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
