"""Staggered DiD of primary-fee abolition on GER. Reads data.db only."""
import json, sqlite3, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm

warnings.filterwarnings("ignore")
B = 999
SEED = 20261013
EMIN, EMAX = -6, 5

con = sqlite3.connect("data.db")
panel = pd.read_sql("SELECT * FROM wb_primary_enrolment WHERE year<=2010", con)
dates = pd.read_sql("SELECT iso3, first_year, alt_year FROM fee_abolition_dates", con)
panel = panel.merge(dates[["iso3", "first_year"]], on="iso3", how="left")
panel["g"] = panel["first_year"].fillna(0).astype(int)
panel["log_gdp"] = np.log(panel["gdp_pc"])
years = np.arange(1980, 2011)
T = len(years)
raw_rows = len(panel)
sample_flow = {"raw_rows_1980_2010": raw_rows,
               "rows_with_ger_primary": int(panel.ger_primary.notna().sum()),
               "rows_ger_outlier_flag": int(panel.ger_outlier.fillna(0).sum())}


def wide(col, df=panel):
    w = df.pivot(index="iso3", columns="year", values=col).reindex(columns=years)
    return w


def build(col, df=panel):
    w = wide(col, df)
    keep = w.index[w.notna().any(axis=1)]
    w = w.loc[keep]
    g = df.drop_duplicates("iso3").set_index("iso3").loc[keep, "g"].values.astype(int)
    return w.values.astype(float), g, list(keep)


def covX(units):
    cols = []
    for c in ["log_gdp", "urban_share"]:
        cols.append(wide(c).loc[units].values)
    return np.stack(cols, axis=2)  # n,T,k


def cs_core(Y, g, ant=0, nyt=False, X=None, emin=EMIN, emax=EMAX):
    ref = -1 - ant
    es = list(range(emin, emax + 1))
    gt = {}
    for c in sorted(set(g[g > 0])):
        b = c + ref
        if b < years[0] or b > years[-1]:
            continue
        bi = b - years[0]
        for e in es:
            if e == ref:
                continue
            t = c + e
            if t < years[0] or t > years[-1]:
                continue
            ti = t - years[0]
            ok = np.isfinite(Y[:, ti]) & np.isfinite(Y[:, bi])
            tr = ok & (g == c)
            ct = ok & ((g == 0) | ((g > max(t, b) + ant) & (g != c) if nyt else (g == 0)))
            if nyt:
                ct = ok & ((g == 0) | ((g > max(t, b) + ant)))
            if X is not None:
                ci = c - 1 - years[0]
                xv = np.all(np.isfinite(X[:, ci, :]), axis=1)
                tr &= xv
                ct &= xv
            if tr.sum() == 0 or ct.sum() < 3:
                continue
            d = Y[:, ti] - Y[:, bi]
            if X is None:
                a = d[tr].mean() - d[ct].mean()
            else:
                Xc = sm.add_constant(X[ct][:, c - 1 - years[0], :], has_constant="add")
                if ct.sum() < Xc.shape[1] + 2:
                    continue
                beta = np.linalg.lstsq(Xc, d[ct], rcond=None)[0]
                Xt = sm.add_constant(X[tr][:, c - 1 - years[0], :], has_constant="add")
                a = (d[tr] - Xt @ beta).mean()
            gt[(c, e)] = (a, tr.sum())
    theta = []
    for e in es:
        if e == ref:
            theta.append(0.0)
            continue
        v = [(a, n) for (c, ee), (a, n) in gt.items() if ee == e]
        theta.append(np.average([a for a, n in v], weights=[n for a, n in v]) if v else np.nan)
    post = [(a, n) for (c, e), (a, n) in gt.items() if e >= 0]
    att = np.average([a for a, n in post], weights=[n for a, n in post]) if post else np.nan
    return np.array([att] + theta), gt


