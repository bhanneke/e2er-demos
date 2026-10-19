# Data Review: Monthly 2 m air temperature, Frankfurt am Main (NASA POWER), 1981-2025

Reviewer: data_reviewer. Scope: source documentation, sample construction, missing values, variable definitions, outliers, measurement quality, time handling, consistency of reported numbers. I checked the draft against the data dictionary, the data summary and the specification. I did not re-run any code. Internal arithmetic was checked by hand.

## Overall assessment

The raw data are clean and well documented upstream. The series has 540 monthly values, no missing values, no -999 fill codes, no duplicates and no calendar gaps. The raw table is kept separate from the clean table. The source file has a SHA-256 hash, and the API version and access date are recorded. The split is fixed by rule (last 36 months), and the climatology is computed on 1981-2010, inside the training window. For a one-series study, that is a sound base.

The weaknesses are mostly in what reaches the paper:
- The manuscript omits several provenance items that exist upstream.
- It has no sample-flow table or summary-statistics table.
- The measurement-quality discussion of a reanalysis product is thin.
- The baseline and interval comparisons depend on construction choices that the text does not state.

None of these invalidates the numbers. Several of them change how the headline "30 percent gain" should be read.

## 1. Source documentation

What the paper does well:
- It identifies NASA POWER, the parameter (T2M) and the coordinates.
- It states that the series is MERRA-2-derived, a grid-cell value and not a station record.
- It states that there is no DWD data.

Gaps:
1. **Version and access date are missing from the paper.** The dictionary records POWER monthly/annual API v2.10.0, accessed 2026-10-13, community RE, and a source-file hash. The manuscript gives none of them. POWER revises data between versions, so a reader who reruns the load later may get different values. Add a data statement with version, access date, community and hash (or a pointer to `data_sources.json`).
2. **The grid is not described.** The paper does not give the cell size (0.5° lat x 0.625° lon, roughly 55 x 40 km at this latitude), the grid-cell elevation (171.6 m) or how the requested point is snapped to a cell. The sentence on elevation differences cannot be assessed without that number. Report the elevation and, if possible, the offset to a reference station.
3. **No MERRA-2 citation.** The text says POWER "derives its meteorological parameters from the MERRA-2 reanalysis" but cites only `NASA_POWER`. Gelaro et al. (2017) is the standard reference. The literature review lists it as not yet in the bib, so it must be registered before the draft cites it.
4. **POWER's referencing guide asks for both the POWER Reference and the Data Reference.** The paper cites only one key. The dictionary's `citation` field contains the full data reference. Include it.
5. **The reason the sample ends in 2025-12 is stated correctly** (whole-year monthly load). The access date is 2026-10-13, so nine further months exist but are excluded. Say that explicitly so it does not look like a choice made after seeing the data. It is also a mild argument for the hold-out being the freshest, least-revised part of the record (see section 6).
6. **Unit of observation and population.** The paper states "monthly, one grid cell", which is enough. It should also say plainly that this is a single series (N = 1 location), so the findings do not generalise spatially. The paper currently says this only as future work.

## 2. Sample construction

- The flow is 540 raw, then 504 train plus 36 hold-out, with nothing dropped. This is stated in prose only. A three-row sample-flow table would let the checks (0 NULL, 0 fill, 0 duplicates, 0 gaps, 0 month-13 rows) be seen at a glance. The "month 13" annual-mean row that POWER returns, and its exclusion, are not mentioned in the paper. Mention them, or state that annual means are recomputed from the twelve monthly values.
- The split is exogenous to the outcome (last 36 months, fixed by the horizon). This is appropriate. The paper should state the rule and not only the dates.
- **The hold-out is used in descriptives.** The decade mean "2021-2025 = 11.19" mixes 2021-2022 (training) with 2023-2025 (hold-out). The full-sample mean (9.94) and the anomaly mean and SD (0.44, 1.90) also include the hold-out. These are descriptive and are not used for model choice, so there is no leakage. But the text should label them as full-sample, and the last "decade" is a five-year block that is not comparable to the others. The data summary itself flags that hold-out figures are shown for description only. The paper should carry that flag.
- **The anomaly SD of 1.90 mixes trend and irregular variation.** It is computed against a fixed 1981-2010 climatology over 1981-2025. A warming trend of about 0.5 °C per decade, plus a positive mean anomaly of 0.44, inflates it. The introduction's "irregular anomalies of roughly two degrees" is therefore an upper bound on the irregular component. It is worth reporting the SD of detrended anomalies, which also gives the noise scale for the interval widths below.

