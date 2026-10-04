from pathlib import Path

import yaml

from scripts.preflight_contribution import build_bundle


ROOT = Path(__file__).resolve().parents[1]


def test_reusable_ci_and_preflight_workflows_exist():
    reusable = (ROOT / ".github/workflows/reusable-ci.yml").read_text(encoding="utf-8")
    preflight = (ROOT / ".github/workflows/contribution-preflight.yml").read_text(encoding="utf-8")
    tests = (ROOT / ".github/workflows/tests.yml").read_text(encoding="utf-8")
    assert "workflow_call:" in reusable
    assert "scripts.preflight_contribution" in reusable
    assert "workflow_dispatch:" in preflight
    assert "uses: ./.github/workflows/reusable-ci.yml" in preflight
    assert "pull_request:" in tests
    assert "uses: ./.github/workflows/reusable-ci.yml" in tests


def test_workflow_yaml_parses():
    for name in ("reusable-ci.yml", "contribution-preflight.yml", "tests.yml"):
        data = yaml.safe_load((ROOT / ".github/workflows" / name).read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert data.get("jobs")


def test_preflight_bundle_collects_existing_receipts(tmp_path, monkeypatch):
    root = tmp_path
    (root / "contributions").mkdir()
    manifest = root / "contributions/demo.json"
    manifest.write_text('{"schema":"solkraft/contribution/v1","skill":"demo"}', encoding="utf-8")
    (root / "build/contributions").mkdir(parents=True)
    (root / "build/contributions/latest.json").write_text(
        '{"status":"passed","source_sha256":"abc","full_regression":{"total":100000,"passed":100000}}',
        encoding="utf-8",
    )
    (root / "build").mkdir(exist_ok=True)
    (root / "build/local-ci.json").write_text('{"status":"passed"}', encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts/results-routing-100000.json").write_text(
        '{"total":100000,"passed":100000}', encoding="utf-8"
    )
    (root / "solkraft/skillpacks/demo").mkdir(parents=True)
    (root / "solkraft/skillpacks/demo/SKILL.md").write_text("demo", encoding="utf-8")
    (root / "dist").mkdir()
    (root / "dist/solkraft-demo.whl").write_bytes(b"wheel")
    (root / "docs/downloads").mkdir(parents=True)
    (root / "docs/downloads/solkraft-plugin.zip").write_bytes(b"plugin")

    import scripts.preflight_contribution as preflight
    monkeypatch.setattr(preflight, "ROOT", root)
    summary = build_bundle(manifest)
    assert summary["status"] == "passed"
    assert summary["routing_passed"] == 100000
    assert (root / summary["bundle"]["path"]).is_file()
