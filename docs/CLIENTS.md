<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Connect an agent

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Contract-aware routing uses semantic capability identity plus machine-readable `contract.yaml` metadata for typed inputs/outputs, namespaced effects, capability/resource requirements, declarative verification, provenance, trust, and exact digests.
- Public REST, MCP, and CLI routing default to **hardened** policy. Opaque or otherwise inadmissible capabilities fail closed; the Python library stays compatibility-oriented unless stricter policy is requested.
- SolKraft is advisory and non-executing. Runtime authority remains with the host and `execution_authorized` remains `false`.
- The compact `ContractIndex` supplies routing/API/MCP/docs metadata without loading every full `SKILL.md` body into the hot path.
- Read-only MCP tools: `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, `get_selection_graph`, `get_skill_contract`, and `get_contract_index`.
- Reusable CI and pre-PR contribution validation share contract/schema, routing, packaging, installed-MCP, index/hardening, and evidence gates.
- Latest local acceptance: **100,000 / 100,000** unique 250-word requests passed with **100 ask families per skill**, **100% eligible target recall**, **100% hardened blocking**, and **100% consequential-boundary correctness**; no explicit skill IDs were injected.
- The public Validation display is a clearly labeled **recorded reenactment**, not live browser CI.

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

For a hosted instance, use the Streamable HTTP URL `https://YOUR-SERVICE.onrender.com/mcp/` and the `Authorization: Bearer <your-key>` header. The five tools are `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, and `get_selection_graph`.

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
