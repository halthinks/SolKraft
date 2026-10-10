import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def receipt():
    return {
        'shard_index': 0, 'shard_count': 1, 'catalog': {'skill_count': 1, 'selectable_skill_count': 1},
        'source': {'revision': 'test', 'inputs_sha256': 'a', 'harness': 'production-router/frozen-catalog'},
        'corpus': {'single_prompts_per_skill_configured': 1000, 'development_partition_boundary': 800,
                   'holdout_partition_start': 800, 'composition_cases_configured': 100000,
                   'stability_base_cases_configured': 10000, 'stability_repeats': 10, 'shard_corpus_sha256': 'a'},
        'single': {'cases': 1000, 'passed': 1000, 'holdout_eligible_cases': 200, 'holdout_eligible_passed': 200},
        'composition': {'cases': 100000, 'all_targets_selected': 100000, 'target_order_preserved': 100000},
        'stability': {'base_cases': 10000, 'executions': 100000, 'mismatches': 0},
        'per_skill': {'sample': {'cases': 1000, 'passed': 1000}},
        'single_prompt_hashes_by_skill': {'sample': [str(i) for i in range(1000)]},
    }

def aggregate(tmp_path, data, second=None):
    (tmp_path / 'results-semantic-router-proof-shard-0.json').write_text(json.dumps(data), encoding='utf-8')
    if second:
        (tmp_path / 'results-semantic-router-proof-shard-1.json').write_text(json.dumps(second), encoding='utf-8')
    output = tmp_path / 'summary.json'
    run = subprocess.run([sys.executable, '-m', 'scripts.aggregate_semantic_router_benchmark', '--input', str(tmp_path), '--output', str(output)], cwd=ROOT, capture_output=True, text=True)
    return run, json.loads(output.read_text()) if output.exists() else None

def test_complete_counts_required(tmp_path):
    data = receipt()
    data['composition']['cases'] = 1
    data['composition']['all_targets_selected'] = 1
    data['composition']['target_order_preserved'] = 1
    run, result = aggregate(tmp_path, data)
    assert run.returncode == 2
    assert result['gates']['composition_coverage_rate']
    assert not result['gates']['complete_execution_counts']
    assert not result['proof_passed']

def test_smoke_cannot_be_full_proof(tmp_path):
    data = receipt()
    data['corpus']['composition_cases_configured'] = 1
    data['composition'] = {'cases': 1, 'all_targets_selected': 1, 'target_order_preserved': 1}
    run, result = aggregate(tmp_path, data)
    assert run.returncode == 2
    assert not result['gates']['full_corpus_configuration']

def test_mixed_sources_rejected(tmp_path):
    first, second = receipt(), receipt()
    first['shard_count'] = second['shard_count'] = 2
    second['shard_index'] = 1
    second['source']['inputs_sha256'] = 'different'
    run, result = aggregate(tmp_path, first, second)
    assert run.returncode != 0
    assert 'inconsistent source identity' in run.stderr
    assert result is None

def test_mixed_configuration_rejected(tmp_path):
    first, second = receipt(), receipt()
    first['shard_count'] = second['shard_count'] = 2
    second['shard_index'] = 1
    second['corpus']['stability_repeats'] = 1
    run, result = aggregate(tmp_path, first, second)
    assert run.returncode != 0
    assert 'inconsistent corpus configuration' in run.stderr
    assert result is None

def test_missing_slice_cannot_pass(tmp_path):
    data = receipt()
    data['slice_count'] = 2
    run, result = aggregate(tmp_path, data)
    assert run.returncode == 2
    assert not result['gates']['complete_shard_slice_topology']
