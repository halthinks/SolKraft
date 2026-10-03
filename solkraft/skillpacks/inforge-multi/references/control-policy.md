# InForge production control policy

Control version: 3.0.0

## Operating decisions

- Full whole-document transposition is mandatory for InForge Single, Multi, and Ultra. Do not automatically shorten simple tasks. A compact profile requires a separately named future skill and explicit user selection.
- Transposition and execution are separate. The skill returns a prompt only. The provenance field `execution_boundary=transpose_only` is mandatory.
- Use semantic golden contracts rather than exact-prose snapshots. Different wording may pass only when every user requirement and every required source role is evidenced.
- Keep the private audit package out of the returned prompt. The prompt contains only the final provenance line and, when required, the confirmation gate.

## Structured intent record

Create these fields before drafting:

- `objective`: nonempty string.
- `scope`, `inputs`, `assumptions`, and `authorization_boundaries`: arrays of strings.
- `constraints`, `deliverables`, `acceptance_criteria`, and `unacceptable_partial_outcomes`: arrays of objects with unique `id` and nonempty `text`.
- `search_policy`: the task-appropriate search rule and its source in the user request or higher-priority policy.
- `risk_categories`: zero or more categories from the list below.
- `high_consequence`: true exactly when `risk_categories` is nonempty.
- `confirmation_required`: equal to `high_consequence`.

## High-consequence categories

1. `destructive_or_irreversible`: deletion, irreversible migration, key rotation, destructive overwrite, or comparable loss risk.
2. `external_side_effect`: sending messages, publishing, purchasing, submitting, or changing third-party state.
3. `production_or_deployment`: production changes, releases, deployments, rollbacks, or live infrastructure.
4. `security_or_privileged_access`: exploitation, privilege changes, access-control changes, or sensitive security operations.
5. `credentials_or_sensitive_data`: secrets, credentials, private personal data, regulated data, or confidential datasets.
6. `financial_commitment`: spending, trading, binding procurement, or material resource commitment.
7. `legal_medical_financial_reliance`: outputs intended for consequential legal, medical, or financial reliance.
8. `broad_scope_state_change`: large-scale mutations whose exact blast radius is not already bounded.

For any high-consequence task, insert this sentence verbatim after the transposed task specification and before instructions that authorize execution:

`Before performing any state-changing or externally consequential action, present the transposed scope, deliverables, acceptance criteria, and irreversible or external effects to the user and obtain explicit confirmation.`

Do not insert the gate for a purely read-only, low-consequence task. A high-stakes read-only analysis may still require the gate if the prompt directs the later agent to act on the result.

## Private role map

Create one entry for every `required_role_id` in `manifest.json`:

- `source_role_id`
- `source_function`
- `status`: `mapped` or `not_applicable`
- `task_expression`
- `prompt_evidence`: an exact substring from the final prompt
- `requirement_ids`: referenced constraint, deliverable, acceptance-criterion, or insufficient-outcome IDs
- `authorization_basis`: `user_explicit`, `higher_priority_policy`, `derived_nonexpansive`, or `not_applicable`
- `feasibility_basis`
- `search_policy_basis`
- `justification`: required for `not_applicable`

Every user requirement ID must appear in at least one mapped role. `omitted_requirement_ids` and `added_permissions` must both be empty.

## Feasibility and authority controls

Record every consequential feasibility claim with `claim`, `status` (`verified`, `assumption`, or `unknown`), and `basis`. Do not turn an assumption into a verified fact. Do not translate “assume a proof exists” into a false guarantee that the user's task is feasible.

Derived requirements may clarify or operationalize the user's request but may not expand authorization. Any new permission, system, recipient, destructive action, publication, or financial commitment fails validation.

## Provenance

Append one final line after the transposed search paragraph:

`InForge provenance: profile=<profile>; control_version=<control_version>; source_version=<source_version>; source_sha256=<source_sha256>; contract_sha256=<contract_sha256>; execution_boundary=transpose_only`

Fill every value exactly from `references/manifest.json`. Do not shorten hashes or alter field order.

## Pass criteria

A package passes only when:

1. Bundle hashes match.
2. All required structured-intent fields exist.
3. Every required source role is mapped or explicitly justified as not applicable.
4. Every user requirement ID has prompt evidence.
5. No user requirement is omitted.
6. No permission is added.
7. Risk classification and confirmation behavior agree.
8. Prompt evidence substrings exist exactly in the prompt.
9. Structural transposition validation passes.
10. The exact provenance line is present.
