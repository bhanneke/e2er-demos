import json
import math
import os
import subprocess

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "estimation_results.json")
REGION_ORDER = ["AFR", "AMR", "SEAR", "EUR", "EMR", "WPR"]


def query(sql):
    res = subprocess.run(
        ["e2er-data", "query", "sql", sql],
        capture_output=True, text=True, check=True,
    )
    payload = json.loads(res.stdout)
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return pd.DataFrame(payload["rows"], columns=payload["columns"])


def clean(x):
    if x is None:
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if math.isnan(x) else float(x)
    return x


def describe(s):
    s = s.dropna()
    n = len(s)
    out = {
        "n": int(n),
        "mean": clean(s.mean()) if n else None,
        "sd": clean(s.std(ddof=1)) if n > 1 else None,
        "min": clean(s.min()) if n else None,
        "p5": clean(s.quantile(0.05)) if n else None,
        "p25": clean(s.quantile(0.25)) if n else None,
        "median": clean(s.median()) if n else None,
        "p75": clean(s.quantile(0.75)) if n else None,
        "p95": clean(s.quantile(0.95)) if n else None,
        "max": clean(s.max()) if n else None,
    }
    return out


# ---- sample flow -------------------------------------------------------
raw_by_type = query(
    "SELECT spatial_type, COUNT(*) AS n, COUNT(value) AS n_value "
    "FROM who_rs198_2021 GROUP BY spatial_type"
)
raw_countries = query(
    "SELECT COUNT(*) AS n, COUNT(value) AS n_value, COUNT(DISTINCT location) AS n_loc "
    "FROM who_rs198_2021 WHERE spatial_type = 'COUNTRY'"
)
missing_countries = query(
    "SELECT location, value_text FROM who_rs198_2021 "
    "WHERE spatial_type = 'COUNTRY' AND value IS NULL ORDER BY location"
)
clean_df = query(
    "SELECT iso3, country_name, who_region_name, who_region, value, low, high "
    "FROM who_rs198_2021_clean ORDER BY iso3"
)
mismatch = query(
    "SELECT COUNT(*) AS n FROM who_rs198_2021_clean c "
    "JOIN who_rs198_2021 r ON r.location = c.iso3 AND r.spatial_type = 'COUNTRY' "
    "WHERE c.value <> r.value OR (c.value IS NULL) <> (r.value IS NULL)"
)

n_raw_countries = int(raw_countries["n"].iloc[0])
n_raw_valued = int(raw_countries["n_value"].iloc[0])
n_clean = len(clean_df)

duplicates = int(clean_df["iso3"].duplicated().sum())
unmapped = int(clean_df["who_region"].isna().sum())
out_of_range = clean_df[(clean_df["value"] < 0) | (clean_df["value"] > 50)]
value_mismatch = int(mismatch["n"].iloc[0])

sample_flow = {
    "raw_rows_all_spatial_types": int(raw_by_type["n"].sum()),
    "raw_country_rows": n_raw_countries,
    "dropped_no_value": n_raw_countries - n_raw_valued,
    "countries_with_value": n_raw_valued,
    "dropped_not_in_clean_table": n_raw_valued - n_clean,
    "final_n": n_clean,
    "excluded_countries": missing_countries.to_dict(orient="records"),
    "duplicate_iso3_rows": duplicates,
    "unmapped_who_region": unmapped,
    "values_outside_0_50": out_of_range[["iso3", "value"]].to_dict(orient="records"),
    "clean_vs_raw_value_mismatches": value_mismatch,
}

# ---- national distribution --------------------------------------------
v = clean_df["value"]
national = describe(v)

# ---- by WHO region -----------------------------------------------------
grand_mean = v.mean()
ss_total = float(((v - grand_mean) ** 2).sum())
group_rows = []
ss_between = 0.0
for code in REGION_ORDER:
    sub = clean_df.loc[clean_df["who_region"] == code, "value"]
    if len(sub) == 0:
        continue
    ss_between += len(sub) * (sub.mean() - grand_mean) ** 2
    name = clean_df.loc[clean_df["who_region"] == code, "who_region_name"].iloc[0]
    row = {"group": code, "group_name": name}
    row.update(describe(sub))
    group_rows.append(row)
between_share = float(ss_between / ss_total) if ss_total > 0 else None

# ---- distribution bins and region counts -------------------------------
edges = np.histogram_bin_edges(v.to_numpy(), bins="fd")
counts, _ = np.histogram(v.to_numpy(), bins=edges)
bins = [
    {"lower": float(edges[i]), "upper": float(edges[i + 1]), "count": int(counts[i])}
    for i in range(len(counts))
]
assert sum(b["count"] for b in bins) == national["n"]

