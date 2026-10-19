import sqlite3, json, math
import pandas as pd, numpy as np

con = sqlite3.connect("data.db")
df = pd.read_sql("SELECT * FROM planets", con)
N0 = len(df)
dups = int(df.duplicated("pl_name").sum())
df = df.drop_duplicates("pl_name")


def grp(r):
    if pd.isna(r.pl_rade):
        return "no_radius"
    if isinstance(r.pl_rade_reflink, str) and "CALCULATED_VALUE" in r.pl_rade_reflink:
        return "calculated"
    return "measured_transiting" if r.tran_flag == 1 else "measured_non_transiting"


df["radius_group"] = df.apply(grp, axis=1)
df["rad_limit_flagged"] = (df.pl_radelim.fillna(0) != 0).astype(int)
df["per_limit_flagged"] = (df.pl_orbperlim.fillna(0) != 0).astype(int)
df["in_rp_sample"] = ((df.pl_rade > 0) & (df.pl_orbper > 0)).astype(int)
df["log10_rade"] = np.log10(df.pl_rade.where(df.pl_rade > 0))
df["log10_orbper"] = np.log10(df.pl_orbper.where(df.pl_orbper > 0))
df.to_sql("planets_classified", con, if_exists="replace", index=False)
con.commit()

QN = ["min", "p1", "p5", "p10", "p25", "median", "p75", "p90", "p95", "p99", "max"]


def q(s):
    v = s.dropna().values
    if len(v) == 0:
        return None
    qs = np.quantile(v, [0, .01, .05, .1, .25, .5, .75, .9, .95, .99, 1])
    d = dict(n=int(len(v)), mean=float(v.mean()), sd=float(v.std(ddof=1)) if len(v) > 1 else None)
    d.update({k: float(x) for k, x in zip(QN, qs)})
    return d


groups = ["calculated", "measured_transiting", "measured_non_transiting", "no_radius"]
S = df[df.in_rp_sample == 1]
out = dict(n_observations=int(len(S)), n_units=int(len(S)))
out["time_coverage"] = dict(start_iso=str(int(df.disc_year.min())), end_iso=str(int(df.disc_year.max())),
                            n_periods=int(df.disc_year.max() - df.disc_year.min() + 1))
out["outcome"] = dict(radius_earth=q(S.pl_rade), period_days=q(S.pl_orbper))
flow = [("raw rows in planets (pscomppars)", N0), ("remove duplicate pl_name", len(df))]
d1 = df[df.pl_rade.notna()]
flow.append(("pl_rade not missing", len(d1)))
d2 = d1[d1.pl_orbper.notna()]
flow.append(("pl_orbper not missing", len(d2)))
d3 = d2[(d2.pl_rade > 0) & (d2.pl_orbper > 0)]
flow.append(("pl_rade > 0 and pl_orbper > 0 (radius-period sample)", len(d3)))
out["sample_flow"] = [dict(step=s, n=int(n), dropped=int(0 if i == 0 else flow[i - 1][1] - n)) for i, (s, n) in enumerate(flow)]
assert len(d3) == len(S)

out["duplicates_pl_name"] = dups
miss_cols = ["pl_orbper", "pl_orbperlim", "pl_rade", "pl_radelim", "pl_rade_reflink", "pl_bmasse", "pl_bmassprov", "st_teff", "sy_dist", "tran_flag", "disc_year"]
out["missing"] = {c: dict(n_missing=int(df[c].isna().sum()), share_missing=float(df[c].isna().mean())) for c in miss_cols}
out["radius_group_counts_all"] = {g: int((df.radius_group == g).sum()) for g in groups}
out["by_group"] = {}
for g in groups[:3]:
    G = S[S.radius_group == g]
    out["by_group"][g] = dict(n=int(len(G)), radius_earth=q(G.pl_rade), period_days=q(G.pl_orbper),
                              log10_radius=q(G.log10_rade), log10_period=q(G.log10_orbper),
                              n_radius_limit_flagged=int(G.rad_limit_flagged.sum()), n_period_limit_flagged=int(G.per_limit_flagged.sum()))
