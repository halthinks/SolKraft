# SolKraft plugin

Install Python 3.11+ and the runtime first:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft --sparse .agents/plugins --sparse plugins/solkraft
codex plugin add solkraft@solkraft
```

Launch Codex with `solkraft` on PATH and start a new session. This package contains a supported Codex manifest, a local stdio MCP connection, and a compact integration skill. The separately installed Python runtime contains the catalog and router. The plugin does not require a hosted API, user account, or service key. Your agent's existing model and tooling costs still apply.

Ask normally, for example: “Investigate this bug, implement the fix, and verify the release build.” The integration skill helps the host search or route, retrieve useful methods, apply them through its own tools, and verify its work. SolKraft tools are read-only; they never run your repository themselves.

Full setup, verification, and troubleshooting: https://github.com/halthinks/SolKraft/blob/main/docs/PLUGIN.md