def boot(fun, n, B=B, seed=SEED):
    rng = np.random.default_rng(seed)
    pt = np.asarray(fun(np.arange(n)), float)
    dr = np.array([fun(rng.integers(0, n, n)) for _ in range(B)], float)
    return pt, dr


def pval(est, se, df):
    if not (np.isfinite(est) and np.isfinite(se)) or se <= 0:
        return None, None
    t = est / se
    return float(t), float(2 * stats.t.sf(abs(t), df))


def coef(est, se, df):
    t, p = pval(est, se, df)
    if t is None:
        return {"estimate": float(est), "se": None, "t_stat": None, "p_value": None, "df": df}
    return {"estimate": float(est), "se": float(se), "t_stat": t, "p_value": p, "df": int(df),
            "ci_lower": float(est - stats.t.ppf(.975, df) * se), "ci_upper": float(est + stats.t.ppf(.975, df) * se)}


def nobs(Y):
    return int(np.isfinite(Y).sum())


def spec_entry(name, Y, g, units, pt, dr, hyp=None, estimator="callaway_santanna", extra=None, fe=None,
               controls=None, label=None):
    G = len(units)
    se = np.nanstd(dr, axis=0, ddof=1)
    entry = {"specification": name, "estimator": estimator,
             "n_observations": nobs(Y), "n_clusters": G, "cluster_level": "iso3",
             "n_treated_clusters": int((g > 0).sum()),
             "fixed_effects": fe if fe is not None else [], "controls": controls or [],
             "bootstrap_draws": int(len(dr)), "df": G - 1,
             "coefficients": {"att": coef(pt[0], se[0], G - 1)},
             "diagnostics": {"df_residual": G - 1, "n_cohorts": int(len(set(g[g > 0]))),
                             "bootstrap_valid_draws": int(np.isfinite(dr[:, 0]).sum())}}
    if hyp:
        entry["hypothesis"] = hyp
    if extra:
        entry.update(extra)
    return entry


results, rob = {}, {}
out = {}

# ---------- Main: CS, never-treated, level and log ----------
Y, g, units = build("ger_primary")
n_units = len(units)
treated_units = [u for u, gg in zip(units, g) if gg > 0]
sample_flow["units_with_ger"] = n_units
sample_flow["treated_units"] = treated_units
sample_flow["comparison_units"] = int((g == 0).sum())
sample_flow["rows_in_main_sample"] = nobs(Y)

es_list = list(range(EMIN, EMAX + 1))


def run_cs(Y, g, units, **kw):
    f = lambda idx: cs_core(Y[idx], g[idx], X=(kw.get("X")[idx] if kw.get("X") is not None else None),
                            **{k: v for k, v in kw.items() if k != "X"})[0]
    return boot(f, len(units))


pt, dr = run_cs(Y, g, units)
base_gt = cs_core(Y, g)[1]
cohort_att = {}
main_extra = {"base": "universal (g-1)", "aggregation": "cohort-size weighted mean of ATT(g,t), t>=g, e in [0,5]",
              "comparison_group": "never_treated (undated comparison units)", "ci_type": "pointwise"}
results["main"] = spec_entry("Callaway-Sant'Anna ATT, GER level, undated comparison group", Y, g, units, pt, dr,
                             hyp="H1", extra=main_extra)
results["main"]["diagnostics"]["pre_trend_p_value"] = None
main_pt, main_dr = pt, dr

# event study
se_es = np.nanstd(dr, axis=0, ddof=1)
periods = []
for k, e in enumerate(es_list):
    est, se = pt[k + 1], se_es[k + 1]
    if np.isnan(est):
        continue
    d = {"relative_period": e, "estimate": float(est), "se": float(se)}
    d["ci_lower"], d["ci_upper"] = float(est - 1.96 * se), float(est + 1.96 * se)
    periods.append(d)
out["event_study"] = {"reference_period": -1, "estimator": "callaway_santanna", "base": "universal",
                      "outcome": "ger_primary", "ci_type": "pointwise, 1.96 SE", "periods": periods}

