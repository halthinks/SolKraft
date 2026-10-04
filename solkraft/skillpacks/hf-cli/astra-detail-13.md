<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf sandbox` — Run and manage sandboxes on Hugging Face Jobs.

- `hf sandbox cp SRC DST` — Copy a file between the local machine and a sandbox (docker-style). `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox create` — Create a sandbox: a dedicated VM by default, or a cheap shared one with `--pool`. `[--pool TEXT --flavor [cpu-basic|cpu-upgrade|cpu-performance|cpu-xl|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8|h200|h200x2|h200x4|h200x8|rtx-pro-6000|rtx-pro-6000x2|rtx-pro-6000x4|rtx-pro-6000x8] --idle-timeout TEXT --env TEXT --secrets TEXT --env-file TEXT --secrets-file TEXT --volume TEXT --namespace TEXT --forward-hf-token --format [auto|human|agent|json|quiet]]`
- `hf sandbox exec SANDBOX_ID COMMAND` — Run a command in a sandbox, streaming output. Exits with the command's exit code. `[--workdir TEXT --env TEXT --env-file TEXT --timeout FLOAT --namespace TEXT]`
- `hf sandbox kill` — Terminate a sandbox, a whole shared host, or everything (--all). `[--all --yes --namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox pool create` — Warm a pool: boot one host VM now, tagged so it can be found later by its pool id. `[--flavor [cpu-basic|cpu-upgrade|cpu-performance|cpu-xl|t4-small|t4-medium|l4x1|l4x4|l40sx1|l40sx4|l40sx8|a10g-small|a10g-large|a10g-largex2|a10g-largex4|a100-large|a100x4|a100x8|h200|h200x2|h200x4|h200x8|rtx-pro-6000|rtx-pro-6000x2|rtx-pro-6000x4|rtx-pro-6000x8] --per-host INTEGER RANGE --max-hosts INTEGER RANGE --idle-timeout TEXT --namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox pool delete POOL_ID` — Terminate every host VM of a pool (and therefore all its sandboxes). `[--yes --namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox pool ls` — List running sandbox pools (grouped from their host VMs). `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox process kill SANDBOX_ID PID` — Stop a background process running in a sandbox. `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox process ls SANDBOX_ID` — List the background processes running in a sandbox (started with `hf sandbox spawn`). `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf sandbox spawn SANDBOX_ID COMMAND` — Start a long-running command in the background and return its pid (don't wait). `[--workdir TEXT --env TEXT --env-file TEXT --namespace TEXT]`
