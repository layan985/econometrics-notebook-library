"""Transparent reference implementations for the Econometrics Notebook Library."""
from __future__ import annotations
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.spatial.distance import cdist

def simulate_clustered_regression(n_clusters: int=12, cluster_size: int=40, beta: float=0.0, seed: int=7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_clusters):
        cluster_shock = rng.normal(scale=1.2)
        x_cluster = rng.normal()
        for j in range(cluster_size):
            x = 0.7 * x_cluster + rng.normal()
            y = beta * x + cluster_shock + rng.normal(scale=1.0)
            rows.append({'cluster': g, 'x': x, 'y': y})
    return pd.DataFrame(rows)

def wild_cluster_bootstrap_t(y: np.ndarray, X: np.ndarray, clusters: np.ndarray, tested_index: int, null: float=0.0, B: int=999, weights: str='rademacher', seed: int=1234) -> dict:
    """Null-imposed wild cluster bootstrap-t for OLS.

    X should include the intercept if desired. Cluster-robust standard errors use
    statsmodels' finite-sample correction. Bootstrap residuals come from the
    restricted model under H0.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    clusters = np.asarray(clusters)
    groups = np.unique(clusters)
    fit = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': clusters})
    beta_hat = fit.params[tested_index]
    se_hat = fit.bse[tested_index]
    t_obs = float((beta_hat - null) / se_hat)
    idx_other = [j for j in range(X.shape[1]) if j != tested_index]
    y_r = y - X[:, tested_index] * null
    X_r = X[:, idx_other]
    rfit = sm.OLS(y_r, X_r).fit()
    fitted_null = rfit.fittedvalues + X[:, tested_index] * null
    u_r = y - fitted_null
    t_boot = np.empty(B)
    webb_support = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
    for b in range(B):
        if weights == 'rademacher':
            draw = rng.choice([-1.0, 1.0], size=len(groups))
        elif weights == 'webb':
            draw = rng.choice(webb_support, size=len(groups))
        else:
            raise ValueError("weights must be 'rademacher' or 'webb'")
        wmap = dict(zip(groups, draw))
        w = np.array([wmap[g] for g in clusters])
        y_star = fitted_null + u_r * w
        fstar = sm.OLS(y_star, X).fit(cov_type='cluster', cov_kwds={'groups': clusters})
        t_boot[b] = (fstar.params[tested_index] - null) / fstar.bse[tested_index]
    p = float((1 + np.sum(np.abs(t_boot) >= abs(t_obs))) / (B + 1))
    return {'beta': float(beta_hat), 'se_cluster': float(se_hat), 't_obs': t_obs, 'p_wild': p, 't_boot': t_boot}

def simulate_spatial_cross_section(n: int=260, beta: float=1.0, seed: int=99) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0, 100, size=(n, 2))
    dist = cdist(coords, coords)
    cov = np.exp(-dist / 18.0) + np.eye(n) * 1e-06
    spatial_error = np.linalg.cholesky(cov) @ rng.normal(size=n)
    x = rng.normal(size=n)
    y = 0.5 + beta * x + spatial_error
    return pd.DataFrame({'xcoord': coords[:, 0], 'ycoord': coords[:, 1], 'x': x, 'y': y})

def conley_covariance(X: np.ndarray, residuals: np.ndarray, coords: np.ndarray, cutoff: float, kernel: str='bartlett') -> np.ndarray:
    """Cross-sectional spatial HAC covariance with Euclidean distances."""
    X = np.asarray(X, float)
    u = np.asarray(residuals, float)
    coords = np.asarray(coords, float)
    d = cdist(coords, coords)
    if kernel == 'bartlett':
        K = np.maximum(1.0 - d / cutoff, 0.0)
    elif kernel == 'uniform':
        K = (d <= cutoff).astype(float)
    else:
        raise ValueError("kernel must be 'bartlett' or 'uniform'")
    xu = X * u[:, None]
    meat = xu.T @ K @ xu
    bread = np.linalg.inv(X.T @ X)
    return bread @ meat @ bread
