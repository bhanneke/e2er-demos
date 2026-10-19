"""Descriptive analysis: annual M>=5 counts and Gutenberg-Richter b-values by decade.
Reads eq_clean_m45 from data.db; writes estimation_results.json."""
import json
import sqlite3
import numpy as np
import pandas as pd
from scipy import stats

SEED = 20260101
NBOOT = 1000
DM = 0.1
LOG10E = np.log10(np.e)
DECADES = [(1976, 1985), (1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025)]
MW_FAMILY = {"mw", "mwc", "mww", "mwr", "mwb", "mwp"}

con = sqlite3.connect("data.db")
df = pd.read_sql("SELECT year, mag, magType, depth FROM eq_clean_m45", con)
raw_n = sum(con.execute(f"SELECT COUNT(*) FROM usgs_raw_{a}_{b}").fetchone()[0] for a, b in DECADES)
df["mi"] = np.round(df["mag"] * 10).astype(int)  # integer tenths of magnitude
df["decade"] = [f"{a}-{b}" for y in df["year"] for a, b in DECADES if a <= y <= b]
N_ALL = len(df)
rng = np.random.default_rng(SEED)


def b_ml(m, mc, dm=DM):
    m = np.asarray(m)
    mean = m.mean()
    return LOG10E / (mean - (mc - dm / 2))


def b_se_shibolt(m):
    m = np.asarray(m)
    n = len(m)
    b = b_ml(m, m.min())
    return 2.30 * b**2 * np.sqrt(((m - m.mean()) ** 2).sum() / (n * (n - 1)))


def b_stats(mi, mc):
    """b-value, SEs and bootstrap CI for integer-tenths magnitudes mi at completeness mc."""
    m = mi[mi >= round(mc * 10)] / 10.0
    n = len(m)
    if n < 50:
        return None
    b = b_ml(m, mc)
    se_sb = 2.30 * b**2 * np.sqrt(((m - m.mean()) ** 2).sum() / (n * (n - 1)))
    idx = rng.integers(0, n, size=(NBOOT, n))
    means = m[idx].mean(axis=1)
    bb = LOG10E / (means - (mc - DM / 2))
    return {"mc": round(float(mc), 1), "n": int(n), "b": float(b), "se_shi_bolt": float(se_sb),
            "se_aki": float(b / np.sqrt(n)), "boot_lo": float(np.percentile(bb, 2.5)),
            "boot_hi": float(np.percentile(bb, 97.5))}


def mc_estimates(mi):
    """Maximum curvature (+0.2) and goodness-of-fit (90/95) completeness from M>=4.5 events."""
    vals, counts = np.unique(mi, return_counts=True)
    mc_mx = vals[np.argmax(counts)] / 10.0
    out = {"maxc": float(mc_mx), "maxc_plus_0.2": round(float(mc_mx) + 0.2, 1)}
    res = {}
    for mc10 in range(45, 66):
        mc = mc10 / 10
        sel = mi[mi >= mc10] / 10.0
        if len(sel) < 50:
            break
        b = b_ml(sel, mc)
        grid = np.arange(mc10, sel.max() * 10 + 1) / 10.0
        obs = np.array([(sel >= g - 1e-9).sum() for g in grid], dtype=float)
        a = np.log10(len(sel)) + b * mc
        syn = 10 ** (a - b * grid)
        res[mc] = 100 - 100 * np.abs(obs - syn).sum() / obs.sum()
    for lvl in (90, 95):
        ok = [mc for mc, r in res.items() if r >= lvl]
        out[f"gft{lvl}"] = min(ok) if ok else None
    out["gft_r_at_5.0"] = float(res.get(5.0, np.nan))
    return out


def utsu(b1, n1, b2, n2):
    d = (-2 * (n1 + n2) * np.log(n1 + n2) + 2 * n1 * np.log(n1 + n2 * b1 / b2)
         + 2 * n2 * np.log(n2 + n1 * b2 / b1) - 2)
    lr = d + 2  # likelihood-ratio statistic, chi2(1) under equal b
    return float(d), float(lr), float(stats.chi2.sf(lr, 1))


def by_decade(sub, mc_map):
    out = {}
    for dec, g in sub.groupby("decade"):
        out[dec] = b_stats(g["mi"].values, mc_map[dec])
    return out


