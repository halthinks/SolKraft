### `hf repos` — Manage repos on the Hub.

- `hf repos branch create REPO_ID BRANCH` — Create a new branch for a repo on the Hub. `[--revision TEXT --type [model|dataset|space] --exist-ok --format [auto|human|agent|json|quiet]]`
- `hf repos branch delete REPO_ID BRANCH` — Delete a branch from a repo on the Hub. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf repos cp SRC` — Copy files between local paths, repositories, and buckets. `[--format [auto|human|agent|json|quiet]]`
- `hf repos create REPO_ID` — Create a new repo on the Hub. `[--type [model|dataset|space] --sdk TEXT --template TEXT --private --public --protected --exist-ok --resource-group-id TEXT --region [us|eu] --flavor [cpu-basic|cpu-upgrade|zero-a10g|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8] --storage [small|medium|large] --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT --format [auto|human|agent|json|quiet]]`
- `hf repos delete REPO_ID` — Delete a repo from the Hub. This is an irreversible operation. `[--type [model|dataset|space] --missing-ok --yes --format [auto|human|agent|json|quiet]]`
- `hf repos delete-files REPO_ID PATTERNS` — Delete files from a repo on the Hub. `[--type [model|dataset|space] --revision TEXT --commit-message TEXT --commit-description TEXT --create-pr --format [auto|human|agent|json|quiet]]`
- `hf repos duplicate FROM_ID` — Duplicate a repo on the Hub (model, dataset, or Space). `[--type [model|dataset|space] --private --public --protected --exist-ok --flavor [cpu-basic|cpu-upgrade|zero-a10g|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8] --storage [small|medium|large] --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT --format [auto|human|agent|json|quiet]]`
- `hf repos list` — List all repos (models, datasets, spaces, buckets) with storage info. `[--namespace TEXT --type [model|dataset|space|bucket] --search TEXT --limit INTEGER --explore --format [auto|human|agent|json|quiet]]`
- `hf repos move FROM_ID TO_ID` — Move a repository from a namespace to another namespace. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf repos settings REPO_ID` — Update the settings of a repository. `[--gated [auto|manual|false] --private --public --protected --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf repos tag create REPO_ID TAG` — Create a tag for a repo. `[--message TEXT --revision TEXT --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf repos tag delete REPO_ID TAG` — Delete a tag for a repo. `[--yes --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf repos tag list REPO_ID` — List tags for a repo. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
