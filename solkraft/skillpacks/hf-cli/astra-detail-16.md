<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf webhooks` — Manage webhooks on the Hub.

- `hf webhooks create --watch TEXT` — Create a new webhook. `[--url TEXT --job-id TEXT --domain [repo|discussions] --secret TEXT --format [auto|human|agent|json|quiet]]`
- `hf webhooks delete WEBHOOK_ID` — Delete a webhook permanently. `[--yes --format [auto|human|agent|json|quiet]]`
- `hf webhooks disable WEBHOOK_ID` — Disable an active webhook. `[--format [auto|human|agent|json|quiet]]`
- `hf webhooks enable WEBHOOK_ID` — Enable a disabled webhook. `[--format [auto|human|agent|json|quiet]]`
- `hf webhooks info WEBHOOK_ID` — Show full details for a single webhook. `[--format [auto|human|agent|json|quiet]]`
- `hf webhooks list` — List all webhooks for the current user. `[--format [auto|human|agent|json|quiet]]`
- `hf webhooks update WEBHOOK_ID` — Update an existing webhook. Only provided options are changed. `[--url TEXT --watch TEXT --domain [repo|discussions] --secret TEXT --format [auto|human|agent|json|quiet]]`
