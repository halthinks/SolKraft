# Semantic router proof

The legacy 100,000-request benchmark is useful for contract-policy and hardening
regression, but it is not sufficient evidence that SolKraft can route a wide
surface of natural-language requests or assemble the correct multi-skill route.

The semantic proof suite is the stronger acceptance gate.

## Corpus

### 1. One thousand distinct prompts per skill

Every bundled skill receives **1,000 distinct natural-language prompts** generated
from that skill's domain metadata and rare semantic anchors.

The 1,000 cases are split into:

- **800 development cases**
- **200 locked holdout cases**

The prompt generator varies request framing, context, tone, deliverable language,
semantic anchors, and ambiguity. A subset deliberately includes the skill's
nearest semantic neighbors as distractors.

The aggregate receipt also merges the single-skill prompt hashes from every shard and requires exactly **1,000 unique prompt hashes for every skill**.\n\nThe harness rejects corpus leakage:

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
execution authority. Any change across identical runs is a stability failure.

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

A green shard is not enough. Only the aggregate receipt may declare
`proof_passed: true`.

## Evidence

Harness:

- `scripts/semantic_router_benchmark.py`
- `scripts/aggregate_semantic_router_benchmark.py`

CI:

- `.github/workflows/semantic-router-proof.yml`

Aggregate receipt:

- `scripts/results-semantic-router-proof-summary.json` when a completed run is
  intentionally checked in.

Until that aggregate receipt passes, the public site must not describe the
legacy 100k contract replay as proof of broad semantic routing diversity.
