<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Connect your hosted SolKraft library to an agent

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

4. Start a fresh session. In the terminal app use `/mcp` and check that the server offers five tools. `codex mcp list` checks saved configuration; listing and calling tools checks the connection. For the desktop app, the process starting the connection must also have the environment variable; changing a separate terminal does not update an already-running app.
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
