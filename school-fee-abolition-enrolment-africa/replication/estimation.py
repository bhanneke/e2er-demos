"""
Replication script for: Did Abolishing Primary-School Fees Raise Enrolment?
Evidence from Staggered Reforms in Sub-Saharan Africa
Paper ID: 30170166-245c-4c41-a957-50eb2f1cf0df

Requirements: numpy, pandas, scipy, statsmodels, matplotlib (python >= 3.9)
Usage: python replication/estimation.py   (paths are relative to this file)
Output: replication/output/ (tables as CSV, figures as PNG, estimation_results.json)

README (kept here because the package ships a single file)
----------------------------------------------------------
1. Data requirements. Reads ../data.db (SQLite), tables:
   - wb_primary_enrolment: country-year panel (World Bank WDI), cut at 2010 (= last
     cohort 2005 + 5, so later abolitions never enter the comparison group).
   - fee_abolition_dates: published-source first years (MWI 1994, UGA 1997, LSO 2000,
     TZA 2002, ZMB 2002 [low confidence], KEN 2003, RWA 2003, GHA 2005). All other
     countries are undated comparison units, NOT verified never-abolishers.
   - ger_event_time_means: raw GER means by event time (Figure 2 only).
   Data files are not shipped. replication/data_queries.sql and replication/audit_log.csv
   document how data.db was built. Do not use Allium for these tables.
2. Environment: pip install numpy pandas scipy statsmodels matplotlib
   (record `pip freeze` with your run; versions used for the paper are in the audit log).
3. Steps: (a) place data.db one level above this file; (b) run
   `python replication/estimation.py` (bootstrap-heavy, roughly 10-20 minutes).
4. Output map (replication/output/):
   table1_summary.csv        -> Table 1, sample flow and GER summary
   table2_main_att.csv       -> Table 2, main CS ATT and estimator comparison
   table3_robustness.csv     -> Table 3, robustness, gender, NER, completion
   table_event_study.csv     -> Figure 1 data (CS event study)
   table_leave_one_out.csv   -> leave-one-country-out ATTs (robustness text)
   fig_event_study.png       -> Figure 1
   fig_ger_event_time.png    -> Figure 2
   estimation_results.json   -> every estimate, incl. pre-trend Wald, HonestDiD,
                                Goodman-Bacon, placebo, H3
5. Audit trail: replication/audit_log.csv and replication/data_queries.sql.

Estimation (econometric_spec.md): Callaway-Sant'Anna ATT, no covariates, undated
comparison group, anticipation 0, universal base g-1; country-level bootstrap
(999 draws, seed 20261013), SE = SD of draws, t with G-1 df. Standard errors are
cluster (country) bootstrap SEs, as the spec requires, not HC. TWFE is a benchmark
with country-clustered SEs and a Webb wild cluster bootstrap-t. H5 is not estimable
with these data; H6 uses the completion rate as a partial proxy.
"""
import json, sqlite3, warnings
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm

np.random.seed(42)
warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = HERE.parent / "data.db"

B = 999
SEED = 20261013
EMIN, EMAX = -6, 5

# ── 1. Load data ──────────────────────────────────────────────────────────────
con = sqlite3.connect(str(DB_PATH))
panel = pd.read_sql("SELECT * FROM wb_primary_enrolment WHERE year<=2010", con)
dates = pd.read_sql("SELECT iso3, first_year, alt_year FROM fee_abolition_dates", con)
event_time_means = pd.read_sql("SELECT * FROM ger_event_time_means", con)
con.close()

# ── 2. Variable construction ──────────────────────────────────────────────────
panel = panel.merge(dates[["iso3", "first_year"]], on="iso3", how="left")
panel["g"] = panel["first_year"].fillna(0).astype(int)  # g = 0: undated comparison unit
panel["log_gdp"] = np.log(panel["gdp_pc"])
years = np.arange(1980, 2011)
T = len(years)
raw_rows = len(panel)
sample_flow = {"raw_rows_1980_2010": raw_rows,
               "rows_with_ger_primary": int(panel.ger_primary.notna().sum()),
               "rows_ger_outlier_flag": int(panel.ger_outlier.fillna(0).sum())}


def wide(col, df=panel):
    return df.pivot(index="iso3", columns="year", values=col).reindex(columns=years)


