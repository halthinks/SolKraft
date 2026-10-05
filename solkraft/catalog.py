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
        self._identity_token_to_skills: dict[str, frozenset[str]] = {}
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
            all_desc_tokens = TOKEN_RE.findall(record.description.casefold())
            profiles[skill_id] = {
                "description_norm": " ".join(record.description.casefold().split()),
                "description_tokens": tuple(desc_tokens),
                "description_set": frozenset(desc_tokens),
                "signature_phrase": " ".join(all_desc_tokens[: min(14, len(all_desc_tokens))]),
                "name_tokens": tuple(name_tokens),
                "name_set": frozenset(name_tokens),
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
            ranked = sorted(
                distinct,
                key=lambda token: (-self._identity_idf.get(token, 1.0), token),
            )
            profile["anchors"] = tuple(ranked[:12])
            profile["anchor_weight"] = (
                sum(self._identity_idf.get(token, 1.0) for token in profile["anchors"])
                or 1.0
            )
        token_to_skills = {}
        for skill_id, token_set in token_sets.items():
            for token in token_set:
                token_to_skills.setdefault(token, set()).add(skill_id)
        self._identity_token_to_skills = {
            token: frozenset(skill_ids)
            for token, skill_ids in token_to_skills.items()
        }
        self._identity_profiles = profiles

    def identity_rank(self, query: str, *, limit: int = 5) -> list[dict]:
        """Rank capability identities using query-centric IDF evidence.

        This is designed for natural-language requests that may mention only
        a few distinctive domain anchors. Scores are relative evidence, not
        probabilities.
        """
        query_tokens = {
            token for token in TOKEN_RE.findall(query.casefold())
            if len(token) > 2
        }
        catalog_tokens = {
            token for token in query_tokens
            if token in self._identity_idf
        }
        if not catalog_tokens:
            return []

        query_weight = sum(self._identity_idf[token] for token in catalog_tokens) or 1.0
        candidate_ids = set()
        for token in catalog_tokens:
            candidate_ids.update(self._identity_token_to_skills.get(token, ()))

        ranked = []
        for skill_id in candidate_ids:
            profile = self._identity_profiles[skill_id]
            desc = profile["description_set"]
            names = profile["name_set"]
            overlap = desc & catalog_tokens
            name_overlap = names & catalog_tokens
            if not overlap and not name_overlap:
                continue

            weighted_overlap = sum(
                self._identity_idf.get(token, 1.0) for token in overlap
            )
            query_precision = weighted_overlap / query_weight
            description_coverage = weighted_overlap / max(profile["weight"], 1.0)
            name_score = len(name_overlap) / max(len(names), 1)
            score = (
                0.72 * query_precision
                + 0.28 * description_coverage
                + 0.12 * name_score
            )
            ranked.append({
                "id": skill_id,
                "score": round(score, 6),
                "query_precision": round(query_precision, 6),
                "description_coverage": round(description_coverage, 6),
                "name_score": round(name_score, 6),
                "matched_tokens": sorted(
                    overlap,
                    key=lambda token: (-self._identity_idf.get(token, 1.0), token),
                ),
            })

        ranked.sort(key=lambda row: (-row["score"], row["id"].casefold()))
        return ranked[:max(1, int(limit))]
    def identity_matches(
        self,
        query: str,
        *,
        min_overlap: int = 3,
        min_weighted_overlap: float = 5.0,
        limit: int = 12,
    ) -> list[dict]:
        """Return multiple high-confidence capability identities in query order.

        This is for compound requests where several distinct capabilities can be
        expressed in one objective. A candidate must match several distinctive
        public-metadata tokens; generic one- or two-token overlaps are ignored.
        Results are ordered by the earliest matched token in the request, then
        by semantic strength.
        """
        normalized = " ".join(query.casefold().split())
        query_sequence = [
            token for token in TOKEN_RE.findall(normalized)
            if len(token) > 2
        ]
        if not query_sequence:
            return []

        query_tokens = set(query_sequence)
        first_position = {}
        for index, token in enumerate(query_sequence):
            first_position.setdefault(token, index)

        candidate_ids = set()
        for token in query_tokens:
            candidate_ids.update(self._identity_token_to_skills.get(token, ()))

        matches = []
        for skill_id in candidate_ids:
            profile = self._identity_profiles[skill_id]
            desc = profile["description_set"]
            names = profile["name_set"]
            overlap = desc & query_tokens
            if len(overlap) < min_overlap:
                continue

            weighted_overlap = sum(
                self._identity_idf.get(token, 1.0)
                for token in overlap
            )
            if weighted_overlap < min_weighted_overlap:
                continue

            coverage = weighted_overlap / profile["weight"]
            name_hits = len(names & query_tokens) / max(len(names), 1)
            score = coverage + 0.18 * name_hits
            earliest = min(first_position[token] for token in overlap)
            matches.append({
                "id": skill_id,
                "score": round(score, 6),
                "overlap": len(overlap),
                "weighted_overlap": round(weighted_overlap, 6),
                "first_token_index": earliest,
                "matched_tokens": sorted(
                    overlap,
                    key=lambda token: (first_position.get(token, 10**9), token),
                ),
                "reason": "compound distinctive capability tokens",
            })

        matches.sort(
            key=lambda row: (
                row["first_token_index"],
                -row["weighted_overlap"],
                -row["score"],
                row["id"].casefold(),
            )
        )
        return matches[:max(limit, 0)]

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

        tokenized_query = " ".join(TOKEN_RE.findall(normalized))
        signature_hits = []
        for skill_id, profile in self._identity_profiles.items():
            signature = profile["signature_phrase"]
            if len(signature.split()) >= 5 and signature in tokenized_query:
                signature_hits.append((len(signature.split()), skill_id))
        if signature_hits:
            signature_hits.sort(key=lambda row: (-row[0], row[1].casefold()))
            longest = signature_hits[0][0]
            winners = [skill_id for size, skill_id in signature_hits if size == longest]
            if len(winners) == 1:
                return {
                    "id": winners[0],
                    "score": 1.8,
                    "margin": 1.8,
                    "reason": "unique published capability signature",
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

            anchors = set(profile.get("anchors") or ())
            anchor_overlap = anchors & query_tokens
            anchor_weight = sum(
                self._identity_idf.get(token, 1.0) for token in anchor_overlap
            )
            anchor_coverage = anchor_weight / profile.get("anchor_weight", 1.0)
            anchor_hits = len(anchor_overlap)

            # Long natural-language requests often express a capability through
            # only a handful of its most distinctive terms. Score those rare
            # anchors directly instead of requiring broad overlap with every
            # word in the published description.
            anchor_signal = 0.0
            if anchor_hits >= 2:
                anchor_signal = anchor_coverage * 1.35 + min(anchor_hits, 5) * 0.055

            score = max(
                coverage + 0.18 * name_hits,
                anchor_signal + 0.08 * name_hits,
            )
            if score > 0:
                scored.append((score, skill_id))

        if not scored:
            return None
        scored.sort(key=lambda row: (-row[0], row[1].casefold()))
        best_score, best_id = scored[0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0
        margin = best_score - second_score
        best_profile = self._identity_profiles[best_id]
        best_anchor_hits = len(set(best_profile.get("anchors") or ()) & query_tokens)
        adaptive_min = min_score
        adaptive_margin = min_margin
        if best_anchor_hits >= 4:
            adaptive_min = min(adaptive_min, 0.42)
            adaptive_margin = min(adaptive_margin, 0.055)
        elif best_anchor_hits >= 3:
            adaptive_min = min(adaptive_min, 0.48)
            adaptive_margin = min(adaptive_margin, 0.065)
        if best_score < adaptive_min or margin < adaptive_margin:
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
