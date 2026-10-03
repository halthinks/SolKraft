from pathlib import Path
import hashlib

import pytest

from solkraft import catalog as catalog_module
from solkraft.catalog import RESERVED_SKILL_DIGESTS, SkillCatalog, SkillNotFound
from solkraft.routing import BUNDLE_ROOT


def write_skill(root: Path, name: str, description: str, body: str = "# Skill\n\nUseful body.\n") -> Path:
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "SKILL.md"
    path.write_text(f"---\nname: {name}\ndescription: {description!r}\n---\n\n{body}", encoding="utf-8")
    return path


def test_discovers_skills_without_loading_all_bodies(tmp_path):
    root = tmp_path / "skills"
    entry = write_skill(root, "data-chart", "Build a chart from tabular data.")
    catalog = SkillCatalog([root])

    rows = catalog.search("make a chart from data", limit=3)

    assert rows
    assert rows[0]["id"] == "data-chart"
    assert rows[0]["description"] == "Build a chart from tabular data."
    assert "path" not in rows[0]
    assert catalog.get("data-chart")["content"].endswith("Useful body.\n")
    assert entry.exists()


def test_exclusion_filter_does_not_hide_other_specialist_skills(tmp_path, monkeypatch):
    root = tmp_path / "skills"
    blocked = "reserved-private-skill"
    digest = hashlib.sha256(blocked.encode()).hexdigest()
    monkeypatch.setattr(catalog_module, "RESERVED_SKILL_DIGESTS", {digest})
    write_skill(root, blocked, "Private skill.")
    write_skill(root, "engineering-verification", "Verify an engineering design.")
    write_skill(root, "pcb-routing", "Route a printed circuit board.")
    write_skill(root, "writing-review", "Review and improve prose.")

    catalog = SkillCatalog([root])

    assert {row["id"] for row in catalog.list()} == {"engineering-verification", "pcb-routing", "writing-review"}


def test_bundled_catalog_uses_reserved_fingerprints_and_contains_engineering_skills():
    catalog = SkillCatalog([BUNDLE_ROOT])
    assert len(catalog.records()) >= 230
    assert "solforge-workflow-engineering-requirements" in {record.id for record in catalog.records()}
    for record in catalog.records():
        identifiers = {record.name.casefold(), *(part.casefold() for part in record.entrypoint.relative_to(record.root).parts)}
        assert not any(hashlib.sha256(value.encode()).hexdigest() in RESERVED_SKILL_DIGESTS for value in identifiers)


def test_rejects_path_traversal_and_references_outside_entrypoint(tmp_path):
    root = tmp_path / "skills"
    write_skill(root, "writing-review", "Review prose.")
    (tmp_path / "secret.txt").write_text("private", encoding="utf-8")
    catalog = SkillCatalog([root])

    with pytest.raises(SkillNotFound):
        catalog.get("../../secret")


def test_duplicate_ids_get_stable_source_namespaces(tmp_path):
    left = tmp_path / "vendor-one"
    right = tmp_path / "vendor-two"
    write_skill(left, "deploy", "Deploy a website.")
    write_skill(right, "deploy", "Deploy an application.")

    catalog = SkillCatalog([left, right])

    assert {row["id"] for row in catalog.list()} == {"vendor-one:deploy", "vendor-two:deploy"}
