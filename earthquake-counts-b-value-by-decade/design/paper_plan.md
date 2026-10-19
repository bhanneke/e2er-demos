# Paper Plan: Yearly Counts of M≥5 Earthquakes and Stability of the Gutenberg–Richter b-value, 1976–2025

Template: descriptive data study. No causal claims, no identification strategy, no JEL codes (keywords only).

## 1. Phenomenon and motivation

**Phenomenon.** Public and media narratives periodically claim that "earthquakes are increasing". The global annual count of M≥5 events fluctuates visibly (e.g., high-count years after 2004 Sumatra, 2010 Maule, 2011 Tohoku). Whether the count shows any secular trend, or only clustered bursts around great events, is an empirical question that is easy to get wrong if the catalogue's detection threshold and magnitude scale change over time.

**Why it needs explanation.** Seismological theory (stationary Poisson background plus Omori–Utsu aftershock clustering plus Gutenberg–Richter scaling) predicts a roughly stable long-run rate with strongly overdispersed annual counts. A trend in raw counts could therefore reflect (a) real rate changes, (b) catalogue artefacts (magnitude-type conversions, network changes), or (c) a few great-event sequences. A time-varying b-value would be a further sign of either artefact or physical change (e.g., stress-state dependence of b).

**Who cares.** The answer informs how counts are communicated to the public and the media, and what reference rates hazard modellers can use. It also shows how much of an apparent trend is an artefact of the catalogue. The note on magnitude homogeneity also matters to anyone using ComCat for rate analysis.

**Research question.** How has the yearly number of M≥5 earthquakes worldwide changed from 1976 to 2025, and is the b-value stable across decades once completeness magnitude (Mc) is taken into account?

**Contribution type.** New quantification/robustness (descriptive). The contribution is a transparent, fully reproducible audit with explicit sensitivity to Mc method, magnitude type and declustering. It is not a "first to study" claim; the literature on global rate stationarity and b-value is extensive. Closest work to be cited and positioned against by the literature reviewer (to be verified via `e2er-lit search`, not cited from memory):
- Gutenberg & Richter (1944, 1956) for the frequency–magnitude relation.
- Aki (1965) and Utsu (1965, 1966) for the b-value MLE and the two-sample comparison test.
- Wiemer & Wyss (2000) for Mc estimation and b-value stability; Woessner & Wiemer (2005) for Mc uncertainty.
- Marzocchi & Sandri (2003) for MLE with magnitude binning and Mc selection.
- Gardner & Knopoff (1974) and Reasenberg (1985) for declustering; Zaliapin & Ben-Zion (2013) for nearest-neighbour declustering.
- Ekström, Nettles & Dziewoński (2012) for the Global CMT catalogue.
- Michael (2011), Shearer & Stark (2012), and Daub et al. (2012) on whether the clustering of great earthquakes is statistically distinguishable from Poisson. Also Bufe & Perkins (2005), Kagan & Jackson (2011), and Kagan (2010), who argue about apparent global rate variation.
- Positioning check against Michael (2011) (consistency with a Poisson/ETAS null for the annual count) is particularly important.

## 2. Data

**Source: `usgs` (USGS ComCat via the FDSN event web service).** Reasons:
- It is the only seismic catalogue among the permitted sources. Global CMT (GCMT) is not in the permitted list, so the plan cannot rely on it. The data architect must not substitute it; the paper must state this limitation. The Mw-only sensitivity sample in §3.4 is the proxy for GCMT-style homogeneity.
- ComCat holds the ISC-GEM-backed, NEIC-reviewed global M≥~4.5 record. Its coverage of M≥5 is generally complete from the mid-1970s.

**Pull.** `starttime=1976-01-01`, `endtime=2025-12-31 23:59:59` (UTC), `minmagnitude=4.0` (to give buffer below Mc for the Mc estimation, and a lower bound for sensitivity analysis), `eventtype=earthquake`, `orderby=time-asc`. Query in monthly (or finer if the 20,000-event limit binds) slices. Fields kept: id, time, latitude, longitude, depth, mag, magType, net, nst, status, updated, place, type. Download once, store raw, and hash.

