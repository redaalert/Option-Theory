"""
importance_sampling.py
-----------------------
Efficient Monte Carlo pricing of deep out-of-the-money (DOTM) European
options via exponential-tilting importance sampling under Black-Scholes
(GBM) dynamics.

Theory reference: P. Glasserman, "Monte Carlo Methods in Financial
Engineering", Springer 2004, Chapter 4 -- specifically:
  * Sec 4.6.1, Example 4.6.1 (normal change of mean / likelihood ratio)
  * Sec 4.6.2 "Change of Drift: Normal Approximation and Optimal Path",
    eq. (4.90): the importance density's mode is found by maximizing
        F(z) - 0.5 * z^2
    over the input z, where G(z) = exp(F(z)) is the (non-discounted)
    payoff as a function of the driving normal variate z. For a single
    N(0,1) driver (one-step European payoff) this reduces to a 1-D
    root-finding problem instead of the general fixed-point iteration
    Glasserman uses for path-dependent (Asian) payoffs.

Model
-----
Under the risk-neutral measure, terminal price:
    S(T) = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z),   Z ~ N(0,1)

Discounted call payoff:
    Y(Z) = exp(-r*T) * (S(T) - K)^+

Ordinary Monte Carlo estimator:
    alpha_hat = (1/n) * sum Y(Z_i),           Z_i ~ N(0,1) iid

Importance sampling estimator (mean-shift by mu, cf. eq. 4.83/4.87):
    alpha_hat_IS = (1/n) * sum Y(Z_i) * exp(-mu*Z_i + 0.5*mu^2),
                                    Z_i ~ N(mu,1) iid
which is unbiased for any mu (the likelihood ratio dF0/dF_mu evaluated
at the drawn points), and which recovers exp(-mu*Z+0.5*mu^2) as derived
in Example 4.6.1 of the text for a change of mean of a scalar normal.
"""

from __future__ import annotations
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from dataclasses import dataclass


# --------------------------------------------------------------------
# Closed-form Black-Scholes (ground truth to validate MC against)
# --------------------------------------------------------------------
def bs_call_price(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


# --------------------------------------------------------------------
# Result container
# --------------------------------------------------------------------
@dataclass
class MCResult:
    price: float
    stderr: float
    variance_per_path: float
    n: int

    @property
    def ci95(self):
        return (self.price - 1.96 * self.stderr, self.price + 1.96 * self.stderr)


# --------------------------------------------------------------------
# Ordinary Monte Carlo
# --------------------------------------------------------------------
def mc_price_call(S0, K, r, sigma, T, n, rng=None) -> MCResult:
    rng = np.random.default_rng() if rng is None else rng
    Z = rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    Y = np.exp(-r * T) * np.maximum(ST - K, 0.0)
    price = Y.mean()
    var = Y.var(ddof=1)
    return MCResult(price=price, stderr=np.sqrt(var / n), variance_per_path=var, n=n)


# --------------------------------------------------------------------
# Optimal mean-shift for importance sampling
# --------------------------------------------------------------------
def naive_shift(S0, K, r, sigma, T) -> float:
    """
    Shift the mean of Z so that E_mu[S(T)] lands exactly on the strike K
    (cf. Glasserman Example 4.6.1 -- classic 'shift to strike' heuristic).
    """
    return (np.log(K / S0) - (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def optimal_mode_shift(S0, K, r, sigma, T) -> float:
    """
    True mode-matching drift from Glasserman Sec 4.6.2 (eq. 4.90):
    choose mu = z* solving

        max_z  F(z) - 0.5 z^2 ,     G(z) = exp(F(z)) = (S(z) - K)^+

    First-order condition for z > z_K (in-the-money region, where the
    payoff is differentiable): S'(z) = (S(z) - K) * z, i.e.

        z = sigma*sqrt(T) * S(z) / (S(z) - K)

    which is the one-step (m=1) specialisation of eq. (4.91) used there
    for Asian options. Solved by 1-D root finding.
    """
    zK = naive_shift(S0, K, r, sigma, T)  # boundary of the {S(T) > K} region

    def S_of_z(z):
        return S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)

    def foc(z):
        Sz = S_of_z(z)
        return sigma * np.sqrt(T) * Sz - (Sz - K) * z

    lo, hi = zK + 1e-6, zK + 50.0
    # bracket search: foc(lo) should be > 0 (payoff still rising fast),
    # foc should cross zero once moving right (concave objective in log(S)).
    try:
        return brentq(foc, lo, hi, maxiter=200)
    except ValueError:
        # fallback: coarse scan then bisect
        zs = np.linspace(lo, zK + 200, 20000)
        vals = np.array([foc(z) for z in zs])
        sign_change = np.where(np.diff(np.sign(vals)) != 0)[0]
        if len(sign_change) == 0:
            return zK  # degenerate fallback
        i = sign_change[0]
        return brentq(foc, zs[i], zs[i + 1], maxiter=200)


# --------------------------------------------------------------------
# Importance-sampled Monte Carlo
# --------------------------------------------------------------------
def mc_price_call_is(S0, K, r, sigma, T, n, mu, rng=None) -> MCResult:
    rng = np.random.default_rng() if rng is None else rng
    Z = mu + rng.standard_normal(n)                       # Z ~ N(mu, 1)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoff = np.exp(-r * T) * np.maximum(ST - K, 0.0)
    likelihood_ratio = np.exp(-mu * Z + 0.5 * mu**2)       # dF0/dF_mu, eq (4.83)
    Y = payoff * likelihood_ratio
    price = Y.mean()
    var = Y.var(ddof=1)
    return MCResult(price=price, stderr=np.sqrt(var / n), variance_per_path=var, n=n)


# --------------------------------------------------------------------
# Convenience: variance reduction factor + equivalent path-count savings
# --------------------------------------------------------------------
def variance_reduction_factor(std_result: MCResult, is_result: MCResult) -> float:
    """Var[ordinary MC per path] / Var[IS per path]  ('m' in resume line)."""
    return std_result.variance_per_path / is_result.variance_per_path
