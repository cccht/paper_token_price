from pathlib import Path

from experiments.run_reproducibility_bundle import build_commands


def test_build_commands_include_economic_supplemental_and_tests(tmp_path):
    commands = build_commands(output_root=tmp_path, smoke=False, skip_tests=False)

    assert commands[0][-3:] == ["--full", "--output-root", str(tmp_path / "economic")]
    assert Path(commands[1][1]).name == "run_supplemental_experiments.py"
    assert commands[1].count("--vllm-aggregate") == 2
    assert Path(commands[2][1]).name == "run_calibration_uncertainty_experiments.py"
    assert commands[2][-4:] == ["--maxiter", "30", "--output-root", str(tmp_path / "calibration_uncertainty")]
    assert commands[-1][-3:] == ["-m", "pytest", "-q"]


def test_build_commands_can_skip_tests_and_use_smoke_mode(tmp_path):
    commands = build_commands(output_root=tmp_path, smoke=True, skip_tests=True)

    assert "--smoke" in commands[0]
    assert all("pytest" not in command for command in commands)
