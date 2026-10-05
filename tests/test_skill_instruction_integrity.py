from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_skill_instruction_integrity():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_skill_instructions.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
