"""Derive the static console from the same catalog and graph as the service."""
from pathlib import Path
import hashlib
import json
import re

from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, catalog_graph


def main():
    root = Path(__file__).resolve().parents[1]
    catalog = SkillCatalog([BUNDLE_ROOT])
    assets = root / 'docs/assets'
    entries = [record.public() for record in catalog.records()]
    (assets / 'catalog.json').write_text(json.dumps(entries, ensure_ascii=False) + '\n', encoding='utf-8')
    current = {f'{record.id}.json' for record in catalog.records()}
    for stale in (assets / 'skills').glob('*.json'):
        if stale.name not in current:
            stale.unlink()
    for record in catalog.records():
        (assets / 'skills' / f'{record.id}.json').write_text(
            json.dumps(catalog.get(record.id), ensure_ascii=False) + '\n', encoding='utf-8')
    (assets / 'graph.json').write_text(json.dumps(catalog_graph(catalog), ensure_ascii=False) + '\n', encoding='utf-8')
    index = root / 'docs/index.html'
    version = hashlib.sha256((assets / 'app.js').read_bytes()).hexdigest()[:12]
    text = re.sub(r'assets/app\.js(?:\?v=[a-z0-9]+)?', f'assets/app.js?v={version}', index.read_text(encoding='utf-8'))
    index.write_text(text, encoding='utf-8')
    print(json.dumps({'skills': len(entries), 'version': version}))


if __name__ == '__main__':
    main()
