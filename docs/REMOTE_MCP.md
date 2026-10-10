<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Connect your hosted SolKraft library to an agent

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


You are connecting three things: **your service** holds the skills, **MCP** carries tool requests, and **your agent app** reads the instructions and does your work. You do not need to memorize skill names.

First finish the Render steps in the [interactive walkthrough](https://halthinks.github.io/SolKraft/#setup-lab). Keep your service address and private operator key. A healthy service returns `status: ok` at `/healthz`. That checks whether it is running; it does not check the protected MCP tools.

## Direct remote connection with Codex

1. Copy your service's MCP address: `https://YOUR-SERVICE.onrender.com/mcp/`.
2. Open your existing `~/.codex/config.toml`. Here `~` means your home/user folder. Add this table once, replacing the service address:

```toml
[mcp_servers.solkraft_remote]
url = "https://YOUR-SERVICE.onrender.com/mcp/"
bearer_token_env_var = "SOLKRAFT_API_KEY"
startup_timeout_sec = 120
```

3. In the terminal from which you start Codex, set the same private key you put in Render. Do this locally; never put the real key in a repository, screenshot or issue.

Windows PowerShell:

```powershell
$env:SOLKRAFT_API_KEY = "YOUR_KEY"
codex mcp list
codex
```

Linux / WSL / Omarchy:

```sh
export SOLKRAFT_API_KEY="YOUR_KEY"
codex mcp list
codex
```

4. Start a fresh session. In the terminal app use `/mcp` and check that the server offers seven read-only tools: `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, `get_selection_graph`, `get_skill_contract`, and `get_contract_index`. `codex mcp list` checks saved configuration; listing and calling tools checks the connection. For the desktop app, the process starting the connection must also have the environment variable; changing a separate terminal does not update an already-running app.
5. Ask: “Use SolKraft to choose methods for inspecting this codebase, fixing a bug, and testing the release. Retrieve the useful procedures and apply them within my task.” Check that the agent retrieves skills and then uses its own tools. A saved server address alone does not prove that happened.

The local plugin is another option. It starts a local library process and needs no hosted service. Choose one connection for the same library to avoid redundant tools. These remote configuration fields are documented in [Codex MCP setup](https://developers.openai.com/codex/mcp).

## Use a skill in ChatGPT today

**Direct ChatGPT connection has not been tested yet.** SolKraft requires a private API key, and we have not verified a ChatGPT setup that sends it correctly. Do not disable the key requirement to try to connect.

You can use the skill instructions without connecting a server:

1. Open [Explore](https://halthinks.github.io/SolKraft/#explore).
2. Search for the kind of help you need, such as software testing.
3. Open a skill and copy its instructions.
4. Paste the instructions into ChatGPT with your task. Ask it to follow the procedure and explain its results.

This gives ChatGPT a method to follow. It does not let ChatGPT connect to your SolKraft server automatically. You need no Render account or API key for copying instructions. Codex users who want automatic retrieval can follow the connection steps above.

## Common problems

| What you see | What to check |
|---|---|
| 401 / Unauthorized | The app must send the exact Render key as `Authorization: Bearer <key>`. |
| Timeout | Open `/healthz` and inspect Render logs. Free services can sleep and wake slowly. |
| URL saved but no tools | Restart the host and check its MCP status; saved configuration is not a tool-call test. |
| OAuth sign-in fails | SolKraft does not implement OAuth. Use Codex above, or copy a skill into ChatGPT. |
| Tools work but no skill is used | Ask the host to retrieve and apply relevant methods; tools supply capability, not guaranteed model behavior. |

The API explorer's Connect button tests REST catalog access. It does not connect ChatGPT or Codex for you.
