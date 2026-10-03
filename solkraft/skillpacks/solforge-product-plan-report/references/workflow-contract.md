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
  order. The server assigns `REQ-001`, `REQ-002`, and so on.
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

## Prompt-generation output

The generator returns:

- exact immutable prompt and SHA-256;
- exact directive path and SHA-256;
- all evaluated production origins and the selected Product Systems Masterplan
  origin;
- Single or Multi topology;
- topology selection source and evidence;
- Full-Power effort controls;
- live capability inventory selected by operation evidence from actual skill,
  route, and tool contracts rather than names;
- request and source manifests;
- report-only authority;
- a durable stage program with required work units, required operations,
  selected capabilities, dependencies, and recovery state;
- an explicit user choice between standalone-chat and durable-artifact
  delivery;
- an exact accepted-plan completion hash.

Prompt generation writes no product source and starts no execution.

## Durable execution

Execution starts through `solforge_run_plan_report` only after the user chooses
`standalone_chat` or `durable_artifact`. The choice is immutable. Goal state is
informational and never consulted in either mode.

The program is a DAG:

1. intake lock;
2. source inventory;
3. full source study, full repository study, requirements traceability, and
   external research become independently runnable after source inventory;
7. architecture and MVP;
8. report writing;
9. independent challenge;
10. package and finalization preparation.

Every runnable node must first be atomically claimed with
`solforge_claim_plan_report_stage`. Claims bind stage, worker, revision, token,
and lease. Independent nodes may hold simultaneous claims. Stale revisions,
expired claims, duplicate claims, cross-worker recording, and double-completion
are rejected.

`solforge_record_plan_report_stage` accepts a claimed completed stage only when every
declared work unit has an evidence-backed result receipt and every required
operation has a receipt from a capability selected for that operation. Stage
dependencies, hashes, and idempotency are server enforced. A blocked receipt
keeps the stage recoverable; `solforge_run_plan_report` returns all runnable
nodes, active claims, and dependency blockers after restart, interruption, or
context compaction.

Pass counts written in prose are not execution evidence. Only persisted
work-unit, capability, and transition receipts count.

## Append-only amendments

Before acceptance, every later user request or source enters through
`solforge_amend_plan_report`. The amendment:

- preserves the new request verbatim;
- assigns the next stable `REQ-###` and source IDs;
- writes an immutable hash-linked directive supplement;
- updates effective request and source manifest hashes;
- archives prior affected stage executions without erasing them;
- preserves still-valid source and requirement receipts by exact ID;
- reopens every affected downstream stage.

The root prompt hash never changes. Finalization binds both the root prompt and
the latest effective directive, request register, source manifest, and amendment
lineage.

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

`solforge_finalize_plan_report` verifies:

1. root prompt and effective directive identity;
2. completion of every durable execution stage and receipt contract;
3. all required source studies;
4. repository evidence;
5. all effective request mappings, including amendments;
6. report-section completion;
7. the complete inline report and its hash in standalone mode, or actual
   artifact bytes against supplied SHA-256 values in durable-artifact mode;
8. no-semantic-substitution audit.

The acceptance receipt is immutable and idempotent. A different package cannot
replace an accepted package under the same session.
