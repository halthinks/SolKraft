# Sol Search Research Contract

Use this contract for every substantial `sol-search` run. It defines source and claim quality controls for general research without requiring an external workflow runtime.

## Required research record

### Exact request

- Verbatim user request
- Decision supported
- Required freshness
- Mandatory files, repositories, datasets, reports, images, and links
- Scope exclusions and authority boundary
- Claim ceiling

### Source ledger

| Field | Requirement |
| --- | --- |
| `source_id` | Stable ID used by claims |
| `title` | Human-readable source name |
| `url_or_path` | Direct URL or absolute local path |
| `source_type` | Standard, official docs, upstream repo, paper, dataset, local source, baseline, or other |
| `date_or_version` | Publication, revision, access date, commit, or release |
| `authority` | Why this source can support the assigned claim |
| `claim_scope` | Exact claims it may support |
| `limitations` | What it cannot prove |

Order the strongest sources first. Search results and secondary summaries may
help discovery, but they are not material authority when a primary source is
available.

### Claim ledger

| Field | Requirement |
| --- | --- |
| `claim_id` | Stable ID |
| `claim` | One testable material statement |
| `classification` | Observed fact, sourced fact, inference, or recommendation |
| `status` | Supported, mixed, unsupported, or blocked |
| `confidence` | High, medium, or low with a reason |
| `supporting_sources` | Source IDs |
| `contrary_or_limiting_evidence` | Strongest counterevidence or boundary |
| `uncertainty` | Missing evidence and its decision impact |

Do not combine several independently falsifiable assertions into one claim.

## Repository study gate

When a repository is in scope, record:

- absolute root, active revision, and worktree state;
- file and directory inventory with generated/dependency exclusions;
- runtime owners for the researched behavior;
- material source, configuration, schema, test, and documentation files;
- relevant history, declared checks, and observed test evidence;
- current capability, missing capability, and recommendation-to-file mapping.

Never convert declared tests, design prose, a queued run, or a source file into
proof that runtime or physical behavior passed.

## Currency gate

For standards, APIs, models, libraries, products, or vendor capabilities that
may change:

1. identify the current revision or release;
2. check maintenance, deprecation, and replacement status;
3. preserve the accessed date;
4. distinguish historical evidence from a current integration contract;
5. state when licensed or unavailable material limits the conclusion.

## Vendor interface ladder

Evaluate each level independently:

1. product capability claim;
2. documented operator workflow;
3. accepted file or exchange format;
4. local scripting or plugin surface;
5. documented public remote API;
6. partner/private API;
7. required license, account, hardware, or commercial entitlement;
8. verified behavior on the target version and configuration.

Evidence at one level does not prove a higher level. Absence of a public API in
reviewed material means "not established," not "does not exist."

## Evidence and acceptance ladder

Use a domain-specific ladder whenever completion can be overclaimed. A typical
physical-system ladder is:

1. design prepared;
2. package exported;
3. software validation passed;
4. target preflight passed;
5. execution acknowledged;
6. target reported completion;
7. result inspected or measured;
8. result accepted for the named criteria;
9. process qualified across defined conditions.

Keep adjacent states separate in both findings and recommendations.

## Comparison contract

When comparing reports, tools, architectures, or approaches:

- use the same question and claim boundary;
- disclose dimensions and weights;
- bind each score or judgment to evidence;
- identify where the baseline remains equal or better;
- separate measured results from modeled or editorial judgments;
- never equate more sources, tokens, headings, or elapsed time with higher
  decision quality.

Useful dimensions include source authority/currency, semantic model,
execution/safety semantics, target applicability, local implementation fit,
evidence boundaries, and unresolved-risk reduction.

## Challenge audit

Record pass, fail, or not applicable for:

- material citations exist and resolve;
- no orphan sources or claims;
- no unsupported material claim;
- contrary evidence is visible;
- uncertainty changes the recommendation where appropriate;
- current versions and standards are checked;
- file/UI/API/entitlement claims remain separate;
- local code claims use concrete owners and paths;
- comparisons use a symmetric disclosed rubric;
- visuals show only supported relationships and measurements;
- multiple exports preserve the same claims and boundaries.

The audit may pass with unresolved uncertainty. It may not hide that uncertainty
or promote it into a fact.
