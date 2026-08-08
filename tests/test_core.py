import numpy as np
import statsmodels.api as sm

from econnotes.core import (
    aggregate_att_event,
    bjs_imputation,
    conley_covariance,
    cs_att_gt,
    effective_number_of_shocks,
    iv_ratio,
    local_projections,
    randomization_inference_complete,
    shock_level_iv_equivalent,
    simulate_local_projection_series,
    simulate_randomized_experiment,
    simulate_shift_share,
    simulate_staggered_panel,
    synthetic_control_weights,
)


def test_shift_share_shock_level_equivalence():
    sim = simulate_shift_share(seed=1)
    beta1 = iv_ratio(sim["y"], sim["x"], sim["z"])
    beta2 = shock_level_iv_equivalent(sim["y"], sim["x"], sim["shares"], sim["shocks"])
    assert abs(beta1 - beta2) < 1e-10


def test_synthetic_control_simplex():
    rng = np.random.default_rng(1)
    Y0 = rng.normal(size=(12, 5))
    true_w = np.array([0.4, 0.3, 0.2, 0.1, 0.0])
    y1 = Y0 @ true_w
    w = synthetic_control_weights(y1, Y0)
    assert np.isclose(w.sum(), 1.0, atol=1e-7)
    assert np.all(w >= -1e-8)
    assert np.mean((y1 - Y0 @ w) ** 2) < 1e-8


def test_conley_covariance_is_symmetric_psdish():
    rng = np.random.default_rng(2)
    X = sm.add_constant(rng.normal(size=(80, 1)))
    u = rng.normal(size=80)
    coords = rng.uniform(size=(80, 2))
    V = conley_covariance(X, u, coords, cutoff=0.5)
    assert np.allclose(V, V.T, atol=1e-10)
    assert np.all(np.diag(V) >= 0)


def test_randomization_inference_rejects_wrong_sharp_null():
    sim = simulate_randomized_experiment(n=60, n_treated=30, tau=1.0, seed=9)
    out0 = randomization_inference_complete(sim["y"], sim["z"], tau_null=0.0, B=1500, seed=3)
    out1 = randomization_inference_complete(sim["y"], sim["z"], tau_null=1.0, B=1500, seed=3)
    assert out0["p_value"] < out1["p_value"]


def test_bjs_recovers_positive_effect_path():
    df = simulate_staggered_panel(n_units=160, seed=12)
    est, _ = bjs_imputation(df)
    assert est.loc[est.event_time == 0, "estimate"].iloc[0] > 0.3
    assert est.loc[est.event_time == 2, "estimate"].iloc[0] > est.loc[est.event_time == 0, "estimate"].iloc[0]


def test_cs_att_positive():
    df = simulate_staggered_panel(n_units=180, seed=13)
    att = aggregate_att_event(cs_att_gt(df))
    assert att.loc[att.event_time == 0, "estimate"].iloc[0] > 0.2


def test_local_projection_shape_and_sign():
    df = simulate_local_projection_series(T=700, seed=4)
    lp = local_projections(df, horizons=range(5), lags=2)
    assert len(lp) == 5
    assert lp.loc[0, "estimate"] > 0.4


def test_effective_shocks_bounds():
    sim = simulate_shift_share(n_regions=50, n_sectors=10, seed=5)
    n_eff = effective_number_of_shocks(sim["shares"])
    assert 1 <= n_eff <= 10 + 1e-8
