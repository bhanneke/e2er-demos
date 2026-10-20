import sqlite3, json, numpy as np, pandas as pd
from collections import defaultdict

con = sqlite3.connect("data.db")
gdp = pd.read_sql("SELECT geo, geo_label, value, flag FROM gdp_pps_nuts2 WHERE time='2024'", con)
pop = pd.read_sql("SELECT geo, value AS population FROM pop_nuts2 WHERE time='2024'", con)
bnd = pd.read_sql("SELECT nuts_id, cntr_code, name_latn, geometry FROM nuts2_boundaries", con)

flow = [("raw 2024 rows, gdp_pps_nuts2", len(gdp))]
gdp = gdp.dropna(subset=["value"])
flow.append(("drop missing value", len(gdp)))
gdp = gdp[~gdp.geo.str[:2].isin(("TR", "RS", "ME", "MK"))]
flow.append(("drop non-EU27 (TR, RS, ME, MK)", len(gdp)))
d = gdp.merge(bnd, left_on="geo", right_on="nuts_id", how="left", indicator=True, validate="1:1")
assert (d._merge == "both").all()
d = d.merge(pop, on="geo", how="left", validate="1:1")
flow.append(("merge to GISCO NUTS 2024 geometry (unmatched = 0)", len(d)))
outer = {"ES70", "PT20", "PT30"} | {"FRY%d" % i for i in range(1, 6)}
all244 = d.copy()
d = d[~d.geo.isin(outer)].reset_index(drop=True)
flow.append(("drop 8 outermost regions = primary sample", len(d)))


def polys(g):
    gj = json.loads(g)
    return gj["coordinates"] if gj["type"] == "MultiPolygon" else [gj["coordinates"]]


def centroid(g):
    A = cx = cy = 0.0
    for poly in polys(g):
        for k, r in enumerate(poly):
            r = np.array(r)
            x, y = r[:, 0], r[:, 1]
            c = x[:-1] * y[1:] - x[1:] * y[:-1]
            s = 1.0 if k == 0 else -1.0
            sg = np.sign(c.sum()) or 1.0
            A += s * abs(c.sum()) / 2
            cx += s * sg * ((x[:-1] + x[1:]) * c).sum() / 6
            cy += s * sg * ((y[:-1] + y[1:]) * c).sum() / 6
    return cx / A, cy / A, A / 1e6


for df in (d, all244):
    cc = df.geometry.apply(centroid)
    df["cx"] = [c[0] for c in cc]
    df["cy"] = [c[1] for c in cc]
    df["area_km2"] = [c[2] for c in cc]


def queen(df):
    vm = defaultdict(set)
    for i, g in zip(df.geo, df.geometry):
        for poly in polys(g):
            for r in poly:
                for x, y in r:
                    vm[(round(x), round(y))].add(i)
    nb = {i: set() for i in df.geo}
    for s in vm.values():
        for i in s:
            nb[i] |= s - {i}
    return nb


nb = queen(d)
xy = d.set_index("geo")[["cx", "cy"]]
names = d.set_index("geo").name_latn
islands = [i for i in nb if not nb[i]]
isl_info = []
for i in islands:
    dist = np.hypot(xy.cx - xy.loc[i, "cx"], xy.cy - xy.loc[i, "cy"]).drop(i)
    j = dist.idxmin()
    nb[i] = {j}
    isl_info.append({"id": i, "name": names[i], "linked_to": j, "distance_km": round(float(dist.min()) / 1000, 1)})
rows = [(i, j, 1 / len(nb[i])) for i in nb for j in sorted(nb[i])]
pd.DataFrame(rows, columns=["from", "to", "weight"]).to_csv("spatial_weights.csv", index=False)


def knn(df, k=5):
    X = df[["cx", "cy"]].values
    ids = list(df.geo)
    out = []
    for a, i in enumerate(ids):
        dd = np.hypot(X[:, 0] - X[a, 0], X[:, 1] - X[a, 1])
        dd[a] = np.inf
        for b in np.argsort(dd, kind="stable")[:k]:
            out.append((i, ids[b], 1 / k))
    return pd.DataFrame(out, columns=["from", "to", "weight"])


knn(d).to_csv("spatial_weights_knn5.csv", index=False)
knn(all244).to_csv("spatial_weights_knn5_all244.csv", index=False)


