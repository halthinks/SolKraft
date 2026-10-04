<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Sol Merge Report Workflow Contract

## Required Inputs

- The exact decision question and mandatory requirements.
- One target repository or codebase.
- One or more candidate repositories or codebases.
- Locators and revisions when known.
- Any target architecture, runtime, license, security, cost, or operational
  constraints supplied by the user.

## Capability Selection

The workflow must evaluate the live capability surface before prompt
generation:

1. Skills are assessed from their full instruction bodies, declared
   dependencies, availability, domain applicability, and authority limits.
2. Routes are assessed from typed deliverables, mutation modes, continuation
   contracts, and callable state.
3. Tools are assessed from registered callable contracts, schemas, flow
   ownership, and availability.
4. Titles, display names, filenames, branding, and topical keywords are not
   evidence.
5. Select the smallest set that completely covers prompt generation,
   repository study, current-source research, context curation, route
   selection, symmetric comparison, adversarial review, contract validation,
   provenance, and report production.
6. Keep an exclusion ledger. Do not select all by default.

## Repository Evidence

For every target:

- immutable revision or equivalent fingerprint;
- worktree state when local;
- complete file inventory and material-file count;
- architecture owners, interfaces, state and data flow;
- dependency manifests, lockfiles, build tools, runtimes, platforms, services,
  hardware and deployment boundaries;
- tests, CI, examples, releases, history and maintenance;
- licenses, notices, dependency licenses, security and provenance metadata;
- omitted paths and reasons;
- claim-level evidence references and contrary evidence.

README statements and package metadata are claims. They do not prove an
implemented capability without implementation/interface evidence and
test/runtime support.

## Decision Model

Each candidate receives all six dimensions:

1. capabilities;
2. architecture fit;
3. runtime and dependency fit;
4. evidence quality;
5. licensing;
6. risks.

The report also supplies integration effort, migration sequence, adapters,
validation gates, rollback, uncertainty, conditions, blockers, confidence, and
decision-changing evidence.

Allowed recommendations are `adopt`, `conditional_adopt`, `pilot`, `reject`,
and `replace`. A fatal architecture, runtime, licensing, security, or
evidence-quality conflict cannot be averaged away.

## Authority

The workflow is read-only except for writing report artifacts and immutable
SolForge state. It does not authorize Git operations, source edits, dependency
installation, external publishing, deployment, purchasing, or communication.
