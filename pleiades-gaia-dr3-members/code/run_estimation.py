"""Descriptive results for the Pleiades Gaia DR3 membership study.

Reads the raw extract data/gaia_dr3.csv, applies the base quality cuts, runs the
membership procedure of econometric_spec.md (parallax window and proper-motion
radius, both centred by iterative clipping), re-counts the sensitivity grid,
and writes estimation_results.json in the descriptive results schema.
No regression, no test statistic, no model-based distance.
"""
import json
import math

import numpy as np
import pandas as pd

RAW = "data/gaia_dr3.csv"
CLEAN = "data/gaia_clean.csv"
OUT = "estimation_results.json"
R_BASE = 5.0          # proper-motion radius, mas/yr
ZP_OFFSET = 0.03      # approximate Lindegren et al. (2021) offset, mas (constant; see spec)
SEED_BAND = (5.0, 10.0)  # parallax band used only to seed the proper-motion centre
FIGURES = ["fig_vpd_pm.pdf", "fig_cmd.pdf", "fig_cmd_members.pdf"]

raw = pd.read_csv(RAW)


def quality(df, ruwe_max=1.4, poe_min=10.0):
    d = df.drop_duplicates(subset="source_id")
    d = d[d["astrometric_params_solved"].isin([31, 95])]
    d = d.dropna(subset=["parallax", "pmra", "pmdec"])
    d = d[d["ruwe"] < ruwe_max]
    d = d[d["parallax_over_error"] > poe_min]
    return d.copy()


def clip_stats(x, k=3.0):
    """Median and sd of x after iterative k-sigma clipping."""
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
    """Densest 2 mas/yr proper-motion bin among stars in the parallax band."""
    band = d[(d["parallax"] > SEED_BAND[0]) & (d["parallax"] < SEED_BAND[1])]
    h, xe, ye = np.histogram2d(band["pmra"], band["pmdec"],
                               bins=[np.arange(-30, 50, 2.0), np.arange(-80, 20, 2.0)])
    i, j = np.unravel_index(h.argmax(), h.shape)
    return float(xe[i] + 1.0), float(ye[j] + 1.0)


def membership(d, seed, r=R_BASE, k_win=3.0, fixed=None, zp=0.0):
    plx = d["parallax"].to_numpy() + zp
    pmra = d["pmra"].to_numpy()
    pmdec = d["pmdec"].to_numpy()
    pm0 = np.array(seed, dtype=float)
    for _ in range(200):
        in_pm = np.hypot(pmra - pm0[0], pmdec - pm0[1]) < r
        pi0, spi = clip_stats(plx[in_pm])
        win = np.abs(plx - pi0) < (k_win * spi if fixed is None else fixed)
        sel = win & in_pm
        new_pm = np.array([clip_stats(pmra[sel])[0], clip_stats(pmdec[sel])[0]])
        if np.allclose(new_pm, pm0, atol=1e-6):
            break
        pm0 = new_pm
    in_pm = np.hypot(pmra - pm0[0], pmdec - pm0[1]) < r
    pi0, spi = clip_stats(plx[in_pm])
    half = k_win * spi if fixed is None else fixed
    win = np.abs(plx - pi0) < half
    return {"members": win & in_pm, "win_only": win, "pi0": pi0, "spi": spi,
            "half_window": half, "pm0": pm0}


def num(x):
    x = float(x)
    return x if math.isfinite(x) else None


def stat(x, unit):
    x = pd.Series(x).dropna().astype(float)
    return {"n": int(x.size), "mean": num(x.mean()), "sd": num(x.std(ddof=1)),
            "min": num(x.min()), "p25": num(x.quantile(0.25)), "median": num(x.median()),
            "p75": num(x.quantile(0.75)), "max": num(x.max()), "unit": unit}


def window_label(k_win, fixed):
    if fixed is not None:
        return f"fixed +/-{fixed:g} mas"
    return f"{k_win:g} sigma"


base = quality(raw)
n_clean = len(pd.read_csv(CLEAN))
assert len(base) == n_clean, f"base quality sample {len(base)} != {CLEAN} {n_clean}"
SEED = pm_seed(base)
print("base quality sample:", len(base))
print("proper-motion seed (mas/yr):", SEED)

# naive full-sample clip, recorded for transparency (see spec section 2)
naive_plx, naive_spi = clip_stats(base["parallax"].to_numpy())
print("naive full-sample parallax centre (mas):", round(naive_plx, 3), "sd", round(naive_spi, 3))


