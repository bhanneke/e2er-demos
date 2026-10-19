"""Clean the ComCat raw tables, build derived tables, write summary_statistics.json and figure_spec.json.
Descriptive only: counts, shares, means. No b-values, Mc, trends or tests."""
import json, sqlite3
import numpy as np, pandas as pd

con = sqlite3.connect("data.db")
RAW = ["usgs_raw_1976_1985", "usgs_raw_1986_1995", "usgs_raw_1996_2005", "usgs_raw_2006_2015", "usgs_raw_2016_2025"]
raw = {t: pd.read_sql(f"SELECT * FROM {t}", con) for t in RAW}
rows_raw = {t: len(d) for t, d in raw.items()}
df = pd.concat(raw.values(), ignore_index=True)
n_raw = len(df)
flow = [{"step": "raw rows (5 tables, M>=4.5)", "n": n_raw, "dropped": 0}]

def step(label, d, prev):
    flow.append({"step": label, "n": int(len(d)), "dropped": int(prev - len(d))})
    return d

df["t"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
df["year"] = df["t"].dt.year
df["decade"] = ((df["year"] - 1976) // 10).map(lambda k: f"{1976+10*k}-{1985+10*k}")

type_by_dec = df.groupby(["decade", "type"]).size().unstack(fill_value=0)
type_tot = df["type"].value_counts(dropna=False)

dups_id = int(df.duplicated("id").sum())
n0 = len(df); df = df.drop_duplicates("id"); df = step("drop repeated ids", df, n0)
n0 = len(df); df = df[df["type"] == "earthquake"]; df = step("keep type == 'earthquake'", df, n0)
null_mag = int(df["mag"].isna().sum())
n0 = len(df); df = df[df["mag"].notna() & (df["mag"] >= 4.5)]; df = step("drop null mag / mag < 4.5", df, n0)
n0 = len(df); df = df[(df["year"] >= 1976) & (df["year"] <= 2025)]; df = step("origin time within 1976-2025", df, n0)

# missing values before filling anything
miss = {c: int(df[c].isna().sum()) for c in ["time", "latitude", "longitude", "depth", "mag", "magType", "net"]}
df["magType"] = df["magType"].str.lower()
MW = {"mw", "mww", "mwc", "mwb", "mwr", "mwp", "mwr"}
def cls(m):
    if m is None or (isinstance(m, float) and np.isnan(m)): return "missing"
    if m in MW: return "mw_family"
    if m in ("mb", "mb_lg"): return "mb"
    if m == "ms" or m.startswith("ms"): return "ms"
    if m in ("ml", "md"): return "ml_md"
    return "other"
df["mag_class"] = df["magType"].map(cls)
df = df.sort_values("t").reset_index(drop=True)

# ranges
rng = {"lat_out": int(((df.latitude < -90) | (df.latitude > 90)).sum()),
       "lon_out": int(((df.longitude < -180) | (df.longitude > 180)).sum()),
       "depth_out_of_[-5,800]": int(((df.depth < -5) | (df.depth > 800)).sum()),
       "depth_negative": int((df.depth < 0).sum()),
       "mag_gt_10": int((df.mag > 10).sum())}

# near duplicates: within 16 s, 100 km, 0.5 mag (flag only)
tt = df["t"].astype("int64").to_numpy() / 1e9
lat = np.radians(df.latitude.to_numpy()); lon = np.radians(df.longitude.to_numpy()); mg = df.mag.to_numpy()
pairs = []
for i in range(len(df)):
    j = i + 1
    while j < len(df) and tt[j] - tt[i] <= 16:
        d = 6371 * np.arccos(np.clip(np.sin(lat[i]) * np.sin(lat[j]) + np.cos(lat[i]) * np.cos(lat[j]) * np.cos(lon[i] - lon[j]), -1, 1))
        if d <= 100 and abs(mg[i] - mg[j]) <= 0.5:
            pairs.append((df.net[i], df.net[j]))
        j += 1
pair_ct = pd.Series(["-".join(sorted(map(str, p))) for p in pairs]).value_counts().to_dict() if pairs else {}

# derived table: clean
out = df[["id", "time", "year", "latitude", "longitude", "depth", "mag", "magType", "mag_class", "net", "type", "status"]].copy()
out.to_sql("eq_clean_m45", con, if_exists="replace", index=False)

# annual counts
yrs = pd.DataFrame({"year": range(1976, 2026)})
def cnt(mask): return df[mask].groupby("year").size().reindex(yrs.year, fill_value=0).to_numpy()
a = yrs.copy()
a["n_m45"] = cnt(df.mag >= 4.5); a["n_m50"] = cnt(df.mag >= 5.0 - 1e-9); a["n_m55"] = cnt(df.mag >= 5.5 - 1e-9)
a["n_m60"] = cnt(df.mag >= 6.0 - 1e-9); a["n_m70"] = cnt(df.mag >= 7.0 - 1e-9)
m5 = df.mag >= 5.0 - 1e-9
a["n_m50_mw"] = cnt(m5 & (df.mag_class == "mw_family")); a["n_m50_mb"] = cnt(m5 & (df.mag_class == "mb"))
a["n_m50_ms"] = cnt(m5 & (df.mag_class == "ms"))
a["n_m50_other"] = a["n_m50"] - a["n_m50_mw"] - a["n_m50_mb"] - a["n_m50_ms"]
a["n_m50_shallow"] = cnt(m5 & (df.depth <= 70))
a["max_mag"] = df.groupby("year").mag.max().reindex(yrs.year).to_numpy()
a.to_sql("eq_annual_counts", con, if_exists="replace", index=False)

# bvalue windows: inputs only; Mc values are estimated in the analysis step, so only the n_total row per decade
dec = []
for k in range(5):
    s = 1976 + 10 * k; e = s + 9
    sub = df[(df.year >= s) & (df.year <= e)]
    dec.append({"window": f"{s}-{e}", "start_year": s, "end_year": e, "window_type": "decade",
                "n_total": int(len(sub))})
pd.DataFrame(dec).to_sql("eq_bvalue_windows", con, if_exists="replace", index=False)
con.commit()

# magType mix by decade
mix = df.groupby(["decade", "mag_class"]).size().unstack(fill_value=0)
mix_share = mix.div(mix.sum(axis=1), axis=0)
mt_dec = df.groupby(["decade", "magType"]).size().unstack(fill_value=0)
mix5 = df[m5].groupby(["decade", "mag_class"]).size().unstack(fill_value=0)
mix5_share = mix5.div(mix5.sum(axis=1), axis=0)
status_year = df.groupby("year").status.apply(lambda s: float((s == "reviewed").mean()))

# decade descriptive stats
decstats = {}
for d, g in df.groupby("decade"):
    ann = a[(a.year >= int(d[:4])) & (a.year <= int(d[5:]))]
    decstats[d] = {"n_events_m45": int(len(g)), "n_m50": int((g.mag >= 5).sum()),
                   "mean_annual_m50": float(ann.n_m50.mean()), "sd_annual_m50": float(ann.n_m50.std(ddof=1)),
                   "median_annual_m50": float(ann.n_m50.median()), "min_annual_m50": int(ann.n_m50.min()),
                   "max_annual_m50": int(ann.n_m50.max()),
                   "mean_annual_m55": float(ann.n_m55.mean()), "mean_annual_m60": float(ann.n_m60.mean()),
                   "mean_annual_m70": float(ann.n_m70.mean()),
                   "mean_mag": float(g.mag.mean()), "median_depth_km": float(g.depth.median())}
mag = df.mag; q = mag.quantile([.25, .5, .75])
dep = df.depth

stats = {
    "n_observations": int(len(df)), "n_units": int(len(df)),
    "time_coverage": {"start_iso": "1976-01-01", "end_iso": "2025-12-31", "n_periods": 50,
                      "first_event": df.time.iloc[0], "last_event": df.time.iloc[-1]},
    "outcome": {"mag": {"mean": float(mag.mean()), "sd": float(mag.std()), "min": float(mag.min()), "p25": float(q[.25]),
                        "median": float(q[.5]), "p75": float(q[.75]), "max": float(mag.max()), "n": int(mag.notna().sum())},
                "depth_km": {"mean": float(dep.mean()), "sd": float(dep.std()), "min": float(dep.min()),
                             "median": float(dep.median()), "max": float(dep.max()), "n": int(dep.notna().sum())},
                "annual_count_m50": {"mean": float(a.n_m50.mean()), "sd": float(a.n_m50.std(ddof=1)),
                                     "min": int(a.n_m50.min()), "median": float(a.n_m50.median()), "max": int(a.n_m50.max()),
                                     "n_years": 50, "total": int(a.n_m50.sum())}},
    "sample_flow": flow,
    "raw_rows_by_table": rows_raw,
    "removed_by_type_all_decades": {str(k): int(v) for k, v in type_tot.items()},
    "type_by_decade": {d: {str(k): int(v) for k, v in r.items()} for d, r in type_by_dec.iterrows()},
    "duplicates": {"repeated_ids": dups_id, "near_duplicate_pairs_flagged": len(pairs),
                   "near_duplicate_by_net_pair": {k: int(v) for k, v in pair_ct.items()}},
    "missingness_counts_after_cleaning": miss,
    "missingness_pct": {k: v / len(df) * 100 for k, v in miss.items()},
    "null_mag_after_dedup_and_type": null_mag,
    "range_checks": rng,
    "magtype_counts_by_decade": {d: {str(k): int(v) for k, v in r.items()} for d, r in mt_dec.iterrows()},
    "magclass_share_by_decade_m45": {d: {str(k): float(v) for k, v in r.items()} for d, r in mix_share.iterrows()},
    "magclass_share_by_decade_m50": {d: {str(k): float(v) for k, v in r.items()} for d, r in mix5_share.iterrows()},
    "reviewed_share_by_year_min": float(status_year.min()),
    "reviewed_share_2025": float(status_year.loc[2025]),
    "by_decade": decstats,
}
json.dump(stats, open("summary_statistics.json", "w"), indent=1)

# figure spec
yv = a.year.tolist()
fig = {"figures": [
    {"filename": "fig_annual_counts_m5.pdf", "figure_type": "time_series", "label": "fig:annual_counts",
     "caption_hint": "Yearly number of M>=5 earthquakes in ComCat (preferred magnitude), 1976-2025, with M>=6 for comparison",
     "series": [{"label": "M>=5", "x": yv, "y": a.n_m50.tolist(),
                 "source": {"table": "eq_annual_counts", "columns": {"x": "year", "y": "n_m50"}}},
                {"label": "M>=6", "x": yv, "y": a.n_m60.tolist(),
                 "source": {"table": "eq_annual_counts", "columns": {"x": "year", "y": "n_m60"}}}],
     "x_label": "Year", "y_label": "Earthquakes per year"},
    {"filename": "fig_magtype_mix.pdf", "figure_type": "bar", "label": "fig:magtype_mix",
     "caption_hint": "Share of M>=5 events whose preferred magnitude is of moment-magnitude family, by decade",
     "categories": list(mix5_share.index), "values": [float(mix5_share.loc[d].get("mw_family", 0) * 100) for d in mix5_share.index],
     "y_label": "Moment-magnitude family share of M>=5 events (%)"}]}
json.dump(fig, open("figure_spec.json", "w"), indent=1)

print(json.dumps(flow, indent=1)); print(rows_raw); print(dict(type_tot)); print(dups_id, len(pairs), pair_ct)
print(miss, rng); print(mix_share.round(3)); print(mix5_share.round(3)); print(a.to_string())
print(json.dumps(decstats, indent=1)); print(status_year.tail(3))