def build(col, df=panel):
    w = wide(col, df)
    keep = w.index[w.notna().any(axis=1)]
    w = w.loc[keep]
    g = df.drop_duplicates("iso3").set_index("iso3").loc[keep, "g"].values.astype(int)
    return w.values.astype(float), g, list(keep)


def covX(units):
    cols = [wide(c).loc[units].values for c in ["log_gdp", "urban_share"]]
    return np.stack(cols, axis=2)  # n,T,k


# ── Estimators ────────────────────────────────────────────────────────────────
def cs_core(Y, g, ant=0, nyt=False, X=None, emin=EMIN, emax=EMAX):
    """Callaway-Sant'Anna ATT(g,t), base g-1-ant for all e; returns [ATT, theta(e)...]."""
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
            ct = ok & (g == 0)
            if nyt:
                ct = ok & ((g == 0) | (g > max(t, b) + ant))
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
    """Country-level (pairs) bootstrap."""
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
               controls=None):
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


def run_cs(Y, g, units, **kw):
    X = kw.get("X")
    f = lambda idx: cs_core(Y[idx], g[idx], X=(X[idx] if X is not None else None),
                            **{k: v for k, v in kw.items() if k != "X"})[0]
    return boot(f, len(units))


results, out = {}, {}

# ── 3. Summary statistics / sample flow ───────────────────────────────────────
Y, g, units = build("ger_primary")
n_units = len(units)
treated_units = [u for u, gg in zip(units, g) if gg > 0]
sample_flow["units_with_ger"] = n_units
sample_flow["treated_units"] = treated_units
sample_flow["comparison_units"] = int((g == 0).sum())
sample_flow["rows_in_main_sample"] = nobs(Y)
es_list = list(range(EMIN, EMAX + 1))

# ── 4. Main specification: CS, undated comparison group (H1) ──────────────────
pt, dr = run_cs(Y, g, units)
main_extra = {"base": "universal (g-1)", "aggregation": "cohort-size weighted mean of ATT(g,t), t>=g, e in [0,5]",
              "comparison_group": "never_treated (undated comparison units)", "ci_type": "pointwise"}
results["main"] = spec_entry("Callaway-Sant'Anna ATT, GER level, undated comparison group", Y, g, units, pt, dr,
                             hyp="H1", extra=main_extra)

# event study
se_es = np.nanstd(dr, axis=0, ddof=1)
periods = []
for k, e in enumerate(es_list):
    est, se = pt[k + 1], se_es[k + 1]
    if np.isnan(est):
        continue
    periods.append({"relative_period": e, "estimate": float(est), "se": float(se),
                    "ci_lower": float(est - 1.96 * se), "ci_upper": float(est + 1.96 * se)})
out["event_study"] = {"reference_period": -1, "estimator": "callaway_santanna", "base": "universal",
                      "outcome": "ger_primary", "ci_type": "pointwise, 1.96 SE", "periods": periods}

# pre-trend Wald test (bootstrap covariance)
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

# HonestDiD (conservative closed-form relative-magnitudes bound)
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
hd["breakdown_mbar"] = float(max((abs(att) - 1.96 * se_att) / (Mval * mean_h), 0.0))
sens = {"honest_did_rm": hd}

# log GER
Yl, gl, ul = build("log_ger")
ptl, drl = run_cs(Yl, gl, ul)
results["cs_log_ger"] = spec_entry("Callaway-Sant'Anna ATT, log GER", Yl, gl, ul, ptl, drl, hyp="H1", extra=main_extra)

# ── 5. Robustness checks ──────────────────────────────────────────────────────
# not-yet-treated comparison
ptn, drn = run_cs(Y, g, units, nyt=True)
results["cs_not_yet_treated"] = spec_entry("CS ATT, GER level, not-yet-treated comparison", Y, g, units, ptn, drn,
                                           extra={"base": "universal (g-1)", "comparison_group": "not_yet_treated"})
# anticipation = 1
pta, dra = run_cs(Y, g, units, ant=1)
results["anticipation_1"] = spec_entry("CS ATT, anticipation = 1 (base g-2)", Y, g, units, pta, dra,
                                       extra={"base": "universal (g-2)"})
