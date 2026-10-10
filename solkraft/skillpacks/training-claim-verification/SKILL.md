---
name: training-claim-verification
description: Use when making, changing, reviewing, or committing claims about ML training status, model-head readiness, dataset verification, proxy evidence, or RFKIT/promotion readiness.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Training Claim Verification

## Core Rule

Never call a model/head/dataset trained, ready, verified, or promotable unless an exact artifact, exact dataset evidence, and exact contract prove that claim.

## Required Checks

1. Contract check
   - Identify the exact model/head ID.
   - Find the declared contract file or schema.
   - A `trained_head` claim requires a head-specific artifact for that exact head.
   - A related model artifact is only `proxy_artifact_only` or `public_proxy_available_head_not_trained`.

2. Data check
   - Verify local data with a probe/report, hash, schema, or file-layout check.
   - Manifest-only means not verified.
   - A downloaded file is not verified until integrity and expected structure are checked.

3. Label check
   - Confirm the labels match the head objective.
   - Activity labels do not prove wearer self-motion.
   - Pose/keypoints do not prove outline, zones, or target-domain body state unless a mapper contract exists.

4. Promotion check
   - Public proxy training may complete.
   - RFKIT target-domain claims require exact RFKitChestRig captures, validation evidence, and promotion gates.
   - If stationary anchor/ground-node evidence is required, state whether it exists.

5. Red-team check
   - List what could make the claim false.
   - Search for contradictory status text in docs/reports/tests.
   - Add or update a regression test for the exact mistake before changing code.

## Mandatory Triple Check

Before changing, reviewing, committing, or repeating any training-status claim, run all three gates:

1. Artifact gate
   - Confirm the exact artifact path exists for the exact model/head ID.
   - Confirm the artifact hash matches the exact training report.
   - Confirm the report schema matches the claim type.

2. Dataset gate
   - Confirm a local verifier/probe proves the expected archive, file layout, hash, and sample count.
   - Confirm manifest-only, metadata-only, URL-only, and partial-download states remain unverified.
   - Confirm the report names the dataset variant exactly, for example `NTU-Fi-HAR` versus `NTU-Fi-HumanID`.

3. Objective gate
   - Confirm labels match the head objective.
   - Confirm a proxy objective is named as proxy only.
   - Confirm promotion boundaries say `may_promote_rfkit_claims: false` unless exact RFKitChestRig plus StationaryAnchor evidence exists.

If any gate fails, do not soften the wording. Use the exact state: `proxy_artifact_only`, `public_proxy_available_head_not_trained`, `metadata_only_not_trainable`, `manifest_only`, `adapter_missing_not_trainable`, `blocked_waiting_for_capture`, or `artifact_present_unverified`.

## Required Contradiction Search

Before finalizing, search live repo text for stale claim language:

```powershell
rg -n "trained_public_proxy|proxy_trained|ready/trained|metadata verified means|manifest-only dataset is verified|activity classifier proves self motion|shared head trained from proxy artifact" README.md CURRENT_STATE.md docs reports research training tests
```

Any hit must be either removed, corrected, or explicitly allowed by a test with context.

## Minimum Verification Commands

Before final or commit, run the smallest targeted tests plus the project-level verification that covers the claim.

For RVSAC/WiFlow-style repos:

```powershell
py -3 -m pytest tests\test_training_head_contracts.py tests\test_training_model_inventory.py -q
py -3 scripts\18_inventory_trainable_models.py --out reports\training_model_inventory.json
py -3 -m pytest tests -q
py -3 scripts\08_pipeline_status.py --require-promotable
```

The last command should fail until real RFKIT promotion evidence exists. Treat that failure as expected only after reading the output.

## Forbidden Shortcuts

- Do not infer a head is trained from a dataset-level or benchmark artifact.
- Do not call a dataset verified from a registry entry alone.
- Do not collapse HumanID, HAR, gait, self-motion, pose, outline, or tactical-state labels into each other.
- Do not replace missing RFKIT evidence with public benchmark results.
- Do not make a positive status claim without fresh command output.
- Do not call a source URL, DOI, Kaggle page, Google Drive folder, or partial archive a verified local dataset.
- Do not call a baseline artifact a shared-head artifact unless it lives under `output/shared_csi_heads/<head_id>/` and has a matching `rvsac-shared-csi-head-training-report-v1` report.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
