"""Derive the static console from the same catalog and graph as the service."""
from pathlib import Path
import hashlib
import json
import re

from solkraft.catalog import SkillCatalog
from solkraft.contract_schema import load_contract_schema
from solkraft.routing import BUNDLE_ROOT, catalog_graph, contract_index, route_request


def main():
    root = Path(__file__).resolve().parents[1]
    catalog = SkillCatalog([BUNDLE_ROOT])
    assets = root / 'docs/assets'
    contract_view = contract_index(catalog)
    contracts = {item["id"]: item for item in contract_view.entries()}
    entries = [
        {
            **record.public(),
            "contract": {
                "status": contracts[record.id]["status"],
                "trust": contracts[record.id]["trust"],
                "effects": contracts[record.id]["effects"],
                "capabilities": contracts[record.id]["capabilities"],
            },
        }
        for record in catalog.records()
    ]
    structure = {}
    for record in catalog.records():
        folder = BUNDLE_ROOT / record.id
        entrypoint = folder / 'SKILL.md'
        if entrypoint.is_file():
            content = entrypoint.read_text(encoding='utf-8')
            structure[record.id] = {
                'headings': re.findall(r'^#{1,3} (.+)$', content, re.MULTILINE),
                'python_files': [str(path.relative_to(folder)).replace('\\', '/')
                                 for path in sorted(folder.rglob('*.py')) if '__pycache__' not in path.parts],
                'references': [str(path.relative_to(folder)).replace('\\', '/')
                               for path in sorted((folder / 'references').rglob('*'))
                               if path.is_file() and '__pycache__' not in path.parts],
            }
    (assets / 'skill-structure.json').write_text(json.dumps(structure, ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'catalog.json').write_text(json.dumps(entries, ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'contracts.json').write_text(json.dumps(list(contracts.values()), ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'contract-index.json').write_text(json.dumps(contract_view.public(), ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'contract-schema.json').write_text(json.dumps(load_contract_schema(), ensure_ascii=False) + '\n', encoding='utf-8')
    current = {f'{record.id}.json' for record in catalog.records()}
    for stale in (assets / 'skills').glob('*.json'):
        if stale.name not in current:
            stale.unlink()
    for record in catalog.records():
        (assets / 'skills' / f'{record.id}.json').write_text(
            json.dumps({**catalog.get(record.id), "contract": contracts[record.id]}, ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'graph.json').write_text(json.dumps(catalog_graph(catalog), ensure_ascii=False) + '\n', encoding='utf-8')
    objective = 'Inspect the codebase, fix the bug, add a regression test, and verify the release build. Do not deploy or publish anything.'
    example = {'objective': objective, 'route': route_request(catalog, objective, max_skills=10)}
    (assets / 'example-route.json').write_text(json.dumps(example, ensure_ascii=False) + '\n', encoding='utf-8')
    index = root / 'docs/index.html'
    text = index.read_text(encoding='utf-8')
    versions = {}
    for name in ('app.js', 'flow.js', 'setup.js', 'static-data.js', 'style.css'):
        version = hashlib.sha256((assets / name).read_bytes()).hexdigest()[:12]
        versions[name] = version
        text = re.sub(r'assets/' + re.escape(name) + r'(?:\?v=[a-z0-9]+)?', f'assets/{name}?v={version}', text)
    index.write_text(text, encoding='utf-8')
    print(json.dumps({'skills': len(entries), 'contract_generation': contract_view.generation, 'versions': versions}))


if __name__ == '__main__':
    main()
