"""Dynamic-FP convergence chase with a regret-based stopping criterion and
round-by-round checkpointing (so a reaped run can resume). Congested regime.
Real output only.
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
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import firm_profit, system_profit, type_channel_demand

import os

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"
TAG = os.environ.get("FP_TAG", "")  # set FP_TAG=fine for a finer-grid replication
CKPT = OUT / f"fp_dynamic_ckpt{('_' + TAG) if TAG else ''}.json"
CAP = np.array([300.0, 120.0])
# Grid resolution: default coarse (delta 4 levels, base 2); FP_TAG=fine uses
# delta 5 levels and base 3 to test robustness of the +9.3% / delta_A>>delta_B result.
if TAG == "fine":
    GRID = list(itertools.product(np.linspace(0.27, 0.88, 3), np.linspace(-0.4, 0.4, 5),
                                  np.linspace(0.60, 1.6, 3), np.linspace(-0.4, 0.4, 5)))
else:
    GRID = list(itertools.product(np.linspace(0.30, 0.85, 2), np.linspace(-0.4, 0.4, 4),
                                  np.linspace(0.70, 1.5, 2), np.linspace(-0.4, 0.4, 4)))


def _cfg():
    return PeakShavingConfig.default().evolve(firm_capacity=CAP, pop_rigid=0.4, pop_elastic=0.6)


def _eval(idx, fps, cfg):
    w = np.vstack([fps[0].wholesale(cfg), fps[1].wholesale(cfg)])
    pd = np.vstack([fps[0].direct(cfg), fps[1].direct(cfg)])
    st, res = intermediary_best_response(w, pd, cfg, qos_shape="sigmoid")
    return firm_profit(idx, st, res, cfg), st, res


def _br(idx, other_fp, cfg):
    o = 1 - idx
    best_v, best_val = None, -9e9
    for c in GRID:
        fps = [None, None]; fps[idx] = FirmParams.from_vector(np.array(c)); fps[o] = other_fp
        v, _, _ = _eval(idx, fps, cfg)
        if v > best_val:
            best_val, best_v = v, np.array(c)
    return best_v, best_val


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = _cfg()
    if CKPT.exists():
        st = json.loads(CKPT.read_text())
        avg = [np.array(st["avg0"]), np.array(st["avg1"])]
        start = st["round"] + 1
        print(f"resume from round {start}", flush=True)
    else:
        avg = [np.array([0.40, 0., 0.85, 0.]), np.array([0.45, 0., 0.88, 0.])]
        start = 1
    MAXR = 40
    for rnd in range(start, MAXR + 1):
        fps_avg = [FirmParams.from_vector(avg[0]), FirmParams.from_vector(avg[1])]
        cur = [_eval(i, fps_avg, cfg)[0] for i in range(2)]
        nb, reg = [], []
        for i in range(2):
            bv, bval = _br(i, FirmParams.from_vector(avg[1 - i]), cfg)
            nb.append(bv); reg.append(bval - cur[i])
        wgt = 1.0 / (rnd + 1.0)
        for i in range(2):
            avg[i] = (1 - wgt) * avg[i] + wgt * nb[i]
        maxreg = max(reg)
        CKPT.write_text(json.dumps({"round": rnd, "avg0": avg[0].tolist(),
                                    "avg1": avg[1].tolist(), "maxreg": maxreg}))
        print(f"round {rnd} maxregret={maxreg:.2f}", flush=True)
        if maxreg < 5.0:
            print(f"CONVERGED round {rnd} maxregret={maxreg:.3f}", flush=True)
            break

    fps = [FirmParams.from_vector(avg[0]), FirmParams.from_vector(avg[1])]
    _, st, res = _eval(0, fps, cfg)
    dE = type_channel_demand(res["prices"], res["qos_channel"], cfg, "elastic").sum(axis=0)
    dR = type_channel_demand(res["prices"], res["qos_channel"], cfg, "rigid").sum(axis=0)
    t = np.arange(cfg.num_periods)
    out = {"system_profit": system_profit(st, res, cfg),
           "peak_util": float(res["utilization"].max()),
           "min_qos": float(res["qos_firm"].min()),
           "firm_params": [avg[0].tolist(), avg[1].tolist()],
           "elastic_centroid": float(np.sum(t * dE) / dE.sum()),
           "rigid_centroid": float(np.sum(t * dR) / dR.sum()),
           "delta_A": abs(avg[0][1]), "delta_B": abs(avg[1][1])}
    (OUT / f"peak_shaving_fp_dynamic_converged{('_' + TAG) if TAG else ''}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"FINAL sys={out['system_profit']:.1f} peakU={out['peak_util']:.3f} "
          f"minQoS={out['min_qos']:.3f} eC={out['elastic_centroid']:.3f} rC={out['rigid_centroid']:.3f} "
          f"dA={out['delta_A']:.3f} dB={out['delta_B']:.3f}", flush=True)
    print("SAVED", flush=True)


if __name__ == "__main__":
    main()