def ref(df):
    return (df.value * df.population).sum() / df.population.sum()


def prep(df):
    o = pd.DataFrame({"id": df.geo, "name": df.name_latn, "country": df.geo.str[:2], "gdp_pps": df.value.astype(float),
                      "flag": df.flag.fillna(""), "population": df.population, "area_km2": df.area_km2.round(1)})
    o["gdp_index"] = (df.value / ref(df) * 100).round(2).values
    o["ln_gdp_pps"] = np.log(o.gdp_pps).round(5)
    return o


u = prep(d)
u.to_csv("spatial_units.csv", index=False)
prep(all244).to_csv("spatial_units_all244.csv", index=False)
u.to_sql("gdp_pps_sample", con, if_exists="replace", index=False)
con.commit()


def stats(s):
    q = s.quantile([.05, .1, .25, .5, .75, .9, .95])
    return {"n": int(s.count()), "mean": float(s.mean()), "sd": float(s.std()), "min": float(s.min()),
            "p5": float(q[.05]), "p10": float(q[.1]), "p25": float(q[.25]), "median": float(q[.5]),
            "p75": float(q[.75]), "p90": float(q[.9]), "p95": float(q[.95]), "max": float(s.max())}


deg = pd.Series({i: len(nb[i]) for i in nb})
srt = u.sort_values("gdp_pps")
ctry = u.groupby("country").gdp_pps.agg(["count", "mean", "min", "max"])
pw = float(ref(d))
sf = [{"step": s, "n": n, "dropped": (0 if k == 0 else flow[k - 1][1] - n)} for k, (s, n) in enumerate(flow)]
sf.append({"step": "final estimation sample (primary)", "n": len(u), "dropped": 0})
out = {
    "n_observations": len(u), "n_units": len(u),
    "time_coverage": {"start_iso": "2024-01-01", "end_iso": "2024-12-31", "n_periods": 1},
    "outcome": {"gdp_pps": stats(u.gdp_pps), "gdp_index": stats(u.gdp_index), "ln_gdp_pps": stats(u.ln_gdp_pps)},
    "population_weighted_mean_gdp_pps": pw,
    "n_all244": len(all244), "mean_gdp_pps_all244": float(all244.value.mean()),
    "ratio_max_to_min": float(u.gdp_pps.max() / u.gdp_pps.min()),
    "ratio_p90_to_p10": float(u.gdp_pps.quantile(.9) / u.gdp_pps.quantile(.1)),
    "n_regions_above_pop_weighted_mean": int((u.gdp_pps > pw).sum()),
    "flags": {"provisional": int((u.flag == "p").sum()), "estimated": int((u.flag == "e").sum()), "none": int((u.flag == "").sum())},
    "population": {"total": int(u.population.sum()), "missing": int(u.population.isna().sum())},
    "top5": [{"id": r.id, "gdp_pps": r.gdp_pps} for _, r in srt.tail(5)[::-1].iterrows()],
    "bottom5": [{"id": r.id, "gdp_pps": r.gdp_pps} for _, r in srt.head(5).iterrows()],
    "by_country": {c: {"n": int(r["count"]), "mean": float(r["mean"]), "min": float(r["min"]), "max": float(r["max"])} for c, r in ctry.iterrows()},
    "weights": {"queen": {"n_links": len(rows), "n_islands_linked_to_nearest": len(islands), "mean_neighbours": float(deg.mean()),
                          "min_neighbours": int(deg.min()), "max_neighbours": int(deg.max())},
                "knn5": {"k": 5, "n_links": len(d) * 5}, "knn5_all244": {"k": 5, "n_links": len(all244) * 5}},
    "sample_flow": sf,
    "merge_coverage": {"data_regions_matched_to_geometry": len(all244), "data_regions_without_geometry": 0,
                       "boundary_units_total": len(bnd), "boundary_units_without_eu27_data": len(bnd) - len(all244)},
    "data_quality_log": {"missing_gdp_values_2024": 0, "nuts_code_recoding_needed": 0, "crs_epsg": 3035,
                         "islands": isl_info},
}
json.dump(out, open("summary_statistics.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["outcome", "weights", "sample_flow", "flags", "population", "top5", "bottom5",
                                      "merge_coverage", "population_weighted_mean_gdp_pps", "n_regions_above_pop_weighted_mean"]}, indent=1))
print(isl_info)
