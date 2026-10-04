"""Read-only catalog of instruction-based skills."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Iterable

import yaml

from .contracts import contract_from_declaration


RETIRED_SKILLS = frozenset(json.loads((Path(__file__).parent / 'retired-skills.json').read_text(encoding='utf-8'))['skills'])
MAX_ENTRYPOINT_BYTES = 128_000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}$")
TOKEN_RE = re.compile(r"[a-z0-9]+")
RESERVED_SKILL_DIGESTS = frozenset({
    '088a975a1b2e13c8b3d25ebf2bfe6a09bf14cab64aad091985157100690a1e61',
    "0495f731a53b6b2bf383ce23195c4fc8e80fdaf772104067c8e61e7433921904",
    "4c5286c8e758c4a2b88fcbd71a38d3e5601e000796e1b917ff51db89f6aee5a9",
    "b45df0229355259f8587ddc98766447d0806449f8b6874a763cf9a52f468b9f2",
    "3e3a2b9765ca7dad250a071877b7738f800c0c525085fc2a20c51c3e7835044f",
})


def _is_reserved_skill(name: str, relative: Path) -> bool:
    identifiers = {name.casefold(), *(part.casefold() for part in relative.parts)}
    identifiers.update(name.casefold().split("-"))
    return any(hashlib.sha256(value.encode("utf-8")).hexdigest() in RESERVED_SKILL_DIGESTS for value in identifiers)


class SkillNotFound(KeyError):
    """The requested skill is not in the public catalog."""


@dataclass(frozen=True)
class SkillRecord:
    id: str
    description: str
    root: Path
    entrypoint: Path
    name: str
    contract: dict

    def public(self, score: float | None = None) -> dict:
        item = {"id": self.id, "name": self.name, "description": self.description, "contract": self.contract}
        if score is not None:
            item["score"] = round(score, 4)
        return item


class SkillCatalog:
    """Index SKILL.md metadata; load a body only after the caller selects it."""

    def __init__(self, roots: Iterable[str | Path], *, preferred_root: Path | None = None):
        self.roots = tuple(Path(root).expanduser() for root in roots)
        self.preferred_root = preferred_root.resolve() if preferred_root else None
        self._records: dict[str, SkillRecord] = {}
        self.refresh()

    def refresh(self) -> int:
        candidates: list[tuple] = []
        seen_contents = set()
        for root in self.roots:
            try:
                resolved_root = root.resolve(strict=True)
            except (OSError, RuntimeError):
                continue
            if not resolved_root.is_dir():
                continue
            try:
                entrypoints = self._entrypoints(resolved_root)
                for entrypoint in entrypoints:
                    try:
                        resolved_entry = entrypoint.resolve(strict=True)
                        resolved_entry.relative_to(resolved_root)
                        if entrypoint.is_symlink() or not resolved_entry.is_file():
                            continue
                        if resolved_entry.stat().st_size > MAX_ENTRYPOINT_BYTES:
                            continue
                        metadata = self._frontmatter(resolved_entry)
                    except (OSError, RuntimeError, ValueError, yaml.YAMLError):
                        continue
                    name = metadata.get("name")
                    description = metadata.get("description")
                    if not isinstance(name, str) or not ID_RE.fullmatch(name.strip()):
                        continue
                    name = name.strip()
                    if not isinstance(description, str) or not description.strip():
                        continue
                    description = " ".join(description.split())[:2000]
                    relative = resolved_entry.relative_to(resolved_root)
                    if name in RETIRED_SKILLS or _is_reserved_skill(name, relative):
                        continue
                    digest = hashlib.sha256(resolved_entry.read_bytes()).digest()
                    if digest in seen_contents:
                        continue
                    seen_contents.add(digest)
                    contract = contract_from_declaration({
                        "inputs": metadata.get("inputs"),
                        "side_effects": metadata.get("side_effects"),
                        "auth_scope": metadata.get("auth_scope"),
                        "test_contract": metadata.get("test_contract"),
                    })
                    candidates.append((name, description, resolved_root, resolved_entry, root.name or "skills", contract))
            except OSError:
                continue

        counts = Counter(row[0] for row in candidates)
        records: dict[str, SkillRecord] = {}
        for name, description, root, entrypoint, namespace, contract in candidates:
            skill_id = f"{namespace}:{name}" if counts[name] > 1 and root != self.preferred_root else name
            if skill_id in records:
                relative_parent = entrypoint.parent.relative_to(root).as_posix().replace("/", ".")
                skill_id = f"{namespace}.{relative_parent}:{name}"
            if not ID_RE.fullmatch(skill_id):
                continue
            records[skill_id] = SkillRecord(skill_id, description, root, entrypoint, name, contract)
        self._records = dict(sorted(records.items(), key=lambda pair: pair[0].casefold()))
        return len(self._records)

    @staticmethod
    def _entrypoints(root: Path):
        for parent, directories, files in os.walk(root, followlinks=False):
            directories[:] = sorted(d for d in directories
                if (not d.startswith('.') or d == '.system')
                and d not in {'node_modules', '__pycache__', 'dist', 'build'}
                and not (Path(parent) / d).is_symlink())
            if 'SKILL.md' in files:
                yield Path(parent) / 'SKILL.md'

    @staticmethod
    def _frontmatter(path: Path) -> dict:
        with path.open("r", encoding="utf-8-sig") as handle:
            text = handle.read(MAX_ENTRYPOINT_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_ENTRYPOINT_BYTES:
            return {}
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}
        try:
            end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
        except StopIteration:
            return {}
        data = yaml.safe_load("\n".join(lines[1:end]))
        return data if isinstance(data, dict) else {}

    def list(self, limit: int = 100, offset: int = 0) -> list[dict]:
        records = list(self._records.values())[offset:offset + limit]
        return [record.public() for record in records]

    def search(self, query: str, limit: int = 10, *, declared_only: bool = False) -> list[dict]:
        terms = [term for term in TOKEN_RE.findall(query.casefold()) if len(term) > 1]
        records = [record for record in self._records.values() if not declared_only or record.contract.get("declared")]
        if not terms:
            return [record.public() for record in records[:limit]]
        scored: list[tuple[float, SkillRecord]] = []
        for record in records:
            contract_text = " ".join(record.contract.get("inputs") or [])
            skill_terms = set(TOKEN_RE.findall((record.id + " " + record.description + " " + contract_text).casefold()))
            if not skill_terms:
                continue
            exact_name = 3.5 * sum(1 for term in terms if term in record.id.casefold())
            overlap = sum(1 for term in terms if term in skill_terms)
            coverage = overlap / max(len(set(terms)), 1)
            score = exact_name + overlap + coverage * 2.0
            if record.contract.get("declared"):
                score += 1.0
            if score > 0:
                scored.append((score, record))
        scored.sort(key=lambda row: (-row[0], row[1].id.casefold()))
        return [record.public(score) for score, record in scored[:limit]]

    def get(self, skill_id: str) -> dict:
        record = self._records.get(skill_id)
        if record is None:
            raise SkillNotFound(skill_id)
        try:
            resolved = record.entrypoint.resolve(strict=True)
            resolved.relative_to(record.root)
            if resolved.is_symlink() or not resolved.is_file():
                raise SkillNotFound(skill_id)
            if resolved.stat().st_size > MAX_ENTRYPOINT_BYTES:
                raise SkillNotFound(skill_id)
            content = resolved.read_text(encoding="utf-8-sig")
        except (OSError, RuntimeError, ValueError) as exc:
            raise SkillNotFound(skill_id) from exc
        return {**record.public(), "content": content}

    def get_resource(self, skill_id: str, resource: str) -> dict:
        record = self._records.get(skill_id)
        if record is None or not resource:
            raise SkillNotFound(skill_id)
        try:
            target = (record.entrypoint.parent / resource).resolve(strict=True)
            target.relative_to(record.root)
            if not target.is_file() or target.stat().st_size > MAX_ENTRYPOINT_BYTES:
                raise SkillNotFound(resource)
            if target.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py", ".txt"}:
                raise SkillNotFound(resource)
            content = target.read_text(encoding="utf-8-sig")
        except (OSError, RuntimeError, ValueError, UnicodeError) as exc:
            raise SkillNotFound(resource) from exc
        return {"skill_id": skill_id, "resource": resource, "content": content}

    def records(self) -> tuple[SkillRecord, ...]:
        return tuple(self._records.values())
