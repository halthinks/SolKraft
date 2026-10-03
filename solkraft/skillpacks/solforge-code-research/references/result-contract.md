# Code Research result contract

The result is a structured object bound to the accepted `planHash`, `graphHash`, `whitepaperSha256`, and `repositoryProfileSha256`. [result-schema.json](result-schema.json) is the machine-readable shape; the runtime validator adds plan-dependent hashes, coverage layers, evidence references, focused-boundary, and completion invariants.

## Required sections

- `scopeAndRepositoryGraph`
- `evidence`
- `explicitIntent`
- `inferredDesign`
- `capabilityMap`
- `inconsistencies`
- `coverage`
- `completionGaps`
- `endState`
- `remediationSteps`
- `criticFindings`
- `falsificationProbes`
- `regressionAnalysis`
- `semanticAlignment`
- `uncertainties`
- `implementationHandoff`
- `completionClaim`
- `mutations` (empty during research)
- `externalEffects` (empty during research)

## Evidence

Each evidence item has a unique `id`, `locator`, `observationMethod`, `result`, and `verificationStatus`. Include repository/revision provenance when applicable. An absence item also has `claimType: absence` and `absenceBoundary` describing files, symbols, history, commands, sources, or targets searched.

Every item in the material sections has a globally unique `id` and non-empty `evidenceIds` referring to real evidence. Inferred-design items also have `confidence` from 0 to 1 and `contraryEvidenceIds` referring only to real evidence IDs. When the contrary-evidence list is empty, `contraryEvidenceSearchBoundary` states exactly where and how contrary evidence was sought.

For `focused_mastery`, `scopeAndRepositoryGraph.focusBoundary` contains non-empty `included`, `excluded`, `regressionBoundary`, `affectedContracts`, and `affectedDependents` arrays plus an `outOfBoundaryDependencies` array. The boundary is evidence-governed; narrowing work does not erase dependencies or regression surfaces.

## Coverage and capability

`coverage` has one item for every layer in the accepted plan with `status`, `explanation`, and evidence IDs. Each cited evidence record names that exact layer in `coverageLayers`; one generic observation cannot impersonate whole-system coverage. Total completion requires at least eight distinct coverage evidence records and focused mastery at least five. A layer that is genuinely not applicable still needs evidence and an explanation; omission is not coverage.

`capabilityMap.classification` is one of:

- `implemented`
- `partial`
- `latent_underexposed`
- `emergent_inferred`
- `missing`
- `contradictory`
- `obsolete`
- `unverifiable`

## Remediation

Every completion gap appears in at least one remediation step and no step may name a phantom gap. Each step includes `gapIds`, a live registry-backed `skillId`, a callable `toolRoute`, prerequisites, ordered dependencies, risks, `verification`, `rollback`, `acceptance`, stop conditions, landing, repository-qualified `intendedMutations`, and at least one repository-qualified focused test command. Regression checks are added only for directly affected boundaries, adversarial checks only for material security, safety, trust, or destructive-action risk, and a full suite only when explicitly requested or no cheaper decisive release check exists. Mutation paths are relative to the named repository and cannot escape it. These fields are the later closure execution allowlist, not suggestions.

Every remediation step also includes a `plainLanguage` object with five non-empty fields: `currentFailure`, `exactChange`, `observableOutcome`, `check`, and `remainingUnproved`. User-facing plans, Goals, progress, and completion reports lead with these explanations. Restrictions come only from explicit user constraints and the accepted effect plan; the result must not manufacture or routinely narrate a blanket list of absent actions. Gap IDs, route names, and hashes may follow only as secondary traceability.

SolForge remains an external control plane. Remediation may not add `.solforge` state or SolForge receipts, capsules, checkpoints, research ledgers, evidence stores, required wrappers, runtime imports, or configuration to a target repository merely because SolForge performed the work. The target must remain independently buildable, runnable, testable, releasable, and understandable without SolForge installed.

`implementationHandoff.implementationAuthorized` is always false. It may contain ordered child capsule specifications, but applying them requires a separately accepted flow.

## Challenge and regression

`criticFindings` records an independent `challenge` and its evidence-supported `disposition`. `falsificationProbes` records a `hypothesis`, executable or inspectable `method`, and observed `outcome`. `regressionAnalysis` records the affected `boundary`, material `risk`, and non-empty executable `tests`. In focused mode each regression item has non-empty `focusBoundaryRefs` that exactly reference accepted `focusBoundary.regressionBoundary` entries. These are mandatory operational artifacts, not optional narrative.

## Completion claim

`completionClaim.status` is `qualified_complete` or `incomplete`. Qualified completion requires no critical open gap or critical unresolved uncertainty and includes `designEnvelopeHash`, the SHA-256 of the exact `endState` array. The claim is limited to the accepted design envelope.

In an automatic loop, a qualified Research pass with no repair steps still supplies at least one repository-qualified command in `completionClaim.testCommands.focused`. Saving clean findings is not convergence: SolForge runs and records that focused check before Mastery may inspect the changed repository independently.

Validation still ensures that research claims are structurally meaningful and evidence-backed. Execution is driven by the accepted Decision Program and plan receipts, never by Goal state or a second receipt gate. The service records the real current repository state, actual changed paths, focused-check output, and any external effects as traceability. Repository drift, an adjacent in-scope file change, a missing caller-formatted mutation record, or a failed focused check does not terminate an autonomous loop. In `auto_loop_until_stopped`, every cycle stores a readable Markdown action plan and structured JSON execution plan outside the target repositories, links them from the durable program ledger, and immediately continues. The plan includes plain-language actions, exact repository work, focused checks, and the ordered skill/tool route. A failed focused check is stored as the next repair action and updates the same program instead of forcing another approval or terminating the loop.
