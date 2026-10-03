# Code Research mastery contract

## Purpose

Code Research reconstructs what the system is, what it was intended to be, what its existing mechanisms make possible, what prevents that capability from being real, and the exact evidence-supported program needed to close the difference.

It is not merely static analysis, test coverage, architecture review, feature ideation, or a defect list. Those are evidence lanes inside one design-envelope investigation.

## Semantic reference

Planning is bound to the released SHA-256 of `docs/whitepapers/solforge-autonomous-work-system-whitepaper.md`. The result must include a semantic alignment matrix for:

- the compact public surface and complete Advanced reachability;
- live callable capability proof;
- top-three routing and Advanced all;
- dependency-aware steering;
- final acceptance as exact authority and direct approved-plan dispatch;
- truthful provider and tool availability;
- hash-bound capsules, evidence handoffs, recovery, and acceptance;
- explicit uncertainty and claim-to-evidence mapping; and
- versioned policy without opaque drift.

## Design reconstruction

Separate three forms of intent:

1. **Explicit intent** — directly supported by the user objective, public promises, documentation, schemas, types, tests, manifests, decisions, issues, or history.
2. **Inferred intent** — the strongest design explanation that reconciles implementation structure and behavior. It requires confidence, support, contrary evidence, and alternatives.
3. **Latent design consequence** — a capability or constraint implied by existing mechanisms and composition but not fully named or exposed. It must not be reported as implemented without behavioral evidence.

Map invariants, state machines, interfaces, data ownership, error and recovery behavior, trust boundaries, target platforms, packaging and release behavior, and user-visible workflows where applicable.

## Inconsistency classes

Inspect source, architecture, interfaces/contracts, configuration, tests, build, packaging, runtime, UX, security/trust, data/state, portability, documentation, release, and operations. Classify at least:

- declaration/implementation divergence;
- sibling or companion drift;
- unreachable or decorative capability;
- partial lifecycle;
- missing failure or recovery path;
- incompatible invariant or state transition;
- stale documentation, schema, manifest, or test oracle;
- unsafe trust or authority boundary;
- target/platform mismatch;
- missing verification or unsupported completion claim; and
- obsolete code whose retained behavior contradicts the current envelope.

## Completion standard

Total completion passes only when every material design-envelope item is implemented and verified, explicitly rejected with evidence, or retained as a declared blocker. A critical open gap, critical unresolved uncertainty, unverified required target, stale fingerprint, or unsupported absence claim blocks `qualified_complete`.

Focused mastery uses the same rule inside its accepted boundary. Out-of-boundary discoveries are recorded with their dependency and risk but do not silently expand scope.

## Route integrity

Every remediation step names a live registry-backed skill and callable route, prerequisites, repository-qualified intended mutations, at least one repository-qualified focused check, verification evidence, rollback, acceptance, stop conditions, and landing. Regression checks are conditional on directly affected boundaries, adversarial or falsification checks on material security, safety, trust, or destructive-action risk, and full-suite checks on explicit user direction or the absence of a cheaper decisive release check. Repository IDs are canonical and case-colliding identities are invalid. Relative mutation paths may not escape their declared repository and remediation may not invent gap IDs. Test-runner arguments that collect, import, skip, or otherwise produce a success code without executing the declared tests are invalid. Package-manager script wrappers cannot qualify as decisive evidence. A zero exit is still a failure unless evidence proves a positive pass count from the invoked runner. Node additionally requires explicit repository-local test files whose source hash and AST-bound literal test registrations are captured and observed in runner output. Pytest executes with a fresh service-owned configuration, cleared `addopts`, disabled plugin autoload, and a service-owned JUnit report whose pass/failure/error/skip counts determine acceptance. The accepted Decision Program and plan receipts are the execution contract. The closure program may select `auto_loop_until_stopped`; every later cycle updates the durable program ledger and links complete readable and structured action files stored under the external SolForge data root. Those files name the ordered SolForge skills, Codex skills, MCP tools, built-in tools, subagents, and loop functions required for the cycle. No later approval is required for unchanged scope. Receipts and fingerprints preserve traceability and tell the next planner what changed; they do not deny in-scope execution. A changed repository is re-read and replanned under the active program. Goal state is ignored. Only direct user Pause or Stop, qualified completion, or a genuine missing-access or external-dependency blocker stops dispatch.

Closure recording is single-writer and intent-bound. An atomic renewable lease prevents concurrent retries from executing the same tests twice across the selected bounded commands; a completed replay succeeds only when its canonical recording-intent hash is identical. An exact replay of a failed intent returns the existing failure receipt without rerunning tests. The service runs the selected commands in each declared repository, strips inherited parent test-runner control state, captures stdout and stderr content plus hashes, and durably records failed attempts before returning failure. Every repair claim names one failure receipt from the same program, cycle, and strategy and cites that receipt's retrievable failed evidence. A successful execution receipt binds the actual per-repository file delta. In bounded modes it terminates the accepted repair cycle. In `auto_loop_until_stopped` it atomically advances to the next receipt-bound research iteration unless the user paused or stopped the loop.

## Repository fingerprint

The request service resolves each supplied root to an absolute path and computes `content-tree-sha256-v1`. It walks directory entries in lexical order, excludes only `.git` internals, records directories, symlink targets, special entries, relative file paths and sizes, and hashes every regular-file byte. For a Git worktree it additionally binds the canonical Git root, HEAD, and porcelain status as `content-tree-sha256-v1+git-head-status`. Acceptance, plan compilation, result validation, and result recording recompute the same fingerprint and fail closed on drift. This makes non-Git skill packages first-class while retaining Git provenance when available.

Local SolForge session state, receipts, evidence ledgers, and accepted research artifacts are permitted provenance. They are not target repository `mutations` and are not `externalEffects`; both result arrays remain empty throughout read-only research.
