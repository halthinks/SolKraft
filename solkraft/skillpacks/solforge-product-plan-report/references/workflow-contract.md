# Product Plan Report Workflow Contract

## Trigger

Select `solforge-product-plan-report` when the requested terminal deliverable
combines all of the following:

1. research or evidence synthesis;
2. an MVP definition or MVP plan rather than implementation;
3. a detailed product, system, engineering, or design plan;
4. source files or repositories that must influence the result;
5. a final professional report.

The user's explicit report wording controls. Code, repository, archive, or
hardware inputs are source obligations and do not convert the route to
`solforge-codebase`.

## Prompt-generation input

### Exact text

- `exactVision`: the user's authoritative product vision verbatim.
- `requestTexts`: every mandatory request statement verbatim and in original
  order. Assign `REQ-001`, `REQ-002`, and so on.
- `reportTitle`: optional title only; it may not replace the vision.
- `profile`: normally `auto`. `single` or `multi` is accepted only with a
  matching `profileSelection` whose source is `explicit_user` and whose
  `verbatim` field preserves the user's actual topology choice.

### Source manifest

Every source has:

- a stable ID;
- kind;
- exact locator;
- description of why it is in scope;
- required status;
- `studyMode: full`;
- a SHA-256 when already available.

The generator adds `SRC-USER-REQUEST`, hashes the vision and requests, and
rejects duplicate IDs or partial study modes.

## Execute the report work

Preserve the exact vision and requests, inventory the required sources, study material inputs, research unresolved assumptions, derive architecture and MVP decisions, write the report, and inspect the finished output. Respect dependencies and use native tools actually available.

When the user supplies amendments, preserve them, identify affected decisions, retain valid evidence, and revisit dependent sections. Prompt production and report execution remain separate deliverables; no stage-claim tool, receipt service, lease, or server-generated acceptance is required.

## Mandatory report sections

- executive summary
- user vision verbatim
- source inventory
- repository study
- requirements traceability
- research synthesis
- feasibility
- system architecture
- product-line architecture
- hardware design
- software and firmware design
- networking and data
- user experience
- MVP definition
- implementation plan
- BOM and cost
- power and runtime
- security, privacy, and safety
- validation plan
- risk register
- decisions, assumptions, and gaps
- appendices

Sections directly requested by a `REQ-###` must be complete. Other sections may
be not applicable only with a rationale and evidence.

## Repository evidence

For each repository, finalization requires:

- immutable revision;
- inventory count;
- material-file review count;
- history review;
- tests review;
- omitted paths and reasons;
- concrete evidence references.

The report must map current capabilities, reusable components, incompatibilities,
migration work, and validation owners to the plan.

## Request traceability

Every `REQ-###` requires at least one:

- prompt clause;
- source or user-request evidence ID;
- report section;
- observable acceptance check.

This mapping is the defense against semantic substitution. A polished synonym
does not satisfy a missing request.

## Final acceptance

Before delivery, verify:

1. root prompt and effective directive identity;
2. completion of the required stages with concrete supporting evidence;
3. all required source studies;
4. repository evidence;
5. all effective request mappings, including amendments;
6. report-section completion;
7. the complete inline report and its hash in standalone mode, or actual
   artifact bytes against supplied SHA-256 values in durable-artifact mode;
8. no-semantic-substitution audit.

Keep delivered versions identifiable and revalidate changed output rather than claiming an earlier check covers new bytes.
