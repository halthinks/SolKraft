---
name: solforge-workflow-launcher-release-readiness
description: Reconcile artifacts, checksums, SBOM, provenance, signing readiness, CI, documentation, updates, and support into a truthful release matrix.
---

# Assess launcher release readiness

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the release target first: version or tag, intended platforms and distribution channels, and the acceptance criteria for "ready" — which artifacts must exist, whether signing is required before distribution or merely verified as possible, and which documentation must ship with the release. Inspect the actual build outputs and release configuration rather than release notes or intent. When an equivalent reconciliation was already completed and its inputs are unchanged, reuse it instead of repeating the check.

Build the matrix one row per platform or channel. For each, confirm the artifact exists at its intended path or location and recompute its checksum against any recorded value — a recorded checksum copied into a manifest without recomputation is unverified, not verified. Check that the SBOM enumerates what the shipped binary actually contains and that provenance attestation ties the artifact to a specific source revision and build run. Confirm CI is green on the exact commit or tag being released; a passing pipeline on a neighboring branch or an earlier commit is not evidence for this release.

Assess signing readiness without performing the signature: signing identity available, tooling configured, and a test signature verifiable if the channel permits one. Distinguish "can be signed" from "is signed" and record which applies. Verify the update path — feed configuration, version metadata, and rollback or support statements — matches the artifacts actually being released, and that user-facing documentation names the correct version, platforms, and known limits. A ready cell asserted from configuration intent rather than an inspected artifact is weak evidence.

Report the matrix with each cell marked ready, blocked, or not applicable, the evidence behind each ready claim, and the specific gap behind each blocked one. Publishing, uploading, or signing for distribution is a separate effect requiring its own authorization. Use [signing and provenance](../solforge-sign-and-prove/SKILL.md) when missing checksums, SBOMs, or signing evidence must be produced before the matrix can be completed.
