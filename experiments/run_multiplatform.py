"""
Multi-Platform Token Dynamic Pricing Game
==========================================
Three-layer market with capacity exit mechanism.

Participants:
  - Manufacturers (A,B,C): own GPU, set direct prices + capacity
  - Intermediary (I): buys from manufacturers, resells with markup
  - Users: choose (channel, period) from 32 alternatives

Equilibrium: Best-Response Dynamics with capacity adjustment.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

# ══════════════════════════════════════════════════════
# Parameters
# ══════════════════════════════════════════════════════

NUM_PERIODS = 8
PERIOD_HOURS = 3.0
NUM_MFG = 3
MFG_NAMES = ["A", "B", "C"]

MFG_CAPACITY = np.array([500.0, 300.0, 150.0])
MFG_CAPACITY_MIN = np.array([50.0, 30.0, 15.0])
MFG_COST = np.array([0.35, 0.38, 0.40])
MFG_BRAND = np.array([1.0, 0.7, 0.5])
EXIT_COST_RATE = 0.30

DEGRADE_THRESHOLD = 0.82
DEGRADE_KAPPA = 15.0

BASE_RIGID = np.array([200, 150, 300, 600, 800, 900, 700, 250], dtype=float)
RIGID_WTP = 1.80
RIGID_CHURN = 5.0
FLEX_BASE = 400.0
ALPHA = 3.5
P_REF = 0.80
PEAK_PREFERENCE = np.array([0.3, 0.2, 0.5, 0.8, 1.0, 1.0, 0.9, 0.4], dtype=float)
MARKET_GROWTH = 2.5
CHURN_FUTURE_COST = 0.60
DEGRADE_CHURN_FACTOR = 0.35

INTERMEDIARY_CONVENIENCE = 0.3
ROUTING_SENSITIVITY = 2.0
ROUTING_DEGRADE_AVOID = 3.0
USER_DEGRADE_SENSITIVITY = 1.0

RNG_SEED = 42
OUTPUT_DIR = PROJECT_ROOT / "figures_multi"


# ══════════════════════════════════════════════════════
# Core Functions
# ══════════════════════════════════════════════════════

def degradation_function(u: np.ndarray) -> np.ndarray:
    u = np.asarray(u, dtype=float)
    return np.where(u <= DEGRADE_THRESHOLD, 1.0,
                    np.exp(-DEGRADE_KAPPA * (u - DEGRADE_THRESHOLD) ** 2))


def compute_demands(
    p_direct: np.ndarray,
    p_intermediary: np.ndarray,
    routing: np.ndarray,
    g_active: np.ndarray,
) -> tuple[np.ndarray, ...]:
    """Compute demands across all channels with capacity constraints.

    Args:
        p_direct: (NUM_MFG, NUM_PERIODS) direct prices
        p_intermediary: (NUM_PERIODS,) intermediary retail prices
        routing: (NUM_MFG, NUM_PERIODS) routing weights (sum to 1 per period)
        g_active: (NUM_MFG, NUM_PERIODS) active GPU capacity per manufacturer per period

    Returns:
        shares, flex_demand, rigid_demand, mfg_served, mfg_util, mfg_phi
    """
    p_all = np.vstack([p_direct, p_intermediary.reshape(1, -1)])
    brand = np.concatenate([MFG_BRAND, [INTERMEDIARY_CONVENIENCE]])
    tau = np.log(PEAK_PREFERENCE + 1e-10)

    deg_penalty = np.zeros((NUM_MFG + 1, NUM_PERIODS))

    for _ in range(4):
        utility = (-ALPHA * (p_all - P_REF)
                   + np.log(brand.reshape(-1, 1) + 1e-10)
                   + tau.reshape(1, -1)
                   - USER_DEGRADE_SENSITIVITY * deg_penalty)
        utility -= np.max(utility)
        exp_u = np.exp(utility)
        shares = exp_u / np.sum(exp_u)

        avg_price = np.sum(shares * p_all)
        growth = 1.0 + MARKET_GROWTH * max(P_REF - avg_price, 0)
        flex_demand = FLEX_BASE * growth * shares

        rigid_demand = np.zeros((NUM_MFG + 1, NUM_PERIODS))
        for ch in range(NUM_MFG + 1):
            rigid_demand[ch] = BASE_RIGID * expit(RIGID_CHURN * (RIGID_WTP - p_all[ch]))

        mfg_served = np.zeros((NUM_MFG, NUM_PERIODS))
        for i in range(NUM_MFG):
            total_demand = (rigid_demand[i] + flex_demand[i]
                            + routing[i] * (rigid_demand[NUM_MFG] + flex_demand[NUM_MFG]))
            scale = np.minimum(g_active[i, :] / np.maximum(total_demand, 1e-10), 1.0)
            mfg_served[i] = total_demand * scale

        mfg_util = mfg_served / g_active
        mfg_phi = degradation_function(mfg_util)

        for i in range(NUM_MFG):
            deg_penalty[i] = 1.0 - mfg_phi[i]
        deg_penalty[NUM_MFG] = 1.0 - np.sum(routing * mfg_phi, axis=0)

    return shares, flex_demand, rigid_demand, mfg_served, mfg_util, mfg_phi


def manufacturer_profit(
    i: int,
    p_direct_all: np.ndarray,
    p_intermediary: np.ndarray,
    routing: np.ndarray,
    g_active: np.ndarray,
) -> float:
    """Profit for manufacturer i including exit cost for unused capacity."""
    _, _, rigid, served, _, mfg_phi = compute_demands(
        p_direct_all, p_intermediary, routing, g_active
    )
    phi_i = mfg_phi[i]
    w_i = MFG_COST[i]

    revenue = np.sum(p_direct_all[i] * phi_i * served[i] * PERIOD_HOURS)
    operating_cost = np.sum(w_i * g_active[i, :] * PERIOD_HOURS)
    churned = np.maximum(BASE_RIGID - rigid[i], 0)
    churn_cost = np.sum(churned * CHURN_FUTURE_COST * PERIOD_HOURS)
    degrade_cost = np.sum((1 - phi_i) * rigid[i] * DEGRADE_CHURN_FACTOR * PERIOD_HOURS)
    exit_cost = np.sum(EXIT_COST_RATE * (MFG_CAPACITY[i] - g_active[i, :]) * PERIOD_HOURS)

    return revenue - operating_cost - churn_cost - degrade_cost - exit_cost


def intermediary_profit(
    markup: np.ndarray,
    p_direct: np.ndarray,
    routing: np.ndarray,
    g_active: np.ndarray,
) -> float:
    """Intermediary profit = retail revenue - wholesale cost."""
    p_intermediary = np.sum(routing * p_direct, axis=0) + markup
    _, _, rigid, _, _, _ = compute_demands(
        p_direct, p_intermediary, routing, g_active
    )
    D_I = rigid[NUM_MFG]  # simplified: only rigid demand via intermediary
    # In full model, flex demand also goes through intermediary
    # Using total demand for more realistic profit
    shares, flex, _, _, _, _ = compute_demands(
        p_direct, p_intermediary, routing, g_active
    )
    D_I_total = rigid[NUM_MFG] + flex[NUM_MFG]

    retail_revenue = np.sum(p_intermediary * D_I_total * PERIOD_HOURS)
    wholesale_cost = np.sum(np.sum(routing * p_direct, axis=0) * D_I_total * PERIOD_HOURS)
    return retail_revenue - wholesale_cost


def optimize_intermediary(
    p_direct: np.ndarray,
    routing: np.ndarray,
    g_active: np.ndarray,
    n_trials: int = 10,
) -> np.ndarray:
    """Optimize intermediary markup given manufacturer prices and routing."""
    best_markup = np.full(NUM_PERIODS, 0.15)
    best_profit = -1e9

    for trial in range(n_trials):
        mu0 = (np.random.uniform(0.05, 0.5, NUM_PERIODS) if trial > 0
               else np.full(NUM_PERIODS, 0.15))
        bounds = [(0.01, 0.80)] * NUM_PERIODS

        def obj(mu):
            return -intermediary_profit(mu, p_direct, routing, g_active)

        try:
            res = minimize(obj, mu0, method='L-BFGS-B', bounds=bounds,
                           options={'maxiter': 2000})
            if -res.fun > best_profit:
                best_profit = -res.fun
                best_markup = res.x.copy()
        except Exception:
            pass

    return best_markup


def compute_routing(p_direct: np.ndarray, mfg_phi: np.ndarray) -> np.ndarray:
    """Routing weights: prefer cheaper + less degraded manufacturers."""
    routing = np.zeros((NUM_MFG, NUM_PERIODS))
    for t in range(NUM_PERIODS):
        util = -ROUTING_SENSITIVITY * p_direct[:, t] + ROUTING_DEGRADE_AVOID * mfg_phi[:, t]
        util -= np.max(util)
        exp_r = np.exp(util)
        routing[:, t] = exp_r / np.sum(exp_r)
    return routing


def compute_equilibrium(
    max_iter: int = 8,
    tol: float = 0.01,
    with_intermediary: bool = True,
) -> dict[str, Any]:
    """Find Nash equilibrium via best-response dynamics."""

    # Initialize
    p_direct = np.array([
        [0.45, 0.45, 0.60, 0.95, 1.15, 1.25, 1.05, 0.45],
        [0.50, 0.45, 0.65, 1.00, 1.10, 1.20, 1.00, 0.50],
        [0.42, 0.42, 0.50, 0.55, 0.60, 0.65, 0.58, 0.42],
    ])
    g_active = np.tile(MFG_CAPACITY.reshape(-1, 1), (1, NUM_PERIODS))
    routing = np.ones((NUM_MFG, NUM_PERIODS)) / NUM_MFG
    markup = np.zeros(NUM_PERIODS)

    for iteration in range(max_iter):
        p_old = p_direct.copy()
        g_old = g_active.copy()

        # Update routing
        _, _, _, _, _, mfg_phi = compute_demands(
            p_direct,
            np.full(NUM_PERIODS, 100.0) if not with_intermediary
            else np.sum(routing * p_direct, axis=0) + markup,
            routing, g_active
        )
        routing = compute_routing(p_direct, mfg_phi)

        # Optimize intermediary (if applicable)
        if with_intermediary:
            markup = optimize_intermediary(p_direct, routing, g_active, n_trials=15)
        p_intermediary = (np.sum(routing * p_direct, axis=0) + markup
                          if with_intermediary else np.full(NUM_PERIODS, 100.0))

        # Each manufacturer best-responds (price + capacity)
        for i in range(NUM_MFG):
            w_i = MFG_COST[i]
            best_p = p_direct[i].copy()
            best_g = g_active[i].copy()
            best_prof = manufacturer_profit(i, p_direct, p_intermediary, routing, g_active)

            for trial in range(15):
                if trial == 0:
                    x0 = np.concatenate([p_direct[i], g_active[i]])
                elif i == 2 and trial < 5:
                    x0 = np.concatenate([
                        np.random.uniform(w_i + 0.05, 0.80, NUM_PERIODS),
                        np.random.uniform(MFG_CAPACITY_MIN[i], MFG_CAPACITY[i], NUM_PERIODS)
                    ])
                else:
                    x0 = np.concatenate([
                        np.random.uniform(w_i + 0.05, 1.5, NUM_PERIODS),
                        np.random.uniform(MFG_CAPACITY_MIN[i] * 0.5, MFG_CAPACITY[i], NUM_PERIODS)
                    ])

                bounds = ([(w_i + 0.05, RIGID_WTP + 0.3)] * NUM_PERIODS
                          + [(MFG_CAPACITY_MIN[i], MFG_CAPACITY[i])] * NUM_PERIODS)

                def obj(x, ii=i):
                    pd_new = p_direct.copy()
                    pd_new[ii] = x[:NUM_PERIODS]
                    ga_new = g_active.copy()
                    ga_new[ii] = x[NUM_PERIODS:]
                    return -manufacturer_profit(ii, pd_new, p_intermediary, routing, ga_new)

                try:
                    res = minimize(obj, x0, method='L-BFGS-B', bounds=bounds,
                                   options={'maxiter': 3000})
                    pd_new = p_direct.copy()
                    pd_new[i] = res.x[:NUM_PERIODS]
                    ga_new = g_active.copy()
                    ga_new[i] = res.x[NUM_PERIODS:]
                    prof = manufacturer_profit(i, pd_new, p_intermediary, routing, ga_new)
                    if prof > best_prof:
                        best_prof = prof
                        best_p = res.x[:NUM_PERIODS].copy()
                        best_g = res.x[NUM_PERIODS:].copy()
                except Exception:
                    pass

            p_direct[i] = best_p
            g_active[i] = best_g

        diff = max(np.max(np.abs(p_direct - p_old)), np.max(np.abs(g_active - g_old)))
        print(f"  Iter {iteration + 1}: max_change={diff:.4f}")
        if diff < tol:
            break

    # Final evaluation
    p_intermediary = (np.sum(routing * p_direct, axis=0) + markup
                      if with_intermediary else np.full(NUM_PERIODS, 100.0))
    shares, flex, rigid, served, mfg_util, mfg_phi = compute_demands(
        p_direct, p_intermediary, routing, g_active
    )

    mfg_profits = [
        manufacturer_profit(i, p_direct, p_intermediary, routing, g_active)
        for i in range(NUM_MFG)
    ]

    int_profit = 0.0
    if with_intermediary:
        int_profit = intermediary_profit(markup, p_direct, routing, g_active)

    return {
        "p_direct": p_direct,
        "g_active": g_active,
        "markup": markup,
        "routing": routing,
        "mfg_profits": mfg_profits,
        "int_profit": int_profit,
        "mfg_phi": mfg_phi,
        "mfg_util": mfg_util,
        "shares": shares,
        "flex": flex,
        "rigid": rigid,
        "served": served,
    }


# ══════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    np.random.seed(RNG_SEED)

    print("=" * 60)
    print("Multi-Platform Token Dynamic Pricing Game")
    print("=" * 60)

    # Monopoly baseline
    from run_experiment import optimize_dynamic_prices, uniform_pricing
    import run_experiment
    orig_G, orig_K = run_experiment.CAPACITY, run_experiment.DEGRADE_KAPPA
    run_experiment.CAPACITY = float(np.sum(MFG_CAPACITY))
    run_experiment.DEGRADE_KAPPA = DEGRADE_KAPPA
    mono_uni = uniform_pricing()
    mono_dyn = optimize_dynamic_prices(n_trials=50)
    run_experiment.CAPACITY, run_experiment.DEGRADE_KAPPA = orig_G, orig_K

    # Competition without intermediary
    print("\n--- Competition (no intermediary) ---")
    eq_no_int = compute_equilibrium(max_iter=8, with_intermediary=False)

    # Competition with intermediary
    print("\n--- Competition (with intermediary) ---")
    eq_int = compute_equilibrium(max_iter=8, with_intermediary=True)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Monopoly UNI:        ${mono_uni['profit']:.0f}  phi_min={np.min(mono_uni['quality']):.3f}")
    print(f"  Monopoly DYN:        ${mono_dyn['profit']:.0f}  phi_min={np.min(mono_dyn['quality']):.3f}")
    total_no_int = sum(eq_no_int['mfg_profits'])
    print(f"  Competition (no I):  ${total_no_int:.0f}  phi_min={np.min(eq_no_int['mfg_phi']):.3f}")
    total_int = sum(eq_int['mfg_profits']) + eq_int['int_profit']
    print(f"  Competition (w/ I):  ${total_int:.0f}  phi_min={np.min(eq_int['mfg_phi']):.3f}  (I=${eq_int['int_profit']:.0f})")

    for label, eq in [("No I", eq_no_int), ("W/ I", eq_int)]:
        print(f"\n  Details ({label}):")
        for i in range(NUM_MFG):
            cap_pct = np.mean(eq['g_active'][i] / MFG_CAPACITY[i] * 100)
            spread = np.max(eq['p_direct'][i]) - np.min(eq['p_direct'][i])
            print(f"    Mfg {MFG_NAMES[i]}: ${eq['mfg_profits'][i]:.0f}  "
                  f"phi={np.min(eq['mfg_phi'][i]):.3f}  "
                  f"avg_p=${np.mean(eq['p_direct'][i]):.3f}  "
                  f"spread=${spread:.2f}  "
                  f"cap={cap_pct:.0f}%  "
                  f"prices={np.round(eq['p_direct'][i], 2)}")
        if eq['int_profit'] > 0:
            print(f"    Intermediary: ${eq['int_profit']:.0f}  "
                  f"avg_markup=${np.mean(eq['markup']):.3f}")


if __name__ == "__main__":
    main()