# pre-trend Wald
pre_idx = [k + 1 for k, e in enumerate(es_list) if e < -1 and np.isfinite(pt[k + 1])]
th = pt[pre_idx]
ok = np.all(np.isfinite(dr[:, pre_idx]), axis=1)
V = np.cov(dr[ok][:, pre_idx].T)
W = float(th @ np.linalg.pinv(V) @ th)
pp = float(stats.chi2.sf(W, len(pre_idx)))
out["pre_trends"] = {"test": "Wald test that pre-treatment event-time effects (e=-6..-2) are jointly zero, bootstrap covariance",
                     "statistic": W, "df": len(pre_idx), "p_value": pp, "n_pre_periods": len(pre_idx),
                     "note": "A non-rejection is not evidence of parallel trends (low power, Roth 2022)."}
results["main"]["pre_trend_p_value"] = pp
results["main"]["diagnostics"]["pre_trend_p_value"] = pp

# HonestDiD (conservative relative magnitudes)
thetas = np.array([0.0 if e == -1 else pt[k + 1] for k, e in enumerate(es_list) if e <= -1])
Mval = float(np.nanmax(np.abs(np.diff(thetas))))
att, se_att = pt[0], np.nanstd(dr[:, 0], ddof=1)
mean_h = np.mean(np.arange(0, EMAX + 1) + 1)
hd = {"method": "Rambachan-Roth relative magnitudes (conservative closed-form bound, not the exact procedure)",
      "M_max_pre_change": Mval, "target": "overall ATT, mean horizon factor %.1f" % mean_h}
for mb in (0.5, 1, 2):
    w = mb * Mval * mean_h
    hd["mbar_%s" % str(mb).replace(".", "_")] = {"mbar": mb, "ci_lower": float(att - w - 1.96 * se_att),
                                                  "ci_upper": float(att + w + 1.96 * se_att)}
hd["mbar"] = 1.0
hd["ci_lower"] = hd["mbar_1"]["ci_lower"]
hd["ci_upper"] = hd["mbar_1"]["ci_upper"]
bd = (abs(att) - 1.96 * se_att) / (Mval * mean_h)
hd["breakdown_mbar"] = float(max(bd, 0.0))
sens = {"honest_did_rm": hd}

# ---------- log GER ----------
Yl, gl, ul = build("log_ger")
ptl, drl = run_cs(Yl, gl, ul)
results["cs_log_ger"] = spec_entry("Callaway-Sant'Anna ATT, log GER", Yl, gl, ul, ptl, drl, hyp="H1", extra=main_extra)

# ---------- Not-yet-treated ----------
ptn, drn = run_cs(Y, g, units, nyt=True)
results["cs_not_yet_treated"] = spec_entry("CS ATT, GER level, not-yet-treated comparison", Y, g, units, ptn, drn,
                                           extra={"base": "universal (g-1)", "comparison_group": "not_yet_treated"})
ptnl, drnl = run_cs(Yl, gl, ul, nyt=True)
results["cs_not_yet_treated_log"] = spec_entry("CS ATT, log GER, not-yet-treated", Yl, gl, ul, ptnl, drnl)
sens["not_yet_treated"] = {"method": "comparison group: not yet treated", "estimate": float(ptn[0]),
                           "se": float(np.nanstd(drn[:, 0], ddof=1))}

# ---------- Anticipation 1 ----------
pta, dra = run_cs(Y, g, units, ant=1)
results["anticipation_1"] = spec_entry("CS ATT, anticipation = 1 (base g-2)", Y, g, units, pta, dra,
                                       extra={"base": "universal (g-2)"})
sens["anticipation_1"] = {"method": "anticipation of one year", "estimate": float(pta[0]),
                          "se": float(np.nanstd(dra[:, 0], ddof=1))}

# ---------- window [-5,5] ----------
f55 = lambda idx: cs_core(Y[idx], g[idx], emin=-5, emax=5)[0]
pt55, dr55 = boot(f55, len(units))
results["window_m5_p5"] = spec_entry("CS ATT, event window [-5,5]", Y, g, units, pt55, dr55)

