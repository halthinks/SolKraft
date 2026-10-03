# Choose a connection

The [interactive walkthrough](https://halthinks.github.io/SolKraft/#setup-lab) has selectable Render, API/MCP, and local plugin paths, platform-specific commands, animated request cards, and copy controls. Its animation illustrates setup; only the console's Connect button sends a real authenticated request.

| Your goal | Use | Why |
| --- | --- | --- |
| Browse or manually give an agent a procedure | Static explorer | No installation, server, or key needed |
| Have local Codex retrieve procedures naturally | Python runtime + Codex plugin | Local stdio MCP, without a hosted service |
| Build an app, script, or custom integration | REST API | Ordinary HTTP requests and JSON responses |
| Let a remote compatible agent retrieve skills | Hosted MCP | Standard tool discovery and calls over HTTPS |

## Render walkthrough

1. Open [Deploy Blueprint](https://render.com/deploy?repo=https://github.com/halthinks/SolKraft). Connect the repository as required by your Render account. The committed `render.yaml` defines the Python web service, Free plan, build `pip install .`, startup `python -m solkraft api`, and `/healthz` check.
2. Generate an operator key with `python -c "import secrets; print(secrets.token_urlsafe(32))"`. Enter it in Render as `SOLKRAFT_API_KEY`, which the Blueprint intentionally does not supply. Do not commit or publish it. `SOLKRAFT_CORS_ORIGINS=https://halthinks.github.io` permits this explorer; use comma-separated exact origins for other consoles.
3. Deploy. Render supplies `PORT`; the CLI binds to `0.0.0.0` on that port. Inspect logs for installation/startup errors. Open `https://YOUR-SERVICE.onrender.com/healthz` and expect `{"status":"ok","service":"solkraft"}`. This endpoint is public and does not prove protected requests succeed.
4. In the explorer, enter the base service URL, then the key in the Bearer key field and click Connect. The protected catalog must load before the UI reports success. Use Compose a route to send your objective. Keys remain in tab memory; they are not saved in local storage or placed in URLs.
5. For a compatible remote MCP client, configure `https://YOUR-SERVICE.onrender.com/mcp/` and its `Authorization: Bearer YOUR_KEY` header. See [CLIENTS.md](CLIENTS.md) for client and ChatGPT authentication limits.

Render's [Blueprint documentation](https://render.com/docs/infrastructure-as-code) explains account setup. [Free web services](https://render.com/docs/free) sleep after 15 minutes without inbound traffic and have cold starts and resource limits. The UI allows time for waking; this is not an uptime guarantee. A local plugin does not need Render.

## What the API does

An application programming interface is a contract between software. This REST API accepts HTTP and returns JSON. Protected endpoints require the operator's bearer key. Browser access also requires an allowed CORS origin.

| Endpoint | Result |
| --- | --- |
| `GET /healthz` | Public liveness response |
| `GET /v1/skills?q=...&limit=20&offset=0` | Search/list metadata, counts, pagination |
| `GET /v1/skills/{id}` | Selected skill instructions |
| `GET /v1/skills/{id}/resources/{path}` | Selected supporting resource |
| `POST /v1/route` | Advisory ordered skills, reasons, unresolved work |
| `GET /v1/graph` | Catalog and workflow relationships |
| `POST /v1/refresh` | Rebuild the in-memory catalog index |

The refresh operation updates server indexing; it does not modify skill files. A route never runs code or grants authority. The website's platform selector generates REST examples for Bash and PowerShell. For complete request fields see [CLIENTS.md](CLIENTS.md).

## What MCP does

[Model Context Protocol](https://modelcontextprotocol.io/docs/learn/architecture) standardizes how agent clients communicate with servers. A client initializes the connection, discovers tool names and input schemas, and sends tool calls. SolKraft supports local **stdio** (the client launches `solkraft mcp`) and remote **Streamable HTTP** (`/mcp/`).

| Tool | Exact purpose |
| --- | --- |
| `search_skills` | Find compact metadata for relevant procedures |
| `route_request` | Compose advisory stages from objective/context |
| `get_skill` | Retrieve the chosen entrypoint text |
| `get_skill_resource` | Retrieve a supporting file when needed |
| `get_selection_graph` | Inspect available nodes and relationships |

The MCP server has no repository editor, shell executor, deployment tool, or LLM inside it. The host agent reads returned procedures and uses its own tools to perform authorized work. MCP supplies communication, not automatic adoption or proof of task completion. SolKraft currently supports bearer keys, not OAuth. ChatGPT custom apps depend on account policy and compatible authentication; the Codex plugin cannot be installed directly into browser ChatGPT.

## What the plugin does

The plugin registers the MCP launch command and a concise integration skill that tells Codex when retrieval helps. The separately installed Python package provides the service, catalog, and router. See [PLUGIN.md](PLUGIN.md) for installation. Start a new session with the runtime on PATH, then ask for outcomes normally. Selection is guided rather than guaranteed; old sessions do not retroactively gain the tools.

## Windows, WSL, and Omarchy

SolKraft is a portable Python service and static web console. It does not require separate native GUI builds. Install the same package into the OS environment where the client runs. A Windows Python environment and a WSL Linux environment are separate; installing in one does not install in the other.

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
```

Linux, WSL, and Omarchy (Python 3.11+ and Git required):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
```

Use the environment's absolute Python path in a manual MCP configuration when the host does not inherit its PATH. On distributions packaging Python separately, install the distribution's venv support if creation fails. Omarchy uses the Linux package path; a dedicated native binary is not required. Portability is a design property, not evidence of execution on every distribution: consult [VALIDATION.md](../VALIDATION.md) for actual tested environments.

## Build and verify locally

From a repository checkout with Python 3.11+, Node.js, and Git:

```bash
python -m pip install -e ".[dev]"
python -m scripts.local_ci
```

The gate runs Python/router tests, syntax and setup behavior checks, generates the console and plugin ZIP, builds a wheel, installs it in a temporary environment, verifies the installed catalog outside the checkout, and calls the ZIP plugin's five tools over real MCP. It stops on a failed step and records `build/local-ci.json`; the built wheel is in `dist/`. Temporary environments reuse existing dependencies, so this is not a clean dependency-resolution or offline-install test.

Automatic GitHub build/test runs are disabled; the verification workflow remains manually available. Pages only uploads already generated static files. Run the gate and review generated changes before pushing. A passing Windows run does not establish WSL/Omarchy qualification; run the same gate in those environments when release support requires it.
