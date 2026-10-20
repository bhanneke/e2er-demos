"""
Replication script for: Spatial clustering of GDP per inhabitant across EU NUTS-2 regions, 2024
Paper ID: 620f7e1f-43a0-4f27-b982-57099cbbc277

Descriptive spatial analysis (no regression, no causal claim): distribution of GDP per inhabitant
in PPS, global Moran's I under four weights definitions, Moran scatterplot, local Moran's I (LISA)
with Benjamini-Hochberg FDR, Getis-Ord Gi*, sensitivity (drop LU / IE / top 5 / capitals,
within-country demeaning, 244-region kNN), maps.

Requirements: pandas, numpy, matplotlib (standard library: json, sqlite3, pathlib)
Usage: python replication/estimation.py      (from the workspace root, or anywhere)
Output: replication/output/ (tables as CSV, estimation_results.json, figures as PNG)

Inference: permutation (999 draws, seeded). No standard errors are involved; the paper's
"robust SE" convention does not apply because no regression is estimated.

Inputs (not shipped; see README.md):
  data/gdp_pps_nuts2.csv   Eurostat nama_10r_2gdp, unit PPS_EU27_2020_HAB
  data/pop_nuts2.csv       Eurostat demo_r_d2jan, total population, 1 Jan 2024
  GISCO NUTS 2024 1:20m boundaries (EPSG:3035): data/nuts2_boundaries.csv if present,
  otherwise table nuts2_boundaries in data.db (columns nuts_id, geometry = GeoJSON string)
"""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon
import numpy as np
import pandas as pd

SEED, NP = 20241014, 999          # permutation seed and number of permutations
np.random.seed(42)
rng = np.random.default_rng(SEED)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Load data ──────────────────────────────────────────────────────────────
gdp = pd.read_csv(ROOT / "data" / "gdp_pps_nuts2.csv", dtype={"time": str})
gdp = gdp[(gdp.time == "2024") & (gdp.unit == "PPS_EU27_2020_HAB")][["geo", "geo_label", "value", "flag"]]
pop = pd.read_csv(ROOT / "data" / "pop_nuts2.csv", dtype={"time": str})
pop = pop[pop.time == "2024"][["geo", "value"]].rename(columns={"value": "population"})
if (ROOT / "data" / "nuts2_boundaries.csv").exists():
    bnd = pd.read_csv(ROOT / "data" / "nuts2_boundaries.csv")
else:
    bnd = pd.read_sql("SELECT nuts_id, cntr_code, name_latn, geometry FROM nuts2_boundaries",
                      sqlite3.connect(ROOT / "data.db"))

# ── 2. Variable construction and sample ───────────────────────────────────────
flow = [("raw 2024 rows", len(gdp))]
gdp = gdp.dropna(subset=["value"])
flow.append(("drop missing value", len(gdp)))
gdp = gdp[~gdp.geo.str[:2].isin(("TR", "RS", "ME", "MK"))]
flow.append(("drop non-EU27 (TR, RS, ME, MK)", len(gdp)))
d = gdp.merge(bnd, left_on="geo", right_on="nuts_id", how="left", indicator=True, validate="1:1")
assert (d._merge == "both").all(), "unmatched NUTS codes"
d = d.merge(pop, on="geo", how="left", validate="1:1")
OUTER = {"ES70", "PT20", "PT30"} | {"FRY%d" % i for i in range(1, 6)}
all244 = d.copy()
d = d[~d.geo.isin(OUTER)].reset_index(drop=True)
flow.append(("drop 8 outermost regions = primary sample", len(d)))
pd.DataFrame(flow, columns=["step", "n"]).to_csv(OUTPUT_DIR / "table_sample_flow.csv", index=False)  # sample flow (data section)


def polys(g):
    gj = json.loads(g)
    return gj["coordinates"] if gj["type"] == "MultiPolygon" else [gj["coordinates"]]


def centroid(g):
    """Area-weighted centroid and area (km2) of a (Multi)Polygon in EPSG:3035 metres."""
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


def ref(df):  # population-weighted mean = EU27 reference for the index
    return (df.value * df.population).sum() / df.population.sum()


