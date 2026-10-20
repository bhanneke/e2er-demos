"""Data check, quality cuts and descriptive sample summary for the Gaia DR3 Pleiades extract.

Reads data/gaia_dr3.csv (the raw extract, 14,066 rows, pulled 2026-10-13),
runs the data check (units, duplicate source_id, missing values per column),
applies the base quality cuts, writes data/gaia_clean.csv and writes the
count log and descriptive ranges to summary_statistics.json.
No membership fit, no regression, no test statistic is computed here.
"""
import json
import numpy as np
import pandas as pd

RAW = "data/gaia_dr3.csv"
CLEAN = "data/gaia_clean.csv"
OUT = "summary_statistics.json"

df = pd.read_csv(RAW)
n_raw = len(df)
print(f"raw rows: {n_raw}")

# ---- data check -------------------------------------------------------------
print("\n== dtypes ==")
print(df.dtypes.to_string())

n_dup = int(df["source_id"].duplicated().sum())
print(f"\nduplicate source_id rows: {n_dup}")

missing = df.isna().sum()
print("\n== missing values per column ==")
print(pd.DataFrame({"n_missing": missing, "share": (missing / n_raw).round(4)}).to_string())

# unit / range checks against the extract's own pre-filter
print("\n== range checks ==")
print(f"min parallax: {df['parallax'].min():.4f} mas (extract requires > 2)")
print(f"min parallax_over_error: {df['parallax_over_error'].min():.3f} (extract requires > 5)")
print(f"dist_deg max: {df['dist_deg'].max():.4f} deg (cone radius 3)")
print("astrometric_params_solved counts:")
print(df["astrometric_params_solved"].value_counts(dropna=False).to_string())

# ---- cuts, each logged ------------------------------------------------------
flow = [{"step": "raw extract (gaia_dr3, pulled 2026-10-13)", "n": n_raw, "dropped": 0}]
d = df.drop_duplicates(subset="source_id")
flow.append({"step": "drop duplicate source_id", "n": len(d), "dropped": n_raw - len(d)})

n_prev = len(d)
d = d[d["astrometric_params_solved"].isin([31, 95])]
d = d.dropna(subset=["parallax", "pmra", "pmdec"])
flow.append({"step": "5- or 6-parameter solution (31, 95) and non-null parallax and proper motion",
             "n": len(d), "dropped": n_prev - len(d)})

n_prev = len(d)
d = d[d["ruwe"] < 1.4]
flow.append({"step": "ruwe < 1.4", "n": len(d), "dropped": n_prev - len(d)})

n_prev = len(d)
d = d[d["parallax_over_error"] > 10]
flow.append({"step": "parallax_over_error > 10 (final quality sample)", "n": len(d), "dropped": n_prev - len(d)})

d = d.copy()
d.to_csv(CLEAN, index=False)
print(f"\nwrote {CLEAN} with {len(d)} rows")

print("\n== count log ==")
for s in flow:
    print(f"{s['n']:>8}  dropped {s['dropped']:>8}  {s['step']}")

# ---- descriptive ranges (no inference) --------------------------------------
def q(x):
    x = pd.Series(x).dropna()
    return {
        "min": float(x.min()), "p25": float(x.quantile(0.25)), "median": float(x.median()),
        "p75": float(x.quantile(0.75)), "max": float(x.max()), "n": int(x.size),
    }

cmd = d.dropna(subset=["bp_rp", "phot_g_mean_mag"])
ranges = {
    "parallax_mas": q(d["parallax"]),
    "pmra_mas_yr": q(d["pmra"]),
    "pmdec_mas_yr": q(d["pmdec"]),
    "phot_g_mean_mag": q(d["phot_g_mean_mag"]),
    "bp_rp": q(cmd["bp_rp"]),
    "ruwe": q(d["ruwe"]),
    "parallax_over_error": q(d["parallax_over_error"]),
}
for k, v in ranges.items():
    print(k, {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()})

n_no_bprp = int(len(d) - len(cmd))
missing_clean = {c: int(d[c].isna().sum()) for c in d.columns}

summary = {
    "n_observations": int(len(d)),
    "n_units": int(d["source_id"].nunique()),
    "time_coverage": {"start_iso": None, "end_iso": None, "n_periods": None},
    "sample_flow": flow,
    "raw_rows": n_raw,
    "duplicate_source_id_rows": n_dup,
    "missing_values_raw": {c: int(v) for c, v in missing.items()},
    "missing_values_clean": missing_clean,
    "rows_without_bp_rp_in_clean_sample": n_no_bprp,
    "cmd_rows_with_bp_rp": int(len(cmd)),
    "ranges": ranges,
    "outcome": {
        "mean": None, "sd": None, "min": None, "p25": None, "median": None, "p75": None, "max": None,
    },
}
with open(OUT, "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nwrote {OUT}")
