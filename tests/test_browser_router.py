"""The Pages runtime contains and executes the same public production router."""
import json
import subprocess
import sys
import zipfile

from scripts.build_browser_router import build_runtime


def test_browser_runtime_is_deterministic_and_routes_in_isolation(tmp_path):
    first = tmp_path / 'first.zip'
    second = tmp_path / 'second.zip'
    receipt = build_runtime(first)
    build_runtime(second)
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        names = archive.namelist()
        assert 'solkraft/routing.py' in names
        assert 'solkraft/skillpacks/solforge/references/selection-graph.json' in names
        assert not any('__pycache__' in name or name.endswith('.pyc') for name in names)
        archive.extractall(tmp_path / 'runtime')
    code = '''import json, sys
sys.path.insert(0, sys.argv[1])
from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request
catalog = SkillCatalog([BUNDLE_ROOT])
result = route_request(catalog, "Inspect the codebase, then diagnose the crash, build the fix and test it", policy={"contract_mode":"hardened"})
assert len(catalog.records()) == 173
assert result["execution_authorized"] is False
assert "solforge-workflow-software-diagnose" in result["selected"]
assert "solforge-workflow-software-test" in result["selected"]
print(json.dumps(result["selected"]))'''
    result = subprocess.run([sys.executable, '-c', code, str(tmp_path / 'runtime')], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)
    assert receipt['file_count'] > 800
