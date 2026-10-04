"""Run 100,000 advanced, exactly-250-word contract-aware routing requests.

The benchmark is deterministic and balanced across every bundled skill. It does
not inject explicit skill IDs into route requests. Each skill receives at least
25 distinct ask families; with the current 173-skill bundle each skill receives
578 requests and six receive 579.

This is a routing/contract benchmark, not proof that an external agent executed
or completed the requested work.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import time

from solkraft.catalog import SkillCatalog
import solkraft.routing as routing_module
from solkraft.contract_policy import evaluate_contract, normalize_policy
from solkraft.contracts import contract_from_node
from solkraft.routing import BUNDLE_ROOT, catalog_graph, contract_index, route_request


TOTAL_REQUESTS = 100_000
MIN_ASK_FAMILIES = 25
EXACT_WORDS = 250
RESULT_PATH = Path(__file__).with_name("results-advanced-contract-100000.json")
WORD_RE = re.compile(r"\b[\w'-]+\b")

ASKS = (
    "Review a demanding real-world situation that needs this specialized capability: {description}. Determine the correct method, preserve the stated scope, and return an evidence-backed result for {subject}",
    "Inspect a difficult operational problem whose required capability is described as follows: {description}. Identify the right procedure, prerequisites, constraints, and observable completion evidence for {subject}",
    "Analyze a high-stakes request requiring this capability: {description}. Work through the relevant reasoning, dependencies, edge cases, and verification expectations for {subject}",
    "Research the best way to satisfy a complex request using the capability described here: {description}. Separate evidence from assumptions and produce a reproducible result for {subject}",
    "Compare viable approaches for a complex task that specifically requires this capability: {description}. Preserve tradeoffs, constraints, uncertainty, and acceptance evidence for {subject}",
    "Validate a difficult work request centered on this capability: {description}. Determine what must be true before completion can be claimed and identify the correct specialist procedure for {subject}",
    "Audit a complex scenario that requires the following capability: {description}. Examine risks, assumptions, dependencies, evidence quality, and completion conditions for {subject}",
    "Design a rigorous approach for a real request whose needed capability is: {description}. Make the method inspectable, preserve constraints, and define evidence for success for {subject}",
    "Build a defensible work plan for a difficult request that requires this capability: {description}. Preserve scope, interfaces, dependencies, validation, and handoff evidence for {subject}",
    "Create a complete specialist response for a challenging request requiring this capability: {description}. Keep assumptions explicit and make the result independently reviewable for {subject}",
    "Prepare a robust approach to a complex task that needs this capability: {description}. Identify inputs, outputs, failure modes, dependencies, and verification evidence for {subject}",
    "Investigate a difficult case where the necessary specialist capability is: {description}. Trace evidence, competing explanations, dependencies, and the conditions required to close the work for {subject}",
    "Diagnose a complex problem whose correct handling requires this capability: {description}. Find the appropriate specialist method, expose uncertainty, and define verification evidence for {subject}",
    "Test the proposed handling of a challenging request requiring this capability: {description}. Exercise assumptions, boundaries, failure cases, and observable acceptance criteria for {subject}",
    "Verify a complex result using the specialist capability described here: {description}. Check prerequisites, evidence, constraints, and any unresolved conditions before claiming completion for {subject}",
    "Draft an evidence-bound deliverable for a complex request that requires this capability: {description}. Preserve source lineage, limitations, acceptance criteria, and reviewer-ready structure for {subject}",
    "Write a precise specialist deliverable for a difficult request centered on this capability: {description}. Separate facts, assumptions, uncertainty, dependencies, and verifiable outcomes for {subject}",
    "Plan the full handling of a challenging request requiring this capability: {description}. Sequence dependencies, identify gates, retain evidence, and define completion conditions for {subject}",
    "Evaluate a complex scenario that requires this capability: {description}. Judge alternatives, evidence strength, risks, dependencies, and the correct specialist result for {subject}",
    "Summarize and resolve a difficult request whose needed capability is: {description}. Preserve the important distinctions, evidence, constraints, open questions, and acceptance conditions for {subject}",
    "Explain and apply the specialist capability described here to a demanding real-world request: {description}. Keep the explanation operational, evidence-based, bounded, and verifiable for {subject}",
    "Check a complex task that depends on this capability: {description}. Identify hidden assumptions, edge cases, dependencies, evidence gaps, and the correct completion signal for {subject}",
    "Formulate a rigorous specialist approach for a difficult request requiring this capability: {description}. Define inputs, outputs, constraints, uncertainty, verification, and review evidence for {subject}",
    "Solve a challenging practical problem using the capability described here: {description}. Preserve traceability, distinguish assumptions from evidence, and make the result testable for {subject}",
    "Outline a complete specialist workflow for a complex request requiring this capability: {description}. Include prerequisites, dependencies, validation, risk boundaries, and evidence needed for independent review for {subject}",
)

SUBJECTS = (
    "a regulated service change",
    "a multi-team engineering program",
    "a customer-facing product decision",
    "an evidence-sensitive research effort",
    "a production readiness review",
    "a cross-platform implementation",
    "a high-impact operational change",
    "a constrained technical investigation",
    "a reviewable decision package",
    "a complex integration handoff",
    "a reliability-sensitive workflow",
    "a long-lived maintenance decision",
    "a reproducible analysis package",
    "a safety-conscious design review",
    "a dependency-heavy delivery plan",
    "a provenance-sensitive audit",
)

CONTEXT_WORDS = (
    "preserve traceability source identities assumptions baselines constraints alternatives measurements "
    "risk hypotheses acceptance criteria limitations data lineage review observations configuration snapshots "
    "ownership timelines dependencies uncertainty bounds evidence provenance interfaces scope privacy accessibility "
    "maintenance fallback behavior operational context input coverage baseline comparisons review cadence change control "
    "reproducibility escalation verification benefits residual risks deadlines accountable roles version lineage rationale "
    "exception handling approval status resource limits observable outcomes recovery conditions system boundaries validation "
    "delivery constraints lessons incident response monitoring criteria independent review exact inputs expected outputs "
    "tradeoffs failure modes counterevidence confidence calibration retained artifacts test receipts decision logs rollback "
    "conditions stakeholder objectives compatibility portability integrity confidentiality availability human review "
    "handoff requirements auditability deterministic behavior bounded retries structured evidence conservative interpretation "
    "machine readable contracts typed dataflow capability requirements resource scopes trust provenance verification receipts"
).split()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def exactly_250(active: str, *, case_id: int, skill_ordinal: int, variant: int) -> str:
    active_words = words(active)
    prefix = " ".join(active_words) + ". Context notes:"
    prefix_count = len(active_words) + 2
    if prefix_count >= EXACT_WORDS:
        active_words = active_words[: EXACT_WORDS - 12]
        prefix = " ".join(active_words) + ". Context notes:"
        prefix_count = len(active_words) + 2

    needed = EXACT_WORDS - prefix_count
    context = []
    marker = [
        f"case{case_id:06d}",
        f"skillordinal{skill_ordinal:03d}",
        f"variant{variant:02d}",
        "advanced",
        "benchmark",
    ]
    context.extend(marker)
    cursor = (case_id * 17 + skill_ordinal * 31 + variant * 13) % len(CONTEXT_WORDS)
    while len(context) < needed:
        context.append(CONTEXT_WORDS[cursor % len(CONTEXT_WORDS)])
        cursor += 1
    context = context[:needed]
    prompt = prefix + " " + " ".join(context)
    assert len(words(prompt)) == EXACT_WORDS
    return prompt


def expectation(entry: dict, node: dict) -> str:
    if node.get("effect") is True:
        return "consequential-not-selected"
    if entry.get("status") in {"opaque", "invalid", "unsupported"}:
        return "hardened-block"
    return "select-target"


def main() -> None:
    started = time.perf_counter()
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    if not records:
        raise SystemExit("No bundled skills discovered.")

    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    entries = {entry["id"]: entry for entry in index.entries()}

    # Freeze immutable routing metadata for this benchmark corpus. route_request
    # still executes the production routing/policy/dataflow/validation path for
    # every request; this only removes repeated filesystem/index refresh work.
    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index
    if set(entries) != {record.id for record in records}:
        raise AssertionError("Contract index/catalog membership mismatch.")

    skill_count = len(records)
    base = TOTAL_REQUESTS // skill_count
    remainder = TOTAL_REQUESTS % skill_count
    if base < MIN_ASK_FAMILIES:
        raise AssertionError("Request count cannot satisfy per-skill ask-family minimum.")

    seen_hashes: set[str] = set()
    aggregate_digest = hashlib.sha256()
    per_skill = {}
    global_failures = []
    examples = []
    totals = Counter()

    global_case = 0
    for skill_ordinal, record in enumerate(records):
        entry = entries[record.id]
        node = graph["nodes"][record.id]
        expected = expectation(entry, node)
        case_count = base + (1 if skill_ordinal < remainder else 0)
        ask_families = set()
        metrics = Counter()
        failures = []

        description_words = words(record.description)
        description = " ".join(description_words[:48])
        if not description:
            description = "perform the specialized procedure described by this bundled skill"

        for local_case in range(case_count):
            ask_id = local_case % len(ASKS)
            ask_families.add(ask_id)
            subject = SUBJECTS[(local_case + skill_ordinal * 7) % len(SUBJECTS)]
            active = ASKS[ask_id].format(description=description, subject=subject)
            prompt = exactly_250(
                active,
                case_id=global_case,
                skill_ordinal=skill_ordinal,
                variant=ask_id,
            )
            prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            if prompt_hash in seen_hashes:
                raise AssertionError(f"duplicate request hash at case {global_case}")
            seen_hashes.add(prompt_hash)
            aggregate_digest.update(prompt.encode("utf-8"))
            aggregate_digest.update(b"\0")

            policy = {"contract_mode": "hardened"}
            route = route_request(
                catalog,
                prompt,
                max_skills=50,
                policy=policy,
            )
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

            metrics["cases"] += 1
            metrics["exact_250_words"] += int(len(words(prompt)) == EXACT_WORDS)
            metrics["execution_advisory"] += int(route.get("execution_authorized") is False)
            metrics["hardened_policy"] += int(
                (route.get("route_policy") or {}).get("contract_mode") == "hardened"
            )
            metrics["no_invalid_selected_contract"] += int(not invalid_selected)
            metrics["target_selected"] += int(record.id in selected)
            metrics["target_primary"] += int(bool(selected) and selected[0] == record.id)
            metrics["no_unresolved"] += int(not route.get("unselected_requested_stages"))

            policy_expected = (
                target_decision["status"] == "denied"
                if entry.get("status") in {"opaque", "invalid", "unsupported"}
                else target_decision["status"] != "denied"
            )
            metrics["target_policy_correct"] += int(policy_expected)

            if expected == "select-target":
                expectation_ok = record.id in selected
                metrics["select_target_cases"] += 1
                metrics["select_target_passed"] += int(expectation_ok)
            elif expected == "hardened-block":
                expectation_ok = record.id not in selected and target_decision["status"] == "denied"
                metrics["hardened_block_cases"] += 1
                metrics["hardened_block_passed"] += int(expectation_ok)
            else:
                expectation_ok = record.id not in selected
                metrics["consequential_cases"] += 1
                metrics["consequential_passed"] += int(expectation_ok)

            case_ok = all((
                len(words(prompt)) == EXACT_WORDS,
                route.get("execution_authorized") is False,
                (route.get("route_policy") or {}).get("contract_mode") == "hardened",
                not invalid_selected,
                policy_expected,
                expectation_ok,
            ))
            metrics["passed"] += int(case_ok)
            if not case_ok:
                failure = {
                    "case": global_case,
                    "ask_family": ask_id,
                    "target": record.id,
                    "expected": expected,
                    "target_status": entry.get("status"),
                    "target_trust": (entry.get("trust") or {}).get("state"),
                    "target_policy": target_decision["status"],
                    "selected": selected,
                    "selection_status": route.get("selection_status"),
                    "unresolved": route.get("unselected_requested_stages"),
                    "invalid_selected": invalid_selected,
                    "prompt_sha256": prompt_hash,
                }
                if len(failures) < 3:
                    failures.append(failure)
                if len(global_failures) < 100:
                    global_failures.append(failure)

            if len(examples) < 8 and local_case == 0:
                examples.append({
                    "target": record.id,
                    "expected": expected,
                    "prompt": prompt,
                    "prompt_sha256": prompt_hash,
                    "selected": selected,
                    "selection_status": route.get("selection_status"),
                })

            global_case += 1

        if len(ask_families) < MIN_ASK_FAMILIES:
            raise AssertionError(f"{record.id}: only {len(ask_families)} ask families")

        per_skill[record.id] = {
            "description": record.description,
            "contract_status": entry.get("status"),
            "trust_state": (entry.get("trust") or {}).get("state"),
            "legacy_effect": node.get("effect"),
            "expectation": expected,
            "ask_families": len(ask_families),
            **dict(metrics),
            "failures": failures,
        }
        totals.update(metrics)

    if global_case != TOTAL_REQUESTS:
        raise AssertionError(f"generated {global_case}, expected {TOTAL_REQUESTS}")
    if len(seen_hashes) != TOTAL_REQUESTS:
        raise AssertionError("global request uniqueness failed")

    elapsed = time.perf_counter() - started
    select_cases = totals["select_target_cases"]
    blocked_cases = totals["hardened_block_cases"]
    consequential_cases = totals["consequential_cases"]

    result = {
        "schema": "solkraft/advanced-contract-benchmark/v1",
        "system": "contract-aware hardened public routing",
        "total_requests": TOTAL_REQUESTS,
        "passed": totals["passed"],
        "failed": TOTAL_REQUESTS - totals["passed"],
        "pass_rate": round(totals["passed"] / TOTAL_REQUESTS, 6),
        "exact_words": EXACT_WORDS,
        "exact_250_word_requests": totals["exact_250_words"],
        "globally_unique_requests": len(seen_hashes),
        "request_corpus_sha256": aggregate_digest.hexdigest(),
        "explicit_skill_ids_injected": False,
        "skill_count": skill_count,
        "requests_per_skill_min": min(item["cases"] for item in per_skill.values()),
        "requests_per_skill_max": max(item["cases"] for item in per_skill.values()),
        "ask_families_required_per_skill": MIN_ASK_FAMILIES,
        "ask_families_min_observed": min(item["ask_families"] for item in per_skill.values()),
        "automatic_selection": {
            "eligible_cases": select_cases,
            "target_selected": totals["select_target_passed"],
            "recall": round(totals["select_target_passed"] / select_cases, 6) if select_cases else None,
            "target_primary": totals["target_primary"],
            "primary_rate": round(totals["target_primary"] / select_cases, 6) if select_cases else None,
        },
        "hardened_blocking": {
            "opaque_invalid_unsupported_cases": blocked_cases,
            "correctly_blocked": totals["hardened_block_passed"],
            "correct_block_rate": round(totals["hardened_block_passed"] / blocked_cases, 6) if blocked_cases else None,
        },
        "consequential_boundary": {
            "cases": consequential_cases,
            "correctly_not_selected": totals["consequential_passed"],
            "correct_rate": round(totals["consequential_passed"] / consequential_cases, 6) if consequential_cases else None,
        },
        "contract_integrity": {
            "execution_authorized_false": totals["execution_advisory"],
            "hardened_policy_present": totals["hardened_policy"],
            "no_invalid_or_opaque_selected_contracts": totals["no_invalid_selected_contract"],
            "target_policy_correct": totals["target_policy_correct"],
        },
        "route_quality": {
            "no_unresolved_requested_stages": totals["no_unresolved"],
            "no_unresolved_rate": round(totals["no_unresolved"] / TOTAL_REQUESTS, 6),
        },
        "elapsed_seconds": round(elapsed, 3),
        "requests_per_second": round(TOTAL_REQUESTS / elapsed, 2) if elapsed else None,
        "immutable_metadata_cached": True,
        "contract_status_counts": dict(Counter(item["contract_status"] for item in per_skill.values())),
        "trust_state_counts": dict(Counter(item["trust_state"] for item in per_skill.values())),
        "expectation_counts": dict(Counter(item["expectation"] for item in per_skill.values())),
        "failures": global_failures,
        "examples": examples,
        "per_skill": per_skill,
        "notes": [
            "Requests are deterministically generated, exactly 250 words, and globally unique.",
            "No explicit skill IDs are passed to route_request.",
            "Automatic-selection recall is scored only for non-consequential skills with usable declared/legacy contract state.",
            "Opaque/invalid/unsupported skills are scored on correct hardened blocking rather than target selection.",
            "Legacy graph nodes marked effect:true are scored on remaining unselected; SolKraft does not authorize execution.",
            "This benchmark evaluates routing and contract-policy behavior, not external execution quality.",
        ],
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        key: value
        for key, value in result.items()
        if key not in {"per_skill", "failures", "examples"}
    }, indent=2))

    # Fail the benchmark job if a core contract/safety invariant is violated.
    safety_ok = all((
        totals["exact_250_words"] == TOTAL_REQUESTS,
        len(seen_hashes) == TOTAL_REQUESTS,
        totals["execution_advisory"] == TOTAL_REQUESTS,
        totals["hardened_policy"] == TOTAL_REQUESTS,
        totals["no_invalid_selected_contract"] == TOTAL_REQUESTS,
        totals["target_policy_correct"] == TOTAL_REQUESTS,
    ))
    if not safety_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