# window [-5,5]
f55 = lambda idx: cs_core(Y[idx], g[idx], emin=-5, emax=5)[0]
pt55, dr55 = boot(f55, len(units))
results["window_m5_p5"] = spec_entry("CS ATT, event window [-5,5]", Y, g, units, pt55, dr55)
# drop flagged outliers
Yo, go, uo = build("ger_primary", panel.assign(ger_primary=panel.ger_primary.where(panel.ger_outlier.fillna(0) == 0)))
pto, dro = run_cs(Yo, go, uo)
results["drop_outliers"] = spec_entry("CS ATT, flagged GER outliers dropped", Yo, go, uo, pto, dro)
# drop ZMB (low confidence) and GHA (capitation grant)
gd = g.copy()
for i, u in enumerate(units):
    if u in ("ZMB", "GHA"):
        gd[i] = -1
ptd, drd = run_cs(Y, gd, units)
results["drop_zmb_gha"] = spec_entry("CS ATT, ZMB and GHA excluded", Y, gd, units, ptd, drd)
# pre-treatment controls (outcome regression)
Xc = covX(units)
ptc, drc = run_cs(Y, g, units, X=Xc)
results["controls"] = spec_entry("CS ATT with outcome regression on log GDP pc and urban share at g-1",
                                 Y, g, units, ptc, drc, controls=["log_gdp_pc_g_minus_1", "urban_share_g_minus_1"],
                                 extra={"base": "universal (g-1)"})
# placebo: dates moved 3 years earlier, post-abolition data dropped
Yp, gp = Y.copy(), g.copy()
for i in range(len(units)):
    if g[i] > 0:
        Yp[i, years >= g[i]] = np.nan
        gp[i] = g[i] - 3
fp = lambda idx: cs_core(Yp[idx], gp[idx], emin=-6, emax=2)[0]
ptp, drp = boot(fp, len(units))
sep = np.nanstd(drp[:, 0], ddof=1)
tp, pvp = pval(ptp[0], sep, len(units) - 1)
out["placebo"] = {"fake_date_minus_3": {"estimate": float(ptp[0]), "se": float(sep), "p_value": pvp,
                                       "df": len(units) - 1, "n_observations": nobs(Yp)}}
# leave-one-country-out (point estimates)
loco = {}
for u in treated_units:
    gg = g.copy()
    gg[units.index(u)] = -1
    loco[u] = float(cs_core(Y, gg)[0][0])
results["leave_one_country_out"] = {"specification": "CS ATT dropping each treated country in turn",
                                    "n_observations": nobs(Y), "n_clusters": n_units,
                                    "coefficients": {"att": {"estimate": float(np.mean(list(loco.values()))), "se": None, "p_value": None},
                                                     "att_min": {"estimate": min(loco.values())},
                                                     "att_max": {"estimate": max(loco.values())}},
                                    "by_dropped_country": loco}

# ── 6. Heterogeneity and secondary outcomes ──────────────────────────────────
# H4: female vs male GER
Yf, gf, uf = build("ger_female")
Ym, gm, um = build("ger_male")
common = [u for u in uf if u in um]
Yf, Ym, gc = Yf[[uf.index(u) for u in common]], Ym[[um.index(u) for u in common]], gf[[uf.index(u) for u in common]]
fg = lambda idx: np.concatenate([cs_core(Yf[idx], gc[idx])[0], cs_core(Ym[idx], gc[idx])[0]])
ptg, drg = boot(fg, len(common))
L = len(es_list) + 1
for nm, sl, Yx in (("gender_female", slice(0, L), Yf), ("gender_male", slice(L, 2 * L), Ym)):
    results[nm] = spec_entry("CS ATT, %s GER" % nm.split("_")[1], Yx, gc, common, ptg[sl], drg[:, sl],
                             hyp="H4" if nm == "gender_female" else None)
results["gender_gap"] = spec_entry("CS ATT difference: female minus male GER", Yf, gc, common,
                                   np.array([ptg[0] - ptg[L]]), (drg[:, 0] - drg[:, L])[:, None], hyp="H4")

# H2: NER and GER on the NER-observed sample
Yn, gn, un = build("ner_primary")
Yg_n = wide("ger_primary").reindex(un).values.astype(float)
Yg_n[~np.isfinite(Yn)] = np.nan
fn = lambda idx: np.concatenate([cs_core(Yn[idx], gn[idx])[0], cs_core(Yg_n[idx], gn[idx])[0]])
ptn2, drn2 = boot(fn, len(un))
results["ner"] = spec_entry("CS ATT, net enrolment rate", Yn, gn, un, ptn2[:L], drn2[:, :L], hyp="H2")
results["ger_on_ner_sample"] = spec_entry("CS ATT, GER on NER-observed country-years", Yg_n, gn, un,
                                          ptn2[L:], drn2[:, L:], hyp="H2")
