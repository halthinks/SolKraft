<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Code Research result contract

Bind the result to the inspected source identity, accepted scope, requirements, and evidence. Use structured output when requested; no service-generated plan or graph receipt is required.

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

`coverage` has one item for every layer in the agreed scope with `status`, `explanation`, and evidence IDs. Each cited evidence record names that exact layer in `coverageLayers`; one generic observation cannot impersonate whole-system coverage. Use distinct evidence for materially different coverage claims; fixed evidence counts do not establish completeness. A layer that is genuinely not applicable still needs evidence and an explanation; omission is not coverage.

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

Every completion gap appears in at least one remediation step and no step may name a phantom gap. Each step includes `gapIds`, a relevant skill and an available host tool, prerequisites, ordered dependencies, risks, `verification`, `rollback`, `acceptance`, stop conditions, landing, repository-qualified `intendedMutations`, and at least one repository-qualified focused test command. Regression checks are added only for directly affected boundaries, adversarial checks only for material security, safety, trust, or destructive-action risk, and a full suite only when explicitly requested or no cheaper decisive release check exists. Mutation paths are relative to the named repository and cannot escape it. These fields make remediation actionable without granting execution authority.

Every remediation step also includes a `plainLanguage` object with five non-empty fields: `currentFailure`, `exactChange`, `observableOutcome`, `check`, and `remainingUnproved`. User-facing plans, Goals, progress, and completion reports lead with these explanations. Restrictions come only from explicit user constraints and the accepted effect plan; the result must not manufacture or routinely narrate a blanket list of absent actions. Gap IDs, route names, and hashes may follow only as secondary traceability.

The target repository must remain independently buildable, runnable, testable, and understandable. Add workflow-specific state only when the task or repository requires it. A research handoff identifies proposed implementation; it does not authorize that implementation.

## Challenge and regression

`criticFindings` records an independent `challenge` and its evidence-supported `disposition`. `falsificationProbes` records a `hypothesis`, executable or inspectable `method`, and observed `outcome`. `regressionAnalysis` records the affected `boundary`, material `risk`, and non-empty executable `tests`. In focused mode each regression item has non-empty `focusBoundaryRefs` that exactly reference accepted `focusBoundary.regressionBoundary` entries. These are mandatory operational artifacts, not optional narrative.

## Completion claim

`completionClaim.status` is `qualified_complete` or `incomplete`. Qualified completion requires no critical open gap or critical unresolved uncertainty and includes `designEnvelopeHash`, the SHA-256 of the exact `endState` array. The claim is limited to the accepted design envelope.

Completion is limited to the accepted audit boundary. Bind every behavioral claim to observed checks, preserve failures and unresolved dependencies, and stop when the requested acceptance holds. No service-generated receipt or perpetual loop is required.
