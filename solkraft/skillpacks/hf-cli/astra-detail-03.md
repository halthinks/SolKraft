<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf cache` — Manage local cache directory.

- `hf cache list` — List cached repositories or revisions. `[--cache-dir TEXT --revisions --filter TEXT --sort [accessed|accessed:asc|accessed:desc|modified|modified:asc|modified:desc|name|name:asc|name:desc|size|size:asc|size:desc] --limit INTEGER --show-warnings --format [auto|human|agent|json|quiet]]`
- `hf cache prune` — Remove detached revisions and incomplete downloads from the cache. `[--cache-dir TEXT --yes --dry-run --format [auto|human|agent|json|quiet]]`
- `hf cache rm TARGETS` — Remove cached repositories or revisions. `[--cache-dir TEXT --yes --dry-run --format [auto|human|agent|json|quiet]]`
- `hf cache verify REPO_ID` — Verify checksums for a single repo revision from cache or a local directory. `[--type [model|dataset|space] --revision TEXT --cache-dir TEXT --local-dir TEXT --fail-on-missing-files --fail-on-extra-files --format [auto|human|agent|json|quiet]]`
