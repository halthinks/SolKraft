# Semantic router proof

## Exact-match acceptance

The current full local gate requires **473,000 actual production-router calls**
across **32 shard-slice receipts**. A complete source-bound aggregate receipt is
required before claiming acceptance. The October 10 full local CI completed that run on Windows and passed all
22 steps and all 15 semantic gates across 32/32 receipts.
The console publishes [the receipt and recorded examples](assets/semantic-proof.json)
only when the current source identity, complete corpus, and every gate agree.

| Surface | Actual routing calls required |
| --- | ---: |
| Single-skill selection and hardened policy decisions | 173,000 |
| Clarified compound exact matching | 100,000 |
| Unchanged original compound diagnostics | 100,000 |
| Repeat stability | 100,000 |
| Total | 473,000 |

## Executed current result

| Measure | Executed result |
| --- | ---: |
| Eligible exact single-skill selection, with no unresolved stages | 111,000 / 111,000 (100%) |
| Hardened policy decisions | 62,000 / 62,000 (100%) |
| Combined single-skill and policy behavior | 173,000 / 173,000 (100%) |
| Deterministic holdout behavior and minimum per-skill rates | 100% |
| Clarified compound coverage, order, and exact sets | 100,000 / 100,000 (100%) |
| Clarified compound extra selections | 0 |
| Clarified compound requests without unresolved stages | 100,000 / 100,000 |
| Repeat stability | 100,000 / 100,000, zero mismatches |
| Original compound exact sets | 44,704 / 100,000 (44.704%) |
| Original compound extra selections | 0 |
| Original compound requests without unresolved stages | 44,704 / 100,000 |
| Original requests requiring clarification | 55,296 / 100,000 |

All 473,000 calls executed the production router. Original requests remain a
separate diagnostic: 55,296 requests are now reported as ambiguous and requiring
clarification rather than being padded with extra skills. Their 44.704% exact rate
must not be described as 100%. The clarified acceptance corpus reached 100%.

The tested source-input SHA-256 is
`1404e9a26fa11f106b606089de0bbb15e375297c34fc3c28f912d30864ab6714`.
The receipt records checkout revision
`5696a981ae056bffd45242e9a53d6f1021540343`; the input digest identifies the actual
tested candidate including changes beyond that revision. Local evidence is in
`build/semantic-proof-exact/summary.json` and `build/local-ci.json`; the console
publishes the source-bound aggregate in `assets/semantic-proof.json`.

The same local CI passed 369 Python regression tests, seven Node setup tests,
four Node validation-display tests, compilation, contract and hardening gates,
static/plugin generation, wheel build and installation, outside-checkout catalog
verification, and a real packaged-plugin MCP integration check. This is Windows
local evidence, not evidence of a hosted deployment or another platform.

SolKraft must select the requested capability set without adding unrelated skills.
When public capability evidence admits several methods, the router must expose
ambiguity and request clarification rather than selecting every candidate. An
unresolved ambiguous request cannot count as a successful exact match.

The user approved clarifying ambiguous generated requests while retaining the
original corpus as a separate diagnostic. The clarified suite preserves every
original topic, expected target, and case count. It adds capability-specific words
from public metadata until the requested conjunction distinguishes its target;
it never inserts skill IDs. Improvements to public descriptions must reflect the
actual procedure and resources, rather than inventing distinctions to pass tests.

## Retained rejected baseline

The earlier October 10 run completed **373,000 calls** and **32/32 receipts** under
weaker configured gates. Its results are preserved as historical failure evidence:

| Measure | Historical result |
| --- | ---: |
| Single-skill selection and policy decisions | 172,933 / 173,000 (99.961%) |
| Eligible target selection | 110,933 / 111,000 (99.940%) |
| Hardened policy decisions | 62,000 / 62,000 |
| Compound target coverage | 100,000 / 100,000 |
| Compound target order | 99,655 / 100,000 (99.655%) |
| Exact compound skill sets | 27,697 / 100,000 (27.697%) |
| Extra compound selections | 233,968 |
| Compound requests with no unresolved stages | 60,000 / 100,000 |
| Repeat stability | 100,000 / 100,000, zero mismatches |

This baseline **does not satisfy current acceptance**. Coverage did not establish
precision, and the former gates allowed extra selections and unresolved stages.
Passing those gates was insufficient to complete the requested repair.

## Corpus

### Single-skill requests

