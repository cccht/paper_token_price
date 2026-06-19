"""Run damping and initial-condition audits for SMPT V&V."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.peak_shaving_smpt_tools import (
    OUT,
    congested_base,
    evaluate_params,
    load_policy_vectors,
    params_from_vectors,
    trace_fixed_point_residuals,
)


def audit_rows() -> list[dict[str, float | str | bool | int]]:
    cfg = congested_base()
    policies = load_policy_vectors()
    cases = ["uniform", "dynamic_coarse", "dynamic_fine"]
    initial_values = [0.5, 0.75, 1.0]
    damping_values = [0.2, 0.35, 0.5]
    rows = []
    for case in cases:
        record = evaluate_params(case, params_from_vectors(policies[case]), cfg, static_shape=case == "uniform")
        for initial_qos in initial_values:
            for damping in damping_values:
                trace = trace_fixed_point_residuals(
                    record["prices"],
                    record["routing"],
                    cfg,
                    initial_qos=initial_qos,
                    damping=damping,
                )
                rows.append({
                    "case": case,
                    "initial_qos": initial_qos,
                    "damping": damping,
                    "iterations": trace["iterations"],
                    "final_residual": trace["final_residual"],
                    "max_residual": trace["max_residual"],
                    "converged": trace["converged"],
                })
    return rows


def write_rows(rows: list[dict[str, float | str | bool | int]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "smpt_vv_damping_initial.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "rows": len(rows),
        "converged": sum(bool(r["converged"]) for r in rows),
        "max_final_residual": max(float(r["final_residual"]) for r in rows),
        "max_iterations": max(int(r["iterations"]) for r in rows),
    }
    (OUT / "smpt_vv_damping_initial_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"csv": str(path.relative_to(ROOT)), **summary}, indent=2))


if __name__ == "__main__":
    write_rows(audit_rows())
