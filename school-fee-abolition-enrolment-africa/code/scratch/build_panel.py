import json, sqlite3
import numpy as np, pandas as pd

END = 2010  # panel ends at last cohort (2005) + five years, so later abolitions never enter the comparison group
con = sqlite3.connect("data.db")
enr = pd.read_sql("select * from wdi_primary_enrolment", con)
ctl = pd.read_sql("select * from wdi_controls", con)
names = {"SE.PRM.ENRR": "ger_primary", "SE.PRM.ENRR.MA": "ger_male", "SE.PRM.ENRR.FE": "ger_female",
         "SE.PRM.NENR": "ner_primary", "SE.PRM.CMPT.ZS": "completion_rate", "SP.POP.TOTL": "population",
         "NY.GDP.PCAP.KD": "gdp_pc", "SP.URB.TOTL.IN.ZS": "urban_share", "SH.DYN.MORT": "u5_mortality"}
long = pd.concat([enr, ctl])
long["var"] = long["indicator"].map(names)
wide = long.pivot_table(index=["iso3", "year"], columns="var", values="value", aggfunc="first").reset_index()
cn = long.drop_duplicates("iso3").set_index("iso3")["country"]
wide.insert(1, "country", wide["iso3"].map(cn))
wide.columns.name = None
for c in names.values():
    if c not in wide: wide[c] = np.nan
wide["ger_outlier"] = ((wide.ger_primary > 150) | (wide.ger_primary < 10)).astype(int)
wide["log_ger"] = np.log(wide.ger_primary)
n_all = len(wide)
wide = wide[wide.year <= END].copy()

# treatment table: researcher-checked dates from published abstracts (OpenAlex check, 2026-10-13)
iso = sorted(wide.iso3.unique())
SRC = {
 "MWI": (1994, None, "national", "Chimombo 2009, Compare, doi:10.1080/03050060902921003", "high"),
 "UGA": (1997, None, "national", "Kan and Klasen 2020, Review of Development Economics, doi:10.1111/rode.12725", "high"),
 "TZA": (2002, 2001, "national", "Lindsjo 2017, International Journal of Educational Development (no DOI recorded); coded at first fee-free school year Jan 2002, PEDP declared 2001", "high"),
 "KEN": (2003, None, "national", "Oketch and Somerset 2010, CREATE Pathways to Access 37 (no DOI)", "high"),
 "GHA": (2005, None, "national", "Pajibo and Tamanja 2017, doi:10.20448/journal.522.2017.31.53.63", "high"),
 "LSO": (2000, None, "phased from grade 1", "doi:10.1080/09751122.2013.11890101", "high"),
 "RWA": (2003, None, "national", "doi:10.1155/2012/396019", "high"),
 "ZMB": (2002, None, "national", "Concept paper 2020, 'Universal Free Primary Education Policy implemented in 2002' (no DOI)", "low"),
}
prov = {k: v[0] for k, v in SRC.items()}
fa = pd.DataFrame({"iso3": iso})
fa["country"] = fa.iso3.map(cn)
fa["first_year"] = fa.iso3.map(prov)
fa["alt_year"] = fa.iso3.map({k: v[1] for k, v in SRC.items() if v[1]})
fa["abolition_scope"] = fa.iso3.map({k: v[2] for k, v in SRC.items()}).fillna("unknown")
fa["verification_status"] = np.where(fa.first_year.notna(), "published source", "unverified")
fa["source_doi"] = fa.iso3.map({k: v[3] for k, v in SRC.items()})
fa["confidence"] = fa.iso3.map({k: v[4] for k, v in SRC.items()})
fa["provisional_first_year"] = np.nan
fa["notes"] = np.where(fa.first_year.notna(), "researcher-checked published abstract",
                       "no abolition date known: comparison unit, not a verified never-abolisher")
fa.to_csv("data/fee_abolition_years.csv", index=False)
wide.to_sql("wb_primary_enrolment", con, if_exists="replace", index=False)
fa.to_sql("fee_abolition_dates", con, if_exists="replace", index=False)

# sample flow
w = wide
flow = [("country-years 1980-2018 (49 economies x 39 years)", n_all),
        ("end panel in 2010 (last cohort 2005 + 5 years)", len(w))]
w = w[(w.year >= 1985) & (w.year <= END)]; flow.append(("restrict to 1985-2010", len(w)))
w = w[w.ger_primary.notna()]; flow.append(("drop null GER (no imputation)", len(w)))
sf, prev = [], None
for s, n in flow:
    sf.append({"step": s, "n": int(n), "dropped": 0 if prev is None else int(prev - n)}); prev = n
sf.append({"step": "final descriptive sample", "n": int(len(w)), "dropped": 0})
ana = w.copy()

def share(df, c): return float(df[c].notna().mean())
miss = {}
win = wide[(wide.year >= 1985) & (wide.year <= END)]
for c in ["ger_primary", "ger_male", "ger_female", "ner_primary", "completion_rate", "population", "gdp_pc", "urban_share", "u5_mortality"]:
    miss[c] = {"share_nonnull_1985_2010": share(win, c),
               "share_nonnull_1985_1994": share(win[win.year <= 1994], c),
               "share_nonnull_1995_2004": share(win[(win.year >= 1995) & (win.year <= 2004)], c),
               "share_nonnull_2005_2010": share(win[win.year >= 2005], c)}
