# Data Review: Yearly M>=5 earthquake counts and Gutenberg-Richter b-value stability, 1976-2025 (USGS ComCat)

Scope of this review: the data source, sample construction, cleaning, variable definitions, measurement quality, internal numerical consistency, and the way the data limit what the paper can say. I had the draft text, the data dictionary, the data summary and the analysis specification. I did not have the table files (`tables/*.tex`), `estimation_results.json`, `data_quality.json` or the figures. Every check below is therefore against numbers quoted in the text or in the supporting documents.

## 1. Overall assessment

The data work is above average for a descriptive study. The source is identified with a DOI. The five-file load is documented with URLs and hashes. The cleaning is rule-based and the removed rows are counted by type. The paper does not hide the heterogeneity of the catalogue. It reports the magnitude-type mix by decade, keeps aftershocks and says so, flags the censoring of Mc at the load floor, and reports the pairs where the likelihood-ratio test and the bootstrap disagree.

Most of the arithmetic I could verify holds (section 3). The main weaknesses are structural and come from the data design:

- The research question asks about the b-value "once the completeness magnitude is taken into account". For three of the five decades, Mc cannot be located because the load floor of M4.5 coincides with the estimated maximum-curvature mode.
- The headline b-values and standard errors treat about 280,000 clustered, serially dependent events as independent.
- The 50 annual values behind the count claims are summarised only by decade means, with no uncertainty attached to those means.
- One pair of estimates looks suspicious and should be checked in the code (section 4.4).

## 2. Source documentation and sample construction

**Strengths**
- The source, DOI, catalogue citation, geographic scope (worldwide), time coverage (1976-01-01 to 2025-12-31 UTC), unit of observation and the half-open load windows are all documented. The raw row counts are consistent across documents: 37,121 + 42,573 + 50,984 + 73,394 + 74,436 = 278,508.
- The sample flow reconciles: 278,508 raw rows, minus 561 non-earthquakes, minus 1 row without a usable magnitude, leaves 277,946. The sum of the decade counts (36,781 + 42,441 + 50,975 + 73,390 + 74,359) is also 277,946.
- The removals by decade are plausible. Nuclear explosions are 329 in 1976-85 and 130 in 1986-95. Volcanic eruptions (71) fall in 2016-25.
- Duplicates by `id` were checked (none found).

**Issues**
1. **Data vintage and load date are missing from the paper.** The data summary says ComCat events are revised after review and that 2025 may still change. The text gives no retrieval date. The status split (reviewed/automatic share per year, at least 99.5% reviewed) appears only in the data summary. A one-sentence vintage statement with the load date and the reviewed share belongs in Section 3. The checksums in the dictionary show that the load is reproducible, but ComCat itself is a moving target.
2. **Near-duplicates are not mentioned in the paper.** The data step flagged 211 near-duplicate pairs (within 16 s, 100 km and 0.5 magnitude units), mostly us-us, and kept them. The paper says only that there are no repeated identifiers. This is small relative to 278k events, but it is exactly the case of a single event carried under two ids. Report the 211 pairs and say they were kept.
3. **Events with no magnitude are unobservable.** The dictionary notes that the request filters on magnitude, so null-magnitude events cannot enter the raw tables. The paper says "one row with no usable magnitude" was removed. It should add that null-magnitude events excluded by the server cannot be counted.
4. **Explosion screening is label-based.** Removal depends on ComCat's `type` field. Early nuclear tests (mb 5-6) that carry an `earthquake` label would inflate early mb counts. This is probably minor, but the paper should say that screening is only as good as the label. 470 labelled nuclear explosions in the first two decades is large relative to the M>=6 counts of those decades.
5. **No sample-size or power concern.** Every decade has more than 13,900 events at M>=5. The informative sample size is not the issue. The dependence of events is (section 5).

## 3. Numerical consistency checks I could perform