**Data checks (the data_quality gate).**
- Units: time in UTC, magnitude dimensionless, depth in km.
- Duplicates: dedupe by event id; flag events within 16 s and 100 km of each other as potential duplicates from multiple contributing networks (report counts removed).
- Missing values: mag, magType, time, lat/lon. Report the number dropped. No imputation.
- Keep only `type == "earthquake"`; drop explosions, quarry blasts, etc.
- Report the magType composition by year (mb, Ms, Mw/Mwc/Mww/Mwr/Mwb, ML, mb_Lg, etc.). Pre-1990 M5–6 events are largely mb/Ms, later ones increasingly Mww. This is the central heterogeneity concern.
- Check the 2025 tail: recent events carry "reviewed" vs "automatic" status; magnitudes may be revised. Report the share of non-reviewed events in 2025 and run counts with and without them. The data pull date is recorded in the paper (today is 2026-10-14, so 2025 should be largely reviewed).

**Magnitude definitions used.**
- **M_pref** (main sample): the ComCat preferred magnitude, whatever type. This is what most users count. Counts at M≥5 use it.
- **M_w-only** (homogeneity sample): events with magType in the Mw family (Mw, Mwc, Mwb, Mwr, Mww). Coverage is nearly complete for M≥5.5 from 1976 on (reflecting the GCMT-contributed moment tensors), and thinner at 5.0–5.5 in early years. This sample is the target of the "Mw-based" requirement. Report its coverage ratio to M_pref per year and magnitude bin, and use it for headline counts above a threshold (M≥5.5, M≥6) where it is complete, with M≥5.0 reported as a separate series with the coverage caveat explicitly stated.
- Do not apply ad hoc regression conversions between magnitude scales in the main analysis. One conversion-based sensitivity (e.g., a published mb→Mw relation, cited) is allowed as a robustness row only, clearly labelled.

## 3. Analysis plan

All estimates are descriptive. Code to be written in Python (pandas, numpy, scipy, statsmodels), seed fixed, to be run as a single script from raw data to tables and figures.

### 3.1 Annual counts (Part 1)

Series: N_t(M≥m) for t = 1976..2025 and thresholds m ∈ {5.0, 5.5, 6.0, 7.0, 8.0}, for M_pref and M_w-only. Primary series: M≥5 (M_pref); and M≥5.5/6 (M_w-only).

Descriptives:
- Mean, median, SD, min, max, and index of dispersion (variance/mean) by decade (1976–85, 86–95, 96–2005, 2006–15, 2016–25), where the fifth decade is 2016–2025 and the first is 10 years.
- Trend description: OLS of count on year (descriptive slope, HAC/Newey–West SE, not a causal effect); Poisson and negative binomial GLM with log link on year (rate ratio per decade); Mann–Kendall test and Theil–Sen slope as non-parametric checks. Piecewise-linear/LOESS smooth for visual shape. Report all specs regardless of result.
- Compare the trend with and without the top-k count years, i.e., leave-out of the years with great earthquakes (the 2004–2005 Sumatra, 2010 Maule, 2011 Tohoku, 2025 Myanmar and Kamchatka sequences are to be verified in the data, not asserted).
- Overdispersion and clustering: (i) Poisson dispersion test (variance/mean, with a parametric-bootstrap p-value) on the raw counts; (ii) the same on the declustered counts (§3.3); (iii) negative-binomial dispersion parameter; (iv) annual share of M≥5 count contributed by the single largest sequence (the aftershock zones of M≥7.5–8 events, defined as events within a time-space window around the mainshock, say 1 year and a magnitude-scaled radius following Gardner–Knopoff); (v) the correlation between annual M≥5 count and the annual seismic moment released by M≥7.5 events, as a descriptive association only.
- Comparison with a simulated null: simulate ETAS-like or simply a stationary Poisson-mainshock-plus-Omori catalogue calibrated to the data and show where the observed annual-count distribution falls (descriptive benchmark; the ETAS parameters are fit by maximum likelihood on the M≥5 catalogue and reported; if too heavy to fit globally, use the declustering-based Poisson-mainshocks-with-aftershock-multiplier simplification and state it).

