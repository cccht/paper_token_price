from __future__ import annotations

import csv
import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ArtifactPaths:
    raw_jsonl: Path
    summary_json: Path
    summary_csv: Path
    aggregate_json: Path
    aggregate_csv: Path


def _summary_row(record: dict[str, Any]) -> dict[str, Any]:
    evaluation = record["policy_evaluation"]
    diagnostics = record["diagnostics"]
    return {
        "experiment": record["experiment"],
        "policy": record["policy"],
        "seed": record["seed"],
        "parameter": record["parameter"],
        "parameter_value": record["parameter_value"],
        "profit": evaluation["profit"],
        "welfare": evaluation["welfare"],
        "posted_bill": evaluation["posted_bill"],
        "effective_bill": evaluation["effective_bill"],
        "mean_price": sum(evaluation["prices"]) / len(evaluation["prices"]),
        "min_qos": min(evaluation["qos"]),
        "max_utilization": max(evaluation["utilization"]),
        "demand_converged": evaluation["demand"]["converged"],
        "demand_iterations": evaluation["demand"]["iterations"],
        "cap_residual": diagnostics["cap_residual"],
        "bill_cap_residual": diagnostics["bill_cap_residual"],
        "objective_evaluations": diagnostics["objective_evaluations"],
        "optimizer_success": diagnostics["success"],
        "solver_success": diagnostics["solver_success"],
    }


def _aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = (row["experiment"], row["policy"], row["parameter"], row["parameter_value"])
        groups.setdefault(key, []).append(row)
    aggregates = []
    for key, members in groups.items():
        aggregate = dict(zip(("experiment", "policy", "parameter", "parameter_value"), key))
        aggregate["runs"] = len(members)
        for metric in (
            "profit",
            "welfare",
            "posted_bill",
            "effective_bill",
            "mean_price",
            "min_qos",
            "max_utilization",
        ):
            values = [float(member[metric]) for member in members]
            aggregate[f"{metric}_mean"] = statistics.mean(values)
            aggregate[f"{metric}_std"] = statistics.pstdev(values)
            aggregate[f"{metric}_min"] = min(values)
            aggregate[f"{metric}_max"] = max(values)
        aggregates.append(aggregate)
    return aggregates


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(
    records: list[dict[str, Any]],
    *,
    output_root: Path,
    run_id: str,
) -> ArtifactPaths:
    raw_dir = output_root / "raw" / run_id
    summary_dir = output_root / "summaries" / run_id
    raw_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    raw_jsonl = raw_dir / "records.jsonl"
    summary_json = summary_dir / "summary.json"
    summary_csv = summary_dir / "summary.csv"
    aggregate_json = summary_dir / "aggregate.json"
    aggregate_csv = summary_dir / "aggregate.csv"
    rows = [_summary_row(record) for record in records]
    aggregates = _aggregate_rows(rows)
    raw_jsonl.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    summary_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    aggregate_json.write_text(
        json.dumps(aggregates, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_csv(summary_csv, rows)
    _write_csv(aggregate_csv, aggregates)
    return ArtifactPaths(raw_jsonl, summary_json, summary_csv, aggregate_json, aggregate_csv)