def prep(df):
    o = pd.DataFrame({"id": df.geo, "name": df.name_latn, "country": df.geo.str[:2], "gdp_pps": df.value.astype(float),
                      "flag": df.flag.fillna(""), "population": df.population, "area_km2": df.area_km2.round(1)})
    o["gdp_index"] = (df.value / ref(df) * 100).round(2).values
    o["ln_gdp_pps"] = np.log(o.gdp_pps).round(5)
    return o


U, A244 = prep(d), prep(all244)
ids = list(U.id)
n = len(ids)
ix = {k: i for i, k in enumerate(ids)}
x = U.gdp_pps.values.astype(float)
pop_v = U.population.values.astype(float)
cty = U.country.values

# ── 2b. Spatial weights ───────────────────────────────────────────────────────
def rowstd(W):
    s = W.sum(1, keepdims=True)
    return np.divide(W, s, out=np.zeros_like(W), where=s > 0)


def queen_neighbours(df):
    """Queen contiguity: regions sharing at least one boundary vertex (rounded to 1 m)."""
    vm = defaultdict(set)
    for i, g in zip(df.geo, df.geometry):
        for poly in polys(g):
            for r in poly:
                for px, py in r:
                    vm[(round(px), round(py))].add(i)
    nb = {i: set() for i in df.geo}
    for s in vm.values():
        for i in s:
            nb[i] |= s - {i}
    return nb


nb = queen_neighbours(d)
xy = d.set_index("geo")[["cx", "cy"]]
islands = [i for i in nb if not nb[i]]
for i in islands:  # island regions: link to nearest region by centroid distance
    dist = np.hypot(xy.cx - xy.loc[i, "cx"], xy.cy - xy.loc[i, "cy"]).drop(i)
    nb[i] = {dist.idxmin()}
Wq = np.zeros((n, n))
for i in nb:
    for j in nb[i]:
        Wq[ix[i], ix[j]] = 1.0
Wq = rowstd(Wq)


def knn(Dm, k):
    W = np.zeros_like(Dm)
    D2 = Dm + np.diag(np.full(len(Dm), np.inf))
    for i in range(len(Dm)):
        W[i, np.argsort(D2[i], kind="stable")[:k]] = 1
    return rowstd(W)


C = d[["cx", "cy"]].values
D = np.sqrt(((C[:, None, :] - C[None, :, :]) ** 2).sum(2)) / 1000.0     # km
Wk5, Wk8 = knn(D, 5), knn(D, 8)
with np.errstate(divide="ignore"):
    Wid = rowstd(np.where(D > 0, 1 / D, 0))                             # inverse distance, all pairs
C2 = all244[["cx", "cy"]].values
D2m = np.sqrt(((C2[:, None, :] - C2[None, :, :]) ** 2).sum(2)) / 1000.0
Wk5_244 = knn(D2m, 5)

# ── 3. Summary statistics ─────────────────────────────────────────────────────
def gini(v):
    v = np.sort(v)
    m = len(v)
    return float((2 * np.arange(1, m + 1) - m - 1).dot(v) / (m * v.sum()))


def theil(v, w):
    s = w / w.sum()
    mu = (s * v).sum()
    return float((s * v / mu * np.log(v / mu)).sum())


mu_w = (x * pop_v).sum() / pop_v.sum()
cm = pd.DataFrame({"c": cty, "xp": x * pop_v, "p": pop_v}).groupby("c").sum()
T = theil(x, pop_v)
Tb = theil((cm.xp / cm.p).values, cm.p.values)
srt = U.sort_values("gdp_pps")
dist_stats = dict(
    cv=float(x.std(ddof=0) / x.mean()),
    cv_pop_weighted=float(np.sqrt((pop_v * (x - mu_w) ** 2).sum() / pop_v.sum()) / mu_w),
    gini=gini(x), theil_pop_weighted=T, theil_between_country=Tb, theil_within_country=T - Tb,
    share_between_country=float(Tb / T), max_min_ratio=float(x.max() / x.min()),
    p90_p10_ratio=float(np.percentile(x, 90) / np.percentile(x, 10)), pop_weighted_mean=float(mu_w),
    top5=[[i, float(v)] for i, v in zip(srt.id[::-1][:5], srt.gdp_pps[::-1][:5])],
    bottom5=[[i, float(v)] for i, v in zip(srt.id[:5], srt.gdp_pps[:5])])