### 3.2 Gutenberg–Richter b-value and completeness (Part 2)

Model: log10 N(≥M) = a − bM, estimated by maximum likelihood on the exponential tail above Mc.

**Estimator.** Aki/Utsu MLE with binning correction: b̂ = log10(e) / (mean(M) − (Mc − ΔM/2)), with ΔM = 0.1 where ComCat reports 0.1 magnitude steps (check the empirical magnitude resolution by year, because early events can be reported at 0.1 resolution with heaping at x.0 and x.5; report digit-preference diagnostics and, if heaping is severe, estimate on a coarsened ΔM = 0.2 or 0.5 grid as a sensitivity). Standard error: b̂/√N (Shi & Bolt, 1982 variant with the sample variance also reported). Report N used in every window.

**Windows.**
- Decades as above (5 windows).
- Rolling windows: 10-year windows moving yearly (1976–85 … 2016–25), plus 5-year windows moving yearly as a noisier sensitivity.
- Because the sample above Mc≈5 is large (several thousand events per decade), the precision of the b-value should be high; the plan reports the actual precision rather than assuming.

**Mc estimation per window** (never one global Mc):
1. Maximum curvature (MAXC) on the 0.1-bin non-cumulative distribution, plus the +0.2 correction (Woessner & Wiemer 2005) as the default conservative variant.
2. Goodness-of-fit test (GFT, Wiemer & Wyss 2000): the lowest Mc at which the fit to the power law reaches ≥95% (and the ≥90% fall-back).
3. b-value stability (MBS; Cao & Gao 2002): the lowest Mc beyond which b̂ is stable within its uncertainty.
4. Bootstrap uncertainty of Mc (resample events, 1000 reps) per method; report the median and the 2.5–97.5% range.
Primary Mc: the consensus (the maximum of the three, or MAXC+0.2 if they disagree strongly; decide this rule before looking at b results and state it in the paper). The main analysis also fixes a floor Mc ≥ 5.0 (the threshold that the research question uses) as an alternative "fixed-Mc" specification. Sensitivity grid: Mc ∈ {4.5, 4.6, ..., 5.5} for each window, producing a b̂ vs Mc stability plot (Mc-plateau plot).

**Large-magnitude caveats.** Estimate the b-value in the M<7.5 range as well (upper truncation at M_max≈ 7.5–8 using the truncated-GR likelihood, or simply restrict to M ≤ 7.5) so that the few giant events do not dominate the tail; report both truncated and untruncated.

**Joint reporting.** In each window, the table reports Mc (3 methods), N(≥Mc), b̂, SE, bootstrap 95% CI, and the fraction of M_w-type events above Mc.

### 3.3 Stability tests (Part 3)

