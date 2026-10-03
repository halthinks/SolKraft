### `hf auth` — Manage authentication (login, logout, etc.).

- `hf auth list` — List all stored access tokens. `[--format [auto|human|agent|json|quiet]]`
- `hf auth login` — Login from your browser, or using a token from huggingface.co/settings/tokens. `[--add-to-git-credential --force --format [auto|human|agent|json|quiet]]`
- `hf auth logout` — Logout from a specific token. `[--token-name TEXT --format [auto|human|agent|json|quiet]]`
- `hf auth switch` — Switch between access tokens. `[--token-name TEXT --add-to-git-credential --format [auto|human|agent|json|quiet]]`
- `hf auth token` — Print the current access token to stdout. `[--format [auto|human|agent|json|quiet]]`
- `hf auth whoami` — Find out which huggingface.co account you are logged in as. `[--format [auto|human|agent|json|quiet]]`
