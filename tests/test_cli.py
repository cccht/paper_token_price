import subprocess
import sys
from pathlib import Path


def test_smoke_cli_writes_artifacts(tmp_path):
    script = Path(__file__).resolve().parents[1] / "experiments" / "run_experiment.py"

    result = subprocess.run(
        [sys.executable, str(script), "--smoke", "--output-root", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert "mode=smoke" in result.stdout
    assert list((tmp_path / "summaries").rglob("summary.csv"))
