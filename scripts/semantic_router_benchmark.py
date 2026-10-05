"""Semantic routing proof benchmark.

This suite is intentionally different from the legacy 100k contract benchmark.

It measures three things:
1. 1,000 distinct single-skill natural-language prompts per catalog skill.
2. 100,000 distinct multi-skill composition prompts spanning 2-5 skills.
3. 100,000 repeat executions over 10,000 difficult prompts (10 repeats each)
   to prove deterministic stability and absence of cross-request contamination.

The corpus never injects a skill id or copies a full published description.
It is deterministic so failures are reproducible and sharded so CI can scale.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import time

from solkraft.catalog import SkillCatalog
import solkraft.routing as routing_module
from solkraft.routing import BUNDLE_ROOT, catalog_graph, contract_index, route_request

SINGLE_PROMPTS_PER_SKILL = 1_000
DEV_PROMPTS_PER_SKILL = 800
HOLDOUT_PROMPTS_PER_SKILL = 200
COMPOSITION_CASES = 100_000
STABILITY_BASE_CASES = 10_000
STABILITY_REPEATS = 10

WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?", re.I)
RESULT_TEMPLATE = "results-semantic-router-proof-shard-{shard:02d}-of-{count:02d}.json"

STOPWORDS = frozenset("""
a an and are as at be been being by can could did do does for from had has have
how i if in into is it its may might more most must my no not of on or our should
so than that the their them then there these they this those to under up use using
was we were what when where which while who why will with would you your
ability about after again against all also any because before between both but
during each few further here hers herself himself itself just me myself once only
other ours ourselves out over own same she some such themselves through too very
capability capabilities skill skills procedure procedures method methods request
requests task tasks work working result results evidence specialist specialized
complex difficult real world correct appropriate relevant published bundled
""".split())

ACTION_OPENERS = (
    "Help me figure out",
    "I need to troubleshoot",
    "Can you work out",
    "Please investigate",
    "I am trying to resolve",
    "Walk me through",
    "I need a practical way to handle",
    "Can you diagnose",
    "Show me how to approach",
    "I need to verify",
)

CONTEXTS = (
    "before a production handoff",
    "inside an existing engineering project",
    "for a review that has to survive scrutiny",
    "while several teams are changing adjacent pieces",
    "with incomplete inputs and a tight deadline",
    "after an earlier attempt produced conflicting evidence",
    "without changing unrelated parts of the system",
    "for a maintainer who did not build the original implementation",
    "while preserving rollback and auditability",
    "with a requirement that the outcome be independently checkable",
)

DELIVERABLES = (
    "Give me the concrete next actions and the evidence that would prove they worked.",
    "Keep the answer operational and tell me what a reviewer should verify.",
    "I care about the actual deliverable, not a broad overview.",
    "Call out the assumptions that could change the recommended path.",
    "Make the completion criteria explicit and observable.",
    "Separate what is known from what still needs to be checked.",
    "Show the important failure cases and how the result should be validated.",
    "Preserve the constraints instead of silently relaxing them.",
    "Give me a reproducible path another person can follow.",
    "Include the checks that distinguish a real pass from a plausible-looking answer.",
)

TONE_PREFIXES = (
    "",
    "Quick question: ",
    "I am stuck on something. ",
    "For context, this is a live project. ",
    "Treat this like a maintainer request. ",
    "I need a second pair of eyes here. ",
    "Assume I know the domain basics. ",
    "Explain this like an implementation handoff. ",
    "This is not theoretical. ",
    "I want the shortest defensible path. ",
)

CONNECTORS = (
    "Then",
    "After that",
    "In the same request",
    "Also",
    "Next",
    "As a separate stage",
    "Once that is clear",
    "Without losing that context",
)

DOMAIN_FALLBACKS = ("engineering", "software", "research", "analysis", "operations")


def tokens(text: str) -> list[str]:
    return [token.casefold() for token in WORD_RE.findall(text or "")]


def normalized(text: str) -> str:
    return " ".join(tokens(text))


def expectation(entry: dict, node: dict) -> str:
    if node.get("effect") is True:
        return "consequential-not-selected"
    if entry.get("status") in {"opaque", "invalid", "unsupported"}:
        return "hardened-block"
    return "select-target"


def build_profiles(records, graph):
    token_sets: dict[str, set[str]] = {}
    raw_tokens: dict[str, list[str]] = {}
    for record in records:
        node = graph["nodes"][record.id]
        source = " ".join((
            record.description,
            str(node.get("domain") or ""),
            " ".join(map(str, node.get("inputs") or [])),
            " ".join(map(str, node.get("outputs") or [])),
        ))
        values = [
            token for token in tokens(source)
            if len(token) >= 3 and token not in STOPWORDS and not token.isdigit()
        ]
        raw_tokens[record.id] = values
        token_sets[record.id] = set(values)

    df = Counter()
    for values in token_sets.values():
        df.update(values)
    total = max(len(records), 1)

    profiles = {}
    for record in records:
        skill_id = record.id
        node = graph["nodes"][skill_id]
        unique = sorted(
            token_sets[skill_id],
            key=lambda token: (-(math.log((total + 1) / (df[token] + 1)) + 1), token),
        )
        if len(unique) < 8:
            for token in tokens(record.name):
                if token not in STOPWORDS and token not in unique:
                    unique.append(token)
        if len(unique) < 4:
            for token in raw_tokens[skill_id]:
                if token not in unique:
                    unique.append(token)
        if not unique:
            unique = ["domain", "workflow", "verification", "output"]

        profiles[skill_id] = {
            "anchors": unique[:18],
            "domain": " ".join(tokens(str(node.get("domain") or "general"))) or "general",
            "description_norm": normalized(record.description),
            "id_norm": normalized(record.id),
        }

    ids = [record.id for record in records]
    for skill_id in ids:
        own = token_sets[skill_id]
        scored = []
        for other in ids:
            if other == skill_id:
                continue
            theirs = token_sets[other]
            union = own | theirs
            score = len(own & theirs) / len(union) if union else 0.0
            scored.append((score, other))
        scored.sort(key=lambda row: (-row[0], row[1].casefold()))
        profiles[skill_id]["nearest"] = [other for _, other in scored[:5]]
    return profiles


def anchor_phrase(profile: dict, case_index: int, width: int = 4) -> str:
    anchors = profile["anchors"]
    picked = []
    cursor = (case_index * 7 + 3) % len(anchors)
    for offset in range(width * 4):
        token = anchors[(cursor + offset * 5) % len(anchors)]
        if token not in picked:
            picked.append(token)
        if len(picked) == width:
            break
    return ", ".join(picked)


def leakage_violations(prompt: str, skill_id: str, description: str) -> list[str]:
    issues = []
    prompt_norm = normalized(prompt)
    desc_norm = normalized(description)
    literal_id = skill_id.casefold()
    if any(sep in literal_id for sep in "-_:./") and literal_id in prompt.casefold():
        issues.append("skill_id")
    if desc_norm and len(desc_norm.split()) >= 5 and desc_norm in prompt_norm:
        issues.append("full_description")
    desc_words = desc_norm.split()
    if len(desc_words) >= 8:
        for idx in range(len(desc_words) - 7):
            if " ".join(desc_words[idx:idx + 8]) in prompt_norm:
                issues.append("description_8gram")
                break
    return issues


def single_prompt(record, profile: dict, profiles: dict, case_index: int) -> str:
    opener_index = case_index % 10
    context_index = (case_index // 10) % 10
    deliverable_index = (case_index // 100) % 10
    tone_index = (case_index * 7 + case_index // 13) % 10
    anchors = anchor_phrase(profile, case_index, 4)
    domain = profile["domain"] if profile["domain"] != "general" else DOMAIN_FALLBACKS[case_index % len(DOMAIN_FALLBACKS)]
    prompt = (
        f"{TONE_PREFIXES[tone_index]}{ACTION_OPENERS[opener_index]} a {domain} problem "
        f"centered on {anchors} {CONTEXTS[context_index]}. {DELIVERABLES[deliverable_index]}"
    )
    if case_index % 5 == 0 and profile["nearest"]:
        neighbor = profiles[profile["nearest"][case_index % len(profile["nearest"])]]
        distractor = anchor_phrase(neighbor, case_index + 19, 2)
        prompt += (
            f" There is adjacent context involving {distractor}, but do not let that replace "
            f"the primary need around {anchors}."
        )
    elif case_index % 7 == 0 and profile["nearest"]:
        neighbor = profiles[profile["nearest"][(case_index // 7) % len(profile["nearest"])]]
        distractor = anchor_phrase(neighbor, case_index + 31, 2)
        prompt += (
            f" Someone suggested treating this mainly as {distractor}; check that interpretation "
            f"rather than assuming it is the right route."
        )
    return prompt


def composition_prompt(records_by_id, profiles, target_ids: list[str], case_index: int) -> str:
    clauses = []
    for position, skill_id in enumerate(target_ids):
        profile = profiles[skill_id]
        anchors = anchor_phrase(profile, case_index * 11 + position * 37, 3)
        domain = profile["domain"] if profile["domain"] != "general" else DOMAIN_FALLBACKS[(case_index + position) % len(DOMAIN_FALLBACKS)]
        opener = ACTION_OPENERS[(case_index + position * 3) % len(ACTION_OPENERS)]
        context = CONTEXTS[(case_index // 7 + position * 2) % len(CONTEXTS)]
        clause = f"{opener} the {domain} part involving {anchors} {context}."
        if position:
            connector = CONNECTORS[(case_index + position) % len(CONNECTORS)]
            clause = f"{connector}, {clause[0].lower()}{clause[1:]}"
        clauses.append(clause)
    return " ".join(clauses) + " " + DELIVERABLES[(case_index * 3) % len(DELIVERABLES)]


def route_fingerprint(route: dict) -> str:
    payload = {
        "selected": route.get("selected") or [],
        "stages": [
            {"stage": row.get("stage"), "selected": row.get("selected") or [], "reason": row.get("reason")}
            for row in (route.get("stages") or [])
        ],
        "unselected": route.get("unselected_requested_stages") or [],
        "blocked": route.get("blocked_stages") or [],
        "execution_authorized": route.get("execution_authorized"),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def ordered_subsequence(expected: list[str], actual: list[str]) -> bool:
    cursor = 0
    for item in actual:
        if cursor < len(expected) and item == expected[cursor]:
            cursor += 1
    return cursor == len(expected)


def selectable_ids(records, graph, entries) -> list[str]:
    return [record.id for record in records if expectation(entries[record.id], graph["nodes"][record.id]) == "select-target"]


def composition_targets(selectable: list[str], case_index: int) -> list[str]:
    size = 2 + (case_index % 4)
    n = len(selectable)
    if n < size:
        raise AssertionError("not enough selectable skills for composition benchmark")
    start = (case_index * 17 + case_index // 11) % n
    strides = (7, 11, 13, 17, 19)
    result = []
    for offset in range(size):
        candidate = selectable[(start + offset * strides[offset]) % n]
        bump = 1
        while candidate in result:
            candidate = selectable[(start + offset * strides[offset] + bump * 23) % n]
            bump += 1
        result.append(candidate)
    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--single-per-skill", type=int, default=SINGLE_PROMPTS_PER_SKILL)
    parser.add_argument("--composition-cases", type=int, default=COMPOSITION_CASES)
    parser.add_argument("--stability-base-cases", type=int, default=STABILITY_BASE_CASES)
    parser.add_argument("--stability-repeats", type=int, default=STABILITY_REPEATS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        parser.error("invalid shard configuration")
    if not 1 <= args.single_per_skill <= SINGLE_PROMPTS_PER_SKILL:
        parser.error(f"--single-per-skill must be 1..{SINGLE_PROMPTS_PER_SKILL}")
    if args.composition_cases < 0 or args.stability_base_cases < 0 or args.stability_repeats < 1:
        parser.error("case counts must be non-negative and repeats >= 1")
    return args


def main():
    args = parse_args()
    started = time.perf_counter()
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    if not records:
        raise SystemExit("No bundled skills discovered.")
    records_by_id = {record.id: record for record in records}
    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    entries = {entry["id"]: entry for entry in index.entries()}
    profiles = build_profiles(records, graph)
    selectable = selectable_ids(records, graph, entries)

    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index

    digest = hashlib.sha256()
    prompt_hashes = set()
    leakage = Counter()
    single = Counter()
    composition = Counter()
    stability = Counter()
    per_skill = defaultdict(Counter)
    confusion = defaultdict(Counter)
    failures = []
    policy = {"contract_mode": "hardened"}

    def remember_prompt(prompt: str, targets: list[str]) -> None:
        value = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        prompt_hashes.add(value)
        digest.update(value.encode("ascii"))
        for target in targets:
            if value in seen_by_target[target]:
                raise AssertionError(f"duplicate prompt generated for target {target}")
            seen_by_target[target].add(value)
            issues = leakage_violations(prompt, target, records_by_id[target].description)
            for issue in issues:
                leakage[issue] += 1
            if issues:
                raise AssertionError(f"benchmark prompt leaked metadata for {target}: {issues}")

    global_case = 0
    for record in records:
        profile = profiles[record.id]
        expected = expectation(entries[record.id], graph["nodes"][record.id])
        for local_case in range(args.single_per_skill):
            case_id = global_case
            global_case += 1
            if case_id % args.shard_count != args.shard_index:
                continue
            prompt = single_prompt(record, profile, profiles, local_case)
            remember_prompt(prompt, [record.id])
            split = "holdout" if local_case >= DEV_PROMPTS_PER_SKILL else "dev"
            route = route_request(catalog, prompt, max_skills=50, policy=policy)
            selected = route.get("selected") or []
            top = selected[0] if selected else None
            if expected == "select-target":
                ok = record.id in selected
                single["eligible_cases"] += 1
                single["eligible_passed"] += int(ok)
                single[f"{split}_eligible_cases"] += 1
                single[f"{split}_eligible_passed"] += int(ok)
                per_skill[record.id]["top1"] += int(top == record.id)
                if not ok and top:
                    confusion[record.id][top] += 1
            else:
                ok = record.id not in selected
                single["boundary_cases"] += 1
                single["boundary_passed"] += int(ok)
                single[f"{split}_boundary_cases"] += 1
                single[f"{split}_boundary_passed"] += int(ok)
            per_skill[record.id][f"{split}_cases"] += 1
            per_skill[record.id][f"{split}_passed"] += int(ok)
            per_skill[record.id]["cases"] += 1
            per_skill[record.id]["passed"] += int(ok)
            single["cases"] += 1
            single["passed"] += int(ok)
            if not ok and len(failures) < 30:
                failures.append({"suite":"single","case":case_id,"target":record.id,"split":split,"expected":expected,"selected":selected[:8],"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest()})

    for case_id in range(args.composition_cases):
        if case_id % args.shard_count != args.shard_index:
            continue
        targets = composition_targets(selectable, case_id)
        prompt = composition_prompt(records_by_id, profiles, targets, case_id)
        remember_prompt(prompt, targets)
        route = route_request(catalog, prompt, max_skills=50, policy=policy)
        selected = route.get("selected") or []
        selected_set = set(selected)
        target_set = set(targets)
        coverage_ok = target_set.issubset(selected_set)
        exact_ok = selected_set == target_set
        order_ok = ordered_subsequence(targets, selected)
        unresolved_ok = not route.get("unselected_requested_stages")
        composition["cases"] += 1
        composition["all_targets_selected"] += int(coverage_ok)
        composition["exact_target_set"] += int(exact_ok)
        composition["target_order_preserved"] += int(order_ok)
        composition["no_unresolved"] += int(unresolved_ok)
        composition["extra_selected_total"] += max(0, len(selected_set - target_set))
        composition[f"size_{len(targets)}_cases"] += 1
        composition[f"size_{len(targets)}_coverage"] += int(coverage_ok)
        if (not coverage_ok or not order_ok) and len(failures) < 30:
            failures.append({"suite":"composition","case":case_id,"targets":targets,"selected":selected[:12],"coverage_ok":coverage_ok,"order_ok":order_ok,"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest()})

    for base_case in range(args.stability_base_cases):
        if base_case % args.shard_count != args.shard_index:
            continue
        if base_case % 2 == 0:
            record = records[(base_case * 29 + 7) % len(records)]
            local_case = 800 + ((base_case * 37) % HOLDOUT_PROMPTS_PER_SKILL)
            prompt = single_prompt(record, profiles[record.id], profiles, local_case)
            targets = [record.id]
        else:
            targets = composition_targets(selectable, base_case * 97)
            prompt = composition_prompt(records_by_id, profiles, targets, base_case * 97)
        base_hash = hashlib.sha256(prompt.encode()).hexdigest()
        digest.update(("stability:" + base_hash).encode("ascii"))
        for target in targets:
            issues = leakage_violations(prompt, target, records_by_id[target].description)
            for issue in issues:
                leakage[issue] += 1
            if issues:
                raise AssertionError(f"stability prompt leaked metadata for {target}: {issues}")
        fingerprints = []
        for _ in range(args.stability_repeats):
            fingerprints.append(route_fingerprint(route_request(catalog, prompt, max_skills=50, policy=policy)))
        baseline = fingerprints[0]
        mismatches = sum(1 for item in fingerprints[1:] if item != baseline)
        stability["base_cases"] += 1
        stability["executions"] += args.stability_repeats
        stability["mismatches"] += mismatches
        stability["stable_base_cases"] += int(mismatches == 0)
        if mismatches and len(failures) < 30:
            failures.append({"suite":"stability","base_case":base_case,"targets":targets,"mismatches":mismatches,"prompt_sha256":base_hash})

    elapsed = time.perf_counter() - started
    per_skill_result = {}
    for skill_id in sorted(per_skill, key=str.casefold):
        metrics = per_skill[skill_id]
        result = dict(metrics)
        if metrics["cases"]:
            result["rate"] = round(metrics["passed"] / metrics["cases"], 8)
        if metrics["dev_cases"]:
            result["dev_rate"] = round(metrics["dev_passed"] / metrics["dev_cases"], 8)
        if metrics["holdout_cases"]:
            result["holdout_rate"] = round(metrics["holdout_passed"] / metrics["holdout_cases"], 8)
        if metrics["cases"]:
            result["top1_rate"] = round(metrics["top1"] / metrics["cases"], 8)
        per_skill_result[skill_id] = result

    summary = {
        "schema":"solkraft/semantic-router-proof-shard/v1",
        "shard_index":args.shard_index,
        "shard_count":args.shard_count,
        "catalog":{"skill_count":len(records),"selectable_skill_count":len(selectable)},
        "corpus":{
            "single_prompts_per_skill_configured":args.single_per_skill,
            "development_partition_boundary":min(DEV_PROMPTS_PER_SKILL,args.single_per_skill),
            "holdout_partition_start":DEV_PROMPTS_PER_SKILL,
            "composition_cases_configured":args.composition_cases,
            "stability_base_cases_configured":args.stability_base_cases,
            "stability_repeats":args.stability_repeats,
            "explicit_skill_ids_injected":False,
            "full_descriptions_injected":False,
            "prompt_hashes_in_shard":len(prompt_hashes),
            "shard_corpus_sha256":digest.hexdigest(),
        },
        "leakage":dict(leakage),
        "single":dict(single),
        "composition":dict(composition),
        "stability":dict(stability),
        "per_skill":per_skill_result,
        "confusion":{skill_id:dict(rows.most_common(8)) for skill_id,rows in confusion.items()},
        "sample_failures":failures,
        "performance":{
            "elapsed_seconds":round(elapsed,3),
            "routes_per_second_approx":round((single["cases"]+composition["cases"]+stability["executions"])/elapsed,2) if elapsed else None,
        },
    }
    output = args.output or Path(__file__).with_name(RESULT_TEMPLATE.format(shard=args.shard_index,count=args.shard_count))
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"output":str(output),"single_cases":single["cases"],"composition_cases":composition["cases"],"stability_executions":stability["executions"],"leakage":dict(leakage)},separators=(",",":")))


if __name__ == "__main__":
    main()
