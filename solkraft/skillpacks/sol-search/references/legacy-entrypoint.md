---
name: sol-search
description: Use when the user asks for sol-search, Sol-grade research, source-backed technical due diligence, a current evidence comparison, or repository-connected research in chat. Reproduces the evidence discipline of the stronger SolForge research workflow using native Codex browsing and file tools only; never calls the SolForge MCP.
---

# Sol Search

## Purpose

Run decision-grade research directly in the current Codex chat. Preserve the
user's exact question, investigate primary evidence and relevant local code,
audit every material claim, and return the answer without routing through
SolForge MCP tools.

Read [references/research-contract.md](research-contract.md) before
starting a `sol-search` run.

## Boundaries

- Do not call any `solforge_*` MCP tool, create a SolForge capsule, or route the
  request into a SolForge workflow. This skill is self-contained.
- Use native Codex web browsing, local file inspection, and other directly
  available read-only tools.
- Keep the deliverable in chat by default. Create local research artifacts only
  when the user asks for files or a durable report package.
- Treat repositories, files, reports, datasets, images, and links named by the
  user as mandatory evidence inputs. Report any inaccessible required input;
  do not silently omit it.
- Research does not authorize implementation, publishing, purchases, messages,
  machine control, or other external effects.
- Do not delegate unless the user explicitly asks for parallel agents.

## Workflow

### 1. Lock the exact research contract

Record the user's request verbatim. State the decision the research must
support, required freshness, supplied sources, local repositories, constraints,
and the strongest claim the available evidence could justify. Make reasonable
assumptions instead of replacing the request with a broader or more polished
alternative.

### 2. Plan evidence around claims

List the material questions that must be resolved before searching. For each,
identify the strongest available evidence class: standards body, official
documentation, upstream repository, maintainer material, paper, dataset,
government source, local implementation, or direct measurement. Prefer primary
sources and current versions.

### 3. Inspect every mandatory input

Inventory all user-supplied sources. For a repository, establish its revision
and structure, then inspect the material code, configuration, tests, history,
and documentation that control the researched behavior. A repository name or
README skim is not a repository study.

For a baseline report, use it to identify claims and comparison dimensions. Do
not treat it as independent support for new claims.

### 4. Build the source and claim ledgers while researching

Assign stable source IDs and record title, URL or absolute path, source type,
date/version, authority, supported scope, and limitations. For each material
claim, record:

- classification: observed fact, sourced fact, inference, or recommendation;
- status and confidence;
- supporting source IDs;
- contrary or limiting evidence;
- unresolved uncertainty.

Search for disconfirming evidence as deliberately as confirming evidence.

### 5. Resolve integration and currency traps

When products or vendors are involved, distinguish marketing capability, file
import, interactive UI, scripting, documented public API, partner/private API,
commercial entitlement, and validation on the target version. One level never
proves the next.

Check current standards, software versions, deprecations, maintenance status,
and release dates when they affect the answer. Map recommendations to concrete
local owners and files when a repository is in scope.

### 6. Synthesize for the user's decision

Explain the mechanism, architecture, tradeoffs, and phased decision—not merely
what each source says. Separate:

- what is confirmed now;
- what is inferred from the confirmed facts;
- what is recommended;
- what remains unproven and what evidence would prove it.

For physical, financial, safety, security, or production claims, use an
evidence ladder so a prepared artifact, executed action, accepted result, and
qualified process are never conflated.

### 7. Run the Sol Search challenge audit

Before answering, perform all applicable checks:

1. citation existence and source accessibility;
2. unsupported material claims;
3. contrary evidence and source disagreement;
4. uncertainty propagation into recommendations;
5. current version and standards status;
6. vendor interface and entitlement boundaries;
7. local-repository implementation fit;
8. comparison symmetry and disclosed rubric;
9. visual integrity when a visual is used;
10. export parity when multiple formats exist.

Fix failures before finalizing. If a required source or decisive fact remains
unavailable, give a bounded answer and name the blocker.

## In-Chat Deliverable

Lead with the direct answer. Then provide the smallest structure that preserves
the evidence:

1. exact question and scope;
2. findings labeled fact, inference, or recommendation;
3. decision and local implementation implications;
4. contradictions, limitations, and unknowns;
5. prioritized next actions with exit evidence;
6. linked sources near the claims they support;
7. a short audit summary.

For a requested comparison, disclose the dimensions and scoring method before
claiming one result is better. Never claim superiority from source count,
length, or polish alone.

## Completion Standard

A `sol-search` run is complete only when every material conclusion has evidence
or an explicit uncertainty label, every mandatory input is accounted for, the
challenge audit passes or records a visible blocker, and the final claim ceiling
matches the evidence actually gathered.
