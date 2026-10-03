---
name: hf-cli
description: Manage Hugging Face Hub resources with the hf CLI, including authentication, repositories, models, datasets, Spaces, jobs, and cache.
---

Install: `curl -LsSf https://hf.co/cli/install.sh | bash -s`.

The Hugging Face Hub CLI tool `hf` is available. IMPORTANT: The `hf` command replaces the deprecated `huggingface-cli` command.

Use `hf --help` to view available functions. Note that auth commands are now all under `hf auth` e.g. `hf auth whoami`.

Generated with `huggingface_hub v1.27.0`. Run `hf skills add --force` to regenerate.

## Commands

- `hf cp SRC` — Copy files between local paths, repositories, and buckets. `[--format [auto|human|agent|json|quiet]]`
- `hf download REPO_ID` — Download files from the Hub. `[--type [model|dataset|space] --revision TEXT --include TEXT --exclude TEXT --cache-dir TEXT --local-dir TEXT --force-download --dry-run --max-workers INTEGER --format [auto|human|agent|json|quiet]]`
- `hf env` — Print information about the environment. `[--format [auto|human|agent|json|quiet]]`
- `hf sync` — Sync files between local directory and a bucket. `[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose --format [auto|human|agent|json|quiet]]`
- `hf update` — Update the `hf` CLI to the latest version. `[--format [auto|human|agent|json|quiet]]`
- `hf upload REPO_ID` — Upload a file or a folder to the Hub. Recommended for single-commit uploads. `[--type [model|dataset|space] --revision TEXT --private --include TEXT --exclude TEXT --delete TEXT --commit-message TEXT --commit-description TEXT --create-pr --every FLOAT --format [auto|human|agent|json|quiet]]`
- `hf upload-large-folder REPO_ID LOCAL_PATH` — [Deprecated] Upload a large folder to the Hub. Use `hf upload` instead. `[--type [model|dataset|space] --revision TEXT --private --include TEXT --exclude TEXT --num-workers INTEGER --no-report --no-bars --format [auto|human|agent|json|quiet]]`
- `hf version` — Print information about the hf version. `[--format [auto|human|agent|json|quiet]]`

### `hf auth` — Manage authentication (login, logout, etc.).

Read [`hf auth` — Manage authentication (login, logout, etc.).](astra-detail-01.md) when using `hf auth`. Paths in that reference remain relative to this skill directory.


### `hf buckets` — Commands to interact with buckets.

Read [`hf buckets` — Commands to interact with buckets.](astra-detail-02.md) when using `hf buckets`. Paths in that reference remain relative to this skill directory.


### `hf cache` — Manage local cache directory.

Read [`hf cache` — Manage local cache directory.](astra-detail-03.md) when using `hf cache`. Paths in that reference remain relative to this skill directory.


### `hf collections` — Interact with collections on the Hub.

Read [`hf collections` — Interact with collections on the Hub.](astra-detail-04.md) when using `hf collections`. Paths in that reference remain relative to this skill directory.


### `hf datasets` — Interact with datasets on the Hub.

Read [`hf datasets` — Interact with datasets on the Hub.](astra-detail-05.md) when using `hf datasets`. Paths in that reference remain relative to this skill directory.


### `hf discussions` — Manage discussions and pull requests on the Hub.

Read [`hf discussions` — Manage discussions and pull requests on the Hub.](astra-detail-06.md) when using `hf discussions`. Paths in that reference remain relative to this skill directory.


### `hf endpoints` — Manage Hugging Face Inference Endpoints.

Read [`hf endpoints` — Manage Hugging Face Inference Endpoints.](astra-detail-07.md) when using `hf endpoints`. Paths in that reference remain relative to this skill directory.


### `hf extensions` — Manage hf CLI extensions.

Read [`hf extensions` — Manage hf CLI extensions.](astra-detail-08.md) when using `hf extensions`. Paths in that reference remain relative to this skill directory.


### `hf jobs` — Run and manage Jobs on the Hub.

Read [`hf jobs` — Run and manage Jobs on the Hub.](astra-detail-09.md) when using `hf jobs`. Paths in that reference remain relative to this skill directory.


### `hf models` — Interact with models on the Hub.

Read [`hf models` — Interact with models on the Hub.](astra-detail-10.md) when using `hf models`. Paths in that reference remain relative to this skill directory.


### `hf papers` — Interact with papers on the Hub.

Read [`hf papers` — Interact with papers on the Hub.](astra-detail-11.md) when using `hf papers`. Paths in that reference remain relative to this skill directory.


### `hf repos` — Manage repos on the Hub.

Read [`hf repos` — Manage repos on the Hub.](astra-detail-12.md) when using `hf repos`. Paths in that reference remain relative to this skill directory.


### `hf sandbox` — Run and manage sandboxes on Hugging Face Jobs.

Read [`hf sandbox` — Run and manage sandboxes on Hugging Face Jobs.](astra-detail-13.md) when using `hf sandbox`. Paths in that reference remain relative to this skill directory.


### `hf skills` — Manage skills for AI assistants.

Read [`hf skills` — Manage skills for AI assistants.](astra-detail-14.md) when using `hf skills`. Paths in that reference remain relative to this skill directory.


### `hf spaces` — Interact with spaces on the Hub.

Read [`hf spaces` — Interact with spaces on the Hub.](astra-detail-15.md) when using `hf spaces`. Paths in that reference remain relative to this skill directory.


### `hf webhooks` — Manage webhooks on the Hub.

Read [`hf webhooks` — Manage webhooks on the Hub.](astra-detail-16.md) when using `hf webhooks`. Paths in that reference remain relative to this skill directory.


## Common options

- `--format` — Output format: `--format json` (or `--json`) or `--format table` (default).
- `-q / --quiet` — Quiet output (one ID per line).
- `--revision` — Git revision id which can be a branch name, a tag, or a commit hash.
- `--token` — Use a User Access Token. Prefer setting `HF_TOKEN` env var instead of passing `--token`.
- `--type` — The type of repository (model, dataset, or space).

## Mounting repos as local filesystems

Read [Mounting repos as local filesystems](astra-detail-17.md) when mounting Hub resources as local filesystems. Paths in that reference remain relative to this skill directory.


## Tips

- Use `hf <command> --help` for full options, descriptions, usage, and real-world examples
- Authenticate with `HF_TOKEN` env var (recommended) or with `--token`
- Update the CLI with `hf update` (uses the correct command for the detected install method)
