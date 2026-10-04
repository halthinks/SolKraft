<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Codebase execution contract

## Required derived-capsule provenance

The active capsule must bind:

- `runId`, profile, and inherited effort-profile hash;
- parent prompt-capsule path and SHA-256;
- exact hardened-prompt SHA-256;
- exact completed Sol-result SHA-256;
- post-prompt route configuration and SHA-256;
- route-widget receipt SHA-256;
- `routeId: codebase` and `skillId: solforge-codebase`;
- repository identifier, canonical path boundary, expected HEAD, and working-tree fingerprint when available;
- mutation mode, permissions, prohibitions, budgets, deliverables, and acceptance criteria.

Reject missing, stale, altered, or mismatched provenance. Never repair an approved capsule during execution.

## Route modes

| Mode | Permitted result | Not permitted |
|---|---|---|
| `read_only` | Diagnosis, architecture map, evidence report, test results | Tracked-source writes or external effects |
| `propose_changes` | Everything read-only plus patch plan or unapplied diff artifact | Applying, committing, pushing, or deploying changes |
| `apply_approved_changes` | Exact approved writes and verification within declared paths | Any undeclared path, effect, or permission expansion |

## Evidence minimum

Each material codebase claim records repository HEAD, working-tree state, file or artifact locator, observation method, result, and verification status. Historical claims cite commits or logs. Runtime claims cite commands and outputs. Absence claims describe the search boundary.

## Acceptance minimum

Acceptance covers all inherited requirements plus repository integrity, scope compliance, test proportionality, regression risk, unsupported claims, adverse evidence, mutation receipts, and rollback evidence. The derived route cannot lower a parent requirement or terminal condition.