1. **Bootstrap CIs** for b̂ in each window (1000–5000 resamples of events, re-estimating Mc inside each replicate to propagate completeness uncertainty; also a version holding Mc fixed to show how much of the CI comes from Mc uncertainty). Percentile and BCa intervals.
2. **Utsu (1992/1999) test** for the difference between two b-values: ΔA = −2 (N1+N2) ln(N1+N2) + 2 N1 ln(N1 + N2 b1/b2) + 2 N2 ln(N1 b2/b1 + N2) − 2 ln-terms as in Utsu's AIC form, with the ΔAIC criterion and the associated probability exp(−ΔA/2 − 2)... The precise formula is implemented from the cited primary source, not from memory; unit-tested against a synthetic case with known difference. Apply to all adjacent-decade pairs and all decade pairs (10 comparisons), with Holm correction. Add a permutation version (shuffle the decade labels of events) as a distribution-free cross-check, and a likelihood-ratio test of a common b across the five decades.
3. **Rolling-window changepoint description:** Report the range of b̂ over rolling windows and a CUSUM/Pettitt-type diagnostic of b̂ over time, with bootstrap null bands. Descriptive only.
4. **Sensitivity to Mc choice:** repeat 3.2–3.3 under each Mc method and fixed Mc ∈ {5.0, 5.2, 5.5}; report the min–max of b̂ per decade across specifications and the fraction of specifications in which each Utsu comparison rejects.
5. **Sensitivity to declustering:** apply (a) Gardner–Knopoff (1974) windows, (b) Reasenberg (1985) clustering, (c) Zaliapin–Ben-Zion nearest-neighbour proximity (with the threshold chosen from the data via the mixture-model fit, with the b-value parameter of the proximity itself set to a fixed value and varied ±0.1 as sensitivity). Re-estimate counts (3.1) and b (3.2–3.3) on mainshocks only. Note the known tension: declustering that uses b itself, or magnitude-dependent windows, may bias b̂; report both the declustered and undeclustered results.
6. **Sensitivity to magnitude type:** M_w-only sample (complete only at higher thresholds, so Mc is necessarily higher, ~5.5), and the sample excluding events of type mb/ML. Plus the sample with magnitudes shifted by a published mb→Mw relation as a labelled robustness row.
7. **Sensitivity to location:** drop the regions dominating the great-event sequences (e.g., the Sumatra–Andaman and Tohoku aftershock zones) and re-estimate b̂, to see whether decadal differences reflect a few sequences. Descriptive only.
8. **Synthetic validation:** simulate stationary GR catalogues with known b=1 and with the observed Mc and N per window, with magnitudes rounded to the observed resolution; verify nominal coverage of the bootstrap CIs and the size of the Utsu test (including the effect of estimating Mc). If the size is distorted, report it and calibrate the p-values from the simulated null.

## 4. Figures and tables (specification for the figure_data check)

Each figure is saved as PNG/PDF with a matching CSV of the plotted values, so figures can be re-read against data.

- **Fig 1.** Annual count of M≥5 (M_pref) 1976–2025 as bars, with the Mw-only M≥5.5 and M≥6 counts as lines, a LOESS/Theil–Sen trend overlay, and labelled great-earthquake years. Panel B: the share of the M≥5 count made up by Mw-type magnitudes per year (the homogeneity diagnostic).
- **Fig 2.** Magnitude-type composition of M≥5 events by year (stacked area), and the share of events by contributing network.
- **Fig 3.** Annual counts at M≥5 raw vs declustered, and counts for M≥7 and M≥8, plus a histogram of annual counts against the fitted Poisson and negative-binomial pmf (dispersion illustration).
- **Fig 4.** Frequency–magnitude distribution (cumulative and non-cumulative, log scale) per decade with Mc marked and GR fit overlaid.
- **Fig 5.** Mc by window and method (MAXC, MAXC+0.2, GFT, MBS) with bootstrap bands, on rolling and decade windows.
- **Fig 6.** b̂ over time (rolling 10-yr and 5-yr windows) with bootstrap 95% bands, for the main spec and the sensitivity set (declustered, Mw-only, fixed Mc); horizontal reference at the full-period b̂.
- **Fig 7.** b̂ against Mc (stability plot) by decade.
- **Fig 8.** Utsu-test heat-map of pairwise decade comparisons (ΔAIC or Holm-adjusted p), main spec and a panel for the specification-curve share of rejections.
- **Fig 9 (appendix).** Simulation check: coverage of the bootstrap CI and Utsu test size.

- **Table 1.** Data pipeline: raw events, removals by reason (type, duplicates, missing), final N; magnitude-type composition by decade.
- **Table 2.** Annual-count summary by decade for each threshold: mean, median, SD, dispersion index, max year.
- **Table 3.** Trend estimates (OLS-HAC, Poisson, NB, Mann–Kendall/Theil–Sen), raw and declustered, with and without great-event years. All specifications listed.
- **Table 4.** Mc by decade and method, with bootstrap range; N above Mc.
- **Table 5.** b̂, SE, bootstrap CI by decade, main spec.
- **Table 6.** Utsu tests: pairwise decades, ΔAIC and p, Holm-adjusted, plus the common-b LR test.
- **Table 7.** Sensitivity matrix: b̂ by decade across Mc methods, declustering methods, magnitude samples and spatial exclusions.
- **Appendix tables.** Heaping diagnostics; the ComCat query slices and download date; list of the largest sequences.

