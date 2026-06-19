"""Helpers for SMPT-oriented peak-shaving diagnostics."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import (
    MarketState,
    FIXED_POINT_MAX_ITER,
    FIXED_POINT_TOL,
    QOS_DAMPING,
    _firm_loads,
    choice_shares_with_exit,
    channel_demand,
    inclusive_value,
    qos_factor,
    solve_market_fixed_point,
    system_profit,
)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "artifacts" / "peak_shaving" / "20260618"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260619_smpt"
FIG = ROOT / "figures" / "peak_shaving_smpt"
CAP = np.array([300.0, 120.0])
QOS_SHAPE = "sigmoid"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def congested_base() -> PeakShavingConfig:
    return PeakShavingConfig.default().evolve(firm_capacity=CAP, pop_rigid=0.4, pop_elastic=0.6)


def load_policy_vectors() -> dict[str, list[list[float]]]:
    congested = load_json(SRC / "peak_shaving_congested_fp.json")
    coarse = load_json(SRC / "peak_shaving_fp_dynamic_converged.json")
    fine = load_json(SRC / "peak_shaving_fp_dynamic_converged_fine.json")
    return {
        "uniform": congested["uniform"]["firm_params"],
        "dynamic_coarse": coarse["firm_params"],
        "dynamic_fine": fine["firm_params"],
    }


def discount_only_params(params: FirmParams) -> FirmParams:
    return FirmParams(params.wbar, min(params.delta, 0.0), params.pdbar, min(params.delta_d, 0.0))


def peak_only_params(params: FirmParams) -> FirmParams:
    return FirmParams(params.wbar, max(params.delta, 0.0), params.pdbar, max(params.delta_d, 0.0))


def params_from_vectors(vectors: list[list[float]]) -> list[FirmParams]:
    return [FirmParams.from_vector(np.asarray(v, dtype=float)) for v in vectors]


def vectors_from_params(params: list[FirmParams]) -> list[list[float]]:
    return [p.to_vector().tolist() for p in params]


def evaluate_params(
    case: str,
    params: list[FirmParams],
    cfg: PeakShavingConfig | None = None,
    static_shape: bool = False,
) -> dict[str, Any]:
    cfg = cfg or congested_base()
    if static_shape:
        cfg = cfg.evolve(load_shape_hat=np.zeros(cfg.num_periods))
    wholesale = np.vstack([params[0].wholesale(cfg), params[1].wholesale(cfg)])
    direct = np.vstack([params[0].direct(cfg), params[1].direct(cfg)])
    state, res = intermediary_best_response(wholesale, direct, cfg, qos_shape=QOS_SHAPE)
    return record_from_state(case, state, res, cfg)


def record_from_state(case: str, state: MarketState, res: dict[str, Any], cfg: PeakShavingConfig) -> dict[str, Any]:
    prices = res["prices"]
    demand = res["demand"]
    qos = res["qos_channel"]
    served = demand * qos
    exit_rigid = choice_shares_with_exit(prices, qos, cfg, "rigid")[1]
    exit_elastic = choice_shares_with_exit(prices, qos, cfg, "elastic")[1]
    avg_price = float(np.sum(prices * demand) / max(np.sum(demand), 1e-12))
    weighted_iv = (
        cfg.pop_rigid * inclusive_value(prices, qos, cfg, "rigid")
        + cfg.pop_elastic * inclusive_value(prices, qos, cfg, "elastic")
    )
    return {
        "case": case,
        "prices": prices,
        "routing": state.routing,
        "utilization": res["utilization"],
        "qos_firm": res["qos_firm"],
        "system_profit": system_profit(state, res, cfg),
        "peak_utilization": float(res["utilization"].max()),
        "minimum_qos": float(res["qos_firm"].min()),
        "served_volume": float(np.sum(served) * cfg.period_hours),
        "average_paid_price": avg_price,
        "exit_probability_rigid": exit_rigid,
        "exit_probability_elastic": exit_elastic,
        "weighted_inclusive_value": weighted_iv,
        "fixed_point_converged": bool(res["converged"]),
        "fixed_point_iterations": int(res["iterations"]),
    }


def admitted_fraction_for_threshold(utilization: np.ndarray, threshold: float) -> np.ndarray:
    peak_by_period = np.max(utilization, axis=0)
    return np.minimum(1.0, threshold / np.maximum(peak_by_period, 1e-12))


def summarize_records(records: list[dict[str, float]], reference_case: str) -> dict[str, dict[str, float]]:
    ref = next(r for r in records if r["case"] == reference_case)
    out = {}
    for rec in records:
        out[rec["case"]] = {
            "profit_gain_pct_vs_reference": 100.0 * (rec["system_profit"] - ref["system_profit"]) / abs(ref["system_profit"]),
            "qos_gain_vs_reference": rec["minimum_qos"] - ref["minimum_qos"],
            "peak_reduction_vs_reference": ref["peak_utilization"] - rec["peak_utilization"],
        }
    return out


def build_phase_grid(capacity_scales: list[float], alpha_scales: list[float]) -> list[dict[str, float]]:
    return [
        {"capacity_scale": float(c), "alpha_scale": float(a)}
        for c in capacity_scales
        for a in alpha_scales
    ]


def trace_fixed_point_residuals(
    prices: np.ndarray,
    routing: np.ndarray,
    cfg: PeakShavingConfig,
    qos_shape: str = QOS_SHAPE,
    initial_qos: float = 1.0,
    damping: float = QOS_DAMPING,
) -> dict[str, Any]:
    qos_firm = np.full((2, cfg.num_periods), float(initial_qos))
    residuals: list[float] = []
    converged = False
    for _ in range(1, FIXED_POINT_MAX_ITER + 1):
        qos_channel = np.vstack([np.sum(routing * qos_firm, axis=0)[None, :], qos_firm])
        demand = channel_demand(prices, qos_channel, cfg)
        loads = _firm_loads(demand, routing)
        util = loads / np.maximum(cfg.firm_capacity[:, None], 1e-8)
        target = qos_factor(util, cfg, qos_shape)
        residual = float(np.max(np.abs(target - qos_firm)))
        residuals.append(residual)
        if residual <= FIXED_POINT_TOL:
            converged = True
            break
        qos_firm = damping * target + (1.0 - damping) * qos_firm
    return {
        "iterations": len(residuals),
        "final_residual": residuals[-1],
        "max_residual": max(residuals),
        "converged": converged,
        "initial_qos": float(initial_qos),
        "damping": float(damping),
        "residuals": residuals,
    }


def make_baseline_param_sets() -> dict[str, list[FirmParams]]:
    policies = load_policy_vectors()
    uniform = params_from_vectors(policies["uniform"])
    coarse = params_from_vectors(policies["dynamic_coarse"])
    return {
        "optimal_static_qos_routing": uniform,
        "off_peak_discount_only": [discount_only_params(p) for p in coarse],
        "peak_surcharge_only": [peak_only_params(p) for p in coarse],
        "dynamic_coarse": coarse,
        "dynamic_fine": params_from_vectors(policies["dynamic_fine"]),
    }


def evaluate_equal_routing(case: str, params: list[FirmParams], cfg: PeakShavingConfig | None = None) -> dict[str, Any]:
    cfg = cfg or congested_base()
    wholesale = np.vstack([params[0].wholesale(cfg), params[1].wholesale(cfg)])
    direct = np.vstack([params[0].direct(cfg), params[1].direct(cfg)])
    state, _ = intermediary_best_response(wholesale, direct, cfg, qos_shape=QOS_SHAPE)
    equal_state = MarketState(state.retail, state.direct, state.wholesale, np.full((2, cfg.num_periods), 0.5))
    res = solve_market_fixed_point(equal_state.channel_prices(), equal_state.routing, cfg, QOS_SHAPE)
    return record_from_state(case, equal_state, res, cfg)


def admission_control_record(reference: dict[str, Any], threshold: float) -> dict[str, Any]:
    fractions = admitted_fraction_for_threshold(reference["utilization"], threshold)
    return {
        "case": "admission_control_uniform",
        "admitted_fraction_min": float(np.min(fractions)),
        "admitted_fraction_mean": float(np.mean(fractions)),
        "peak_utilization_target": float(threshold),
        "minimum_qos_reference": float(reference["minimum_qos"]),
        "note": "Diagnostic only: period-level admission fractions needed to keep peak utilization below threshold.",
    }
