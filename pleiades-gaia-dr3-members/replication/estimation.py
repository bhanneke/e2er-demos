"""
Replication script for: Which Stars within 3 Degrees of the Pleiades Centre Share Its Astrometry?
A Descriptive Reading of Gaia DR3 Membership, Parallax Distance and the Colour--Magnitude Diagram
Paper ID: 09bc8be0-20c4-4a5d-8241-282ccd2a45b1

Requirements: pandas, numpy, matplotlib
Usage: python estimation.py   (run from any directory)
Input: data/gaia_dr3.csv (raw Gaia DR3 extract, pulled 2026-10-13; see README.md)
Output: replication/output/ (tables as CSV, figures as PNG, estimation_results.json)

Descriptive only: counts, medians, percentiles, binned locus summaries and a
sensitivity grid of re-counts. No regression, no significance test, no causal claim.
"""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

np.random.seed(42)  # no stochastic step; seeded for the audit trail

ROOT = Path(__file__).resolve().parent.parent          # workspace root
RAW = ROOT / "data" / "gaia_dr3.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

R_BASE = 5.0                  # proper-motion radius, mas/yr (base)
ZP_OFFSET = 0.03              # approximate Lindegren et al. (2021) offset, mas (sensitivity only)
SEED_BAND = (5.0, 10.0)       # parallax band used only to seed the proper-motion centre, mas
EXPECTED_QUALITY_N = 9970     # quality sample size reported in the paper (sanity check)

# ── 1. Load data ──────────────────────────────────────────────────────────────
raw = pd.read_csv(RAW)
print("raw extract rows:", len(raw))


def quality(df, ruwe_max=1.4, poe_min=10.0):
    """Base quality cuts: duplicates, 5-/6-parameter solutions, non-null astrometry, RUWE, parallax S/N."""
    d = df.drop_duplicates(subset="source_id")
    d = d[d["astrometric_params_solved"].isin([31, 95])]
    d = d.dropna(subset=["parallax", "pmra", "pmdec"])
    d = d[d["ruwe"] < ruwe_max]
    d = d[d["parallax_over_error"] > poe_min]
    return d.copy()


def sample_flow(df):
    """Row counts at each base-quality filter, for Table 1 (sample flow)."""
    steps = [("raw extract", len(df))]
    d = df.drop_duplicates(subset="source_id")
    steps.append(("remove duplicate source_id", len(d)))
    d = d[d["astrometric_params_solved"].isin([31, 95])].dropna(subset=["parallax", "pmra", "pmdec"])
    steps.append(("astrometric_params_solved in {31, 95}; non-null astrometry", len(d)))
    d = d[d["ruwe"] < 1.4]
    steps.append(("ruwe < 1.4", len(d)))
    d = d[d["parallax_over_error"] > 10.0]
    steps.append(("parallax_over_error > 10 (quality sample)", len(d)))
    return steps


base = quality(raw)
assert len(base) == EXPECTED_QUALITY_N, f"quality sample {len(base)} != {EXPECTED_QUALITY_N}"
flow = sample_flow(raw)

# ── 2. Variable construction ──────────────────────────────────────────────────
# Membership is built from the base quality sample. Distances are 1000 / parallax (pc),
# uncorrected for the zero point, and are labelled as such everywhere.


def clip_stats(x, k=3.0):
    """Median and sd of x after iterative k-sigma clipping (spec section 2, steps 1 and 3)."""
    x = np.asarray(x, dtype=float)
    keep = np.ones(len(x), dtype=bool)
    for _ in range(200):
        m = np.median(x[keep])
        s = x[keep].std(ddof=1)
        new = np.abs(x - m) < k * s
        if (new == keep).all():
            break
        keep = new
    return float(np.median(x[keep])), float(x[keep].std(ddof=1))


def pm_seed(d):
    """Densest 2 mas/yr proper-motion bin among quality stars in the parallax band (seed only)."""
    band = d[(d["parallax"] > SEED_BAND[0]) & (d["parallax"] < SEED_BAND[1])]
    h, xe, ye = np.histogram2d(band["pmra"], band["pmdec"],
                               bins=[np.arange(-30, 50, 2.0), np.arange(-80, 20, 2.0)])
    i, j = np.unravel_index(h.argmax(), h.shape)
    return float(xe[i] + 1.0), float(ye[j] + 1.0)


