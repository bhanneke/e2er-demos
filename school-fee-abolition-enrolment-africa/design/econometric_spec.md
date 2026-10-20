# Econometric Specification

(Written before estimation from `identification_strategy.md`, `did_design.json`, `identification_spec.json`, and the researcher's instructions. Realized numbers are filled in at the end under "Results".)

## 1. Data and sample
- Panel: `wb_primary_enrolment` (country-year), 1980-2010 (ends 2010 = last cohort 2005 + 5, so later abolitions never enter the comparison group). 49 units, 1,519 rows; `ger_primary` observed in 1,211.
- Treatment: `fee_abolition_dates.first_year` (published-source dates, verified 2026-10-13): MWI 1994, UGA 1997, LSO 2000 (phased from grade 1), TZA 2002 and ZMB 2002 (ZMB low confidence), KEN 2003, RWA 2003, GHA 2005 (capitation grant). Cohorts: 1994, 1997, 2000, 2002, 2003, 2005 (8 treated countries).
- Comparison: all countries with an empty `first_year`. They are undated comparison units, not verified never-abolishers; contamination would bias towards zero.
- Missing values: country-years with missing outcome are dropped from that outcome's regression (no zero coding). Rows flagged `ger_outlier` are kept in the main specification and dropped in a robustness check. Sample flow (raw rows -> non-missing outcome -> units in the design) is reported in the results.

## 2. Estimands and estimators
Outcome: `ger_primary` (level, % points) and `log_ger` (log points); secondary: `ger_female`, `ger_male`, `ner_primary`.

1. **Main (`main`)**: Callaway-Sant'Anna (2021), no covariates, outcome regression-free (group-time DiD), never-treated (undated) comparison group, anticipation 0, **varying base for pre-periods** and base g-1 for post-periods. Overall ATT = cohort-size-weighted average of ATT(g,t) over t >= g within the event window [0, 5]; dynamic aggregation theta(e) for e in [-6, 5], reference e = -1. Only balanced pairs (units observed in both t and base) are used. Inference: country-level bootstrap (999 draws, fixed seed), SE = SD of draws, pointwise bands, df = G-1 for p-values. Clusters = countries (iso3).
2. **Not-yet-treated** comparison group CS.
3. **Static TWFE** (country and year FE, cluster iso3) as benchmark only, with **Goodman-Bacon decomposition** (weight on already-treated-as-control comparisons) and **wild cluster bootstrap-t (Webb weights)** p-value.
4. **Sun-Abraham** interaction-weighted event study (country+year FE, cohort x relative-period dummies, never-treated control), clustered by country; **BJS imputation** (FE fitted on untreated observations only, effects imputed for treated, bootstrap SE).
5. **Pre-trend test**: joint Wald test on pre-period CS event-time coefficients with the bootstrap covariance, chi2 with k df.
6. **HonestDiD (conservative relative-magnitudes version)**: M = max absolute consecutive change among pre-period estimates, bound for Mbar in {0.5, 1, 2}, and breakdown Mbar. This is the conservative closed-form bound described in the skill, not the exact Rambachan-Roth procedure.
7. **Heterogeneity / secondary outcomes**: CS on `ger_female`, `ger_male` (H4: difference of ATTs, bootstrap of the difference), `ner_primary` (H2: GER vs NER ATT on the same sample, difference), log GER.
8. **Initial level (H3)**: cohort-country ATTs (post minus pre) regressed on pre-abolition mean GER, 8 countries, descriptive. 
9. **Not estimable with the data in data.db**: H5 (capitation grant status by country is not in the warehouse) and H6 (pupil-teacher ratio not loaded; completion rate available only as a partial proxy, estimated as a secondary outcome). This is stated rather than substituted.

## 3. Robustness (sidecar `robustness_results.json` is not requested by the work order; all checks are written into `estimation_results.json` under their own keys)
Anticipation = 1; leave-one-country-out over the 8 treated countries (range of ATT); leave-one-cohort-out-style via the same loop; drop ZMB and GHA; drop flagged GER outliers; add pre-treatment controls (log GDP per capita, urbanisation, measured in the year before abolition, entering CS via a regression-adjusted version: outcome change regressed on pre-treatment covariates among controls, outcome regression DiD); placebo with treatment moved 3 years earlier on pre-treatment data only; window [-5,5].

## 4. Caveats stated up front
Eight treated clusters in six cohorts, five of which have 1-2 countries; GER is subject to denominator error; GER may rise through over-age enrolment (NER check); LSO phased and GHA capitation grants are weaker treatments; a non-rejected pre-trend test is not evidence of parallel trends.

## 5. Results
All numbers from `estimation_results.json` (script `run_estimation.py`, seed 20261013, 999 bootstrap draws; 499 for Sun-Abraham/BJS). Inference: country-level bootstrap SE, t with G-1 = 46 df. Dates are as published; the comparison group is undated, not verified never-abolishers.

**Sample flow.** 1,519 raw rows (49 countries, 1980-2010) -> 1,211 with `ger_primary` (47 countries; 8 treated, 39 comparison) = main N. Missing outcomes dropped, no interpolation. 9 rows flagged as outliers (dropped in a check). No exclusions relative to the registered sample.

**Main (H1).** CS ATT on GER level = 22.04 pp (SE 5.54, p = 0.0002; `estimation_results.json#main.coefficients.att`). Log GER: 0.192 (SE 0.055, p = 0.001; `cs_log_ger`), roughly 21%. Event study (reference -1, universal base): e=0 11.9 (SE 4.9), e=1 23.2, e=2 23.8, e=3 22.0, e=4 24.7, e=5 27.5 (SE 6.3): an immediate jump that persists through year 5, consistent with H1.

**Pre-trends.** Joint Wald test of e=-6..-2: W = 0.76, df 5, p = 0.98. The pre-period coefficients at e=-6..-4 are -5.1, -5.3, -3.6 with SE 5-8: imprecise and drifting slightly negative, so the test has little power; it is not read as evidence of parallel trends. Placebo (dates 3 years earlier, post data dropped): 3.86 (SE 4.70, p = 0.42).

**Sensitivity (HonestDiD, conservative relative-magnitudes bound).** M = 3.27 (largest pre-period change). Overall ATT intervals: Mbar 0.5 [5.5, 38.6]; Mbar 1 [-0.25, 44.3]; Mbar 2 [-11.7, 55.8]; breakdown Mbar = 0.98. The effect is robust to post-trend violations up to roughly the size of the largest pre-period change, not beyond.

**Estimator checks (level ATT).** Not-yet-treated 22.12 (SE 5.58); anticipation = 1 21.84 (6.26); Sun-Abraham 22.03 (5.74); BJS imputation 22.73 (10.26); static TWFE 23.37 (cluster-robust SE 9.70, p = 0.020; wild cluster bootstrap-t p = 0.062); TWFE log GER 0.150 (SE 0.108, wild p = 0.21). TWFE is benchmark only. The Sun-Abraham and BJS SEs are unit (pairs) bootstrap SEs, not wild bootstrap; the wild bootstrap is run for TWFE only.

**Goodman-Bacon.** Only 13 countries have complete GER for 1985-2010 (treated: LSO, TZA, UGA; 10 comparison), so the decomposition is on this balanced subsample; it reproduces the balanced-panel TWFE coefficient exactly (17.07). 95.6% of weight is on treated-vs-never comparisons, 2.5% early-vs-later-control and 1.9% on later-vs-already-treated comparisons: negative-weighting is not a concern in this subsample. It does not describe the full unbalanced sample.

**Gender (H4).** Female ATT 21.60 (SE 5.38), male 21.40 (SE 5.99), difference 0.20 (SE 2.71, p = 0.94): no evidence that girls gained more.

**Net enrolment (H2).** NER ATT 13.45 (SE 3.93, p = 0.001) on 684 observations; GER on the same NER-observed sample 14.78 (SE 3.63); GER minus NER 1.33 (SE 2.48, p = 0.59). The sign matches the over-age hypothesis but the difference is not distinguishable from zero; NER is sparse (few pre-period observations for several treated countries), so the NER sample is selected.

**Initial level (H3).** Country ATTs regressed on mean pre-abolition GER (5 years), 8 countries: slope -0.71 (HC3 SE 0.48, p = 0.18, df 6). Negative as predicted, imprecise. Country ATTs range from 8.9 (KEN) to 51.8 (UGA); MWI 41.5.

**Robustness.** Leave-one-country-out ATT ranges from 17.46 (dropping UGA) to 24.06 (dropping KEN). Dropping ZMB and GHA: 24.35 (SE 7.08). Dropping flagged outliers: 21.17 (SE 5.59). Pre-treatment controls (log GDP pc, urban share at g-1): 19.11 (SE 5.33). Window [-5,5]: identical ATT (22.04), since the overall ATT uses e>=0 only.

**Not estimated.** H5 (capitation-grant status is not in data.db) has no result entry. H6: pupil-teacher ratios are not in the data; the completion rate is reported as a partial proxy (ATT 5.83, SE 3.84, p = 0.14), which rises by less than enrolment (22.0), consistent with the direction of H6. Randomization-inference p-values and never-treated fake-date placebos listed in the pre-registration were not run. The covariate-adjusted spec uses an outcome-regression CS, not doubly robust.
