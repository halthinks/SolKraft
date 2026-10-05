from __future__ import annotations
import argparse, json, hashlib
from collections import Counter, defaultdict
from pathlib import Path

THRESHOLDS = {
    'single_global_rate': 0.95,
    'single_holdout_rate': 0.95,
    'per_skill_rate': 0.90,
    'composition_coverage_rate': 0.90,
    'composition_order_rate': 0.95,
    'stability_rate': 1.0,
}

def div(a,b):
    return round(a/b, 8) if b else None

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args=p.parse_args()
    files=sorted(args.input.rglob('results-semantic-router-proof-shard-*.json'))
    if not files:
        raise SystemExit('no shard results found')

    single=Counter(); composition=Counter(); stability=Counter(); leakage=Counter()
    per_skill=defaultdict(Counter); confusion=defaultdict(Counter); failures=[]; digests=[]
    catalog=None; configured=None
    for path in files:
        data=json.loads(path.read_text(encoding='utf-8'))
        catalog = catalog or data['catalog']
        configured = configured or data['corpus']
        single.update(data.get('single',{})); composition.update(data.get('composition',{})); stability.update(data.get('stability',{})); leakage.update(data.get('leakage',{}))
        for sid, metrics in data.get('per_skill',{}).items():
            per_skill[sid].update({k:v for k,v in metrics.items() if isinstance(v,int)})
        for sid, rows in data.get('confusion',{}).items():
            confusion[sid].update(rows)
        failures.extend(data.get('sample_failures',[])[:3])
        digests.append(data['corpus']['shard_corpus_sha256'])

    per_skill_out={}
    min_rate=1.0; min_holdout=1.0; below=[]
    for sid in sorted(per_skill, key=str.casefold):
        m=per_skill[sid]
        rate=div(m['passed'],m['cases'])
        dev=div(m['dev_passed'],m['dev_cases'])
        hold=div(m['holdout_passed'],m['holdout_cases'])
        top1=div(m['top1'],m['cases'])
        per_skill_out[sid]={**dict(m),'rate':rate,'dev_rate':dev,'holdout_rate':hold,'top1_rate':top1}
        if rate is not None: min_rate=min(min_rate,rate)
        if hold is not None: min_holdout=min(min_holdout,hold)
        if rate is not None and rate < THRESHOLDS['per_skill_rate']:
            below.append({'skill':sid,'rate':rate,'holdout_rate':hold})

    single_rate=div(single['passed'],single['cases'])
    holdout_cases=single['holdout_eligible_cases']+single['holdout_boundary_cases']
    holdout_passed=single['holdout_eligible_passed']+single['holdout_boundary_passed']
    holdout_rate=div(holdout_passed,holdout_cases)
    composition_coverage=div(composition['all_targets_selected'],composition['cases'])
    composition_order=div(composition['target_order_preserved'],composition['cases'])
    composition_exact=div(composition['exact_target_set'],composition['cases'])
    stability_rate=div(stability['executions']-stability['mismatches'],stability['executions'])

    gates={
        'no_metadata_leakage': sum(leakage.values()) == 0,
        'single_global_rate': single_rate is not None and single_rate >= THRESHOLDS['single_global_rate'],
        'single_holdout_rate': holdout_rate is not None and holdout_rate >= THRESHOLDS['single_holdout_rate'],
        'every_skill_rate': not below and min_rate >= THRESHOLDS['per_skill_rate'],
        'composition_coverage_rate': composition_coverage is not None and composition_coverage >= THRESHOLDS['composition_coverage_rate'],
        'composition_order_rate': composition_order is not None and composition_order >= THRESHOLDS['composition_order_rate'],
        'stability_rate': stability_rate == THRESHOLDS['stability_rate'],
    }
    proof_passed=all(gates.values())
    digest=hashlib.sha256(''.join(sorted(digests)).encode()).hexdigest()

    out={
        'schema':'solkraft/semantic-router-proof-summary/v1',
        'proof_passed':proof_passed,
        'thresholds':THRESHOLDS,
        'gates':gates,
        'catalog':catalog,
        'corpus':{
            'single_prompts_per_skill':configured['single_prompts_per_skill_configured'],
            'composition_cases':configured['composition_cases_configured'],
            'stability_base_cases':configured['stability_base_cases_configured'],
            'stability_repeats':configured['stability_repeats'],
            'expected_total_executions': catalog['skill_count']*configured['single_prompts_per_skill_configured'] + configured['composition_cases_configured'] + configured['stability_base_cases_configured']*configured['stability_repeats'],
            'explicit_skill_ids_injected':False,
            'full_descriptions_injected':False,
            'aggregate_shard_digest_sha256':digest,
        },
        'single':{**dict(single),'rate':single_rate,'holdout_rate':holdout_rate,'min_per_skill_rate':min_rate,'min_per_skill_holdout_rate':min_holdout},
        'composition':{**dict(composition),'coverage_rate':composition_coverage,'order_rate':composition_order,'exact_set_rate':composition_exact},
        'stability':{**dict(stability),'execution_stability_rate':stability_rate},
        'leakage':dict(leakage),
        'skills_below_threshold':sorted(below,key=lambda x:(x['rate'],x['skill']))[:50],
        'per_skill':per_skill_out,
        'confusion':{sid:dict(rows.most_common(10)) for sid,rows in confusion.items()},
        'sample_failures':failures[:40],
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'proof_passed':proof_passed,'gates':gates,'output':str(args.output)},separators=(',',':')))
    if not proof_passed:
        raise SystemExit(2)

if __name__=='__main__':
    main()
