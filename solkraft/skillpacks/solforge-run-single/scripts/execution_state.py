#!/usr/bin/env python3
"""Maintain and constrain a SolForge Single execution ledger."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
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
 "paused":{"blocked","declined","terminated"}, "complete":set(), "blocked":set(), "declined":set(), "terminated":set(),
}
APPROACH_STATUSES={"candidate","active","blocked","falsified","superseded","integrated","accepted"}

def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,data):
    tmp=Path(str(path)+".tmp"); tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(tmp,path)
def fail(msg): print(f"ERROR: {msg}",file=sys.stderr); return 1
def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
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
    p=sub.add_parser("pause"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("--reason",required=True); p.add_argument("--checkpoint",required=True)
    p=sub.add_parser("resume"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("--reason",required=True)
    p=sub.add_parser("rebind-pause"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("--reason",required=True); p.add_argument("--checkpoint",required=True)
    p=sub.add_parser("approach"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("id"); p.add_argument("family"); p.add_argument("status",choices=sorted(APPROACH_STATUSES)); p.add_argument("--hypothesis",default=""); p.add_argument("--evidence",default=""); p.add_argument("--blocker",default="")
    p=sub.add_parser("action"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("action_id"); p.add_argument("kind"); p.add_argument("target"); p.add_argument("--requirement-id",action="append",required=True); p.add_argument("--tool",required=True); p.add_argument("--expected",required=True); p.add_argument("--actual",required=True); p.add_argument("--evidence",required=True); p.add_argument("--rollback",default="not_applicable"); p.add_argument("--mutation",action="store_true"); p.add_argument("--external",action="store_true"); p.add_argument("--elapsed",type=float,default=0); p.add_argument("--tools",type=int,default=1); p.add_argument("--rounds",type=int,default=0); p.add_argument("--agents",type=int,default=1); p.add_argument("--cost",type=float,default=0); p.add_argument("--retry",action="store_true")
    p=sub.add_parser("evidence"); p.add_argument("capsule"); p.add_argument("state"); p.add_argument("requirement_id"); p.add_argument("locator"); p.add_argument("method"); p.add_argument("result",choices=["passed","failed","blocked"])
    args=ap.parse_args()
    try:
        if args.cmd=="init":
            c=load_validate(args.capsule); status="awaiting_confirmation" if requires_confirmation(c) and c["confirmation"] is None else "preflight"
            s={"schema_version":"1.1.0","capsule_sha256":c["capsule_sha256"],"status":status,"created_unix":int(time.time()),"usage":{"elapsed_seconds":0,"tool_calls":0,"rounds":0,"agents":1,"cost_usd":0,"retries":0},"approaches":{},"actions":[],"evidence":{r["id"]:[] for r in c["payload"]["requirements"]},"violations":[],"events":[],"pause":None,"audit_receipt":None}
            event(s,"initialized",status); write(args.state,s); print(f"PASS: initialized {status}"); return 0
        c,s=get(args.capsule,args.state)
        if args.cmd=="pause":
            if s["status"] in {"complete","blocked","declined","terminated"}: return fail("terminal state is immutable")
            if s["status"]=="paused": print("PASS: already paused"); return 0
            if s["status"] not in {"ready","executing","verifying","adversarial_audit"}: return fail(f"cannot pause from {s['status']}")
            if any(a.get("status") not in {"closed","interrupted_recovered"} for a in s.get("actions",[])): return fail("safe pause requires no open or unrecovered action")
            checkpoint=Path(args.checkpoint).resolve()
            if not checkpoint.is_file(): return fail("pause checkpoint must be an existing file")
            old=s["status"]
            s["pause"]={"resume_status":old,"reason":args.reason,"checkpoint_path":str(checkpoint),"checkpoint_sha256":sha256_file(checkpoint),"paused_unix":int(time.time())}
            s["status"]="paused"; event(s,"paused",s["pause"]); write(args.state,s); print(f"PASS: {old} -> paused"); return 0
        if args.cmd=="resume":
            if s["status"]!="paused": return fail("resume requires paused state")
            pause=s.get("pause") or {}; checkpoint=Path(str(pause.get("checkpoint_path","")))
            if not checkpoint.is_file() or sha256_file(checkpoint)!=pause.get("checkpoint_sha256"): return fail("pause checkpoint missing or changed; revalidate before resume")
            load_validate(args.capsule,check_sources=True,require_confirmation=True)
            target=pause.get("resume_status")
            if target not in {"ready","executing","verifying","adversarial_audit"}: return fail("invalid recorded resume state")
            s["status"]=target; pause["resumed_unix"]=int(time.time()); pause["resume_reason"]=args.reason
            event(s,"resumed",{"to":target,"reason":args.reason,"checkpoint_sha256":pause["checkpoint_sha256"]}); write(args.state,s); print(f"PASS: paused -> {target}"); return 0
        if args.cmd=="rebind-pause":
            if s["status"]!="paused": return fail("rebind-pause requires paused state")
            load_validate(args.capsule,check_sources=True,require_confirmation=True)
            checkpoint=Path(args.checkpoint).resolve()
            if not checkpoint.is_file(): return fail("replacement pause checkpoint must be an existing file")
            pause=s.get("pause") or {}; old_hash=pause.get("checkpoint_sha256"); new_hash=sha256_file(checkpoint)
            history=pause.setdefault("rebind_history",[])
            history.append({"old_checkpoint_sha256":old_hash,"new_checkpoint_sha256":new_hash,"reason":args.reason,"rebound_unix":int(time.time())})
            pause["checkpoint_path"]=str(checkpoint); pause["checkpoint_sha256"]=new_hash; pause["reason"]=args.reason
            s["pause"]=pause; event(s,"pause_rebound",history[-1]); write(args.state,s); print("PASS: paused checkpoint rebound"); return 0
        if args.cmd=="transition":
            if args.to=="complete": return fail("complete is reserved for acceptance_audit.py --complete")
            if args.to not in TRANSITIONS.get(s["status"],set()): return fail(f"invalid transition {s['status']} -> {args.to}")
            if args.to=="ready":
                load_validate(args.capsule, require_confirmation=True)
                if s["status"] not in {"preflight","awaiting_confirmation"}: return fail("ready requires preflight")
            if args.to in {"blocked","declined","terminated"} and not args.reason.strip(): return fail("terminal transition requires a reason")
            old=s["status"]; s["status"]=args.to; event(s,"transition",{"from":old,"to":args.to,"reason":args.reason}); write(args.state,s); print(f"PASS: {old} -> {args.to}"); return 0
        if s["status"] in {"complete","blocked","declined","terminated"}: return fail("terminal state is immutable")
        if s["status"]=="paused": return fail("paused state accepts only resume or terminal transition")
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
            if args.agents != 1: violations.append("Single execution must use exactly one agent")
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
