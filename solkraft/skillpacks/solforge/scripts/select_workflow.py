"""Read-only native workflow selection with clause scope and explainable ranking.

Uses local rules and lexical evidence only: no network, models, or effect execution.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import unicodedata

STOP = set('a an the this that these those it its of for to in on with and or as is are be by from my our your please can could would i you we'.split())
DOMAIN_PATTERNS = {
    'software': r'\b(software|code|codebase|repo(?:sitory|sitories)?|application|app|service|endpoint|module|functionality|stack trace|exception|program|library|feature|api|csv export|linux|windows|macos)\b',
    'data': r'\b(data|dataset|records|rows|columns|revenue|sales|forecast|chart)\b',
    'science': r'\b(science|scientific|literature|papers|studies|experiment|hypothesis)\b',
    'mathematics': r'\b(mathematics|mathematical|theorem|lemma|proof|equation|axiom|conjecture)\b',
    'business': r'\b(business|market|competitors|investment|economics|strategy)\b',
    'legal_policy': r'\b(legal|laws?|policy|privacy|jurisdiction\w*|regulat\w*|obligations)\b',
    'engineering': r'\b(engineering|prototype|requirements|tolerance|hazard)\b',
    'writing': r'\b(writing|article|draft|manuscript|prose|document|report|email|release notes)\b',
}
ACTION_START = r'(?:research|investigate|implement|build|fix|refactor|test|verify|validate|draft|write|review|compare|diagnose|use|deploy|publish|send|delete|prove|explain|compile|create|generate|stop|pause|resume)\b'
# Graphs are immutable loaded selection data during normal CLI and session use.
# Retain a small identity cache so repeated routing does not rebuild the same
# lexical documents and document frequencies for every request.
_LEXICAL_INDEX_CACHE = {}


def normalize(text):
    return unicodedata.normalize('NFKC', text).casefold().replace('’', "'").replace('–', '-').replace('—', '-')


def tokens(text):
    result = []
    for word in re.findall(r'[a-z0-9]+', normalize(text)):
        if word in STOP or len(word) < 2:
            continue
        # Deliberately conservative inflection handling; domains and synonyms are data.
        if len(word) > 5 and word.endswith('ies'):
            word = word[:-3] + 'y'
        elif len(word) > 4 and word.endswith('s') and not word.endswith(('ss', 'us', 'is')):
            word = word[:-1]
        result.append(word)
    return result


def scope_clauses(objective):
    text = re.sub(r'[ \t]+', ' ', normalize(objective)).strip()
    # Inline formatting of a skill ID is a reference, not an embedded instruction.
    text = re.sub(r'`((?:solforge[\w-]*|sol-search|sol-merge-report))`', r'\1', text)
    ignored = []
    def hide(match):
        ignored.append({'text': match.group(0), 'reason': 'quoted content'})
        return ' '
    # Quoted source instructions must not become a request to execute their contents.
    text = re.sub(r'```[\s\S]*?```|`[^`\n]*`|"[^"\n]*"|(?<!\w)\x27[^\x27\n]+\x27(?!\w)', hide, text)
    boundary = r'[;\n]+|[.!?](?:\s+|$)|\b(?:then|after that|however|instead|but)\b|,\s*(?=(?:then\s+)?'+ACTION_START+r')|\band\s+(?='+ACTION_START+r')'
    parts = [p.strip(' ,:') for p in re.split(boundary, text) if p.strip(' ,:')]
    active = []
    for part in parts:
        if re.search(r'\b(already (?:complete|implemented|finished|done)|(?:implementation|research|refactor|build) is already|we (?:finished|completed))\b', part):
            ignored.append({'text': part, 'reason': 'completed work'})
            continue
        if re.search(r'\b(later|tomorrow|next month|next week|after approval)\b', part) and not re.search(r'\b(now|today)\b', part):
            ignored.append({'text': part, 'reason': 'deferred work'})
            continue
        neg = re.search(r"\b(?:do not|don't|dont|never|skip|avoid|without|no need to|rather than|no (?:implementation|code changes|coding|research|refactoring)|not asking (?:you )?to)\b", part)
        if neg:
            ignored.append({'text': part[neg.start():], 'reason': 'excluded scope'})
            part = part[:neg.start()].strip(' ,:')
        if part:
            part = re.sub(r'^(?:(?:please|just)\s+|(?:could|would|can|will) you\s+)+', '', part)
            active.append(part)
    return active, ignored



PR_OBJECT = r'\b(?:pull request|merge request|pr)\b'
DELIVERY_OBJECT = r'\b(?:pull request|merge request|pr|ci|github actions|code diff|build pipeline|branch|release[ -]gate|quality gate|approval gate|pre[ -]merge|before merge|regression suite|unit tests?|pending change|candidate release|release candidate|production candidate|patch set|patch queue|merge queue(?: entry)?|repository|feature branch|release branch|hotfix branch|staging branch|backport branch|dependency update|latest commit|final review|before release|before final approval)\b'
CODE_REVIEW_OBJECT = r'\b(?:code|diff|change(?:s|d)?|files?|call path|implementation|ownership|architecture|history|module boundar(?:y|ies)|api changes?|patch contents?)\b'

def delivery_intent(clause, context):
    """Resolve compound software artifacts before generic verb/topic matching.

    Returns (skill, reason) or None. Empty skill means the artifact mention is
    ambiguous, not a request to write prose. Context never selects an effect.
    """
    pr = bool(re.search(PR_OBJECT, clause))
    delivery = bool(re.search(DELIVERY_OBJECT, clause)) or bool(re.search(
        r'\b(?:required checks?|merge checks?|verification step|feature diff|modified module|patch|code changes? before merge|test pipeline|candidate build|smoke tests?|status checks?|validation job|deployment check|integration suite)\b', clause))
    # Writing ABOUT checks is a content request, not execution of those checks.
    if re.match(r'(?:write|draft|compose|create|prepare|polish|edit|revise|review|critique)\b', clause):
        if re.search(r'\b(?:description|body|title|summary|email|article|letter|essay|prose)\b', clause):
            return ('solforge-workflow-writing-review' if re.match(r'(?:review|revise|edit|polish|critique)\b', clause) else 'solforge-workflow-writing-draft'), 'explicit text deliverable'
        if re.search(r'\b(?:report|document|whitepaper)\b', clause):
            return None  # Existing document/report rules own this request.
        if re.search(r'\b(?:announcement|note|message|changelog)\b', clause):
            return ('solforge-workflow-writing-review' if re.match(r'(?:review|revise|edit|polish|critique)\b', clause) else 'solforge-workflow-writing-draft'), 'explicit text deliverable'
    # Delivery-specific routing starts here.  Do not turn generic requests to
    # validate data, fact-check prose, or review an architecture into CI work.
    if not delivery:
        return None
    if re.match(r'(?:explain|describe|summarize|what)\b', clause):
        return '', 'explanatory artifact mention'
    if re.search(r'\b(?:diagnos\w*|investigat\w*|debug|find why|why|review)\b', clause) and re.search(r'\b(?:fail\w*|broken|error\w*|red|timeout\w*|times? out|flaky|blocked|crash\w*|does not complete)\b', clause) and not (re.match(r'review\b', clause) and re.search(CODE_REVIEW_OBJECT, clause)):
        return 'solforge-workflow-software-diagnose', 'failing software delivery checks'
    if re.search(r'\b(?:review|inspect|check|understand|trace)\b', clause) and re.search(CODE_REVIEW_OBJECT, clause) and not re.search(r'\b(?:merge readiness|test pipeline|build-and-test gate)\b', clause):
        return 'solforge-workflow-codebase', 'review of code changes'
    if re.search(r'\b(?:run|execute|check|verify|verifying|validate|test|prepare)\b', clause) and re.search(r'\b(?:ci|continuous integration|checks?|tests?|suite|release[ -]gate|quality gate|merge readiness|regression|verification|validation|status checks?|acceptance|smoke|build|build-and-test|continuous delivery)\b', clause):
        return 'solforge-workflow-software-test', 'software verification or repository release gate'
    if re.match(r'(?:verify|validate|check)\b', clause):
        return 'solforge-workflow-software-test', 'verification of a repository delivery artifact'
    if re.match(r'(?:write|add|create)\b', clause) and re.search(r'\b(?:unit|regression|integration|automated) tests?\b', clause):
        return 'solforge-workflow-software-test', 'software test creation'
    if context.get('stage') == 'repository-release-gate' and ((delivery and re.match(r'(?:draft|prepare|continue|resume|finish)\b', clause)) or re.match(r'(?:continue|resume|finish) (?:the )?(?:release[ -]gate|checks|verification)\b', clause)):
        return 'solforge-workflow-software-test', 'current repository release-gate stage'
    if delivery and re.search(r'\b(?:draft|prepare|open|create)\b', clause):
        return '', 'PR artifact alone does not specify verification or prose writing'
    return None


def _binding_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return ' '.join(
            part for part in (value.get('name'), value.get('description'))
            if isinstance(part, str) and part
        )
    return ''


def lexical_index(nodes):
    documents = {
        k: Counter(tokens(' '.join([
            n['id'],
            n['description'],
            n.get('domain', ''),
            *[_binding_text(item) for item in n.get('outputs', [])],
        ])))
        for k, n in nodes.items()
    }
    df = Counter(t for d in documents.values() for t in d)
    avg = sum(sum(d.values()) for d in documents.values()) / max(1, len(documents))
    return documents, df, avg


def cached_lexical_index(nodes):
    key = id(nodes)
    cached = _LEXICAL_INDEX_CACHE.get(key)
    if cached is not None and cached[0] is nodes:
        return cached[1]
    index = lexical_index(nodes)
    # Keep the cache bounded for callers that load several graphs in one run.
    if len(_LEXICAL_INDEX_CACHE) >= 8:
        _LEXICAL_INDEX_CACHE.clear()
    _LEXICAL_INDEX_CACHE[key] = (nodes, index)
    return index


def lexical_score(node_id, query, index):
    docs, df, avg = index
    doc = docs[node_id]
    length = sum(doc.values())
    score = 0.0
    for term in set(tokens(query)):
        f = doc.get(term, 0)
        if f:
            idf = math.log(1 + (len(docs) - df[term] + .5) / (df[term] + .5))
            score += idf * f * 2.2 / (f + 1.2 * (.25 + .75 * length / max(avg, 1)))
    return score


def route(graph, objective, explicit=(), context=None):
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError('A nonempty objective is required.')
    if isinstance(explicit, str) or not isinstance(explicit, (list, tuple)) or not all(isinstance(x, str) for x in explicit):
        raise ValueError('skills must be a list of skill IDs.')
    if context is not None and not isinstance(context, dict):
        raise ValueError('context must be an object.')
    if (context or {}).get('stage') not in (None, 'repository-release-gate'):
        raise ValueError('Unknown context stage: ' + str(context['stage']))
    nodes = graph['nodes']
    unknown = set(explicit) - set(nodes)
    if unknown:
        raise ValueError('Unknown skills: ' + ', '.join(sorted(unknown)))
    matcher = graph.get('matcher', {})
    selected = list(dict.fromkeys(explicit))
    reasons = {s: ['explicit selection'] for s in selected}
    scores = {s: 100.0 for s in selected}
    alternatives = []
    active, ignored = scope_clauses(objective)
    visible = ' '.join(active)
    explanatory = bool(re.search(r'\b(?:explain|what is|what does|describe|summarize).{0,20}(?:solforge|sol-search)', visible)) or bool(re.match(r'(?:what (?:is|does|are)|define (?:the word|the term)|meaning of)\b', visible))
    # Context disambiguates subject matter, never contributes action authority.
    domains = [name for name, pattern in DOMAIN_PATTERNS.items() if re.search(pattern, visible)]
    given_domain = (context or {}).get('domain')
    domain_words = matcher.get('context_domains', {})
    if given_domain is not None:
        if not isinstance(given_domain, str) or given_domain not in domain_words:
            raise ValueError('Unknown context domain: ' + str(given_domain))
        if given_domain not in domains:
            domains.append(given_domain)
    domain_evidence = ' '.join(domain_words.get(d, '') for d in domains)
    if not explicit and not explanatory:
        for name, node in nodes.items():
            if not node['effect'] and re.search(r'(?<![\w-])' + re.escape(name) + r'(?![\w-])', visible):
                selected.append(name)
                reasons[name] = ['named skill in active request']
                scores[name] = 100.0
    if not selected and not explanatory:
        index = cached_lexical_index(nodes)
        candidates = []
        for stage, clause in enumerate(active):
            decision = delivery_intent(clause, context or {})
            # Prompt authorship owns embedded delivery work, as for other domains.
            if decision is not None and not re.search(r'\bprompt\b', visible):
                name, reason = decision
                if name:
                    candidates.append({'id': name, 'lane': 'writing' if 'writing-' in name else ('software-investigation' if name.endswith(('diagnose', 'codebase')) else 'verification'), 'stage': stage, 'score': 110.0, 'matched_clause': clause, 'concepts': [], 'reason': reason})
                else:
                    ignored.append({'text': clause, 'reason': reason})
                continue
            concepts = [label for label, pattern in matcher.get('concept_aliases', {}).items() if re.search(pattern, clause)]
            # Context has only domain vocabulary; aliases are matched against original active text.
            evidence = clause + ' ' + domain_evidence + ' ' + ' '.join(concepts)
            lanes = {}
            information_only = bool(re.match(r'(?:please |just )?(?:research|look up|explain|describe|summarize|check|verify|test|review|plan|compare|contrast)\b', clause))
            topic_only = bool(re.match(r'(?:write|draft|compose|create) (?:a |an |the )?(?:report|article|document|essay|summary) (?:about|on)\b', clause))
            for rule in graph['rules']:
                if topic_only and rule['lane'] not in ['report', 'writing', 'delivery']:
                    continue
                if nodes[rule['id']]['effect']:
                    continue
                if information_only and rule['lane'] in ['implementation', 'execution']:
                    continue
                matches = [re.search(p, evidence, re.I) for p in rule['all']]
                if not all(matches) or any(re.search(p, clause, re.I) for p in rule.get('unless', [])):
                    continue
                # A domain hint cannot, by itself, introduce a new requested action.
                if not any(re.search(p, clause + ' ' + ' '.join(concepts), re.I) for p in rule['all']):
                    continue
                lexical = lexical_score(rule['id'], clause, index)
                score = rule['priority'] + min(lexical, 12) + min(len(rule['all']), 4)
                candidate = {'id': rule['id'], 'lane': rule['lane'], 'stage': stage, 'score': round(score, 3),
                             'matched_clause': clause, 'concepts': concepts, 'reason': 'matched ' + rule['lane'] + ' intent'}
                old = lanes.get(rule['lane'])
                if old is None or (score, rule['id']) > (old['score'], old['id']):
                    if old:
                        alternatives.append(old)
                    lanes[rule['lane']] = candidate
                else:
                    alternatives.append(candidate)
            # Keep separate requested stages, but avoid routing the same research to a generic and specialist wrapper.
            if 'research' in lanes and any(x in lanes for x in ['science', 'mathematics', 'legal', 'claim-review', 'software-investigation', 'comparison']):
                alternatives.append(lanes.pop('research'))
            # Specific methods replace generic wrappers for the same request, not independent stages.
            if 'portability' in lanes and lanes.get('software-investigation', {}).get('id') == 'solforge-workflow-codebase':
                alternatives.append(lanes.pop('software-investigation'))
            if 'artifact-evidence' in lanes and lanes.get('delivery', {}).get('id') == 'solforge-workflow-launcher-release-readiness':
                alternatives.append(lanes.pop('delivery'))
            if re.fullmatch(r'(?:investigate|diagnose|inspect) (?:it|that|this)', clause) and any(c['lane']=='software-investigation' for c in candidates):
                lanes.pop('software-investigation', None)
            candidates.extend(lanes.values())
        prompt_candidates = [c for c in candidates if c['lane'] == 'prompt']
        if prompt_candidates:
            # Embedded work inside a generated prompt is not an execution request.
            candidates = prompt_candidates
        for c in sorted(candidates, key=lambda c: (c['stage'], -c['score'], c['id'])):
            name = c['id']
            if name not in selected:
                selected.append(name)
                scores[name] = c['score']
                reasons[name] = []
            reason = c['reason'] + ': ' + c['matched_clause']
            if reason not in reasons[name]:
                reasons[name].append(reason)
    followups = [e for e in graph['edges'] if e['from'] in selected and e['type'] != 'select']
    return {'objective': objective, 'selected': selected,
            'skills': [dict(nodes[s], reasons=reasons[s], match_score=scores[s]) for s in selected],
            'followups': followups, 'execution_authorized': False,
            'matcher_version': 3, 'selection_status': 'matched' if selected else 'abstained',
            'selection_trace': {'active_clauses': active, 'ignored_clauses': ignored, 'context_domains': domains, 'context_stage': (context or {}).get('stage'),
                                'score_meaning': 'Relative matching evidence; not a probability.', 'alternatives': alternatives},
            'next': 'Read selected entrypoints in request order. Evaluate follow-up conditions within user authority.' if selected else 'No confident match. Use domain context or an exact skill ID; ordinary tasks may need no workflow.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--objective')
    parser.add_argument('--skills', nargs='*', default=[])
    parser.add_argument('--request-file', type=Path)
    parser.add_argument('--context-domain')
    parser.add_argument('--context-stage', choices=['repository-release-gate'])
    parser.add_argument('--compose', action='store_true', help='compose an ordered route for a compound request')
    parser.add_argument('--max-skills', type=int, default=50, help='strict skill ceiling for --compose (1-50)')
    parser.add_argument('--list', dest='domain')
    parser.add_argument('--explain', action='store_true')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('--graph', type=Path, default=Path(__file__).resolve().parent.parent/'references'/'selection-graph.json')
    a = parser.parse_args()
    g = json.loads(a.graph.read_text(encoding='utf-8-sig'))
    root = a.graph.parent.parent
    if a.domain:
        result = [dict(n, path=str((root/n['path']).resolve())) for n in g['nodes'].values() if a.domain == 'all' or n['domain'] == a.domain]
    else:
        request = json.loads(a.request_file.read_text(encoding='utf-8-sig')) if a.request_file else {'objective': a.objective, 'skills': a.skills, 'context': {k: v for k, v in {'domain': a.context_domain, 'stage': a.context_stage}.items() if v is not None}}
        if a.compose:
            from compose_route import compose_route
            result = compose_route(g, request.get('objective'), request.get('skills', []), request.get('context'), a.max_skills)
        else:
            result = route(g, request.get('objective'), request.get('skills', []), request.get('context'))
        for n in result['skills']:
            n['path'] = str((root/n['path']).resolve())
            n['file_available'] = Path(n['path']).is_file()
        if not a.explain:
            result.pop('selection_trace')
        if a.compact:
            compact_fields = ['id', 'path', 'file_available', 'reasons', 'match_score']
            result['skills'] = [{k: n.get(k) for k in compact_fields} for n in result['skills']]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
