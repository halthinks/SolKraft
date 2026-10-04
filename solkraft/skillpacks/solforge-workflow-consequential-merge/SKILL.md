---
name: solforge-workflow-consequential-merge
description: Carry out an explicitly authorized merge action for its exact target and verify the resulting effect.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Merge an authorized change

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact change and target: the repository, the source branch or pull request with its reviewed commit range, the destination branch, and the intended merge method (merge commit, squash, rebase, or merge queue). Then verify explicit authorization for this action against this target — a request to review or prepare a change, a prior approval for a different branch or commit range, or selection of this skill grants no effect. Record the authorization evidence: who granted it, when, and the scope it covers. Confirm the target tip the authorization saw is still the current tip; if it has moved, the authorization must cover the new state before proceeding.

Inspect the merge surface before acting. Check required reviews, status checks, and branch protections rather than assuming they passed; a green mergeable flag from before the latest push is stale. Assess reversibility and blast radius: whether a revert commit or force-push can undo this, what the merge method does to history, and which downstream effects (auto-deploy, release, publication) the target branch triggers. Resolve conflicts deliberately and record any semantic resolution, since a mechanically clean three-way merge can still combine incompatible behavior.

Execute the merge through the real system — the git remote, hosting platform, or queue — never by simulating or announcing it. Then observe the effect on the exact target: fetch and confirm the destination tip is the expected merge commit, confirm the change set is present, and run the post-merge checks the target warrants. A merge queued or still merging is not merged; reconcile any uncertain outcome (timeout, reported conflict, unexpected tip) before any retry, because retrying an already-applied merge can double-apply the change.

Return a merge evidence record: the authorization evidence, source and target identifiers, tip commit before and after, merge method, conflict resolutions, and observed post-merge state, with remaining limits or failed preconditions stated plainly. Use [SolForge Build](../solforge-build/SKILL.md) when a failed merge or conflict requires changing the underlying code before a reattempt.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
