<!-- solkraft-doc-sync: contract-aware-v1 | semantic-exact-match | 2026-10 -->

# Connect an agent

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The current acceptance gate requires **473,000 production-router calls across all 32 slices**: 173,000 single-skill cases, 100,000 clarified compound requests, 100,000 unchanged original compound diagnostics, and 100,000 stability executions.
- Acceptance requires **100% of 111,000 eligible single-skill exact selections and 62,000 hardened policy decisions**, plus **100% holdout, per-skill, compound exact-set, coverage, order, and stability results**, with **zero extra selections and zero unresolved stages** in clarified compound requests. Clarifications preserve every original topic and target; the original corpus remains a separate diagnostic.
- The historical 373,000-call run reached **27.697% compound exact matching** and is rejected as evidence of completion. Current results belong to the source-bound aggregate receipt; the October 10 full local CI passed all 22 steps and all 15 semantic gates across 32/32 receipts. Generated-corpus success does not establish perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Read the root `AGENTS.md` as the host's operating procedure. Use skill search when a procedure would help, route compound or ambiguous requests, retrieve selected entrypoints, then follow their references as needed. Retain established task context across continuations. The service retrieves instructions; the host performs authorized work with its own tools.

## Local MCP

Install SolKraft in a Python environment. Clients supporting MCP stdio can use this conventional server configuration (place it in the client's documented MCP settings file):

```json
{
  "mcpServers": {
    "solkraft": {
      "command": "python",
      "args": ["-m", "solkraft", "mcp"]
    }
  }
}
```

Use the Python executable from the environment where SolKraft is installed. Configuration filenames and field placement vary by client; this is a server definition, not a claim that every client uses the same settings path.

For a hosted instance, use the Streamable HTTP URL `https://YOUR-SERVICE.onrender.com/mcp/` and the `Authorization: Bearer <your-key>` header. The seven read-only tools are `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, `get_selection_graph`, `get_skill_contract`, and `get_contract_index`.

## CLI and API access

Grok CLI or any agent with shell access can call the portable commands directly:

```sh
python -m solkraft search "repository release gate"
python -m solkraft route "Draft PR" --context-stage repository-release-gate
python -m solkraft get solforge-workflow-software-test
python -m solkraft resource solforge references/native-execution.md
python -m solkraft graph
```

API clients send JSON to `POST /v1/route`, including the bearer header:

```json
{
  "objective": "Inspect the repository, implement the fix, then verify regression behavior",
  "max_skills": 50,
  "skills": [],
  "context": {"domain": "software"}
}
```

Read `selected`, ordered `stages`, `selection_trace`, and `unselected_requested_stages`; fetch the selected skill bodies rather than loading the whole catalog into context. Explicit IDs are supported across the configured catalog. Operator-mounted skill roots join discovery and explicit routing through `SOLKRAFT_SKILL_ROOTS`, using the operating system's path separator.

Connecting a service does not install these behavioral instructions into every existing agent session. The host must load `AGENTS.md` or equivalent instructions. Long-running hosts should retain them and reassess relevant skills as the work changes stage.

For the complete local installed catalog, add `--installed` to the CLI invocation, including MCP stdio arguments `["-m", "solkraft", "mcp", "--installed"]`. This scans the standard Codex, agent, and plugin skill roots while preserving stable bundled workflow IDs.


## ChatGPT web

Follow the [step-by-step remote connection guide](REMOTE_MCP.md) and the website's **Connect your agent** walkthrough. They include a direct bearer-authenticated Codex path and the ChatGPT authentication compatibility check.

The local Codex plugin does not install a remote service into browser ChatGPT. For manual use, inspect and copy a selected skill in the console, then paste it alongside your task. For MCP use, deploy the API and connect its reachable HTTPS `/mcp/` endpoint using a supported custom app. Follow OpenAI’s [current developer-mode documentation](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt) for plan eligibility and workspace controls; these vary by account and change over time.

The API currently accepts operator bearer keys, not OAuth. A remote client must support the required Authorization header, or the operator must supply a trusted gateway with the authentication mechanism that client supports. SolKraft does not ship a ChatGPT OAuth registration or a universally usable hosted endpoint. Do not disable authentication just to make a connector work. GitHub Pages serves the explorer and downloadable plugin; it cannot run Python or host MCP.

## Why use this rather than a prompt library?

A prompt library asks the user to choose and paste instructions. SolKraft adds selective agent retrieval, context-aware routing of compound work, and inspectable relationships. Only the selected bodies enter the conversation. This can reduce unnecessary context, but this release does not establish a numerical token or task-quality improvement.

[skills.sh](https://skills.sh/docs/cli) provides skill discovery and installation. [Superpowers](https://github.com/obra/superpowers) provides an opinionated software development methodology through agent skills and integrations. SolKraft’s focus is a multi-domain catalog with a deterministic router and a callable REST/MCP retrieval layer. They can complement each other; no superiority benchmark is claimed.
