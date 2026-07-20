"""Build an eight-period intraday load anchor from the public BurstGPT trace."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SOURCE_COMMIT = "d895a53bb7b8ec137d0d2fe203b335835a78c10a"
SOURCE_URL = (
    "https://raw.githubusercontent.com/HPMLL/BurstGPT/"
    f"{SOURCE_COMMIT}/data/BurstGPT_1.csv"
)
DEFAULT_CACHE = Path("/tmp") / f"burstgpt_{SOURCE_COMMIT[:8]}_1.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / f"burstgpt_{SOURCE_COMMIT[:8]}_8period"
SOURCE_BYTES = 50_853_373


def _token_count(row: dict[str, str]) -> float:
    total = row.get("Total tokens", "").strip()
    if total:
        return float(total)
    return float(row["Request tokens"]) + float(row["Response tokens"])


def _daily_arrays(path: Path, periods: int) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], int, int]:
    request_by_day: dict[int, np.ndarray] = {}
    token_by_day: dict[int, np.ndarray] = {}
    rows_read = 0
    rows_skipped = 0
    seconds_per_period = 86400 / periods
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            rows_read += 1
            try:
                timestamp = float(row["Timestamp"])
                tokens = _token_count(row)
                if timestamp < 0.0 or tokens < 0.0:
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                rows_skipped += 1
                continue
            day = int(timestamp // 86400)
            period = min(int((timestamp % 86400) // seconds_per_period), periods - 1)
            request_by_day.setdefault(day, np.zeros(periods))[period] += 1.0
            token_by_day.setdefault(day, np.zeros(periods))[period] += tokens
    return request_by_day, token_by_day, rows_read, rows_skipped


def _daily_shares(values: dict[int, np.ndarray], days: list[int]) -> np.ndarray:
    rows = np.vstack([values[day] for day in days])
    totals = np.sum(rows, axis=1, keepdims=True)
    return rows / np.maximum(totals, 1e-12)


def _normalized_shape(profile: np.ndarray) -> np.ndarray:
    centered = profile - np.mean(profile)
    scale = np.max(np.abs(centered))
    return centered / scale if scale > 0.0 else np.zeros_like(centered)


def aggregate_trace(path: Path, *, periods: int = 8, exclude_edge_days: bool = True) -> dict:
    if periods <= 0 or 86400 % periods != 0:
        raise ValueError("periods must be a positive divisor of 86400")
    request_by_day, token_by_day, rows_read, rows_skipped = _daily_arrays(path, periods)
    days = sorted(set(request_by_day) & set(token_by_day))
    if exclude_edge_days and len(days) >= 3:
        days = days[1:-1]
    days = [
        day for day in days
        if np.all(request_by_day[day] > 0.0) and np.sum(token_by_day[day]) > 0.0
    ]
    if not days:
        raise ValueError("trace contains no complete days for the requested period grid")
    request_shares = _daily_shares(request_by_day, days)
    token_shares = _daily_shares(token_by_day, days)
    token_mean = np.mean(token_shares, axis=0)
    return {
        "rows_read": rows_read,
        "rows_skipped": rows_skipped,
        "days_used": days,
        "request_share_mean": np.mean(request_shares, axis=0),
        "request_share_std": np.std(request_shares, axis=0),
        "token_share_mean": token_mean,
        "token_share_std": np.std(token_shares, axis=0),
        "normalized_token_load": _normalized_shape(token_mean),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_trace(url: str, cache_path: Path, *, expected_bytes: int) -> Path:
    if cache_path.exists() and cache_path.stat().st_size == expected_bytes:
        return cache_path
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(5):
        partial_size = cache_path.stat().st_size if cache_path.exists() else 0
        command = [
            "curl", "-L", "--fail", "--silent", "--show-error",
            "--connect-timeout", "20", "--speed-limit", "1024",
            "--speed-time", "30", "--max-time", "180",
        ]
        if 0 < partial_size < expected_bytes:
            command.extend(["--continue-at", "-"])
        command.extend(["--output", str(cache_path), url])
        subprocess.run(command, check=False)
        if cache_path.exists() and cache_path.stat().st_size == expected_bytes:
            return cache_path
    actual = cache_path.stat().st_size if cache_path.exists() else 0
    raise IOError(f"download size mismatch: expected {expected_bytes}, received {actual}")


def write_anchor(result: dict, source: Path, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "burstgpt_8period_load_profile.csv"
    metadata_path = output_dir / "burstgpt_8period_load_metadata.json"
    fields = [
        "period", "request_share_mean", "request_share_std",
        "token_share_mean", "token_share_std", "normalized_token_load",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for period in range(len(result["token_share_mean"])):
            writer.writerow({field: period + 1 if field == "period" else result[field][period]
                             for field in fields})
    metadata = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_repository": "https://github.com/HPMLL/BurstGPT",
        "source_commit": SOURCE_COMMIT,
        "source_url": SOURCE_URL,
        "source_sha256": _sha256(source),
        "source_bytes": source.stat().st_size,
        "license": "CC-BY-4.0",
        "method": "mean of complete-day normalized 3-hour request and token profiles",
        "rows_read": result["rows_read"],
        "rows_skipped": result["rows_skipped"],
        "days_used": result["days_used"],
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return csv_path, metadata_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-url", default=SOURCE_URL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-bytes", type=int, default=SOURCE_BYTES)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = download_trace(args.source_url, args.cache, expected_bytes=args.expected_bytes)
    result = aggregate_trace(source, periods=8, exclude_edge_days=True)
    paths = write_anchor(result, source, args.output_dir)
    print(json.dumps({
        "outputs": [str(path.relative_to(ROOT)) for path in paths],
        "source_sha256": _sha256(source),
        "rows_read": result["rows_read"],
        "days_used": len(result["days_used"]),
    }, indent=2))


if __name__ == "__main__":
    main()
