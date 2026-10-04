---
name: solforge-workflow-consequential-delete
description: Carry out an explicitly authorized delete action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Delete an authorized target

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact target and its unambiguous identifier — path, record key, resource ID, or remote object — along with the intended scope and who requested it. Resolve relative or partial references against the real system before acting; an ambiguous target stops the task until it is resolved. Confirm that an explicit effect authorization names this action on this target: selection of this workflow, a plan, or an include-all request grants no authority to delete anything.

Before acting, assess reversibility and blast radius. Check for backups, version history, or restore points that would make the deletion recoverable, and enumerate dependents — references, links, jobs, or shared resources — that the target feeds. If the blast radius extends beyond the authorized target, or the deletion is irreversible without explicit user acknowledgment of that, stop and confirm rather than proceeding. Never widen a narrow authorization to neighboring items that merely seem unused; deleting extra targets is an unauthorized effect, not efficiency.

Execute only the authorized deletion, then verify against the target itself: confirm it is actually absent, that dependents and neighboring objects are intact, and that the answer reflects committed state rather than a cached or eventually consistent view. Record the authorization provenance — who authorized, when, and under what scope — together with the exact target, the action taken, and the observed result. If the outcome is uncertain or the deletion partially fails, reconcile that state before any retry; a blind retry can hit a recreated or different target.

Report the deleted target, the authorization evidence, the verification result, and any scope that was declined or left pending confirmation. Use [result validation](../solforge-result-validator/SKILL.md) when the deletion feeds a broader acceptance claim beyond the observed effect itself.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
