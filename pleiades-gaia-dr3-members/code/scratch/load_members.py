"""Re-load the quality sample and the members into data.db for the members' CMD.

Reads the gaia_dr3 table from data.db, applies the base quality cut, and writes
two tables: gaia_clean (the quality sample, with cmd_group = 'Member' or
'Field') and pleiades_members (the members with bp_rp, phot_g_mean_mag,
parallax, pmra, pmdec). The membership functions below are copied unchanged
from run_estimation.py; the selection, the seed and the grid are not changed.
Checks the counts against estimation_results.json and writes a members block
to summary_statistics.json. No new estimate is computed.
"""
import json
import sqlite3

import numpy as np
import pandas as pd

DB = "data.db"
CLEAN_CSV = "data/gaia_clean.csv"
RESULTS = "estimation_results.json"
SUMMARY = "summary_statistics.json"
R_BASE = 5.0
SEED_BAND = (5.0, 10.0)


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


conn = sqlite3.connect(DB)
raw = pd.read_sql_query("SELECT * FROM gaia_dr3", conn)
base = quality(raw).sort_values("source_id").reset_index(drop=True)
print("quality sample from data.db:", len(base))

csv_ids = pd.read_csv(CLEAN_CSV, usecols=["source_id"])["source_id"]
assert set(base["source_id"]) == set(csv_ids), "quality sample differs from data/gaia_clean.csv"

seed = pm_seed(base)
res = membership(base, seed)
mem = res["members"]
n_members = int(mem.sum())
print("seed:", seed, "members:", n_members, "pi0:", round(res["pi0"], 4), "pm0:", np.round(res["pm0"], 3))

with open(RESULTS) as fh:
    expected = json.load(fh)
assert n_members == expected["membership"]["stage_counts"]["pm_radius"], "member count differs"
assert abs(res["pi0"] - expected["membership"]["parallax_centre_mas"]) < 1e-9, "parallax centre differs"

base["cmd_group"] = np.where(mem, "Member", "Field")
gaia_clean = base.copy()
gaia_clean.to_sql("gaia_clean", conn, if_exists="replace", index=False)

members = base.loc[mem, ["source_id", "bp_rp", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]]
members.to_sql("pleiades_members", conn, if_exists="replace", index=False)

n_clean = int(conn.execute("SELECT COUNT(*) FROM gaia_clean").fetchone()[0])
n_mem_tab = int(conn.execute("SELECT COUNT(*) FROM pleiades_members").fetchone()[0])
cmd_mem = int(conn.execute(
    "SELECT COUNT(*) FROM gaia_clean WHERE cmd_group = 'Member' AND bp_rp IS NOT NULL "
    "AND phot_g_mean_mag IS NOT NULL").fetchone()[0])
cmd_field = int(conn.execute(
    "SELECT COUNT(*) FROM gaia_clean WHERE cmd_group = 'Field' AND bp_rp IS NOT NULL "
    "AND phot_g_mean_mag IS NOT NULL").fetchone()[0])
g_min, g_max = conn.execute(
    "SELECT MIN(phot_g_mean_mag), MAX(phot_g_mean_mag) FROM pleiades_members").fetchone()
bprp_min, bprp_max = conn.execute(
    "SELECT MIN(bp_rp), MAX(bp_rp) FROM pleiades_members WHERE bp_rp IS NOT NULL").fetchone()
conn.commit()
conn.close()

assert n_clean == len(base) and n_mem_tab == n_members
print(f"gaia_clean rows: {n_clean}; pleiades_members rows: {n_mem_tab}")
print(f"CMD rows: members {cmd_mem}, field {cmd_field}, total {cmd_mem + cmd_field}")
print(f"members G range: {g_min:.4f} to {g_max:.4f}; bp_rp range: {bprp_min:.4f} to {bprp_max:.4f}")

with open(SUMMARY) as fh:
    summary = json.load(fh)
summary["members"] = {
    "n_members": n_members,
    "n_quality": int(len(base)),
    "gaia_clean_rows": n_clean,
    "pleiades_members_rows": n_mem_tab,
    "cmd_rows_members": cmd_mem,
    "cmd_rows_field": cmd_field,
    "cmd_rows_total": cmd_mem + cmd_field,
    "members_without_bp_rp": int(n_members - base.loc[mem, "bp_rp"].notna().sum()),
    "phot_g_min": float(g_min),
    "phot_g_max": float(g_max),
    "bp_rp_min": float(bprp_min),
    "bp_rp_max": float(bprp_max),
    "parallax_centre_mas": float(res["pi0"]),
    "pm_centre_mas_yr": [float(res["pm0"][0]), float(res["pm0"][1])],
}
with open(SUMMARY, "w") as fh:
    json.dump(summary, fh, indent=2, allow_nan=False)
print("wrote members block to", SUMMARY)
