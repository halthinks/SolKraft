#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

PASSES = ["blockout", "structural-pass", "form-refinement", "material-pass", "surface-pass", "lighting-pass", "interaction-pass", "optimization-pass"]
CHANNELS = {"wetting", "saturation", "drainage", "drying", "freezing_thawing", "corrosion", "rot", "swelling", "warping", "electrical_ingress", "chemical_contamination", "radiological_contamination", "mud_dust", "heat_fire", "immersion"}
DERIVED = {"mass", "center_of_mass", "friction", "strength", "insulation", "conductivity", "noise", "visibility", "operation", "repair", "salvage"}
HASH = re.compile(r"^[a-f0-9]{64}$")

def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"schema_version","job_id","request","route","sources","environmental_response","img2threejs","blender","unreal","lineage","final"}
    missing = required - d.keys()
    if missing: fail(f"missing top-level keys: {sorted(missing)}")
    for s in d["sources"]:
        for k in ("provider","source_id","license","allowed_use","content_sha256","quarantine_status","security_disposition"):
            if not s.get(k): fail(f"source missing {k}")
        if not HASH.match(s["content_sha256"]): fail("invalid source hash")
        if s["quarantine_status"] != "cleared" and d["final"]["status"] == "accepted": fail("accepted job has uncleared source")
    env = d["environmental_response"]
    names = {c.get("name") for c in env.get("channels", [])}
    if names != CHANNELS: fail(f"environment channels mismatch: missing={sorted(CHANNELS-names)} extra={sorted(names-CHANNELS)}")
    if not DERIVED.issubset(env.get("derived_properties", {}).keys()): fail("missing derived environmental properties")
    for c in env["channels"]:
        if c.get("applicability") == "applicable" and (not c.get("response") or not c.get("validation")): fail(f"applicable channel lacks response/validation: {c['name']}")
    img = d["img2threejs"]
    if d["route"] == "img2threejs_then_blender":
        if not img.get("applicable") or img.get("strict_gate") != "passed" or not img.get("accepted"): fail("img2threejs route not accepted")
        if [p.get("name") for p in img.get("passes", [])] != PASSES: fail("img2threejs locked pass order incomplete")
        for p in img["passes"]:
            if not HASH.match(p.get("render_sha256", "")) or not HASH.match(p.get("comparison_sha256", "")): fail("img2threejs pass evidence hash invalid")
    final = d["final"]["status"]
    if final == "accepted":
        if not d["blender"].get("accepted") or d["blender"].get("status") != "passed": fail("accepted job lacks Blender pass")
        if not d["unreal"].get("accepted") or d["unreal"].get("status") != "passed": fail("accepted job lacks Unreal pass")
        for k in ("pie_evidence","multiplayer_evidence","persistence_evidence","performance_evidence"):
            if not d["unreal"].get(k): fail(f"accepted job lacks {k}")
    print(f"PASS: {d['job_id']} is structurally and semantically valid ({final})")

if __name__ == "__main__":
    if len(sys.argv) != 2: fail("usage: validate_asset_factory_job.py JOB.json")
    main(sys.argv[1])
