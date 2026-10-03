#!/usr/bin/env python3
"""Deterministic positive and negative tests for SolForge Run Single."""
from __future__ import annotations
import copy, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from validate_capsule import canonical_hash

HERE=Path(__file__).parent; PY=sys.executable
def capsule(high=False):
    c={"schema_version":"1.0.0","profile":"single","capsule_id":"selftest","payload":{
      "original_request":"Inspect the fixture with filesystem tools and report the result; mutation is authorized when explicitly confirmed.",
      "structured_intent":{"objective":"Inspect fixture","inputs":[],"constraints":["read only"],"deliverables":["report"],"acceptance_criteria":["inspection evidenced"],"authorization_boundaries":["Filesystem reading is a nonexpansive implementation detail."]},
      "hardened_prompt":"Inspect the fixture and report only verified results.",
      "solforge_provenance":"profile=single; control_version=3.0.0; execution_boundary=transpose_only",
      "requirements":[{"id":"REQ-1","text":"Inspect fixture"}],
      "scope":{"in_scope":["fixture"],"out_of_scope":["fixture/private"]},
      "authorization":{"allowed_actions":["read"],"prohibited_actions":["delete"],"allowed_tools":["filesystem"],"permission_evidence":[{"permission":"read","basis":"user_explicit","evidence":"Inspect"},{"permission":"filesystem","basis":"derived_nonexpansive","evidence":"Filesystem reading"}]+([{"permission":"mutation","basis":"user_explicit","evidence":"mutation is authorized"}] if high else []),"mutation_allowed":high,"external_side_effects_allowed":False},
      "risks":{"categories":["broad_scope_state_change"] if high else [],"high_consequence":high},
      "budgets":{"max_elapsed_seconds":60,"max_tool_calls":3,"max_rounds":2,"max_agents":1,"max_cost_usd":1},
      "retry_limit":1,"source_artifacts":[]},"capsule_sha256":"0"*64,"confirmation":None}
    c["capsule_sha256"]=canonical_hash(c)
    if high: c["confirmation"]={"author":"user","capsule_sha256":c["capsule_sha256"],"confirmed":True,"statement":"I confirm this exact capsule."}
    return c
def run(*args,ok=True):
    r=subprocess.run([PY,*map(str,args)],text=True,capture_output=True)
    if (r.returncode==0)!=ok: raise AssertionError(f"unexpected rc={r.returncode}: {' '.join(map(str,args))}\n{r.stdout}{r.stderr}")
    return (r.stdout+r.stderr).strip()