| Claim in text | Check | Result |
|---|---|---|
| Mean annual M>=5 count 1,669.4; 83,469 / 50 | arithmetic | consistent |
| Overall dispersion index 56.7 | 307.8² / 1669.4 = 56.8 | consistent |
| Dispersion 5.4 (1986-95), 69.2 (2006-15) | 93.1² / 1617.4 = 5.4; 371.4² / 1992.8 = 69.2 | consistent |
| 2006-15 vs 1976-85 "about a quarter higher" | 1992.8 / 1595.9 − 1 = 0.249 | consistent |
| Decade M>=5 totals vs means | 15,959 / 16,174 / 13,906 / 19,928 / 17,502 sum to 83,469 | consistent |
| Mw-family share by decade (10 / 48 / 77 / 63 / 59 %) | implied Mw M>=5 events sum to about 42,950 vs reported 42,956 | consistent |
| 51% Mw over the whole period | 42,956 / 83,469 = 51.5% | consistent (rounds to 51 or 52; state the rounding) |
| 77% shallow (<=70 km) | 214,156 / 277,946 = 77.05% | consistent |
| Shi-Bolt SE 0.006-0.008; Aki 0.0059 vs 0.0063 (1996-2005) | b/sqrt(N) = 1.055 / sqrt(31,143) = 0.0060 | consistent |
| Bootstrap CIs 1.006-1.034 and 1.151-1.173 | about ±1.96 SE | consistent |
| LR statistics 2.4 (2006-15 vs 2016-25), 7.6 (1976-85 vs 2006-15) | normal-approximation z² with these b and N: about 2.7 and 7.3 | consistent in magnitude |
| Common-threshold N (1976-85) = 20,023 vs count mean 2,002 at 4.9 | 20,020 vs 20,023 | consistent (the binned and published thresholds agree here) |
| Spearman 0.27 with p = 0.053 vs Poisson slope CI 0.13-0.68 excluding zero | different tests | different verdicts; discussed in section 5.3 |

Two small points came out of this:

- **Count rule versus binned rule.** Counts use published `mag >= t`. Mc and b use magnitudes rounded to 0.1. The earlier script version gave 83,543 events at the binned 5.0 against 83,469 at the published 5.0, so 74 events (0.09%) differ. The effect is immaterial, and the paper's treatment of the 909 two-decimal events is correct. State the size of the difference (74 events) rather than only the 909 and 96 counts.
- **Binning of two-decimal values.** Rounding a value like 4.95 to 5.0 sits on a bin edge. Say how ties were rounded (half-up or half-even). It affects the 96 events between 4.9 and 5.0 only.

## 4. Completeness magnitude and b-value: data-quality concerns

### 4.1 Mc is censored in three of five decades, so the central question is only partly answered
- The maximum-curvature mode is 4.5 (the load floor) in 1996-2005, 2006-2015 and 2016-2025. Both goodness-of-fit rules also return 4.5 there. A mode at the lower truncation point of the data carries no information about where the catalogue becomes complete.
- Adding 0.2 to a censored mode (giving 4.7) is arbitrary. Yet 4.7 is the "decade-specific Mc" behind the abstract's 1.02-1.16 range.
- The paper acknowledges censoring, but the headline conclusion still reads as if Mc had been accounted for in every decade. The decade-specific comparison mixes Mc = 4.9, 4.7 and 4.5. Differences in b across decades are therefore confounded with differences in threshold by construction. The common-threshold and fixed-5.0 variants are the only clean comparisons. They should be the primary result, not a sensitivity.
- The scope decision to load from 4.5 is the researcher's. I would still say plainly that it cannot be checked whether the catalogue is complete at 4.5, 4.6 and so on in the later decades without events below 4.5. Even a one-off load of M>=4.0 or 4.2 for 2016-25, restricted to the contributing network `us`, would settle whether the mode at 4.5 is truncation or completeness. If the load is not extended, the paper should state that Mc for 1996-2025 is "at most 4.5", not "4.7".

### 4.2 Non-monotone behaviour of b with respect to Mc points at bin-level irregularities
- 2016-25: b = 1.162 at 4.7, 1.220 at 4.9, 1.150 at 5.0.
- 1996-2005: b = 1.055 at 4.7, 0.924 at 4.9, 0.927 at 5.0.
- 1976-85: 1.123 at 4.9, 1.166 at 5.0, 1.191 at 5.1, 1.175 at 5.2.

A move of 0.07 between 4.9 and 5.0 is about nine standard errors. Incompleteness cannot produce a decline in b with rising Mc. These swings are more consistent with irregular bin populations near 4.9 and 5.0, caused by magnitude rounding and heaping, reporting-threshold rules in the contributing networks, or a switch between magnitude scales near M5.

The paper's reading ("a distribution whose slope changes near magnitude 5") is one possible reading. The original plan promised digit-preference and heaping diagnostics and a frequency-magnitude plot per decade with Mc marked. Neither is in the draft, and the data summary confirms they were not produced. I consider these the most valuable missing items:

- a table or figure of the binned frequency-magnitude distribution (counts per 0.1 bin, 4.5-6.0) by decade and by magnitude type;
- a digit-preference check (share of events at x.0 and x.5);
- b versus Mc plots for all five decades. Table `mc_shift` exists, but the shape is not visualised.

