---
name: solforge-workflow-consequential-push
description: Carry out an explicitly authorized push action for its exact target and verify the resulting effect.
---

# Push an authorized change to its target

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the exact action and target before anything moves: what is being pushed (a ref, artifact, message, configuration, or payload), to which destination (remote, branch, registry, queue, environment, or device), and the explicit authorization covering that specific action and target. Selection of this workflow, a graph edge, or an include-all request grants no effect; if the authorization does not name this push to this target, stop and obtain it. Read the destination's current state first so the push is evaluated against what is actually there, not what was assumed.

Confirm reversibility and blast radius before acting. Determine whether the push is a fast-forward or overwrites existing history or state, who or what consumes the destination, and how the prior state would be restored. Prefer the non-destructive form — new ref over force-update, additive publish over replacement — unless overwriting was explicitly authorized. Apply effect-time safeguards the target imposes: protected-branch rules, required credentials, and dry-run or preview modes where the tool offers them. If the observed destination diverges from what the authorization assumed (unexpected commits, a moved target, a stale checkout), stop and re-confirm rather than proceeding on stale assumptions.

Verify the effect on the destination itself, not from the push command's exit status alone: read back the remote ref, query the registry, queue, or device, and compare against the intended state. A successful local command is not evidence of a remote effect, and an "up to date" or silent no-op is not a completed push. When the outcome is uncertain — timeout, partial or missing response — reconcile the actual destination state before any retry; blindly retrying a push whose first attempt may have landed can duplicate or reorder effects.

Record the push evidence: the action, the exact target, the basis of authorization, the observed pre- and post-push state, and the verification performed. Report what landed, how it was confirmed, and any divergence or remaining uncertainty. Use [solforge-build](../solforge-build/SKILL.md) when the push depends on an underlying build or change procedure that must be completed or re-run first.
