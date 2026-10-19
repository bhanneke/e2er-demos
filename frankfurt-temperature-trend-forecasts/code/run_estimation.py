"""Trend estimation, seasonal forecasting models and hold-out evaluation.
Frankfurt am Main monthly T2M (NASA POWER), 1981-01 to 2025-12.
Reads data.db table frankfurt_t2m_monthly; writes estimation_results.json."""
import json
import math
import sqlite3
import warnings

import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from scipy import stats
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf, adfuller, kpss
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")
np.random.seed(20260101)

TRAIN_END, HOLD_START, HOLD_END = "2022-12", "2023-01", "2025-12"
H_FWD, ALPHA, SP = 36, 0.05, 12
ZQ = stats.norm.ppf(1 - ALPHA / 2)


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


# ------------------------------------------------------------------ data
con = sqlite3.connect("data.db")
df = pd.read_sql("SELECT date, year, month, T2M FROM frankfurt_t2m_monthly ORDER BY date", con)
con.close()
n_raw = len(df)
assert df["T2M"].notna().all() and df["date"].is_unique
df["dt"] = pd.to_datetime(df["date"] + "-01")
y_all = pd.Series(df["T2M"].values, index=pd.DatetimeIndex(df["dt"], freq="MS"))
train = y_all[:TRAIN_END]
hold = y_all[HOLD_START:HOLD_END]
assert len(train) == 504 and len(hold) == 36
fwd_idx = pd.date_range("2026-01-01", periods=H_FWD, freq="MS")
hold_idx = hold.index
per = lambda idx: [d.strftime("%Y-%m") for d in idx]
mase_scale = float(np.mean(np.abs(train.values[SP:] - train.values[:-SP])))


# ------------------------------------------------------------------ helpers
def hac_lag(T):
    return int(np.floor(4 * (T / 100) ** (2 / 9)))


