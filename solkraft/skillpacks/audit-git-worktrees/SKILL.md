---
name: audit-git-worktrees
description: Produce a deterministic, evidence-bound, read-only inventory of every Git worktree registered to a canonical repository, including existence, HEAD, branch or detached state, lock/prune metadata, dirty-row count and sample, and whether each HEAD is an ancestor of canonical HEAD. Use when auditing parallel-agent or multi-worktree development, reconciling abandoned or externally created worktrees, deciding what must be preserved before cleanup, or verifying repository topology without modifying worktrees.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Audit Git Worktrees

Preserve the hardware project post-Grok worktree-audit process as a reusable, fail-closed skill.

## Run the audit

1. Resolve the canonical repository explicitly:

   ```powershell
   git -C <candidate-root> rev-parse --show-toplevel
   ```

   Never infer the root from a stale handoff path or the current working directory.

2. Record canonical `HEAD` and `git status --short` before interpreting other worktrees.

3. Run the bundled audit, writing its JSON outside the repository unless the user authorized a repository artifact:

   ```powershell
   python -B <skill-dir>\scripts\audit_worktrees.py --repo <canonical-root> --output <absolute-output-json>
   ```

4. Require exit code `0` and `failures: []`. Treat any `unreadable:<path>` row as incomplete evidence, not as permission to remove that worktree.

5. Review every row, not only the summary. Use:

   - `status_rows == 0` for a clean worktree;
   - `status_rows > 0` for a dirty worktree requiring preservation and separate reconciliation;
   - `head_is_ancestor_of_main == true` only to show the committed head is already reachable from the audited canonical `HEAD`;
   - `head_is_ancestor_of_main == false` to show that committed history is not reachable from canonical `HEAD` and therefore must not be discarded without reconciliation;
   - `locked`, `prunable`, `detached`, `exists`, and `status_sample` as additional evidence, never as deletion authority.

6. If cleanup or integration is later requested, first build an explicit per-worktree decision ledger: preserve, reconcile, integrated/superseded, or removal candidate. Independently verify the exact target immediately before any state-changing command. The audit itself authorizes no mutation.

## Preserve the exact process

The executable keeps the original hardware project schema and classification algorithm:

- parse `git worktree list --porcelain` records;
- inspect each registered path with `git status --porcelain=v1` and `git rev-parse HEAD`;
- compare each worktree HEAD to the canonical audited HEAD using `git merge-base --is-ancestor`;
- retain at most the first 20 status rows as `status_sample` while keeping the complete dirty-row count;
- summarize `registered`, `existing`, `clean`, `dirty`, `merged_or_ancestor`, and `not_ancestor`;
- fail when a registered worktree is missing or unreadable;
- write stable, sorted, indented JSON with a trailing newline.

Read [original-worktree-process.md](references/original-worktree-process.md) when exact provenance, field semantics, or the takeover decision boundary matters. The original source snapshot is preserved byte-for-byte in [worktree-audit_worktrees.original.py](references/worktree-audit_worktrees.original.py).

## Safety and interpretation rules

- Keep the repository and every worktree read-only. The only normal write is the requested audit JSON.
- Never run `git worktree remove`, `git worktree prune`, `git clean`, `git reset`, branch deletion, checkout, merge, cherry-pick, or filesystem deletion merely because of this audit.
- Never equate clean with merged, prunable with disposable, missing with safe to forget, or ancestor status with working-tree content preservation.
- Preserve dirty and non-ancestor worktrees until their committed and uncommitted changes are independently reconciled.
- Keep unrelated-project worktrees separate; registration in one repository does not authorize inspection or mutation of another project.
- Report the audit revision. Ancestor results are relative to the captured `main_head` and can become stale after canonical HEAD advances.
- Treat the output as topology evidence, not product qualification, release approval, deployment authority, or permission for physical/fabrication actions.

## Validate the packaged skill

Run the deterministic temporary-repository self-test after changing the script:

```powershell
python -B <skill-dir>\scripts\selftest_audit_worktrees.py
```

Then run the skill-package validator:

```powershell
python <skill-creator-dir>\scripts\quick_validate.py <skill-dir>
```

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
