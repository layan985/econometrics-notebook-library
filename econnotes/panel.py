"""Transparent reference implementations for the Econometrics Notebook Library."""
from __future__ import annotations
from typing import Sequence
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression, LinearRegression

def simulate_staggered_panel(n_units: int=240, n_periods: int=12, cohorts: Sequence[int]=(4, 6, 8), never_share: float=0.25, seed: int=123) -> pd.DataFrame:
    """Simulate staggered adoption with cohort/event-time heterogeneous effects.

    Untreated potential outcomes satisfy unconditional parallel trends. Errors
    are serially correlated within unit. A time-invariant covariate x is included
    for conditional-DiD demonstrations.
    """
    rng = np.random.default_rng(seed)
    units = np.arange(n_units)
    times = np.arange(n_periods)
    probs = np.array([(1 - never_share) / len(cohorts)] * len(cohorts) + [never_share])
    g_choices = np.array(list(cohorts) + [np.inf])
    G = rng.choice(g_choices, size=n_units, p=probs)
    alpha = rng.normal(0, 1.2, size=n_units)
    x = rng.normal(size=n_units)
    lambda_t = 0.18 * times + 0.25 * np.sin(times / 1.8)
    rows = []
    for i in units:
        eps_prev = 0.0
        for t in times:
            eps = 0.55 * eps_prev + rng.normal(0, 0.55)
            eps_prev = eps
            y0 = alpha[i] + lambda_t[t] + 0.35 * x[i] + eps
            treated = np.isfinite(G[i]) and t >= G[i]
            event_time = t - G[i] if np.isfinite(G[i]) else np.nan
            tau = 0.0
            if treated:
                cohort_scale = 1.0 + 0.1 * (G[i] - min(cohorts))
                tau = cohort_scale * (0.7 + 0.45 * event_time)
            y = y0 + tau
            rows.append({'unit': int(i), 'time': int(t), 'cohort': G[i], 'x': x[i], 'treated': int(treated), 'event_time': event_time, 'tau_true': tau, 'y0': y0, 'y': y})
    return pd.DataFrame(rows)

def _event_name(k: int) -> str:
    return f"evt_{('m' + str(abs(k)) if k < 0 else 'p' + str(k))}"

def twfe_event_study(df: pd.DataFrame, window: tuple[int, int]=(-3, 4), reference: int=-1) -> pd.DataFrame:
    """Conventional TWFE event-study regression with unit/time fixed effects."""
    d = df.copy()
    lo, hi = window
    terms = []
    for k in range(lo, hi + 1):
        if k == reference:
            continue
        name = _event_name(k)
        d[name] = ((d['event_time'] == k) & np.isfinite(d['cohort'])).astype(int)
        terms.append((k, name))
    formula = 'y ~ ' + ' + '.join((name for _, name in terms)) + ' + C(unit) + C(time)'
    fit = smf.ols(formula, d).fit(cov_type='cluster', cov_kwds={'groups': d['unit']})
    rows = []
    for k, name in terms:
        rows.append({'event_time': k, 'estimate': fit.params.get(name, np.nan), 'se': fit.bse.get(name, np.nan), 'method': 'TWFE'})
    return pd.DataFrame(rows)

