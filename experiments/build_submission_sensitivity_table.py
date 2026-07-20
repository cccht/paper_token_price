"""Generate the submission sensitivity table from the audited summary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
SUMMARY_PATH = ARTIFACT_DIR / "spatiotemporal_sensitivity_submission.json"
OUTPUT_PATH = ARTIFACT_DIR / "submission_sensitivity_table.tex"
SCENARIO_ORDER = (
    "baseline",
    "capacity_low",
    "capacity_high",
    "price_sensitivity_low",
    "price_sensitivity_high",
    "migration_cost_low",
    "migration_cost_high",
    "qos_threshold_low",
    "qos_threshold_high",
)
SCENARIO_LABELS = {
    "baseline": "Baseline",
    "capacity_low": r"Capacity $-15\%$",
    "capacity_high": r"Capacity $+15\%$",
    "price_sensitivity_low": r"Utility coefficient $-20\%$",
    "price_sensitivity_high": r"Utility coefficient $+20\%$",
    "migration_cost_low": r"Migration cost $-30\%$",
    "migration_cost_high": r"Migration cost $+30\%$",
    "qos_threshold_low": r"QoS threshold $-0.05$",
    "qos_threshold_high": r"QoS threshold $+0.05$",
}


def _validate(summary: dict) -> list[dict]:
    metadata = summary.get("metadata", {})
    rows = summary.get("rows", [])
    if metadata.get("scenario_count") != len(SCENARIO_ORDER):
        raise ValueError("sensitivity scenario count is not nine")
    if metadata.get("provider_candidate_count") != 1576:
        raise ValueError("provider candidate count is not 1576")
    if tuple(row.get("scenario") for row in rows) != SCENARIO_ORDER:
        raise ValueError("sensitivity scenario order is invalid")
    return rows


def _scientific(value: float) -> str:
    mantissa, exponent = f"{value:.2e}".split("e")
    return rf"${mantissa}\times10^{{{int(exponent)}}}$"


def _signed(value: float, decimals: int) -> str:
    return f"${value:+.{decimals}f}$"


def _table_row(row: dict) -> str:
    regret = max(
        row["uniform_full_max_regret"], row["dynamic_full_max_regret"]
    )
    values = (
        SCENARIO_LABELS[row["scenario"]],
        _scientific(regret),
        _scientific(row["maximum_joint_residual"]),
        _signed(row["aggregate_peak_change_percent"], 2),
        _signed(row["maximum_provider_utilization_change_percent"], 2),
        _signed(row["minimum_provider_qos_change"], 4),
        _signed(row["market_profit_change_percent"], 2),
    )
    return " & ".join(values) + r" \\"


def build_table(summary: dict, *, source_sha256: str) -> str:
    rows = _validate(summary)
    body = "\n".join(_table_row(row) for row in rows)
    return f"""% Generated from the audited sensitivity summary. Do not edit.
% Source SHA-256: {source_sha256}
\\begin{{table}}[H]
\\centering
\\caption{{Finite-game sensitivity results on the common 1,576-candidate set. Each case re-solves both policy games and checks every declared unilateral provider deviation. Maximum regret is the larger uniform or time-varying finite-game value. Maximum residual is taken across both games. Peak, utilization, and profit changes are percentages; minimum-QoS change is absolute.}}
\\label{{tab:resolved_sensitivity}}
\\scriptsize
\\setlength{{\\tabcolsep}}{{2.25pt}}
\\begin{{tabular}}{{@{{}}lrrrrrr@{{}}}}
\\toprule
Case & Maximum regret & Maximum residual & Peak $\\Delta$ (\\%) & Utilization $\\Delta$ (\\%) & Minimum QoS $\\Delta$ & Profit $\\Delta$ (\\%) \\\\
\\midrule
{body}
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""


def main() -> None:
    source_bytes = SUMMARY_PATH.read_bytes()
    summary = json.loads(source_bytes)
    source = build_table(
        summary,
        source_sha256=hashlib.sha256(source_bytes).hexdigest(),
    )
    OUTPUT_PATH.write_text(source, encoding="utf-8")
    print(OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
