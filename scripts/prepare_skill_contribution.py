"""Prepare semantic proof coverage for a newly contributed skill."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, catalog_graph, contract_index
from scripts.semantic_router_benchmark import build_profiles, assign_exact_recall_anchor_sets, shared_anchor_skills

ROOT=Path(__file__).resolve().parents[1]

def plan(manifest: Path):
    data=json.loads(manifest.read_text(encoding="utf-8")); skill=data.get("skill")
    if not skill: raise SystemExit(f"{manifest}: missing skill")
    catalog=SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records=list(catalog.records()); by_id={r.id:r for r in records}
    if skill not in by_id: raise SystemExit(f"{skill}: production catalog does not see the contributed skill")
    graph=catalog_graph(catalog); index=contract_index(catalog)
    entries={e["id"]:e for e in index.entries()}; profiles=build_profiles(records,graph)
    unique=assign_exact_recall_anchor_sets(records,graph,entries,profiles).get(skill)
    shared={a:shared_anchor_skills(profiles,a) for a in profiles[skill]["anchors"]}
    shared={a:v for a,v in shared.items() if len(v)>1}
    return {"schema":"solkraft/skill-proof-plan/v1","skill":skill,"catalog_skill_count":len(records),
      "exact_recall_anchor_set":list(unique) if unique else None,
      "proof_mode":"exact-recall" if unique else "ambiguity","shared_anchor_neighbors":shared,
      "generated_corpus":{"single_prompts_per_skill":1000,"composition_cases":100000,
      "stability_executions":100000,"explicit_skill_ids_injected":False}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("manifest",type=Path)
    ap.add_argument("--output",type=Path,default=ROOT/"build"/"skill-proof-plan.json"); a=ap.parse_args()
    manifest=a.manifest if a.manifest.is_absolute() else ROOT/a.manifest
    payload=plan(manifest); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(payload,separators=(",",":")))
if __name__=="__main__": main()
