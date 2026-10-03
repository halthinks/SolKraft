# Connect an agent

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
