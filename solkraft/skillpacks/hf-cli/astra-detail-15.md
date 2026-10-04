<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf spaces` — Interact with spaces on the Hub.

- `hf spaces card SPACE_ID` — Get the Space card (README) for a Space on the Hub. `[--metadata --text --format [auto|human|agent|json|quiet]]`
- `hf spaces dev-mode SPACE_ID` — Enable or disable dev mode on a Space. `[--stop --format [auto|human|agent|json|quiet]]`
- `hf spaces hardware` — List available hardware options for Spaces. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces hot-reload SPACE_ID` — Hot-reload any Python file of a Space without a full rebuild + restart. `[--local-file PATH --skip-checks --skip-summary --format [auto|human|agent|json|quiet]]`
- `hf spaces info SPACE_ID` — Get info about a space on the Hub. `[--revision TEXT --expand TEXT --format [auto|human|agent|json|quiet]]`
- `hf spaces list` — List spaces on the Hub, or files in a space repo. `[--search TEXT --author TEXT --filter TEXT --sort [created_at|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format [auto|human|agent|json|quiet]]`
- `hf spaces logs SPACE_ID` — Fetch the run or build logs of a Space. `[--build --follow --tail INTEGER --format [auto|human|agent|json|quiet]]`
- `hf spaces pause SPACE_ID` — Pause a Space. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces restart SPACE_ID` — Restart a Space. `[--factory-reboot --format [auto|human|agent|json|quiet]]`
- `hf spaces search QUERY` — Search spaces on the Hub using semantic search. `[--filter TEXT --sdk TEXT --include-non-running --description --limit INTEGER --format [auto|human|agent|json|quiet]]`
- `hf spaces secrets add SPACE_ID` — Add or update secrets for a Space. `[--secrets TEXT --secrets-file TEXT --format [auto|human|agent|json|quiet]]`
- `hf spaces secrets delete SPACE_ID KEY` — Remove a secret from a Space. `[--yes --format [auto|human|agent|json|quiet]]`
- `hf spaces secrets list SPACE_ID` — List secrets for a Space. Secret values are write-only and not returned. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces settings SPACE_ID` — Update the settings of a Space. `[--sleep-time INTEGER --hardware [cpu-basic|cpu-upgrade|zero-a10g|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8] --format [auto|human|agent|json|quiet]]`
- `hf spaces ssh SPACE_ID` — SSH into a Space's Dev Mode container. `[--identity-file PATH --dry-run --auto --format [auto|human|agent|json|quiet]]`
- `hf spaces templates` — List the available Space templates. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces variables add SPACE_ID` — Add or update environment variables for a Space. `[--env TEXT --env-file TEXT --format [auto|human|agent|json|quiet]]`
- `hf spaces variables delete SPACE_ID KEY` — Remove an environment variable from a Space. `[--yes --format [auto|human|agent|json|quiet]]`
- `hf spaces variables list SPACE_ID` — List environment variables for a Space. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces volumes delete SPACE_ID` — Remove all volumes from a Space. `[--yes --format [auto|human|agent|json|quiet]]`
- `hf spaces volumes list SPACE_ID` — List volumes mounted in a Space. `[--format [auto|human|agent|json|quiet]]`
- `hf spaces volumes set SPACE_ID` — Set (replace) volumes for a Space. `[--volume TEXT --format [auto|human|agent|json|quiet]]`
- `hf spaces wait SPACE_ID` — Wait for a Space to finish building/starting. `[--timeout TEXT --format [auto|human|agent|json|quiet]]`