## 3. Missing values and coding

- There are no missing values and no -999 codes. This is verified upstream and stated in the paper. No concern.
- Because the "no missing" claim is a result of a check, cite the check (script and output) or give the counts in a table.

## 4. Variable definitions

- T2M is defined (monthly mean, °C, grid-cell estimate). Missing in the paper: **how POWER aggregates daily to monthly** (simple mean of daily means? of hourly values?). The literature review already flagged this for the data section. State it.
- **The seasonal grouping is ambiguous.** The paper uses DJF, MAM, JJA and SON seasonal means. For 1981, DJF needs December 1980, which is not in the data. Say whether DJF is assigned to the year of January/February, and whether the first winter is dropped or is a two-month mean. This changes n for the winter regression (41 versus 42 versus 43 in the full sample).
- **Annual means in the training regression.** Eq. (1) uses 42 annual means, 1981-2022. Annual means are recomputed from twelve monthly values, which is fine. The slope is expressed per decade as 10 x beta-hat, which is clear.
- Deseasonalising uses month means "in the sample used" (training or full). For the ADF and KPSS this is the training month means, which is consistent with the no-leakage claim. State that the month means for the full-sample trend include the hold-out.
- The climatology window (1981-2010) is fixed in advance and inside the training window. The paper only mentions it in passing. A 1991-2020 WMO normal was planned as a second reference and is not reported. Either report both or say why only one is used.
- No transformations (levels in °C), so the log, winsorising and top-coding issues do not arise.

## 5. Outliers and plausibility of the summary statistics

- Mean 9.94 °C, SD 7.54, minimum -7.03 °C and maximum 24.67 °C are plausible for a Rhine-Main grid cell. The January 1981-2010 climatology of -0.54 °C and the July climatology of 20.11 °C are plausible too. They look somewhat cool compared with what I would expect from the Frankfurt station record. I have not verified this against DWD, so I do not state it as a finding. It is consistent with a reanalysis cell that cannot resolve the urban heat island (see section 6).
- The paper reports no distributional checks beyond mean and SD. Report min, max and, ideally, the extreme months with dates. The coldest month (-7.03 °C) and the warmest (24.67 °C) are single points that bear on the interval-coverage statistics. For a series where the signal is the seasonal cycle, a plot of anomalies with the hold-out shaded (specified in `figure_spec.json`, but not in the manuscript) would serve this purpose.
- The paper includes only two figures (monthly series and annual means). The figures specified upstream (seasonal profile, anomalies) are not in the draft. The researcher's last instruction concerned `fig_seasonal_profile.pdf` having no `source` in `figure_spec.json`. The manuscript does not use this figure, so either include it or drop it from the spec.

## 6. Measurement quality (the main substantive data issue)

1. **Reanalysis versus station.** The manuscript flags this clearly and honestly. It also correctly says that no DWD data are used. What is missing is any quantitative anchor. No external check of level or trend is reported, such as a published DWD value for Hesse or Frankfurt, an ERA5 cell, or a trend from a published station record. Without it, "0.50 °C per decade" cannot be checked for plausibility. A short literature comparison (the Kaspar et al. and DWD climate-report numbers are in the literature review but unverified) would help. At minimum, state that the level and trend are properties of the cell.
2. **Inhomogeneities in the reanalysis.** The plan lists reanalysis breaks from changing assimilated observing systems as a data_reviewer item, and the plan's sensitivity "estimate from 1991 onward" was not carried into the paper. Trend estimates from a reanalysis can be biased by changes in the assimilated observing system, and the paper never mentions it. Add the caveat. If possible, report the 1991-2022 trend as a robustness check. The sensitivity is cheap and the data are already loaded.
3. **Hold-out data may be preliminary.** The hold-out years (2023-2025) are the most recent part of the record. Monthly values near the end of a reanalysis-based product are the most likely to be revised. All headline forecast results are on those 36 months. Say whether POWER marks them as final, and note that a later POWER version may change them.
4. **Urban heat island.** The dictionary says values smooth urban heat. The introduction motivates the question with "municipal heat management" and the plan with Frankfurt as a "recognised urban heat hotspot". The data cannot speak to urban heat. Make sure the policy framing does not suggest it does.
5. **Spatial representativeness** is one cell. Already stated as a caveat. Fine.

