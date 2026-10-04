# Add a skill the system can actually use

A skill is a reusable set of instructions for an AI agent. A contribution is more than that file: it must also teach SolKraft when to select it, prove that ordinary requests find it, and preserve existing routes.

New to GitHub? Fork this repository (make your own copy), create a branch (a separate change), edit and test the files below, then open a pull request (ask maintainers to review the change). You can give this guide to your coding agent. Do not send it your private API key.

## Give your agent this task

> Follow AGENTS.md, ENGINEERING_CONSTRAINTS_V1.json, and docs/SKILL_CONTRIBUTIONS.md. Add a complete SolKraft skill integration for [describe the useful job]. Inspect existing skills first. Deliver the entrypoint, supporting resources, provenance, semantic graph node and routing rules, justified relationships, authored selection cases, meaningful task tests, any necessary parser repairs, and generated console changes. Prove automatic selection without explicit skill IDs. Run the contribution check with --full and report the actual receipt plus realistic task evidence. Preserve existing routes and read-only API/MCP contracts. Do not submit only a SKILL.md or claim that routing simulations prove task quality.

## Required files and parameters

1. Add `solkraft/skillpacks/<skill-id>/SKILL.md`. Use a unique lowercase ID of at most 64 characters, made of letters, digits and hyphens. The folder name and frontmatter `name` must agree. Frontmatter `description` should say what the skill does and when to use it; avoid catchall descriptions. Keep the body useful: prerequisites, non-obvious procedure, result, boundaries, stop conditions, and observable success evidence. References are loaded only when needed. Helpers need executable tests and documented prerequisites.
2. Record author, license and source in `contributions/<skill-id>.json`. First-party contributions use MIT. Include required notices for upstream material and update the repository's provenance/notice records when applicable. Local installation does not establish redistribution rights.
3. Update `solkraft/skillpacks/solforge/references/selection-graph.json`, the routing authority. Add a node with `id`, `description`, `path`, `domain`, `inputs`, `outputs`, `effect: false`, `selection`, and `exit_evidence`. The path is `../<skill-id>/SKILL.md`. Inputs and outputs must describe actual artifacts or information. Exit evidence states how an agent can check its result.
4. Add a rule referencing that node. Required fields are `id`, `all` (all regexes must match), `unless` (any match excludes the rule), `lane`, and numeric `priority`. Use specific action and subject vocabulary from realistic requests. Inspect neighboring rules before choosing a lane or priority; raising priority to win every task is not a fix. Aliases, when justified, belong in the graph's matcher data. JSON regex backslashes must be escaped.
5. Add an edge only for a real relationship: `from`, `to`, `type`, and a meaningful `condition`. Both nodes must exist. Do not invent dependencies just to make the graph look connected.
6. Add authored request cases and task tests. The manifest's `cases` each contain `objective`, optional `context`, and an exact ordered `selected` list. Do not use an explicit skill list to force selection. Include different positive phrases, close neighboring intents, exclusions, quoted instructions, deferred work, compound requests, and relevant conflicts. The automated checker requires positive, excluded, quoted and deferred examples; reviewers require meaningful breadth beyond that minimum.

The composer contains some specialist mappings before the graph matcher. A new graph rule can therefore be overshadowed by an existing mapping. Test through the public `route_request` boundary. If it fails, make a focused failing test and repair the existing parser/graph boundary compatibly; do not bolt on a second independent selector. Change `DOMAIN_PATTERNS` or action segmentation only when real cases demonstrate the need.

## A copyable manifest

Start from [the executable security example](../contributions/software-security.json). It uses an existing skill so you can run the process before creating your own. Replace the ID, provenance and examples for your contribution. A minimal shape is:

```json
{
  "schema": "solkraft/contribution/v1",
  "skill": "your-skill",
  "provenance": {"author": "Your name", "license": "MIT", "source": "Your source or contribution URL"},
  "cases": [
    {"objective": "A real request for your method", "selected": ["your-skill"]},
    {"objective": "Do not perform your method", "selected": []},
    {"objective": "Perform your method tomorrow", "selected": []},
    {"objective": "Explain this quotation: \"perform your method\"", "selected": []}
  ]
}
```

This shape is a starting point, not a completed contribution. Replace every placeholder and add realistic neighboring and compound cases. Use exact expected routes, including existing skills when they belong in the answer.

## Contract authoring CLI

The contract layer can be authored and inspected without loading or executing skill bodies:

```text
solkraft contract init path/to/skill
solkraft contract validate path/to/skill/contract.yaml
solkraft contract lint path/to/skill/contract.yaml
solkraft contract show your-skill-id
solkraft contract schema
solkraft contract migrate --report build/contracts-migration.json
```

Routing policy has matching CLI flags:

```text
solkraft route "Inspect the repository" \
  --strict-contracts \
  --deny-effect deployment.* \
  --grant-capability repo.read \
  --grant-resource repo:example/project
```