region_counts = [
    {"category": r["group"], "count": r["n"]} for r in group_rows
]

# ---- rankings ----------------------------------------------------------
ranked = clean_df.sort_values(["value", "iso3"], ascending=[False, True])
cols = ["iso3", "country_name", "who_region", "value"]
top10 = ranked.head(10)[cols].to_dict(orient="records")
bottom10 = ranked.sort_values(["value", "iso3"], ascending=[True, True]).head(10)[cols].to_dict(orient="records")
tie_at_top_cut = int((v == top10[-1]["value"]).sum())
tie_at_bottom_cut = int((v == bottom10[-1]["value"]).sum())

# ---- association: point estimate vs uncertainty width ------------------
bounds = clean_df.dropna(subset=["low", "high"]).copy()
if len(bounds) >= 3:
    bounds["low"] = bounds["low"].astype(float)
    bounds["high"] = bounds["high"].astype(float)
    bounds["width"] = bounds["high"] - bounds["low"]
    rho = clean(bounds[["value", "width"]].corr(method="spearman").iloc[0, 1])
    assoc_n = len(bounds)
    assoc_note = "Spearman rank correlation between point estimate and GHO interval width"
else:
    rho = None
    assoc_n = len(bounds)
    assoc_note = (
        "Not computed: the GHO low and high bounds are absent for all "
        f"{n_clean} analysed countries in the warehouse extract"
    )

results = {
    "result_kind": "descriptive",
    "sample": {
        "n_observations": n_clean,
        "unit": "country",
        "year": 2021,
        "source": "who_rs198_2021_clean (GHO RS_198, derived from who_rs198_2021)",
        "flow": sample_flow,
    },
    "statistics": {
        "death_rate": dict(
            describe(v),
            unit="deaths per 100,000 population",
            indicator="RS_198",
        ),
    },
    "distributions": {
        "death_rate": {
            "variable": "death_rate",
            "n": national["n"],
            "bins": bins,
        },
        "who_region": {
            "variable": "who_region",
            "n": n_clean,
            "categories": region_counts,
        },
    },
    "groups": {
        "death_rate_by_who_region": {
            "variable": "death_rate",
            "by": "who_region",
            "groups": group_rows,
        },
    },
    "variance_decomposition": {
        "variable": "death_rate",
        "by": "who_region",
        "between_region_share": between_share,
        "ss_between": clean(ss_between),
        "ss_total": clean(ss_total),
        "note": "Share of the total sum of squares explained by WHO region membership; a description, not a test",
    },
    "rankings": {
        "top10_highest": top10,
        "bottom10_lowest": bottom10,
        "ties_at_top_cutoff": tie_at_top_cut,
        "ties_at_bottom_cutoff": tie_at_bottom_cut,
    },
    "associations": {
        "rate_vs_uncertainty_width": {
            "x": "death_rate",
            "y": "uncertainty_width",
            "method": "spearman",
            "estimate": rho,
            "n": assoc_n,
            "note": assoc_note,
        },
    },
    "figures": ["fig_death_rate_hist.pdf"],
}


def scrub(obj):
    if isinstance(obj, dict):
        return {k: scrub(x) for k, x in obj.items()}
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return None if math.isnan(obj) else float(obj)
    return obj


with open(OUT, "w") as fh:
    json.dump(scrub(results), fh, indent=2, allow_nan=False)

# ---- figure spec: histogram drawn from the same bins the results report ---
FIG_OUT = os.path.join(HERE, "figure_spec.json")
figure_spec = {
    "figures": [
        {
            "filename": "fig_death_rate_hist.pdf",
            "figure_type": "histogram",
            "label": "fig:death_rate_hist",
            "caption_hint": "Distribution of the estimated road traffic death rate across countries, 2021 (WHO GHO RS_198)",
            "bins": bins,
            "x_label": "Estimated road traffic death rate (deaths per 100,000 population)",
            "y_label": "Countries",
            "source": {"results": "distributions.death_rate.bins"},
        }
    ]
}
with open(FIG_OUT, "w") as fh:
    json.dump(scrub(figure_spec), fh, indent=2, allow_nan=False)

print(json.dumps(scrub({
    "n": national["n"],
    "mean": national["mean"],
    "median": national["median"],
    "sd": national["sd"],
    "min": national["min"],
    "max": national["max"],
    "p25": national["p25"],
    "p75": national["p75"],
    "between_region_share": between_share,
    "sample_flow": sample_flow,
    "top10": [r["country_name"] for r in top10],
    "bottom10": [r["country_name"] for r in bottom10],
    "rho": rho,
}), indent=2))
