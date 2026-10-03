### `hf buckets` — Commands to interact with buckets.

- `hf buckets cp SRC` — Copy files between local paths, repositories, and buckets. `[--format [auto|human|agent|json|quiet]]`
- `hf buckets create BUCKET_ID` — Create a new bucket. `[--private --region [us|eu] --exist-ok --format [auto|human|agent|json|quiet]]`
- `hf buckets delete BUCKET_ID` — Delete a bucket. `[--yes --missing-ok --format [auto|human|agent|json|quiet]]`
- `hf buckets info BUCKET_ID` — Get info about a bucket. `[--format [auto|human|agent|json|quiet]]`
- `hf buckets list` — List buckets or files in a bucket. `[--human-readable --tree --recursive --search TEXT --format [auto|human|agent|json|quiet]]`
- `hf buckets move FROM_ID TO_ID` — Move (rename) a bucket to a new name or namespace. `[--format [auto|human|agent|json|quiet]]`
- `hf buckets remove ARGUMENT` — Remove files from a bucket. `[--recursive --yes --dry-run --include TEXT --exclude TEXT --format [auto|human|agent|json|quiet]]`
- `hf buckets sync` — Sync files between local directory and a bucket. `[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose --format [auto|human|agent|json|quiet]]`