cov = ana.groupby("iso3").year.agg(["count", "min", "max"])
pre1995 = ana[ana.year < 1995].groupby("iso3").size().reindex(iso).fillna(0)
a = ana.sort_values(["iso3", "year"]).copy()
a["d"] = a.groupby("iso3").ger_primary.diff(); a["gap"] = a.groupby("iso3").year.diff()
jumps = a[(a.d.abs() > 20) & (a.gap == 1)]
gaps = a[a.gap > 1]
out = ana[ana.ger_outlier == 1][["iso3", "year", "ger_primary"]]
out.to_csv("data/ger_outliers.csv", index=False)
jumps[["iso3", "year", "ger_primary", "d"]].to_csv("data/ger_jumps.csv", index=False)

# cohort trends (raw means by first_year cohort)
ana["cohort"] = ana.iso3.map(prov).fillna(0).astype(int)
rows = []
for g, d in ana.groupby("cohort"):
    lab = "undated comparison" if g == 0 else f"cohort {g}"
    for y, dd in d.groupby("year"):
        rows.append({"cohort": lab, "year": int(y), "mean_ger": float(dd.ger_primary.mean()), "n": int(len(dd))})
cm = pd.DataFrame(rows); cm.to_sql("ger_cohort_means", con, if_exists="replace", index=False)
ev = []
for iso3, g in prov.items():
    for _, r in ana[ana.iso3 == iso3].iterrows():
        t = int(r.year - g)
        if -6 <= t <= 8: ev.append({"iso3": iso3, "t": t, "ger": float(r.ger_primary)})
ev = pd.DataFrame(ev)
evm = ev.groupby("t").ger.agg(["mean", "count"]).reset_index()
evm.to_sql("ger_event_time_means", con, if_exists="replace", index=False)
prepost = {}
for iso3, g in prov.items():
    d = ana[ana.iso3 == iso3]
    prepost[iso3] = {"first_year": g, "n_obs": int(len(d)), "n_pre_obs": int((d.year < g).sum()),
                     "n_post_obs": int((d.year >= g).sum()),
                     "mean_ger_pre": float(d[d.year < g].ger_primary.mean()) if (d.year < g).any() else None,
                     "mean_ger_post": float(d[d.year >= g].ger_primary.mean()) if (d.year >= g).any() else None}
con.commit()

def desc(s):
    s = s.dropna()
    return {"n": int(len(s)), "mean": float(s.mean()), "sd": float(s.std()), "min": float(s.min()), "p25": float(s.quantile(.25)),
            "median": float(s.median()), "p75": float(s.quantile(.75)), "max": float(s.max())}
res = {
    "n_observations": int(len(ana)), "n_units": int(ana.iso3.nunique()),
    "n_economies_loaded": int(len(iso)),
    "time_coverage": {"start_year": int(ana.year.min()), "end_year": int(ana.year.max()), "n_periods": 26},
    "outcome": {"ger_primary": desc(ana.ger_primary), "log_ger_primary": desc(ana.log_ger)},
    "other_variables": {c: desc(ana[c]) for c in ["ger_male", "ger_female", "ner_primary", "completion_rate", "gdp_pc", "population", "urban_share", "u5_mortality"]},
    "sample_flow": sf,
    "missingness": miss,
    "countries_with_zero_ger_obs_before_1995": int((pre1995 == 0).sum()),
    "median_ger_obs_per_country": float(cov["count"].median()),
    "ger_outliers_flagged": int(len(out)), "ger_year_jumps_gt20pts": int(len(jumps)), "ger_series_gaps": int(len(gaps)),
    "treatment": {"n_countries_with_published_source_year": len(prov), "n_comparison_units_undated": int(len(iso) - len(prov)),
                  "panel_end_year": END,
                  "pre_post": prepost,
                  "event_time_mean_ger": {str(int(r.t)): {"mean": float(r["mean"]), "n": int(r["count"])} for _, r in evm.iterrows()}},
    "row_counts": {"wdi_primary_enrolment": int(len(enr)), "wdi_controls": int(len(ctl)), "wb_primary_enrolment": int(len(wide)),
                   "fee_abolition_dates": int(len(fa)), "ger_cohort_means": int(len(cm)), "ger_event_time_means": int(len(evm))},
}
json.dump(res, open("summary_statistics.json", "w"), indent=1)

def ser(lab):
    d = cm[cm.cohort == lab]
    return {"label": lab, "x": d.year.tolist(), "y": [round(v, 6) for v in d.mean_ger], "source": {"table": "ger_cohort_means", "columns": {"x": "year", "y": "mean_ger"}, "where": f"cohort = '{lab}'"}}
figs = {"figures": [
    {"filename": "fig_ger_cohort_trends.pdf", "figure_type": "time_series", "label": "fig:ger_cohort_trends",
     "caption_hint": "Raw mean GER by abolition cohort (published-source first_year, panel 1985-2010); undated comparison units are not verified never-abolishers.",
     "series": [ser(l) for l in sorted(cm.cohort.unique())], "x_label": "Year", "y_label": "Mean gross primary enrolment ratio (%)"},
    {"filename": "fig_ger_event_time.pdf", "figure_type": "bar", "label": "fig:ger_event_time",
     "caption_hint": "Raw mean GER in event time for the eight countries with published-source abolition years; composition changes across event times; ZMB is low confidence.",
     "categories": [str(int(t)) for t in evm.t], "values": [round(float(v), 6) for v in evm["mean"]], "y_label": "Mean GER (%)"}]}
json.dump(figs, open("figure_spec.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ["n_observations", "n_units", "sample_flow", "row_counts", "countries_with_zero_ger_obs_before_1995", "median_ger_obs_per_country", "ger_outliers_flagged", "ger_year_jumps_gt20pts", "ger_series_gaps"]}, indent=1))
print(json.dumps(miss)); print(json.dumps(prepost)); print(out.to_string()); print(jumps[["iso3", "year", "d"]].to_string())
