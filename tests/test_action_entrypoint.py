"""Regression tests for the GitHub Action's clause verification boundary."""

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run_action(clauses):
    output = ROOT / "tests" / ".action-output"
    output.unlink(missing_ok=True)
    env = os.environ.copy()
    env["GITHUB_OUTPUT"] = str(output)
    try:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "action_entrypoint.py"),
                "clause",
                "",
                "",
                "",
                "",
                "",
                "",
                json.dumps(clauses),
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        output.unlink(missing_ok=True)


def test_empty_clauses_fail_the_action_closed():
    result = _run_action([])

    assert result.returncode == 1
    assert "Verification FAILED" in result.stdout