# ---------- drop outliers ----------
Yo, go, uo = build("ger_primary", panel.assign(ger_primary=panel.ger_primary.where(panel.ger_outlier.fillna(0) == 0)))
pto, dro = run_cs(Yo, go, uo)
results["drop_outliers"] = spec_entry("CS ATT, flagged GER outliers dropped", Yo, go, uo, pto, dro)

# ---------- drop ZMB, GHA ----------
gd = g.copy()
for i, u in enumerate(units):
    if u in ("ZMB", "GHA"):
        gd[i] = -1
ptd, drd = run_cs(Y, gd, units)
results["drop_zmb_gha"] = spec_entry("CS ATT, ZMB (low confidence) and GHA (capitation grant) excluded", Y, gd, units, ptd, drd)

# ---------- controls ----------
Xc = covX(units)
ptc, drc = run_cs(Y, g, units, X=Xc)
results["controls"] = spec_entry("CS ATT with outcome regression on log GDP pc and urban share at g-1, GER level",
                                 Y, g, units, ptc, drc, controls=["log_gdp_pc_g_minus_1", "urban_share_g_minus_1"],
                                 extra={"base": "universal (g-1)"})

# ---------- placebo: dates moved 3 years earlier, pre-treatment data only ----------
Yp = Y.copy()
gp = g.copy()
for i in range(len(units)):
    if g[i] > 0:
        Yp[i, years >= g[i]] = np.nan
        gp[i] = g[i] - 3
fp = lambda idx: cs_core(Yp[idx], gp[idx], emin=-6, emax=2)[0]
ptp, drp = boot(fp, len(units))
sep = np.nanstd(drp[:, 0], ddof=1)
tp, pvp = pval(ptp[0], sep, len(units) - 1)
out["placebo"] = {"fake_date_minus_3": {"description": "treatment moved 3 years earlier, all post-abolition observations of treated units dropped",
                                       "estimate": float(ptp[0]), "se": float(sep), "p_value": pvp, "df": len(units) - 1,
                                       "n_observations": nobs(Yp)}}

# ---------- Leave-one-country-out ----------
loco = {}
for u in treated_units:
    gg = g.copy()
    gg[units.index(u)] = -1
    loco[u] = float(cs_core(Y, gg)[0][0])
rng_ = (min(loco.values()), max(loco.values()))
results["leave_one_country_out"] = {"specification": "CS ATT dropping each treated country in turn (point estimates)",
                                    "n_observations": nobs(Y), "n_clusters": n_units, "cluster_level": "iso3",
                                    "n_treated_clusters": len(treated_units) - 1, "fixed_effects": [], "controls": [],
                                    "coefficients": {"att_min": {"estimate": rng_[0]}, "att_max": {"estimate": rng_[1]}},
                                    "by_dropped_country": loco, "diagnostics": {}}

# ---------- Gender, NER, H2/H4 ----------
Yf, gf, uf = build("ger_female")
Ym, gm, um = build("ger_male")
common = [u for u in uf if u in um]
fi = [uf.index(u) for u in common]
mi = [um.index(u) for u in common]
Yf, Ym, gc = Yf[fi], Ym[mi], gf[fi]
fg = lambda idx: np.concatenate([cs_core(Yf[idx], gc[idx])[0], cs_core(Ym[idx], gc[idx])[0]])
ptg, drg = boot(fg, len(common))
L = len(es_list) + 1
for nm, sl, Yx in (("gender_female", slice(0, L), Yf), ("gender_male", slice(L, 2 * L), Ym)):
    results[nm] = spec_entry("CS ATT, %s GER" % nm.split("_")[1], Yx, gc, common, ptg[sl], drg[:, sl],
                             hyp="H4" if nm == "gender_female" else None)
