"""Reviewer-corrected re-run. Saves real numbers to a dated artifact dir.
Run combos:
  RAW            : all fixes off (must match original)
  M1             : J-scaling fixed only
  M1+M3          : J-scaling + no-purchase outside option (the consistent model)
Also: smooth QoS shapes (M4) under M1, and welfare/protection/direct-API under M1+M3.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.intermediary_market import IntermediaryConfig
from pricing_sim.fixed_market import (
    run_baselines, optimize_three_layer, evaluate_policy, MarketFix,
    _default_capacity, _single_config, solve_middle_stage,
)

OUT = ROOT / "artifacts" / "reviewer_fixed" / "20260618"
OUT.mkdir(parents=True, exist_ok=True)
TRIALS, MAXITER = 8, 140


def row(r):
    return dict(policy=r.policy, fix=r.fix_tag, system_profit=r.system_profit,
                platform_revenue=r.platform_revenue, intermediary_profit=r.intermediary_profit,
                min_qos=r.diagnostics["min_qos"], peak_util=r.diagnostics["max_utilization"],
                avg_retail=r.avg_retail_price, inclusive_value=r.inclusive_value,
                exit_prob=r.exit_probability, active_min_qos=r.active_min_qos,
                demand_weighted_qos=r.demand_weighted_qos, demand_total=float(r.demand.sum()),
                max_regret=r.diagnostics.get("max_regret", float("nan")))


def main():
    cfg = IntermediaryConfig.default(optimizer_trials=TRIALS, optimizer_maxiter=MAXITER)
    out = {}

    for tag, fix in [("RAW", MarketFix()),
                     ("M1", MarketFix(fix_rigid_scaling=True)),
                     ("M1_M3", MarketFix(fix_rigid_scaling=True, outside_option=True))]:
        res = run_baselines(cfg, fix)
        out[f"baselines_{tag}"] = [row(r) for r in res.values()]
        print(f"[{tag}] baselines done", flush=True)
        for k, r in res.items():
            print(f"   {k:22s} sys={r.system_profit:9.2f} IV={r.inclusive_value:+.3f} exit={r.exit_probability*100:5.1f}% peakU={r.diagnostics['max_utilization']:.4f} minQoS={r.diagnostics['min_qos']:.4f}", flush=True)

    # M4: smooth QoS shapes under the M1 fix (qos-aware three-layer)
    smooth = []
    for shape in ["threshold", "linear", "sigmoid", "sqrt"]:
        fix = MarketFix(fix_rigid_scaling=True, qos_shape=shape)
        r = optimize_three_layer(cfg, fix, qos_aware=True, policy=f"three_layer_{shape}")
        smooth.append(row(r))
        print(f"[M4 {shape:9s}] sys={r.system_profit:9.2f} minQoS={r.diagnostics['min_qos']:.4f} peakU={r.diagnostics['max_utilization']:.4f} activeMinQoS={r.active_min_qos:.4f}", flush=True)
    out["smooth_qos_M1"] = smooth

    (OUT / "reviewer_fixed_records.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", OUT / "reviewer_fixed_records.json", flush=True)


if __name__ == "__main__":
    main()