These flags constrain selection only. The CLI still returns `execution_authorized: false`; grant snapshots describe host authority available for comparison and are never executable credentials.

## Run the checks locally

Install Python 3.11+, Git and Node.js. Activate your Python environment, then:

```text
python -m pip install -e ".[dev]"
python -m scripts.check_contribution contributions/software-security.json
python -m scripts.check_contribution contributions/software-security.json --full
```

For your new skill, substitute your manifest filename. The first command after installation checks registration and authored cases plus contextual variants. `--full` additionally runs the existing 100,000-request regression and `scripts.local_ci`: unit tests, UI checks, generated catalog/graph/skill pages, plugin archive, wheel, and installed MCP verification. A failed command stops the gate. The receipt is `build/contributions/latest.json`; package verification is `build/local-ci.json`.

The full result must show `status: passed`, all targeted cases passing, and exactly 100,000/100,000 regression requests. `targeted_passed` alone is not full acceptance. The receipt includes source and manifest SHA-256 hashes; rerun after source or routing changes. Do not reuse an old receipt for a different candidate.

**What 100,000 means:** this is a synthetic regression battery across ten domains. It checks routing and scope behavior on long requests. It does not contain 100,000 independent skill intents, does not evaluate the new procedure's usefulness, and does not execute an agent or hardware simulation. New-skill cases add the missing targeted coverage. Domain-specific simulations, helper tests, and realistic task demonstrations must be supplied separately where the skill needs them.

## Pre-build the contribution before opening a PR

After the local targeted cases are passing, run the reusable full preflight instead of waiting for a pull request to discover packaging or regression failures:

```text
python -m scripts.preflight_contribution contributions/your-skill.json
```

That command calls the canonical `scripts.check_contribution ... --full` gate. It therefore runs the authored routing cases, the 100,000-request regression, `scripts.local_ci`, static console generation, plugin packaging, wheel build/install verification, and installed MCP checks. It then creates a review bundle at:

```text
build/preflight/<skill>/preflight.json
build/preflight/<skill>-preflight.zip
```

The bundle includes the contribution manifest, candidate `SKILL.md`, `contract.yaml` when present, contribution/local-CI receipts, the 100,000-route result, built wheel, and plugin archive with SHA-256 hashes.

You can run the same gate in GitHub **before opening a PR**. Push the candidate branch, open **Actions → Skill Contribution Preflight**, choose that branch, enter the manifest path such as `contributions/your-skill.json`, and run the workflow. Download the `solkraft-ci-<sha>` artifact and attach or cite its receipts when you later open the PR.

The reusable implementation lives in `.github/workflows/reusable-ci.yml`. Normal repository pull requests call the same workflow through `.github/workflows/tests.yml`; the manual pre-PR wrapper is `.github/workflows/contribution-preflight.yml`. There is one validation path, not a weaker preflight and a stronger PR gate.

## Verification and trust

A Contract v1 sidecar must describe how its result can be checked using declarative evidence. New sidecars should include at least one supported check such as `artifact_exists`, `field_present`, `field_equals`, `check_equals`, or `observed_effects_subset`. Core SolKraft does not run contract-provided commands.

Skill-authored provenance describes origin only. It cannot make a skill reviewed or trusted. Trust is resolved from `solkraft/trust-bindings.json`, whose entries bind an external trust state to the exact contract and `SKILL.md` SHA-256 digests. If either file changes, the binding no longer matches and the skill becomes unreviewed again.

Legacy graph metadata can be converted into typed sidecars with:

```text
python -m scripts.migrate_contracts --report build/contracts-migration.json
python -m scripts.migrate_contracts --write --report build/contracts-migration.json
```

The migration tool never overwrites an existing sidecar and only infers an empty effect set when the legacy graph explicitly says `effect: false`. Generated sidecars carry `provenance.inferred: true` and remain `legacy-inferred`; generation is not review.

See [Verification and trust](VERIFICATION_AND_TRUST.md) for the evidence envelope, result states, trust binding model, audit receipts, and sandbox boundary.

## Submit all affected layers together

Include the entrypoint/resources, provenance/notices, graph node/rules/edges, necessary parser changes, manifest, meaningful tests, and regenerated `docs/assets` files and plugin archive. Search API, MCP retrieval and the static console derive from the same catalog; preserve that single authority. For new dependencies, document installation, portability and failure behavior. General skill contributions should not need new REST endpoints or MCP tools.

In the pull request, describe the user job, why an existing skill was insufficient, representative requests and exclusions, the actual commands/results, hashes of the checked candidate, realistic task evidence, limitations, and redistribution rights. Maintainers still review procedure quality, routing collisions, security and license rights. The gate makes integration failures visible; it cannot guarantee that every future phrase or model will select a skill.