## 7. Time handling

- Dates are ISO YYYY-MM. There is no ambiguity.
- The annual cycle is handled with calendar months. Eq. (3) uses cos(2*pi*tau) with tau in elapsed years. Make sure tau = 0 is explicit (January 1981 or mid-January). The phase in degrees depends on this origin, so the "-1.6 degrees" is only interpretable if the origin is stated. The phase change is origin-independent, so this is a presentation point only.
- Month lengths vary, and monthly means are not adjusted for this. This is negligible for temperature.

## 8. Consistency of reported numbers (hand checks)

| Check | Result |
|---|---|
| Full mean from train and hold-out means: (504 x 9.83 + 36 x 11.46) / 540 | = 9.94. Consistent. |
| Decade means 9.09 to 11.19 | Difference 2.10 °C over about four decades. Consistent with 0.50 to 0.54 °C per decade. |
| MASE = MAE / scale: 1.64 / 2.04 | = 0.80. Consistent. |
| RMSE ratio: 1.30 / 1.92 = 0.68; 1.37 / 1.92 = 0.71 | Consistent. "Around 30 percent" is fine. |
| HAC CI: 0.50 +/- 1.96 x 0.083 | = 0.34 to 0.66. The paper gives 0.34 to 0.67. This is slightly wider than the normal interval, so it is probably a t-based interval. State which. |
| Full-sample harmonic trend 0.054 per year vs annual full-sample slope 0.54 per decade | Consistent. |
| 35 of 36 covered | = 97.2 percent. Consistent. |
| Interval width 7.2 to 7.3 °C | Implies a residual SD of about 1.85 °C. This is in line with the anomaly SD of 1.90. Consistent. |

Items that need clarification:
- **Rolling-origin versus hold-out MASE are not like for like.** The seasonal naive MASE is 0.80 on the hold-out and 1.02 in the rolling exercise. The "candidate" MASE is 0.71-0.73 in the rolling exercise and 0.48-0.50 on the hold-out. The text says the rolling advantage is "smaller" than on the hold-out. By RMSE ratio this is 0.71-0.73 against 0.68-0.71, which is a small difference. The text should give the ratio and not leave the reader to infer the size of the gap from MASE values of different bases.
- **Only harmonic and ETS(A,Ad,A) are cited for the rolling exercise.** The specification says rolling origins were run for "harmonic, ETS and seasonal naive". SARIMA is not in it. The paper says "the candidate models" reach 0.71-0.73, which implies all four. Say which models were included.
- **Mann-Kendall variance inflation of exactly one.** A Hamed-Rao correction that leaves the statistic unchanged implies that no autocorrelation lag was significant. This is possible for 42 annual means, but it should be stated as "no significant lags" and the reader should be reminded that this is the low-power case. The Newey-West bandwidth for T = 42 is floor(4 x 0.42^(2/9)) = 3, which is plausible. State the realised L in the text.
- **KPSS with level null on a trending series.** The paper reads ADF rejection plus KPSS rejection as "trend-stationary". The series is deseasonalised but not detrended, so a level-KPSS rejection is expected under a trend. A trend-KPSS (null: trend-stationary) would test the claim directly. This is a methods point more than a data point, but it affects the interpretation of a data diagnostic.

## 9. The baseline comparison depends on construction choices that need stating