Each of the **173 bundled skills** receives **1,000 distinct generated prompts**:
800 development cases and 200 deterministic holdout cases. Framing, context,
tone, deliverables, semantic anchors, and nearest-neighbor distractors vary.
The 111,000 eligible cases require the exact requested singleton and no unresolved
stages. The remaining 62,000 restricted-skill cases check hardened policy
decisions; that boundary check does not assert an exact empty selected set.

The aggregate merges prompt hashes across shards and requires exactly 1,000
unique hashes per skill. Ambiguous metadata remains diagnostic evidence; it
cannot substitute candidate coverage for exact target selection. The harness
rejects literal structured skill IDs, full published descriptions, copied
eight-word description spans, and duplicate single-skill prompts.

### Clarified compound requests

The acceptance suite contains **100,000 distinct requests**, each requiring two
to five selectable skills. It checks complete target coverage, exact target sets,
target order, extras, unresolved stages, and coverage by route size. Every case
executes the production router. Clarifying words preserve the original topics
and targets while making the intended capability distinguishable.

### Original compound diagnostics

The original **100,000 requests** are reconstructed from the retained original
semantic profiles in `scripts/fixtures/original-semantic-profiles.json`, with
clarification disabled, and routed through the repaired production router.
Their exact-set rate, extra selections, unresolved stages, and requests for
clarification are reported separately in `original_composition_diagnostic`.
Completion of this diagnostic is mandatory; its exact-match rate is not silently
replaced by the clarified corpus rate. Earlier baseline receipts remain retained.

### Stability executions

The suite takes **10,000 difficult base requests** from the holdout and compound
surfaces and routes each **ten times**, for 100,000 executions. Different requests
intervene between repeat rounds. Fingerprints include selected skills, stages,
unresolved work, blocked stages, and execution authority. Any variation across
identical requests fails stability.

## Proof gates

| Gate | Required result |
| --- | ---: |
| Global single-skill behavior (111,000 eligible exact selections plus 62,000 policy decisions) | 100% |
| Deterministic holdout behavior | 100% |
| Every individual skill | 100% |
| Clarified compound target coverage | 100% |
| Clarified compound target-order preservation | 100% |
| Clarified compound exact target sets | 100% |
| Clarified compound extra selections | 0 |
| Clarified compound unresolved stages | 0 |
| Repeat stability | 100%, zero mismatches |
| Metadata leakage | 0 |
| Original compound diagnostic execution | 100,000 / 100,000 |
| Executed corpus and all shard slices | Complete |
| Source identity and corpus configuration across receipts | Identical |

Smoke runs cannot pass the full-corpus gate. The current total grows by 1,000
single-skill calls for every added bundled skill. All slices must use the same
source and configuration; a green individual slice cannot declare proof complete.

## Run locally

Install SolKraft and development dependencies in an isolated environment with
Node.js available, then run the complete local CI:

```powershell
python -m scripts.local_ci --semantic-proof --semantic-workers 6 --semantic-output build/semantic-proof-exact
```

The run uses sixteen logical shards with two resumable slices each. Worker logs
and receipts are in the selected semantic output directory; its `summary.json`
is the aggregate, and `build/local-ci.json` records the complete local gate.
The default output directory is `build/semantic-proof-local/`. Resume only when
source and corpus identities match. After changing source, select a fresh output
directory through `--semantic-output` rather than mixing old and new receipts.

Only the aggregate can declare `proof_passed: true`. Inspect every gate and the
original diagnostics before publishing. The console asset is regenerated from
that aggregate through `scripts.build_semantic_console`; it must reject stale,
incomplete, or weaker evidence even if an old receipt claims success.

## Evidence and practical limits

The harness is `scripts/semantic_router_benchmark.py`; the acceptance authority
is `scripts/aggregate_semantic_router_benchmark.py`. The GitHub workflow is
`.github/workflows/semantic-router-proof.yml`. Local CI also executes authored
requests in `tests/test_natural_routing.py`, parser and ambiguity regressions,
contract boundaries, packaging, and installed wheel/plugin MCP integration.

The generated holdout comes from the same generator, not an independently
collected human-language study. **100% on the clarified tested corpus is not a
claim of perfect arbitrary-language matching.** Original ambiguous requests
remain visible diagnostics, and live routes can still require clarification.
These results concern routing and policy decisions; they do not prove skill
execution quality, installed host-agent behavior, hosted deployment, or authority
to perform effects. SolKraft remains advisory with `execution_authorized: false`.