results["ger_minus_ner"] = spec_entry("CS ATT difference: GER minus NER", Yn, gn, un,
                                      np.array([ptn2[L] - ptn2[0]]), (drn2[:, L] - drn2[:, 0])[:, None], hyp="H2")

# H6 proxy: completion rate (pupil-teacher ratio is not in the data)
Yc, gcm, ucm = build("completion_rate")
ptcr, drcr = run_cs(Yc, gcm, ucm)
results["completion_rate"] = spec_entry("CS ATT, primary completion rate (H6 proxy)", Yc, gcm, ucm, ptcr, drcr, hyp="H6")

# H3: country ATT vs mean pre-abolition GER (descriptive, 8 countries)
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
m3 = sm.OLS(h3.att, sm.add_constant(h3.pre_ger)).fit(cov_type="HC3")  # HC3: small-sample robust
results["h3_initial_level"] = {
    "specification": "Country-level CS ATT regressed on mean GER in the 5 years before abolition (HC3)",
    "hypothesis": "H3", "n_observations": int(len(h3)), "df": int(len(h3) - 2),
    "coefficients": {"pre_ger": coef(m3.params["pre_ger"], m3.bse["pre_ger"], len(h3) - 2)},
    "country_att": {r.iso3: {"att": float(r.att), "pre_ger": float(r.pre_ger)} for r in h3.itertuples()}}


# ── 7. Benchmarks: TWFE + wild cluster bootstrap, Goodman-Bacon ──────────────
def twfe(col):
    d = panel.dropna(subset=[col]).copy()
    d["D"] = ((d.g > 0) & (d.year >= d.g)).astype(float)
    ui = pd.get_dummies(d.iso3, drop_first=False).values.astype(float)
    yi = pd.get_dummies(d.year, drop_first=True).values.astype(float)
    F = np.hstack([ui, yi])
    resid = lambda v: v - F @ np.linalg.lstsq(F, v, rcond=None)[0]
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
    return d, b, se, t, pw, len(ug)


for col, key in (("ger_primary", "twfe_level"), ("log_ger", "twfe_log")):
    d, b, se, t, pw, G = twfe(col)
    c = coef(b, se, G - 1)
    c["wild_bootstrap_p_value"] = pw
    results[key] = {"specification": "Static TWFE (country, year FE), benchmark only; p_value is cluster-robust t, "
                                     "wild_bootstrap_p_value is Webb wild cluster bootstrap-t",
                    "estimator": "twfe", "n_observations": int(len(d)), "n_clusters": G, "cluster_level": "iso3",
                    "fixed_effects": ["iso3", "year"], "df": G - 1, "coefficients": {"att": c}}