def pair_tests(bd):
    res = []
    keys = list(bd.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            x, y = bd[keys[i]], bd[keys[j]]
            if x is None or y is None:
                continue
            d, lr, p = utsu(x["b"], x["n"], y["b"], y["n"])
            overlap = not (x["boot_hi"] < y["boot_lo"] or y["boot_hi"] < x["boot_lo"])
            res.append({"decade_a": keys[i], "decade_b": keys[j], "delta_aic_utsu": d, "lr_stat": lr,
                        "p_value": p, "b_a": x["b"], "b_b": y["b"],
                        "bootstrap_ci_overlap": bool(overlap)})
    return res


# ---------- Mc per decade ----------
mc_dec = {}
for dec, g in df.groupby("decade"):
    mc_dec[dec] = mc_estimates(g["mi"].values)
mc_maxc = {d: v["maxc_plus_0.2"] for d, v in mc_dec.items()}
mc_gft95 = {d: (v["gft95"] if v["gft95"] is not None else mc_maxc[d]) for d, v in mc_dec.items()}
mc_gft90 = {d: (v["gft90"] if v["gft90"] is not None else mc_maxc[d]) for d, v in mc_dec.items()}
MC_COMMON = round(max(mc_maxc.values()), 1)
mc_common_map = {d: MC_COMMON for d in mc_maxc}
mc_fixed = {d: 5.0 for d in mc_maxc}

# ---------- (a) annual counts ----------
years = np.arange(1976, 2026)
ann = df.groupby("year")


def annual(th):
    c = df[df["mag"] >= th - 1e-9].groupby("year").size().reindex(years, fill_value=0)
    return c


counts = {"m5": annual(5.0), "m6": annual(6.0), "m7": annual(7.0), "common": annual(MC_COMMON)}


def count_summary(c):
    d = {"overall": {"n_years": int(len(c)), "mean": float(c.mean()), "sd": float(c.std(ddof=1)),
                     "dispersion_index": float(c.var(ddof=1) / c.mean()), "total": int(c.sum())},
         "decades": {}}
    for a, b in DECADES:
        s = c.loc[a:b]
        d["decades"][f"{a}-{b}"] = {"n_years": int(len(s)), "mean": float(s.mean()), "sd": float(s.std(ddof=1)),
                                    "min": int(s.min()), "max": int(s.max()),
                                    "dispersion_index": float(s.var(ddof=1) / s.mean())}
    return d


def trend(c):
    import statsmodels.api as sm
    X = sm.add_constant((c.index.values - 1976).astype(float))
    y = c.values.astype(float)
    out = {}
    try:
        pm = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC0")
        ci = pm.conf_int()[1]
        out["poisson"] = {"slope_pct_per_year": float(100 * (np.exp(pm.params[1]) - 1)),
                          "ci_lo": float(100 * (np.exp(ci[0]) - 1)), "ci_hi": float(100 * (np.exp(ci[1]) - 1)),
                          "se_robust": "HC0"}
    except Exception as e:
        out["poisson"] = {"error": str(e)}
    try:
        # NB2 with alpha estimated by moments from Poisson fit
        mu = sm.GLM(y, X, family=sm.families.Poisson()).fit().mu
        alpha = max(float((((y - mu) ** 2 - mu) / mu**2).sum() / (len(y) - 2)), 1e-6)
        nb = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=alpha)).fit()
        ci = nb.conf_int()[1]
        out["negbin"] = {"slope_pct_per_year": float(100 * (np.exp(nb.params[1]) - 1)),
                         "ci_lo": float(100 * (np.exp(ci[0]) - 1)), "ci_hi": float(100 * (np.exp(ci[1]) - 1)),
                         "alpha_moment": alpha}
    except Exception as e:
        out["negbin"] = {"error": str(e)}
    rho, p = stats.spearmanr(c.index.values, c.values)
    out["spearman_year"] = {"rho": float(rho), "p_value": float(p), "n": int(len(c))}
    return out


counts_res = {k: {"summary": count_summary(c), "trend": trend(c),
                  "threshold": {"m5": 5.0, "m6": 6.0, "m7": 7.0, "common": MC_COMMON}[k]}
              for k, c in counts.items()}

# magnitude-type mix of M>=5 by decade
m5 = df[df["mag"] >= 5.0 - 1e-9].copy()


def fam(t):
    if t in MW_FAMILY:
        return "Mw family"
    return t if t in ("mb", "ms") else "other"


m5["fam"] = m5["magType"].map(fam)
mix = {}
for dec, g in m5.groupby("decade"):
    vc = g["fam"].value_counts()
    mix[dec] = {"n": int(len(g)), **{k: {"count": int(v), "share": float(v / len(g))} for k, v in vc.items()}}

