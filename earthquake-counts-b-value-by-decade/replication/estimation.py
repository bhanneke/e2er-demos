"""
Replication script for: How Has the Yearly Number of Magnitude 5 and Larger Earthquakes
Changed, 1976-2025? Counts and the Stability of the Gutenberg-Richter b-Value Across Decades
Paper ID: b68c8252-7002-4831-8bce-e6c639b9faf7

Requirements: pandas, numpy, scipy, statsmodels, matplotlib
Usage:   python replication/estimation.py [path/to/data.db]
Output:  replication/output/ (tables as CSV, figures as PNG, results as JSON)

DATA
  Table `eq_clean_m45` of the study's data.db: USGS ComCat (doi 10.5066/F7MS3QZH), worldwide,
  1976-01-01 to 2025-12-31, magnitude >= 4.5, ComCat preferred magnitude, type == 'earthquake',
  aftershocks kept (no declustering). Built from the five raw tables usgs_raw_YYYY_YYYY by
  clean_catalogue.py (see replication/data_queries.sql and replication/audit_log.csv for the
  load commands and the audit trail). No data are shipped with this package.
  The database path is the first command-line argument, else $EQ_DB, else ../data.db
  relative to this file.

ENVIRONMENT (pin in requirements.txt as used for the paper's run; tested API: numpy>=1.24,
  pandas>=2.0, scipy>=1.10, statsmodels>=0.14, matplotlib>=3.7)

STEPS
  1. Load eq_clean_m45.  2. Counts (published magnitude, mag >= threshold).
  3. Mc per decade (max curvature + 0.2; goodness of fit 90/95), on magnitudes binned to 0.1.
  4. Aki-Utsu b with bin correction dM = 0.1, Shi & Bolt SE, bootstrap CI.
  5. Utsu pairwise tests.  6. Mw-family-only and shallow checks.  7. Export.

STANDARD ERRORS: descriptive study, no regression for inference. Trend slopes are labelled
  associations with calendar time (Poisson with HC0 robust SEs; negative binomial with moment alpha).
  b-value SEs: Shi & Bolt (1982); Aki's b/sqrt(N) is reported only as a labelled alternative.

OUTPUT MAP (paper table/figure -> file in replication/output/)
  Table: summary of annual counts and decade means -> table_annual_counts.csv, table_decade_count_summary.csv
  Table: magnitude-type mix of M>=5 by decade       -> table_magtype_mix.csv
  Table: Mc by decade                               -> table_mc_by_decade.csv
  Table: b-values by decade (all Mc rules)          -> table_b_values.csv
  Table: Utsu pairwise tests                        -> table_utsu_pairs.csv
  Table: trend associations                         -> table_count_trends.csv
  Table: checks (Mw-only, shallow)                  -> table_checks_b_values.csv
  Table: Mc sensitivity                             -> table_mc_sensitivity.csv
  Figures: fig_annual_counts_m5.png, fig_annual_counts_m7.png, fig_magtype_mix.png
  All numbers: estimation_results.json
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)

HERE = Path(__file__).parent
OUTPUT_DIR = HERE / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 20260101  # bootstrap seed given in econometric_spec.md
NBOOT = 1000
DM = 0.1
LOG10E = np.log10(np.e)
FLOOR = 4.5  # load floor of the catalogue
DECADES = [(1976, 1985), (1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025)]
MW_FAMILY = {"mw", "mwc", "mww", "mwr", "mwb", "mwp"}
EPS = 1e-9

# ── 1. Load data ──────────────────────────────────────────────────────────────
db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(os.environ.get("EQ_DB", HERE.parent / "data.db"))
con = sqlite3.connect(str(db_path))
df = pd.read_sql("SELECT year, mag, magType, depth FROM eq_clean_m45", con)
raw_n = sum(con.execute(f"SELECT COUNT(*) FROM usgs_raw_{a}_{b}").fetchone()[0] for a, b in DECADES)
con.close()

# ── 2. Variable construction ──────────────────────────────────────────────────
df["mi"] = np.round(df["mag"] * 10).astype(int)  # integer tenths: used for Mc and b only
df["decade"] = [next(f"{a}-{b}" for a, b in DECADES if a <= y <= b) for y in df["year"]]
N_ALL = len(df)
rng = np.random.default_rng(SEED)
years = np.arange(1976, 2026)


def b_ml(m, mc, dm=DM):
    """Aki-Utsu ML b with bin correction: log10(e) / (mean(M) - (Mc - dM/2))."""
    return LOG10E / (np.mean(m) - (mc - dm / 2))


def b_stats(mi, mc):
    """b, Shi & Bolt SE, Aki SE, bootstrap 95% CI for integer-tenth magnitudes at completeness mc."""
    m = mi[mi >= round(mc * 10)] / 10.0
    n = len(m)
    if n < 50:
        return None
    b = b_ml(m, mc)
    se_sb = 2.30 * b**2 * np.sqrt(((m - m.mean()) ** 2).sum() / (n * (n - 1)))
    idx = rng.integers(0, n, size=(NBOOT, n))
    bb = LOG10E / (m[idx].mean(axis=1) - (mc - DM / 2))
    return {"mc": round(float(mc), 1), "n": int(n), "b": float(b), "se_shi_bolt": float(se_sb),
            "se_aki_alt": float(b / np.sqrt(n)), "boot_lo": float(np.percentile(bb, 2.5)),
            "boot_hi": float(np.percentile(bb, 97.5))}


def mc_estimates(mi):
    """Max curvature (+0.2) and goodness-of-fit (90/95%) Mc from events at/above the load floor."""
    vals, cnt = np.unique(mi, return_counts=True)
    mx = vals[np.argmax(cnt)] / 10.0
    out = {"maxc": float(mx), "maxc_plus_0.2": round(float(mx) + 0.2, 1)}
    res = {}
    for mc10 in range(45, 66):
        mc = mc10 / 10
        sel = mi[mi >= mc10] / 10.0
        if len(sel) < 50:
            break
        b = b_ml(sel, mc)
        grid = np.arange(mc10, sel.max() * 10 + 1) / 10.0
        obs = np.array([(sel >= g - EPS).sum() for g in grid], dtype=float)
        syn = 10 ** (np.log10(len(sel)) + b * mc - b * grid)
        res[mc] = 100 - 100 * np.abs(obs - syn).sum() / obs.sum()
    for lvl in (90, 95):
        ok = [mc for mc, r in res.items() if r >= lvl]
        out[f"gft{lvl}"] = min(ok) if ok else None
    return out


def utsu(b1, n1, b2, n2):
    """Utsu (1965) two-sample test: delta-AIC form; LR = d + 2 ~ chi2(1) under equal b."""
    d = (-2 * (n1 + n2) * np.log(n1 + n2) + 2 * n1 * np.log(n1 + n2 * b1 / b2)
         + 2 * n2 * np.log(n2 + n1 * b2 / b1) - 2)
    lr = d + 2
    return float(d), float(lr), float(stats.chi2.sf(lr, 1))


def by_decade(sub, mc_map):
    return {dec: b_stats(g["mi"].values, mc_map[dec]) for dec, g in sub.groupby("decade")}


def pair_tests(bd):
    out, keys = [], list(bd.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            x, y = bd[keys[i]], bd[keys[j]]
            if x is None or y is None:
                continue
            d, lr, p = utsu(x["b"], x["n"], y["b"], y["n"])
            overlap = not (x["boot_hi"] < y["boot_lo"] or y["boot_hi"] < x["boot_lo"])
            out.append({"decade_a": keys[i], "decade_b": keys[j], "delta_aic_utsu": d, "lr_stat": lr,
                        "p_value": p, "b_a": x["b"], "b_b": y["b"], "bootstrap_ci_overlap": bool(overlap)})
    return out


# ── 3. Completeness per decade ────────────────────────────────────────────────
mc_dec = {dec: mc_estimates(g["mi"].values) for dec, g in df.groupby("decade")}
mc_maxc = {d: v["maxc_plus_0.2"] for d, v in mc_dec.items()}
mc_gft95 = {d: (v["gft95"] if v["gft95"] is not None else mc_maxc[d]) for d, v in mc_dec.items()}
mc_gft90 = {d: (v["gft90"] if v["gft90"] is not None else mc_maxc[d]) for d, v in mc_dec.items()}
MC_COMMON = round(max(mc_maxc.values()), 1)  # common threshold = largest decade Mc
mc_common_map = {d: MC_COMMON for d in mc_maxc}
mc_fixed = {d: 5.0 for d in mc_maxc}

# Mc equal to the load floor is censored there (true Mc may be lower)
at_floor = {rule: [d for d, v in mc_dec.items() if v[rule] is not None and abs(v[rule] - FLOOR) < EPS]
            for rule in ("maxc", "gft90", "gft95")}
mc_censored = {"load_floor_magnitude": FLOOR, "decades_at_floor_by_rule": at_floor,
               "note": "Mc = 4.5 equals the load floor (M>=4.5): the estimate is censored there and the true Mc may be lower."}

# ── 4. Yearly counts (published magnitude, mag >= threshold) ──────────────────
def annual(th):
    return df[df["mag"] >= th - EPS].groupby("year").size().reindex(years, fill_value=0)


counts = {"m5": annual(5.0), "m6": annual(6.0), "m7": annual(7.0), "common": annual(MC_COMMON)}
thresholds = {"m5": 5.0, "m6": 6.0, "m7": 7.0, "common": MC_COMMON}


def count_summary(c):
    d = {"overall": {"mean": float(c.mean()), "sd": float(c.std(ddof=1)),
                     "dispersion_index": float(c.var(ddof=1) / c.mean()), "total": int(c.sum())}, "decades": {}}
    for a, b in DECADES:
        s = c.loc[a:b]
        d["decades"][f"{a}-{b}"] = {"mean": float(s.mean()), "sd": float(s.std(ddof=1)), "min": int(s.min()),
                                    "max": int(s.max()), "dispersion_index": float(s.var(ddof=1) / s.mean())}
    return d


def trend(c):
    """Log-linear slope on year (percent/year): an association with calendar time, not an effect."""
    X = sm.add_constant((c.index.values - 1976).astype(float))
    y = c.values.astype(float)
    out = {}
    pm = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC0")  # robust SEs (HC0)
    ci = pm.conf_int()[1]
    out["poisson"] = {"slope_pct_per_year": float(100 * (np.exp(pm.params[1]) - 1)),
                      "ci_lo": float(100 * (np.exp(ci[0]) - 1)), "ci_hi": float(100 * (np.exp(ci[1]) - 1))}
    mu = sm.GLM(y, X, family=sm.families.Poisson()).fit().mu
    alpha = max(float((((y - mu) ** 2 - mu) / mu**2).sum() / (len(y) - 2)), 1e-6)
    nb = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=alpha)).fit()
    ci = nb.conf_int()[1]
    out["negbin"] = {"slope_pct_per_year": float(100 * (np.exp(nb.params[1]) - 1)),
                     "ci_lo": float(100 * (np.exp(ci[0]) - 1)), "ci_hi": float(100 * (np.exp(ci[1]) - 1)),
                     "alpha_moment": alpha}
    rho, p = stats.spearmanr(c.index.values, c.values)
    out["spearman_year"] = {"rho": float(rho), "p_value": float(p), "n": int(len(c))}
    return out


counts_res = {k: {"threshold": thresholds[k], "summary": count_summary(c), "trend": trend(c)}
              for k, c in counts.items()}

# Magnitude-type mix of M>=5 events by decade
m5 = df[df["mag"] >= 5.0 - EPS].copy()
m5["fam"] = m5["magType"].map(lambda t: "Mw family" if t in MW_FAMILY else (t if t in ("mb", "ms") else "other"))
mix = {}
for dec, g in m5.groupby("decade"):
    vc = g["fam"].value_counts()
    mix[dec] = {"n": int(len(g)), **{k: {"count": int(v), "share": float(v / len(g))} for k, v in vc.items()}}

# ── 5. b-values per decade, equality tests ────────────────────────────────────
b_maxc = by_decade(df, mc_maxc)
b_gft95 = by_decade(df, mc_gft95)
b_gft90 = by_decade(df, mc_gft90)
b_common = by_decade(df, mc_common_map)
b_fixed = by_decade(df, mc_fixed)
sens = {f"{s:+.1f}": by_decade(df, {d: round(v + s, 1) for d, v in mc_maxc.items()})
        for s in (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3)}  # Mc sensitivity around maxc+0.2
tests = {"maxc_plus_0.2": pair_tests(b_maxc), "gft95": pair_tests(b_gft95),
         "common_threshold": pair_tests(b_common), "fixed_5.0": pair_tests(b_fixed)}

# ── 6. Checks: Mw-family-only and shallow (depth <= 70 km) samples ────────────
mw_df = df[df["magType"].isin(MW_FAMILY)]
mc_mw = {d: mc_estimates(g["mi"].values)["maxc_plus_0.2"] for d, g in mw_df.groupby("decade")}
sh_df = df[df["depth"] <= 70]
mc_sh = {d: mc_estimates(g["mi"].values)["maxc_plus_0.2"] for d, g in sh_df.groupby("decade")}
b_sh_common = by_decade(sh_df, {d: MC_COMMON for d in mc_sh})
checks = {
    # Mw-only: b at the sample's own Mc only (no common-threshold b: Mw is assigned mostly to larger events)
    "mw_family_only": {"mc_maxc_plus_0.2": mc_mw, "b_own_mc": by_decade(mw_df, mc_mw),
                       "n_events": int(len(mw_df))},
    "shallow_depth_le_70km": {"mc_maxc_plus_0.2": mc_sh, "b_own_mc": by_decade(sh_df, mc_sh),
                              "b_common_threshold": b_sh_common, "pair_tests_common": pair_tests(b_sh_common),
                              "n_events": int(len(sh_df))},
}

# ── 7. Export ─────────────────────────────────────────────────────────────────
# Annual counts by threshold -> annual-counts table
pd.DataFrame({f"n_{k}": c for k, c in counts.items()}).rename_axis("year").to_csv(
    OUTPUT_DIR / "table_annual_counts.csv")
rows = [{"series": k, "threshold": thresholds[k], "period": "overall", **v["summary"]["overall"]}
        for k, v in counts_res.items()]
rows += [{"series": k, "threshold": thresholds[k], "period": dec, **s}
         for k, v in counts_res.items() for dec, s in v["summary"]["decades"].items()]
pd.DataFrame(rows).to_csv(OUTPUT_DIR / "table_decade_count_summary.csv", index=False)  # decade means/SDs/dispersion
pd.DataFrame([{"series": k, "threshold": thresholds[k], "model": m, **v["trend"][m]}
              for k, v in counts_res.items() for m in ("poisson", "negbin", "spearman_year")]
             ).to_csv(OUTPUT_DIR / "table_count_trends.csv", index=False)  # trend associations
pd.DataFrame([{"decade": d, "n": v["n"], **{k: x["share"] for k, x in v.items() if k != "n"}}
              for d, v in mix.items()]).to_csv(OUTPUT_DIR / "table_magtype_mix.csv", index=False)  # type mix
pd.DataFrame([{"decade": d, **v} for d, v in mc_dec.items()]).to_csv(
    OUTPUT_DIR / "table_mc_by_decade.csv", index=False)  # Mc by rule

def flat(block, rule, extra=None):
    return [{"rule": rule, "decade": d, **(extra or {}), **v} for d, v in block.items() if v]


pd.DataFrame(flat(b_maxc, "maxc_plus_0.2") + flat(b_gft95, "gft95") + flat(b_gft90, "gft90")
             + flat(b_common, f"common_{MC_COMMON}") + flat(b_fixed, "fixed_5.0")
             ).to_csv(OUTPUT_DIR / "table_b_values.csv", index=False)  # b by decade, all Mc rules
pd.DataFrame([{"rule": r, **t} for r, ts in tests.items() for t in ts]).to_csv(
    OUTPUT_DIR / "table_utsu_pairs.csv", index=False)  # Utsu pairwise tests
pd.DataFrame(flat(checks["mw_family_only"]["b_own_mc"], "mw_only_own_mc")
             + flat(checks["shallow_depth_le_70km"]["b_own_mc"], "shallow_own_mc")
             + flat(b_sh_common, f"shallow_common_{MC_COMMON}")
             ).to_csv(OUTPUT_DIR / "table_checks_b_values.csv", index=False)  # Mw-only and shallow checks
pd.DataFrame([{"shift": s, "decade": d, **v} for s, bd in sens.items() for d, v in bd.items() if v]).to_csv(
    OUTPUT_DIR / "table_mc_sensitivity.csv", index=False)  # Mc sensitivity

# Figures
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(years, counts["m5"].values, marker="o", ms=3, color="k")
for a, b in DECADES:
    ax.hlines(counts["m5"].loc[a:b].mean(), a, b, color="tab:red", lw=2)
ax.set_xlabel("Year"); ax.set_ylabel("Events with M >= 5.0"); ax.set_title("Yearly M>=5 events (red: decade mean)")
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig_annual_counts_m5.png", dpi=200); plt.close(fig)  # count figure

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(years, counts["m7"].values, marker="o", ms=3, color="k")
ax.set_xlabel("Year"); ax.set_ylabel("Events with M >= 7.0")
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig_annual_counts_m7.png", dpi=200); plt.close(fig)  # M7 figure

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(list(mix.keys()), [100 * v["Mw family"]["share"] if "Mw family" in v else 0 for v in mix.values()],
       color="0.4")
ax.set_ylabel("Mw-family share of M>=5 events (%)"); ax.set_xlabel("Decade")
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig_magtype_mix.png", dpi=200); plt.close(fig)  # type-mix figure

results = {
    "result_kind": "descriptive",
    "sample": {"n_observations": N_ALL, "raw_rows_loaded": int(raw_n), "aftershocks_kept": True,
               "source": "eq_clean_m45 (USGS ComCat, doi 10.5066/F7MS3QZH)"},
    "completeness": {"per_decade": mc_dec, "mc_censored_at_load_floor": mc_censored, "common_threshold": MC_COMMON},
    "counts": counts_res,
    "magtype_mix_m5_by_decade": mix,
    "magtype_mix_m5_by_decade_list": [{"decade": k, "mw_family_share": v.get("Mw family", {}).get("share", 0.0)}
                                      for k, v in mix.items()],
    "b_values": {"decade_mc_maxc_plus_0.2": b_maxc, "decade_mc_gft95": b_gft95, "decade_mc_gft90": b_gft90,
                 "decade_common_threshold": b_common, "decade_fixed_mc_5.0": b_fixed},
    "b_equality_tests": tests,
    "mc_sensitivity_shift": sens,
    "checks": checks,
}
with open(OUTPUT_DIR / "estimation_results_replication.json", "w") as f:  # all numbers, full precision
    json.dump(results, f, indent=1)

print("Mc (maxc, maxc+0.2, gft90, gft95):",
      {d: (v["maxc"], v["maxc_plus_0.2"], v["gft90"], v["gft95"]) for d, v in mc_dec.items()}, "common", MC_COMMON)
print("M>=5 decade means:", {d: round(v["mean"], 1) for d, v in counts_res["m5"]["summary"]["decades"].items()})
print("b (maxc+0.2):", {d: (round(v["b"], 3), v["n"]) for d, v in b_maxc.items() if v})
