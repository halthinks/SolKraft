"""Read-only catalog of instruction-based skills."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Iterable

import yaml

from .contract_index import ContractIndex


RETIRED_SKILLS = frozenset(json.loads((Path(__file__).parent / 'retired-skills.json').read_text(encoding='utf-8'))['skills'])
MAX_ENTRYPOINT_BYTES = 128_000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}$")
TOKEN_RE = re.compile(r"[a-z0-9]+")
# Catalog identity constraints use stable fingerprints.
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

    def public(self, score: float | None = None) -> dict:
        item = {"id": self.id, "name": self.name, "description": self.description}
        if score is not None:
            item["score"] = round(score, 4)
        return item


class SkillCatalog:
    """Index SKILL.md metadata; load a body only after the caller selects it."""

    def __init__(self, roots: Iterable[str | Path], *, preferred_root: Path | None = None):
        self.roots = tuple(Path(root).expanduser() for root in roots)
        self.preferred_root = preferred_root.resolve() if preferred_root else None
        self._records: dict[str, SkillRecord] = {}
        self._contract_index = ContractIndex()
        self._identity_profiles: dict[str, dict] = {}
        self._identity_idf: dict[str, float] = {}
        self.refresh()

    def refresh(self) -> int:
        candidates: list[tuple[str, str, Path, Path, str]] = []
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
                    candidates.append((name, description, resolved_root, resolved_entry, root.name or "skills"))
            except OSError:
                continue

        counts = Counter(row[0] for row in candidates)
        records: dict[str, SkillRecord] = {}
        for name, description, root, entrypoint, namespace in candidates:
            skill_id = f"{namespace}:{name}" if counts[name] > 1 and root != self.preferred_root else name
            # Root names can themselves collide; use a stable relative folder as a second discriminator.
            if skill_id in records:
                relative_parent = entrypoint.parent.relative_to(root).as_posix().replace("/", ".")
                skill_id = f"{namespace}.{relative_parent}:{name}"
            if not ID_RE.fullmatch(skill_id):
                continue
            records[skill_id] = SkillRecord(skill_id, description, root, entrypoint, name)
        self._records = dict(sorted(records.items(), key=lambda pair: pair[0].casefold()))
        self._build_identity_index()
        return len(self._records)

    def _build_identity_index(self) -> None:
        """Build compact semantic identity profiles from public skill metadata."""
        token_sets = {}
        profiles = {}
        for skill_id, record in self._records.items():
            desc_tokens = [
                token for token in TOKEN_RE.findall(record.description.casefold())
                if len(token) > 2
            ]
            name_tokens = [
                token for token in TOKEN_RE.findall(record.name.casefold())
                if len(token) > 1
            ]
            token_set = set(desc_tokens) | set(name_tokens)
            token_sets[skill_id] = token_set
            profiles[skill_id] = {
                "description_norm": " ".join(record.description.casefold().split()),
                "description_tokens": tuple(desc_tokens),
                "name_tokens": tuple(name_tokens),
            }

        document_frequency = Counter()
        for token_set in token_sets.values():
            document_frequency.update(token_set)
        total = max(len(token_sets), 1)
        self._identity_idf = {
            token: math.log((total + 1.0) / (count + 1.0)) + 1.0
            for token, count in document_frequency.items()
        }

        for skill_id, profile in profiles.items():
            distinct = set(profile["description_tokens"]) | set(profile["name_tokens"])
            profile["weight"] = sum(self._identity_idf.get(token, 1.0) for token in distinct) or 1.0
        self._identity_profiles = profiles

    def identity_match(
        self,
        query: str,
        *,
        min_score: float = 0.58,
        min_margin: float = 0.08,
    ) -> dict | None:
        """Return a high-confidence capability identity match, if one exists.

        Exact published-description matches are authoritative for identity only;
        route policy still decides whether that capability is admissible.
        Paraphrase matching uses IDF-weighted coverage and requires a clear
        margin over the next candidate.
        """
        normalized = " ".join(query.casefold().split())
        if not normalized:
            return None

        exact = []
        for skill_id, profile in self._identity_profiles.items():
            phrase = profile["description_norm"]
            if len(phrase) >= 24 and phrase in normalized:
                exact.append(skill_id)
        if len(exact) == 1:
            return {
                "id": exact[0],
                "score": 2.0,
                "margin": 2.0,
                "reason": "exact published capability description",
            }

        query_tokens = set(
            token for token in TOKEN_RE.findall(normalized)
            if len(token) > 2
        )
        if not query_tokens:
            return None

        scored = []
        for skill_id, profile in self._identity_profiles.items():
            desc = set(profile["description_tokens"])
            names = set(profile["name_tokens"])
            overlap = desc & query_tokens
            if not overlap:
                continue
            weighted_overlap = sum(self._identity_idf.get(token, 1.0) for token in overlap)
            coverage = weighted_overlap / profile["weight"]
            name_hits = len(names & query_tokens) / max(len(names), 1)
            score = coverage + 0.18 * name_hits
            if score > 0:
                scored.append((score, skill_id))

        if not scored:
            return None
        scored.sort(key=lambda row: (-row[0], row[1].casefold()))
        best_score, best_id = scored[0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0
        margin = best_score - second_score
        if best_score < min_score or margin < min_margin:
            return None
        return {
            "id": best_id,
            "score": round(best_score, 6),
            "margin": round(margin, 6),
            "reason": "distinctive capability identity tokens",
        }

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

    def search(self, query: str, limit: int = 10) -> list[dict]:
        terms = [term for term in TOKEN_RE.findall(query.casefold()) if len(term) > 1]
        if not terms:
            return self.list(limit=limit)
        scored: list[tuple[float, SkillRecord]] = []
        for record in self._records.values():
            skill_terms = set(TOKEN_RE.findall((record.id + " " + record.description).casefold()))
            if not skill_terms:
                continue
            exact_name = 3.5 * sum(1 for term in terms if term in record.id.casefold())
            overlap = sum(1 for term in terms if term in skill_terms)
            coverage = overlap / max(len(set(terms)), 1)
            score = exact_name + overlap + coverage * 2.0
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

    def contract_index(
        self,
        *,
        legacy_nodes: dict | None = None,
        graph_generation: str | None = None,
    ) -> ContractIndex:
        self._contract_index.refresh(
            self.records(),
            legacy_nodes=legacy_nodes,
            graph_generation=graph_generation,
        )
        return self._contract_index

    def contract_summary(
        self,
        skill_id: str,
        *,
        legacy_nodes: dict | None = None,
        graph_generation: str | None = None,
    ) -> dict:
        if skill_id not in self._records:
            raise SkillNotFound(skill_id)
        return self.contract_index(
            legacy_nodes=legacy_nodes,
            graph_generation=graph_generation,
        ).get(skill_id)

    def records(self) -> tuple[SkillRecord, ...]:
        return tuple(self._records.values())