q = U[["gdp_pps", "gdp_index", "ln_gdp_pps"]].describe(percentiles=[.05, .1, .25, .5, .75, .9, .95]).T
q.to_csv(OUTPUT_DIR / "table1_summary.csv")  # Table 1: summary statistics of GDP per inhabitant (PPS)
pd.DataFrame([{k: v for k, v in dist_stats.items() if not isinstance(v, list)}]).T.rename(columns={0: "value"}).to_csv(
    OUTPUT_DIR / "table1b_distribution.csv")  # Table 1 (distribution measures: Gini, Theil, CV, ratios)

# ── 4. Main specification: global Moran's I, queen contiguity ────────────────
MAIN_N = 236


def moran_I(W, v):
    z = v - v.mean()
    return len(v) / W.sum() * (z @ W @ z) / (z @ z)


def moran(W, v, variable, wdesc, **extra):
    """Global Moran's I with 999-permutation two-sided pseudo p (random reassignment of values)."""
    m = len(v)
    I = moran_I(W, v)
    E = -1 / (m - 1)
    P = np.array([rng.permutation(v) for _ in range(NP)])
    P = P - P.mean(1, keepdims=True)
    Ip = m / W.sum() * np.einsum("ij,ij->i", P @ W.T, P) / (P * P).sum(1)
    p = (1 + (np.abs(Ip - E) >= abs(I - E) - 1e-12).sum()) / (NP + 1)
    r = dict(variable=variable, weights=wdesc, I=float(I), expected=E,
             z=float((I - Ip.mean()) / Ip.std(ddof=1)), p_value=float(p), n_permutations=NP, n_units=int(m))
    r.update(extra)
    return r


QD = "queen contiguity, row-standardised (islands linked to nearest region)"
main_rows = [
    moran(Wq, x, "gdp_pps", QD),
    moran(Wk5, x, "gdp_pps", "kNN k=5 (centroids), row-standardised"),
    moran(Wk8, x, "gdp_pps", "kNN k=8 (centroids), row-standardised"),
    moran(Wid, x, "gdp_pps", "inverse distance 1/km, all pairs, row-standardised"),
    moran(Wq, U.ln_gdp_pps.values, "ln_gdp_pps", QD),
]
pd.DataFrame(main_rows).to_csv(OUTPUT_DIR / "table2_global_moran.csv", index=False)  # Table 2: global Moran's I, main and alternative weights

# Moran scatterplot data
z = (x - x.mean()) / x.std(ddof=0)
lag = Wq @ z
quad = np.where(z >= 0, np.where(lag >= 0, "HH", "HL"), np.where(lag >= 0, "LH", "LL"))
slope = float(np.polyfit(z, lag, 1)[0])  # equals I for row-standardised W
pd.DataFrame(dict(id=ids, z=z.round(4), wz=lag.round(4), quadrant=quad)).to_csv(
    OUTPUT_DIR / "moran_scatter_data.csv", index=False)  # Figure 3 data (Moran scatterplot)

# Local Moran's I (LISA), conditional permutation, plus BH-FDR
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
qq = np.minimum.accumulate((pl[o] * n / (np.arange(n) + 1))[::-1])[::-1]
qv = np.empty(n)
qv[o] = np.minimum(qq, 1)
cl = np.where(pl < 0.05, quad, "ns")
clf = np.where(qv < 0.05, quad, "ns")

# Getis-Ord Gi* (own value included, row-standardised)
Ws = rowstd((Wq > 0).astype(float) + np.eye(n))
gi = (Ws @ x - x.mean()) / (x.std(ddof=0) * np.sqrt((n * (Ws ** 2).sum(1) - 1) / (n - 1)))