### 4.3 Magnitude-type heterogeneity inside the "preferred magnitude"
- The preferred magnitude mixes mb, Ms and several Mw variants (mww, mwc, mwb, mwr, and mwp, a rapid P-wave estimate), each with different saturation, rounding and noise. The "Mw family" is therefore itself heterogeneous. The Mw share of M>=5 events is non-monotone (10, 48, 77, 63, 59%) while the Mw share at M>=4.5 is lower and also non-monotone. This indicates changes in contributing-agency and NEIC procedure rather than a smooth transition.
- Decade aggregation hides where these changes happen. The annual magnitude-type counts already exist in `eq_annual_counts` (`n_m50_mw`, `n_m50_mb`, `n_m50_ms`). An annual stacked share, with breaks marked, would let the reader see whether the 1996-2005 dip or the 2006-2015 peak coincides with a procedure change. It needs no new analysis.
- The paper should state, from USGS documentation, how the preferred magnitude was chosen in the PDE period (for example whether it is mb or Ms depending on size). Selection of the larger of two scales would bias counts at a fixed threshold. I could not verify the rule from the supplied material, so the author should check and state it.
- The draft's interpretation that mb saturation explains the low early M>=6 counts is plausible. It is labelled as unverifiable from the catalogue, which is the right level of claim.

### 4.4 A coincidence in the estimates that should be checked in code
For 1996-2005, the maximum-curvature +0.2 estimate (Mc = 4.7) is 1.055. The 95% and 90% goodness-of-fit estimates (Mc = 4.5 per the text) are also 1.055. For 2006-15 the corresponding values differ (1.149 vs 1.108). Equality to three decimals between estimates at different thresholds, which use different numbers of events (31,143 at 4.7 against about 50,975 at 4.5), is not plausible unless the code assigns the same Mc to both rules in that decade. Please check:

- the Mc actually used for `decade_mc_gft95` and `decade_mc_gft90` in 1996-2005;
- whether Table `bvalues_gft95` shows 4.5 and N = 50,975 there.

If the values coincide for a legitimate reason, say so. If not, fix the table and the sentence that lists "1.123, 0.981, 1.055, 1.108 and 1.226".

### 4.5 Estimator and goodness-of-fit rule
- The GFT percentages (94.0-98.8% at 5.0) are descriptive measures of fit, not tests. The paper uses them to say the catalogue is "complete" at 5.0. Say "consistent with completeness under the GFT rule".
- "Complete at 5.0 in every decade" is also used as the justification for the fixed-5.0 variant. Yet the same variant gives estimates from 0.927 to 1.166, so completeness at 5.0 does not by itself deliver stability. The text handles this correctly. It should avoid reading the GFT as evidence on stationarity.

## 5. Uncertainty, dependence, outliers

### 5.1 Reported precision is far too narrow, and the paper only partly says so
- The Shi-Bolt, Aki and bootstrap intervals all assume independent events. Aftershock sequences of the largest earthquakes (2004, 2010, 2011, among others) can contribute thousands of events to a single decade. The paper acknowledges this in the Discussion. The headline in the abstract ("rejects equality at the 1 percent level in nine of ten pairs") still carries no caveat.
- Add the caveat to the abstract and to the first mention of the test in Results.
- A cheap fix inside the declared scope (no declustering needed): a block bootstrap that resamples whole calendar years within a decade (10 blocks) or whole months. It gives a dependence-aware interval, even if wide.
- A leave-one-year-out b for each decade shows directly whether one year with a great sequence moves the estimate. The checklist item "does dropping any single unit change the results" has not been addressed. Region exclusion was dropped by instruction. Dropping single years is not region exclusion and is nearly free.

### 5.2 Mc uncertainty is not propagated
Bootstrap intervals hold Mc fixed. Mc is itself estimated per decade and per rule, and it is censored in three decades. The paper's own shift table shows that moving Mc by 0.1 changes b by more than the reported intervals. State this next to the intervals.

### 5.3 Counts: decade means without uncertainty
- The rule "describe a change only where the decade means show it" is applied without any measure of uncertainty on a decade mean. With 10 annual values and SDs from 93 to 371, the standard errors of the decade means range from about 30 to 120. Differences such as 1,596 vs 1,750 (+9.7%) are of that order.
- The paper's claim of "no persistent direction" is mostly a statement about 2006-15 vs 2016-25. At the common threshold of 4.9 the last decade (2,449) is 22% above the first (2,002) and higher than the first three decades, and the rank correlation is 0.51. At M>=5 the last decade (1,750) is also above the first three. The conclusion that there is no increase therefore holds at M>=5 in a narrow sense. At 4.9 the evidence is more mixed, and the difference between thresholds 4.9 and 5.0 deserves a sentence in the Conclusion.
- Add a standard error or interval for each decade mean (bootstrap over years), or a table of all 50 annual counts in an appendix. A year-level table would also let readers see the minimum of 1,077 (1998) and the minimum of 1,259 in the first decade, which are not discussed. The first years of the record may reflect catalogue ramp-up rather than seismicity.
- The Poisson-regression interval excludes zero while the Spearman p-value is 0.053. The paper correctly refuses to read the slope as a trend. The Poisson interval uses heteroskedasticity-robust errors, which do not correct for serial correlation. Use HAC or a year-block bootstrap, or drop the interval and report only the point slope.
- The attribution of the 2010 and 2011 peaks to aftershock sequences is stated as untested and sourced to the figure spec. That is acceptable. Do not call 2010 and 2011 the years with "the largest counts" without a ranked table. The second-ranked year should be confirmed from `eq_annual_counts`.

