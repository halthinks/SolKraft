---
name: solforge-workflow-launcher-install
description: Design and implement safe acquisition, integrity, prerequisites, install, launch, update, uninstall, troubleshooting, and rollback for verified targets.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Install and launch software safely

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the target product and exact version, host platform and architecture, install scope (per-user versus system-wide), and what completion means — installer exit, first successful launch, service registration, or a working update. Identify the authoritative distribution channel before acquiring anything; a link from search results or a forum post is not a source. Confirm prerequisites — runtime versions, disk, permissions, conflicting existing installs — before starting, not while recovering from a half-failed install.

Acquire from the vendor's official channel or a repository the user already trusts, and verify integrity before executing anything: validate signatures or checksums against the vendor's independently published value, never one copied from the same page that served the file. Prefer the platform's native mechanism — package manager, signed installer, managed store — over ad-hoc scripts; when a script is required, read it before piping it to a shell.

Treat install, update, and uninstall as state transitions. Record the prior state — existing version, configuration, data locations — so rollback restores rather than overwrites. On launch, confirm the running binary reports the intended version and reaches its first usable state. For updates, preserve user data and configuration; for uninstall, distinguish removing the program from deleting user data and never conflate the two. When troubleshooting, capture the actual error before applying a fix, and change one variable at a time rather than stacking untested workarounds.

Verify completion with observed behavior on this host: the launcher runs, reports the expected version, and performs one real function. An installer exit code of zero is weak evidence if the app fails to launch; success on another machine is no evidence here; a rollback path that was never inspected is not a rollback path. Report what was acquired and from where, the integrity evidence, installed version, launch result, troubleshooting applied, and the prior state retained for rollback. Use [installation planning](../solforge-install-plan/SKILL.md) when the underlying method or a staged plan is needed beyond the current task.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
