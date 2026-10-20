"""Data preparation for the Pleiades Gaia DR3 extract.

Loads the gaia_dr3 table from data.db, applies the base-specification cleaning
steps in order, logs each row count, and writes the clean CSV, the step log and
the sidecar summary_statistics.json. No membership, CMD or test is computed here.
"""
import json
import sqlite3

import numpy as np
import pandas as pd

DB = "data.db"
RAW_TABLE = "gaia_dr3"
CLEAN_CSV = "data/gaia_clean.csv"
STEP_LOG = "data/gaia_clean_steps.json"
SUMMARY = "summary_statistics.json"

RUWE_MAX = 1.4
POE_MIN = 10.0
ASTROMETRIC_OK = [31, 95]

conn = sqlite3.connect(DB)
df = pd.read_sql_query(f"SELECT * FROM {RAW_TABLE}", conn)
conn.close()

steps = []


def log(step, frame, dropped_by=None):
    n = len(frame)
    prev = steps[-1]["n"] if steps else n
    steps.append({"step": step, "n": int(n), "dropped": int(prev - n)})


raw_n = len(df)
log("raw extract (gaia_dr3, pulled 2026-10-13)", df)

# Step 1: duplicate source_id
dup_n = int(df["source_id"].duplicated().sum())
df = df.drop_duplicates(subset="source_id", keep="first")
log("drop duplicate source_id", df)

# Step 2: astrometric solution and non-null parallax and proper motion
needed = ["parallax", "pmra", "pmdec"]
df = df[df["astrometric_params_solved"].isin(ASTROMETRIC_OK)]
df = df.dropna(subset=needed)
log("5- or 6-parameter solution (31, 95) and non-null parallax and proper motion", df)

# Step 3: RUWE
df = df[df["ruwe"] < RUWE_MAX]
log("ruwe < 1.4", df)

# Step 4: parallax over error
df = df[df["parallax_over_error"] > POE_MIN]
log("parallax_over_error > 10 (final quality sample)", df)

clean = df.reset_index(drop=True)
clean.to_csv(CLEAN_CSV, index=False)

with open(STEP_LOG, "w") as fh:
    json.dump({"steps": steps, "raw_rows": raw_n, "duplicate_source_id_rows": dup_n}, fh, indent=2)

# Missingness: raw and clean, not filled
cols = list(df.columns)
raw_missing = {c: int(pd.read_sql_query(
    f"SELECT COUNT(*) AS n FROM {RAW_TABLE} WHERE {c} IS NULL", sqlite3.connect(DB))["n"][0])
    for c in cols}
clean_missing = {c: int(clean[c].isna().sum()) for c in cols}


def desc(s):
    s = s.dropna()
    return {
        "min": float(s.min()), "p25": float(s.quantile(0.25)),
        "median": float(s.median()), "p75": float(s.quantile(0.75)),
        "max": float(s.max()), "n": int(s.size),
    }


ranges = {
    "parallax_mas": desc(clean["parallax"]),
    "pmra_mas_yr": desc(clean["pmra"]),
    "pmdec_mas_yr": desc(clean["pmdec"]),
    "phot_g_mean_mag": desc(clean["phot_g_mean_mag"]),
    "bp_rp": desc(clean["bp_rp"]),
    "ruwe": desc(clean["ruwe"]),
    "parallax_over_error": desc(clean["parallax_over_error"]),
}

summary = {
    "n_observations": int(len(clean)),
    "n_units": int(clean["source_id"].nunique()),
    "time_coverage": {"start_iso": None, "end_iso": None, "n_periods": None},
    "sample_flow": steps,
    "raw_rows": int(raw_n),
    "duplicate_source_id_rows": dup_n,
    "missing_values_raw": raw_missing,
    "missing_values_clean": clean_missing,
    "rows_without_bp_rp_in_clean_sample": int(clean["bp_rp"].isna().sum()),
    "cmd_rows_with_bp_rp": int(clean["bp_rp"].notna().sum()),
    "ranges": ranges,
    "astrometric_params_solved_counts": {str(int(k)): int(v) for k, v in
                                         clean["astrometric_params_solved"].value_counts().items()},
    "outcome": {"mean": None, "sd": None, "min": None, "p25": None,
                "median": None, "p75": None, "max": None},
}

with open(SUMMARY, "w") as fh:
    json.dump(summary, fh, indent=2)

print(json.dumps({"steps": steps, "clean_rows": len(clean),
                  "rows_without_bp_rp": summary["rows_without_bp_rp_in_clean_sample"]}, indent=2))
