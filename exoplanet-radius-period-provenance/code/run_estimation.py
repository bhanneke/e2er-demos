import json, sqlite3
import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261013
rng = np.random.default_rng(SEED)
con = sqlite3.connect("data.db")
raw = pd.read_sql("SELECT * FROM planets_classified", con)
N_RAW = len(raw)
n_norad = int(raw.pl_rade.isna().sum())
n_noper = int(raw.pl_orbper.isna().sum())
df = raw[raw.in_rp_sample == 1].copy()
assert df.pl_rade.notna().all() and df.pl_orbper.notna().all() and (df.pl_orbper > 0).all()
df["lr"] = np.log10(df.pl_rade)
df["lp"] = np.log10(df.pl_orbper)
GROUPS = ["calculated", "measured_transiting", "measured_non_transiting"]
sub = {"all": df}
for g in GROUPS:
    sub[g] = df[df.radius_group == g]
N = len(df)
assert sum(len(sub[g]) for g in GROUPS) == N

def desc(x, unit):
    x = np.asarray(x, float)
    q = lambda p: float(np.quantile(x, p))
    return {"n": int(len(x)), "mean": float(x.mean()), "sd": float(x.std(ddof=1)) if len(x) > 1 else 0.0,
            "min": float(x.min()), "p5": q(.05), "p10": q(.10), "p25": q(.25), "median": q(.5),
            "p75": q(.75), "p90": q(.90), "p95": q(.95), "max": float(x.max()), "unit": unit}

statistics, groups = {}, {}
for k, d in sub.items():
    statistics[f"radius_{k}"] = desc(d.pl_rade, "Earth radii")
    statistics[f"period_{k}"] = desc(d.pl_orbper, "days")
    statistics[f"log10_radius_{k}"] = desc(d.lr, "log10(Earth radii)")
    statistics[f"log10_period_{k}"] = desc(d.lp, "log10(days)")
    statistics[f"geomean_radius_{k}"] = {"n": len(d), "mean": float(10 ** d.lr.mean()), "unit": "Earth radii (geometric mean)"}
    statistics[f"geomean_period_{k}"] = {"n": len(d), "mean": float(10 ** d.lp.mean()), "unit": "days (geometric mean)"}
    groups[k] = {"n": len(d), "share_of_sample": len(d) / N, "count": len(d)}
    statistics[f"share_{k}"] = {"n": N, "count": len(d), "share": len(d) / N}

# bins
pmax = df.pl_orbper.max(); rmax = df.pl_rade.max()
p_edges = [0.05, 1, 3, 10, 30, 100, 300, 1000, 3000, float(10 ** np.ceil(np.log10(pmax * 1.0001)))]
r_edges = [0.0, 1, 1.5, 2, 4, 8, 15, float(np.ceil(rmax * 1.0001))]
def lab(e, i): return f"{e[i]:g}-{e[i+1]:g}"
def binned(x, edges):
    c, _ = np.histogram(x, bins=edges)
    return [int(v) for v in c]
def bins_obj(x, edges):
    c = binned(x, edges)
    return [{"lower": float(edges[i]), "upper": float(edges[i + 1]), "count": c[i]} for i in range(len(c))]
dist = {}
for k, d in sub.items():
    dist[f"period_bins_{k}"] = {"variable": "pl_orbper (days)", "n": len(d), "bins": bins_obj(d.pl_orbper, p_edges)}
    dist[f"radius_bins_{k}"] = {"variable": "pl_rade (Earth radii)", "n": len(d), "bins": bins_obj(d.pl_rade, r_edges)}
    # fine log10 histograms (0.25 dex period, 0.1 dex radius)
    fp = np.arange(np.floor(df.lp.min() * 4) / 4, df.lp.max() + 0.25, 0.25)
    fr = np.arange(np.floor(df.lr.min() * 10) / 10, df.lr.max() + 0.1, 0.1)
    dist[f"log10_period_fine_{k}"] = {"variable": "log10 pl_orbper", "n": len(d), "bins": bins_obj(d.lp, fp)}
    dist[f"log10_radius_fine_{k}"] = {"variable": "log10 pl_rade", "n": len(d), "bins": bins_obj(d.lr, fr)}
    dist[f"method_{k}"] = {"variable": "discoverymethod", "n": len(d),
        "categories": [{"category": m, "count": int(c)} for m, c in d.discoverymethod.value_counts().items()]}
    # joint
    H, _, _ = np.histogram2d(d.pl_rade, d.pl_orbper, bins=[r_edges, p_edges])
    cats = []
    for i in range(len(r_edges) - 1):
        for j in range(len(p_edges) - 1):
            cats.append({"category": f"R {lab(r_edges,i)} Re | P {lab(p_edges,j)} d", "count": int(H[i, j]),
                         "share": float(H[i, j] / len(d)) if len(d) else None,
                         "radius_lower": r_edges[i], "radius_upper": r_edges[i+1],
                         "period_lower": p_edges[j], "period_upper": p_edges[j+1]})
    dist[f"joint_cells_{k}"] = {"variable": "radius bin x period bin", "n": len(d), "categories": cats}
    assert sum(c["count"] for c in cats) == len(d)

# full sample flow / cross-tabs
ct = raw.groupby(["radius_group", "tran_flag"]).size().reset_index(name="count")
dist["radius_group_by_tran_flag_all6445"] = {"variable": "radius_group x tran_flag", "n": N_RAW,
    "categories": [{"category": f"{r.radius_group} | tran_flag={r.tran_flag}", "count": int(r["count"])} for _, r in ct.iterrows()]}
dist["method_all_catalogue"] = {"variable": "discoverymethod (all 6,445)", "n": N_RAW,
    "categories": [{"category": m, "count": int(c)} for m, c in raw.discoverymethod.value_counts().items()]}
