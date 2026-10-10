"""Complete the full semantic corpus locally with resumable worker slices.

Run after installing .[dev]: python -m scripts.local_semantic_ci --workers 6.
Each worker executes the production route function; no route-result memoization.
Only matching source/configuration receipts can be resumed. Aggregation enforces
all 373,000 executions for the current 173-skill bundle.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import sys
import time

from scripts.semantic_router_benchmark import source_identity

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--shards', type=int, default=16)
    parser.add_argument('--slices', type=int, default=2)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/semantic-proof-local')
    args = parser.parse_args()
    if min(args.workers, args.shards, args.slices) < 1:
        parser.error('workers, shards, and slices must be positive')
    args.output.mkdir(parents=True, exist_ok=True)
    source = source_identity()
    started = time.monotonic()

    def worker(shard, part):
        path = args.output / f'results-semantic-router-proof-shard-{shard}-slice-{part}.json'
        if path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
            corpus = data.get('corpus', {})
            if (data.get('source') != source or data.get('shard_count') != args.shards
                or data.get('slice_count') != args.slices
                or corpus.get('single_prompts_per_skill_configured') != 1000
                or corpus.get('composition_cases_configured') != 100000
                or corpus.get('stability_base_cases_configured') != 10000
                or corpus.get('stability_repeats') != 10):
                raise RuntimeError(f'Stale or incompatible receipt: {path}. Use a new output directory.')
            return f'resumed {shard}/{part}'
        print(f'[local-semantic-ci] start {shard}/{part}', flush=True)
        log = path.with_suffix('.log')
        with log.open('w', encoding='utf-8') as stream:
            subprocess.run([sys.executable, '-m', 'scripts.semantic_router_benchmark',
                            '--shard-index', str(shard), '--shard-count', str(args.shards),
                            '--slice-index', str(part), '--slice-count', str(args.slices),
                            '--output', str(path)], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
        return f'completed {shard}/{part}'

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(worker, shard, part) for shard in range(args.shards) for part in range(args.slices)]
        for future in as_completed(futures):
            print(f'[local-semantic-ci] {future.result()}; elapsed {time.monotonic() - started:.0f}s', flush=True)
    subprocess.run([sys.executable, '-m', 'scripts.aggregate_semantic_router_benchmark',
                    '--input', str(args.output), '--output', str(args.output / 'summary.json')], cwd=ROOT, check=True)

if __name__ == '__main__':
    main()
