"""A failed local build step must never look like a successful release."""
import subprocess
import sys

import pytest

from scripts.local_ci import run_step


def test_local_gate_records_failure_and_stops(tmp_path):
    receipt = []
    with pytest.raises(subprocess.CalledProcessError):
        run_step('failing build', [sys.executable, '-c', 'raise SystemExit(7)'],
                 tmp_path, {}, receipt)
    assert receipt[0]['exit_code'] == 7
    assert receipt[0]['name'] == 'failing build'