dg = ptg[:L][0] - ptg[L:][0]
ddr = drg[:, 0] - drg[:, L]
results["gender_gap"] = spec_entry("CS ATT difference: female minus male GER", Yf, gc, common, np.array([dg]),
                                   ddr[:, None], hyp="H4",
                                   extra={"note": "positive = girls' GER rose more than boys'"})

# NER on NER sample and GER on same sample
Yn, gn, un = build("ner_primary")
Yg_n = wide('ger_primary').reindex(un).values.astype(float)
Yg_n[~np.isfinite(Yn)] = np.nan
fn = lambda idx: np.concatenate([cs_core(Yn[idx], gn[idx])[0], cs_core(Yg_n[idx], gn[idx])[0]])
ptn2, drn2 = boot(fn, len(un))
Ln = len(es_list) + 1
results["ner"] = spec_entry("CS ATT, net enrolment rate", Yn, gn, un, ptn2[:Ln], drn2[:, :Ln], hyp="H2")
results["ger_on_ner_sample"] = spec_entry("CS ATT, GER restricted to NER-observed country-years", Yg_n, gn, un,
                                          ptn2[Ln:], drn2[:, Ln:], hyp="H2")
dd = ptn2[Ln] - ptn2[0]
results["ger_minus_ner"] = spec_entry("CS ATT difference: GER minus NER on common sample", Yn, gn, un,
                                      np.array([dd]), (drn2[:, Ln] - drn2[:, 0])[:, None], hyp="H2",
                                      extra={"note": "positive = GER effect exceeds NER effect (over-age enrolment)"})

# H6 proxy: completion rate
Yc, gcm, ucm = build("completion_rate")
ptcr, drcr = run_cs(Yc, gcm, ucm)
results["completion_rate"] = spec_entry("CS ATT, primary completion rate (H6 proxy; PTR not in data)", Yc, gcm, ucm,
                                        ptcr, drcr, hyp="H6")

# ---------- H3: country ATT vs baseline GER ----------
rows = []
for u in treated_units:
    i = units.index(u)
    gg = np.where(g > 0, -1, g)
    gg[i] = g[i]
    a = cs_core(Y, gg)[0][0]
    ci = g[i] - years[0]
    pre = Y[i, max(ci - 5, 0):ci]
    rows.append((u, a, np.nanmean(pre) if np.isfinite(pre).any() else np.nan))
h3 = pd.DataFrame(rows, columns=["iso3", "att", "pre_ger"]).dropna()
m3 = sm.OLS(h3.att, sm.add_constant(h3.pre_ger)).fit(cov_type="HC3")
results["h3_initial_level"] = {
    "specification": "Country-level CS ATT regressed on mean GER in the 5 years before abolition (HC3)",
    "hypothesis": "H3", "n_observations": int(len(h3)), "n_clusters": int(len(h3)), "cluster_level": "iso3",
    "fixed_effects": [], "controls": [], "df": int(len(h3) - 2),
    "coefficients": {"pre_ger": coef(m3.params["pre_ger"], m3.bse["pre_ger"], len(h3) - 2)},
    "country_att": {r.iso3: {"att": float(r.att), "pre_ger": float(r.pre_ger)} for r in h3.itertuples()},
    "diagnostics": {"r_squared": float(m3.rsquared), "df_residual": int(len(h3) - 2)}}

