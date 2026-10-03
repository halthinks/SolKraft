# Connect your hosted SolKraft library to an agent

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

## ChatGPT custom app: check compatibility first

ChatGPT account/workspace eligibility and menus can change. Follow the [current OpenAI instructions](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt). At a high level: enable developer mode with the necessary permission, open Settings → Apps → Create, name the app, provide the HTTPS MCP address, choose compatible authentication, scan tools, create the app, and select it in a new chat.

**This release does not supply OAuth.** It protects MCP with an operator bearer key. If your custom-app form cannot send that key in an Authorization header, direct connection is blocked. Do not select unauthenticated access or disable server protection to bypass this. Use the direct Codex connection above or copy a skill manually. An advanced operator may configure a trusted OAuth gateway, but that gateway is a separate deployment and is not supplied or verified by SolKraft.

With compatible authentication, Scan Tools should discover `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, and `get_selection_graph`. Create the app and select/mention it when asking for retrieval. Workspace publishing requires the appropriate administrator permissions. Follow-up messages needing new retrieval may need the app selected again. Connecting does not silently change every existing chat.

## Common problems

| What you see | What to check |
|---|---|
| 401 / Unauthorized | The app must send the exact Render key as `Authorization: Bearer <key>`. |
| Timeout | Open `/healthz` and inspect Render logs. Free services can sleep and wake slowly. |
| URL saved but no tools | Restart the host and check its MCP status; saved configuration is not a tool-call test. |
| OAuth sign-in fails | SolKraft does not implement OAuth. Choose a compatible client or a separately configured gateway. |
| Tools work but no skill is used | Ask the host to retrieve and apply relevant methods; tools supply capability, not guaranteed model behavior. |

The API explorer's Connect button tests REST catalog access. It does not connect ChatGPT or Codex for you.