dist["mass_provenance_calculated"] = {"variable": "pl_bmassprov", "n": len(sub["calculated"]),
    "categories": [{"category": str(m), "count": int(c)} for m, c in sub["calculated"].pl_bmassprov.fillna("missing").value_counts().items()]}

# comparisons
def boot_diff(a, b, fn, B=2000):
    a = np.asarray(a); b = np.asarray(b)
    out = np.empty(B)
    for i in range(B):
        out[i] = fn(rng.choice(a, len(a))) - fn(rng.choice(b, len(b)))
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]
def compare(a, b, tag):
    res = {"n_calculated": len(a), "n_measured_transiting": len(b)}
    for var in ["lr", "lp"]:
        for name, p in [("median", .5), ("p10", .1), ("p25", .25), ("p75", .75), ("p90", .9)]:
            f = lambda x, p=p: np.quantile(x, p)
            diff = float(f(a[var]) - f(b[var]))
            ci = boot_diff(a[var], b[var], f)
            res[f"{var}_{name}_diff"] = {"estimate": diff, "ci_lower": ci[0], "ci_upper": ci[1], "ratio_10_pow": float(10 ** diff)}
        ks = stats.ks_2samp(a[var], b[var])
        res[f"{var}_ks_distance"] = float(ks.statistic)
    return res
comparisons = {"calculated_minus_measured_transiting": compare(sub["calculated"], sub["measured_transiting"], "main")}
# joint cell share differences (percentage points)
cd = []
for ca, cb in zip(dist["joint_cells_calculated"]["categories"], dist["joint_cells_measured_transiting"]["categories"]):
    cd.append({"cell": ca["category"], "share_calculated": ca["share"], "share_measured_transiting": cb["share"],
               "diff_pp": 100 * (ca["share"] - cb["share"])})
comparisons["cell_share_differences"] = cd
# robustness
clean = df[(df.rad_limit_flagged == 0) & (df.per_limit_flagged == 0)]
comparisons["robust_excl_limit_flagged"] = compare(clean[clean.radius_group == "calculated"], clean[clean.radius_group == "measured_transiting"], "r1")
comparisons["robust_excl_limit_flagged"]["n_dropped"] = int(N - len(clean))
c1 = df[df.pl_orbper <= 1000]
comparisons["robust_period_le_1000d"] = compare(c1[c1.radius_group == "calculated"], c1[c1.radius_group == "measured_transiting"], "r2")

# associations
def boot_spear(x, y, B=2000):
    x = np.asarray(x); y = np.asarray(y); n = len(x); out = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        out.append(stats.spearmanr(x[i], y[i])[0])
    return [float(np.nanpercentile(out, 2.5)), float(np.nanpercentile(out, 97.5))]
assoc = {}
for k, d in sub.items():
    if len(d) < 10: continue
    r = stats.spearmanr(d.lp, d.lr)[0]
    ci = boot_spear(d.lp, d.lr)
    assoc[f"radius_period_{k}"] = {"x": "log10 pl_orbper", "y": "log10 pl_rade", "method": "spearman",
        "estimate": float(r), "n": len(d), "ci_lower": ci[0], "ci_upper": ci[1]}
cal = sub["calculated"].dropna(subset=["pl_bmasse"])
cal = cal[cal.pl_bmasse > 0]
r = stats.spearmanr(np.log10(cal.pl_bmasse), cal.lr)[0]
assoc["mass_radius_calculated"] = {"x": "log10 pl_bmasse (Earth masses)", "y": "log10 pl_rade", "method": "spearman",
    "estimate": float(r), "n": len(cal)}
_ci = boot_spear(np.log10(cal.pl_bmasse), cal.lr)
assoc["mass_radius_calculated"].update(ci_lower=_ci[0], ci_upper=_ci[1])
mt = sub["measured_transiting"].dropna(subset=["pl_bmasse"]); mt = mt[mt.pl_bmasse > 0]
assoc["mass_radius_measured_transiting"] = {"x": "log10 pl_bmasse (Earth masses)", "y": "log10 pl_rade", "method": "spearman",
    "estimate": float(stats.spearmanr(np.log10(mt.pl_bmasse), mt.lr)[0]), "n": len(mt)}

sample = {"n_observations": N, "unit": "confirmed planet", "source": "data.db table planets_classified (NASA Exoplanet Archive pscomppars)",
          "sample_flow": [{"step": "raw rows", "n": N_RAW},
                          {"step": "missing radius dropped", "dropped": n_norad},
                          {"step": "missing period dropped (some also lack radius)", "dropped_period_missing": n_noper},
                          {"step": "radius and period present", "n": N}],
          "n_raw": N_RAW, "n_missing_radius": n_norad, "n_missing_period": n_noper,
          "note": "pl_controv_flag not loaded; controversial planets not excluded. Limit-flagged values kept in main sample."}

out = {"result_kind": "descriptive", "sample": sample, "statistics": statistics, "distributions": dist,
       "associations": assoc, "groups": groups, "comparisons": comparisons,
       "bootstrap": {"resamples": 2000, "seed": SEED, "method": "percentile"},
       "quantile_definition": "numpy default (Hyndman-Fan type 7)",
       "figures": ["fig_radius_period_all.pdf", "fig_radius_period_by_group.pdf", "fig_marginals_by_group.pdf", "fig_mass_radius_calculated.pdf"]}
json.dump(out, open("estimation_results.json", "w"), indent=1, default=float)
print(json.dumps({k: groups[k] for k in groups}))
print({k: statistics[f"radius_{k}"]["median"] for k in sub}, {k: statistics[f"period_{k}"]["median"] for k in sub})
print(json.dumps(comparisons["calculated_minus_measured_transiting"]["lr_median_diff"]), assoc)
