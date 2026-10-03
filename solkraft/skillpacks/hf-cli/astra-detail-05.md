### `hf datasets` — Interact with datasets on the Hub.

- `hf datasets card DATASET_ID` — Get the dataset card (README) for a dataset on the Hub. `[--metadata --text --format [auto|human|agent|json|quiet]]`
- `hf datasets info DATASET_ID` — Get info about a dataset on the Hub. `[--revision TEXT --expand TEXT --format [auto|human|agent|json|quiet]]`
- `hf datasets leaderboard DATASET_ID` — List model scores from a dataset leaderboard. This command helps find the best models for a task or compare models by benchmark scores. Use 'hf datasets ls --filter benchmark:official' to list available leaderboards. `[--limit INTEGER --format [auto|human|agent|json|quiet]]`
- `hf datasets list` — List datasets on the Hub, or files in a dataset repo. `[--search TEXT --author TEXT --filter TEXT --sort [created_at|downloads|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format [auto|human|agent|json|quiet]]`
- `hf datasets parquet DATASET_ID` — List parquet file URLs available for a dataset. `[--subset TEXT --split TEXT --format [auto|human|agent|json|quiet]]`
- `hf datasets sql SQL` — Execute a raw SQL query with DuckDB against dataset parquet URLs. `[--format [auto|human|agent|json|quiet]]`
