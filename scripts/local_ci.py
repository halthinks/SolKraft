"""Cross-platform local release gate. Run: python -m scripts.local_ci.

Install .[dev], Node.js, setuptools and wheel first. No GitHub runner is used.
Artifact checks reuse the current environment's dependencies; they do not prove
a fresh offline installation or a platform that was not executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run_step(name, command, cwd, env, receipt):
    print(f'\n[local-ci] {name}', flush=True)
    started = time.monotonic()
    result = subprocess.run(command, cwd=cwd, env=env, check=False)
    receipt.append({'name': name, 'exit_code': result.returncode,
                    'seconds': round(time.monotonic() - started, 3)})
    result.check_returncode()


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    node = shutil.which('node')
    if not node:
        raise SystemExit('Node.js is required for the UI checks. Install Node.js and retry.')
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    env = dict(os.environ)
    env['SOLFORGE_TEST_ROOT'] = str(ROOT / 'solkraft/skillpacks')
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    steps = []
    receipt = {'schema': 'solkraft/local-ci/v1', 'platform': sys.platform,
               'python': sys.version.split()[0], 'status': 'running', 'steps': steps}
    def run(name, command, cwd=ROOT, step_env=env):
        run_step(name, command, cwd, step_env, steps)
    try:
        run('Python and routing tests', [sys.executable, '-m', 'pytest', '-q', 'tests',
                                       'solkraft/skillpacks/solforge/tests', '-p', 'no:cacheprovider'])
        run('Python compilation', [sys.executable, '-m', 'compileall', '-q', 'solkraft', 'scripts'])
        run('Contract migration report', [sys.executable, '-m', 'scripts.migrate_contracts',
                                         '--report', 'build/contracts-migration.json'])
        for asset in ('app.js', 'flow.js', 'setup.js', 'static-data.js'):
            run(f'{asset} syntax', [node, '--check', f'docs/assets/{asset}'])
        run('Setup behavior tests', [node, '--test', 'tests/setup.test.cjs'])
        run('Build static console', [sys.executable, '-m', 'scripts.build_console'])
        run('Package plugin', [sys.executable, 'scripts/package_plugin.py'])
        with tempfile.TemporaryDirectory(prefix='solkraft-ci-') as temporary:
            workspace = Path(temporary)
            run('Build wheel', [sys.executable, '-m', 'pip', 'wheel', '.', '--no-deps',
                               '--no-build-isolation', '--wheel-dir', str(workspace / 'wheels')])
            wheel = next((workspace / 'wheels').glob('solkraft-*.whl'))
            artifact = ROOT / 'dist' / wheel.name
            artifact.parent.mkdir(exist_ok=True)
            shutil.copy2(wheel, artifact)
            receipt['wheel'] = {'name': wheel.name, 'sha256': hashlib.sha256(wheel.read_bytes()).hexdigest()}
            run('Create artifact environment', [sys.executable, '-m', 'venv', '--system-site-packages', str(workspace / 'venv')])
            executable_dir = workspace / 'venv' / ('Scripts' if os.name == 'nt' else 'bin')
            python = executable_dir / ('python.exe' if os.name == 'nt' else 'python')
            run('Install built wheel', [str(python), '-m', 'pip', 'install', '--no-deps', '--force-reinstall', str(wheel)], workspace)
            with zipfile.ZipFile(ROOT / 'docs/downloads/solkraft-plugin.zip') as archive:
                archive.extractall(workspace / 'plugin')
            artifact_env = dict(env, SOLKRAFT_TEST_PLUGIN_ROOT=str(workspace / 'plugin/solkraft'))
            artifact_env['PATH'] = str(executable_dir) + os.pathsep + env['PATH']
            artifact_env.pop('PYTHONPATH', None)
            run('Installed catalog outside checkout', [str(python), '-c',
                'from solkraft.catalog import SkillCatalog; from solkraft.routing import BUNDLE_ROOT; '
                'assert "site-packages" in str(BUNDLE_ROOT); '
                'assert len(SkillCatalog([BUNDLE_ROOT]).records()) >= 173; print("Installed catalog verified")'],
                workspace, artifact_env)
            run('ZIP plugin against installed MCP runtime', [str(python), '-m', 'pytest', '-q',
                str(ROOT / 'tests/test_plugin.py'), '-p', 'no:cacheprovider'], workspace, artifact_env)
        run('Whitespace review', ['git', '-c', f'safe.directory={ROOT.as_posix()}', 'diff', '--check'])
        receipt['status'] = 'passed'
    except (subprocess.CalledProcessError, OSError, StopIteration) as error:
        receipt['status'] = 'failed'
        receipt['error'] = str(error)
        raise
    finally:
        (build / 'local-ci.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
        print(f'\n[local-ci] {receipt["status"]}; receipt: build/local-ci.json', flush=True)


if __name__ == '__main__':
    main()
