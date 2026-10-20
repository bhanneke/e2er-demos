import json, sqlite3, numpy as np, pandas as pd

SEED, NP = 20241014, 999
rng = np.random.default_rng(SEED)
BASE = ["id", "name", "country", "gdp_pps", "flag", "population", "area_km2", "gdp_index", "ln_gdp_pps"]
U = pd.read_csv("spatial_units.csv")[BASE]
ids = list(U.id)
n = len(ids)
ix = {k: i for i, k in enumerate(ids)}
x = U.gdp_pps.values.astype(float)


def dense(fn, idl=ids):
    w = pd.read_csv(fn)
    m = np.zeros((len(idl), len(idl)))
    j = {k: i for i, k in enumerate(idl)}
    for a, b, v in zip(w["from"], w["to"], w.weight):
        m[j[a], j[b]] += v
    return m


def rowstd(W):
    s = W.sum(1, keepdims=True)
    return np.divide(W, s, out=np.zeros_like(W), where=s > 0)


def moran_I(W, v):
    z = v - v.mean()
    return len(v) / W.sum() * (z @ W @ z) / (z @ z)


MAIN_N = 236


def moran(W, v, variable, wdesc, **extra):
    m = len(v)
    I = moran_I(W, v)
    E = -1 / (m - 1)
    S0 = W.sum()
    P = np.array([rng.permutation(v) for _ in range(NP)])
    P = P - P.mean(1, keepdims=True)
    Ip = m / S0 * np.einsum("ij,ij->i", P @ W.T, P) / (P * P).sum(1)
    p = (1 + (np.abs(Ip - E) >= abs(I - E) - 1e-12).sum()) / (NP + 1)
    d = dict(statistic="morans_i", variable=variable, weights=wdesc, estimate=round(float(I), 5),
             expected=round(E, 6), z=round(float((I - Ip.mean()) / Ip.std(ddof=1)), 3), p_value=round(float(p), 4),
             p_value_method="permutation", n_permutations=NP, alternative="two-sided", n_units=int(m))
    d.update(extra)
    if m != MAIN_N:  # expected value stated only for the main sample size
        d["expected_note"] = f"-1/(n-1) = {E:.6f} for this statistic's own n"
        del d["expected"]
    return d


Wq = dense("spatial_weights.csv")
Wk5 = dense("spatial_weights_knn5.csv")
con = sqlite3.connect("data.db")
b = pd.read_sql("SELECT nuts_id, geometry FROM nuts2_boundaries", con).set_index("nuts_id")


def cen(g):
    gj = json.loads(g)
    polys = gj["coordinates"] if gj["type"] == "MultiPolygon" else [gj["coordinates"]]
    A = cx = cy = 0.0
    for poly in polys:
        for k, r in enumerate(poly):
            r = np.array(r)
            X, Y = r[:, 0], r[:, 1]
            c = X[:-1] * Y[1:] - X[1:] * Y[:-1]
            s = 1.0 if k == 0 else -1.0
            sg = np.sign(c.sum()) or 1.0
            A += s * abs(c.sum()) / 2
            cx += s * sg * ((X[:-1] + X[1:]) * c).sum() / 6
            cy += s * sg * ((Y[:-1] + Y[1:]) * c).sum() / 6
    return cx / A, cy / A


C = np.array([cen(b.loc[k, "geometry"]) for k in ids])
D = np.sqrt(((C[:, None, :] - C[None, :, :]) ** 2).sum(2)) / 1000.0


def knn(Dm, k):
    W = np.zeros_like(Dm)
    D2 = Dm + np.diag(np.full(len(Dm), np.inf))
    for i in range(len(Dm)):
        W[i, np.argsort(D2[i])[:k]] = 1
    return rowstd(W)


Wk8 = knn(D, 8)
with np.errstate(divide="ignore"):
    Wid = rowstd(np.where(D > 0, 1 / D, 0))


def save(W, fn):
    r, c = np.nonzero(W)
    pd.DataFrame({"from": [ids[i] for i in r], "to": [ids[j] for j in c], "weight": W[r, c]}).to_csv(fn, index=False)


save(Wk8, "spatial_weights_knn8.csv")
save(Wid, "spatial_weights_invdist.csv")

