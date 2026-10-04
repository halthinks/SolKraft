"""Cloud-shard validator for 100,000 advanced SolKraft requests.

Expands the original 25 ask families to 100 using four adversarial modifiers,
then deterministically shards the same 100,000-case corpus across cloud workers.
Every processed case must pass; any miss exits nonzero after printing a compact
JSON summary for aggregation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import time

import scripts.advanced_contract_benchmark as base
import solkraft.routing as routing_module
from solkraft.catalog import SkillCatalog
from solkraft.contract_policy import evaluate_contract, normalize_policy
from solkraft.contracts import contract_from_node
from solkraft.routing import BUNDLE_ROOT, catalog_graph, contract_index, route_request


ASK_MODIFIERS = (
    "Also distinguish the target capability from adjacent skills that may sound similar, and keep the final method specific to the published capability.",
    "Include one misleading near-neighbor interpretation, reject it explicitly, and preserve evidence showing why the selected capability is the correct one.",
    "Assume one input is incomplete or ambiguous; identify what can proceed, what must be elicited, and what evidence resolves ambiguity without changing capability identity.",
    "Treat this as a compound operational context with distracting constraints, while preserving the primary specialist ask and making the chosen capability independently reviewable.",
)
ASKS = tuple(
    f"{ask} {modifier}"
    for ask in base.ASKS
    for modifier in ASK_MODIFIERS
)
assert len(ASKS) == 100

TOTAL_REQUESTS = 100_000
EXACT_WORDS = 250


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    args = parser.parse_args()
    if args.shard_count < 1:
        parser.error("--shard-count must be >= 1")
    if not 0 <= args.shard_index < args.shard_count:
        parser.error("--shard-index out of range")
    return args


def main():
    args = parse_args()
    started = time.perf_counter()

    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    entries = {entry["id"]: entry for entry in index.entries()}

    # Immutable benchmark metadata is frozen once per shard. Each request still
    # executes production route_request -> policy -> dataflow -> validation.
    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index

    skill_count = len(records)
    base_count = TOTAL_REQUESTS // skill_count
    remainder = TOTAL_REQUESTS % skill_count

    totals = Counter()
    failures_by_skill = Counter()
    sample_failures = []
    processed = 0
    global_case = 0

    for skill_ordinal, record in enumerate(records):
        entry = entries[record.id]
        node = graph["nodes"][record.id]
        expected = base.expectation(entry, node)
        case_count = base_count + (1 if skill_ordinal < remainder else 0)
        description = " ".join(base.words(record.description)[:48])
        if not description:
            description = "perform the specialized procedure described by this bundled skill"

        for local_case in range(case_count):
            case_id = global_case
            global_case += 1
            if case_id % args.shard_count != args.shard_index:
                continue

            processed += 1
            ask_id = local_case % len(ASKS)
            subject = base.SUBJECTS[(local_case + skill_ordinal * 7) % len(base.SUBJECTS)]
            active = ASKS[ask_id].format(description=description, subject=subject)
            prompt = base.exactly_250(
                active,
                case_id=case_id,
                skill_ordinal=skill_ordinal,
                variant=ask_id,
            )

            policy = {"contract_mode": "hardened"}
            route = route_request(catalog, prompt, max_skills=50, policy=policy)
            contract = contract_from_node(node)
            target_decision = evaluate_contract(
                contract,
                normalize_policy(policy, prompt),
            )

            selected = route.get("selected") or []
            selected_contracts = route.get("selected_contracts") or {}
            invalid_selected = [
                skill_id
                for skill_id, compact in selected_contracts.items()
                if compact.get("status") in {"opaque", "invalid", "unsupported"}
            ]

            exact_words = len(base.words(prompt)) == EXACT_WORDS
            safety_ok = all((
                exact_words,
                route.get("execution_authorized") is False,
                (route.get("route_policy") or {}).get("contract_mode") == "hardened",
                not invalid_selected,
            ))

            if entry.get("status") in {"opaque", "invalid", "unsupported"}:
                policy_ok = target_decision["status"] == "denied"
            else:
                policy_ok = target_decision["status"] != "denied"

            if expected == "select-target":
                expectation_ok = record.id in selected
                totals["eligible_cases"] += 1
                totals["target_selected"] += int(expectation_ok)
                totals["target_primary"] += int(bool(selected) and selected[0] == record.id)
            elif expected == "hardened-block":
                expectation_ok = record.id not in selected and target_decision["status"] == "denied"
                totals["block_cases"] += 1
                totals["blocked_correctly"] += int(expectation_ok)
            else:
                expectation_ok = record.id not in selected
                totals["consequential_cases"] += 1
                totals["consequential_correct"] += int(expectation_ok)

            case_ok = safety_ok and policy_ok and expectation_ok
            totals["passed"] += int(case_ok)
            totals["failed"] += int(not case_ok)
            totals["execution_advisory"] += int(route.get("execution_authorized") is False)
            totals["hardened_policy"] += int(
                (route.get("route_policy") or {}).get("contract_mode") == "hardened"
            )
            totals["no_invalid_selected"] += int(not invalid_selected)
            totals["policy_correct"] += int(policy_ok)
            totals["no_unresolved"] += int(not route.get("unselected_requested_stages"))

            if not case_ok:
                failures_by_skill[record.id] += 1
                if len(sample_failures) < 12:
                    sample_failures.append({
                        "case": case_id,
                        "target": record.id,
                        "ask_family": ask_id,
                        "expected": expected,
                        "target_status": entry.get("status"),
                        "target_policy": target_decision["status"],
                        "selected": selected,
                        "selection_status": route.get("selection_status"),
                        "identity_trace": (route.get("selection_trace") or {}).get("capability_identity"),
                    })

    elapsed = time.perf_counter() - started
    expected_processed = (TOTAL_REQUESTS - args.shard_index + args.shard_count - 1) // args.shard_count
    if processed != expected_processed:
        raise AssertionError((processed, expected_processed))

    summary = {
        "schema": "solkraft/cloud-validator-shard/v2",
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "processed": processed,
        "passed": totals["passed"],
        "failed": totals["failed"],
        "pass_rate": round(totals["passed"] / processed, 8),
        "ask_families": len(ASKS),
        "exact_words": EXACT_WORDS,
        "eligible_cases": totals["eligible_cases"],
        "target_selected": totals["target_selected"],
        "target_primary": totals["target_primary"],
        "block_cases": totals["block_cases"],
        "blocked_correctly": totals["blocked_correctly"],
        "consequential_cases": totals["consequential_cases"],
        "consequential_correct": totals["consequential_correct"],
        "execution_advisory": totals["execution_advisory"],
        "hardened_policy": totals["hardened_policy"],
        "no_invalid_selected": totals["no_invalid_selected"],
        "policy_correct": totals["policy_correct"],
        "no_unresolved": totals["no_unresolved"],
        "elapsed_seconds": round(elapsed, 3),
        "requests_per_second": round(processed / elapsed, 2),
        "failed_targets": dict(failures_by_skill.most_common()),
        "sample_failures": sample_failures,
    }
    print(json.dumps(summary, separators=(",", ":")))

    if totals["failed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
