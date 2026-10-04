<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf endpoints` — Manage Hugging Face Inference Endpoints.

- `hf endpoints catalog deploy --repo TEXT` — Deploy an Inference Endpoint from the Model Catalog. `[--name TEXT --accelerator TEXT --namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf endpoints catalog list` — List available Catalog models. `[--format [auto|human|agent|json|quiet]]`
- `hf endpoints delete NAME` — Delete an Inference Endpoint permanently. `[--namespace TEXT --yes --format [auto|human|agent|json|quiet]]`
- `hf endpoints deploy NAME --repo TEXT --framework TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --region TEXT --vendor TEXT` — Deploy an Inference Endpoint from a Hub repository. `[--namespace TEXT --task TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric [pendingRequests|hardwareUsage] --scaling-threshold FLOAT --revision TEXT --custom-image TEXT --health-route TEXT --port INTEGER --container-command TEXT --container-args TEXT --env TEXT --env-file TEXT --secrets TEXT --secrets-file TEXT --type [public|protected|authenticated|private] --format [auto|human|agent|json|quiet]]`
- `hf endpoints describe NAME` — Get information about an existing endpoint. `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf endpoints list` — Lists all Inference Endpoints for the given namespace. `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf endpoints pause NAME` — Pause an Inference Endpoint. `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf endpoints resume NAME` — Resume an Inference Endpoint. `[--namespace TEXT --fail-if-already-running --format [auto|human|agent|json|quiet]]`
- `hf endpoints scale-to-zero NAME` — Scale an Inference Endpoint to zero. `[--namespace TEXT --format [auto|human|agent|json|quiet]]`
- `hf endpoints update NAME` — Update an existing endpoint. `[--namespace TEXT --repo TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --framework TEXT --revision TEXT --task TEXT --container-command TEXT --container-args TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric [pendingRequests|hardwareUsage] --scaling-threshold FLOAT --format [auto|human|agent|json|quiet]]`