QD = "queen contiguity, row-standardised (islands linked to nearest region)"
ss = {}
ss["moran_gdp_queen"] = moran(Wq, x, "gdp_pps", QD, weights_file="spatial_weights.csv")
ss["moran_gdp_knn5"] = moran(Wk5, x, "gdp_pps", "k = 5 nearest neighbours (centroids), row-standardised", weights_file="spatial_weights_knn5.csv")
ss["moran_gdp_knn8"] = moran(Wk8, x, "gdp_pps", "k = 8 nearest neighbours (centroids), row-standardised", weights_file="spatial_weights_knn8.csv")
ss["moran_gdp_invdist"] = moran(Wid, x, "gdp_pps", "inverse distance (1/km, all pairs), row-standardised", weights_file="spatial_weights_invdist.csv")
ss["moran_lngdp_queen"] = moran(Wq, U.ln_gdp_pps.values, "ln_gdp_pps", QD, weights_file="spatial_weights.csv")
A = pd.read_csv("spatial_units_all244.csv")
ids244 = list(A.id)
rob = {}
rob["moran_gdp_knn5_all244"] = moran(dense("spatial_weights_knn5_all244.csv", ids244), A.gdp_pps.values.astype(float), "gdp_pps",
                                    "k = 5 nearest neighbours, row-standardised, 244 EU27 regions incl. outermost")

pop = U.population.values.astype(float)


def sub(keep, desc):
    k = np.array(keep)
    Ws = rowstd(Wq[np.ix_(k, k)])
    r = moran(Ws, x[k], "gdp_pps", "queen, row-standardised, after " + desc)
    r["n_isolated_after_drop"] = int((Ws.sum(1) == 0).sum())
    r["dropped"] = desc
    return r


def drop(codes):
    codes = [c for c in codes if c in ix]
    return [i for i in range(n) if ids[i] not in codes], codes


caps = "BE10 BG41 CZ01 DK01 DE30 EE00 IE06 EL30 ES30 FR10 HR05 ITI4 CY00 LV00 LT01 LU00 HU11 MT00 NL32 AT13 PL91 PT17 PT1A RO32 SI04 SK01 FI1B SE11".split()
top5 = list(U.sort_values("gdp_pps", ascending=False).id[:5])
irl = [i for i in ids if i.startswith("IE")]
for key, codes in [("drop_LU00", ["LU00"]), ("drop_Ireland", irl), ("drop_top5", top5), ("drop_capital_regions", caps)]:
    keep, cs = drop(codes)
    r = sub(keep, "dropping %d regions" % len(cs))
    r["dropped_ids"] = cs
    rob["sens_" + key] = r
cty = U.country.values
nat = pd.Series(x * pop).groupby(cty).transform("sum") / pd.Series(pop).groupby(cty).transform("sum")
rob["sens_within_country_demeaned"] = moran(Wq, x - nat.values, "gdp_pps minus national population-weighted mean", QD)
cross = float((Wq * (cty[:, None] != cty[None, :])).sum() / Wq.sum())

z = (x - x.mean()) / x.std(ddof=0)
lag = Wq @ z
quad = np.where(z >= 0, np.where(lag >= 0, "HH", "HL"), np.where(lag >= 0, "LH", "LL"))
slope = float(np.polyfit(z, lag, 1)[0])
scatter = [dict(id=i, z=round(float(a), 4), wz=round(float(c), 4), quadrant=q) for i, a, c, q in zip(ids, z, lag, quad)]

Ii = z * lag
pl = np.zeros(n)
for i in range(n):
    others = np.delete(np.arange(n), i)
    wi = Wq[i, Wq[i] > 0]
    k = len(wi)
    sel = others[rng.random((NP, n - 1)).argsort(1)[:, :k]]
    sim = z[i] * (z[sel] * wi).sum(1)
    pl[i] = (1 + (sim >= Ii[i]).sum()) / (NP + 1) if Ii[i] > 0 else (1 + (sim <= Ii[i]).sum()) / (NP + 1)
o = np.argsort(pl)
q = pl[o] * n / (np.arange(n) + 1)
q = np.minimum.accumulate(q[::-1])[::-1]
qv = np.empty(n)
qv[o] = np.minimum(q, 1)
cl = np.where(pl < 0.05, quad, "ns")
clf = np.where(qv < 0.05, quad, "ns")


def cnt(c):
    return {k: {"count": int((c == k).sum())} for k in ["HH", "LL", "HL", "LH", "ns"]}


