"""
Replication script for: Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021
Paper ID: 66f43096-d973-4dc0-afaa-d086434dd927

Descriptive cross-sectional study. No regression, no effect, no causal parameter.
Data: WHO Global Health Observatory indicator RS_198 (estimated road traffic death
rate, deaths per 100,000 population), calendar year 2021, all locations.

Requirements: pandas, numpy, matplotlib
Usage: python estimation.py
Output: replication/output/ (tables as CSV, figure as PDF)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)

HERE = Path(__file__).resolve().parent
DATA_FILE = HERE.parent / "data" / "who_rs198_2021.csv"
OUTPUT_DIR = HERE / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REGION_CODES = {
    "Africa": "AFR",
    "Americas": "AMR",
    "South-East Asia": "SEAR",
    "Europe": "EUR",
    "Eastern Mediterranean": "EMR",
    "Western Pacific": "WPR",
}
REGION_ORDER = ["AFR", "AMR", "SEAR", "EUR", "EMR", "WPR"]
PLAUSIBLE_MIN, PLAUSIBLE_MAX = 0.0, 50.0


def describe(s):
    """N, mean, SD (ddof=1), min, quartiles, median, max; type-7 quantiles (numpy default)."""
    s = s.dropna()
    return pd.Series({
        "N": len(s),
        "mean": s.mean(),
        "sd": s.std(ddof=1),
        "min": s.min(),
        "p25": s.quantile(0.25),
        "median": s.median(),
        "p75": s.quantile(0.75),
        "max": s.max(),
    })


# ── 1. Load data ──────────────────────────────────────────────────────────────
# Raw GHO extract written by the data step (e2er-data who_gho, RS_198, 2021).
raw = pd.read_csv(DATA_FILE)
n_raw_rows = len(raw)

# ── 2. Variable construction ──────────────────────────────────────────────────
# Sample flow: keep country rows, drop duplicates (keep first), drop missing value.
flow = {"raw_rows": n_raw_rows}
countries = raw[raw["spatial_type"] == "COUNTRY"].copy()
flow["country_rows"] = len(countries)
flow["dropped_non_country_rows"] = n_raw_rows - len(countries)

dup_mask = countries["location"].duplicated(keep="first")
flow["duplicate_iso3_rows_dropped"] = int(dup_mask.sum())
countries = countries[~dup_mask]

missing = countries[countries["value"].isna()][["location", "parent_location"]]
flow["dropped_missing_value"] = len(missing)
flow["excluded_countries"] = ", ".join(missing["location"].tolist())
sample = countries.dropna(subset=["value"]).copy()
flow["final_N"] = len(sample)

sample = sample.rename(columns={"location": "iso3", "parent_location": "who_region_name"})
sample["who_region"] = sample["who_region_name"].map(REGION_CODES)
flow["unmapped_region_rows"] = int(sample["who_region"].isna().sum())
sample["value"] = sample["value"].astype(float)
v = sample["value"]

# Data-quality checks (plausibility flagged, not dropped)
out_of_range = sample[(v < PLAUSIBLE_MIN) | (v > PLAUSIBLE_MAX)][["iso3", "value"]]
flow["values_outside_0_50"] = len(out_of_range)

flow_df = pd.DataFrame([{"step": k, "value": v_} for k, v_ in flow.items()])
flow_df.to_csv(OUTPUT_DIR / "sample_flow.csv", index=False)  # Sample flow (Section 2, Data)

# ── 3. Summary statistics ─────────────────────────────────────────────────────
# Table 1: national distribution of the estimated death rate
table1 = describe(v).to_frame(name="death_rate").T
table1.to_csv(OUTPUT_DIR / "table1_summary.csv")  # Table 1: national distribution

# Sensitivity: distribution with and without the extreme tails
tails = pd.DataFrame({
    "statistic": ["p5", "p95", "trimmed_mean_5_95", "sd_trimmed_5_95"],
    "value": [
        v.quantile(0.05),
        v.quantile(0.95),
        v[(v >= v.quantile(0.05)) & (v <= v.quantile(0.95))].mean(),
        v[(v >= v.quantile(0.05)) & (v <= v.quantile(0.95))].std(ddof=1),
    ],
})
tails.to_csv(OUTPUT_DIR / "table_a1_tail_sensitivity.csv", index=False)  # Appendix: tail sensitivity

# ── 4. Main descriptive results ───────────────────────────────────────────────
# Table 2: summary by WHO region, with one-way variance partition (eta-squared)
by_region = []
for code in REGION_ORDER:
    sub = sample.loc[sample["who_region"] == code, "value"]
    if len(sub) == 0:
        continue
    row = describe(sub)
    row.name = code
    by_region.append(row)
table2 = pd.DataFrame(by_region)
table2.index.name = "who_region"
table2.to_csv(OUTPUT_DIR / "table2_by_who_region.csv")  # Table 2: summary by WHO region

grand_mean = v.mean()
ss_total = ((v - grand_mean) ** 2).sum()
ss_between = sum(
    len(g) * (g.mean() - grand_mean) ** 2
    for _, g in sample.groupby("who_region")["value"]
)
eta_sq = pd.DataFrame([{
    "ss_between": ss_between,
    "ss_total": ss_total,
    "eta_squared": ss_between / ss_total,
}])
eta_sq.to_csv(OUTPUT_DIR / "table2b_variance_partition.csv", index=False)  # Table 2 note: between-region share of variance

# Distribution bins for the histogram (Freedman-Diaconis, as in the results file)
edges = np.histogram_bin_edges(v.to_numpy(), bins="fd")
counts, _ = np.histogram(v.to_numpy(), bins=edges)
bins_df = pd.DataFrame({
    "lower": edges[:-1],
    "upper": edges[1:],
    "count": counts,
})
bins_df.to_csv(OUTPUT_DIR / "figure1_histogram_bins.csv", index=False)  # Figure 1: histogram bin counts

# Rankings: ten highest and ten lowest countries (ties broken by ISO3)
ranked = sample.sort_values(["value", "iso3"], ascending=[False, True])
cols = ["iso3", "who_region", "value"]
top10 = ranked.head(10)[cols].reset_index(drop=True)
bottom10 = ranked.sort_values(["value", "iso3"], ascending=[True, True]).head(10)[cols].reset_index(drop=True)
top10.to_csv(OUTPUT_DIR / "table3_top10_highest.csv", index_label="rank")  # Table 3a: ten highest rates
bottom10.to_csv(OUTPUT_DIR / "table3_bottom10_lowest.csv", index_label="rank")  # Table 3b: ten lowest rates

# Uncertainty bounds: the GHO extract carries no low/high values, so no association is computed
assoc = pd.DataFrame([{
    "statistic": "spearman_rho_value_vs_interval_width",
    "estimate": np.nan,
    "N": int(sample[["low", "high"]].dropna().shape[0]),
    "note": "Not computed: GHO low/high bounds absent in the extract",
}])
assoc.to_csv(OUTPUT_DIR / "table4_uncertainty_association.csv", index=False)  # Section 4: uncertainty association (null)

# ── 5. Robustness checks ──────────────────────────────────────────────────────
# Region counts and shares by region (sample composition)
composition = sample["who_region"].value_counts().reindex(REGION_ORDER).rename("countries").to_frame()
composition["share"] = composition["countries"] / composition["countries"].sum()
composition.to_csv(OUTPUT_DIR / "table_a2_region_composition.csv")  # Appendix: countries per region

# Median-based regional comparison (robust to tails)
robust_region = sample.groupby("who_region")["value"].median().reindex(REGION_ORDER).rename("median").to_frame()
robust_region.to_csv(OUTPUT_DIR / "table_a3_regional_medians.csv")  # Appendix: regional medians

# ── 6. Export results ─────────────────────────────────────────────────────────
# Figure 1: national distribution of the estimated road traffic death rate
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(v.to_numpy(), bins=edges, color="#4C72B0", edgecolor="white")
ax.set_xlabel("Estimated road traffic death rate (deaths per 100,000 population)")
ax.set_ylabel("Countries")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig_death_rate_hist.pdf")  # Figure 1: national distribution histogram
plt.close(fig)

print(f"Analysed countries: {len(sample)}")
print(table1.round(2).to_string())
print(table2.round(2).to_string())
print(f"Eta-squared (WHO region): {eta_sq['eta_squared'].iloc[0]:.3f}")
