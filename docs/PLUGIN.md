# Install SolKraft in Codex

The repository ships a native Codex plugin, a repository marketplace, and a downloadable ZIP. The plugin combines a compact integration skill with the five read-only MCP tools. The Python runtime contains the 173 bundled skills and the SolForge router. It runs locally; no hosted account or model API key is required for the service itself.

## Install

Use Python 3.11 or newer in the environment from which you launch Codex:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft
codex plugin add solkraft@solkraft
```

Restart the local client or start a new Codex session. Check the installed plugin in the client's plugin list. The package is not currently published on PyPI; `pip install solkraft` is not the documented installation route.

For a checkout, install with `python -m pip install .` and register it using `codex plugin marketplace add .`. The ZIP at [the console download](https://halthinks.github.io/SolKraft/downloads/solkraft-plugin.zip) contains the plugin configuration and integration skill, not Python or its dependencies. Installing the runtime remains required.

This uses OpenAI's [supported compatibility manifest and repository marketplace format](https://developers.openai.com/plugins/build/plugins). It is repository distribution, not a claim of acceptance into OpenAI's public directory. Client versions without `codex plugin` can use the manual MCP setup in [CLIENTS.md](CLIENTS.md).

## What happens when you ask

Try: “Inspect this repository, fix the bug, add a regression test, and verify the release build. Do not deploy.”

1. The host considers the integration skill from its description. It searches for an obvious procedure or calls `route_request` for compound work.
2. The router returns an advisory selection and ordered stages. The host checks the proposed route against the actual task.
3. The host calls `get_skill` for the chosen procedure and `get_skill_resource` for supporting material when needed.
4. The host applies those instructions using its own file, shell, browser, and other tools, preserving repository contracts and user authorization.
5. The host checks the result and reports what the evidence establishes. SolKraft itself only discovers and retrieves methods.

The integration skill recommends capability-preserving execution for substantial work. That procedure preserves inputs, dependencies, authority, and acceptance evidence while the host works. Installing a plugin does not force every model to obey every instruction or update already-running sessions. A fresh session is the supported starting point; useful behavior still depends on the host and model.

## Verify the connection

Ask the new session to list SolKraft tools, search for a software test procedure, route “Draft PR” with context `{"stage":"repository-release-gate"}`, and retrieve `solforge-workflow-software-test`. You should see actual tool calls and returned content, with `execution_authorized: false` in the route. A conversational claim without those calls is not connection evidence.

## Troubleshoot

- **No module named solkraft:** the plugin's `solkraft` executable is missing or resolves to a different environment. Install with that Python, launch Codex from the activated environment, or configure the MCP command to the appropriate SolKraft executable.
- **Plugin missing:** inspect `codex plugin list`, confirm the marketplace is registered, enable the plugin, then start a new session.
- **Tools available but unused:** explicitly request one call to confirm connectivity. The integration skill provides natural-use guidance, but a tool connection alone is not a guaranteed model behavior hook.
- **ChatGPT web:** it cannot launch this local stdio process. Use a supported remote MCP connection or manually copy selected instructions; see [CLIENTS.md](CLIENTS.md).

## Development evidence

`tests/test_plugin.py` starts the configured stdio subprocess outside the source directory, initializes a real MCP session, lists all five tools, searches, routes a repository release gate, retrieves its skill and a reference, and reads the catalog graph. Run it with the Python runtime installed. Marketplace installation is separately checked with the Codex CLI in an isolated `CODEX_HOME`; neither check proves every host/model will choose the plugin naturally on every task.