# ---------- (b)-(d) b-values ----------
b_maxc = by_decade(df, mc_maxc)
b_gft95 = by_decade(df, mc_gft95)
b_gft90 = by_decade(df, mc_gft90)
b_common = by_decade(df, mc_common_map)
b_fixed = by_decade(df, mc_fixed)

# Mc sensitivity: shift decade-specific maxc+0.2 by -0.3..+0.3
sens = {}
for sft in (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3):
    mm = {d: round(v + sft, 1) for d, v in mc_maxc.items()}
    sens[f"{sft:+.1f}"] = by_decade(df, mm)

# Fixed Mc sensitivity on common threshold grid
tests = {"maxc_plus_0.2": pair_tests(b_maxc), "gft95": pair_tests(b_gft95),
         "common_threshold": pair_tests(b_common), "fixed_5.0": pair_tests(b_fixed)}

# checks
mw_df = df[df["magType"].isin(MW_FAMILY)]
mc_mw = {d: mc_estimates(g["mi"].values)["maxc_plus_0.2"] for d, g in mw_df.groupby("decade")}
sh_df = df[df["depth"] <= 70]
mc_sh = {d: mc_estimates(g["mi"].values)["maxc_plus_0.2"] for d, g in sh_df.groupby("decade")}
checks = {
    "mw_family_only": {"mc_maxc_plus_0.2": mc_mw, "b_own_mc": by_decade(mw_df, mc_mw), "n_events": int(len(mw_df)),
                       "n_events_m5plus": int((mw_df["mag"] >= 5.0 - 1e-9).sum())},
    "shallow_depth_le_70km": {"mc_maxc_plus_0.2": mc_sh, "b_common_threshold": by_decade(sh_df, {d: MC_COMMON for d in mc_sh}),
                              "b_own_mc": by_decade(sh_df, mc_sh), "n_events": int(len(sh_df)),
                              "n_events_m5plus": int((sh_df["mag"] >= 5.0 - 1e-9).sum())},
}
checks["mw_family_only"]["note"] = ("No b at the common threshold: moment magnitudes are assigned mainly to larger events, "
    "so the Mw-only sample is not complete at the common threshold; b is reported at the sample's own Mc only.")
checks["shallow_depth_le_70km"]["pair_tests_common"] = pair_tests(checks["shallow_depth_le_70km"]["b_common_threshold"])

# Mc at the load floor (M>=4.5): estimate is censored there
FLOOR = 4.5
at_floor = {}
for rule in ("maxc", "gft90", "gft95"):
    at_floor[rule] = [d for d, v in mc_dec.items() if v[rule] is not None and abs(v[rule] - FLOOR) < 1e-9]
mc_censored = {"load_floor_magnitude": FLOOR,
               "decades_at_floor_by_rule": at_floor,
               "note": ("Mc = 4.5 equals the load floor (events with M>=4.5 only): the estimate is censored at the floor "
                        "and the true Mc may be lower. Decades listed are those where the raw rule returns 4.5; "
                        "for these decades b at Mc=4.5 uses all loaded events.")}

# ---------- schema blocks ----------
def qstats(x, unit):
    x = np.asarray(x, dtype=float)
    q = np.percentile(x, [5, 25, 50, 75, 95])
    return {"n": int(len(x)), "mean": float(x.mean()), "sd": float(x.std(ddof=1)), "min": float(x.min()),
            "p5": float(q[0]), "p25": float(q[1]), "median": float(q[2]), "p75": float(q[3]),
            "p95": float(q[4]), "max": float(x.max()), "unit": unit}


statistics = {
    "magnitude_all": qstats(df["mag"], "magnitude (preferred, ComCat)"),
    "depth_km": qstats(df["depth"], "km"),
    "annual_count_m5": qstats(counts["m5"], "events per year"),
    "annual_count_m6": qstats(counts["m6"], "events per year"),
    "annual_count_m7": qstats(counts["m7"], "events per year"),
    f"annual_count_common_m{MC_COMMON}": qstats(counts["common"], "events per year"),
    "share_m5_mw_family": {"n": int(len(m5)), "count": int(m5["fam"].eq("Mw family").sum()),
                           "share": float(m5["fam"].eq("Mw family").mean())},
    "share_shallow_le_70km": {"n": N_ALL, "count": int(len(sh_df)), "share": float(len(sh_df) / N_ALL)},
}