U["local_i"] = Ii.round(4)
U["lisa_p"] = pl.round(4)
U["lisa_p_fdr"] = qv.round(4)
U["lisa_cluster"] = np.where(cl == "ns", "Not significant", cl)
U["lisa_cluster_fdr"] = np.where(clf == "ns", "Not significant", clf)
U["gi_star_z"] = gi.round(3)
U["moran_quadrant"] = quad
U.to_csv(OUTPUT_DIR / "table3_lisa_by_region.csv", index=False)  # Table 3 / Figure 4 data: LISA, FDR, Gi* by region
cnt = pd.DataFrame({"uncorrected_p05": pd.Series(cl).value_counts(), "bh_fdr_q05": pd.Series(clf).value_counts()}).fillna(0).astype(int)
cnt.to_csv(OUTPUT_DIR / "table3b_lisa_counts.csv")  # Table 3: LISA cluster counts (uncorrected and FDR)
U[U.lisa_cluster.isin(["HH", "LL"])].groupby(["country", "lisa_cluster"]).size().unstack(1).fillna(0).astype(int).to_csv(
    OUTPUT_DIR / "table3c_lisa_by_country.csv")  # Table 3: HH/LL regions by country

# ── 5. Robustness checks ──────────────────────────────────────────────────────
rob = [moran(Wk5_244, A244.gdp_pps.values.astype(float), "gdp_pps",
             "kNN k=5, 244 EU27 regions incl. outermost", dropped="none (outermost regions added)")]


def sub(codes, label):
    codes = [c for c in codes if c in ix]
    k = np.array([i for i in range(n) if ids[i] not in codes])
    Wsub = rowstd(Wq[np.ix_(k, k)])
    r = moran(Wsub, x[k], "gdp_pps", "queen, row-standardised, after " + label,
              dropped="%s (%d regions)" % (label, len(codes)), n_isolated_after_drop=int((Wsub.sum(1) == 0).sum()))
    return r


CAPS = ("BE10 BG41 CZ01 DK01 DE30 EE00 IE06 EL30 ES30 FR10 HR05 ITI4 CY00 LV00 LT01 LU00 HU11 MT00 NL32 AT13 "
        "PL91 PT17 PT1A RO32 SI04 SK01 FI1B SE11").split()
top5 = list(srt.id[::-1][:5])
irl = [i for i in ids if i.startswith("IE")]
rob.append(sub(["LU00"], "dropping LU00"))
rob.append(sub(irl, "dropping Irish regions"))
rob.append(sub(top5, "dropping top 5 regions"))
rob.append(sub(CAPS, "dropping national capital regions"))
nat = pd.Series(x * pop_v).groupby(cty).transform("sum") / pd.Series(pop_v).groupby(cty).transform("sum")
rob.append(moran(Wq, x - nat.values, "gdp_pps minus national population-weighted mean", QD,
                 dropped="within-country demeaned (permutation null not adapted to demeaned data)"))
pd.DataFrame(rob).to_csv(OUTPUT_DIR / "table4_robustness.csv", index=False)  # Table 4: sensitivity of Moran's I

dist_sens = []
for key, codes in [("drop_LU00", ["LU00"]), ("drop_Ireland", irl), ("drop_capital_regions", CAPS)]:
    keep = [v for i, v in zip(ids, x) if i not in codes]
    v = np.array(keep)
    dist_sens.append(dict(sample=key, n=len(v), cv=float(v.std(ddof=0) / v.mean()), gini=gini(v)))
pd.DataFrame(dist_sens).to_csv(OUTPUT_DIR / "table4b_distribution_sensitivity.csv", index=False)  # Table 4: CV/Gini sensitivity

# ── 6. Export results and figures ─────────────────────────────────────────────
res = dict(
    n_units=n, distribution=dist_stats, global_moran=main_rows, robustness=rob, moran_scatter_slope=slope,
    share_queen_links_crossing_borders=float((Wq * (cty[:, None] != cty[None, :])).sum() / Wq.sum()),
    lisa_counts_uncorrected={k: int((cl == k).sum()) for k in ["HH", "LL", "HL", "LH", "ns"]},
    lisa_counts_fdr={k: int((clf == k).sum()) for k in ["HH", "LL", "HL", "LH", "ns"]},
    gi_star_hot_z_gt_1_96=int((gi > 1.96).sum()), gi_star_cold_z_lt_m1_96=int((gi < -1.96).sum()),
    seed=SEED, n_permutations=NP)
