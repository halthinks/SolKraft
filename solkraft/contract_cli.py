"""Contract authoring helpers for the SolKraft CLI."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from .contract_schema import load_contract_schema, validate_v1_document
from .contract_verify import SUPPORTED_CHECKS


def _contract_path(target: str | Path) -> Path:
    path = Path(target).expanduser()
    if path.is_dir():
        return path / "contract.yaml"
    if path.name == "SKILL.md":
        return path.parent / "contract.yaml"
    return path


def _skill_id_from_entrypoint(folder: Path) -> str:
    entrypoint = folder / "SKILL.md"
    if not entrypoint.is_file():
        raise ValueError("SKILL.md was not found next to the target contract.")
    text = entrypoint.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must contain YAML frontmatter.")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed.") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    skill_id = data.get("name") if isinstance(data, dict) else None
    if not isinstance(skill_id, str) or not skill_id:
        raise ValueError("SKILL.md frontmatter must contain a name.")
    return skill_id


def init_contract(target: str | Path) -> dict:
    path = _contract_path(target)
    if path.exists():
        raise ValueError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    skill_id = _skill_id_from_entrypoint(path.parent)
    data = {
        "schema_version": "1.0",
        "skill_id": skill_id,
        "contract_revision": 1,
        "inputs": [],
        "outputs": [],
        "effects": [],
        "authority": {"capabilities": [], "resources": []},
        "risk": {
            "external": False,
            "destructive": False,
            "idempotent": True,
            "reversible": True,
            "open_world": False,
        },
        "verification": {
            "mode": "declarative",
            "description": "Replace this scaffold with evidence-backed checks for the real skill result.",
            "checks": [
                {"id": "result-present", "type": "field_present", "field": "result"}
            ],
        },
        "provenance": {"declaration": "author"},
        "extensions": {},
    }
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return {"path": str(path), "contract": data}


def validate_contract_path(target: str | Path, *, lint: bool = False) -> dict:
    path = _contract_path(target)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return {"path": str(path), "valid": False, "errors": [str(exc)], "warnings": []}
    errors = validate_v1_document(data)
    warnings = []
    if isinstance(data, dict):
        checks = ((data.get("verification") or {}).get("checks") or [])
        for check in checks:
            if isinstance(check, dict) and check.get("type") not in SUPPORTED_CHECKS:
                errors.append("unsupported declarative verification check type: " + str(check.get("type")))
        if lint and not checks:
            warnings.append("contract has no machine verification checks")
        if lint and (data.get("provenance") or {}).get("inferred") is True:
            warnings.append("contract is migration-inferred and cannot be treated as reviewed")
    return {"path": str(path), "valid": not errors, "errors": errors, "warnings": warnings}


def schema_document() -> dict:
    return load_contract_schema()


def migrate_contracts(*, write: bool = False, report: str | Path | None = None) -> dict:
    try:
        from scripts.migrate_contracts import migrate
    except ImportError as exc:
        raise RuntimeError("contract migrate requires a SolKraft source checkout") from exc
    result = migrate(write=write)
    if report:
        path = Path(report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result
