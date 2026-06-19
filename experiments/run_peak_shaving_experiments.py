"""Peak-shaving dynamic pricing experiments (P1-P5). Real solver outputs only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import solve_firm_nash
from pricing_sim.peak_shaving_market import type_channel_demand

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"


def _demand_centroid(demand_t: np.ndarray, config: PeakShavingConfig) -> float:
    """时段重心(加权平均时段索引), 用于度量负载迁移。"""
    t = np.arange(config.num_periods)
    return float(np.sum(t * demand_t) / max(np.sum(demand_t), 1e-12))


def uniform_vs_dynamic(config: PeakShavingConfig) -> dict:
    # 统一定价: 通过把 load_shape_hat 置零强制 delta 无效(等价 delta=0)
    uni_cfg = config.evolve(load_shape_hat=np.zeros(config.num_periods))
    uni = solve_firm_nash(uni_cfg, seed=0)
    dyn = solve_firm_nash(config, seed=0)
    return {"uniform": uni, "dynamic": dyn}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default()

    # --- 实验1: 统一 vs 动态 (P2, P3) ---
    cmp = uniform_vs_dynamic(cfg)
    summary = {}
    for name, r in cmp.items():
        util = r["res"]["utilization"]
        summary[name] = {
            "system_profit": r["system_profit"],
            "peak_util": float(util.max()),
            "min_qos_firm": float(r["res"]["qos_firm"].min()),
            "converged": r["converged"],
            "firm_params": r["firm_params"],
        }
        print(f"[exp1 {name}] sys={r['system_profit']:.2f} peakU={util.max():.4f} "
              f"minQoS={r['res']['qos_firm'].min():.4f} conv={r['converged']}", flush=True)

    # --- 实验2: 负载迁移 (P1: 弹性迁移, 刚性不动) ---
    p1 = {}
    for name, r in cmp.items():
        prices = r["res"]["prices"]; qos = r["res"]["qos_channel"]
        dR = type_channel_demand(prices, qos, cfg, "rigid").sum(axis=0)    # (T,)
        dE = type_channel_demand(prices, qos, cfg, "elastic").sum(axis=0)  # (T,)
        p1[name] = {"rigid_centroid": _demand_centroid(dR, cfg),
                    "elastic_centroid": _demand_centroid(dE, cfg)}
    rigid_shift = p1["dynamic"]["rigid_centroid"] - p1["uniform"]["rigid_centroid"]
    elastic_shift = p1["dynamic"]["elastic_centroid"] - p1["uniform"]["elastic_centroid"]
    print(f"[exp2 P1] rigid_centroid_shift={rigid_shift:+.4f} elastic_centroid_shift={elastic_shift:+.4f} "
          f"P1_holds={abs(elastic_shift) > abs(rigid_shift)}", flush=True)
    summary["P1_migration"] = {"rigid_shift": rigid_shift, "elastic_shift": elastic_shift,
                               "P1_holds": bool(abs(elastic_shift) > abs(rigid_shift)), **p1}

    # --- 实验3: 小厂vs大厂动态强度 (P4) ---
    dyn = cmp["dynamic"]
    fp = dyn["firm_params"]
    delta_A, delta_B = abs(fp[0][1]), abs(fp[1][1])
    print(f"[exp3] delta_A(大厂)={delta_A:.4f} delta_B(小厂)={delta_B:.4f} "
          f"P4_holds={delta_B > delta_A}", flush=True)
    summary["P4_delta"] = {"delta_A": delta_A, "delta_B": delta_B, "P4_holds": bool(delta_B > delta_A)}

    # --- 实验4: 弹性占比扫描 (P5) ---
    sweep = []
    for pe in [0.0, 0.2, 0.4, 0.6, 0.8]:
        c = cfg.evolve(pop_rigid=1 - pe, pop_elastic=pe)
        uni = solve_firm_nash(c.evolve(load_shape_hat=np.zeros(c.num_periods)), seed=0)
        dyn = solve_firm_nash(c, seed=0)
        gain = 100 * (dyn["system_profit"] - uni["system_profit"]) / abs(uni["system_profit"])
        sweep.append({"pop_elastic": pe, "uniform": uni["system_profit"],
                      "dynamic": dyn["system_profit"], "gain_pct": gain})
        print(f"[exp4 pe={pe}] uni={uni['system_profit']:.1f} dyn={dyn['system_profit']:.1f} gain={gain:+.2f}%", flush=True)
    summary["elastic_sweep"] = sweep

    (OUT / "peak_shaving_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", OUT / "peak_shaving_summary.json", flush=True)


if __name__ == "__main__":
    main()