### 5.4 Outliers
Magnitude range (4.5 to 9.1) and depth range (-3 to 700.9 km) pass the range checks. The 128 events with negative depth are immaterial for the shallow split. No data errors in magnitude were found. There is no winsorising or trimming, and none is needed for counts. The few great earthquakes do matter for the upper tail of the FMD. The b estimator is computed on all magnitudes above Mc with no upper cut-off, so the 9.1 events enter the mean magnitude. The original plan proposed an upper-magnitude truncation sensitivity (for example M<7.5). A one-line check would show whether b changes. It is not in the scope list, so I flag it as optional.

## 6. Subsample checks

- **Mw-only sample.** Mc of 5.2-5.6, N = 857 in the first decade, 50,274 events overall. The Mw-assigned population is selected: moment magnitudes are computed mostly for larger or more significant events. Its FMD below the threshold is shaped by that selection. The paper's decision to report b only at its own Mc and not at the common threshold is correct. The comparison with the full sample is then "different thresholds, different population", and the paper says so.
- **Shallow sample.** 214,156 events. Reproducing the full-sample pattern is informative. The shallow cut-off of 70 km is a standard split but is not justified in the text. One sentence on why 70 km would help.
- The Mw-only estimates for the two latest decades (0.921, 0.995) contradict the full-sample rise, which the paper shows. Conclusions in the abstract ("the data cannot separate physical change from catalogue change") are appropriately worded.

## 7. Variable definitions, units, time

- Units are stated for depth (km) and magnitude (with type). The year is a UTC calendar year, stated. There are no monetary variables.
- Decade windows are consistently defined (10 calendar years). The 2025 end date is complete to 2025-12-31T23:04Z.
- Binning: "ΔM = 0.1" and the correction use a bin-centre convention. State that bins are centred on the rounded value and that Mc is a bin centre. Otherwise the correction of Mc − ΔM/2 can be misread.
- The "common threshold" is introduced as 4.9, derived from the largest decade value of maximum curvature +0.2. Give the thresholds in one place (a small table: Mc rule x decade) so that the reader can see which decade is censored at which value.
- Quantiles in the summary table use linear interpolation; this is stated.

## 8. Reproducibility and presentation

- The pipeline is well documented. Each number in the text has a source comment. The `tables/*.tex` and `estimation_results.json` fields could not be checked here. The figure check should confirm that Figure 2 (magnitude-type mix) matches the decade shares quoted (10, 48, 77, 63, 59%).
- Required additions to the paper itself: (a) the load date, (b) a sample-flow table (it exists in the data summary, and the text gives the numbers but a table is clearer), (c) the near-duplicate count, (d) a figure or table of the binned FMD by decade, (e) b versus Mc plots, (f) decade-mean intervals.
- The data summary says three further figures (FMD per decade, b with intervals, Mc over time) were not produced. The draft has two figures, with no figure showing the b-values at all. A descriptive paper whose main finding is a b-value comparison needs a b-by-decade figure with intervals for the main specifications.

## 9. Prioritised list of requests

1. Check the identical 1.055 values for 1996-2005 (maximum curvature +0.2 at 4.7 versus GFT at 4.5), and correct tables or text if the Mc is mislabelled (4.4).
2. Present the common-threshold and fixed-5.0 comparisons as the primary result. Describe the decade-specific Mc comparison as confounded by censored Mc in 1996-2025 (4.1).
3. Add the binned FMD by decade, digit-preference/heaping diagnostics and b versus Mc plots, to test whether the 4.9-to-5.0 swings are bin irregularities (4.2).
4. Add a year-block bootstrap (or a leave-one-year-out b) and a caveat in the abstract on the dependence of events (5.1).
5. Add uncertainty to decade means of annual counts, and temper the "no increase" wording for the 4.9 threshold (5.3).
6. State the data vintage and load date, the near-duplicate count, the null-magnitude limitation, and how the PDE-period preferred magnitude was chosen (2, 4.3).
7. Show the annual magnitude-type shares (data already in `eq_annual_counts`) to locate procedure changes (4.3).
8. Optional: sensitivity of b to an upper magnitude cut-off and to Mc propagation (5.2, 5.4).

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