out["n_not_in_rp_sample_by_group"] = {g: int(((df.radius_group == g) & (df.in_rp_sample == 0)).sum()) for g in groups}
out["limit_flags"] = dict(radius_nonzero=int(df.rad_limit_flagged.sum()), period_nonzero=int(df.per_limit_flagged.sum()),
                          radius_flag_empty=int(df.pl_radelim.isna().sum()), period_flag_empty=int(df.pl_orbperlim.isna().sum()))
tfs = sorted(df.tran_flag.dropna().unique())
out["crosstab_group_by_tran_flag"] = {g: {str(int(t)): int(((df.radius_group == g) & (df.tran_flag == t)).sum()) for t in tfs} for g in groups}
meths = df.discoverymethod.value_counts()
out["discovery_method_counts"] = {m: int(n) for m, n in meths.items()}
out["crosstab_group_by_method"] = {g: {m: int(((df.radius_group == g) & (df.discoverymethod == m)).sum()) for m in meths.index} for g in groups}
out["calculated_with_tran_flag_1"] = int(((df.radius_group == "calculated") & (df.tran_flag == 1)).sum())
out["tran_flag_0_total"] = int((df.tran_flag == 0).sum())
out["calculated_bmassprov"] = {str(k): int(v) for k, v in df[df.radius_group == "calculated"].pl_bmassprov.fillna("missing").value_counts().items()}
out["calculated_without_mass"] = int(((df.radius_group == "calculated") & df.pl_bmasse.isna()).sum())
out["plausibility"] = dict(radius_gt_25=int((df.pl_rade > 25).sum()), radius_le_0=int((df.pl_rade <= 0).sum()),
                           radius_lt_0p3=int((df.pl_rade < 0.3).sum()), period_lt_0p09=int((df.pl_orbper < 0.09).sum()),
                           period_gt_1e6=int((df.pl_orbper > 1e6).sum()), period_le_0=int((df.pl_orbper <= 0).sum()),
                           mass_gt_13000=int((df.pl_bmasse > 13000).sum()))
ok = df.pl_rade.notna() & df.pl_radj.notna()
ratio = df.pl_rade[ok] / df.pl_radj[ok]
out["unit_check_rade_over_radj"] = dict(n=int(ok.sum()), median=float(ratio.median()), min=float(ratio.min()), max=float(ratio.max()),
                                        n_outside_11p0_11p4=int(((ratio < 11.0) | (ratio > 11.4)).sum()))
mm = df.pl_bmasse.notna() & df.pl_bmassj.notna()
mr = df.pl_bmasse[mm] / df.pl_bmassj[mm]
out["unit_check_mass"] = dict(n=int(mm.sum()), median=float(mr.median()), min=float(mr.min()), max=float(mr.max()))
out["disc_year_counts"] = {str(int(y)): int(n) for y, n in df.disc_year.value_counts().sort_index().items()}


def hist(vals, lo, hi, w):
    edges = np.arange(lo, hi + 1e-9, w)
    c, _ = np.histogram(vals, bins=edges)
    return [dict(lower=float(round(10 ** a, 6)), upper=float(round(10 ** b, 6)), count=int(k)) for a, b, k in zip(edges[:-1], edges[1:], c)]


rl = (math.floor(S.log10_rade.min() * 4) / 4, math.ceil(S.log10_rade.max() * 4) / 4)
pl = (math.floor(S.log10_orbper.min() * 4) / 4, math.ceil(S.log10_orbper.max() * 4) / 4)
out["distributions"] = dict(bin_rule="equal width 0.25 dex in log10; counts sum to n of the group; lower/upper in Earth radii or days")
for g in ["calculated", "measured_transiting"]:
    G = S[S.radius_group == g]
    for name, col, lim in [("radius", "log10_rade", rl), ("period", "log10_orbper", pl)]:
        b = hist(G[col], lim[0], lim[1], 0.25)
        assert sum(x["count"] for x in b) == len(G)
        out["distributions"][f"{name}_{g}"] = dict(n=int(len(G)), bins=b)