def sun_abraham_iw(df: pd.DataFrame, window: tuple[int, int]=(-3, 4), reference: int=-1) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Interaction-weighted event study, never-treated comparison version."""
    d = df.copy()
    treated_cohorts = sorted((int(g) for g in d.loc[np.isfinite(d.cohort), 'cohort'].unique()))
    terms: list[tuple[int, int, str]] = []
    for g in treated_cohorts:
        events = sorted((int(k) for k in d.loc[d.cohort == g, 'event_time'].dropna().unique() if int(k) != reference))
        for k in events:
            name = f'sa_g{g}_{_event_name(k)}'
            d[name] = ((d['cohort'] == g) & (d['event_time'] == k)).astype(int)
            terms.append((g, k, name))
    formula = 'y ~ ' + ' + '.join((name for _, _, name in terms)) + ' + C(unit) + C(time)'
    fit = smf.ols(formula, d).fit(cov_type='cluster', cov_kwds={'groups': d['unit']})
    cohort_counts = d[['unit', 'cohort']].drop_duplicates()['cohort'].value_counts()
    cell_rows = []
    for g, k, name in terms:
        cell_rows.append({'cohort': g, 'event_time': k, 'estimate': fit.params.get(name, np.nan), 'se': fit.bse.get(name, np.nan), 'n_cohort': int(cohort_counts.get(float(g), cohort_counts.get(g, 0)))})
    cells = pd.DataFrame(cell_rows)
    lo, hi = window
    agg_rows = []
    for k in range(lo, hi + 1):
        if k == reference:
            continue
        sub = cells[(cells.event_time == k) & cells.estimate.notna()].copy()
        if sub.empty:
            continue
        w = sub['n_cohort'].to_numpy(float)
        w /= w.sum()
        est = float(np.sum(w * sub['estimate'].to_numpy()))
        se = float(np.sqrt(np.sum((w * sub['se'].to_numpy()) ** 2)))
        agg_rows.append({'event_time': k, 'estimate': est, 'se': se, 'method': 'Sun-Abraham IW'})
    return (pd.DataFrame(agg_rows), cells)

def cs_att_gt(df: pd.DataFrame, use_covariate: bool=True, control: str='not_yet') -> pd.DataFrame:
    """Group-time ATT(g,t) with a panel doubly-robust score."""
    wide_y = df.pivot(index='unit', columns='time', values='y')
    unit_info = df.groupby('unit', as_index=True).first()[['cohort', 'x']]
    treated_cohorts = sorted((int(g) for g in unit_info.loc[np.isfinite(unit_info.cohort), 'cohort'].unique()))
    max_t = int(df.time.max())
    rows = []
    for g in treated_cohorts:
        b = g - 1
        if b not in wide_y.columns:
            continue
        for t in range(g, max_t + 1):
            if t not in wide_y.columns:
                continue
            if control == 'never':
                ctrl_mask = ~np.isfinite(unit_info.cohort.to_numpy())
            elif control == 'not_yet':
                ctrl_mask = ~np.isfinite(unit_info.cohort.to_numpy()) | (unit_info.cohort.to_numpy() > t)
            else:
                raise ValueError("control must be 'never' or 'not_yet'")
            tr_mask = unit_info.cohort.to_numpy() == g
            keep = tr_mask | ctrl_mask
            ids = unit_info.index.to_numpy()[keep]
            D = tr_mask[keep].astype(int)
            dy = (wide_y.loc[ids, t] - wide_y.loc[ids, b]).to_numpy(float)
            X = unit_info.loc[ids, ['x']].to_numpy(float)
            if use_covariate:
                ps = LogisticRegression(C=1000000.0, solver='lbfgs').fit(X, D).predict_proba(X)[:, 1]
                ps = np.clip(ps, 0.01, 0.99)
                m0_model = LinearRegression().fit(X[D == 0], dy[D == 0])
                m0 = m0_model.predict(X)
                pD = D.mean()
                score = D * (dy - m0) / pD - (1 - D) * (ps / (1 - ps)) * (dy - m0) / pD
                att = float(score.mean())
                se = float(score.std(ddof=1) / np.sqrt(len(score)))
            else:
                att = float(dy[D == 1].mean() - dy[D == 0].mean())
                se = float(np.sqrt(dy[D == 1].var(ddof=1) / D.sum() + dy[D == 0].var(ddof=1) / (1 - D).sum()))
            rows.append({'cohort': g, 'time': t, 'event_time': t - g, 'att': att, 'se': se, 'n_treated': int(D.sum()), 'n_control': int((1 - D).sum())})
    return pd.DataFrame(rows)

def aggregate_att_event(att_gt: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for e, sub in att_gt.groupby('event_time'):
        w = sub['n_treated'].to_numpy(float)
        w /= w.sum()
        est = float(np.sum(w * sub['att'].to_numpy()))
        se = float(np.sqrt(np.sum((w * sub['se'].to_numpy()) ** 2)))
        rows.append({'event_time': int(e), 'estimate': est, 'se': se, 'method': "Callaway-Sant'Anna DR"})
    return pd.DataFrame(rows).sort_values('event_time')

def bjs_imputation(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Borusyak-Jaravel-Spiess imputation estimator for a simple panel FE model."""
    d = df.copy()
    untreated = d['treated'] == 0
    fit = smf.ols('y ~ C(unit) + C(time) + x', data=d.loc[untreated]).fit()
    d['y0_hat'] = fit.predict(d)
    d['tau_hat'] = d['y'] - d['y0_hat']
    rows = []
    tr = d[d.treated == 1].copy()
    for e, sub in tr.groupby('event_time'):
        vals = sub.tau_hat.to_numpy(float)
        rows.append({'event_time': int(e), 'estimate': float(vals.mean()), 'se': float(vals.std(ddof=1) / np.sqrt(len(vals))), 'n': len(vals), 'method': 'BJS imputation'})
    return (pd.DataFrame(rows).sort_values('event_time'), d)
