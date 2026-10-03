import json, sys
from pathlib import Path

REQ={"selection_id","product","profile","revision","selected_mpn","manufacturer","role","state","requirements","selection_reason","candidates","evidence","constraints","validation_gates","evidence_maturity","claim_ceiling","electronic_budgets","worst_case_margin"}
STATES={"SELECTED","CONDITIONAL","BLOCKED"}

def main(path):
    d=json.loads(Path(path).read_text(encoding="utf-8")); errors=[]
    miss=sorted(REQ-set(d));
    if miss: errors.append("missing: "+", ".join(miss))
    if d.get("state") not in STATES: errors.append("invalid selection state")
    candidates=d.get("candidates",[])
    if len(candidates)<2: errors.append("at least two candidates are required")
    for i,c in enumerate(candidates):
        for key in ("manufacturer","mpn","disposition","reason","evidence"):
            if not c.get(key): errors.append(f"candidate {i} missing {key}")
    if d.get("state")=="SELECTED" and d.get("validation_gates"):
        unresolved=[g for g in d["validation_gates"] if g.get("status")!="PASS"]
        if unresolved: errors.append("SELECTED has unresolved validation gates; use CONDITIONAL")
    budgets=d.get("electronic_budgets",{})
    applicable=d.get("applicable_electronic_domains",[])
    for domain in applicable:
        item=budgets.get(domain)
        if not item: errors.append(f"missing applicable electronic budget: {domain}")
        elif not all(k in item for k in ("requirements","worst_case","margin","evidence","validation_method")):
            errors.append(f"electronic budget {domain} lacks requirements/worst_case/margin/evidence/validation_method")
    if errors: print("FAIL\n"+"\n".join(errors)); return 1
    print(f"PASS: {d['selection_id']} with {len(candidates)} compared candidates")
    return 0
if __name__=="__main__": raise SystemExit(main(sys.argv[1]))