json.dump(res, open(OUTPUT_DIR / "estimation_results.json", "w"), indent=1)  # all headline numbers in one file

ATT = "© EuroGeographics for the administrative boundaries"
geom = d.set_index("geo").geometry


def draw_map(values, cmap_fn, title, fn, legend=None):
    fig, ax = plt.subplots(figsize=(7, 7))
    patches, cols = [], []
    for i in ids:
        for poly in polys(geom[i]):
            patches.append(MplPolygon(np.array(poly[0]), closed=True))
            cols.append(cmap_fn(values[i]))
    ax.add_collection(PatchCollection(patches, facecolor=cols, edgecolor="white", linewidth=0.2))
    ax.set_xlim(2.4e6, 6.6e6)
    ax.set_ylim(1.35e6, 5.45e6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    if legend:
        ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in legend.values()], labels=list(legend.keys()),
                  loc="upper left", fontsize=7, frameon=False)
    fig.text(0.01, 0.01, ATT + "; Eurostat data, statistics computed by the authors", fontsize=6)
    fig.savefig(OUTPUT_DIR / fn, dpi=200, bbox_inches="tight")  # map figure
    plt.close(fig)


qs = np.quantile(x, [.2, .4, .6, .8])
pal = ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"]
val = dict(zip(ids, x))
draw_map(val, lambda v: pal[int(np.searchsorted(qs, v))], "GDP per inhabitant, PPS (EU27 2020), 2024, quintiles",
         "fig_map_gdp_pps_2024.png",
         {"Q%d" % (k + 1): pal[k] for k in range(5)})  # Figure 1: choropleth of GDP per inhabitant
brk = [50, 75, 100, 125, 150]
pal2 = ["#b2182b", "#ef8a62", "#fddbc7", "#d1e5f0", "#67a9cf", "#2166ac"]
idx = dict(zip(ids, U.gdp_index))
draw_map(idx, lambda v: pal2[int(np.searchsorted(brk, v))], "GDP per inhabitant, PPS (EU27 = 100), 2024",
         "fig_map_gdp_index.png",
         {"<50": pal2[0], "50-75": pal2[1], "75-100": pal2[2], "100-125": pal2[3], "125-150": pal2[4], ">150": pal2[5]})  # Figure 2
CATS = {"HH": "#b2182b", "LL": "#2166ac", "HL": "#ef8a62", "LH": "#67a9cf", "ns": "#e0e0e0"}
draw_map(dict(zip(ids, cl)), lambda v: CATS[v], "LISA clusters (queen, 999 permutations, p < 0.05 uncorrected)",
         "fig_map_lisa.png", CATS)  # Figure 4: LISA cluster map

fig, ax = plt.subplots(figsize=(5.5, 5))
for g, c in CATS.items():
    if g != "ns":
        m = quad == g
        ax.scatter(z[m], lag[m], s=12, color=c, label=g)
ax.axhline(0, color="grey", lw=.5)
ax.axvline(0, color="grey", lw=.5)
ax.plot([z.min(), z.max()], [slope * z.min(), slope * z.max()], color="black", lw=1)
ax.set_xlabel("Standardised GDP per inhabitant (z)")
ax.set_ylabel("Spatial lag of z (queen, row-standardised)")
ax.legend(fontsize=7)
fig.savefig(OUTPUT_DIR / "fig_moran_scatter.png", dpi=200, bbox_inches="tight")  # Figure 3: Moran scatterplot
plt.close(fig)

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(x, bins=30, color="#2166ac")
ax.set_xlabel("GDP per inhabitant, PPS (EU27 2020), 2024")
ax.set_ylabel("Regions")
fig.savefig(OUTPUT_DIR / "fig_dist_gdp_pps_2024.png", dpi=200, bbox_inches="tight")  # distribution figure
plt.close(fig)

print(pd.DataFrame(main_rows)[["weights", "I", "z", "p_value"]].to_string())
print(res["lisa_counts_uncorrected"], res["lisa_counts_fdr"])
