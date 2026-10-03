---
name: solforge-release-matrix
description: Reconcile platform artifacts, signing, provenance, update support, and release-readiness evidence.
---

# SolForge Release Matrix

Reconcile platform artifacts, signing, provenance, update support, and release-readiness evidence.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Build a target-by-target matrix of artifact identity, build result, installation or launch result, compatibility, and unresolved release gates. Keep missing, failed, and passed checks distinct. Promote a target only on evidence for that exact artifact and environment.