Bs = (Wq > 0).astype(float) + np.eye(n)
Ws = rowstd(Bs)
S = x.std(ddof=0)
gi = (Ws @ x - x.mean()) / (S * np.sqrt((n * (Ws ** 2).sum(1) - 1) / (n - 1)))


def gini(v):
    v = np.sort(v)
    m = len(v)
    return float((2 * np.arange(1, m + 1) - m - 1).dot(v) / (m * v.sum()))


def theil(v, w):
    s = w / w.sum()
    mu = (s * v).sum()
    return float((s * v / mu * np.log(v / mu)).sum())


mu_w = (x * pop).sum() / pop.sum()
cm = pd.DataFrame({"c": cty, "xp": x * pop, "p": pop}).groupby("c").sum()
T = theil(x, pop)
Tb = theil((cm.xp / cm.p).values, cm.p.values)


def desc(a):
    return dict(n=int(len(a)), mean=float(a.mean()), sd=float(a.std(ddof=1)), min=float(a.min()), median=float(np.median(a)), max=float(a.max()))


variables = {"gdp_pps": desc(x), "gdp_index": desc(U.gdp_index.values), "ln_gdp_pps": desc(U.ln_gdp_pps.values)}
srt = U.sort_values("gdp_pps")
dist = dict(cv=float(x.std(ddof=0) / x.mean()), cv_pop_weighted=float(np.sqrt((pop * (x - mu_w) ** 2).sum() / pop.sum()) / mu_w),
            gini=gini(x), theil_pop_weighted=T, theil_between_country=Tb, theil_within_country=T - Tb, share_between_country=float(Tb / T),
            max_min_ratio=float(x.max() / x.min()), p90_p10_ratio=float(np.percentile(x, 90) / np.percentile(x, 10)),
            pop_weighted_mean=float(mu_w),
            top5=[[i, float(v)] for i, v in zip(srt.id[::-1][:5], srt.gdp_pps[::-1][:5])],
            bottom5=[[i, float(v)] for i, v in zip(srt.id[:5], srt.gdp_pps[:5])])
dist_sens = {}
for key, codes in [("drop_LU00", ["LU00"]), ("drop_Ireland", irl), ("drop_capital_regions", caps)]:
    k, _ = drop(codes)
    v = x[k]
    dist_sens[key] = dict(n=len(k), cv=float(v.std(ddof=0) / v.mean()), gini=gini(v))

U["local_i"] = np.round(Ii, 4)
U["lisa_p"] = np.round(pl, 4)
U["lisa_p_fdr"] = np.round(qv, 4)
U["lisa_cluster"] = np.where(cl == "ns", "Not significant", cl)
U["lisa_cluster_fdr"] = np.where(clf == "ns", "Not significant", clf)
U["gi_star_z"] = np.round(gi, 3)
U["moran_quadrant"] = quad
U.to_csv("spatial_units.csv", index=False)
pd.DataFrame(scatter).to_csv("moran_scatter_data.csv", index=False)

cc = U[U.lisa_cluster.isin(["HH", "LL"])].groupby(["country", "lisa_cluster"]).size().unstack(1).fillna(0).astype(int)
CATS = {"HH": {"label": "High-High", "color": "#b2182b"}, "LL": {"label": "Low-Low", "color": "#2166ac"},
        "HL": {"label": "High-Low", "color": "#ef8a62"}, "LH": {"label": "Low-High", "color": "#67a9cf"},
        "Not significant": {"label": "Not significant", "color": "#e0e0e0"}}
