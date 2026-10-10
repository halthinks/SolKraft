<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Install SolKraft in Codex

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The full local semantic run completed **373,000 routing calls across all 32 slices** and passed its configured gates. Single-skill decisions: **99.961%**; compound target coverage: **100%**; ordering: **99.655%**; stability: **100%**.
- Exact compound skill sets: **27.697%**, with **233,968 extra selections** and **60,000/100,000 requests without unresolved stages**. Coverage is not precision; passing this generated corpus does not prove perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

<!-- END SOLKRAFT CURRENT SYSTEM -->


The repository ships a native Codex plugin, a repository marketplace, and a downloadable ZIP. The plugin combines a compact integration skill with seven read-only MCP tools. The Python runtime contains the 173 bundled skills and the SolForge router. It runs locally; no hosted account or model API key is required for the service itself.

## Install the included private plugin

SolKraft ships its own plugin in this repository. Install it directly from GitHub; it is not listed in the public plugin directory. It runs on your computer. You do not need Render, a hosted API, or a SolKraft API key. You still need your usual Codex access.

You need Python 3.11 or newer, Git, and Codex with plugin support. Open PowerShell on Windows or your terminal on Linux. Run `codex plugin --help` and check that it lists `add` and `marketplace`. If they are missing, update Codex or use the manual MCP setup in CLIENTS.md.


Use Python 3.11 or newer and Git in the environment from which you launch Codex:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft --sparse .agents/plugins --sparse plugins/solkraft
codex plugin add solkraft@solkraft
```

Codex calls a plugin source a “marketplace.” Here that means this GitHub repository, not a shop or a purchase. The first Codex command registers the source; the second installs its plugin.

The sparse flags download the marketplace and plugin folders without checking out the full skill source tree. This avoids unnecessarily large marketplace caches and deep Windows path failures.

Start Codex from the same terminal, then open a new chat. Check the installed plugin in the client's plugin list. The package is not currently published on PyPI; `pip install solkraft` is not the documented installation route.

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

`tests/test_plugin.py` starts the configured stdio subprocess outside the source directory, initializes a real MCP session, lists all seven tools, searches, routes a repository release gate, retrieves skill/resource data, reads the catalog graph, and verifies the contract metadata/index tools. Run it with the Python runtime installed. Marketplace installation is separately checked with the Codex CLI in an isolated `CODEX_HOME`; neither check proves every host/model will choose the plugin naturally on every task.
