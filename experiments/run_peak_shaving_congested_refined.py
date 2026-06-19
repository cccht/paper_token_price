"""Refined congested-regime peak-shaving run. Uses a finer firm grid (esp. on the
dynamic-strength dimensions delta/delta_d) so P1/P4 get a fair adjudication and
P2/P3 are confirmed at higher resolution. Real solver output only.

This module overrides the firm grid resolution locally (monkeypatch of the grid
arrays is avoided; instead we call a refined best-response copy) to keep the
library default coarse for speed while this script does the careful run.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import (
    FirmParams, intermediary_best_response, expand_price)
from pricing_sim.peak_shaving_market import (
    firm_profit, intermediary_profit, system_profit, type_channel_demand)

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"
CONGESTED_CAP = np.array([300.0, 120.0])
QOS = "sigmoid"


def _refined_firm_br(idx, params, config, qos_shape):
    """Finer grid than the library default: delta/delta_d at 5 levels."""
    other = 1 - idx
    wb_lo, wb_hi = config.wholesale_lower, config.wholesale_upper
    wbar_grid = np.unique(np.concatenate([np.linspace(wb_lo + 0.02, wb_hi - 0.02, 3),
                                          [params[idx].wbar]]))
    pdbar_grid = np.unique(np.concatenate([np.linspace(0.60, 1.6, 3), [params[idx].pdbar]]))
    delta_grid = np.linspace(-0.4, 0.4, 5)
    deltad_grid = np.linspace(-0.4, 0.4, 5)
    best_vec = params[idx].to_vector()

    def ev(vec):
        fps = [None, None]; fps[idx] = FirmParams.from_vector(vec); fps[other] = params[other]
        w = np.vstack([fps[0].wholesale(config), fps[1].wholesale(config)])
        pd = np.vstack([fps[0].direct(config), fps[1].direct(config)])
        st, res = intermediary_best_response(w, pd, config, qos_shape=qos_shape)
        return firm_profit(idx, st, res, config)

    best_val = ev(best_vec)
    for wb, dl, pdb, dld in itertools.product(wbar_grid, delta_grid, pdbar_grid, deltad_grid):
        v = np.array([wb, dl, pdb, dld]); val = ev(v)
        if val > best_val:
            best_val = val; best_vec = v
    return FirmParams.from_vector(best_vec)


def _refined_nash(config, dynamic, max_sweeps=6, qos_shape=QOS):
    params = [FirmParams(0.40, 0.0, 0.85, 0.0), FirmParams(0.45, 0.0, 0.88, 0.0)]
    if not dynamic:
        config = config.evolve(load_shape_hat=np.zeros(config.num_periods))
    damping = 0.7
    for sweep in range(1, max_sweeps + 1):
        old = np.concatenate([p.to_vector() for p in params])
        for idx in range(2):
            br = _refined_firm_br(idx, params, config, qos_shape)
            blended = damping * br.to_vector() + (1 - damping) * params[idx].to_vector()
            params[idx] = FirmParams.from_vector(blended)
        change = float(np.max(np.abs(np.concatenate([p.to_vector() for p in params]) - old)))
        print(f"   [sweep {sweep}] change={change:.4f}", flush=True)
        if change < 3e-3:
            break
    w = np.vstack([params[0].wholesale(config), params[1].wholesale(config)])
    pd = np.vstack([params[0].direct(config), params[1].direct(config)])
    st, res = intermediary_best_response(w, pd, config, qos_shape=qos_shape)
    return params, st, res, sweep


def _centroid(d_t, cfg):
    t = np.arange(cfg.num_periods)
    return float(np.sum(t * d_t) / max(np.sum(d_t), 1e-12))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default().evolve(firm_capacity=CONGESTED_CAP,
                                             pop_rigid=0.4, pop_elastic=0.6)
    out = {"regime": "congested_refined", "firm_capacity": CONGESTED_CAP.tolist(),
           "qos_shape": QOS, "firm_grid": "wbar3 x delta5 x pdbar3 x deltad5"}

    print("=== uniform ===", flush=True)
    pu, su, ru, swu = _refined_nash(cfg, dynamic=False)
    print("=== dynamic ===", flush=True)
    pd_, sd, rd, swd = _refined_nash(cfg, dynamic=True)

    for name, params, st, res, sw in [("uniform", pu, su, ru, swu), ("dynamic", pd_, sd, rd, swd)]:
        util = res["utilization"]
        out[name] = {"system_profit": system_profit(st, res, cfg),
                     "peak_util": float(util.max()),
                     "min_qos_firm": float(res["qos_firm"].min()),
                     "firm_params": [p.to_vector().tolist() for p in params],
                     "sweeps": sw}
        print(f"[{name}] sys={system_profit(st,res,cfg):.2f} peakU={util.max():.4f} "
              f"minQoS={res['qos_firm'].min():.4f} sweeps={sw}", flush=True)

    p2 = out["dynamic"]["peak_util"] < out["uniform"]["peak_util"]
    p3 = out["dynamic"]["min_qos_firm"] > out["uniform"]["min_qos_firm"]
    gain = 100 * (out["dynamic"]["system_profit"] - out["uniform"]["system_profit"]) / abs(out["uniform"]["system_profit"])
    # P1
    p1 = {}
    for name, st, res in [("uniform", su, ru), ("dynamic", sd, rd)]:
        prices = res["prices"]; qos = res["qos_channel"]
        dR = type_channel_demand(prices, qos, cfg, "rigid").sum(axis=0)
        dE = type_channel_demand(prices, qos, cfg, "elastic").sum(axis=0)
        p1[name] = {"rigid_centroid": _centroid(dR, cfg), "elastic_centroid": _centroid(dE, cfg)}
    eshift = p1["dynamic"]["elastic_centroid"] - p1["uniform"]["elastic_centroid"]
    rshift = p1["dynamic"]["rigid_centroid"] - p1["uniform"]["rigid_centroid"]
    dA, dB = abs(pd_[0].to_vector()[1]), abs(pd_[1].to_vector()[1])
    out["predictions"] = {
        "P2_peak_shaving": bool(p2), "P3_qos_improve": bool(p3), "profit_gain_pct": gain,
        "P1_migration": {"elastic_shift": eshift, "rigid_shift": rshift, "holds": bool(abs(eshift) > abs(rshift))},
        "P4_small_firm": {"delta_A": dA, "delta_B": dB, "holds": bool(dB > dA)},
    }
    print(f"[P2]{p2} [P3]{p3} gain={gain:+.2f}% "
          f"[P1] e={eshift:+.3f} r={rshift:+.3f} hold={abs(eshift)>abs(rshift)} "
          f"[P4] dB={dB:.3f} dA={dA:.3f} hold={dB>dA}", flush=True)
    (OUT / "peak_shaving_congested_refined.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", flush=True)


if __name__ == "__main__":
    main()
