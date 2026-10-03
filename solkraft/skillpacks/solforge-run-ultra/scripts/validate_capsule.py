#!/usr/bin/env python3
"""Validate an immutable SolForge Ultra execution capsule using only stdlib."""
from __future__ import annotations
import argparse, hashlib, json, math, os, re, sys
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")
PROVENANCE = re.compile(r"profile=ultra.*execution_boundary=transpose_only")
RISK_CATEGORIES = {
    "destructive_or_irreversible", "external_side_effect", "production_or_deployment",
    "security_or_privileged_access", "credentials_or_sensitive_data", "financial_commitment",
    "legal_medical_financial_reliance", "broad_scope_state_change",
}

class ValidationError(ValueError): pass

def _expect(condition: bool, message: str) -> None:
    if not condition: raise ValidationError(message)

def _keys(obj, required, where):
    _expect(isinstance(obj, dict), f"{where} must be an object")
    _expect(set(obj) == set(required), f"{where} keys mismatch: expected {sorted(required)}")

def _strings(value, where, minimum=0, unique=False):
    _expect(isinstance(value, list) and len(value) >= minimum, f"{where} must be a list with at least {minimum} item(s)")
    _expect(all(isinstance(x, str) and x.strip() for x in value), f"{where} entries must be nonempty strings")
    if unique: _expect(len(value) == len(set(value)), f"{where} entries must be unique")