# ---------- TWFE + wild cluster bootstrap ----------
def twfe(col):
    d = panel.dropna(subset=[col]).copy()
    d["D"] = ((d.g > 0) & (d.year >= d.g)).astype(float)
    ui = pd.get_dummies(d.iso3, drop_first=False).values.astype(float)
    yi = pd.get_dummies(d.year, drop_first=True).values.astype(float)
    F = np.hstack([ui, yi])
    def resid(v):
        return v - F @ np.linalg.lstsq(F, v, rcond=None)[0]
    yt, Dt = resid(d[col].values.astype(float)), resid(d.D.values)
    cl = d.iso3.values
    ug = np.unique(cl)
    def tstat(yv):
        b = (Dt @ yv) / (Dt @ Dt)
        e = yv - b * Dt
        s = sum((Dt[cl == c] @ e[cl == c]) ** 2 for c in ug)
        k = F.shape[1] + 1
        adj = len(ug) / (len(ug) - 1) * (len(yv) - 1) / (len(yv) - k)
        se = np.sqrt(adj * s) / (Dt @ Dt)
        return b, se, b / se
    b, se, t = tstat(yt)
    rng = np.random.default_rng(SEED)
    webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
    idx = {c: np.where(cl == c)[0] for c in ug}
    ts = []
    for _ in range(B):
        w = rng.choice(webb, len(ug))
        wv = np.empty(len(yt))
        for j, c in enumerate(ug):
            wv[idx[c]] = w[j]
        ts.append(tstat(yt * wv)[2])
    pw = float((np.abs(ts) >= abs(t)).mean())
    r2w = 1 - ((yt - b * Dt) ** 2).sum() / (yt ** 2).sum()
    return d, b, se, t, pw, len(ug), r2w

for col, key, hyp in (("ger_primary", "twfe_level", None), ("log_ger", "twfe_log", None)):
    d, b, se, t, pw, G, r2w = twfe(col)
    c = coef(b, se, G - 1)
    c["wild_bootstrap_p_value"] = pw
    results[key] = {"specification": "Static TWFE (country, year FE), benchmark only; wild cluster bootstrap-t (Webb), p_value is cluster-robust t",
                    "estimator": "twfe", "n_observations": int(len(d)), "n_clusters": G, "cluster_level": "iso3",
                    "n_treated_clusters": len(treated_units), "fixed_effects": ["iso3", "year"], "controls": [],
                    "df": G - 1, "coefficients": {"att": c},
                    "diagnostics": {"within_r_squared": float(r2w), "df_residual": G - 1, "wild_bootstrap_draws": B,
                                    "wild_bootstrap_p_value": pw}}

