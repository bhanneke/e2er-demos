# Identification Strategy

## 1. Causal claim
Abolishing tuition and mandatory fees in public primary schools raised the gross primary enrolment ratio (GER) in sub-Saharan African countries, because removing direct costs lowers the price of schooling for households at the margin of enrolling. The estimand is the average effect on the treated countries (ATT) by years since abolition, aggregated over adoption cohorts.

## 2. Identifying variation
Staggered adoption between the mid-1990s and mid-2000s. Within a country, GER after abolition is compared with its own pre-abolition GER, relative to the same change in countries that have not (yet) abolished fees. Country and year effects are absorbed by the estimator (differencing against a base period and a comparison group).

**Treatment timing.** `first_year` is the first calendar year in which the school year starts with fees abolished nationally in public primary schools. Policies announced in an election campaign or decree but implemented later are dated by implementation; the announcement year goes in a separate column (`announce_year`) used for anticipation checks. Partial or regional abolitions, fee reductions and capitation-grant-only reforms are not treated and are listed as ambiguous cases for robustness. The dates must come from published sources (Kattan and Burnett 2004; Grogan 2009; Morgan et al. 2014; country studies such as Kan and Klasen 2020), at least two per country, retrieved by the data pipeline and cited. They are not filled in from memory here. They are stored in the data.db table `fee_abolition_dates`, never typed into the estimation script. Countries without a documented nationally binding abolition in the window are never treated.

**Sample window.** 1985-2015, sub-Saharan countries with GER data in the World Bank WDI (SE.PRM.ENRR). Each cohort needs at least 3 observed pre-years (the design check requires 2). Event window [-6, 8], reference period -1. Always-treated countries (abolished before the panel) are excluded.

## 3. Estimators
- **Main:** Callaway-Sant'Anna, no covariates, never-treated comparison group; cohort-size weighted ATT over t >= g plus event-time aggregation. The base period (varying or universal) is stated in the results.
- **Checks:** not-yet-treated comparison; Sun-Abraham (country and year FE); Borusyak-Jaravel-Spiess imputation; Gardner two-stage.
- **Benchmark only:** static TWFE with Goodman-Bacon decomposition, showing the weight on already-treated-as-control comparisons and explaining any gap to the main estimate. TWFE is not the headline estimate (staggered timing).

## 4. Inference
Few treated clusters (cohorts of 1-6 countries). Main standard errors: country-level bootstrap, at least 999 draws, fixed seed, pointwise bands. Wild cluster bootstrap-t (Webb weights) for TWFE and Sun-Abraham as the small-cluster check, with the number of treated clusters reported.

## 5. Threats and responses
1. **Anticipation (campaign announcements).** Run anticipation = 1 (base period g-2); report leads at -1 and -2; re-date by announcement year.
2. **Endogenous timing (enrolment trends, donor support, HIPC relief).** Event-study leads and a joint Wald pre-trend test; Rambachan-Roth sensitivity (relative magnitudes, Mbar 0.5, 1, 2, and the breakdown value) reported whatever the pre-test shows; placebo with treatment moved 3 years earlier on pre-treatment data; covariate-adjusted Callaway-Sant'Anna using pre-abolition GER level and trend. A non-rejected pre-test is not read as proof of parallel trends (low power).
3. **Concurrent shocks (EFA, Fast Track Initiative, HIPC, conflict, GDP, aid).** Year effects remove common shocks only. Robustness: pre-treatment log GDP per capita and aid per capita as covariates (no post-treatment controls); drop conflict country-years; drop late cohorts; regional comparison restriction.
4. **Data breaks and GER measurement error (population denominators).** Also use log GER, enrolment counts (SE.PRM.ENRL), net enrolment where available; winsorize at 1/99%; drop flagged breaks and countries with fewer than 15 observations. Denominator error biases estimates only if it is correlated with adoption timing; this cannot be verified.
5. **Few treated clusters, spillovers.** Wild bootstrap; leave-one-cohort-out and leave-one-country-out. Cross-border spillovers to comparison countries would bias towards zero.
6. **Unbalanced panel.** Callaway-Sant'Anna uses balanced pairs; the main sample is also re-run on a balanced panel.