def canonical_hash(capsule: dict) -> str:
    immutable = {k: v for k, v in capsule.items() if k not in {"capsule_sha256", "confirmation"}}
    raw = json.dumps(immutable, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def requires_confirmation(capsule: dict) -> bool:
    p = capsule["payload"]
    return bool(p["risks"]["high_consequence"] or p["authorization"]["mutation_allowed"] or p["authorization"]["external_side_effects_allowed"])

def validate(c, check_sources=False, require_confirmation=False):
    _keys(c, ["schema_version", "profile", "capsule_id", "payload", "capsule_sha256", "confirmation"], "capsule")
    _expect(c["schema_version"] == "1.0.0", "unsupported schema_version")
    _expect(c["profile"] == "ultra", "profile must be ultra")
    _expect(isinstance(c["capsule_id"], str) and c["capsule_id"].strip(), "capsule_id must be nonempty")
    p = c["payload"]
    pkeys = ["original_request", "structured_intent", "hardened_prompt", "solforge_provenance", "requirements", "scope", "authorization", "risks", "budgets", "retry_limit", "source_artifacts"]
    _keys(p, pkeys, "payload")
    for k in ("original_request", "hardened_prompt", "solforge_provenance"):
        _expect(isinstance(p[k], str) and p[k].strip(), f"payload.{k} must be nonempty")
    _expect(PROVENANCE.search(p["solforge_provenance"]) is not None, "provenance must bind profile=ultra and execution_boundary=transpose_only")
    i = p["structured_intent"]
    _keys(i, ["objective", "inputs", "constraints", "deliverables", "acceptance_criteria", "authorization_boundaries"], "structured_intent")
    _expect(isinstance(i["objective"], str) and i["objective"].strip(), "objective must be nonempty")
    for k in ("inputs", "constraints", "deliverables"): _strings(i[k], f"structured_intent.{k}")
    _strings(i["acceptance_criteria"], "structured_intent.acceptance_criteria", 1)
    _strings(i["authorization_boundaries"], "structured_intent.authorization_boundaries")
    reqs = p["requirements"]
    _expect(isinstance(reqs, list) and reqs, "requirements must be nonempty")
    ids=[]
    for n, r in enumerate(reqs):
        _keys(r, ["id", "text"], f"requirements[{n}]")
        _expect(isinstance(r["id"], str) and re.match(r"^[A-Za-z0-9_.-]+$", r["id"]), f"invalid requirement id at {n}")
        _expect(isinstance(r["text"], str) and r["text"].strip(), f"empty requirement text at {n}"); ids.append(r["id"])
    _expect(len(ids) == len(set(ids)), "requirement ids must be unique")
    s=p["scope"]; _keys(s, ["in_scope", "out_of_scope"], "scope"); _strings(s["in_scope"], "scope.in_scope", 1, True); _strings(s["out_of_scope"], "scope.out_of_scope", 0, True)
    a=p["authorization"]; _keys(a, ["allowed_actions", "prohibited_actions", "allowed_tools", "permission_evidence", "mutation_allowed", "external_side_effects_allowed"], "authorization")
    _strings(a["allowed_actions"], "authorization.allowed_actions", 1, True); _strings(a["prohibited_actions"], "authorization.prohibited_actions", 0, True)
    _strings(a["allowed_tools"], "authorization.allowed_tools", 1, True)
    _expect(isinstance(a["permission_evidence"], list) and a["permission_evidence"], "permission_evidence must be nonempty")
    evidenced=set()
    for n, row in enumerate(a["permission_evidence"]):
        _keys(row, ["permission", "basis", "evidence"], f"permission_evidence[{n}]")
        _expect(isinstance(row["permission"], str) and row["permission"].strip(), "permission must be nonempty")
        _expect(row["basis"] in {"user_explicit", "derived_nonexpansive", "higher_priority_policy"}, "invalid permission basis")
        evidence_sources=[p["original_request"], *i["authorization_boundaries"]]
        _expect(isinstance(row["evidence"], str) and any(row["evidence"] in source for source in evidence_sources), "permission evidence must be an exact request or authorization-boundary substring")
        evidenced.add(row["permission"])
    _expect(set(a["allowed_actions"]) <= evidenced, "every allowed action needs authority evidence")
    _expect(set(a["allowed_tools"]) <= evidenced, "every allowed tool needs authority evidence")
    _expect(not set(a["allowed_actions"]) & set(a["prohibited_actions"]), "an action cannot be both allowed and prohibited")
    _expect(type(a["mutation_allowed"]) is bool and type(a["external_side_effects_allowed"]) is bool, "authorization flags must be boolean")
    if a["mutation_allowed"]: _expect("mutation" in evidenced, "mutation authority needs evidence")
    if a["external_side_effects_allowed"]: _expect("external_side_effect" in evidenced, "external authority needs evidence")
    r=p["risks"]; _keys(r, ["categories", "high_consequence"], "risks"); _strings(r["categories"], "risks.categories", 0, True)
    _expect(set(r["categories"]) <= RISK_CATEGORIES, "unknown risk category"); _expect(type(r["high_consequence"]) is bool, "high_consequence must be boolean")
    if r["categories"]: _expect(r["high_consequence"], "risk categories require high_consequence=true")
    b=p["budgets"]; _keys(b, ["max_elapsed_seconds", "max_tool_calls", "max_rounds", "max_agents", "max_cost_usd"], "budgets")
    _expect(type(b["max_elapsed_seconds"]) in (int,float) and math.isfinite(b["max_elapsed_seconds"]) and b["max_elapsed_seconds"] > 0, "max_elapsed_seconds must be finite and positive")
    _expect(type(b["max_tool_calls"]) is int and b["max_tool_calls"] >= 1, "max_tool_calls must be a positive integer")
    _expect(type(b["max_rounds"]) is int and b["max_rounds"] >= 1, "max_rounds must be positive integer")
    _expect(type(b["max_agents"]) is int and b["max_agents"] >= 2, "max_agents must authorize at least two native Ultra agents")
    _expect(type(b["max_cost_usd"]) in (int,float) and math.isfinite(b["max_cost_usd"]) and b["max_cost_usd"] >= 0, "max_cost_usd must be finite and nonnegative")
    _expect(type(p["retry_limit"]) is int and p["retry_limit"] >= 0, "retry_limit must be nonnegative integer")
    _expect(isinstance(p["source_artifacts"], list), "source_artifacts must be a list")
    seen=set()
    for n, art in enumerate(p["source_artifacts"]):
        _keys(art, ["path", "sha256"], f"source_artifacts[{n}]")
        _expect(isinstance(art["path"], str) and art["path"].strip(), "artifact path must be nonempty")
        _expect(isinstance(art["sha256"], str) and HEX64.match(art["sha256"]), "artifact sha256 invalid")
        _expect(art["path"] not in seen, "duplicate source artifact path"); seen.add(art["path"])
        if check_sources:
            path=Path(os.path.expandvars(os.path.expanduser(art["path"])))
            _expect(path.is_file(), f"source artifact missing: {path}")
            _expect(hashlib.sha256(path.read_bytes()).hexdigest() == art["sha256"], f"source artifact changed: {path}")
    _expect(isinstance(c["capsule_sha256"], str) and HEX64.match(c["capsule_sha256"]), "capsule_sha256 invalid")
    _expect(c["capsule_sha256"] == canonical_hash(c), "capsule hash mismatch (tampering or noncanonical hash)")
    conf=c["confirmation"]
    if conf is not None:
        _keys(conf, ["author", "capsule_sha256", "confirmed", "statement"], "confirmation")
        _expect(conf["author"] == "user" and conf["confirmed"] is True, "confirmation must be user-authored and explicit")
        _expect(conf["capsule_sha256"] == c["capsule_sha256"], "confirmation is not bound to this capsule hash")
        _expect(isinstance(conf["statement"], str) and conf["statement"].strip(), "confirmation statement must be nonempty")
    if require_confirmation and requires_confirmation(c): _expect(conf is not None, "high-risk, mutating, or external work requires hash-bound user confirmation")
    return c

def load_validate(path, check_sources=False, require_confirmation=False):
    try: data=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e: raise ValidationError(f"cannot read capsule: {e}")
    return validate(data, check_sources, require_confirmation)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("capsule"); ap.add_argument("--profile", choices=("ultra",), default="ultra"); ap.add_argument("--check-sources", action="store_true"); ap.add_argument("--require-confirmation", action="store_true"); args=ap.parse_args()
    try: c=load_validate(args.capsule, args.check_sources, args.require_confirmation)
    except ValidationError as e: print(f"ERROR: {e}", file=sys.stderr); return 1
    if c["profile"] != args.profile: print(f"ERROR: profile must be {args.profile}", file=sys.stderr); return 1
    suffix = " (confirmation required before execution)" if requires_confirmation(c) and c["confirmation"] is None else ""
    print(f"PASS: valid SolForge Ultra capsule {c['capsule_sha256']}{suffix}"); return 0

if __name__ == "__main__": raise SystemExit(main())
