<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

### `hf discussions` — Manage discussions and pull requests on the Hub.

- `hf discussions close REPO_ID NUM` — Close a discussion or pull request. `[--comment TEXT --yes --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions comment REPO_ID NUM` — Comment on a discussion or pull request. `[--body TEXT --body-file PATH --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions create REPO_ID --title TEXT` — Create a new discussion or pull request on a repo. `[--body TEXT --body-file PATH --pull-request --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions diff REPO_ID NUM` — Show the diff of a pull request. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions edit REPO_ID NUM COMMENT_ID` — Edit an existing comment on a discussion or pull request. `[--body TEXT --body-file PATH --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions info REPO_ID NUM` — Get info about a discussion or pull request. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions list REPO_ID` — List discussions and pull requests on a repo. `[--status [open|closed|merged|draft|all] --kind [all|discussion|pull_request] --author TEXT --limit INTEGER --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions merge REPO_ID NUM` — Merge a pull request. `[--comment TEXT --yes --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions rename REPO_ID NUM NEW_TITLE` — Rename a discussion or pull request. `[--type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
- `hf discussions reopen REPO_ID NUM` — Reopen a closed discussion or pull request. `[--comment TEXT --yes --type [model|dataset|space] --format [auto|human|agent|json|quiet]]`
