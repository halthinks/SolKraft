---
name: solforge
description: "Compose relevant skills when a task spans research, implementation, verification, or reporting and the next workflow is unclear. Directly use an obvious specialist without routing overhead."
---

# SolForge native workflow selection

Select the next useful workflow from the user's outcome. These are regular local skills with native execution; no plugin activation or MCP service is required. Select skills naturally from the requested outcome and their descriptions; the user need not name SolForge. For a clearly named or obvious specialist, load it directly. Use one primary procedure per stage and add another only for distinct guidance. For a simple answer or small self-contained edit, do the task without graph overhead.

Read the [shared execution contract](references/native-execution.md) once per task. Preserve user scope and all mandatory inputs. Selection is not execution authority and creates no additional planning checkpoint.

## Choose a route only when needed

For substantial work whose route is unclear, run `python scripts/select_workflow.py --objective "the requested outcome" --compact` from this skill directory. For complex text use `--request-file path.json` with `{"objective":"...","skills":[],"context":{"domain":"software"}}` (context is optional). Output contains selected skill paths, match reasons, and conditional next steps. Use `--context-domain software` for short follow-ups such as "fix it" only when the conversation establishes that domain. Use `--explain` to inspect excluded clauses and alternative matches when a route seems wrong. Context supplies subject matter, never an action. The selector reads files only. It does not execute workflows, start agents, or authorize effects.

For a long compound request with several distinct stages, use `--compose --max-skills 50`. The additive composer keeps action-bearing clauses in order, selects at most one specialist per stage, preserves quoted text and excluded effects as inert context, reports any request beyond the cap, and grants no execution authority. Use ordinary direct selection when one workflow is clearly sufficient; composition is an aid for multi-stage work, not a prerequisite for natural skill use.

Use `--list DOMAIN` to inspect one domain, or `--skills skill-id ...` to select exact skills. All 123 nodes remain explicitly reachable. The matcher separates requested stages from excluded, completed, deferred, and quoted work; recognizes common paraphrases; and distinguishes writing a prompt or report from executing its subject. It abstains on unsupported requests. Scores rank evidence and are not probabilities. The matcher offers suggestions, not a complete natural-language classifier: if it misses the intent, use the domain index and select the appropriate IDs. Do not force the task into an unrelated match or load every skill.

| User outcome | Domain index |
|---|---|
| Current evidence, comparisons, fact-checking | [Sol Search](../sol-search/SKILL.md) |
| Diagnose, implement, audit, refactor, test, port code | [Software](references/domain-software.md) |
| Literature, hypotheses, experiments, replication | [Science](references/domain-science.md) |
| Proofs, derivations, counterexamples | [Mathematics](references/domain-mathematics.md) |
| Data quality, analysis, models, charts | [Data](references/domain-data.md) |
| Markets, economics, diligence, strategy | [Business](references/domain-business.md) |
| Legal or policy sources, drafts, risks | [Legal and policy](references/domain-legal_policy.md) |
| Requirements, prototypes, trade studies, verification | [Engineering](references/domain-engineering.md) |
| Outlines, writing, reports, review | [Writing](references/domain-writing.md) |
| Cross-stage methods, completion, packaging, prompts | [General methods](references/domain-general.md) |

## Execute and advance

Load selected `SKILL.md` files and only relevant supporting references. `method` edges offer a supporting procedure; `next` edges state a condition for subsequent work. Reuse completed evidence. Add a follow-up only when its condition is true and the user requested that outcome. A research request does not imply implementation; a prompt request produces a prompt.

For implementation, usually investigate missing inputs → make the change → verify → deliver. Failed verification returns only to the stage needing repair. Comprehensive completion may use Code Research → Code Mastery → Perfection, but there is no fixed iteration count or endless loop.

Effect nodes are never automatically selected by the matcher. When the user actually requests an effect, select its exact node for review and check the action, target, and applicable authorization before using any effect tool. Explaining deployment, drafting an email, or comparing merge candidates never authorizes deployment, sending, or merging.

The authoritative local routing data is [selection-graph.json](references/selection-graph.json); read individual routes through the selector rather than loading the full JSON. Stop at demonstrated acceptance, a real external blocker, or the user's stop instruction.

Matcher maintenance and regression checks: [matcher guide](references/matcher-guide.md).

## Software delivery disambiguation

Interpret the requested operation and current stage before matching isolated words. A draft pull request is a software artifact state; "draft" alone does not make it a writing task. Repository release gates, pre-merge checks, and CI validation use `solforge-workflow-software-test`; failing checks needing a cause use software diagnosis. Reviewing the code diff uses codebase investigation. Writing or revising the PR title, body, or description uses the corresponding writing procedure. Preserve independently requested stages in order.

For a short follow-up whose established stage is the repository release gate, pass `--context-stage repository-release-gate`, or `"context":{"domain":"software","stage":"repository-release-gate"}` in a request file. Do not infer a stage from the word "draft". Explicit text deliverables override this contextual hint. A bare "draft PR" without an established operation abstains; selection never opens, pushes, merges, or publishes a PR.