def membership(d, seed, r=R_BASE, k_win=3.0, fixed=None, zp=0.0):
    """Parallax window |plx - pi0| < k*sigma_pi and PM radius < r, both centred by clipping."""
    plx = d["parallax"].to_numpy() + zp
    pmra = d["pmra"].to_numpy()
    pmdec = d["pmdec"].to_numpy()
    pm0 = np.array(seed, dtype=float)
    for _ in range(200):
        in_pm = np.hypot(pmra - pm0[0], pmdec - pm0[1]) < r
        pi0, sigma_pi = clip_stats(plx[in_pm])
        half = k_win * sigma_pi if fixed is None else fixed
        sel = (np.abs(plx - pi0) < half) & in_pm
        new_pm = np.array([clip_stats(pmra[sel])[0], clip_stats(pmdec[sel])[0]])
        if np.allclose(new_pm, pm0, atol=1e-6):
            break
        pm0 = new_pm
    in_pm = np.hypot(pmra - pm0[0], pmdec - pm0[1]) < r
    pi0, sigma_pi = clip_stats(plx[in_pm])
    half = k_win * sigma_pi if fixed is None else fixed
    win = np.abs(plx - pi0) < half
    return {"members": win & in_pm, "win_only": win, "pi0": pi0, "sigma_pi": sigma_pi,
            "half_window": half, "pm0": pm0}


def window_label(k_win, fixed):
    return f"fixed +/-{fixed:g} mas" if fixed is not None else f"{k_win:g} sigma"


def count_row(label, ruwe=1.4, poe=10.0, r=R_BASE, k_win=3.0, fixed=None, zp=0.0, g_floor=None):
    """One re-count of the sensitivity grid; the centres are recomputed with the same seed."""
    d = quality(raw, ruwe, poe)
    if g_floor is not None:
        d = d[d["phot_g_mean_mag"] > g_floor]
    res = membership(d, SEED, r=r, k_win=k_win, fixed=fixed, zp=zp)
    return {"row": label, "pm_radius_mas_yr": r, "parallax_window": window_label(k_win, fixed),
            "ruwe_max": ruwe, "parallax_over_error_min": poe,
            "zero_point": "approx Lindegren offset" if zp else "none",
            "g_floor": g_floor, "n_quality": int(len(d)),
            "n_members": int(res["members"].sum()),
            "parallax_centre_mas": float(res["pi0"]),
            "pm_centre_mas_yr": [float(res["pm0"][0]), float(res["pm0"][1])]}


SEED = pm_seed(base)
naive_plx, naive_sigma = clip_stats(base["parallax"].to_numpy())
print("proper-motion seed (mas/yr):", SEED)
print("naive full-sample parallax centre (mas, not used):", round(naive_plx, 3))

# ── 3. Summary statistics and membership ────────────────────────────────────────
res = membership(base, SEED)
mem_mask = res["members"]
members = base[mem_mask].copy()
n_members = int(mem_mask.sum())
print("members:", n_members, "pi0", round(res["pi0"], 4), "sigma_pi", round(res["sigma_pi"], 4),
      "pm0", np.round(res["pm0"], 3))

members["distance_pc"] = 1000.0 / members["parallax"]
members["distance_modulus_mag"] = 5.0 * np.log10(members["distance_pc"]) - 5.0
cm = members.dropna(subset=["bp_rp", "phot_g_mean_mag"])


def stat(x, unit):
    x = pd.Series(x).dropna().astype(float)
    return {"n": int(x.size), "mean": float(x.mean()), "sd": float(x.std(ddof=1)),
            "min": float(x.min()), "p25": float(x.quantile(0.25)), "median": float(x.median()),
            "p75": float(x.quantile(0.75)), "max": float(x.max()), "unit": unit}


statistics = {
    "parallax_mas": stat(members["parallax"], "mas"),
    "pmra_mas_yr": stat(members["pmra"], "mas/yr"),
    "pmdec_mas_yr": stat(members["pmdec"], "mas/yr"),
    "distance_pc": stat(members["distance_pc"], "pc"),
    "distance_modulus_mag": stat(members["distance_modulus_mag"], "mag"),
    "phot_g_mean_mag": stat(members["phot_g_mean_mag"], "mag"),
    "bp_rp": stat(cm["bp_rp"], "mag"),
    "members_share": {"n": len(base), "share": n_members / len(base), "count": n_members},
}

# ── 4. Main specification (membership counts and stage flow) ────────────────────
# Table 2: stage counts; Table 3: membership sensitivity grid
stage_counts = {"quality": len(base), "parallax_window": int(res["win_only"].sum()),
                "pm_radius": n_members}

