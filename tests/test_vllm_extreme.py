import pytest

from pricing_sim.vllm_extreme import (
    SafetyLimits,
    build_prompt_for_token_target,
    health_session,
    stop_reason,
    write_scan_checkpoint,
)


def test_stop_reason_accepts_healthy_level():
    assert stop_reason(
        {"success_rate": 0.99},
        [{"gpu_temperature_celsius": 70.0}],
        free_disk_gib=40.0,
        service_healthy=True,
        limits=SafetyLimits(),
    ) is None


def test_stop_reason_rejects_excessive_temperature():
    reason = stop_reason(
        {"success_rate": 1.0},
        [{"gpu_temperature_celsius": 83.0}],
        free_disk_gib=40.0,
        service_healthy=True,
        limits=SafetyLimits(max_temperature_celsius=82.0),
    )

    assert reason == "gpu temperature exceeded 82.0 C"


def test_stop_reason_rejects_failed_service_or_low_disk():
    limits = SafetyLimits(min_free_disk_gib=30.0)

    assert stop_reason(
        {"success_rate": 1.0},
        [],
        free_disk_gib=29.0,
        service_healthy=True,
        limits=limits,
    ) == "free disk below 30.0 GiB"
    assert stop_reason(
        {"success_rate": 1.0},
        [],
        free_disk_gib=40.0,
        service_healthy=False,
        limits=limits,
    ) == "vLLM health check failed"


def test_health_session_ignores_environment_proxy():
    assert health_session().trust_env is False


def test_build_prompt_for_token_target_repeats_until_target():
    prompt = build_prompt_for_token_target(
        "abc",
        5,
        count_tokens=lambda text: len(text.split()),
    )

    assert len(prompt.split()) >= 5


def test_build_prompt_for_token_target_rejects_zero_token_base():
    counts = iter([0, 0])

    with pytest.raises(ValueError, match="must produce tokens"):
        build_prompt_for_token_target(
            "abc",
            5,
            count_tokens=lambda text: next(counts),
        )


def test_write_scan_checkpoint_persists_completed_levels(tmp_path):
    write_scan_checkpoint(
        tmp_path,
        [{"concurrency": 128, "success_rate": 1.0}],
        {"model": "test-model"},
    )

    assert "concurrency,success_rate" in (tmp_path / "summary.csv").read_text(
        encoding="utf-8-sig"
    )
    assert '"model": "test-model"' in (tmp_path / "metadata.json").read_text(
        encoding="utf-8"
    )
