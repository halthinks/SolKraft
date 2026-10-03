#!/usr/bin/env python3
"""Maintain and constrain an InForge Ultra execution ledger."""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from validate_capsule import ValidationError, load_validate, requires_confirmation

TRANSITIONS = {
 "preflight":{"awaiting_confirmation","ready","blocked","declined","terminated"},
 "awaiting_confirmation":{"ready","blocked","declined","terminated"},
 "ready":{"executing","blocked","declined","terminated"},
 "executing":{"verifying","blocked","declined","terminated"},
 "verifying":{"executing","adversarial_audit","blocked","declined","terminated"},
 "adversarial_audit":{"executing","verifying","blocked","declined","terminated"},
 "complete":set(), "blocked":set(), "declined":set(), "terminated":set(),
}
APPROACH_STATUSES={"candidate","active","blocked","falsified","superseded","integrated","accepted"}

def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,data):
    tmp=Path(str(path)+".tmp"); tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(tmp,path)
def fail(msg): print(f"ERROR: {msg}",file=sys.stderr); return 1
def get(capsule,state_path):
    c=load_validate(capsule); s=read(state_path)
    if s.get("capsule_sha256") != c["capsule_sha256"]: raise ValidationError("state is bound to a different capsule")
    return c,s
def event(s,kind,detail): s["events"].append({"sequence":len(s["events"])+1,"kind":kind,"detail":detail})
def over(c,s):
    b=c["payload"]["budgets"]; u=s["usage"]
    checks={"elapsed_seconds":b["max_elapsed_seconds"],"tool_calls":b["max_tool_calls"],"rounds":b["max_rounds"],"agents":b["max_agents"],"cost_usd":b["max_cost_usd"]}
    return [k for k,m in checks.items() if u[k] > m] + (["retries"] if u["retries"] > c["payload"]["retry_limit"] else [])
