# Code Research mastery contract

## Purpose

Code Research reconstructs what the system is, what it was intended to be, what its existing mechanisms make possible, what prevents that capability from being real, and the exact evidence-supported program needed to close the difference.

It is not merely static analysis, test coverage, architecture review, feature ideation, or a defect list. Those are evidence lanes inside one design-envelope investigation.

## Semantic reference

Use the current user objective and repository contracts as the design authority. Compare public capability claims with real call paths, input dependencies, failure behavior, recovery, and observed outputs. Cite the exact source revision and distinguish implemented, inferred, incomplete, and unavailable capability. No SolForge whitepaper hash or external decision service is required.

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

Every remediation step identifies the gap, affected source boundary, prerequisites, intended changes, decisive verification, risk, and recovery. Choose actual host tools and relevant skills; do not invent registered adapters. Run checks that exercise the claimed behavior, inspect their result, and distinguish skips and setup failures from passes. Order repairs by dependency, preserve existing authority, and stop when the accepted end state is demonstrated.

## Repository fingerprint

Bind material findings to the actual repository revision, working-tree state, files, or artifact hashes needed for reproducibility. Re-read changed boundaries and invalidate only evidence that depends on them. Hashes identify content; they do not establish behavioral correctness or grant authority.
