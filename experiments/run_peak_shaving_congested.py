"""Peak-shaving in the CONGESTED regime (tight capacity). The baseline config is
uncongested (peak util ~0.26), so peak-shaving/QoS effects are trivial there.
Tightening capacity to G=(300,120) lifts peak utilization to ~0.91 under uniform
pricing, activating the congestion mechanism. Real solver outputs only.
"""
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
CONGESTED_CAP = np.array([300.0, 120.0])  # cap_scale=0.20, peak util ~0.91 uniform


def _centroid(d_t, cfg):
    t = np.arange(cfg.num_periods)
    return float(np.sum(t * d_t) / max(np.sum(d_t), 1e-12))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default().evolve(firm_capacity=CONGESTED_CAP,
                                             pop_rigid=0.4, pop_elastic=0.6)
    summary = {"regime": "congested", "firm_capacity": CONGESTED_CAP.tolist(),
               "pop_elastic": 0.6}

    uni = solve_firm_nash(cfg.evolve(load_shape_hat=np.zeros(cfg.num_periods)),
                          seed=0, max_sweeps=3, n_starts=1)
    dyn = solve_firm_nash(cfg, seed=0, max_sweeps=3, n_starts=1)
    for name, r in [("uniform", uni), ("dynamic", dyn)]:
        util = r["res"]["utilization"]
        summary[name] = {"system_profit": r["system_profit"],
                         "peak_util": float(util.max()),
                         "min_qos_firm": float(r["res"]["qos_firm"].min()),
                         "converged": r["converged"], "firm_params": r["firm_params"]}
        print(f"[{name}] sys={r['system_profit']:.2f} peakU={util.max():.4f} "
              f"minQoS={r['res']['qos_firm'].min():.4f} conv={r['converged']}", flush=True)

    # P2 削峰: 动态 peakU 应低于统一
    p2 = summary["dynamic"]["peak_util"] < summary["uniform"]["peak_util"]
    # P3 刚性QoS改善: 动态 minQoS 应高于统一
    p3 = summary["dynamic"]["min_qos_firm"] > summary["uniform"]["min_qos_firm"]
    gain = 100 * (dyn["system_profit"] - uni["system_profit"]) / abs(uni["system_profit"])
    print(f"[P2 削峰] dyn_peakU<uni_peakU = {p2}", flush=True)
    print(f"[P3 QoS改善] dyn_minQoS>uni_minQoS = {p3}", flush=True)
    print(f"[利润增益] {gain:+.2f}%", flush=True)

    # P1 负载迁移
    p1 = {}
    for name, r in [("uniform", uni), ("dynamic", dyn)]:
        prices = r["res"]["prices"]; qos = r["res"]["qos_channel"]
        dR = type_channel_demand(prices, qos, cfg, "rigid").sum(axis=0)
        dE = type_channel_demand(prices, qos, cfg, "elastic").sum(axis=0)
        p1[name] = {"rigid_centroid": _centroid(dR, cfg), "elastic_centroid": _centroid(dE, cfg)}
    rshift = p1["dynamic"]["rigid_centroid"] - p1["uniform"]["rigid_centroid"]
    eshift = p1["dynamic"]["elastic_centroid"] - p1["uniform"]["elastic_centroid"]
    print(f"[P1 迁移] elastic_shift={eshift:+.4f} rigid_shift={rshift:+.4f} holds={abs(eshift)>abs(rshift)}", flush=True)

    # P4 小厂动态强度
    dA, dB = abs(dyn["firm_params"][0][1]), abs(dyn["firm_params"][1][1])
    print(f"[P4 小厂] delta_B={dB:.4f} > delta_A={dA:.4f} = {dB>dA}", flush=True)

    summary["predictions"] = {
        "P1_migration": {"elastic_shift": eshift, "rigid_shift": rshift, "holds": bool(abs(eshift) > abs(rshift)), **p1},
        "P2_peak_shaving": bool(p2),
        "P3_qos_improve": bool(p3),
        "P4_small_firm_dynamic": {"delta_A": dA, "delta_B": dB, "holds": bool(dB > dA)},
        "profit_gain_pct": gain,
    }
    (OUT / "peak_shaving_congested.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", OUT / "peak_shaving_congested.json", flush=True)


if __name__ == "__main__":
    main()