def save(path,obj): path.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
def main():
  tests=[]
  with tempfile.TemporaryDirectory() as td:
    d=Path(td); cap=d/"cap.json"; state=d/"state.json"; save(cap,capsule())
    run(HERE/"validate_capsule.py",cap); run(HERE/"execution_state.py","init",cap,state)
    run(HERE/"execution_state.py","transition",cap,state,"ready"); run(HERE/"execution_state.py","transition",cap,state,"executing")
    run(HERE/"execution_state.py","approach",cap,state,"A1","direct","accepted","--hypothesis","read and inspect")
    run(HERE/"execution_state.py","action",cap,state,"X1","read","fixture/file.txt","--requirement-id","REQ-1","--tool","filesystem","--expected","inspect fixture","--actual","observed","--evidence","fixture/file.txt","--tools","1","--rounds","1","--agents","1")
    run(HERE/"execution_state.py","evidence",cap,state,"REQ-1","fixture/file.txt","direct inspection","passed")
    run(HERE/"execution_state.py","transition",cap,state,"verifying"); run(HERE/"execution_state.py","transition",cap,state,"adversarial_audit")
    run(HERE/"acceptance_audit.py",cap,state,"--complete"); assert json.loads(state.read_text())["status"]=="complete"; tests.append("positive completion")

    pause_cap=d/"pause.json"; pause_state=d/"pause.state"; checkpoint=d/"checkpoint.json"
    save(pause_cap,capsule()); save(checkpoint,{"completed_ids":["T1"],"status":"paused"})
    run(HERE/"execution_state.py","init",pause_cap,pause_state)
    run(HERE/"execution_state.py","transition",pause_cap,pause_state,"ready")
    run(HERE/"execution_state.py","transition",pause_cap,pause_state,"executing")
    run(HERE/"execution_state.py","pause",pause_cap,pause_state,"--reason","operator requested safe pause","--checkpoint",checkpoint)
    paused=json.loads(pause_state.read_text()); assert paused["status"]=="paused" and paused["pause"]["checkpoint_sha256"]
    run(HERE/"execution_state.py","action",pause_cap,pause_state,"PX","read","fixture","--requirement-id","REQ-1","--tool","filesystem","--expected","x","--actual","x","--evidence","x",ok=False)
    run(HERE/"execution_state.py","resume",pause_cap,pause_state,"--reason","checkpoint verified")
    assert json.loads(pause_state.read_text())["status"]=="executing"; tests.append("safe pause and resume")

    tamper_cap=d/"pause-tamper.json"; tamper_state=d/"pause-tamper.state"; tamper_checkpoint=d/"tamper-checkpoint.json"
    save(tamper_cap,capsule()); save(tamper_checkpoint,{"completed_ids":["T1"]})
    run(HERE/"execution_state.py","init",tamper_cap,tamper_state); run(HERE/"execution_state.py","transition",tamper_cap,tamper_state,"ready"); run(HERE/"execution_state.py","transition",tamper_cap,tamper_state,"executing")
    run(HERE/"execution_state.py","pause",tamper_cap,tamper_state,"--reason","outage","--checkpoint",tamper_checkpoint)
    save(tamper_checkpoint,{"completed_ids":["T1","T2"]})
    run(HERE/"execution_state.py","resume",tamper_cap,tamper_state,"--reason","unsafe changed checkpoint",ok=False)
    run(HERE/"execution_state.py","rebind-pause",tamper_cap,tamper_state,"--reason","replacement checkpoint independently revalidated","--checkpoint",tamper_checkpoint)
    run(HERE/"execution_state.py","resume",tamper_cap,tamper_state,"--reason","rebound checkpoint verified")
    rebound=json.loads(tamper_state.read_text()); assert rebound["status"]=="executing" and rebound["pause"]["rebind_history"]
    tests.append("changed checkpoint rejection and paused rebind")

    bad=copy.deepcopy(capsule()); bad["payload"]["original_request"]="tampered"; save(d/"tampered.json",bad); run(HERE/"validate_capsule.py",d/"tampered.json",ok=False); tests.append("tamper rejection")
    bad=capsule(); bad["profile"]="multi"; bad["capsule_sha256"]=canonical_hash(bad); save(d/"profile.json",bad); run(HERE/"validate_capsule.py",d/"profile.json",ok=False); tests.append("profile rejection")
    bad=capsule(); bad["payload"]["budgets"]["max_agents"]=2; bad["capsule_sha256"]=canonical_hash(bad); save(d/"agents.json",bad); run(HERE/"validate_capsule.py",d/"agents.json",ok=False); tests.append("imaginary-agent rejection")
    high=capsule(True); high["confirmation"]=None; save(d/"unconfirmed.json",high); run(HERE/"validate_capsule.py",d/"unconfirmed.json"); run(HERE/"validate_capsule.py",d/"unconfirmed.json","--require-confirmation",ok=False); tests.append("confirmation gate")
    save(d/"scope.json",capsule()); run(HERE/"execution_state.py","init",d/"scope.json",d/"scope.state"); run(HERE/"execution_state.py","transition",d/"scope.json",d/"scope.state","ready"); run(HERE/"execution_state.py","transition",d/"scope.json",d/"scope.state","executing"); run(HERE/"execution_state.py","action",d/"scope.json",d/"scope.state","X","read","elsewhere","--requirement-id","REQ-1","--tool","filesystem","--expected","x","--actual","no","--evidence","none",ok=False); tests.append("scope expansion rejection")
    save(d/"budget.json",capsule()); run(HERE/"execution_state.py","init",d/"budget.json",d/"budget.state"); run(HERE/"execution_state.py","transition",d/"budget.json",d/"budget.state","ready"); run(HERE/"execution_state.py","transition",d/"budget.json",d/"budget.state","executing"); run(HERE/"execution_state.py","action",d/"budget.json",d/"budget.state","X","read","fixture","--requirement-id","REQ-1","--tool","filesystem","--expected","x","--actual","no","--evidence","none","--tools","4",ok=False); tests.append("budget rejection")
    save(d/"missing.json",capsule()); run(HERE/"execution_state.py","init",d/"missing.json",d/"missing.state"); run(HERE/"execution_state.py","transition",d/"missing.json",d/"missing.state","ready"); run(HERE/"execution_state.py","transition",d/"missing.json",d/"missing.state","executing"); run(HERE/"execution_state.py","approach",d/"missing.json",d/"missing.state","A","direct","accepted"); run(HERE/"execution_state.py","transition",d/"missing.json",d/"missing.state","verifying"); run(HERE/"execution_state.py","transition",d/"missing.json",d/"missing.state","adversarial_audit"); run(HERE/"acceptance_audit.py",d/"missing.json",d/"missing.state","--complete",ok=False); tests.append("missing-evidence rejection")
  print(f"PASS: {len(tests)}/{len(tests)} selftests: "+", ".join(tests)); return 0
if __name__=="__main__": raise SystemExit(main())