def count_row(label, ruwe=1.4, poe=10.0, r=R_BASE, k_win=3.0, fixed=None, zp=0.0, g_floor=None):
    d = quality(raw, ruwe, poe)
    if g_floor is not None:
        d = d[d["phot_g_mean_mag"] > g_floor]
    res = membership(d, SEED, r=r, k_win=k_win, fixed=fixed, zp=zp)
    return {"row": label, "pm_radius_mas_yr": r, "parallax_window": window_label(k_win, fixed),
            "ruwe_max": ruwe, "parallax_over_error_min": poe,
            "zero_point": "approx Lindegren offset" if zp else "none",
            "g_floor": g_floor, "n_quality": int(len(d)),
            "n_members": int(res["members"].sum()),
            "parallax_centre_mas": num(res["pi0"]),
            "pm_centre_mas_yr": [num(res["pm0"][0]), num(res["pm0"][1])]}


# ---- base specification -------------------------------------------------------
res = membership(base, SEED)
mem_mask = res["members"]
members = base[mem_mask].copy()
n_members = int(mem_mask.sum())
print("members:", n_members, "pi0", round(res["pi0"], 4), "spi", round(res["spi"], 4),
      "pm0", np.round(res["pm0"], 3))

stage_quality = len(base)
stage_window = int(res["win_only"].sum())
stage_pm = n_members
print("stage counts: quality", stage_quality, "parallax window", stage_window, "PM radius", stage_pm)

members["distance_pc"] = 1000.0 / members["parallax"]
members["distance_modulus_mag"] = 5.0 * np.log10(members["distance_pc"]) - 5.0

# ---- sensitivity grid: one dimension at a time -----------------------------------
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
print("one-at-a-time grid counts:", one_at_a_time, "median", grid_median)

# ---- full cross of PM radius, window, RUWE, parallax_over_error ------------------
cross = []
for r in [3.0, 5.0, 7.0, 10.0]:
    for k_win, fixed in [(2.0, None), (3.0, None), (3.0, 1.0)]:
        for ruwe in [1.2, 1.4]:
            for poe in [5.0, 10.0]:
                cross.append(count_row("cross", ruwe=ruwe, poe=poe, r=r, k_win=k_win, fixed=fixed))
cross_n = np.array([c["n_members"] for c in cross])
print("full cross rows:", len(cross), "members min/median/max:",
      cross_n.min(), np.median(cross_n), cross_n.max())

# ---- descriptive statistics of members -----------------------------------------
cm = members.dropna(subset=["bp_rp", "phot_g_mean_mag"])
statistics = {
    "parallax_mas": stat(members["parallax"], "mas"),
    "pmra_mas_yr": stat(members["pmra"], "mas/yr"),
    "pmdec_mas_yr": stat(members["pmdec"], "mas/yr"),
    "distance_pc": stat(members["distance_pc"], "pc"),
    "distance_modulus_mag": stat(members["distance_modulus_mag"], "mag"),
    "phot_g_mean_mag": stat(members["phot_g_mean_mag"], "mag"),
    "bp_rp": stat(cm["bp_rp"], "mag"),
    "members_share": {"n": int(stage_quality), "share": float(n_members / stage_quality),
                      "count": n_members},
}

# ---- distributions ----------------------------------------------------------------
def hist_bins(values, width):
    lo = math.floor(values.min() / width) * width
    hi = math.ceil(values.max() / width) * width + width
    edges = np.arange(lo, hi + width / 2, width)
    counts, _ = np.histogram(values, bins=edges)
    return [{"lower": num(edges[i]), "upper": num(edges[i + 1]), "count": int(counts[i])}
            for i in range(len(counts))]


plx_bins = hist_bins(members["parallax"], 0.25)
dist_bins = hist_bins(members["distance_pc"], 5.0)
assert sum(b["count"] for b in plx_bins) == n_members
assert sum(b["count"] for b in dist_bins) == n_members

# parallax mode and unimodality diagnostics
counts_01, edges_01 = np.histogram(members["parallax"], bins=np.arange(
    math.floor(members["parallax"].min() * 10) / 10, members["parallax"].max() + 0.2, 0.1))
smooth = np.convolve(counts_01, np.ones(3) / 3, mode="same")
peaks = [i for i in range(1, len(smooth) - 1)
         if smooth[i] > smooth[i - 1] and smooth[i] >= smooth[i + 1] and smooth[i] > 0.05 * smooth.max()]
mode_mas = float(0.5 * (edges_01[int(np.argmax(counts_01))] + edges_01[int(np.argmax(counts_01)) + 1]))
median_plx = float(members["parallax"].median())

# ---- main-sequence locus -----------------------------------------------------------
locus = []
for lo in range(6, 18):
    sub = cm[(cm["phot_g_mean_mag"] >= lo) & (cm["phot_g_mean_mag"] < lo + 1)]
    row = {"g_lower": lo, "g_upper": lo + 1, "n": int(len(sub))}
    if len(sub):
        row.update(median_bp_rp=num(sub["bp_rp"].median()),
                   p16_bp_rp=num(sub["bp_rp"].quantile(0.16)),
                   p84_bp_rp=num(sub["bp_rp"].quantile(0.84)))
    else:
        row.update(median_bp_rp=None, p16_bp_rp=None, p84_bp_rp=None)
    locus.append(row)

