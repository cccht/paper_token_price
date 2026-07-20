"""Fit the final market QoS function to the existing vLLM measurements."""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "artifacts" / "peak_shaving" / "20260619_submission"
POINTS_PATH = SOURCE_DIR / "vllm_qos_anchor_points.csv"
SUMMARY_PATH = SOURCE_DIR / "vllm_qos_anchor_summary.json"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_final"


def load_anchor_points(path: Path = POINTS_PATH) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [{
        "profile": row["profile"],
        "model": row["model"],
        "normalized_utilization": float(row["normalized_utilization"]),
        "observed_qos": float(row["observed_qos"]),
        "observed_qos_ci95": float(row["observed_qos_ci95"]),
        "repeats": int(float(row["repeats"])),
    } for row in rows]


def _qos_curve(
    utilization: np.ndarray,
    threshold: float,
    strength: float,
) -> np.ndarray:
    excess = np.maximum(np.asarray(utilization, dtype=float) - threshold, 0.0)
    return np.exp(-strength * excess * excess)


def pooled_qos_fit(points: list[dict]) -> dict:
    utilization = np.array(
        [point["normalized_utilization"] for point in points], dtype=float
    )
    observed = np.array([point["observed_qos"] for point in points], dtype=float)

    def residual(parameters: np.ndarray) -> np.ndarray:
        return _qos_curve(utilization, parameters[0], parameters[1]) - observed

    result = least_squares(
        residual,
        x0=np.array([1.0, 0.8]),
        bounds=(np.array([1.0, 0.01]), np.array([1.5, 10.0])),
    )
    fitted = _qos_curve(utilization, result.x[0], result.x[1])
    profiles = sorted({str(point["profile"]) for point in points})
    rmse_by_profile = {}
    for profile in profiles:
        mask = np.array([point["profile"] == profile for point in points])
        rmse_by_profile[profile] = float(
            np.sqrt(np.mean((fitted[mask] - observed[mask]) ** 2))
        )
    return {
        "threshold": float(result.x[0]),
        "strength": float(result.x[1]),
        "rmse": float(np.sqrt(np.mean((fitted - observed) ** 2))),
        "rmse_by_profile": rmse_by_profile,
        "fitted_qos": fitted,
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _leave_one_profile_out(points: list[dict]) -> dict[str, dict[str, float]]:
    profiles = sorted({str(point["profile"]) for point in points})
    results = {}
    for train_profile in profiles:
        test_profile = next(item for item in profiles if item != train_profile)
        train = [point for point in points if point["profile"] == train_profile]
        test = [point for point in points if point["profile"] == test_profile]
        fit = pooled_qos_fit(train)
        utilization = np.array(
            [point["normalized_utilization"] for point in test], dtype=float
        )
        observed = np.array([point["observed_qos"] for point in test], dtype=float)
        predicted = _qos_curve(utilization, fit["threshold"], fit["strength"])
        results[f"train_{train_profile}_test_{test_profile}"] = {
            "threshold": fit["threshold"],
            "strength": fit["strength"],
            "train_rmse": fit["rmse"],
            "test_rmse": float(np.sqrt(np.mean((predicted - observed) ** 2))),
        }
    return results


def build_calibration() -> dict:
    points = load_anchor_points()
    fit = pooled_qos_fit(points)
    script_path = Path(__file__).resolve()
    sources = (
        POINTS_PATH,
        SUMMARY_PATH,
        ROOT / "pricing_sim" / "peak_shaving_market.py",
        script_path,
    )
    serialized_points = []
    for point, fitted in zip(points, fit["fitted_qos"]):
        serialized_points.append({**point, "pooled_fitted_qos": float(fitted)})
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "fit_function": "q(u)=exp(-strength*max(u-threshold,0)^2)",
            "fit_constraint": (
                "threshold >= 1 because all measured points at u <= 1 met the SLA"
            ),
            "qos_definition": "TTFT SLA rate with threshold 0.5 seconds",
            "measurement_boundary": (
                "Two Qwen2.5 models on one RTX 4090; five repeats per concurrency."
            ),
            "source_sha256": {
                str(path.relative_to(ROOT)): _sha256(path) for path in sources
            },
        },
        "pooled_fit": {
            key: value for key, value in fit.items() if key != "fitted_qos"
        },
        "leave_one_profile_out": _leave_one_profile_out(points),
        "points": serialized_points,
    }


def write_calibration(artifact: dict) -> tuple[Path, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "qos_calibration.json"
    csv_path = OUT / "qos_calibration_points.csv"
    json_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(artifact["points"][0]))
        writer.writeheader()
        writer.writerows(artifact["points"])
    return json_path, csv_path


def main() -> None:
    paths = write_calibration(build_calibration())
    print(json.dumps({"outputs": [str(path.relative_to(ROOT)) for path in paths]}))


if __name__ == "__main__":
    main()
