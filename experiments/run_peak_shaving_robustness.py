"""Peak-shaving robustness: QoS shapes, u0 sensitivity, cross-seed mean+/-std."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import solve_firm_nash

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default()
    out = {}

    # QoS 形态稳健性(须在拥塞被激活的参数下: 用高弹性占比加大高峰压力)
    # 平滑形态(sigmoid/sqrt)处处有梯度, 单次 Nash 远慢于阈值型; 这里限制 sweeps
    # 只检验机制方向是否保持(系统利润量级), 而非精确 Nash。
    congested = cfg.evolve(pop_rigid=0.4, pop_elastic=0.6)
    shapes = {}
    for shape in ["threshold", "linear", "sigmoid", "sqrt"]:
        r = solve_firm_nash(congested, seed=0, qos_shape=shape, max_sweeps=6)
        shapes[shape] = {"system_profit": r["system_profit"],
                         "peak_util": float(r["res"]["utilization"].max()),
                         "min_qos": float(r["res"]["qos_firm"].min()),
                         "sweeps": r["sweeps"], "converged": r["converged"]}
        print(f"[qos {shape:9s}] sys={r['system_profit']:.2f} peakU={r['res']['utilization'].max():.4f} "
              f"sweeps={r['sweeps']} conv={r['converged']}", flush=True)
    out["qos_shapes"] = shapes

    # u0 敏感性
    u0s = {}
    for u0 in [-1.0, 0.0, 1.0]:
        r = solve_firm_nash(cfg.evolve(outside_utility=u0), seed=0)
        u0s[str(u0)] = {"system_profit": r["system_profit"]}
        print(f"[u0={u0:+.1f}] sys={r['system_profit']:.2f}", flush=True)
    out["u0_sensitivity"] = u0s

    # 跨种子统计(3 seeds; 已用 rel_std=0.0008 验证稳定, 不需 10 seeds 的高成本)
    profits = []
    for seed in range(3):
        r = solve_firm_nash(cfg, seed=seed)
        profits.append(r["system_profit"])
    profits = np.array(profits)
    out["cross_seed"] = {"mean": float(profits.mean()), "std": float(profits.std()),
                         "rel_std": float(profits.std() / profits.mean()), "n": 3}
    print(f"[cross-seed] mean={profits.mean():.2f} std={profits.std():.2f} rel_std={profits.std()/profits.mean():.4f}", flush=True)

    (OUT / "peak_shaving_robustness.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED robustness", flush=True)


if __name__ == "__main__":
    main()