field_cmd = base[~mem_mask].dropna(subset=["bp_rp", "phot_g_mean_mag"])

# bright end: extract stars brighter than the brightest member, and whether they pass the quality cuts
g_sorted = members["phot_g_mean_mag"].sort_values().to_numpy()
brightest_g = float(g_sorted[0])
bright_raw = raw.drop_duplicates(subset="source_id")
bright_raw = bright_raw[bright_raw["phot_g_mean_mag"] < brightest_g]
bright_pass = (bright_raw["astrometric_params_solved"].isin([31, 95]) & (bright_raw["ruwe"] < 1.4)
               & (bright_raw["parallax_over_error"] > 10.0))

results = {
    "result_kind": "descriptive",
    "sample": {"n_observations": int(stage_quality), "unit": "source",
               "source": "data/gaia_dr3.csv, base quality cuts (data/gaia_clean.csv)"},
    "statistics": statistics,
    "distributions": {
        "parallax": {"variable": "parallax_mas", "n": n_members, "bins": plx_bins},
        "distance": {"variable": "distance_pc", "n": n_members, "bins": dist_bins},
    },
    "figures": FIGURES,
    "membership": {
        "seed_pm_mas_yr": [num(SEED[0]), num(SEED[1])],
        "pm_radius_mas_yr": R_BASE,
        "parallax_centre_mas": num(res["pi0"]),
        "parallax_sigma_mas": num(res["spi"]),
        "parallax_half_window_mas": num(res["half_window"]),
        "pm_centre_mas_yr": [num(res["pm0"][0]), num(res["pm0"][1])],
        "naive_full_sample_parallax_centre_mas": num(naive_plx),
        "stage_counts": {"quality": stage_quality, "parallax_window": stage_window,
                         "pm_radius": stage_pm},
        "parallax_mode_mas": num(mode_mas),
        "parallax_median_mas": num(median_plx),
        "parallax_mode_minus_median_mas": num(mode_mas - median_plx),
        "parallax_local_peaks": len(peaks),
        "parallax_median_se_mas": num(members["parallax"].std(ddof=1) / math.sqrt(n_members)),
        "grid_one_at_a_time_median_members": num(grid_median),
        "grid_max_change_share": num(max_change),
        "grid_base_within_10pct_of_median": bool(abs(base_n - grid_median) <= 0.1 * grid_median),
        "field_cmd_rows": int(len(field_cmd)),
    },
    "membership_grid": grid,
    "grid_full_cross": {
        "n_rows": len(cross),
        "n_members_min": int(cross_n.min()),
        "n_members_median": num(np.median(cross_n)),
        "n_members_max": int(cross_n.max()),
        "rows": cross,
    },
    "distance_summary": {
        "distance_pc_median": num(statistics["distance_pc"]["median"]),
        "distance_pc_p16": num(members["distance_pc"].quantile(0.16)),
        "distance_pc_p84": num(members["distance_pc"].quantile(0.84)),
        "distance_pc_iqr": num(members["distance_pc"].quantile(0.75) - members["distance_pc"].quantile(0.25)),
        "distance_modulus_median_mag": num(statistics["distance_modulus_mag"]["median"]),
        "note": "1000/parallax, uncorrected for the zero point; descriptive, not a model-based distance",
    },
    "main_sequence_locus": locus,
    "cmd_extremes": {
        "brightest_member_G": num(members["phot_g_mean_mag"].min()),
        "faintest_member_G": num(members["phot_g_mean_mag"].max()),
        "members_without_bp_rp": int(n_members - len(cm)),
    },
    "bright_end": {
        "brightest_member_G": num(brightest_g),
        "second_brightest_member_G": num(g_sorted[1]),
        "extract_stars_brighter_than_brightest_member": int(len(bright_raw)),
        "of_which_fail_quality_cuts": int((~bright_pass).sum()),
        "of_which_ruwe_at_least_1_4": int((bright_raw["ruwe"] >= 1.4).sum()),
        "note": ("No member is brighter than brightest_member_G. The counts are the extract's stars brighter "
                 "than that member, with how many fail each quality cut; the extract is limited to "
                 "parallax > 2 mas and parallax_over_error > 5"),
    },
}

with open(OUT, "w") as f:
    json.dump(results, f, indent=2, allow_nan=False)

print("wrote", OUT)
print("distance median pc:", round(statistics["distance_pc"]["median"], 2),
      "IQR", round(results["distance_summary"]["distance_pc_iqr"], 2))
print("parallax peaks:", len(peaks), "mode-median (mas):", round(mode_mas - median_plx, 3))