def bacon(lo, hi):
    d = panel[(panel.year >= lo) & (panel.year <= hi)]
    cnt = d.groupby("iso3").ger_primary.count()
    d = d[d.iso3.isin(cnt[cnt == hi - lo + 1].index)].copy()
    d["D"] = ((d.g > 0) & (d.year >= d.g)).astype(float)
    d.loc[(d.g > 0) & (d.g <= lo), "D"] = np.nan
    dropunits = d[d.D.isna()].iso3.unique()
    d = d[~d.iso3.isin(dropunits)]
    Wd = d.pivot(index="iso3", columns="year", values="ger_primary")
    gu = d.drop_duplicates("iso3").set_index("iso3").g.loc[Wd.index]
    yrs = Wd.columns.values
    groups = sorted(set(gu[gu > 0])) + [0]
    n = {k: (gu == k).sum() for k in groups}
    Ntot = len(Wd)
    if n.get(0, 0) == 0 or len(groups) < 2:
        return None
    Dbar = {k: ((yrs >= k).mean() if k > 0 else 0.0) for k in groups}
    mean = {k: Wd[gu == k].mean(axis=0).values for k in groups}
    did = lambda k, tp_, tq, ctrl, cp, cq: ((mean[k][tq].mean() - mean[k][tp_].mean())
                                            - (mean[ctrl][cq].mean() - mean[ctrl][cp].mean()))
    comps = []
    for k in groups[:-1]:
        pre, post = yrs < k, yrs >= k
        nku = n[k] / (n[k] + n[0])
        s = ((n[k] + n[0]) / Ntot) ** 2 * nku * (1 - nku) * Dbar[k] * (1 - Dbar[k])
        comps.append(("treated_vs_never", k, 0, did(k, pre, post, 0, pre, post), s))
    tg = groups[:-1]
    for i, k in enumerate(tg):
        for l in tg[i + 1:]:
            nkl = n[k] / (n[k] + n[l])
            sh = ((n[k] + n[l]) / Ntot) ** 2
            win = yrs < l
            pre, post = (yrs < k) & win, (yrs >= k) & win
            vk = (Dbar[k] - Dbar[l]) / (1 - Dbar[l]) * (1 - Dbar[k]) / (1 - Dbar[l])
            comps.append(("early_vs_later_control", k, l, did(k, pre, post, l, pre, post),
                          sh * ((1 - Dbar[l]) ** 2) * nkl * (1 - nkl) * vk))
            pre, post = (yrs >= k) & (yrs < l), yrs >= l
            vl = Dbar[l] / Dbar[k] * (Dbar[k] - Dbar[l]) / Dbar[k]
            comps.append(("later_vs_already_treated_control", k, l, did(l, pre, post, k, pre, post),
                          sh * (Dbar[k] ** 2) * nkl * (1 - nkl) * vl))
    tot = sum(c[4] for c in comps)
    est = sum(c[3] * c[4] for c in comps) / tot
    ui = pd.get_dummies(d.iso3).values.astype(float)
    yi = pd.get_dummies(d.year, drop_first=True).values.astype(float)
    Fm = np.hstack([ui, yi])
    r = lambda v: v - Fm @ np.linalg.lstsq(Fm, v, rcond=None)[0]
    Dt = r(d.D.values)
    direct = float((Dt @ r(d.ger_primary.values)) / (Dt @ Dt))
    agg = {}
    for typ in set(c[0] for c in comps):
        ws = sum(c[4] for c in comps if c[0] == typ)
        agg[typ] = {"weight": float(ws / tot),
                    "weighted_mean_estimate": float(sum(c[3] * c[4] for c in comps if c[0] == typ) / max(ws, 1e-12))}
    return {"window": [lo, hi], "n_units": int(Ntot), "units": list(Wd.index),
            "treated_units": [u for u in Wd.index if gu[u] > 0], "n_comparison_units": int(n[0]),
            "twfe_balanced_direct": direct, "decomposition_weighted_sum": float(est), "by_type": agg,
            "components": [{"type": c[0], "early_cohort": int(c[1]), "late_cohort": int(c[2]),
                            "estimate": float(c[3]), "weight": float(c[4] / tot)} for c in comps]}


gb = None
for lo, hi in ((1985, 2010), (1990, 2010), (1990, 2008)):
    try:
        gb = bacon(lo, hi)
    except Exception as ex:
        gb = {"error": str(ex)}
    if gb and "components" in gb and len(gb["treated_units"]) >= 2:
        break
out["goodman_bacon"] = gb


# ── 8. Heterogeneity-robust alternatives: Sun-Abraham and BJS ────────────────
def long_frame(col, idx=None, units_=None):
    d = panel.dropna(subset=[col])[["iso3", "year", "g", col]].rename(columns={col: "y"})
    if idx is None:
        return d
    grp = {u: x for u, x in d.groupby("iso3")}
    parts = []
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
    inwin = (d.g == 0) | ((d.e >= EMIN) & (d.e <= EMAX))
    Xm, yv = Xm[inwin.values], d.y.values[inwin.values]
    cf = np.linalg.lstsq(Xm, yv, rcond=None)[0][ui.shape[1] + yi.shape[1]:]
    thx = {}
    for e in range(EMIN, EMAX + 1):
        sel = [(cf[k], m[2]) for k, m in enumerate(meta) if m[1] == e]
        thx[e] = np.average([a for a, w in sel], weights=[w for a, w in sel]) if sel else (0.0 if e == -1 else np.nan)
    post = [(cf[k], m[2]) for k, m in enumerate(meta) if m[1] >= 0]
    sa_att = np.average([a for a, w in post], weights=[w for a, w in post])
    # BJS imputation: FE fitted on untreated observations only
    unt = ((d.g == 0) | (d.year < d.g)).values
    Fa = np.hstack([ui, yi])
    bb = np.linalg.lstsq(Fa[unt], d.y.values[unt], rcond=None)[0]
    tr = ((d.g > 0) & (d.e >= 0) & (d.e <= EMAX)).values
    bj_att = (d.y.values[tr] - Fa[tr] @ bb).mean()
    return np.array([sa_att] + [thx[e] for e in range(EMIN, EMAX + 1)] + [bj_att])