EXT = [-12, 34, 35, 72]
res = {
    "result_kind": "spatial",
    "units": {"type": "NUTS 2 region", "n_units": n, "id_field": "id", "crs": "EPSG:3035", "year": 2024,
              "note": "EU27 NUTS 2024 regions excluding 8 outermost regions; 13 island regions linked to nearest region (queen)"},
    "variables": variables,
    "distribution": dist, "distribution_sensitivity": dist_sens,
    "spatial_statistics": ss,
    "moran_scatter": {"variable": "gdp_pps", "weights": "queen, row-standardised", "slope": slope, "data_file": "moran_scatter_data.csv",
                      "quadrant_counts": {k: int((quad == k).sum()) for k in ["HH", "LL", "HL", "LH"]}},
    "robustness": rob,
    "clusters": cnt(cl),
    "cluster_details": {
                 "method": "local Moran's I, queen row-standardised, conditional permutation 999, pseudo p in direction of sign of I_i, p < 0.05 uncorrected",
                 "seed": SEED, "n_significant_p05": int((cl != "ns").sum()), "expected_false_positives_p05": round(0.05 * n, 1),
                 "fdr_bh_q05": cnt(clf), "n_significant_fdr": int((clf != "ns").sum()),
                 "hh_ll_by_country": {c: {k: int(v) for k, v in r.items()} for c, r in cc.iterrows()},
                 "hh_ids": list(U.id[cl == "HH"]), "ll_ids": list(U.id[cl == "LL"]),
                 "hl_ids": list(U.id[cl == "HL"]), "lh_ids": list(U.id[cl == "LH"])},
    "getis_ord": {"statistic": "gi_star", "weights": "queen incl. own value, row-standardised",
                  "hot_spots_z_gt_1.96": int((gi > 1.96).sum()), "cold_spots_z_lt_-1.96": int((gi < -1.96).sum()),
                  "note": "analytic z, not corrected for multiple testing"},
    "share_queen_links_crossing_borders": cross,
    "maps": [
        {"id": "map_gdp_pps", "figure": "fig_map_gdp_pps_2024.pdf", "variable": "gdp_pps", "classification": "quantiles", "classes": 5,
         "legend_label": "GDP per inhabitant, PPS (EU27 2020), 2024", "extent": EXT},
        {"id": "map_gdp_index", "figure": "fig_map_gdp_index.pdf", "variable": "gdp_index", "classification": "breaks",
         "breaks": [0, 50, 75, 100, 125, 150, 1000], "legend_label": "GDP per inhabitant, PPS (EU27 = 100)", "extent": EXT},
        {"id": "map_lisa", "figure": "fig_map_lisa.pdf", "variable": "lisa_cluster", "classification": "categories",
         "categories": CATS, "legend_label": "LISA clusters (p < 0.05, 999 permutations)", "extent": EXT}],
}
json.dump(res, open("estimation_results.json", "w"), indent=1)

BND = {"table": "nuts2_boundaries", "id_column": "nuts_id", "geometry_column": "geometry"}
ATT = "© EuroGeographics for the administrative boundaries"
new = [
    {"filename": "fig_map_gdp_index.pdf", "figure_type": "map", "label": "fig:map_gdp_index", "map_type": "choropleth",
     "caption_hint": "GDP per inhabitant in PPS, EU27 = 100, NUTS 2, 2024", "boundaries": BND,
     "data": {"file": "spatial_units.csv", "id_column": "id", "value_column": "gdp_index"}, "classification": "breaks",
     "breaks": [0, 50, 75, 100, 125, 150, 1000], "crs": "EPSG:3035", "projection": "none", "extent": EXT,
     "legend_label": "GDP per inhabitant, PPS (EU27 = 100)", "attribution": ATT},
    {"filename": "fig_map_lisa.pdf", "figure_type": "map", "label": "fig:map_lisa", "map_type": "categories",
     "caption_hint": "LISA clusters of GDP per inhabitant (PPS), queen weights, p<0.05 uncorrected", "boundaries": BND,
     "data": {"file": "spatial_units.csv", "id_column": "id", "value_column": "lisa_cluster"}, "categories": CATS,
     "crs": "EPSG:3035", "projection": "none", "extent": EXT, "legend_label": "LISA clusters", "attribution": ATT},
    {"filename": "fig_moran_scatter.pdf", "figure_type": "scatter", "label": "fig:moran_scatter",
     "caption_hint": "Moran scatterplot of GDP per inhabitant (standardised) against its spatial lag, queen weights",
     "x": [p["z"] for p in scatter], "y": [p["wz"] for p in scatter], "groups": quad.tolist(),
     "x_label": "Standardised GDP per inhabitant (z)", "y_label": "Spatial lag of z (queen, row-standardised)"}]
try:
    fs = json.load(open("figure_spec.json"))
except Exception:
    fs = {"figures": []}
fs["figures"] = [f for f in fs["figures"] if f["filename"] not in {a["filename"] for a in new}] + new
json.dump(fs, open("figure_spec.json", "w"), indent=1)

for k, v in ss.items():
    print(k, v["estimate"], v["z"], v["p_value"], v.get("n_isolated_after_drop"))
print(res["clusters"], res["cluster_details"]["n_significant_p05"], res["cluster_details"]["fdr_bh_q05"])
print(dist, dist_sens, slope, cross, res["getis_ord"])
print(rob["sens_drop_capital_regions"]["dropped_ids"])
