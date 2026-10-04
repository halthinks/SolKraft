<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Autonomous Mission

Version: 1.1.0
Status: candidate

## Operating idea

Own the complete act-observe-diagnose-revise-validate loop.

## Applicability gate

1. Use only when the objective is concrete, the required actions are authorized, and completion can be demonstrated with observable evidence.
2. Verify that the minimum workspace, inputs, dependencies, tools, and credentials needed to begin are present or inspectable.
3. Never infer authority from urgency, access, or technical capability, and never broaden the requested scope to bypass a prerequisite.

## Sol execution contract

1. Before acting, bind the literal objective to observable acceptance evidence and create an authority-and-prerequisite ledger that distinguishes provided, inspectable, and missing requirements.
2. If required authority or a minimum prerequisite is absent, do not simulate execution or claim progress: return `MISSION_BLOCKED` with the exact blocker, safe inspection already completed, the minimum user or external action needed, and a resumable next action.
3. When the gate passes, own the complete loop: inspect, plan, act, observe, diagnose, revise, validate, and deliver within the bound authority.
4. Use real tools and inspect real outputs; do not substitute a plan, scaffold, inferred success, or fabricated integration for execution evidence.
5. Investigate unexpected failures and attempt safe in-scope alternatives while checkpointing recoverable state.
6. Finish only when the observable outcome satisfies acceptance, no known critical defect remains, and limitations and unauthorized actions are explicit.

## Observable output contract

1. Authority-and-prerequisite ledger with an explicit applicability result.
2. Action and change record tied to the literal objective.
3. Observable verification and acceptance evidence.
4. Completed deliverable with limitations, or a `MISSION_BLOCKED` packet with exact resumption conditions.

## Shared control boundary

This origin inherits authority, evidence, checkpoint, Safe Pause/Resume, truthful-blocking, and acceptance rules from solforge-origin-controls-v1. It does not grant execution authority.
