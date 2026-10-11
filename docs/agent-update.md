# Update SolKraft for your agent

Canonical guide: https://halthinks.github.io/SolKraft/agent-update.md

Use this guide to update an existing SolKraft installation. Inspect the current installation first and preserve local changes, configuration, credentials, and custom skills. Update only SolKraft. Do not reset a checkout or remove a plugin to force an update.

## Python runtime and bundled skills

Use the same Python environment that launches the SolKraft MCP service. For an installation from GitHub, run:

```sh
python -m pip install --upgrade "git+https://github.com/halthinks/SolKraft.git"
```

This updates the runtime and its bundled skills together. For an editable checkout, inspect `git status` and the remote first, preserve local changes, and update through that checkout's normal Git workflow instead. Do not replace an editable installation with a second package installation.

## Native Codex plugin

Inspect `codex plugin marketplace list` and identify the SolKraft repository source. Refresh that source using its actual configured name:

```sh
codex plugin marketplace upgrade <SolKraft-source-name>
codex plugin add solkraft@solkraft
```

Replace the placeholder with the name reported by the list command. `marketplace` is Codex's command name for the GitHub plugin source. If your client lacks these commands, use its supported plugin update control; do not invent a replacement command. The plugin alone does not install Python or the runtime.

## Restart and verify

Restart the SolKraft MCP process and open a fresh agent session. Verify real tool calls: list the seven SolKraft tools, search for a software test procedure, route a compound request, and retrieve one selected skill. Report the installed package source/revision when available, the returned skill count, and the actual verification results. Selection remains advisory and `execution_authorized` remains `false`.

For a remote MCP service, update its deployed runtime through the service owner's normal deployment process. Updating a local package does not update a remote server. Preserve the endpoint and credentials.

Installation details: https://github.com/halthinks/SolKraft/blob/main/docs/PLUGIN.md
Source: https://github.com/halthinks/SolKraft
