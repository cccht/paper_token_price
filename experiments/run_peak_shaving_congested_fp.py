"""Fictitious-play solver for the congested-regime firm Nash, to tame the
best-response limit cycle seen with naive damped best response.

Continuous fictitious play: each firm best-responds (via the existing coarse
grid) to the OTHER firm's running-average strategy, not its latest strategy.
The running average is the empirical play distribution's mean and damps cycles.
We track the time-average strategy profile, which is the standard FP convergence
object. Standalone — does not modify the library (keeps the verified uncongested
path intact). Real solver output only.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
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


def _firm_grid():
    # Moderate grid: keeps delta (dynamic strength) at 4 levels so P4 can be
    # adjudicated, but trims base-price levels to 2 to fit runtime. 2x4x2x4=64.
    wb = np.linspace(0.30, 0.85, 2)
    dl = np.linspace(-0.4, 0.4, 4)
    pdb = np.linspace(0.70, 1.5, 2)
    dld = np.linspace(-0.4, 0.4, 4)
    return list(itertools.product(wb, dl, pdb, dld))


GRID = _firm_grid()


def _best_response_to(idx, other_params: FirmParams, config, qos_shape):
    """Best response of firm idx against a FIXED other-firm strategy (the running
    average, in fictitious play). Returns (FirmParams, profit)."""
    other = 1 - idx
    best_vec, best_val = None, -np.inf
    for cand in GRID:
        fps = [None, None]
        fps[idx] = FirmParams.from_vector(np.array(cand))
        fps[other] = other_params
        w = np.vstack([fps[0].wholesale(config), fps[1].wholesale(config)])
        pd = np.vstack([fps[0].direct(config), fps[1].direct(config)])
        st, res = intermediary_best_response(w, pd, config, qos_shape=qos_shape)
        val = firm_profit(idx, st, res, config)
        if val > best_val:
            best_val, best_vec = val, np.array(cand)
    return FirmParams.from_vector(best_vec), best_val


def fictitious_play(config, dynamic, max_rounds=10, qos_shape=QOS, tol=5e-3):
    if not dynamic:
        config = config.evolve(load_shape_hat=np.zeros(config.num_periods))
    # running average of each firm's strategy (the FP belief)
    avg = [np.array([0.40, 0.0, 0.85, 0.0]), np.array([0.45, 0.0, 0.88, 0.0])]
    history = [list(avg)]
    converged = False
    for rnd in range(1, max_rounds + 1):
        prev_avg = [a.copy() for a in avg]
        br = [None, None]
        for idx in range(2):
            other_avg = FirmParams.from_vector(avg[1 - idx])
            br[idx], _ = _best_response_to(idx, other_avg, config, qos_shape)
        # update running averages toward the new best responses (weight 1/(rnd+1))
        wgt = 1.0 / (rnd + 1.0)
        for idx in range(2):
            avg[idx] = (1 - wgt) * avg[idx] + wgt * br[idx].to_vector()
        change = max(float(np.max(np.abs(avg[i] - prev_avg[i]))) for i in range(2))
        history.append([a.copy() for a in avg])
        print(f"   [round {rnd}] avg_change={change:.4f}", flush=True)
        if change < tol:
            converged = True
            break
    params = [FirmParams.from_vector(avg[0]), FirmParams.from_vector(avg[1])]
    w = np.vstack([params[0].wholesale(config), params[1].wholesale(config)])
    pd = np.vstack([params[0].direct(config), params[1].direct(config)])
    st, res = intermediary_best_response(w, pd, config, qos_shape=qos_shape)
    return params, st, res, rnd, converged


def _centroid(d_t, cfg):
    t = np.arange(cfg.num_periods)
    return float(np.sum(t * d_t) / max(np.sum(d_t), 1e-12))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default().evolve(firm_capacity=CONGESTED_CAP,
                                             pop_rigid=0.4, pop_elastic=0.6)
    out = {"regime": "congested_fictitious_play", "firm_capacity": CONGESTED_CAP.tolist(),
           "qos_shape": QOS}

    t0 = time.time()
    print("=== uniform (FP) ===", flush=True)
    pu, su, ru, ru_rnd, uc = fictitious_play(cfg, dynamic=False)
    print("=== dynamic (FP) ===", flush=True)
    pd_, sd, rd, rd_rnd, dc = fictitious_play(cfg, dynamic=True)

    for name, params, st, res, rnd, conv in [
        ("uniform", pu, su, ru, ru_rnd, uc), ("dynamic", pd_, sd, rd, rd_rnd, dc)]:
        util = res["utilization"]
        out[name] = {"system_profit": system_profit(st, res, cfg),
                     "peak_util": float(util.max()),
                     "min_qos_firm": float(res["qos_firm"].min()),
                     "firm_params": [p.to_vector().tolist() for p in params],
                     "rounds": rnd, "converged": conv}
        print(f"[{name}] sys={system_profit(st,res,cfg):.2f} peakU={util.max():.4f} "
              f"minQoS={res['qos_firm'].min():.4f} rounds={rnd} conv={conv}", flush=True)

    p2 = out["dynamic"]["peak_util"] < out["uniform"]["peak_util"]
    p3 = out["dynamic"]["min_qos_firm"] > out["uniform"]["min_qos_firm"]
    gain = 100 * (out["dynamic"]["system_profit"] - out["uniform"]["system_profit"]) / abs(out["uniform"]["system_profit"])
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
        "both_converged": bool(out["uniform"]["converged"] and out["dynamic"]["converged"]),
    }
    print(f"[total {time.time()-t0:.0f}s] P2={p2} P3={p3} gain={gain:+.2f}% "
          f"P1_hold={abs(eshift)>abs(rshift)}(e{eshift:+.3f}/r{rshift:+.3f}) "
          f"P4_hold={dB>dA}(dB{dB:.3f}/dA{dA:.3f}) bothConv={out['predictions']['both_converged']}", flush=True)
    (OUT / "peak_shaving_congested_fp.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", flush=True)


if __name__ == "__main__":
    main()
