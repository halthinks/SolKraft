"""Check a complete skill integration using the public router, not explicit IDs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from solkraft.catalog import SkillCatalog
from solkraft.contract_loader import load_skill_contract
from solkraft.contract_verify import SUPPORTED_CHECKS
from solkraft.trust import resolve_trust
from solkraft.routing import BUNDLE_ROOT, GRAPH_PATH, get_graph, route_request

ROOT = Path(__file__).resolve().parents[1]


def validate(data, graph, catalog):
    errors = []
    skill = data.get('skill', '')
    if data.get('schema') != 'solkraft/contribution/v1':
        errors.append('Use schema solkraft/contribution/v1.')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', skill):
        errors.append('Skill ID must use lowercase letters, digits and hyphens; maximum 64 characters.')
    record_map = {r.id: r for r in catalog.records()}
    records = set(record_map)
    if skill not in records:
        errors.append('Skill must be published in the bounded catalog.')
    node = graph['nodes'].get(skill)
    if not node:
        errors.append('Register the skill in the semantic core graph, not only the catalog.')
    else:
        for field in ('description', 'domain', 'inputs', 'outputs', 'exit_evidence', 'path'):
            if not node.get(field):
                errors.append('Graph node missing ' + field)
        if node.get('effect') is not False:
            errors.append('Automatic contribution routing must preserve effect: false.')
        if node.get('path') != f'../{skill}/SKILL.md':
            errors.append('Graph path must point to the bundled skill entrypoint.')
    rules = [r for r in graph['rules'] if r.get('id') == skill]
    if not rules:
        errors.append('Add a discriminating graph rule with action and subject vocabulary.')
    for rule in rules:
        if not rule.get('all') or not rule.get('lane') or not isinstance(rule.get('priority'), (int, float)):
            errors.append('Each rule needs all, lane, and numeric priority.')
        for pattern in rule.get('all', []) + rule.get('unless', []):
            try:
                re.compile(pattern)
            except (re.error, TypeError):
                errors.append('Invalid routing regex: ' + str(pattern))
    for edge in graph['edges']:
        if skill in (edge.get('from'), edge.get('to')) and (
                edge.get('from') not in graph['nodes'] or edge.get('to') not in graph['nodes'] or not edge.get('condition')):
            errors.append('Related edges need existing endpoints and a real condition.')
    provenance = data.get('provenance', {})
    if not all(provenance.get(k) for k in ('author', 'license', 'source')):
        errors.append('Provide author, license and source provenance; humans must review redistribution rights.')
    cases = data.get('cases', [])
    if not cases or not any(skill in c.get('selected', []) for c in cases):
        errors.append('Include positive automatic-selection examples.')
    negatives = [c for c in cases if skill not in c.get('selected', [])]
    for pattern, name in [(r'\b(do not|never|skip)\b', 'excluded'), (r'\b(tomorrow|later|next week)\b', 'deferred'), (r'["`]', 'quoted')]:
        if not any(re.search(pattern, c.get('objective', ''), re.I) for c in negatives):
            errors.append(f'Include a {name} negative example.')
    for case in cases:
        if not isinstance(case.get('objective'), str) or not case['objective'].strip() or not isinstance(case.get('selected'), list):
            errors.append('Cases need a nonempty objective and exact ordered selected list.')
        elif set(case['selected']) - records:
            errors.append('Case expects an unavailable skill.')
    if skill in record_map:
        contract = load_skill_contract(
            record_map[skill].entrypoint,
            legacy_node=graph["nodes"].get(skill),
            expected_skill_id=record_map[skill].name,
        )
        if contract.get("source") == "sidecar" and contract.get("status") in {"invalid", "unsupported"}:
            errors.append("contract.yaml must be a supported valid Contract v1 sidecar.")
        verification = contract.get("verification") or {}
        if contract.get("source") == "sidecar" and contract.get("status") == "declared":
            if not verification.get("checks"):
                errors.append("Declared Contract v1 sidecars must include at least one declarative verification check.")
            for check in verification.get("checks") or []:
                if check.get("type") not in SUPPORTED_CHECKS:
                    errors.append("Unsupported declarative verification check type: " + str(check.get("type")))
    return errors


def simulate(data, catalog, variants=25):
    failures, seen, total, passed = [], set(), 0, 0
    for case in data['cases']:
        for variant in range(variants + 1):
            objective = case['objective']
            if variant:
                # These are contextual robustness variants, not independent intents.
                objective += f'. Context notes: sample {variant} preserves source identities and user requirements.'
            if objective in seen:
                raise ValueError('Duplicate generated request; make the base cases unique.')
            seen.add(objective)
            result = route_request(catalog, objective, max_skills=50, context=case.get('context'))
            total += 1
            good = result['selected'] == case['selected'] and result['execution_authorized'] is False
            passed += good
            if not good and len(failures) < 20:
                failures.append({'objective': objective, 'expected': case['selected'], 'actual': result['selected']})
    return {'total': total, 'unique': len(seen), 'passed': passed, 'failures': failures,
            'meaning': 'Authored intent cases plus contextual variants; not agent execution or skill-quality certification.'}


def source_digest():
    digest = hashlib.sha256()
    for folder in (ROOT / 'solkraft', ROOT / 'scripts'):
        for path in sorted(folder.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix in ('.py', '.json', '.md') and not path.name.startswith('results-'):
                digest.update(path.relative_to(ROOT).as_posix().encode())
                digest.update(path.read_bytes())
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--full', action='store_true', help='Also run the complete 100,000-request regression and local artifact gate.')
    parser.add_argument('--variants', type=int, default=25)
    args = parser.parse_args()
    if not 0 <= args.variants <= 10000:
        parser.error('--variants must be between 0 and 10000')
    data = json.loads(args.manifest.read_text(encoding='utf-8'))
    catalog = SkillCatalog([BUNDLE_ROOT])
    errors = validate(data, get_graph(), catalog)
    record = next((r for r in catalog.records() if r.id == data.get('skill')), None)
    contract = (
        load_skill_contract(
            record.entrypoint,
            legacy_node=get_graph()["nodes"].get(record.id),
            expected_skill_id=record.name,
        )
        if record else {}
    )
    receipt = {'schema': 'solkraft/contribution-result/v1', 'skill': data.get('skill'),
               'source_sha256': source_digest(), 'manifest_sha256': hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
               'status': 'failed', 'errors': errors, 'full_regression': 'not_run',
               'contract': {
                   'status': contract.get('status'),
                   'source': contract.get('source'),
                   'contract_digest': contract.get('contract_digest'),
                   'entrypoint_digest': contract.get('entrypoint_digest'),
                   'trust': resolve_trust(data.get('skill'), contract) if contract else None,
               }}
    try:
        if errors:
            raise ValueError('\n'.join(errors))
        receipt['simulation'] = simulate(data, catalog, args.variants)
        if receipt['simulation']['passed'] != receipt['simulation']['total']:
            raise ValueError('Automatic routing cases failed; inspect the receipt.')
        if args.full:
            subprocess.run([sys.executable, '-m', 'scripts.routing_battery'], cwd=ROOT, check=True)
            result = json.loads((ROOT / 'scripts/results-routing-100000.json').read_text())
            if result['total'] != 100000 or result['passed'] != 100000:
                raise ValueError('The complete 100,000-request regression must pass.')
            receipt['full_regression'] = result
            subprocess.run([sys.executable, '-m', 'scripts.local_ci'], cwd=ROOT, check=True)
        receipt['status'] = 'passed' if args.full else 'targeted_passed'
    except (ValueError, subprocess.CalledProcessError) as error:
        receipt['error'] = str(error)
        raise
    finally:
        target = ROOT / 'build/contributions'
        target.mkdir(parents=True, exist_ok=True)
        (target / 'latest.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
