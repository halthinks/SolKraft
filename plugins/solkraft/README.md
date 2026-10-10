<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolKraft plugin

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The full local semantic run completed **373,000 routing calls across all 32 slices** and passed its configured gates. Single-skill decisions: **99.961%**; compound target coverage: **100%**; ordering: **99.655%**; stability: **100%**.
- Exact compound skill sets: **27.697%**, with **233,968 extra selections** and **60,000/100,000 requests without unresolved stages**. Coverage is not precision; passing this generated corpus does not prove perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](https://github.com/halthinks/SolKraft/blob/main/docs/SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Install Python 3.11+ and the runtime first:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft --sparse .agents/plugins --sparse plugins/solkraft
codex plugin add solkraft@solkraft
```

Launch Codex with `solkraft` on PATH and start a new session. This package contains a supported Codex manifest, a local stdio MCP connection, and a compact integration skill. The separately installed Python runtime contains the catalog and router. The plugin does not require a hosted API, user account, or service key. Your agent's existing model and tooling costs still apply.

Ask normally, for example: “Investigate this bug, implement the fix, and verify the release build.” The integration skill helps the host search or route, retrieve useful methods, apply them through its own tools, and verify its work. SolKraft tools are read-only; they never run your repository themselves.

Full setup, verification, and troubleshooting: https://github.com/halthinks/SolKraft/blob/main/docs/PLUGIN.md