def ols_hac(y, x, lag):
    X = sm.add_constant(np.asarray(x, float))
    r = sm.OLS(np.asarray(y, float), X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
    return r


def trend_entry(y, t, lag, per_unit=10.0):
    r = ols_hac(y, t, lag)
    b, se = float(r.params[1]), float(r.bse[1])
    ci = r.conf_int()[1]
    return {"slope_per_year": b, "slope_per_decade": b * per_unit, "se_per_decade": se * per_unit,
            "ci_lower_per_decade": float(ci[0]) * per_unit, "ci_upper_per_decade": float(ci[1]) * per_unit,
            "p_value": float(r.pvalues[1]), "hac_lag": lag, "n": int(len(y)), "r2": float(r.rsquared)}


def mann_kendall(x):
    x = np.asarray(x, float)
    n = len(x)
    s = sum(np.sign(x[j] - x[i]) for i in range(n - 1) for j in range(i + 1, n))
    _, cnt = np.unique(x, return_counts=True)
    var_s = (n * (n - 1) * (2 * n + 5) - sum(c * (c - 1) * (2 * c + 5) for c in cnt)) / 18.0
    z = (s - np.sign(s)) / math.sqrt(var_s) if s != 0 else 0.0
    slopes = [(x[j] - x[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)]
    sen = float(np.median(slopes))
    # Hamed-Rao autocorrelation correction on ranks of detrended series
    tt = np.arange(n)
    detr = x - sen * tt
    detr = detr - np.median(detr - 0)  # centred
    ranks = stats.rankdata(detr)
    rho = acf(ranks, nlags=n - 2, fft=False)
    bound = stats.norm.ppf(0.975) / math.sqrt(n)
    corr = 0.0
    for i in range(1, n - 1):
        if abs(rho[i]) > bound:
            corr += (n - i) * (n - i - 1) * (n - i - 2) * rho[i]
    nns = max(1 + 2.0 / (n * (n - 1) * (n - 2)) * corr, 1e-6)
    z_c = (s - np.sign(s)) / math.sqrt(var_s * nns) if s != 0 else 0.0
    return {"S": float(s), "z": float(z), "p": float(2 * (1 - stats.norm.cdf(abs(z)))), "sen_slope_per_year": sen,
            "z_corrected": float(z_c), "p_corrected": float(2 * (1 - stats.norm.cdf(abs(z_c)))),
            "variance_inflation": float(nns)}


def deseason(y):
    """subtract month-of-year means estimated on y itself"""
    m = y.groupby(y.index.month).transform("mean")
    return y - m


def aicc(llf, k, n):
    return -2 * llf + 2 * k + 2 * k * (k + 1) / max(n - k - 1, 1)


def harm_X(idx, K, t0=pd.Timestamp("1981-01-01")):
    t = ((idx.year - t0.year) * 12 + (idx.month - t0.month)).values.astype(float)
    cols = {"trend_years": t / 12.0}
    for k in range(1, K + 1):
        cols[f"sin{k}"] = np.sin(2 * np.pi * k * t / 12.0)
        cols[f"cos{k}"] = np.cos(2 * np.pi * k * t / 12.0)
    return sm.add_constant(pd.DataFrame(cols, index=idx), has_constant="add")


# ------------------------------------------------------------------ model fit/forecast functions
def f_snaive(y, h):
    v = y.values
    d = v[SP:] - v[:-SP]
    sig = float(np.std(d, ddof=1))
    idx = pd.date_range(y.index[-1] + pd.offsets.MonthBegin(1), periods=h, freq="MS")
    steps = np.arange(1, h + 1)
    mean = np.array([v[len(v) - SP + ((s - 1) % SP)] for s in steps])
    k = np.ceil(steps / SP)
    half = ZQ * sig * np.sqrt(k)
    return {"idx": idx, "mean": mean, "lower": mean - half, "upper": mean + half,
            "fit": {"sigma2": sig ** 2}, "params": {"seasonal_lag_diff_sd": {"estimate": sig}}}


def f_naive(y, h):
    v = y.values
    sig = float(np.std(np.diff(v), ddof=1))
    idx = pd.date_range(y.index[-1] + pd.offsets.MonthBegin(1), periods=h, freq="MS")
    mean = np.repeat(v[-1], h)
    half = ZQ * sig * np.sqrt(np.arange(1, h + 1))
    return {"idx": idx, "mean": mean, "lower": mean - half, "upper": mean + half,
            "fit": {"sigma2": sig ** 2}, "params": {"first_diff_sd": {"estimate": sig}}}


def f_ets(damped):
    def f(y, h):
        m = ETSModel(y, error="add", trend="add" if damped else None, damped_trend=damped,
                     seasonal="add", seasonal_periods=SP)
        r = m.fit(disp=False, maxiter=2000)
        pr = r.get_prediction(start=len(y), end=len(y) + h - 1).summary_frame(alpha=ALPHA)
        params = {k: {"estimate": float(v)} for k, v in zip(r.param_names, r.params)
                  if not k.startswith(("initial_", "seasonal.")) or k.startswith("initial_level")}
        return {"idx": pr.index, "mean": pr["mean"].values, "lower": pr["pi_lower"].values,
                "upper": pr["pi_upper"].values,
                "fit": {"aic": float(r.aic), "bic": float(r.bic), "log_likelihood": float(r.llf),
                        "sigma2": float(r.mse)}, "params": params}
    return f


def sarima_fit(y, order, sorder, trend):
    return SARIMAX(y, order=order, seasonal_order=sorder + (SP,), trend=trend).fit(disp=False, maxiter=200)


def sarima_trend(order, sorder):
    return "c" if order[1] + sorder[1] <= 1 else None


def f_sarima_fixed(order, sorder):
    def f(y, h):
        tr = sarima_trend(order, sorder)
        r = sarima_fit(y, order, sorder, tr)
        fc = r.get_forecast(h)
        ci = fc.conf_int(alpha=ALPHA)
        params = {n: {"estimate": float(p), "se": float(s)} for n, p, s in zip(r.param_names, r.params, r.bse)}
        return {"idx": fc.predicted_mean.index, "mean": fc.predicted_mean.values,
                "lower": ci.iloc[:, 0].values, "upper": ci.iloc[:, 1].values,
                "fit": {"aic": float(r.aic), "bic": float(r.bic), "log_likelihood": float(r.llf),
                        "sigma2": float(r.params.get("sigma2", np.nan))}, "params": params}
    return f


def select_sarima(y):
    """Hyndman-Khandakar-style: D by seasonal strength, d by KPSS, p,q<=3, P,Q<=2 stepwise by AICc."""
    stl = STL(y, period=SP, robust=True).fit()
    fs = max(0.0, 1 - np.var(stl.resid) / np.var(stl.resid + stl.seasonal))
    D = 1 if fs > 0.64 else 0
    z = y.diff(SP).dropna() if D else y
    d = 0
    for _ in range(2):
        p = kpss(z, regression="c", nlags="auto")[1]
        if p < 0.05:
            d += 1
            z = z.diff().dropna()
        else:
            break
    n = len(y) - d - D * SP
    cache = {}

    def score(o):
        if o in cache:
            return cache[o]
        p, q, P, Q = o
        try:
            tr = sarima_trend((p, d, q), (P, D, Q))
            r = sarima_fit(y, (p, d, q), (P, D, Q), tr)
            k = len(r.params)
            s = aicc(r.llf, k, n) if np.isfinite(r.llf) else np.inf
        except Exception:
            s = np.inf
        cache[o] = s
        return s

    cur = min([(2, 2, 1, 1), (0, 0, 0, 0), (1, 0, 1, 0), (0, 1, 0, 1)], key=score)
    best = score(cur)
    lim = (3, 3, 2, 2)
    improved = True
    while improved:
        improved = False
        for i in range(4):
            for dlt in (-1, 1):
                o = list(cur)
                o[i] += dlt
                if o[i] < 0 or o[i] > lim[i]:
                    continue
                o = tuple(o)
                if score(o) < best - 1e-9:
                    cur, best, improved = o, score(o), True
        if not improved:
            for i, j in [(0, 1), (2, 3), (0, 2), (1, 3)]:
                for a in (-1, 1):
                    o = list(cur)
                    o[i] += a
                    o[j] += a
                    if min(o) < 0 or any(o[k] > lim[k] for k in range(4)):
                        continue
                    o = tuple(o)
                    if score(o) < best - 1e-9:
                        cur, best, improved = o, score(o), True
    p, q, P, Q = cur
    return (p, d, q), (P, D, Q), best, float(fs), len(cache)


def f_harmonic(K):
    def f(y, h):
        X = harm_X(y.index, K)
        r = sm.OLS(y.values, X).fit()
        idx = pd.date_range(y.index[-1] + pd.offsets.MonthBegin(1), periods=h, freq="MS")
        Xf = harm_X(idx, K)
        sf = r.get_prediction(Xf).summary_frame(alpha=ALPHA)
        params = {n: {"estimate": float(p), "se": float(s)} for n, p, s in zip(X.columns, r.params, r.bse)}
        return {"idx": idx, "mean": sf["mean"].values, "lower": sf["obs_ci_lower"].values,
                "upper": sf["obs_ci_upper"].values,
                "fit": {"aic": float(r.aic), "bic": float(r.bic), "log_likelihood": float(r.llf),
                        "sigma2": float(r.mse_resid)}, "params": params}
    return f


def select_K(y):
    out = {}
    for K in range(1, 5):
        X = harm_X(y.index, K)
        r = sm.OLS(y.values, X).fit()
        out[K] = aicc(r.llf, X.shape[1] + 1, len(y))
    return min(out, key=out.get), out


# ------------------------------------------------------------------ 1. diagnostics (training only)
sa_train = deseason(train)
kp = kpss(sa_train, regression="c", nlags="auto")
ad = adfuller(sa_train, regression="c", autolag="AIC")
ann_train = train.groupby(train.index.year).mean()
mk = mann_kendall(ann_train.values)
diagnostics = {
    "kpss_level": {"test": "KPSS (level)", "statistic": float(kp[0]), "p_value": float(kp[1]), "lags": int(kp[2]),
                   "sample_end": TRAIN_END, "note": "seasonally adjusted training series (month means removed); p-value interpolated from the KPSS table, bounded in [0.01, 0.10]"},
    "adf_seasonally_adjusted": {"test": "ADF (constant, AIC lag)", "statistic": float(ad[0]), "p_value": float(ad[1]),
                                "lags": int(ad[2]), "sample_end": TRAIN_END,
                                "note": "seasonally adjusted training series"},
    "mann_kendall_annual": {"test": "Mann-Kendall", "statistic": mk["z"], "p_value": mk["p"],
                            "sen_slope": mk["sen_slope_per_year"], "sen_slope_per_decade": mk["sen_slope_per_year"] * 10,
                            "statistic_autocorr_corrected": mk["z_corrected"], "p_value_autocorr_corrected": mk["p_corrected"],
                            "variance_inflation": mk["variance_inflation"], "S": mk["S"], "n_years": int(len(ann_train)),
                            "sample_end": TRAIN_END,
                            "note": "annual means 1981-2022; corrected variant uses the Hamed-Rao variance adjustment"},
}

# ------------------------------------------------------------------ 2. trend associations (OLS + Newey-West)
trend = {"note": "Associations with calendar time (OLS, Newey-West/HAC errors), not causal effects."}
for label, ys in [("training_1981_2022", y_all[:TRAIN_END]), ("full_1981_2025", y_all)]:
    ann = ys.groupby(ys.index.year).mean()
    yrs = ann.index.values.astype(float)
    trend[f"annual_{label}"] = trend_entry(ann.values, yrs - yrs[0], hac_lag(len(ann)))
    sa = deseason(ys)
    t_years = (np.arange(len(ys))) / 12.0
    e = trend_entry(sa.values, t_years, hac_lag(len(ys)))
    e["hac_lag_24_se_per_decade"] = float(ols_hac(sa.values, t_years, 24).bse[1] * 10)
    e["hac_lag_12_se_per_decade"] = float(ols_hac(sa.values, t_years, 12).bse[1] * 10)
    trend[f"deseasonalised_monthly_{label}"] = e
    # season-specific (meteorological seasons; DJF uses the preceding December)
    s = {}
    shifted = ys.copy()
    sidx = shifted.index
    season = np.select([sidx.month.isin([12, 1, 2]), sidx.month.isin([3, 4, 5]), sidx.month.isin([6, 7, 8])],
                       ["DJF", "MAM", "JJA"], "SON")
    syear = np.where(sidx.month == 12, sidx.year + 1, sidx.year)
    g = pd.DataFrame({"v": ys.values, "season": season, "yr": syear}).groupby(["season", "yr"])["v"].agg(["mean", "count"])
    for sn in ["DJF", "MAM", "JJA", "SON"]:
        gg = g.loc[sn]
        gg = gg[gg["count"] == 3]
        s[sn] = trend_entry(gg["mean"].values, gg.index.values.astype(float) - gg.index.values[0],
                            hac_lag(len(gg)))
    trend[f"seasonal_{label}"] = s
# amplitude / phase drift of the annual harmonic (training sample)
t_m = np.arange(len(train)) / 12.0
w = 2 * np.pi * t_m
Xa = np.column_stack([np.ones_like(t_m), t_m, np.cos(w), np.sin(w), t_m * np.cos(w), t_m * np.sin(w)])
ra = sm.OLS(train.values, Xa).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lag(len(train))})
T_end = t_m[-1]
a0 = np.hypot(ra.params[2], ra.params[3])
a1 = np.hypot(ra.params[2] + ra.params[4] * T_end, ra.params[3] + ra.params[5] * T_end)
ph0 = math.degrees(math.atan2(ra.params[3], ra.params[2]))
ph1 = math.degrees(math.atan2(ra.params[3] + ra.params[5] * T_end, ra.params[2] + ra.params[4] * T_end))
wald = ra.wald_test(np.array([[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]), scalar=True)
trend["seasonal_cycle_drift_training"] = {
    "amplitude_start_degC": float(a0), "amplitude_end_degC": float(a1), "amplitude_change_degC": float(a1 - a0),
    "phase_start_deg": ph0, "phase_end_deg": ph1, "phase_shift_deg": float(ph1 - ph0),
    "joint_wald_stat": float(np.squeeze(wald.statistic)), "joint_wald_p": float(np.squeeze(wald.pvalue)),
    "note": "annual harmonic with linearly drifting coefficients; joint HAC Wald test of both drift terms"}

# ------------------------------------------------------------------ 3. model selection (training only)
K_sel, K_aicc = select_K(train)
order, sorder, sar_aicc, fs, n_fits = select_sarima(train)
specs = {
    "seasonal_naive": ("seasonal naive", f_snaive),
    "naive": ("naive", f_naive),
    "ets_ana": ("ETS(A,N,A)", f_ets(False)),
    "ets_aada": ("ETS(A,Ad,A)", f_ets(True)),
    "sarima": (f"SARIMA{order}x{sorder}[12]" + (" with constant" if sarima_trend(order, sorder) else ""),
               f_sarima_fixed(order, sorder)),
    "harmonic_trend": (f"linear trend + {K_sel} annual harmonic(s), OLS", f_harmonic(K_sel)),
}
order_keys = list(specs)

# ------------------------------------------------------------------ 4. fixed-origin hold-out
models, oos, fc_hold = {}, {}, {}
yh = hold.values


def dm_test(e_base, e_mod, power, h):
    d = np.abs(e_base) ** power - np.abs(e_mod) ** power  # positive = model better
    n = len(d)
    dbar = d.mean()
    dc = d - dbar
    g0 = np.sum(dc * dc) / n
    v = g0
    for k in range(1, h):
        v += 2 * (1 - k / h) * np.sum(dc[k:] * dc[:-k]) / n  # Bartlett weights keep v >= 0
    v = v / n
    if v <= 0:
        return {"statistic": None, "p_value": None}
    stat = dbar / math.sqrt(v)
    hln = math.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    st = stat * hln
    return {"statistic": float(st), "p_value": float(2 * (1 - stats.t.cdf(abs(st), n - 1))), "mean_loss_diff": float(dbar)}


errs = {}
for key in order_keys:
    label, fn = specs[key]
    out = fn(train, 36)
    assert list(out["idx"]) == list(hold_idx), key
    fc_hold[key] = out
    e = yh - out["mean"]
    errs[key] = e
    models[key] = {"model": label, "train_end": TRAIN_END, "n_train": int(len(train)),
                   "fit": out["fit"], "parameters": out["params"]}
models["harmonic_trend"]["selection"] = {"K_aicc": {str(k): v for k, v in K_aicc.items()}, "K_selected": K_sel}
models["sarima"]["selection"] = {"order": list(order), "seasonal_order": list(sorder), "aicc": sar_aicc,
                                 "seasonal_strength": fs, "n_candidate_fits": n_fits,
                                 "rule": "D=1 if STL seasonal strength > 0.64; d by KPSS; p,q<=3,P,Q<=2 stepwise AICc"}

for key in order_keys:
    o = fc_hold[key]
    e = errs[key]
    rm, ma = float(np.sqrt(np.mean(e ** 2))), float(np.mean(np.abs(e)))
    cov = float(np.mean((yh >= o["lower"]) & (yh <= o["upper"])))
    entry = {"model": key, "train_end": TRAIN_END, "test_start": HOLD_START, "test_end": HOLD_END, "n_test": 36,
             "rmse": rm, "mae": ma, "mase": ma / mase_scale, "coverage": cov, "interval_level": 1 - ALPHA,
             "mean_error": float(np.mean(e)),
             "mean_interval_width": float(np.mean(o["upper"] - o["lower"])),
             "predictions": [{"period": p, "forecast": float(f), "lower": float(lo), "upper": float(up)}
                             for p, f, lo, up in zip(per(hold_idx), o["mean"], o["lower"], o["upper"])]}
    blocks = {}
    for b, (a, z) in {"h01_12": (0, 12), "h13_24": (12, 24), "h25_36": (24, 36)}.items():
        blocks[b] = {"rmse": float(np.sqrt(np.mean(e[a:z] ** 2))), "mae": float(np.mean(np.abs(e[a:z]))),
                     "coverage": float(np.mean((yh[a:z] >= o["lower"][a:z]) & (yh[a:z] <= o["upper"][a:z])))}
    entry["by_horizon_block"] = blocks
    if key != "seasonal_naive":
        entry["dm_vs_seasonal_naive"] = {
            "squared_h12": dm_test(errs["seasonal_naive"], e, 2, 12), "absolute_h12": dm_test(errs["seasonal_naive"], e, 1, 12),
            "squared_h1": dm_test(errs["seasonal_naive"], e, 2, 1), "absolute_h1": dm_test(errs["seasonal_naive"], e, 1, 1),
            "note": "positive mean_loss_diff = model has lower loss than seasonal naive; HLN-corrected, t(35); Bartlett long-run variance with truncation h=12 (seasonal cycle) or h=1"}
    oos[f"{key}_test"] = entry
dm_tests = {k.replace("_test", ""): v["dm_vs_seasonal_naive"] for k, v in oos.items() if "dm_vs_seasonal_naive" in v}
horizon_table = {key: {"abs_error_by_h": [float(x) for x in np.abs(errs[key])],
                       "error_by_h": [float(x) for x in errs[key]]} for key in order_keys}
horizon_table["periods"] = per(hold_idx)

# ------------------------------------------------------------------ 5. rolling origin inside training
origins = [pd.Timestamp(f"{yr}-12-01") for yr in range(2000, 2020)]
roll_err = {k: [] for k in order_keys}
roll_tgt_month = []
for o_ in origins:
    ytr = y_all[:o_]
    yte = y_all[o_ + pd.offsets.MonthBegin(1):][:36]
    if len(yte) < 36 or yte.index[-1] > pd.Timestamp("2022-12-01"):
        raise RuntimeError("rolling window leaks into hold-out")
    roll_tgt_month.append(yte.index.month.values)
    for key in order_keys:
        fn = specs[key][1]
        try:
            m = fn(ytr, 36)["mean"]
        except Exception:
            m = np.full(36, np.nan)
        roll_err[key].append(yte.values - m)
roll_err = {k: np.array(v) for k, v in roll_err.items()}  # origins x horizons
tgt_m = np.array(roll_tgt_month)
seas_of = lambda m: np.select([np.isin(m, [12, 1, 2]), np.isin(m, [3, 4, 5]), np.isin(m, [6, 7, 8])], [0, 1, 2], 3)
tgt_s = seas_of(tgt_m)
base_rmse_h = np.sqrt(np.nanmean(roll_err["seasonal_naive"] ** 2, axis=0))
rolling = {"origins": [o_.strftime("%Y-%m") for o_ in origins], "horizon": 36, "n_origins": len(origins),
           "note": "Origins overlap (36-month horizon, annual spacing): errors are not independent. Used for horizon and season skill, not for model choice of the frozen setup."}
for key in order_keys:
    E = roll_err[key]
    rm_h = np.sqrt(np.nanmean(E ** 2, axis=0))
    blocks = {}
    for b, (a, z) in {"h01_12": (0, 12), "h13_24": (12, 24), "h25_36": (24, 36)}.items():
        r_b = float(np.sqrt(np.nanmean(E[:, a:z] ** 2)))
        r_s = float(np.sqrt(np.nanmean(roll_err["seasonal_naive"][:, a:z] ** 2)))
        blocks[b] = {"rmse": r_b, "mae": float(np.nanmean(np.abs(E[:, a:z]))), "relative_rmse_vs_seasonal_naive": r_b / r_s}
    seas = {}
    for si, sn in enumerate(["DJF", "MAM", "JJA", "SON"]):
        msk = tgt_s == si
        r_k = float(np.sqrt(np.nanmean(E[msk] ** 2)))
        r_s = float(np.sqrt(np.nanmean(roll_err["seasonal_naive"][msk] ** 2)))
        seas[sn] = {"rmse": r_k, "relative_rmse_vs_seasonal_naive": r_k / r_s}
    rolling[key] = {"rmse_overall": float(np.sqrt(np.nanmean(E ** 2))), "mae_overall": float(np.nanmean(np.abs(E))),
                    "mase_overall": float(np.nanmean(np.abs(E)) / mase_scale),
                    "rmse_by_horizon": [float(x) for x in rm_h],
                    "relative_rmse_by_horizon": [float(x) for x in rm_h / base_rmse_h],
                    "by_horizon_block": blocks, "by_target_season": seas}
    if key != "seasonal_naive":
        rolling[key]["dm_vs_seasonal_naive_pooled_squared"] = dm_test(
            roll_err["seasonal_naive"].ravel(), E.ravel(), 2, 36)

# ------------------------------------------------------------------ 6. forecasts beyond the data (refit on all 540 months)
forecasts = {}
for key in order_keys:
    label, fn = specs[key]
    out = fn(y_all, H_FWD)
    assert list(out["idx"]) == list(fwd_idx), key
    models[f"{key}_full"] = {"model": label + " (refit on all periods)", "train_end": HOLD_END,
                             "n_train": int(len(y_all)), "fit": out["fit"], "parameters": out["params"]}
    forecasts[f"{key}_2026_2028"] = {
        "model": f"{key}_full", "horizon": H_FWD, "interval_level": 1 - ALPHA,
        "points": [{"period": p, "forecast": float(f), "lower": float(lo), "upper": float(up)}
                   for p, f, lo, up in zip(per(fwd_idx), out["mean"], out["lower"], out["upper"])]}
    pts = forecasts[f"{key}_2026_2028"]["points"]
    for p in pts:  # guard: point forecasts inside intervals
        assert p["lower"] <= p["forecast"] <= p["upper"], (key, p)

# ------------------------------------------------------------------ write
ann_full = y_all.groupby(y_all.index.year).mean()
res = {
    "result_kind": "timeseries",
    "series": {"name": "monthly mean 2 m air temperature, Frankfurt am Main (NASA POWER, 50.11 N, 8.68 E)",
               "frequency": "monthly", "start": "1981-01", "end": "2025-12", "n_observations": int(n_raw),
               "unit": "degrees C", "n_train": 504, "n_holdout": 36,
               "mase_scale_seasonal_naive_mae_train": mase_scale,
               "sample_flow": [{"step": "raw monthly rows", "n": int(n_raw)},
                               {"step": "missing T2M dropped", "n": 0},
                               {"step": "training 1981-01..2022-12", "n": 504},
                               {"step": "hold-out 2023-01..2025-12", "n": 36}],
               "note": "Data end in 2025-12 because the POWER monthly load covers whole years."},
    "software": {"python_statsmodels": statsmodels.__version__, "numpy": np.__version__, "pandas": pd.__version__,
                 "seed": 20260101},
    "diagnostics": diagnostics,
    "trend": trend,
    "models": models,
    "forecasts": forecasts,
    "out_of_sample": oos,
    "dm_tests": dm_tests,
    "horizon_errors": horizon_table,
    "rolling_origin": rolling,
}
# ------------------------------------------------------------------ 7. pre-registered hypotheses (preregistration.lock.json)
a_tr = trend["annual_training_1981_2022"]
pair = {}
for b_ in ["ets_ana", "ets_aada", "sarima"]:
    pair[f"{b_}_vs_harmonic_trend"] = dm_test(errs[b_], errs["harmonic_trend"], 2, 12)  # positive = harmonic_trend better
non_naive = [k for k in order_keys if k not in ("seasonal_naive", "naive")]
sn_oos = oos["seasonal_naive_test"]
h2_models = {k: {"holdout_mase": oos[f"{k}_test"]["mase"],
                 "holdout_rmse_ratio_vs_seasonal_naive": oos[f"{k}_test"]["rmse"] / sn_oos["rmse"],
                 "holdout_rmse_ratio_h25_36": oos[f"{k}_test"]["by_horizon_block"]["h25_36"]["rmse"] /
                 sn_oos["by_horizon_block"]["h25_36"]["rmse"],
                 "rolling_mase": rolling[k]["mase_overall"],
                 "rolling_relative_rmse_h25_36": rolling[k]["by_horizon_block"]["h25_36"]["relative_rmse_vs_seasonal_naive"],
                 "dm_squared_h12_p": oos[f"{k}_test"]["dm_vs_seasonal_naive"]["squared_h12"]["p_value"]}
             for k in non_naive}
best_rank = sorted(non_naive, key=lambda k: oos[f"{k}_test"]["rmse"])
_hyp = [
    {"hypothesis": "H1", "test": "OLS/HAC linear trend of annual mean T2M on year, training years 1981-2022",
     "n_observations": a_tr["n"], "estimate_per_decade": a_tr["slope_per_decade"], "se_per_decade": a_tr["se_per_decade"],
     "ci_lower_per_decade": a_tr["ci_lower_per_decade"], "ci_upper_per_decade": a_tr["ci_upper_per_decade"],
     "p_value": a_tr["p_value"], "positive": bool(a_tr["slope_per_decade"] > 0),
     "in_prior_range_0.3_0.5": bool(0.3 <= a_tr["slope_per_decade"] <= 0.5),
     "note": "association with calendar time, not a causal effect"},
    {"hypothesis": "H2", "test": "hold-out and rolling-origin RMSE/MASE of non-naive models relative to seasonal naive",
     "n_observations": 36, "models": h2_models, "seasonal_naive_holdout_mase": sn_oos["mase"],
     "prior_mase_range": [0.75, 0.95],
     "note": "ratio < 1 = model better than seasonal naive; DM p-values in dm_tests"},
    {"hypothesis": "H3", "test": "pairwise Diebold-Mariano (squared error, HLN, h=12) of ETS/SARIMA against harmonic_trend on the hold-out",
     "n_observations": 36, "pairwise_dm": pair, "holdout_rmse_ranking_non_naive": best_rank,
     "n_pairs_significant_5pct": int(sum(1 for v in pair.values() if v["p_value"] is not None and v["p_value"] < 0.05)),
     "note": "positive mean_loss_diff = harmonic_trend lower loss"},
]
res["h1_result"], res["h2_result"], res["h3_result"] = _hyp
# tag the entries that carry each pre-registered result with the hypothesis they test
res["trend"]["annual_training_1981_2022"]["hypothesis"] = "H1"
for k_ in non_naive:
    res["out_of_sample"][f"{k_}_test"]["hypothesis"] = "H2"
    res["dm_tests"][k_]["hypothesis"] = "H2"
res["hypotheses"] = {
    "H1": {"hypothesis": "H1", "result_path": "trend.annual_training_1981_2022", "n_observations": a_tr["n"],
           "estimate_per_decade": a_tr["slope_per_decade"]},
    "H2": {"hypothesis": "H2", "result_path": "out_of_sample / dm_tests / rolling_origin", "n_observations": 36},
    "H3": {"hypothesis": "H3", "result_path": "h3_result.pairwise_dm", "n_observations": 36},
}
with open("estimation_results.json", "w") as f:
    json.dump(clean(res), f, indent=1, allow_nan=False)

print("SARIMA:", order, sorder, "K:", K_sel)
for k, v in oos.items():
    print(k, round(v["rmse"], 3), round(v["mae"], 3), round(v["mase"], 3), round(v["coverage"], 3))
print("DM", {k: (v["squared_h12"]["statistic"], v["squared_h12"]["p_value"]) for k, v in dm_tests.items()})
print("trend annual train", trend["annual_training_1981_2022"]["slope_per_decade"],
      trend["annual_training_1981_2022"]["se_per_decade"])
print("diagnostics", {k: (v["statistic"], v["p_value"]) for k, v in diagnostics.items()})
