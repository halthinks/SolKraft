"""Compose an ordered, advisory route for compound native-skill requests.

This module is intentionally additive to ``select_workflow.route``.  It turns
long requests into action-bearing clauses, selects one primary skill per
requested clause, preserves exclusions, and returns no more than fifty skills.
It executes nothing and grants no authority. The selected route is capped at
fifty skills to keep compound requests bounded and inspectable.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re

from solkraft.constraint_parser import (
    effect_exclusion_start as _effect_exclusion_start,
    excluded_effects as _excluded_effects,
    hide_quotes as _hide_quotes,
)


_ROOT = Path(__file__).resolve().parent.parent
_SELECTOR_SPEC = importlib.util.spec_from_file_location(
    "solforge_selector", _ROOT / "scripts" / "select_workflow.py"
)
selector = importlib.util.module_from_spec(_SELECTOR_SPEC)
assert _SELECTOR_SPEC.loader is not None
_SELECTOR_SPEC.loader.exec_module(selector)

_ACTION = r"research|compare|draft|write|compose|create|prepare|inspect|review|diagnose|investigate|debug|implement|fix|build|refactor|run|test|verify|validate|generate|audit|analyze|summarize|derive|design|perform|conduct|reproduce|replicate|hand\s+off|train|tune|optimize|model|evaluate|plan|formulate|solve|prove|compute|explain|check|package|install|release|visualize|factcheck|outline|find|assess"
def _is_constraint_context(clause):
    """Keep delivery constraints and candidate identifiers out of the route."""
    return bool(re.match(
        r"(?:context notes\b|keep\b|preserve\b|retain\b|identify unresolved\b|state unresolved\b|record\b|distinguish findings\b|avoid unrelated\b|use the requested acceptance\b|candidate revision\b|use candidate revision\b)",
        clause,
    ))


def segment(objective):
    """Return requested, ordered clauses while retaining quoted content as inert."""
    visible, quoted = _hide_quotes(objective)
    text = selector.normalize(visible)
    context_ignored = []
    context_start = re.search(r"\bcontext notes\s*:", text)
    if context_start:
        tail = text[context_start.start():]
        exclusion_start = _effect_exclusion_start(tail)
        if exclusion_start is not None:
            context_ignored.append({"text": tail[:exclusion_start].strip(" ,:"), "reason": "context notes"})
            text = text[:context_start.start()] + " " + tail[exclusion_start:]
        else:
            context_ignored.append({"text": tail.strip(" ,:"), "reason": "context notes"})
            text = text[:context_start.start()]
    # Preserve object lists joined by ``and``; split only where a new action starts.
    boundary = (
        rf"[;\n]+|[.!?](?:\s+(?:next,?\s*)?|$)|\b(?:then|after that|finally|otherwise)\b|"
        rf"\band\s+(?=(?:{_ACTION})\b)"
    )
    raw = [part.strip(" ,:") for part in re.split(boundary, text) if part.strip(" ,:")]
    # ``write and run focused tests`` is one verification request. The first
    # action can otherwise be stranded after action-aware splitting.
    coalesced = []
    index = 0
    while index < len(raw):
        current = raw[index]
        following = raw[index + 1] if index + 1 < len(raw) else ""
        if re.fullmatch(rf"(?:{_ACTION})", current) and re.match(rf"(?:{_ACTION})\b", following):
            coalesced.append(current + " and " + following)
            index += 2
            continue
        if (
            current in {"write", "draft"}
            and re.match(r"run\b", following)
            and re.search(r"\b(?:focused|regression|tests?)\b", following)
        ):
            coalesced.append(current + " and " + following)
            index += 2
            continue
        coalesced.append(current)
        index += 1
    raw = coalesced
    clauses = []
    ignored = context_ignored + [{"text": item, "reason": "quoted content"} for item in quoted]
    for clause in raw:
        if re.search(r"\b(?:tomorrow|next week|next month|later|after approval)\b", clause) and not re.search(r"\b(?:now|today)\b", clause):
            ignored.append({"text": clause, "reason": "deferred work"})
            continue
        # Exclusion clauses never become requested work. Keep any preceding request.
        neg = re.search(r"\b(?:do not|don't|dont|without|never|skip|avoid)\b", clause)
        if neg:
            ignored.append({"text": clause[neg.start():], "reason": "excluded scope"})
            clause = clause[:neg.start()].strip(" ,:")
        if clause and _is_constraint_context(clause):
            ignored.append({"text": clause, "reason": "constraint or context"})
            continue
        if clause:
            clauses.append(clause)
    return clauses, ignored


def _mapped_skill(clause):
    """Return the specialized skill and explanation for a structured clause."""
    c = clause.casefold()
    if re.search(r"\b(?:inspect|review|check|verify|test)\b", c) and re.search(r"\b(?:release gate|pre-merge gate|repository gate)\b", c):
        return "solforge-workflow-software-test", "repository release-gate verification"
    # Route short CI/release-gate failure questions by their diagnostic intent.
    if re.search(r"\b(?:explain|diagnose|investigate|why)\b", c) and re.search(r"\b(?:ci|release gate|required check|build check|test check)\b", c) and re.search(r"\b(?:red|failing|failed|failure|broken)\b", c):
        return "solforge-workflow-software-diagnose", "diagnosis of a failing software gate"
    # A generic writing deliverable should win over incidental domain nouns.
    if re.match(r"(?:write|draft|compose|create|prepare)\b", c) and re.search(r"\b(?:paragraph|description|body|title|summary|memo|notes?|email|document|text)\b", c) and not re.search(r"\b(?:scientific report|legal memo)\b", c):
        return "solforge-workflow-writing-draft", "explicit text deliverable"
    if re.search(r"\brelease readiness\b", c) and re.search(r"\b(?:reconcile|assess|verify|prepare|build|release)\b", c):
        return "solforge-workflow-launcher-release-readiness", "release readiness reconciliation"
    if re.search(r"\b(?:package matrix|native package|runtime-bundled|container artifact)\b", c) and re.search(r"\b(?:build|package|create|prepare)\b", c):
        return "solforge-workflow-launcher-package-matrix", "package matrix construction"
    if re.search(r"\b(?:install|uninstall|rollback|acquisition|prerequisites?)\b", c) and re.search(r"\b(?:installer|installation|target|software|application)\b", c):
        return "solforge-workflow-launcher-install", "safe installation lifecycle"
    if re.search(r"\b(?:security|vulnerabilit(?:y|ies)|trust boundary|unsafe input|exploit)\b", c) and re.search(r"\b(?:review|audit|assess|test|inspect)\b", c):
        return "solforge-workflow-software-security", "software security review"
    if re.search(r"\b(?:legal|policy|jurisdiction|compliance|regulation)\b", c) and re.search(r"\b(?:risk|obligations?|exposure|controls?|evidence gaps?)\b", c) and re.search(r"\b(?:assess|review|identify|audit)\b", c):
        return "solforge-workflow-legal-risk", "legal risk assessment"
    if re.search(r"\b(?:portability|supported platforms?|operating systems?)\b", c) and re.search(r"\b(?:audit|assess|review)\b", c):
        return "solforge-workflow-software-portability-audit", "software portability audit"
    if re.search(r"\b(?:dataset|data quality|data table|data source)\b", c) and re.search(r"\b(?:validate|clean|profile|audit|check)\b", c):
        return "solforge-workflow-data-validate", "data quality validation"
    if re.search(r"\b(?:dataset|data|metrics?|decision)\b", c) and re.search(r"\b(?:analyze|model|estimate|forecast)\b", c):
        return "solforge-workflow-data-analyze", "reproducible data analysis"
    if re.search(r"\b(?:chart|dashboard|visuali[sz]e|plot|figure)\b", c) and re.search(r"\b(?:build|create|visuali[sz]e|prepare)\b", c):
        return "solforge-workflow-data-visualize", "evidence-linked data visualization"
    if re.search(r"\b(?:mathematics|mathematical|theorem|lemma|equation|proof)\b", c):
        if re.search(r"\b(?:literature|related results|known techniques)\b", c): return "solforge-workflow-math-literature", "mathematical literature mapping"
        if re.search(r"\b(?:counterexample|boundary case|obstruction)\b", c): return "solforge-workflow-math-counterexample", "mathematical counterexample search"
        if re.search(r"\b(?:verify|check|audit)\b", c): return "solforge-workflow-math-verify", "mathematical verification"
        if re.search(r"\b(?:prove|proof)\b", c): return "solforge-workflow-math-prove", "mathematical proof construction"
        if re.search(r"\b(?:compute|numerical|symbolic)\b", c): return "solforge-workflow-math-compute", "mathematical computation"
        if re.search(r"\b(?:solve|derivation)\b", c): return "solforge-workflow-math-solve", "mathematical solution"
        if re.search(r"\b(?:explain|intuition)\b", c): return "solforge-workflow-math-explain", "mathematical explanation"
    if re.search(r"\b(?:outline|section architecture|argument structure)\b", c) and re.search(r"\b(?:create|write|prepare|outline)\b", c):
        return "solforge-workflow-writing-outline", "source-aware writing outline"
    if re.search(r"\b(?:fact ?check|citations?|unsupported claims?)\b", c) and re.search(r"\b(?:verify|check|factcheck|review)\b", c):
        return "solforge-workflow-writing-factcheck", "writing fact check"
    if re.search(r"\b(?:revise|polish|clarity|structure|consistency)\b", c) and re.search(r"\b(?:review|revise|edit|improve)\b", c):
        return "solforge-workflow-writing-review", "writing review"
    if re.search(r"\b(?:extend|synthesize|claim-evidence|contradiction analysis)\b", c) and re.search(r"\b(?:research|sources?|evidence)\b", c):
        return "solforge-workflow-research", "evidence-bound research synthesis"
    if re.match(r"(?:write|draft|compose|create|prepare)\b", c) and re.search(r"\bprompt\b", c):
        return "solforge-prompt", "explicit prompt authorship"
    if (
        re.search(r"\b(?:prepare|create|generate)\b", c)
        and re.search(r"\b(?:verified )?handoff\b", c)
    ) or re.search(r"\bhand\s+off\b", c):
        return "solforge-finalize", "verified handoff deliverable"
    if re.search(r"\b(?:provenance|signature|checksum|sbom|artifact digest)\b", c):
        return "solforge-sign-and-prove", "artifact-evidence deliverable"
    if re.search(r"\brelease matrix\b", c):
        return "solforge-release-matrix", "release matrix deliverable"
    if re.search(r"\b(?:scientific report|scientific package|methods and results)\b", c):
        return "solforge-workflow-science-report", "scientific reporting package"
    business = re.search(r"\b(?:business|market|commercial|go-to-market|customer segment|revenue)\b", c)
    if business and re.search(r"\b(?:research|assess|map|size|analyze|build)\b", c) and re.search(r"\b(?:market|demand|customer|segment|competitor|commercial)\b", c):
        return "solforge-workflow-business-market", "business market analysis"
    if business and re.search(r"\b(?:build|design|develop|create)\b", c) and re.search(r"\b(?:business model|revenue|unit economics|pricing|scenario)\b", c):
        return "solforge-workflow-business-model", "business model development"
    if business and re.search(r"\b(?:compare|contrast|evaluate)\b", c) and re.search(r"\b(?:alternatives?|options?|competitors?|business)\b", c):
        return "solforge-workflow-business-compare", "business option comparison"
    if business and re.search(r"\b(?:diligence|red flags?|risks?|assumptions?|viability)\b", c) and re.search(r"\b(?:conduct|review|assess|audit|investigate)\b", c):
        return "solforge-workflow-business-diligence", "business diligence"
    if business and re.search(r"\b(?:strategy|recommendation|roadmap|positioning|priorities)\b", c) and re.search(r"\b(?:create|build|formulate|develop|recommend)\b", c) and not re.search(r"\b(?:explain|define|means?)\b", c):
        return "solforge-workflow-business-strategy", "business strategy"
    ai_system = re.search(r"\b(?:ai|artificial intelligence|machine learning|ml|model|agent)\b", c)
    if ai_system and re.search(r"\b(?:validate|clean|curate|audit|check)\b", c) and re.search(r"\b(?:data|dataset|training|evaluation|labels?)\b", c):
        return "solforge-workflow-data-validate", "AI or agent data validation"
    if ai_system and (re.search(r"\b(?:train|tune|optimize|calibrate|improve)\b", c) or re.search(r"\bmodel\s+(?:the|an|a)\b", c)) and re.search(r"\b(?:agent|ai|model|training|optimization)\b", c):
        return "solforge-workflow-data-model", "AI or agent model optimization"
    if ai_system and re.search(r"\b(?:analyze|assess|measure|diagnose)\b", c) and re.search(r"\b(?:evaluation|metrics?|quality|sensitivity|uncertainty|performance)\b", c):
        return "solforge-workflow-data-analyze", "AI or agent evaluation analysis"
    if ai_system and re.search(r"\b(?:test|verify|validate|evaluate)\b", c) and re.search(r"\b(?:behavior|safety|regression|acceptance|agent|model)\b", c):
        return "solforge-workflow-software-test", "AI or agent behavior verification"
    web = re.search(r"\b(?:web design|website|web application|web app|browser|frontend|front-end)\b", c)
    if web and re.search(r"\b(?:create|design|prototype|build)\b", c) and re.search(r"\b(?:mvp|user flow|wireframe|interface|web design)\b", c):
        return "solforge-workflow-software-mvp-create", "web product design MVP"
    if web and re.search(r"\b(?:implement|build|develop|fix)\b", c):
        return "solforge-workflow-software-build", "web software implementation"
    if web and re.search(r"\b(?:test|verify|validate|check)\b", c) and re.search(r"\b(?:browser|responsive|accessibility|behavior|compatibility|regression)\b", c):
        return "solforge-workflow-software-test", "web behavior verification"
    design = re.search(r"\b(?:cad|ecad|mcad|pcb|schematic|layout|enclosure|bracket|mechanical design|electronic design|product design)\b", c)
    if design and re.search(r"\b(?:requirements?|constraints?|interfaces?|hazards?)\b", c) and re.search(r"\b(?:define|translate|specify|establish)\b", c):
        return "solforge-workflow-engineering-requirements", "engineering requirements definition"
    if design and re.search(r"\b(?:prototype|model|design artifact|layout)\b", c) and re.search(r"\b(?:create|build|develop|produce)\b", c):
        return "solforge-workflow-engineering-prototype", "engineering prototype or design artifact"
    if design and re.search(r"\b(?:compare|contrast|trade|alternatives?|options?)\b", c):
        return "solforge-workflow-engineering-trade", "engineering trade study"
    if design and re.search(r"\b(?:verify|validate|test|check)\b", c) and re.search(r"\b(?:tolerances?|failure modes?|clearance|drc|erc|requirements?)\b", c):
        return "solforge-workflow-engineering-verify", "engineering verification"
    if re.search(r"\b(?:scientific literature|literature review|evidence table|gap map)\b", c):
        return "solforge-workflow-science-literature", "scientific literature review"
    if re.search(r"\b(?:hypothesis|hypotheses|falsifiable|falsifier|prediction)\b", c) and re.search(r"\b(?:derive|formulate|testable|develop)\b", c):
        return "solforge-workflow-science-hypothesis", "testable scientific hypothesis"
    if re.search(r"\b(?:experiment|experimental|controls?|measurements?|power analysis)\b", c) and re.search(r"\b(?:design|specify|plan|prepare)\b", c):
        return "solforge-workflow-science-experiment", "controlled scientific experiment"
    if (
        re.search(r"\b(?:analysis|uncertainty|sensitivity|contrary evidence)\b", c)
        and re.search(r"\b(?:perform|analyze|analysis|reproducible)\b", c)
        and not re.search(r"\b(?:repository|repo|code|files?|implementation|diff|architecture|module)\b", c)
    ):
        return "solforge-workflow-science-analysis", "reproducible scientific analysis"
    if re.search(r"\b(?:reproduce|replicate|replication)\b", c) and re.search(r"\b(?:claim|study|result|published|experiment)\b", c):
        return "solforge-workflow-science-replication", "independent scientific replication"
    if re.search(r"\b(?:scientific report|scientific package|methods and results)\b", c):
        return "solforge-workflow-science-report", "scientific reporting package"
    if re.search(r"\b(?:portability|supported platforms?|operating systems?)\b", c) and re.search(r"\b(?:audit|assess|review)\b", c):
        return "solforge-workflow-software-portability-audit", "software portability audit"
    if re.search(r"\b(?:diagnose|investigate|debug|root cause)\b", c) and re.search(r"\b(?:ci|check|test|build|failure|error|red|broken|flaky)\b", c):
        return "solforge-workflow-software-diagnose", "diagnosis of a software failure"
    if re.search(r"\b(?:inspect|review|trace|understand)\b", c) and re.search(r"\b(?:repository|repo|code|files?|implementation|diff|architecture|module)\b", c):
        return "solforge-workflow-codebase", "repository or code investigation"
    if re.search(r"\b(?:implement|fix|build)\b", c) and re.search(r"\b(?:code|software|compatible|compatibility|repository|fix)\b", c):
        return "solforge-workflow-software-build", "software implementation"
    if re.search(r"\b(?:run|test|verify|validate)\b", c) and re.search(r"\b(?:ci|regression|focused|test|verification|release gate|build)\b", c):
        return "solforge-workflow-software-test", "software verification"
    legal = re.search(r"\b(?:legal|policy|jurisdiction|compliance|regulation)\b", c)
    if legal and re.search(r"\b(?:research|sources?|authoritative)\b", c):
        return "solforge-workflow-legal-research", "legal or policy research"
    if (legal or re.search(r"\bjurisdictions?\b", c)) and re.search(r"\b(?:compare|contrast|jurisdictions?)\b", c):
        return "solforge-workflow-legal-compare", "legal comparison"
    if legal and re.search(r"\b(?:draft|write|memo|document)\b", c):
        return "solforge-workflow-legal-draft", "legal writing"
    if re.search(r"\b(?:research|authoritative sources?)\b", c):
        return "sol-search", "source-backed research"
    if re.search(r"\b(?:compare|contrast|options)\b", c):
        return "solforge-workflow-software-compare", "comparison request"
    if re.search(r"\b(?:draft|write|compose|create|prepare|summarize)\b", c) and re.search(r"\b(?:description|body|title|summary|report|memo|notes?|email|document|text)\b", c):
        return "solforge-workflow-writing-draft", "explicit text deliverable"
    return None


def _fallback_skill(graph, clause, context):
    result = selector.route(graph, clause, context=context)
    return result["selected"][0] if result["selected"] else None


def compose_route(graph, objective, explicit=(), context=None, max_skills=10, blocked_skills=()):
    """Compose up to fifty ordered skills for a compound request.

    ``max_skills`` is a strict ceiling. Explicit skills are preserved first,
    subject to graph validity and the same ceiling. No selected skill executes
    work or authorizes effects.
    """
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("A nonempty objective is required.")
    if not isinstance(max_skills, int) or isinstance(max_skills, bool) or not 1 <= max_skills <= 50:
        raise ValueError("max_skills must be an integer from 1 through 50.")
    if isinstance(explicit, str) or not isinstance(explicit, (list, tuple)):
        raise ValueError("skills must be a list of skill IDs.")
    nodes = graph["nodes"]
    unknown = set(explicit) - set(nodes)
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(sorted(unknown)))

    clauses, ignored = segment(objective)
    excluded_effects = _excluded_effects(objective)
    selected = []
    stages = []
    unselected = []
    blocked = set(blocked_skills or ())

    def add(skill, stage, reason, confidence="high"):
        if skill is None or skill not in nodes or nodes[skill]["effect"] or skill in selected:
            return False
        if skill in blocked:
            unselected.append({"stage": stage + 1, "text": clauses[stage], "candidate": skill, "reason": "candidate inadmissible by contract policy"})
            return False
        if len(selected) >= max_skills:
            unselected.append({"stage": stage, "text": clauses[stage], "candidate": skill, "reason": "skill limit"})
            return False
        selected.append(skill)
        stages.append({"stage": stage + 1, "text": clauses[stage], "selected": [skill], "reason": reason, "confidence": confidence})
        return True

    for skill in explicit:
        if skill in blocked:
            unselected.append({"stage": None, "text": skill, "candidate": skill, "reason": "candidate inadmissible by contract policy"})
        elif len(selected) >= max_skills:
            unselected.append({"stage": None, "text": skill, "candidate": skill, "reason": "skill limit"})
        elif not nodes[skill]["effect"]:
            selected.append(skill)

    whole_objective = objective.casefold()
    math_context = bool(re.search(r"\b(?:mathematics|mathematical|theorem|lemma|equation|proof)\b", whole_objective))
    for index, clause in enumerate(clauses):
        if re.match(r"(?:explain|define)\b", clause.casefold()) and re.search(r"\b(?:business model|strategy class|means?)\b", clause.casefold()):
            unselected.append({"stage": index + 1, "text": clause, "candidate": None, "reason": "explanation request, no development workflow"})
            continue
        mapped = _mapped_skill(clause)
        if mapped is None and math_context:
            c = clause.casefold()
            if re.search(r"\b(?:counterexample|boundary case|obstruction)\b", c):
                mapped = ("solforge-workflow-math-counterexample", "mathematical counterexample search")
            elif re.search(r"\b(?:compute|numerical|symbolic)\b", c):
                mapped = ("solforge-workflow-math-compute", "mathematical computation")
            elif re.search(r"\b(?:verify|check|audit)\b", c):
                mapped = ("solforge-workflow-math-verify", "mathematical verification")
            elif re.search(r"\b(?:prove|proof)\b", c):
                mapped = ("solforge-workflow-math-prove", "mathematical proof construction")
            elif re.search(r"\b(?:solve|derivation)\b", c):
                mapped = ("solforge-workflow-math-solve", "mathematical solution")
            elif re.search(r"\b(?:explain|intuition)\b", c):
                mapped = ("solforge-workflow-math-explain", "mathematical explanation")
        if mapped:
            skill, reason = mapped
        else:
            skill = _fallback_skill(graph, clause, context)
            reason = "existing matcher fallback" if skill else "no confident specialist match"

        stage_selected = []
        if skill and add(skill, index, reason, "high" if mapped else "moderate"):
            stage_selected.append(skill)

        # Only use lexical catalog discovery when the rule/fallback composer
        # could not select a stage. Adding several lexical neighbors beside an
        # already matched capability inflates compound routes and destroys
        # precision. The higher-level router may still replace this provisional
        # choice with stronger query-centric identity evidence.
        if not stage_selected:
            semantic = selector.semantic_candidates(
                nodes,
                clause,
                limit=1,
                blocked=blocked,
            )
            if semantic:
                candidate = semantic[0]
                if add(
                    candidate["id"],
                    index,
                    f"semantic catalog fallback ({candidate['score']})",
                    "moderate",
                ):
                    stage_selected.append(candidate["id"])

        if not stage_selected:
            unselected.append({
                "stage": index + 1,
                "text": clause,
                "candidate": None,
                "reason": reason,
            })

    skills = []
    for skill in selected:
        node = dict(nodes[skill])
        node["reasons"] = [stage["reason"] for stage in stages if skill in stage["selected"]] or ["explicit selection"]
        skills.append(node)
    return {
        "objective": objective,
        "selected": selected,
        "skills": skills,
        "stages": stages,
        "unselected_requested_stages": unselected,
        "excluded_effects": excluded_effects,
        "execution_authorized": False,
        "selection_status": "matched" if selected else "abstained",
        "selection_trace": {"active_clauses": clauses, "ignored_clauses": ignored, "max_skills": max_skills},
        "next": "Read selected entrypoints in request order. Evaluate follow-up conditions within user authority." if selected else "No confident composed route.",
    }
