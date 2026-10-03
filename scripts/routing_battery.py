"""Exercise ten broadly useful domains on 100,000 long requests."""
from __future__ import annotations
import importlib.util, json, re
from pathlib import Path

from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request
CATALOG = SkillCatalog([BUNDLE_ROOT])
class ComposerAdapter:
    @staticmethod
    def compose_route(graph, objective, max_skills=50):
        return route_request(CATALOG, objective, max_skills)
composer = ComposerAdapter()
GRAPH = None

P = {
 "data_decision": (["data-validate", "data-analyze", "data-visualize"], ["validate the dataset quality", "analyze the data decision metrics", "create an evidence-linked decision chart"]),
 "mathematics": (["math-literature", "math-prove", "math-counterexample", "math-compute", "math-solve", "math-verify", "math-explain"], ["research mathematical literature", "prove the mathematical theorem", "find a mathematical counterexample boundary case", "compute a mathematical numerical experiment", "solve the mathematical equation", "verify the mathematical proof", "explain the mathematical intuition"]),
 "legal_policy": (["legal-research", "legal-compare", "legal-risk", "legal-draft"], ["research controlling legal sources", "compare legal jurisdictions", "assess legal risk and obligations", "draft the legal memo"]),
 "science": (["science-literature", "science-hypothesis", "science-experiment", "science-analysis", "science-replication", "science-report"], ["research the scientific literature", "derive a falsifiable hypothesis", "design a controlled experiment", "perform reproducible uncertainty analysis", "reproduce the published scientific claim", "write the scientific report"]),
 "security": (["software-security"], ["audit software security trust boundaries, unsafe input handling, and exploitable behavior"]),
 "portability": (["software-portability-audit"], ["audit software portability across supported platforms and operating systems"]),
 "release_readiness": (["launcher-package-matrix", "launcher-release-readiness"], ["build the native package matrix", "verify release readiness and the release matrix"]),
 "installation": (["launcher-install"], ["design the software installation, prerequisites, rollback, and uninstall lifecycle"]),
 "evidence_writing": (["writing-outline", "writing-draft", "writing-factcheck", "writing-review"], ["create a source-aware outline", "draft the evidence report", "factcheck citations and unsupported claims", "review clarity and structure"]),
 "source_research": (["sol-search", "research"], ["research authoritative sources", "extend the research through claim-evidence contradiction analysis"]),
}
ONE_STAGE_VARIANTS = {
 "security": [
  "audit software security trust boundaries, unsafe input handling, and exploitable behavior for {subject}",
  "review software vulnerabilities, unsafe input paths, trust boundaries, and exploit exposure for {subject}",
  "assess software security controls and exploitable trust boundary failures for {subject}",
  "inspect software security for unsafe input paths and vulnerabilities affecting {subject}",
  "test software security trust boundaries against unsafe input and exploitable behavior for {subject}",
 ],
 "portability": [
  "audit software portability across supported platforms and operating systems for {subject}",
  "assess software portability and platform-specific dependencies across supported targets for {subject}",
  "review compatibility across operating systems and supported platforms for {subject}",
  "audit platform coupling and software portability constraints for {subject}",
  "assess portability risks across operating systems and supported platforms for {subject}",
 ],
 "installation": [
  "design software installation, prerequisites, rollback, and uninstall lifecycle for {subject}",
  "prepare installer prerequisites, integrity checks, and rollback for {subject}",
  "implement application installation, update, and uninstall lifecycle for {subject}",
  "plan safe software acquisition and installation prerequisites for {subject}",
  "create target installer recovery and rollback process for {subject}",
 ],
}
EXPECTED = {name: ["solforge-workflow-" + x if not x.startswith(("sol-", "math-", "science-", "legal-", "data-", "writing-", "software-", "launcher-")) else x for x in values] for name, values in {}}
PREFIX = "solforge-workflow-"
def skill(s):
    special={"sol-search":"sol-search", "research":"solforge-workflow-research"}
    return special.get(s, PREFIX+s)
