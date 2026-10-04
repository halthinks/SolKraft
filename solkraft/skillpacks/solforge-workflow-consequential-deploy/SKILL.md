---
name: solforge-workflow-consequential-deploy
description: Carry out an explicitly authorized deploy action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Deploy to an authorized target

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact deploy action, its exact target, and the artifact being moved: version, commit, image digest, or package identity, plus the source environment it was verified in. Selection of this workflow grants no effect; before acting, confirm explicit user authorization for this action on this target, and record what was authorized, by whom, and when. If the request is ambiguous about the target, the artifact, or the authorization, resolve that before touching anything — never infer a production target from a staging discussion.

Assess blast radius and reversibility before executing: what the deploy touches, who or what depends on the current state, whether a prior version can be restored, and how long rollback takes. If the action is irreversible or the rollback path is untested, say so and get that acknowledged as part of the authorization. Check target health and prerequisites first; a deploy onto a degraded target compounds an existing incident rather than delivering the change.

Execute with the artifact exactly as verified — do not rebuild, retag, or "quickly patch" between verification and deploy, since that invalidates the earlier evidence. Capture the actual commands or pipeline invocations and their output. Then observe the real target: the running version or digest, health and readiness signals, and a functional check against the behavior the deploy was meant to deliver. A green pipeline or a successful upload is not evidence the target changed; a dry-run, plan output, or staged release is not evidence of a live effect.

If post-deploy verification fails, follow the rollback path established during authorization rather than improvising a forward fix under pressure, unless the user explicitly redirects. Report the authorization record, target, artifact identity, observed post-deploy state, verification results, and rollback status. If verification exposes a defect that requires changing code rather than redeploying, use [build](../solforge-build/SKILL.md) for the correction and its verification before a separately authorized redeploy.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