c5 = counts["m5"].values
lo, hi = int(c5.min()), int(c5.max())
edges = np.linspace(np.floor(lo / 100) * 100, np.ceil((hi + 1) / 100) * 100, int((np.ceil((hi + 1) / 100) * 100 - np.floor(lo / 100) * 100) / 100) + 1)
h, e = np.histogram(c5, bins=edges)
dist_counts = {"variable": "annual_count_m5", "n": int(len(c5)),
               "bins": [{"lower": float(e[i]), "upper": float(e[i + 1]), "count": int(h[i])} for i in range(len(h))]}
mag_edges = np.arange(4.5, 9.51, 0.5)
hm, em = np.histogram(df["mag"], bins=np.append(mag_edges[:-1], 9.5))
dist_mag = {"variable": "magnitude_all", "n": N_ALL,
            "bins": [{"lower": float(em[i]), "upper": float(em[i + 1]), "count": int(hm[i])} for i in range(len(hm))]}
vc = m5["magType"].value_counts()
dist_type = {"variable": "magType (M>=5)", "n": int(len(m5)),
             "categories": [{"category": str(k), "count": int(v)} for k, v in vc.items()]}
dist_dec = {"variable": "decade (all M>=4.5)", "n": N_ALL,
            "categories": [{"category": k, "count": int(v)} for k, v in df["decade"].value_counts().sort_index().items()]}

res = {
    "result_kind": "descriptive",
    "sample": {"n_observations": N_ALL, "unit": "earthquake (ComCat preferred magnitude, M>=4.5)",
               "source": "data.db table eq_clean_m45 (USGS ComCat, doi 10.5066/F7MS3QZH)",
               "raw_rows_loaded": int(raw_n), "rows_dropped_in_cleaning": int(raw_n - N_ALL),
               "years": [1976, 2025], "aftershocks_kept": True},
    "statistics": statistics,
    "distributions": {"annual_count_m5": dist_counts, "magnitude": dist_mag, "magtype_m5": dist_type,
                      "events_by_decade": dist_dec},
    "associations": {
        "annual_m5_vs_year": {"x": "year", "y": "annual_count_m5", "method": "spearman",
                              "estimate": counts_res["m5"]["trend"]["spearman_year"]["rho"], "n": 50,
                              "p_value": counts_res["m5"]["trend"]["spearman_year"]["p_value"]},
        f"annual_common_vs_year": {"x": "year", "y": f"annual_count_m{MC_COMMON}", "method": "spearman",
                                    "estimate": counts_res["common"]["trend"]["spearman_year"]["rho"], "n": 50,
                                    "p_value": counts_res["common"]["trend"]["spearman_year"]["p_value"]}},
    "figures": ["fig_annual_counts_m5.pdf", "fig_magtype_mix.pdf"],
    "completeness": {"per_decade": mc_dec, "mc_censored_at_load_floor": mc_censored, "common_threshold": MC_COMMON,
                     "rule_note": "maxc_plus_0.2 = mode of 0.1-binned distribution + 0.2; gft = smallest Mc with fit >=90/95%; null if not reached",
                     "quantile_definition": "numpy percentile, linear interpolation (Hyndman-Fan type 7)"},
    "counts": counts_res,
    "magtype_mix_m5_by_decade": mix,
    "magtype_mix_m5_by_decade_list": [{"decade": k, "mw_family_share": v["Mw family"]["share"]}
                                      for k, v in mix.items()],
    "b_values": {"method": "Aki-Utsu ML, bin correction dM=0.1; SE Shi & Bolt (1982); bootstrap 95pct CI (1000 resamples, seed " + str(SEED) + ")",
                 "decade_mc_maxc_plus_0.2": b_maxc, "decade_mc_gft95": b_gft95, "decade_mc_gft90": b_gft90,
                 "decade_common_threshold": b_common, "decade_fixed_mc_5.0": b_fixed},
    "b_equality_tests": {"method": "Utsu two-sample likelihood-ratio test (delta AIC = LR - 2; p from chi2(1) on LR)",
                         **tests},
    "mc_sensitivity_shift": sens,
    "checks": checks,
}
with open("estimation_results.json", "w") as f:
    json.dump(res, f, indent=1)
print("MC", {d: (v["maxc"], v["maxc_plus_0.2"], v["gft90"], v["gft95"]) for d, v in mc_dec.items()}, "common", MC_COMMON)
for k in ("m5", "common"):
    print(k, {d: round(v["mean"], 1) for d, v in counts_res[k]["summary"]["decades"].items()}, counts_res[k]["trend"])
for name, bd in (("maxc", b_maxc), ("fixed5", b_fixed), ("common", b_common)):
    print(name, {d: (round(v["b"], 3), v["n"]) for d, v in bd.items() if v})
