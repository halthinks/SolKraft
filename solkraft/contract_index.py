"""Compact digest-aware contract metadata index.

The index never loads SKILL.md bodies into route results. It fingerprints the
entrypoint, optional sidecar, and legacy graph generation, and only rebuilds
metadata for skills whose fingerprint changed.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path

from .contract_loader import load_skill_contract
from .trust import resolve_trust


def _sha256_json(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _binding_names(items) -> list[str]:
    names = []
    for item in items or []:
        if isinstance(item, dict):
            name = item.get("name")
        elif isinstance(item, str):
            name = item
        else:
            name = None
        if isinstance(name, str) and name:
            names.append(name)
    return names


class ContractIndex:
    """Incrementally index compact contract metadata and inverse selectors."""

    def __init__(self):
        self._entries: dict[str, dict] = {}
        self._fingerprints: dict[str, str] = {}
        self._membership: dict[str, dict[str, set[str]]] = {}
        self._indexes = {
            "effects": defaultdict(set),
            "capabilities": defaultdict(set),
            "inputs": defaultdict(set),
            "outputs": defaultdict(set),
            "trust": defaultdict(set),
        }
        self.generation = 0
        self.last_refresh = {"changed": [], "removed": [], "reused": []}

    @staticmethod
    def _file_signature(path: Path) -> dict | None:
        try:
            stat = path.stat()
        except OSError:
            return None
        return {
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }

    def _fingerprint(self, record, legacy_node: dict | None, graph_generation: str | None) -> str:
        sidecar = record.entrypoint.parent / "contract.yaml"
        value = {
            "skill_id": record.id,
            "name": record.name,
            "entrypoint": self._file_signature(record.entrypoint),
            "contract": self._file_signature(sidecar),
            "legacy_node": legacy_node or {},
            "graph_generation": graph_generation,
        }
        return _sha256_json(value)

    def _remove_membership(self, skill_id: str) -> None:
        membership = self._membership.pop(skill_id, {})
        for index_name, keys in membership.items():
            index = self._indexes[index_name]
            for key in keys:
                index[key].discard(skill_id)
                if not index[key]:
                    del index[key]

    def _add_membership(self, skill_id: str, entry: dict) -> None:
        membership = {
            "effects": set(entry.get("effects") or []),
            "capabilities": set(entry.get("capabilities") or []),
            "inputs": set(_binding_names(entry.get("inputs"))),
            "outputs": set(_binding_names(entry.get("outputs"))),
            "trust": {entry.get("trust", {}).get("state")} if entry.get("trust", {}).get("state") else set(),
        }
        for index_name, keys in membership.items():
            for key in keys:
                self._indexes[index_name][key].add(skill_id)
        self._membership[skill_id] = membership

    def _build_entry(self, record, legacy_node: dict | None) -> dict:
        contract = load_skill_contract(
            record.entrypoint,
            legacy_node=legacy_node,
            expected_skill_id=record.name,
        )
        trust = resolve_trust(record.id, contract)
        return {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "status": contract.get("status"),
            "source": contract.get("source"),
            "schema_version": contract.get("schema_version"),
            "contract_revision": contract.get("contract_revision"),
            "contract_digest": contract.get("contract_digest"),
            "entrypoint_digest": contract.get("entrypoint_digest"),
            "effects": contract.get("side_effects"),
            "capabilities": list(contract.get("capabilities") or []),
            "resources": list(contract.get("resources") or []),
            "auth_scope": contract.get("auth_scope"),
            "test_contract": contract.get("test_contract"),
            "inputs": list(contract.get("inputs") or []),
            "outputs": list(contract.get("outputs") or []),
            "verification": dict(contract.get("verification") or {}),
            "risk": dict(contract.get("risk") or {}),
            "provenance": dict(contract.get("provenance") or {}),
            "trust": trust,
            "validation_errors": list(contract.get("validation_errors") or []),
        }

    def refresh(self, records, *, legacy_nodes=None, graph_generation: str | None = None) -> dict:
        legacy_nodes = legacy_nodes or {}
        current = {record.id: record for record in records}
        changed, reused, removed = [], [], []

        for skill_id in sorted(set(self._entries) - set(current)):
            self._remove_membership(skill_id)
            self._entries.pop(skill_id, None)
            self._fingerprints.pop(skill_id, None)
            removed.append(skill_id)

        for skill_id, record in sorted(current.items()):
            legacy_node = legacy_nodes.get(skill_id)
            fingerprint = self._fingerprint(record, legacy_node, graph_generation)
            if self._fingerprints.get(skill_id) == fingerprint:
                reused.append(skill_id)
                continue
            self._remove_membership(skill_id)
            entry = self._build_entry(record, legacy_node)
            self._entries[skill_id] = entry
            self._fingerprints[skill_id] = fingerprint
            self._add_membership(skill_id, entry)
            changed.append(skill_id)

        if changed or removed:
            self.generation += 1
        self.last_refresh = {"changed": changed, "removed": removed, "reused": reused}
        return {
            "generation": self.generation,
            "count": len(self._entries),
            **self.last_refresh,
        }

    def get(self, skill_id: str) -> dict:
        return dict(self._entries[skill_id])

    def entries(self) -> list[dict]:
        return [dict(self._entries[key]) for key in sorted(self._entries)]

    def filter(
        self,
        *,
        effect: str | None = None,
        capability: str | None = None,
        input_name: str | None = None,
        output_name: str | None = None,
        trust: str | None = None,
    ) -> list[dict]:
        selectors = []
        for index_name, key in (
            ("effects", effect),
            ("capabilities", capability),
            ("inputs", input_name),
            ("outputs", output_name),
            ("trust", trust),
        ):
            if key is not None:
                selectors.append(set(self._indexes[index_name].get(key, set())))
        if not selectors:
            ids = set(self._entries)
        else:
            ids = set.intersection(*selectors) if selectors else set()
        return [dict(self._entries[key]) for key in sorted(ids)]

    def public(self) -> dict:
        return {
            "generation": self.generation,
            "count": len(self._entries),
            "last_refresh": dict(self.last_refresh),
            "indexes": {
                name: {key: sorted(ids) for key, ids in sorted(index.items())}
                for name, index in self._indexes.items()
            },
            "entries": self.entries(),
        }