pt_s = sa_bjs(long_frame("ger_primary"))
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
results["sun_abraham"] = spec_entry("Sun-Abraham interaction-weighted ATT; unit-bootstrap SE",
                                    Y, g, units, pt_s[:L], dr_s[:, :L], estimator="sun_abraham",
                                    fe=["iso3", "year"])
results["bjs_imputation"] = spec_entry("Borusyak-Jaravel-Spiess imputation ATT; unit-bootstrap SE",
                                       Y, g, units, pt_s[L:], dr_s[:, L:], estimator="borusyak_jaravel_spiess",
                                       fe=["iso3", "year"])
out["sun_abraham_event_study"] = [{"relative_period": e, "estimate": float(pt_s[1 + k]),
                                   "se": float(np.nanstd(dr_s[:, 1 + k], ddof=1))} for k, e in enumerate(es_list)]
out["sensitivity"] = sens
out["sample_flow"] = sample_flow
out["h5_note"] = {"hypothesis": "H5", "status": "not estimable: capitation-grant status by country is not in data.db"}

final = {"main": results.pop("main")}
final.update(results)
final.update(out)


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


# ── 9. Export results ─────────────────────────────────────────────────────────
final = clean(final)
with open(OUTPUT_DIR / "estimation_results.json", "w") as fh:  # all numbers in the paper
    json.dump(final, fh, indent=1)


def row(name, r):
    c = r["coefficients"]["att"]
    return {"specification": name, "att": c.get("estimate"), "se": c.get("se"), "p_value": c.get("p_value"),
            "n_obs": r.get("n_observations"), "n_clusters": r.get("n_clusters")}


t1 = pd.DataFrame([{"item": k, "value": str(v)} for k, v in sample_flow.items()])
desc = panel.ger_primary.describe().rename_axis("item").reset_index()
desc.columns = ["item", "value"]
pd.concat([t1, desc.astype(str)]).to_csv(OUTPUT_DIR / "table1_summary.csv", index=False)  # Table 1

main_keys = ["main", "cs_log_ger", "cs_not_yet_treated", "sun_abraham", "bjs_imputation", "twfe_level", "twfe_log"]
pd.DataFrame([row(k, final[k]) for k in main_keys]).to_csv(OUTPUT_DIR / "table2_main_att.csv", index=False)  # Table 2

rob_keys = ["anticipation_1", "window_m5_p5", "drop_outliers", "drop_zmb_gha", "controls", "gender_female",
            "gender_male", "gender_gap", "ner", "ger_on_ner_sample", "ger_minus_ner", "completion_rate"]
pd.DataFrame([row(k, final[k]) for k in rob_keys]).to_csv(OUTPUT_DIR / "table3_robustness.csv", index=False)  # Table 3

pd.DataFrame(final["event_study"]["periods"]).to_csv(OUTPUT_DIR / "table_event_study.csv", index=False)  # Figure 1 data
pd.Series(loco, name="att_dropping_country").rename_axis("iso3").to_csv(OUTPUT_DIR / "table_leave_one_out.csv")  # robustness text

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

es = pd.DataFrame(final["event_study"]["periods"])
fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(es.relative_period, es.estimate, yerr=1.96 * es.se, fmt="o", capsize=3, color="#1f4e79")
ax.axhline(0, color="grey", lw=.8)
ax.axvline(-1, color="grey", ls="--", lw=.8)
ax.set_xlabel("Years since fee abolition")
ax.set_ylabel("GER, percentage points (reference t = -1)")
ax.set_title("Callaway-Sant'Anna event study (pointwise 95% bands)")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_event_study.png", dpi=200)  # Figure 1
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(event_time_means.t, event_time_means["mean"], marker="o", color="#1f4e79")
ax.axvline(-0.5, color="grey", ls="--", lw=.8)
ax.set_xlabel("Years since fee abolition")
ax.set_ylabel("Mean GER (%)")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_ger_event_time.png", dpi=200)  # Figure 2
plt.close(fig)

print("Main ATT:", final["main"]["coefficients"]["att"])
print("Pre-trend Wald W=%.2f p=%.3f; HonestDiD M=%.2f" % (W, pp, Mval))