# ---------- Goodman-Bacon on balanced panel ----------
def bacon(lo, hi):
    d = panel[(panel.year >= lo) & (panel.year <= hi)]
    cnt = d.groupby("iso3").ger_primary.count()
    bal = cnt[cnt == hi - lo + 1].index
    d = d[d.iso3.isin(bal)].copy()
    d["D"] = ((d.g > 0) & (d.year >= d.g)).astype(float)
    d.loc[(d.g > 0) & (d.g <= lo), "D"] = np.nan
    dropunits = d[d.D.isna()].iso3.unique()
    d = d[~d.iso3.isin(dropunits)]
    W = d.pivot(index="iso3", columns="year", values="ger_primary")
    gu = d.drop_duplicates("iso3").set_index("iso3").g.loc[W.index]
    yrs = W.columns.values
    Tn = len(yrs)
    groups = sorted(set(gu[gu > 0])) + [0]
    n = {k: (gu == k).sum() for k in groups}
    Ntot = len(W)
    if n.get(0, 0) == 0 or len(groups) < 2:
        return None
    Dbar = {k: ((yrs >= k).mean() if k > 0 else 0.0) for k in groups}
    mean = {k: W[gu == k].mean(axis=0).values for k in groups}
    def did(k, tr_pre, tr_post, ctrl, c_pre, c_post):
        return (mean[k][tr_post].mean() - mean[k][tr_pre].mean()) - (mean[ctrl][c_post].mean() - mean[ctrl][c_pre].mean())
    comps = []
    for k in groups[:-1]:
        pre, post = yrs < k, yrs >= k
        b = did(k, pre, post, 0, pre, post)
        nku = n[k] / (n[k] + n[0])
        s = ((n[k] + n[0]) / Ntot) ** 2 * nku * (1 - nku) * Dbar[k] * (1 - Dbar[k])
        comps.append(("treated_vs_never", k, 0, b, s))
    tg = groups[:-1]
    for i, k in enumerate(tg):
        for l in tg[i + 1:]:
            nkl = n[k] / (n[k] + n[l])
            sh = ((n[k] + n[l]) / Ntot) ** 2
            win = yrs < l
            pre, post = (yrs < k) & win, (yrs >= k) & win
            b1 = did(k, pre, post, l, pre, post)
            vk = (Dbar[k] - Dbar[l]) / (1 - Dbar[l]) * (1 - Dbar[k]) / (1 - Dbar[l])
            s1 = sh * ((1 - Dbar[l]) ** 2) * nkl * (1 - nkl) * vk
            comps.append(("early_vs_later_control", k, l, b1, s1))
            win = yrs >= k
            pre, post = (yrs >= k) & (yrs < l), yrs >= l
            b2 = did(l, pre, post, k, pre, post)
            vl = Dbar[l] / Dbar[k] * (Dbar[k] - Dbar[l]) / Dbar[k]
            s2 = sh * (Dbar[k] ** 2) * nkl * (1 - nkl) * vl
            comps.append(("later_vs_already_treated_control", k, l, b2, s2))
    tot = sum(c[4] for c in comps)
    est = sum(c[3] * c[4] for c in comps) / tot
    # direct TWFE on this balanced panel
    dd = d.copy()
    ui = pd.get_dummies(dd.iso3).values.astype(float)
    yi = pd.get_dummies(dd.year, drop_first=True).values.astype(float)
    Fm = np.hstack([ui, yi])
    r = lambda v: v - Fm @ np.linalg.lstsq(Fm, v, rcond=None)[0]
    Dt = r(dd.D.values)
    direct = float((Dt @ r(dd.ger_primary.values)) / (Dt @ Dt))
    agg = {}
    for typ in set(c[0] for c in comps):
        agg[typ] = {"weight": float(sum(c[4] for c in comps if c[0] == typ) / tot),
                    "weighted_mean_estimate": float(sum(c[3] * c[4] for c in comps if c[0] == typ) /
                                                     max(sum(c[4] for c in comps if c[0] == typ), 1e-12))}
    return {"window": [lo, hi], "n_units": int(Ntot), "units": list(W.index),
            "treated_units": [u for u in W.index if gu[u] > 0], "n_comparison_units": int(n[0]),
            "dropped_already_treated_at_start": list(dropunits),
            "twfe_balanced_direct": direct, "decomposition_weighted_sum": float(est),
            "weights_sum_to_one_before_normalisation": float(tot),
            "by_type": agg,
            "components": [{"type": c[0], "early_cohort": int(c[1]), "late_cohort": int(c[2]), "estimate": float(c[3]),
                            "weight": float(c[4] / tot)} for c in comps]}

gb = None
for lo, hi in ((1985, 2010), (1990, 2010), (1990, 2008)):
    try:
        gb = bacon(lo, hi)
    except Exception as ex:
        gb = {"error": str(ex)}
    if gb and "components" in gb and len(gb["treated_units"]) >= 2:
        break
out["goodman_bacon"] = gb

# ---------- Sun-Abraham and BJS ----------
def long_frame(col, idx=None, units_=None):
    d = panel.dropna(subset=[col])[["iso3", "year", "g", col]].rename(columns={col: "y"})
    if idx is None:
        return d
    parts = []
    grp = {u: x for u, x in d.groupby("iso3")}
    for j, i in enumerate(idx):
        u = units_[i]
        if u in grp:
            x = grp[u].copy()
            x["iso3"] = "%s_%d" % (u, j)
            parts.append(x)
    return pd.concat(parts)