json.dump(out, open("summary_statistics.json", "w"), indent=1)


def pts(sub, xcol, ycol, groups=False):
    sub = sub.dropna(subset=[xcol, ycol])
    d = dict(x=[float(v) for v in sub[xcol]], y=[float(v) for v in sub[ycol]])
    if groups:
        d["groups"] = list(sub.radius_group)
    return d


f1 = dict(filename="fig_radius_period_all.pdf", figure_type="scatter", label="fig:radius_period_all",
          caption_hint="Radius against orbital period of all catalogued planets with both values, coloured by radius provenance. Log axes.",
          log_x=True, log_y=True, x_label="Orbital period (days)", y_label="Planet radius (Earth radii)",
          source=dict(table="planets_classified", columns=dict(x="pl_orbper", y="pl_rade", groups="radius_group"), where="in_rp_sample = 1"))
f1.update(pts(S, "pl_orbper", "pl_rade", True))
panels = []
for g, t in [("calculated", "Radius calculated from mass"), ("measured_transiting", "Measured radius, transiting")]:
    p = dict(figure_type="scatter", title=t, log_x=True, log_y=True, x_label="Orbital period (days)", y_label="Planet radius (Earth radii)",
             source=dict(table="planets_classified", columns=dict(x="pl_orbper", y="pl_rade"), where=f"in_rp_sample = 1 AND radius_group = '{g}'"))
    p.update(pts(S[S.radius_group == g], "pl_orbper", "pl_rade"))
    panels.append(p)
f2 = dict(filename="fig_radius_period_by_group.pdf", figure_type="multi_panel", label="fig:radius_period_by_group",
          caption_hint="Radius against period for the two main groups on identical log axes.", ncols=2, panels=panels)


def hp(name, g, xl, title):
    return dict(figure_type="histogram", title=title, bins=out["distributions"][f"{name}_{g}"]["bins"], x_label=xl, y_label="Planets",
                source=dict(results=f"distributions.{name}_{g}.bins", file="summary_statistics.json"))


f3 = dict(filename="fig_marginals_by_group.pdf", figure_type="multi_panel", label="fig:marginals_by_group",
          caption_hint="Marginal histograms (0.25 dex bins) of radius and period for calculated and measured transiting groups.", ncols=2,
          panels=[hp("radius", "calculated", "Radius (Earth radii)", "Radius, calculated"),
                  hp("radius", "measured_transiting", "Radius (Earth radii)", "Radius, measured transiting"),
                  hp("period", "calculated", "Period (days)", "Period, calculated"),
                  hp("period", "measured_transiting", "Period (days)", "Period, measured transiting")])
C = df[df.radius_group == "calculated"]
f5 = dict(filename="fig_mass_radius_calculated.pdf", figure_type="scatter", label="fig:mass_radius_calculated",
          caption_hint="Diagnostic: radius against mass for planets whose radius the archive calculated from mass.", log_x=True, log_y=True,
          x_label="Mass (Earth masses)", y_label="Radius (Earth radii)",
          source=dict(table="planets_classified", columns=dict(x="pl_bmasse", y="pl_rade"),
                      where="radius_group = 'calculated' AND pl_bmasse IS NOT NULL AND pl_rade IS NOT NULL"))
f5.update(pts(C, "pl_bmasse", "pl_rade"))
json.dump(dict(figures=[f1, f2, f3, f5]), open("figure_spec.json", "w"))
keys = ["sample_flow", "radius_group_counts_all", "crosstab_group_by_tran_flag", "calculated_with_tran_flag_1", "tran_flag_0_total", "limit_flags",
        "plausibility", "unit_check_rade_over_radj", "unit_check_mass", "calculated_bmassprov", "calculated_without_mass", "n_not_in_rp_sample_by_group", "missing"]
print(json.dumps({k: out[k] for k in keys}, indent=1))
print(out["crosstab_group_by_method"])
print({g: (out["by_group"][g]["n"], out["by_group"][g]["radius_earth"]["median"], out["by_group"][g]["period_days"]["median"]) for g in out["by_group"]})