1. **Seasonal naive for h > 12.** For h = 13 to 36 the seasonal naive forecast reuses the last observed year (2022) for all three hold-out years. The text defines it as "the value twelve months earlier", which is the h <= 12 case only. The flat error across horizon blocks (1.92, 1.94, 1.89) confirms this. State the definition for all h.
2. **The result is conditional on one reference year.** Seasonal naive uses one year, 2022, as the template. The headline "30 percent" therefore depends on how unusual 2022 was relative to 2023-2025. A single-year baseline is a known noisy comparator. The literature review recommended a climatology benchmark (calendar-month mean of all training years) because seasonal naive carries one year of noise. The plan listed this benchmark as extra, but it is not among the declared models. Without it, the paper cannot say whether the gain comes from "a trend model" or just from "averaging several years". This is the most useful single addition. If the design is frozen and cannot be changed, say so as a limitation.
3. **MASE scale mismatch.** The scale is the in-sample one-year-ahead seasonal-naive MAE. The hold-out seasonal naive errors are at lags of one to three years. A MASE of 0.80 for seasonal naive therefore does not mean "better than in-sample seasonal naive" in the usual sense. This is acceptable but should be explained in one sentence.
4. **Interval width comparison.** The seasonal naive interval is built from the seasonal-lag difference SD scaled by sqrt(number of cycles ahead), so it is wider by construction and grows with horizon. The harmonic regression uses OLS normal intervals that ignore parameter uncertainty and serial correlation. The discussion's claim that a trend-aware model delivers "intervals about half as wide at comparable coverage" mixes model quality with interval construction. Seasonal naive coverage of 100 percent is "conservative", but 35 of 36 for the candidates is not shown to be "better calibrated", since 36 points cannot distinguish 95 from 100 percent either. Tone this down or add an interval score.
5. **The hold-out is warm.** The hold-out mean is 11.46 °C, 1.6 °C above the training mean. The paper already notes that the gain is probably larger than in an average window. The correct reading is that models with a trend or adaptive level win mainly because the baseline's single reference year is cooler than the hold-out. Report the mean error (bias) of each model on the hold-out, as the plan specified, so that the bias and variance contributions can be separated. The bias per model is not in the draft.

## 10. Panel/time-series and survey checks

Not applicable: one series, no weights, no clusters. Serial correlation is handled through HAC errors. The DM test uses 36 overlapping h-step errors, which the paper says limits power. I agree. The paper's wording "statistically indistinguishable" for the four candidates (section Introduction) should read "not distinguishable with 36 months", since failing to reject at n = 36 is weak evidence of equivalence.

## 11. Replication and presentation

- Raw JSON, a cleaned table, hashes and scripts exist upstream. Good. The paper should state where they are (a replication package or repository).
- The paper has **no summary-statistics table** and no sample-flow table. The red-flag list asks for both. The numbers are in `summary_statistics.json`. A single table with N, mean, SD, min, max for the full, training and hold-out samples, plus the month-13 and fill-code checks, would fix both.
- The `% src:` comments tie the numbers to JSON keys. This is good practice. Every number I could trace is consistent with the specification text.
- LaTeX: two `\bibliographystyle` and two `\bibliography` commands (`apalike` with `literature`, then `plainnat` with `refs`). The title and header still read "Untitled Paper", and there is no abstract. The bib check noted that the climate and data references are not registered. These are not data issues, but they would be caught at submission.
- The introduction says the largest estimates are in winter and summer, while Section 4 says the data do not support claims of different rates across seasons. Reword the introduction to "similar across seasons".

## Prioritised requests

1. Add a data statement: POWER API version v2.10.0, access date 2026-10-13, community RE, grid size, grid elevation, daily-to-monthly aggregation, source hash, and both POWER references. Cite MERRA-2.
2. Add a summary-statistics and sample-flow table. Label every hold-out-inclusive number (full-sample mean, anomaly SD, 2021-2025 "decade").
3. Define seasonal naive for h > 12 and explain the MASE scale. Add the climatology benchmark if the frozen design allows, or declare its absence a limitation.
4. Report per-model hold-out bias, and temper the interval-width and "better calibrated" language.
5. Discuss reanalysis inhomogeneity and preliminary end-of-record values. Add a 1991-2022 trend check if it is cheap.
6. Resolve the DJF year assignment for 1981, and state which models entered the rolling-origin exercise and the HAC lag used.
7. Fix the bibliography commands, the title, and the winter/summer wording in the introduction.

OVERALL SCORE: 6.5/10
RECOMMENDATION: Minor Revision
