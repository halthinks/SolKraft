# Semantic router proof

## Completed local result

The October 10 local run completed **373,000 production-router calls** and all
**32/32 shard-slice receipts**. Every configured gate passed. The console's
downloadable [receipt and recorded examples](assets/semantic-proof.json) contains
the exact tested source identity, aggregate metrics, per-skill results, and
sample failures. The release gate regenerates this asset only from a completed
proof whose source inputs match the current checkout.

| Measure | Executed result |
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

The minimum individual skill rate was 93.3%; minimum individual holdout rate
was 93%. All 2,000 cases for skills with ambiguous metadata were executed and
covered. There were no duplicate single-skill prompt hashes or detected metadata
leaks. The authored everyday-language regression suite passed separately.

**Precision remains a limitation.** Extra methods and unresolved stages require
route review. This acceptance gates coverage and order, not exact matching.
The holdout comes from the same generator; it is not a representative independent
human-language study. No skill execution, installed agent behavior, hosted
deployment, or universal semantic accuracy is claimed by these results.

The legacy 100,000-request benchmark is useful for contract-policy and hardening
regression, but it is not sufficient evidence that SolKraft can route a wide
surface of natural-language requests or assemble the correct multi-skill route.

The semantic suite checks generated capability matching and composition. The
independent authored requests in `tests/test_natural_routing.py` also check exact
routes, everyday wording, exclusions, context isolation, and ordering in local CI.

## Corpus

### 1. One thousand distinct prompts per skill

Every bundled skill receives **1,000 distinct natural-language prompts** generated
from that skill's domain metadata and rare semantic anchors.

The 1,000 cases are split into:

- **800 development cases**
- **200 deterministic holdout cases** (from the same generator, not independently
  collected user requests)

The prompt generator varies request framing, context, tone, deliverable language,
semantic anchors, and ambiguity. A subset deliberately includes the skill's
nearest semantic neighbors as distractors.

The aggregate receipt merges single-skill prompt hashes from every shard and
requires exactly **1,000 unique prompt hashes for every skill**.

Skills without a unique metadata conjunction are still executed and counted;
their candidate coverage is reported separately as ambiguity coverage. They are
never credited without calling the router.

The harness rejects corpus leakage:

- no literal structured skill IDs;
- no full published descriptions;
- no copied eight-word description spans;
- no duplicate prompt within a shard.

This corpus is deterministic and generated. It is not represented as 1,000
independently human-authored requests.

### 2. One hundred thousand multi-skill composition requests

The composition suite produces **100,000 distinct requests** that require between
**two and five selectable skills** in the same request.

It measures:

- whether every required target skill is selected;
- exact target-set match;
- whether target order is preserved as a subsequence when support skills are
  inserted;
- unresolved-stage rate;
- extra selected skills;
- coverage by route size.

This is the suite that tests SolKraft's central claim that it can turn one
compound request into a useful sequence of capabilities.

### 3. One hundred thousand stability executions

The stability suite selects **10,000 difficult base requests** from the holdout
and composition surfaces and routes each one **10 times**.

It fingerprints selected skills, stages, unresolved work, blocked stages, and
execution authority. Different requests intervene between repeat rounds. Any
change across identical runs is a stability failure.

## Current execution count

With the current 173-skill bundle, the full proof executes:

- 173,000 single-skill semantic cases;
- 100,000 composition cases;
- 100,000 stability executions;

for **373,000 routing executions**.

The total automatically grows if the catalog gains more skills because every
skill still receives 1,000 single-skill cases.

## Proof gates

The aggregate receipt currently requires:

| Gate | Threshold |
| --- | ---: |
| Global single-skill behavior | >= 95% |
| Locked holdout behavior | >= 95% |
| Every individual skill | >= 90% |
| Multi-skill target coverage | >= 90% |
| Multi-skill target-order preservation | >= 95% |
| Repeat stability | 100% |
| Metadata leakage | 0 |
| Executed case counts and all shard slices | Complete |
| Source identity and corpus configuration across receipts | Identical |

Smoke-size runs cannot pass the full-corpus gate. Exact composition sets and
extra selections are reported even though the historical acceptance thresholds
gate coverage and order. A passing generated corpus does not establish perfect
precision on arbitrary language, execution of skills, or a deployed release.

## Run locally

Install SolKraft and its development dependencies in an isolated environment,
with Node.js available. Run:

```powershell
python -m scripts.local_ci --semantic-proof --semantic-workers 6
```

The default full run uses sixteen logical shards with two resumable slices each.
Receipts and worker logs are under `build/semantic-proof-local/`; the aggregate
is `summary.json` and the complete local gate is `build/local-ci.json`.
Interrupted work can resume with the same command only when source and corpus
identities match. After editing source, choose a fresh output directory with
`python -m scripts.local_semantic_ci --output build/semantic-proof-next`.

A green shard is not enough. Only the aggregate receipt may declare
`proof_passed: true`.

## Evidence

Harness:

- `scripts/semantic_router_benchmark.py`
- `scripts/aggregate_semantic_router_benchmark.py`

CI:

- `.github/workflows/semantic-router-proof.yml`

Aggregate receipt:

- `build/semantic-proof-local/summary.json` for the completed local run.
- `docs/assets/semantic-proof.json` publishes that source-bound aggregate and
  recorded production routing examples for the console.

Until that aggregate receipt passes, the public site must not describe the
legacy 100k contract replay as proof of broad semantic routing diversity.