## 5. Expected outputs and structure for downstream specialists

- **data_architect:** query `usgs` in slices, write `events_raw`, `events_clean`, and the `data_dictionary.json` (fields, units, filters). State in `unavailable`: Global CMT catalogue (not among permitted sources) and any independent catalogue (ISC-GEM, ISC) for validation of the pre-1990 magnitudes. Record the query URL parameters and the download date.
- **data_analyst:** data-quality checks (§2), the summary statistics, and the figure data for Figs 1–3 as a table; re-read the figures after estimation (figure_data gate).
- **econometrics_specialist:** compute §3.1–3.3 and write `estimation_results.json` in the descriptive results schema (summary statistics, trend tests, b̂ per window, Utsu tests); no regression is claimed as an effect.
- **paper_drafter:** short paper (target ~25 pages with appendix), a natural-science style description; abstract plus keywords only (e.g., earthquake catalogue; Gutenberg–Richter law; b-value; completeness magnitude; seismicity rate; declustering), no JEL line. Frame the conclusions descriptively and explicitly refuse any suggestion that the counts or b-values reflect a cause (climate, human activity, etc.).
- Review panel: literature_reviewer, writing_reviewer, data_reviewer, methods_reviewer, plausibility_reviewer.

## 6. Hypotheses stated before seeing the data (descriptive expectations, not tests of a theory)

H1: The raw M≥5 annual count shows no monotone secular trend that survives removal of the years dominated by great-event sequences; the counts are overdispersed relative to Poisson (dispersion index > 1), and the dispersion falls markedly after declustering.
H2: Once Mc is estimated per window, decadal b̂ values are statistically indistinguishable from each other (b ≈ 1) in the Mw-homogeneous sample; apparent differences in the fixed-Mc, M_pref specifications are explained by Mc/magnitude-type heterogeneity.
H3: Utsu-test rejections are concentrated in specifications with too-low Mc, and in comparisons involving windows with giant-earthquake sequences.
If the data contradict these, report that; no revision of the hypotheses after the fact.

## 7. Risks and limitations

- ComCat is not a homogeneous Mw catalogue: the preferred magnitude type changes over time, and magnitudes in 5.0–5.5 are mostly mb in the early years. Mitigation: Mw-only samples and magnitude-type diagnostics; the main count claims are made at thresholds where Mw coverage is high.
- GCMT is not available; no independent catalogue cross-check. The paper must say so.
- Detection in the 1970s–80s is probably complete at M5 globally but not demonstrably so in remote oceanic regions; Mc per window is estimated globally, not regionally, and a global Mc mixes regions (global FMD is a superposition of regional distributions with different Mc; flag as a limitation and, as a robustness check, compute Mc and b on a regional split such as subduction vs. other, if the data permit).
- Declustering methods are model-dependent and can bias b; both versions are reported.
- b-value estimates with a high Mc truncate and are driven by the upper tail; upper-magnitude truncation and giant events can influence the estimate.
- Counts are rounded magnitudes: events at "M5.0" may be reported at 4.95 in some catalogues; the threshold rule (mag ≥ 4.95 vs ≥ 5.0) is stated, and counts using both are reported.
- Magnitude revisions after the pull date for 2024–2025 events.
- Purely descriptive: no inference about causes of any change.

## 8. Feasibility and target outlet

All data come from one public API (`usgs`); the full pipeline is feasible in 3–6 months for one person, mostly compute-light (bootstrap with re-estimated Mc is the heaviest step). Scores (1–5): data 5, identification n/a (descriptive), novelty 2–3 (careful audit, not a new fact), importance 3, feasibility 5. Suitable outlets are seismology or statistical-geophysics journals (e.g., Seismological Research Letters, Bulletin of the Seismological Society of America, Journal of Seismology) or a data/methods note; not a top economics outlet.