# ── 5. Robustness checks (sensitivity grid, one dimension at a time) ───────────
grid = [
    count_row("base"),
    count_row("PM radius 3", r=3.0),
    count_row("PM radius 7", r=7.0),
    count_row("PM radius 10", r=10.0),
    count_row("parallax window 2 sigma", k_win=2.0),
    count_row("parallax window fixed +/-1 mas", fixed=1.0),
    count_row("RUWE < 1.2", ruwe=1.2),
    count_row("parallax_over_error > 5", poe=5.0),
    count_row("zero point correction", zp=ZP_OFFSET),
    count_row("G > 6 floor", g_floor=6.0),
]
base_n = grid[0]["n_members"]
one_at_a_time = [g["n_members"] for g in grid]
grid_median = float(np.median(one_at_a_time))
max_change = max(abs(n - base_n) / base_n for n in one_at_a_time[1:])
print("one-at-a-time member counts:", one_at_a_time, "median", grid_median)

# Full cross: PM radius x parallax window x RUWE x parallax_over_error (48 rows)
cross = []
for r in [3.0, 5.0, 7.0, 10.0]:
    for k_win, fixed in [(2.0, None), (3.0, None), (3.0, 1.0)]:
        for ruwe in [1.2, 1.4]:
            for poe in [5.0, 10.0]:
                cross.append(count_row("cross", ruwe=ruwe, poe=poe, r=r, k_win=k_win, fixed=fixed))
cross_n = np.array([c["n_members"] for c in cross])
print("full cross rows:", len(cross), "members min/median/max:",
      cross_n.min(), np.median(cross_n), cross_n.max())

# ── 6. Distributions: parallax and distance ─────────────────────────────────────
# Figure 3 (distance histogram) and Table 4 (distance summary)


def hist_bins(values, width):
    lo = math.floor(values.min() / width) * width
    hi = math.ceil(values.max() / width) * width + width
    edges = np.arange(lo, hi + width / 2, width)
    counts, _ = np.histogram(values, bins=edges)
    return [{"lower": float(edges[i]), "upper": float(edges[i + 1]), "count": int(counts[i])}
            for i in range(len(counts))]


plx_bins = hist_bins(members["parallax"], 0.25)
dist_bins = hist_bins(members["distance_pc"], 5.0)
assert sum(b["count"] for b in plx_bins) == n_members
assert sum(b["count"] for b in dist_bins) == n_members

# Parallax mode from a 0.1 mas histogram and local-peak count (unimodality check)
edges_01 = np.arange(math.floor(members["parallax"].min() * 10) / 10,
                     members["parallax"].max() + 0.2, 0.1)
counts_01, edges_01 = np.histogram(members["parallax"], bins=edges_01)
smooth = np.convolve(counts_01, np.ones(3) / 3, mode="same")
peaks = [i for i in range(1, len(smooth) - 1)
         if smooth[i] > smooth[i - 1] and smooth[i] >= smooth[i + 1] and smooth[i] > 0.05 * smooth.max()]
i_mode = int(np.argmax(counts_01))
mode_mas = float(0.5 * (edges_01[i_mode] + edges_01[i_mode + 1]))
median_plx = float(members["parallax"].median())
mean_se = float(members["parallax"].std(ddof=1) / math.sqrt(n_members))  # standard error of the mean, sigma/sqrt(n)

# ── 7. Main-sequence locus (CMD) ───────────────────────────────────────────────
# Table 5: median and 16th-84th percentile of BP-RP in 1-mag G bins
locus = []
for lo in range(6, 18):
    sub = cm[(cm["phot_g_mean_mag"] >= lo) & (cm["phot_g_mean_mag"] < lo + 1)]
    row = {"g_lower": lo, "g_upper": lo + 1, "n": int(len(sub))}
    if len(sub):
        row.update(median_bp_rp=float(sub["bp_rp"].median()),
                   p16_bp_rp=float(sub["bp_rp"].quantile(0.16)),
                   p84_bp_rp=float(sub["bp_rp"].quantile(0.84)))
    else:
        row.update(median_bp_rp=None, p16_bp_rp=None, p84_bp_rp=None)
    locus.append(row)

field = base[~mem_mask].dropna(subset=["bp_rp", "phot_g_mean_mag"])

