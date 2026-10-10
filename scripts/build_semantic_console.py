"""Publish a completed source-bound semantic receipt and actual route examples."""
import argparse
import json
from pathlib import Path
from scripts.semantic_router_benchmark import source_identity
from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    ('Fix a repository issue', 'Inspect the repository, diagnose the CI failure, implement a fix, run regression tests, and write the PR description'),
    ('Validate a dataset', 'Validate the dataset for missing rows and duplicate records'),
    ('Compare business options', 'Build a business model, compare the business alternatives, and develop a business strategy'),
    ('Review a mathematical proof', 'Verify every step of the mathematical proof'),
    ('Respect excluded work', 'Do not audit software security'),
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, default=ROOT / 'build/semantic-proof-local/summary.json')
    args = parser.parse_args()
    summary = json.loads(args.receipt.read_text(encoding='utf-8'))
    if not summary.get('proof_passed') or not summary.get('gates') or not all(summary['gates'].values()):
        raise SystemExit('Cannot publish an incomplete or failed semantic proof.')
    if summary.get('source') != source_identity():
        raise SystemExit('Cannot publish a semantic proof for different source inputs.')
    catalog = SkillCatalog([BUNDLE_ROOT])
    names = {r.id: r.name for r in catalog.records()}
    examples = []
    for label, objective in EXAMPLES:
        route = route_request(catalog, objective, policy={'contract_mode': 'hardened'})
        examples.append({'label': label, 'objective': objective, 'route': route,
                         'names': {sid: names[sid] for sid in route['selected']}})
    output = ROOT / 'docs/assets/semantic-proof.json'
    output.write_text(json.dumps({'summary': summary, 'examples': examples}, indent=2) + '\n', encoding='utf-8')
    print(f'Published completed receipt and {len(examples)} production route examples: {output}')

if __name__ == '__main__':
    main()
