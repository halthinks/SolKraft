---
name: solforge-sign-and-prove
description: Create and verify artifact checksums, SBOMs, provenance, and authorized signing evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Sign And Prove

Create and verify artifact checksums, SBOMs, provenance, and authorized signing evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Bind provenance to the exact built artifact and source revision. Verify available hashes, signatures, certificate identity, and verification commands. Use signing credentials only when authorized and available; report unsigned artifacts plainly. A successful signature proves identity and integrity, not functional correctness.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