# ── 8. Export tables ────────────────────────────────────────────────────────────
# Table 1 (sample flow): paper sample-construction table
pd.DataFrame(flow, columns=["step", "n_kept"]).assign(
    n_dropped=lambda t: t["n_kept"].shift(1, fill_value=t["n_kept"].iloc[0]) - t["n_kept"]
).to_csv(OUTPUT_DIR / "table1_sample_flow.csv", index=False)

# Table 2 (membership stage counts): paper membership section
pd.DataFrame([stage_counts]).to_csv(OUTPUT_DIR / "table2_membership_stages.csv", index=False)

# Table 3 (membership sensitivity grid): paper robustness table, one-at-a-time rows
pd.DataFrame(grid).to_csv(OUTPUT_DIR / "table3_membership_grid.csv", index=False)

# Table 3b (full 48-row cross): paper robustness appendix
pd.DataFrame(cross).to_csv(OUTPUT_DIR / "table3b_membership_full_cross.csv", index=False)

# Table 4 (summary statistics of members): paper summary-statistics table
pd.DataFrame([{"variable": k, **{kk: vv for kk, vv in v.items() if kk != "unit"}, "unit": v["unit"]}
              for k, v in statistics.items() if "unit" in v]).to_csv(
    OUTPUT_DIR / "table4_summary_statistics.csv", index=False)

# Table 5 (main-sequence locus by G bin): paper CMD table
pd.DataFrame(locus).to_csv(OUTPUT_DIR / "table5_main_sequence_locus.csv", index=False)

# Table 6 (distance summary, uncorrected 1000/parallax): paper distance paragraph
pd.DataFrame([{
    "distance_pc_median": statistics["distance_pc"]["median"],
    "distance_pc_p16": float(members["distance_pc"].quantile(0.16)),
    "distance_pc_p84": float(members["distance_pc"].quantile(0.84)),
    "distance_pc_iqr": float(members["distance_pc"].quantile(0.75) - members["distance_pc"].quantile(0.25)),
    "distance_modulus_median_mag": statistics["distance_modulus_mag"]["median"],
}]).to_csv(OUTPUT_DIR / "table6_distance_summary.csv", index=False)

