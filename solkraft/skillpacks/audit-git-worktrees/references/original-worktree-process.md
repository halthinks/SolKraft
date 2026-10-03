# Original hardware project worktree-audit process

## Provenance

- Canonical repository: `C:\hardware project Platform`
- Takeover commit: `8c0a48711cb229942fd5cf8aa5889c87f09ea348`
- Original source path: `research/2026-08-24-post-grok-full-diff-audit/audit_worktrees.py`
- Original source SHA-256: `22c001a120e0ff2218e771e7b029dcb0918c4675f3a6ae2c88fc65c2697b3b23`
- Original evidence path: `research/2026-08-24-post-grok-full-diff-audit/worktree-audit.json`

The original audit observed 67 registered and existing worktrees: 40 clean, 27 dirty, 5 whose committed HEAD was an ancestor of the then-canonical HEAD, and 62 whose committed HEAD was not. Those counts are historical evidence bound to the captured `main_head`; never use them as current topology without rerunning the audit.

## Exact field semantics

- `main_head`: canonical `HEAD` captured before per-worktree ancestry checks.
- `path`: registered worktree path from `git worktree list --porcelain`.
- `exists`: whether that path was a directory at audit time.
- `head`: live `git rev-parse HEAD`, falling back to the registered porcelain `HEAD` when unreadable.
- `branch`: porcelain branch ref when present.
- `detached`: whether the porcelain record contains `detached`.
- `locked`: porcelain lock value when present.
- `prunable`: porcelain prune value when present.
- `status_rows`: complete count of `git status --porcelain=v1` rows, or null when unreadable.
- `status_sample`: first 20 porcelain status rows only.
- `head_is_ancestor_of_main`: result of `git merge-base --is-ancestor <worktree-head> <main_head>`.
- `failures`: `unreadable:<path>` for missing/unreadable registered worktrees.

## Original decision boundary

The audit separated inventory from disposition. It did not remove the remaining non-ancestor Grok worktrees because they could contain unmerged engineering data. Only separately classified mailbox-era worktrees were removed after their relevant diffs were independently judged integrated, superseded, or already ancestral. Dirty and non-ancestor worktrees were preserved for later reconciliation.

The original takeover also distinguished:

- committed work accepted for continued verification from broad product qualification;
- historical host-path evidence from current runtime authority;
- host-local agent orchestration from repository product dependencies;
- an isolated prototype from a production cutover.

The worktree audit itself grants no authority to remove worktrees or branches, rewrite evidence, merge code, release software, deploy, fabricate, flash, purchase, or perform physical/lab actions.
