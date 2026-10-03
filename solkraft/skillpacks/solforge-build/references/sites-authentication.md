# Sites Source Authentication

When `.openai/hosting.json` exists or a Git remote resolves to `git.chatgpt-team.site`, never run a plain `git push`, `git fetch`, `git ls-remote`, or another authenticated remote command.

1. Read `project_id` from `.openai/hosting.json`.
2. Immediately before the first authenticated command, call `sites.create_source_repository_write_credential` for that project and refresh it when absent or expired.
3. Verify the returned remote URL and branch. Use the token only as a per-command HTTP `Authorization: Bearer` header.
4. Set `GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=Never`, and an empty `GIT_ASKPASS` for every Git subprocess.
5. Never request or accept a Windows, GitHub, OpenAI, or personal password for a Sites remote. Never persist or display the token.
6. Verify the push using the same still-valid credential or the branch-head SHA recorded by Sites.
