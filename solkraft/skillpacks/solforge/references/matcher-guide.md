<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Native matcher maintenance

Run `python scripts/select_workflow.py --objective "requested outcome" --compact`. Add `--explain` only when inspecting a match. The selector uses local rules, scoped clauses, domain context, concept aliases, and lexical ranking; it needs no model call, network, plugin, or MCP service.

## Selection contract

Explicit IDs in `--skills` remain available for every node. Automatic matching excludes effect nodes. Selection and graph follow-ups never authorize execution. Existing route arguments and result keys remain compatible; optional context, scores, trace, and status are additive.

The matcher splits stages, removes exclusions and completed or deferred work, masks quoted source instructions, and preserves formatted skill IDs. Prompt requests route to prompt writers. Report topics do not imply executing the topic. A domain hint can resolve a short request but cannot invent its action. Relative scores compare eligible rules, not confidence probabilities.

Descriptions and explicit skill IDs still enable native discovery. The script runs only when invoked; it is not a background hook into Codex's internal skill picker. Read the selected entrypoints rather than the whole graph. If wording is unsupported or a scope interpretation is wrong, select the right ID after checking the user's request.

## Change and verify

Edit `references/selection-graph.json`: rules define lane, required patterns, exclusions, and priority; matcher aliases map paraphrases to concepts. Keep effect flags and conditional graph edges intact. Prefer scoped action rules over broad topic keywords. Add a failing example before changing a rule, then run `python tests/test_matcher.py` and `python tests/test_selection_legacy.py` with `SOLFORGE_TEST_ROOT` set to the parent skills directory for the legacy suite.

The 79 authored examples include two separately authored sets. Both were used during development; their pass rate is a regression measure, not independent generalization evidence. Case and spacing variants check normalization. The suite also checks all explicit IDs, exclusions, quoted commands, invalid input, domain-only context, effects, stage order, and graph integrity. Natural-language scope remains heuristic; unfamiliar phrasing and complex nested clauses can require direct selection.

## Delivery routing regression checks

Run `python tests/test_delivery_routing.py` for software-artifact versus text-deliverable routing, CI failures, release gates, contextual follow-ups, compound stages, and authority boundaries. The 63 authored cases also run uppercase and polite-prefix variants. This is regression coverage, not a measured general-language accuracy rate.

Matcher v3 resolves compound delivery intents before generic lexical rules. `context.stage` and `--context-stage` accept `repository-release-gate`; supply this only from established session context. The selected workflow's reason states when the stage was used. Ambiguous artifact mentions abstain instead of forcing a prose route. Explicit skill IDs remain available.
