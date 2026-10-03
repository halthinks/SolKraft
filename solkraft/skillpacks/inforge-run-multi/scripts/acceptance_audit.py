#!/usr/bin/env python3
"""Perform the sole completion gate for InForge Run Single."""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from validate_capsule import ValidationError, load_validate, requires_confirmation

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("capsule"); ap.add_argument("state"); ap.add_argument("--complete",action="store_true"); args=ap.parse_args()
    try:
        c=load_validate(args.capsule,require_confirmation=True); p=Path(args.state); s=json.loads(p.read_text(encoding="utf-8"))
        errors=[]
        if s.get("capsule_sha256") != c["capsule_sha256"]: errors.append("state/capsule hash mismatch")
        if s.get("status") != "adversarial_audit": errors.append("state must be adversarial_audit")
        u=s.get("usage",{}); b=c["payload"]["budgets"]
        for k,m in (("elapsed_seconds",b["max_elapsed_seconds"]),("tool_calls",b["max_tool_calls"]),("rounds",b["max_rounds"]),("agents",b["max_agents"]),("cost_usd",b["max_cost_usd"]),("retries",c["payload"]["retry_limit"])):
            if u.get(k,0) > m: errors.append(f"budget exceeded: {k}")
        if u.get("agents",0) < 2: errors.append("Multi audit requires evidence of at least two real agents")
        if s.get("violations"): errors.append("execution ledger contains rejected authority/scope/budget actions")
        if any(a.get("status") != "closed" for a in s.get("actions",[])): errors.append("open action remains")
        approaches=s.get("approaches",{})
        if not approaches: errors.append("approach registry is empty")
        elif not any(a.get("status") in {"accepted","integrated"} for a in approaches.values()): errors.append("no approach was accepted or integrated")
        expected={r["id"] for r in c["payload"]["requirements"]}; actual=set(s.get("evidence",{}))
        if actual != expected: errors.append("evidence requirement set mismatch")
        for rid in sorted(expected):
            records=s.get("evidence",{}).get(rid,[])
            if not any(x.get("result")=="passed" and str(x.get("locator","")).strip() and str(x.get("method","")).strip() for x in records): errors.append(f"missing passed evidence for {rid}")
        if requires_confirmation(c) and c["confirmation"] is None: errors.append("required confirmation absent")
        if errors:
            for e in errors: print(f"ERROR: {e}",file=sys.stderr)
            return 1
        print(f"PASS: all {len(expected)} requirements have accepted evidence; authority and budgets clean")
        if args.complete:
            pre=digest({k:v for k,v in s.items() if k!="audit_receipt"})
            s["audit_receipt"]={"result":"passed","capsule_sha256":c["capsule_sha256"],"precompletion_state_sha256":pre,"requirement_ids":sorted(expected)}
            s["status"]="complete"; s["events"].append({"sequence":len(s["events"])+1,"kind":"acceptance_complete","detail":c["capsule_sha256"]})
            tmp=Path(str(p)+".tmp"); tmp.write_text(json.dumps(s,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(tmp,p)
            print("PASS: terminal state complete")
        return 0
    except (ValidationError,OSError,json.JSONDecodeError) as e: print(f"ERROR: {e}",file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