# ── 9. Figures ──────────────────────────────────────────────────────────────────
# Figure 1 (vector-point diagram): paper membership figure
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(base["pmra"], base["pmdec"], s=2, c="0.7", label="quality sample")
ax.scatter(members["pmra"], members["pmdec"], s=3, c="C0", label="members")
ax.set_xlabel(r"$\mu_\alpha^*$ (mas/yr)")
ax.set_ylabel(r"$\mu_\delta$ (mas/yr)")
ax.set_xlim(-40, 60)
ax.set_ylim(-90, 30)
ax.legend(markerscale=3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_vpd_pm.png", dpi=200)
plt.close(fig)

# Figure 2a (colour-magnitude diagram of the quality sample): all quality-cut stars, uncorrected for extinction
quality_cm = base.dropna(subset=["bp_rp", "phot_g_mean_mag"])
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(quality_cm["bp_rp"], quality_cm["phot_g_mean_mag"], s=1, c="0.75", label="quality sample")
ax.invert_yaxis()
ax.set_xlabel(r"$BP-RP$ (mag, uncorrected)")
ax.set_ylabel(r"$G$ (mag)")
ax.legend(markerscale=3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_cmd.png", dpi=200)
plt.close(fig)

# Figure 2b (colour-magnitude diagram of the members): members in blue, quality-cut non-members in grey, uncorrected
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(field["bp_rp"], field["phot_g_mean_mag"], s=1, c="0.75", label="quality sample, non-members")
ax.scatter(cm["bp_rp"], cm["phot_g_mean_mag"], s=4, c="C0", label="members")
ax.invert_yaxis()
ax.set_xlabel(r"$BP-RP$ (mag, uncorrected)")
ax.set_ylabel(r"$G$ (mag)")
ax.legend(markerscale=3)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_cmd_members.png", dpi=200)
plt.close(fig)

# Figure 3 (distance histogram): paper distance figure, uncorrected 1000/parallax
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(members["distance_pc"], bins=[b["lower"] for b in dist_bins] + [dist_bins[-1]["upper"]],
        color="C0", edgecolor="white")
ax.set_xlabel("Distance, $1000/\\varpi$ (pc, uncorrected)")
ax.set_ylabel("Members")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_distance_hist.png", dpi=200)
plt.close(fig)

# Bright end (spec section 4.6): extract stars brighter than the brightest member, and the quality cuts they fail
bright_g = float(members["phot_g_mean_mag"].min())
bright = raw[raw["phot_g_mean_mag"] < bright_g]
bright_is_base = bright.index.isin(base.index)
bright_end = {
    "brightest_member_G": bright_g,
    "n_extract_brighter": int(len(bright)),
    "G_range_brighter": [float(bright["phot_g_mean_mag"].min()), float(bright["phot_g_mean_mag"].max())]
    if len(bright) else None,
    "n_passing_quality_sample": int(bright_is_base.sum()),
    "fails": {
        "astrometric_params_solved_not_31_or_95": int((~bright["astrometric_params_solved"].isin([31, 95])).sum()),
        "ruwe_ge_1.4": int((bright["ruwe"] >= 1.4).sum()),
        "parallax_over_error_le_10": int((bright["parallax_over_error"] <= 10).sum()),
    },
    "min_ruwe": float(bright["ruwe"].dropna().min()) if bright["ruwe"].notna().any() else None,
    "note": "records the gap at the bright end; does not identify the cut responsible for each star",
}
print("bright end:", bright_end["n_extract_brighter"], "extract stars brighter than G =", round(bright_g, 3))

# ── 10. Export results JSON ─────────────────────────────────────────────────────
results = {
    "result_kind": "descriptive",
    "sample": {"n_observations": len(base), "unit": "source",
               "source": "data/gaia_dr3.csv, base quality cuts"},
    "statistics": statistics,
    "distributions": {
        "parallax": {"variable": "parallax_mas", "n": n_members, "bins": plx_bins},
        "distance": {"variable": "distance_pc", "n": n_members, "bins": dist_bins},
    },
    "figures": ["fig_vpd_pm.png", "fig_cmd.png", "fig_cmd_members.png", "fig_distance_hist.png"],
    "membership": {
        "seed_pm_mas_yr": [SEED[0], SEED[1]],
        "pm_radius_mas_yr": R_BASE,
        "parallax_centre_mas": float(res["pi0"]),
        "parallax_sigma_mas": float(res["sigma_pi"]),
        "parallax_half_window_mas": float(res["half_window"]),
        "pm_centre_mas_yr": [float(res["pm0"][0]), float(res["pm0"][1])],
        "naive_full_sample_parallax_centre_mas": float(naive_plx),
        "stage_counts": stage_counts,
        "parallax_mode_mas": mode_mas,
        "parallax_median_mas": median_plx,
        "parallax_mode_minus_median_mas": mode_mas - median_plx,
        "parallax_local_peaks": len(peaks),
        "parallax_mean_se_mas": mean_se,
        "grid_one_at_a_time_median_members": grid_median,
        "grid_max_change_share": max_change,
        "grid_base_within_10pct_of_median": bool(abs(base_n - grid_median) <= 0.1 * grid_median),
        "field_cmd_rows": int(len(field)),
    },
    "membership_grid": grid,
    "grid_full_cross": {"n_rows": len(cross), "n_members_min": int(cross_n.min()),
                        "n_members_median": float(np.median(cross_n)),
                        "n_members_max": int(cross_n.max()), "rows": cross},
    "distance_summary": {
        "distance_pc_median": statistics["distance_pc"]["median"],
        "distance_pc_p16": float(members["distance_pc"].quantile(0.16)),
        "distance_pc_p84": float(members["distance_pc"].quantile(0.84)),
        "distance_pc_iqr": float(members["distance_pc"].quantile(0.75) - members["distance_pc"].quantile(0.25)),
        "distance_modulus_median_mag": statistics["distance_modulus_mag"]["median"],
        "note": "1000/parallax, uncorrected for the zero point; descriptive, not a model-based distance",
    },
    "main_sequence_locus": locus,
    "cmd_extremes": {
        "brightest_member_G": float(members["phot_g_mean_mag"].min()),
        "faintest_member_G": float(members["phot_g_mean_mag"].max()),
        "members_without_bp_rp": int(n_members - len(cm)),
    },
    "bright_end": bright_end,
}
with open(OUTPUT_DIR / "estimation_results.json", "w") as f:
    json.dump(results, f, indent=2, allow_nan=False)

print("wrote tables, figures and estimation_results.json to", OUTPUT_DIR)
print("distance median (pc):", round(statistics["distance_pc"]["median"], 2),
      "| members:", n_members, "| brightest member G:", round(float(members["phot_g_mean_mag"].min()), 2))
