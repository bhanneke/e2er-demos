import sqlite3, json
import pandas as pd, numpy as np

con = sqlite3.connect("data.db")
raw = pd.read_sql("SELECT * FROM frankfurt_t2m_monthly", con)
n_raw = len(raw)
n13 = int((raw.month == 13).sum())
df = raw[raw.month.between(1, 12)].copy()
n_fill = int((df.T2M == -999).sum())
df.loc[df.T2M == -999, "T2M"] = np.nan
n_null = int(df.T2M.isna().sum())
assert df.date.is_unique
exp = pd.period_range("1981-01", "2025-12", freq="M").astype(str)
gaps = len(set(exp) - set(df.date))
df = df.sort_values("date").reset_index(drop=True)
df = df[["date", "year", "month", "T2M"]]
clim = df[df.year <= 2010].groupby("month").T2M.mean()
clim_sd = df[df.year <= 2010].groupby("month").T2M.std()
df["clim_1981_2010"] = df.month.map(clim)
df["anomaly"] = df.T2M - df.clim_1981_2010
df["split"] = np.where(df.date <= "2022-12", "train", "holdout")
df.to_sql("frankfurt_t2m_clean", con, if_exists="replace", index=False)
ann = df.groupby("year").agg(T2M=("T2M", "mean"), n_months=("T2M", "count")).reset_index()
ann["split"] = np.where(ann.year <= 2022, "train", "holdout")
ann.to_sql("frankfurt_t2m_annual", con, if_exists="replace", index=False)
con.commit()
tr = df[df.split == "train"]


def desc(s):
    d = {"mean": s.mean(), "sd": s.std(), "min": s.min(), "p25": s.quantile(.25),
         "median": s.median(), "p75": s.quantile(.75), "max": s.max()}
    return {k: round(float(v), 4) for k, v in d.items()}


names = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
clim_tr = tr.groupby("month").T2M.mean()
sd_tr = tr.groupby("month").T2M.std()
dec = {}
for a in range(1981, 2021, 10):
    dec["%d_%d" % (a, a + 9)] = round(float(ann[ann.year.between(a, a + 9)].T2M.mean()), 4)
dec["2021_2025"] = round(float(ann[ann.year >= 2021].T2M.mean()), 4)
ho = df[df.split == "holdout"]
stats = {
    "n_observations": len(df), "n_units": 1,
    "time_coverage": {"start_iso": "1981-01", "end_iso": "2025-12", "n_periods": len(df)},
    "outcome": {"T2M": desc(df.T2M)},
    "outcome_train": {"T2M": desc(tr.T2M), "n": len(tr)},
    "outcome_holdout": {"T2M": desc(ho.T2M), "n": len(ho)},
    "anomaly_train": desc(tr.anomaly),
    "anomaly_full": desc(df.anomaly),
    "split": {"n_train": len(tr), "n_holdout": len(ho)},
    "sample_flow": [
        {"step": "raw rows in frankfurt_t2m_monthly (1981-2025)", "n": n_raw, "dropped": 0},
        {"step": "drop month-13 annual-mean rows", "n": len(df), "dropped": n_raw - len(df)},
        {"step": "drop fill value -999 / missing T2M", "n": int(df.T2M.notna().sum()), "dropped": n_fill + n_null},
        {"step": "final sample (540 months; 504 train, 36 hold-out)", "n": len(df), "dropped": 0}],
    "completeness": {"n_month13_rows": n13, "n_fill_999": n_fill, "n_missing_T2M": n_null,
                     "n_calendar_gaps": gaps, "n_years": int(ann.shape[0]),
                     "n_incomplete_years": int((ann.n_months < 12).sum()),
                     "missing_pct": 100 * n_null / len(df)},
    "climatology_1981_2010": {n: round(float(clim[i + 1]), 4) for i, n in enumerate(names)},
    "climatology_train_1981_2022": {
        "mean": {n: round(float(clim_tr[i + 1]), 4) for i, n in enumerate(names)},
        "sd": {n: round(float(sd_tr[i + 1]), 4) for i, n in enumerate(names)}},
    "annual_means": {"train": desc(ann[ann.split == "train"].T2M),
                     "by_year": {str(r.year): round(float(r.T2M), 4) for r in ann.itertuples()}},
    "decade_means": dec,
    "mean_2013_2022_minus_mean_1981_1990": round(float(
        ann[ann.year.between(2013, 2022)].T2M.mean() - ann[ann.year.between(1981, 1990)].T2M.mean()), 4),
}
json.dump(stats, open("summary_statistics.json", "w"), indent=1)

d = df
fig = {"figures": [
    {"filename": "fig_monthly_t2m.pdf", "figure_type": "time_series", "label": "fig:monthly_t2m",
     "caption_hint": "Monthly mean 2 m air temperature, Frankfurt grid cell, 1981-2025; hold-out 2023-2025 shaded",
     "series": [{"label": "Monthly mean T2M", "x": d.date.tolist(), "y": [float(v) for v in d.T2M],
                 "source": {"table": "frankfurt_t2m_clean", "columns": {"x": "date", "y": "T2M"}}}],
     "shaded_regions": [{"x_start": "2023-01", "x_end": "2025-12", "label": "Hold-out (2023-2025)"}],
     "x_label": "Month", "y_label": "Temperature (degrees C)"},
    {"filename": "fig_seasonal_profile.pdf", "figure_type": "bar", "label": "fig:seasonal_profile",
     "caption_hint": "Monthly climatology 1981-2010 (mean T2M by calendar month, bars +-1 SD across years)",
     "categories": [n.capitalize() for n in names],
     "values": [round(float(clim[i + 1]), 4) for i in range(12)],
     "errors": [round(float(clim_sd[i + 1]), 4) for i in range(12)],
     "y_label": "Mean temperature (degrees C)"},
    {"filename": "fig_annual_means.pdf", "figure_type": "time_series", "label": "fig:annual_means",
     "caption_hint": "Annual mean T2M computed from monthly values, 1981-2025; 2023-2025 are hold-out years",
     "series": [{"label": "Annual mean T2M", "x": [int(y) for y in ann.year], "y": [float(v) for v in ann.T2M],
                 "source": {"table": "frankfurt_t2m_annual", "columns": {"x": "year", "y": "T2M"}}}],
     "shaded_regions": [{"x_start": 2023, "x_end": 2025, "label": "Hold-out years"}],
     "x_label": "Year", "y_label": "Annual mean temperature (degrees C)"},
    {"filename": "fig_anomalies.pdf", "figure_type": "time_series", "label": "fig:anomalies",
     "caption_hint": "Monthly anomalies relative to the 1981-2010 calendar-month climatology",
     "series": [{"label": "Anomaly vs 1981-2010", "x": d.date.tolist(), "y": [float(v) for v in d.anomaly],
                 "source": {"table": "frankfurt_t2m_clean", "columns": {"x": "date", "y": "anomaly"}}}],
     "shaded_regions": [{"x_start": "2023-01", "x_end": "2025-12", "label": "Hold-out (2023-2025)"}],
     "x_label": "Month", "y_label": "Anomaly (degrees C)"}]}
json.dump(fig, open("figure_spec.json", "w"))
for k in ["completeness", "outcome", "outcome_train", "decade_means", "sample_flow",
          "mean_2013_2022_minus_mean_1981_1990", "climatology_1981_2010"]:
    print(k, json.dumps(stats[k]))
