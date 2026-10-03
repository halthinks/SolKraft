---
name: solforge-sign-and-prove
description: Create and verify artifact checksums, SBOMs, provenance, and authorized signing evidence.
---

# SolForge Sign And Prove

Create and verify artifact checksums, SBOMs, provenance, and authorized signing evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Bind provenance to the exact built artifact and source revision. Verify available hashes, signatures, certificate identity, and verification commands. Use signing credentials only when authorized and available; report unsigned artifacts plainly. A successful signature proves identity and integrity, not functional correctness.