## 6. Pre-registered robustness checks
(a) not-yet-treated comparison; (b) Sun-Abraham, BJS, Gardner; (c) anticipation = 1; (d) announcement-year dating; (e) leave-one-cohort-out and leave-one-country-out; (f) drop conflict years; (g) log GER and enrolment counts; (h) window variants (1990-2012, [-5,5]); (i) fake-date placebo and never-treated fake dates; (j) HonestDiD relative-magnitudes bound; (k) Goodman-Bacon decomposition; (l) wild cluster bootstrap.

## 7. Estimand and external validity
ATT for countries that chose to abolish, at their adoption date. GER can rise through over-age and late entry, so effects need not equal gains in net enrolment; the net enrolment check addresses this. Effects likely differ by initial enrolment; cohort heterogeneity is reported.

## 9. Revision after the did_design check (no treated unit)
The check found no treated unit: `fee_abolition_dates.first_year` is empty for all 48 countries, because no date has been verified against a published source and none is filled in from memory. The design now reads timing from `fee_abolition_dates.provisional_first_year`, which holds candidate years for five countries (Malawi 1994, Uganda 1997, Tanzania 2002, Kenya 2003, Ghana 2005). These years come from the project paper plan and are **unverified**; a web search to confirm them could not be run in this revision.

- The treated set is five countries in five single-country cohorts, so inference rests on very few treated clusters. The wild bootstrap and leave-one-cohort-out checks in sections 4 to 6 are central.
- The comparison group is the 43 countries without a candidate date. Some may have abolished fees in the window, so they are undated, not verified never-treated. Contamination biases estimates towards zero; the not-yet-treated check is reported alongside the main estimate.
- Every result is conditional on the provisional dates. Each must be confirmed against the sources in section 2, and the table updated, before an estimate is treated as final. A country whose date cannot be confirmed is dropped from treatment.
- The event window is narrowed to [-6, 5] to match the post-periods available for the latest cohort (2005).

## 10. Revision after the second did_design check (still no treated unit)
The check again found no treated unit: the design read `provisional_first_year`, which the check did not see as treatment dates, and `first_year` was empty. The researcher has since verified eight dates against published abstracts (2026-10-13). The design now reads `fee_abolition_dates.first_year`, which the data analyst fills for these eight countries with `verification_status = 'published source'` and `source_doi`. This supersedes section 9.

- **Cohorts (8 treated countries):** 1994 MWI; 1997 UGA; 2000 LSO (phased from grade 1, so the effect on the national GER is likely diluted in early years); 2002 TZA and ZMB (TZA coded at the first fee-free school year, alt_year 2001; ZMB confidence low); 2003 KEN and RWA; 2005 GHA (capitation grant scheme, a weaker form of abolition). Dates are used as published, not from memory.
- **Comparison group:** the remaining countries have an empty `first_year`. They are undated comparison units, not verified never-abolishers; some may have abolished fees without our knowing, which would bias estimates towards zero. The panel `wb_primary_enrolment` ends in 2010 (last cohort plus five years), so abolitions after 2010 cannot enter the comparison group. This rule is recorded in `data_summary.md`.
- **Pre-periods:** the panel starts in 1980, so even MWI (1994) has 14 potential pre-years, subject to GER availability.
- **Event window:** [-6, 5], reference period -1; GHA 2005 + 5 = 2010 fits the panel end. Inference with 8 treated clusters rests on the bootstrap and leave-one-cohort-out checks; anticipation = 0 as main, 1 as robustness (TZA 2001 declaration is the natural test). Robustness drops ZMB (low confidence) and GHA (capitation grant only).
- The primary specification in `identification_spec.json` is unchanged.

## 8. Data
Tables (as in data_dictionary.json): `wb_primary_enrolment` (World Bank panel with `iso3`, `year`, `ger_primary`, covariates) and `fee_abolition_dates` (`iso3`, `first_year`, `announce_year`, `source`). If documented dates cannot be sourced for a country, it is excluded and listed under `unavailable`.
