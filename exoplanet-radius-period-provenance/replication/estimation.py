"""
Replication script for: How Are Confirmed Exoplanets Distributed in Planet Radius and
Orbital Period? A Descriptive Decomposition by Radius Provenance
Paper ID: 29deb64e-4eb2-4135-979e-35327f8fd7ec

Descriptive study: no regression, no causal claim (see econometric_spec.md). Statistics are
quantiles, counts, bin shares, two-sample KS distances and Spearman rank correlations.
Uncertainty: percentile bootstrap (2,000 resamples), not parametric standard errors, so no
heteroskedasticity-robust SEs apply.

Requirements: pandas, numpy, scipy, matplotlib
Usage: python replication/estimation.py   (from the workspace root, or anywhere)
Input: data/planets.csv (NASA Exoplanet Archive pscomppars, 6,445 rows; see README)
Output: replication/output/ (tables as CSV, figures as PNG, estimation_results_replicated.json)
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)
SEED = 20261013                      # same bootstrap seed as run_estimation.py
rng = np.random.default_rng(SEED)
B = 2000                             # bootstrap resamples

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT_DIR = HERE / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Load data ──────────────────────────────────────────────────────────────
raw = pd.read_csv(ROOT / "data" / "planets.csv")
N_RAW = len(raw)
assert raw.pl_name.is_unique, "pl_name must be unique (one row per planet)"

# ── 2. Variable construction (replication/analysis_prep.py) ──────────────────
def radius_group(r):
    if pd.isna(r.pl_rade):
        return "no_radius"
    if isinstance(r.pl_rade_reflink, str) and "CALCULATED_VALUE" in r.pl_rade_reflink:
        return "calculated"                       # archive label: radius computed from mass
    return "measured_transiting" if r.tran_flag == 1 else "measured_non_transiting"

raw["radius_group"] = raw.apply(radius_group, axis=1)
raw["rad_limit_flagged"] = (raw.pl_radelim.fillna(0) != 0).astype(int)
raw["per_limit_flagged"] = (raw.pl_orbperlim.fillna(0) != 0).astype(int)
raw["in_rp_sample"] = ((raw.pl_rade > 0) & (raw.pl_orbper > 0)).astype(int)

df = raw[raw.in_rp_sample == 1].copy()
df["lr"] = np.log10(df.pl_rade)
df["lp"] = np.log10(df.pl_orbper)
GROUPS = ["calculated", "measured_transiting", "measured_non_transiting"]
sub = {"all": df, **{g: df[df.radius_group == g] for g in GROUPS}}
N = len(df)
assert sum(len(sub[g]) for g in GROUPS) == N

flow = pd.DataFrame([
    ("raw rows", N_RAW),
    ("pl_rade missing (dropped)", int(raw.pl_rade.isna().sum())),
    ("pl_orbper missing (any radius)", int(raw.pl_orbper.isna().sum())),
    ("radius-period sample", N),
], columns=["step", "n"])
flow.to_csv(OUTPUT_DIR / "table_sample_flow.csv", index=False)  # Sample description / data section

# Cross-tabs on all 6,445 rows: provenance by tran_flag and by discovery method
pd.crosstab(raw.radius_group, raw.tran_flag).to_csv(OUTPUT_DIR / "table_group_by_tranflag.csv")  # Data section cross-tab
pd.crosstab(raw.radius_group, raw.discoverymethod).T.to_csv(OUTPUT_DIR / "table_group_by_method.csv")  # Data section cross-tab

# ── 3. Summary statistics (Table 1: radius and period by group) ──────────────
QS = {"p5": .05, "p10": .10, "p25": .25, "median": .50, "p75": .75, "p90": .90, "p95": .95}

def desc(x):
    x = np.asarray(x, float)
    d = {"n": len(x), "mean": x.mean(), "sd": x.std(ddof=1) if len(x) > 1 else np.nan, "min": x.min()}
    d.update({k: np.quantile(x, p) for k, p in QS.items()})   # numpy type-7 quantiles
    d["max"] = x.max()
    return d

rows = []
for k, d in sub.items():
    for var, col in [("radius_earth", "pl_rade"), ("period_days", "pl_orbper"),
                     ("log10_radius", "lr"), ("log10_period", "lp")]:
        rows.append({"group": k, "variable": var, **desc(d[col])})
    rows.append({"group": k, "variable": "geomean_radius_earth", "n": len(d), "mean": 10 ** d.lr.mean()})
    rows.append({"group": k, "variable": "geomean_period_days", "n": len(d), "mean": 10 ** d.lp.mean()})
stats_tab = pd.DataFrame(rows)
stats_tab.to_csv(OUTPUT_DIR / "table1_summary_by_group.csv", index=False)  # Tables: radius_stats, period_stats

groups_tab = pd.DataFrame([{"group": k, "n": len(d), "share_of_sample": len(d) / N} for k, d in sub.items()])
groups_tab.to_csv(OUTPUT_DIR / "table_groups.csv", index=False)  # Table: groups (shares of sample)

# ── 4. Distributions: bins and joint cells ────────────────────────────────────
p_edges = [0.05, 1, 3, 10, 30, 100, 300, 1000, 3000, float(10 ** np.ceil(np.log10(df.pl_orbper.max() * 1.0001)))]
r_edges = [0.0, 1, 1.5, 2, 4, 8, 15, float(np.ceil(df.pl_rade.max() * 1.0001))]

def bin_table(x, edges):
    c, _ = np.histogram(x, bins=edges)
    return pd.DataFrame({"lower": edges[:-1], "upper": edges[1:], "count": c})

rb, pb, joint = [], [], []
for k, d in sub.items():
    rb.append(bin_table(d.pl_rade, r_edges).assign(group=k))
    pb.append(bin_table(d.pl_orbper, p_edges).assign(group=k))
    H, _, _ = np.histogram2d(d.pl_rade, d.pl_orbper, bins=[r_edges, p_edges])
    for i in range(len(r_edges) - 1):
        for j in range(len(p_edges) - 1):
            joint.append({"group": k, "radius_lower": r_edges[i], "radius_upper": r_edges[i + 1],
                          "period_lower": p_edges[j], "period_upper": p_edges[j + 1],
                          "count": int(H[i, j]), "share": H[i, j] / len(d) if len(d) else np.nan})
rb = pd.concat(rb); pb = pd.concat(pb); joint = pd.DataFrame(joint)
rb.to_csv(OUTPUT_DIR / "table_radius_bins.csv", index=False)    # Radius-bin counts (2-4 and 8-15 Re humps)
pb.to_csv(OUTPUT_DIR / "table_period_bins.csv", index=False)    # Period-bin counts
joint.to_csv(OUTPUT_DIR / "table_joint_cells.csv", index=False)  # Joint radius x period cell counts/shares
# Group composition of each radius bin (calculated vs transit-measured share of each pooled hump)
comp = rb.pivot(index="lower", columns="group", values="count")
comp.to_csv(OUTPUT_DIR / "table_radius_bin_composition.csv")  # Humps: 1,901 of 2,090 and 846 of 1,529

# ── 5. Main comparison: calculated vs measured_transiting ─────────────────────
def boot_diff(a, b, fn):
    a, b = np.asarray(a), np.asarray(b)
    out = np.empty(B)
    for i in range(B):
        out[i] = fn(rng.choice(a, len(a))) - fn(rng.choice(b, len(b)))
    return np.percentile(out, [2.5, 97.5])

def compare(a, b):
    rows = []
    for var in ["lr", "lp"]:
        for name, p in [("median", .5), ("p10", .1), ("p25", .25), ("p75", .75), ("p90", .9)]:
            f = lambda x, p=p: np.quantile(x, p)
            diff = f(a[var]) - f(b[var])
            lo, hi = boot_diff(a[var], b[var], f)
            rows.append({"variable": var, "statistic": name, "diff_log10": diff, "ci_lower": lo,
                         "ci_upper": hi, "ratio_10_pow": 10 ** diff})
        rows.append({"variable": var, "statistic": "ks_distance",
                     "diff_log10": stats.ks_2samp(a[var], b[var]).statistic})
    return pd.DataFrame(rows).assign(n_calculated=len(a), n_measured_transiting=len(b))

cal, mt = sub["calculated"], sub["measured_transiting"]
compare(cal, mt).to_csv(OUTPUT_DIR / "table_comparison_main.csv", index=False)  # Main comparison table

cell = joint.pivot_table(index=["radius_lower", "period_lower"], columns="group", values="share")
cell["diff_pp"] = 100 * (cell["calculated"] - cell["measured_transiting"])
cell.to_csv(OUTPUT_DIR / "table_cell_share_differences.csv")  # Joint-cell share differences (pp)

# ── 6. Robustness ─────────────────────────────────────────────────────────────
clean = df[(df.rad_limit_flagged == 0) & (df.per_limit_flagged == 0)]
r1 = compare(clean[clean.radius_group == "calculated"], clean[clean.radius_group == "measured_transiting"])
r1.assign(n_dropped=N - len(clean)).to_csv(OUTPUT_DIR / "table_robust_excl_limit_flagged.csv", index=False)  # Robustness: drop limit-flagged
c1 = df[df.pl_orbper <= 1000]
compare(c1[c1.radius_group == "calculated"], c1[c1.radius_group == "measured_transiting"]).to_csv(
    OUTPUT_DIR / "table_robust_period_le_1000d.csv", index=False)  # Robustness: period <= 1000 d

# ── 7. Associations (Spearman, bootstrap CI) ──────────────────────────────────
def boot_spear(x, y):
    x, y = np.asarray(x), np.asarray(y)
    out = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))
        out.append(stats.spearmanr(x[i], y[i])[0])
    return np.nanpercentile(out, [2.5, 97.5])

arows = []
for k, d in sub.items():
    if len(d) < 10:
        continue
    lo, hi = boot_spear(d.lp, d.lr)
    arows.append({"pair": f"log10 radius ~ log10 period ({k})", "n": len(d),
                  "spearman": stats.spearmanr(d.lp, d.lr)[0], "ci_lower": lo, "ci_upper": hi})
for k in ["calculated", "measured_transiting"]:       # mass-radius diagnostic
    d = sub[k].dropna(subset=["pl_bmasse"])
    d = d[d.pl_bmasse > 0]
    lm = np.log10(d.pl_bmasse)
    lo, hi = boot_spear(lm, d.lr)
    arows.append({"pair": f"log10 radius ~ log10 mass ({k})", "n": len(d),
                  "spearman": stats.spearmanr(lm, d.lr)[0], "ci_lower": lo, "ci_upper": hi})
pd.DataFrame(arows).to_csv(OUTPUT_DIR / "table_associations.csv", index=False)  # Associations table

# Mass provenance of the calculated group
cal.pl_bmassprov.fillna("missing").value_counts().rename_axis("pl_bmassprov").reset_index(name="count").to_csv(
    OUTPUT_DIR / "table_calculated_mass_provenance.csv", index=False)  # Mass-radius diagnostic (Msini vs Mass)

# ── 8. Figures ────────────────────────────────────────────────────────────────
COL = {"calculated": "#d95f02", "measured_transiting": "#1b9e77", "measured_non_transiting": "#7570b3"}

def loglog(ax, xl="Orbital period (days)", yl="Planet radius (Earth radii)"):
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel(xl); ax.set_ylabel(yl)

fig, ax = plt.subplots(figsize=(6, 4.5))                         # Figure 1
for g in GROUPS:
    ax.scatter(sub[g].pl_orbper, sub[g].pl_rade, s=5, alpha=.5, c=COL[g], label=g.replace("_", " "))
loglog(ax); ax.legend(markerscale=3, fontsize=8)
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig1_radius_period_all.png", dpi=200); plt.close(fig)

fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), sharex=True, sharey=True)  # Figure 2
for ax, g in zip(axs, ["calculated", "measured_transiting"]):
    ax.scatter(sub[g].pl_orbper, sub[g].pl_rade, s=5, alpha=.5, c=COL[g])
    ax.set_title(g.replace("_", " ")); loglog(ax)
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig2_radius_period_by_group.png", dpi=200); plt.close(fig)

fr = np.arange(np.floor(df.lr.min() * 4) / 4, df.lr.max() + 0.25, 0.25)  # 0.25 dex bins, as in analysis_prep
fp = np.arange(np.floor(df.lp.min() * 4) / 4, df.lp.max() + 0.25, 0.25)
fig, axs = plt.subplots(2, 2, figsize=(10, 7))                   # Figure 3
for j, g in enumerate(["calculated", "measured_transiting"]):
    axs[0, j].hist(sub[g].lr, bins=fr, color=COL[g]); axs[0, j].set_xlabel("log10 radius (Earth radii)")
    axs[1, j].hist(sub[g].lp, bins=fp, color=COL[g]); axs[1, j].set_xlabel("log10 period (days)")
    axs[0, j].set_title(g.replace("_", " ")); axs[0, j].set_ylabel("Planets"); axs[1, j].set_ylabel("Planets")
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig3_marginals_by_group.png", dpi=200); plt.close(fig)

d = cal.dropna(subset=["pl_bmasse"]); d = d[d.pl_bmasse > 0]
fig, ax = plt.subplots(figsize=(6, 4.5))                         # Figure 4 (mass-radius diagnostic)
ax.scatter(d.pl_bmasse, d.pl_rade, s=5, alpha=.5, c=COL["calculated"])
loglog(ax, "Mass (Earth masses)", "Radius (Earth radii)")
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig4_mass_radius_calculated.png", dpi=200); plt.close(fig)

# ── 9. Export results ─────────────────────────────────────────────────────────
summary = {"n_raw": N_RAW, "n_sample": N, "group_counts": {k: len(v) for k, v in sub.items()},
           "seed": SEED, "bootstrap_resamples": B,
           "note": "pl_controv_flag not loaded; limit-flagged values kept in main sample."}
(OUTPUT_DIR / "estimation_results_replicated.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary, indent=1))