def contained(target, roots):
    t=os.path.normcase(os.path.abspath(os.path.expanduser(target)))
    for root in roots:
        r=os.path.normcase(os.path.abspath(os.path.expanduser(root)))
        try:
            if os.path.commonpath([t,r]) == r: return True
        except ValueError: pass
        if target == root or target.startswith(root.rstrip("/")+"/"): return True
    return False

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("init"); p.add_argument("capsule"); p.add_argument("state")
    p=sub.add_parser("transition"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("to"); p.add_argument("--reason",default="")
    p=sub.add_parser("approach"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("id"); p.add_argument("family"); p.add_argument("status",choices=sorted(APPROACH_STATUSES)); p.add_argument("--hypothesis",default=""); p.add_argument("--evidence",default=""); p.add_argument("--blocker",default="")
    p=sub.add_parser("action"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("action_id"); p.add_argument("kind"); p.add_argument("target"); p.add_argument("--requirement-id",action="append",required=True); p.add_argument("--tool",required=True); p.add_argument("--expected",required=True); p.add_argument("--actual",required=True); p.add_argument("--evidence",required=True); p.add_argument("--rollback",default="not_applicable"); p.add_argument("--mutation",action="store_true"); p.add_argument("--external",action="store_true"); p.add_argument("--elapsed",type=float,default=0); p.add_argument("--tools",type=int,default=1); p.add_argument("--rounds",type=int,default=0); p.add_argument("--agents",type=int,default=1); p.add_argument("--cost",type=float,default=0); p.add_argument("--retry",action="store_true")
    p=sub.add_parser("evidence"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("requirement_id"); p.add_argument("locator"); p.add_argument("method"); p.add_argument("result",choices=["passed","failed","blocked"])
    args=ap.parse_args()
    try:
        if args.cmd=="init":
            c=load_validate(args.capsule); status="awaiting_confirmation" if requires_confirmation(c) and c["confirmation"] is None else "preflight"
            s={"schema_version":"1.0.0","capsule_sha256":c["capsule_sha256"],"status":status,"created_unix":int(time.time()),"usage":{"elapsed_seconds":0,"tool_calls":0,"rounds":0,"agents":1,"cost_usd":0,"retries":0},"approaches":{},"actions":[],"evidence":{r["id"]:[] for r in c["payload"]["requirements"]},"violations":[],"events":[],"audit_receipt":None}
            event(s,"initialized",status); write(args.state,s); print(f"PASS: initialized {status}"); return 0
        c,s=get(args.capsule,args.state)
        if args.cmd=="transition":
            if args.to=="complete": return fail("complete is reserved for acceptance_audit.py --complete")
            if args.to not in TRANSITIONS.get(s["status"],set()): return fail(f"invalid transition {s['status']} -> {args.to}")
            if args.to=="ready":
                load_validate(args.capsule, require_confirmation=True)
                if s["status"] not in {"preflight","awaiting_confirmation"}: return fail("ready requires preflight")
            if args.to in {"blocked","declined","terminated"} and not args.reason.strip(): return fail("terminal transition requires a reason")
            old=s["status"]; s["status"]=args.to; event(s,"transition",{"from":old,"to":args.to,"reason":args.reason}); write(args.state,s); print(f"PASS: {old} -> {args.to}"); return 0
        if s["status"] in {"complete","blocked","declined","terminated"}: return fail("terminal state is immutable")
        if args.cmd=="approach":
            s["approaches"][args.id]={"family":args.family,"status":args.status,"hypothesis":args.hypothesis,"evidence":args.evidence,"blocker":args.blocker}; event(s,"approach",args.id); write(args.state,s); print("PASS: approach recorded"); return 0
        if args.cmd=="action":
            if s["status"] != "executing": return fail("actions require executing state")
            load_validate(args.capsule, require_confirmation=True)
            a=c["payload"]["authorization"]; sc=c["payload"]["scope"]
            violations=[]
            valid_requirement_ids={r["id"] for r in c["payload"]["requirements"]}
            if any(rid not in valid_requirement_ids for rid in args.requirement_id): violations.append("unknown requirement id")
            if args.kind not in a["allowed_actions"] or args.kind in a["prohibited_actions"]: violations.append("unauthorized action kind")
            if args.tool not in a["allowed_tools"]: violations.append("unauthorized tool")
            if not contained(args.target,sc["in_scope"]) or contained(args.target,sc["out_of_scope"]): violations.append("target outside authorized scope")
            if args.mutation and not a["mutation_allowed"]: violations.append("mutation not authorized")
            if args.external and not a["external_side_effects_allowed"]: violations.append("external effect not authorized")
            if (args.mutation or args.external) and (not args.rollback.strip() or args.rollback == "not_applicable"): violations.append("mutation/external action requires rollback or recovery evidence")
            if min(args.elapsed,args.tools,args.rounds,args.agents,args.cost) < 0: violations.append("usage increments cannot be negative")
            if args.agents < 1: violations.append("execution must use at least one verified agent")
            if args.retry and not any(x.get("status") in {"blocked","falsified"} and (x.get("hypothesis") or x.get("blocker")) for x in s["approaches"].values()): violations.append("retry requires a recorded blocked/falsified approach and new mechanism")
            proposed=dict(s["usage"]); proposed["elapsed_seconds"]+=args.elapsed; proposed["tool_calls"]+=args.tools; proposed["rounds"]+=args.rounds; proposed["agents"]=max(proposed["agents"],args.agents); proposed["cost_usd"]+=args.cost; proposed["retries"]+=int(args.retry)
            old=s["usage"]; s["usage"]=proposed; exceeded=over(c,s); s["usage"]=old
            if exceeded: violations.append("budget exceeded: "+", ".join(exceeded))
            if violations:
                s["violations"].append({"action_id":args.action_id,"violations":violations}); event(s,"action_rejected",args.action_id); write(args.state,s); return fail("; ".join(violations))
            s["usage"]=proposed; s["actions"].append({"id":args.action_id,"requirement_ids":args.requirement_id,"kind":args.kind,"target":args.target,"tool":args.tool,"mutation":args.mutation,"external":args.external,"expected":args.expected,"actual":args.actual,"evidence":args.evidence,"rollback":args.rollback,"status":"closed"}); event(s,"action",args.action_id); write(args.state,s); print("PASS: action recorded within authority and budgets"); return 0
        if args.cmd=="evidence":
            if args.requirement_id not in s["evidence"]: return fail("unknown requirement id")
            if not args.locator.strip() or not args.method.strip(): return fail("evidence locator and method must be nonempty")
            s["evidence"][args.requirement_id].append({"locator":args.locator,"method":args.method,"result":args.result}); event(s,"evidence",args.requirement_id); write(args.state,s); print("PASS: evidence recorded"); return 0
    except (ValidationError,OSError,json.JSONDecodeError) as e: return fail(str(e))

if __name__=="__main__": raise SystemExit(main())
