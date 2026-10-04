import json
import sys

from solkraft.__main__ import main


def test_contract_cli_init_validate_and_schema(tmp_path, monkeypatch, capsys):
    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Inspect a demo.\n---\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sys, "argv", ["solkraft", "contract", "init", str(folder)])
    main()
    created = json.loads(capsys.readouterr().out)
    assert created["contract"]["skill_id"] == "demo"
    assert (folder / "contract.yaml").is_file()

    monkeypatch.setattr(
        sys,
        "argv",
        ["solkraft", "contract", "validate", str(folder / "contract.yaml")],
    )
    main()
    validated = json.loads(capsys.readouterr().out)
    assert validated["valid"] is True

    monkeypatch.setattr(sys, "argv", ["solkraft", "contract", "schema"])
    main()
    schema = json.loads(capsys.readouterr().out)
    assert schema["title"] == "SolKraft Skill Contract v1"


def test_route_cli_emits_structured_policy(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "solkraft",
            "route",
            "Inspect the repository. Do not deploy anything.",
            "--strict-contracts",
            "--deny-effect",
            "repo.merge",
            "--grant-capability",
            "repo.read",
            "--grant-resource",
            "repo:demo",
            "--grant-id",
            "cli-grant",
        ],
    )
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["execution_authorized"] is False
    assert result["route_policy"]["contract_mode"] == "strict"
    assert "repo.merge" in result["route_policy"]["denied_effects"]
    assert result["route_policy"]["grant"]["grant_id"] == "cli-grant"



def test_contract_cli_portable_export_import(tmp_path, monkeypatch, capsys):
    root = tmp_path / "skills"
    folder = root / "demo"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Inspect a demo.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        """
schema_version: "1.0"
skill_id: demo
contract_revision: 1
effects: []
verification:
  mode: declarative
  checks:
    - id: result
      type: field_present
      field: result
""".strip() + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("SOLKRAFT_SKILL_ROOTS", str(root))

    monkeypatch.setattr(sys, "argv", ["solkraft", "contract", "export", "demo"])
    main()
    exported = json.loads(capsys.readouterr().out)
    assert exported["schema"] == "solkraft/portable-contract/v1"

    portable = tmp_path / "portable.json"
    portable.write_text(json.dumps(exported), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["solkraft", "contract", "import", str(portable)])
    main()
    imported = json.loads(capsys.readouterr().out)
    assert imported["trust"]["trusted"] is False
    assert imported["authority_granted"] is False