LEADS=["Please carefully", "Please systematically", "Please independently", "Please methodically", "Please transparently", "Please conservatively", "Please thoroughly", "Please directly", "Please sequentially", "Please deliberately"]
SUBJECTS=["a regulated operational decision", "a complex technical system", "a high-stakes planning question", "a customer-facing product decision", "an evidence-bound program review"]
DETAILS=["Preserve traceability and state uncertainty.", "Distinguish evidence from assumptions.", "Record decision limits and dependencies.", "Keep scope bounded and retain review evidence."]
SEPS=["; then ", ", then ", ". Next, ", "; after that, ", ", and then "]
FILLER=("Context notes: revision {rev} concerns {subject}. {detail} Retain source identities, assumptions, baselines, constraints, alternatives, measurements, risk hypotheses, acceptance criteria, limitations, data lineage, review observations, configuration snapshots, ownership, timelines, dependencies, uncertainty bounds, and evidence linking every conclusion to its source, calculation, model, experiment, or observation. Preserve interfaces, distinguish proposed work from completed work, avoid unrelated cleanup, and keep fabrication, ordering, publishing, deployment, purchases, releases, and external communication outside scope. Include reviewer observations, retained artifacts, decision logs, test evidence, approval boundaries, privacy considerations, accessibility needs where relevant, maintenance implications, fallback behavior, and the accountable owner for every material decision. Record stakeholder objectives, operational context, input coverage, baseline comparisons, review cadence, change-control constraints, reproducibility requirements, escalation criteria, verification methods, expected benefits, residual risks, decision deadlines, responsible roles, and the evidence needed for an independent reviewer to reproduce each material conclusion. Preserve units, definitions, sample coverage, version lineage, decision rationale, exception handling, approval status, resource limits, observable outcomes, recovery conditions, system boundaries, validation cadence, delivery constraints, and documented lessons across all stages. Record dependencies, interface owners, incident response contacts, operational monitoring expectations, and criteria for revisiting conclusions when evidence changes.")
def words(x): return len(re.findall(r"\b[\w'-]+\b",x))
def expected(name): return [skill(x) for x in P[name][0]]
def main():
  domains={}; failures=[]
  for name, (_, stages) in P.items():
    seen=set(); bad=[]; low=None
    for lead in LEADS:
      for subject in SUBJECTS:
       for detail in DETAILS:
        for variant_index, sep in enumerate(SEPS):
         for rev in range(10):
          active_stages = [ONE_STAGE_VARIANTS[name][variant_index].format(subject=subject)] if name in ONE_STAGE_VARIANTS else [f"{stage} for {subject}" for stage in stages]
          text=lead+" "+sep.join(active_stages)+". "+FILLER.format(rev=rev,subject=subject,detail=detail)+" Without merging, publishing, deploying, purchasing, or sending."
          if text in seen: raise AssertionError(name+" duplicate")
          seen.add(text); count=words(text)
          if count<200: raise AssertionError(f"{name} {count} words")
          low=count if low is None else min(low,count)
          r=composer.compose_route(GRAPH,text,max_skills=50)
          if r['selected']!=expected(name) or sorted(r['excluded_effects'])!=['deploy','merge','publish','purchase','send'] or r['unselected_requested_stages'] or r['execution_authorized']:
            bad.append({'actual':r['selected'],'unselected':r['unselected_requested_stages']})
    if len(seen)!=10000: raise AssertionError(name+" count")
    domains[name]={'total':10000,'passed':10000-len(bad),'minimum_words':low,'failures':bad[:20]}; failures+=bad[:5]
  out={'domains':domains,'total':100000,'passed':sum(v['passed'] for v in domains.values()),'failures':failures}
  print(json.dumps({'validated_source': 'SolKraft public routing interface'}))
  Path(__file__).with_name('results-routing-100000.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
  print(json.dumps({k:{x:y for x,y in v.items() if x!='failures'} for k,v in domains.items()},indent=2))
  if failures: raise SystemExit(1)
if __name__=='__main__': main()