def sa_bjs(d):
    d = d[d.g >= 0].copy()
    d["e"] = np.where(d.g > 0, d.year - d.g, np.nan)
    ui = pd.get_dummies(d.iso3).values.astype(float)
    yi = pd.get_dummies(d.year, drop_first=True).values.astype(float)
    cols, meta = [], []
    for c in sorted(set(d.g[d.g > 0])):
        for e in range(EMIN, EMAX + 1):
            if e == -1:
                continue
            v = ((d.g == c) & (d.e == e)).values.astype(float)
            if v.sum() > 0:
                cols.append(v)
                meta.append((c, e, v.sum()))
    Xm = np.hstack([ui, yi, np.array(cols).T])
    # drop treated obs outside window (keeps comparison clean)
    inwin = (d.g == 0) | ((d.e >= EMIN) & (d.e <= EMAX))
    Xm, yv = Xm[inwin.values], d.y.values[inwin.values]
    beta = np.linalg.lstsq(Xm, yv, rcond=None)[0]
    cf = beta[ui.shape[1] + yi.shape[1]:]
    th = {}
    for e in range(EMIN, EMAX + 1):
        sel = [(cf[k], m[2]) for k, m in enumerate(meta) if m[1] == e]
        th[e] = np.average([a for a, w in sel], weights=[w for a, w in sel]) if sel else (0.0 if e == -1 else np.nan)
    post = [(cf[k], m[2]) for k, m in enumerate(meta) if m[1] >= 0]
    sa_att = np.average([a for a, w in post], weights=[w for a, w in post])
    # BJS: FE on untreated obs
    unt = ((d.g == 0) | (d.year < d.g)).values
    Fa = np.hstack([ui, yi])
    bb = np.linalg.lstsq(Fa[unt], d.y.values[unt], rcond=None)[0]
    tr = ((d.g > 0) & (d.e >= 0) & (d.e <= EMAX)).values
    tau = d.y.values[tr] - Fa[tr] @ bb
    bj_att = tau.mean()
    return np.array([sa_att] + [th[e] for e in range(EMIN, EMAX + 1)] + [bj_att])

d0 = long_frame("ger_primary")
pt_s = sa_bjs(d0)
rng = np.random.default_rng(SEED)
BS = 499
dr_s = []
for _ in range(BS):
    idx = rng.integers(0, n_units, n_units)
    try:
        dr_s.append(sa_bjs(long_frame("ger_primary", idx, units)))
    except Exception:
        pass
dr_s = np.array(dr_s)
L = len(es_list) + 1
results["sun_abraham"] = spec_entry("Sun-Abraham interaction-weighted ATT (country, year FE; undated comparison); unit-bootstrap SE",
                                    Y, g, units, pt_s[:L], dr_s[:, :L], estimator="sun_abraham",
                                    fe=["iso3", "year"], extra={"bootstrap_draws": int(len(dr_s))})
results["bjs_imputation"] = spec_entry("Borusyak-Jaravel-Spiess imputation ATT (FE fitted on untreated obs); unit-bootstrap SE",
                                       Y, g, units, pt_s[L:], dr_s[:, L:], estimator="borusyak_jaravel_spiess",
                                       fe=["iso3", "year"], extra={"bootstrap_draws": int(len(dr_s))})
out["sun_abraham_event_study"] = [{"relative_period": e, "estimate": float(pt_s[1 + k]),
                                   "se": float(np.nanstd(dr_s[:, 1 + k], ddof=1))} for k, e in enumerate(es_list)]

out["sensitivity"] = sens
out["sample_flow"] = sample_flow
out["h5_note"] = {"hypothesis": "H5", "status": "not estimable: capitation-grant status by country is not in data.db"}

final = {"main": results.pop("main")}
final.update(results)
final.update({k: v for k, v in out.items()})
final["rounding_note"] = None
del final["rounding_note"]


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o

json.dump(clean(final), open("estimation_results.json", "w"), indent=1)
print(json.dumps(clean({k: (final[k]["coefficients"] if isinstance(final[k], dict) and "coefficients" in final[k] else None)
                        for k in final}), indent=0)[:6000])
print("pretrend", W, pp, "M", Mval)
print(json.dumps(clean(out["goodman_bacon"]), indent=0)[:1500] if out["goodman_bacon"] else None)
