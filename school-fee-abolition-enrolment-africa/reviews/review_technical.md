# Technical Review

Paper: "Did Abolishing Primary-School Fees Raise Enrolment? Evidence from Staggered Reforms in Sub-Saharan Africa" (staggered DiD, WDI country-year panel, 8 treated and 39 comparison countries with GER).

Scope and limits of this review. I had the draft, the identification strategy (incl. revisions §9 and §10), the econometric specification with its Results section, the data summary and the data dictionary. I did not have `run_estimation.py`, `estimation_results.json`, `build_panel.py` or the `\input` tables (summary, main, robust_level, robust_log, mechanism). Number checks therefore compare the draft against the Results section of the specification, which quotes the JSON. The code-to-paper alignment is judged from the written specification only.

## Summary Assessment

**Concerns (borderline Major).** The reported numbers in the text agree closely with the pipeline output. Derived quantities also reproduce: t = 22.04/5.54 = 3.98, the 95% CI, exp(0.192)−1 = 21%, the HonestDiD bounds (linear in Mbar, breakdown 0.98), and the leave-one-out values (implied by the country ATTs). The weaknesses are in design and inference, and in how the text describes them.

1. The comparison group is described as "undated", but the project's own plan lists several likely abolishers inside the window. Examples are Ethiopia, Cameroon, Mozambique, Burundi, Madagascar and Benin. These are in the control group of 39, together with always-free-primary countries that the data dictionary says to exclude.
2. Inference rests on a country bootstrap with t(46). This is questionable with 8 treated clusters, four of them single-country cohorts. The one small-cluster check that was run (wild bootstrap on TWFE) already shows a three-fold gap in p-values (0.020 vs 0.062).
3. The abstract says the event study is "flat before the reform". The leads at −4 to −6 are −3.6 to −5.3, and the placebo estimate of 3.9 has the same magnitude.
4. Several treatment-timing and treatment-definition choices contradict the pre-registered rules. The data summary shows a Malawi jump in 1995 for a treatment year of 1994.
5. A sizeable set of pre-registered checks is silently absent from the paper.

The headline sign and rough size are plausibly robust to the checks that were run. The claims of a "stable", "flat-before" and "p < 0.001" result are stronger than the evidence supports.

## Data Pipeline

**D1. Comparison-group contamination is not addressed by the panel end rule (major).**
- §Data says the panel ends in 2010 "so that later abolitions do not enter the comparison group". That protects only against abolitions after 2010. Any undated country that abolished in 1995–2010 stays in the control group for exactly the years that matter.
- The paper plan names Ethiopia, Cameroon, Mozambique, Burundi, Madagascar, Benin and Rwanda as having 2000–2008 dates. Rwanda is now treated; the others are controls.
- The treated set is whichever countries had an abstract the researcher could find. The set is skewed towards anglophone East and Southern Africa (7 of 8), which is selection in the coding of treatment. The "bias towards zero" argument is one-directional and untested.
- The not-yet-treated check does not help: undated abolishers never switch on. A leave-out of plausible abolishers, or a dated-uncertain robustness set (promised in the data dictionary), is needed.

**D2. Always-free and non-comparable controls (major).**
- The data dictionary says countries with free primary education before the window are excluded. The control set still includes MUS, SYC, ZAF, BWA, NAM, CPV and others. The dictionary also says small islands are dropped in a robustness check; I see no such check.
- With GER near or above 100 in these countries, year-on-year changes are mechanically different from low-GER treated countries.

**D3. Sample window deviates from the registered sample (major, documentation).**
- Estimation uses 1980–2010: 1,211 rows, from 1,519 raw rows. The registered analysis window is 1985–2015.
- The Results section says "No exclusions relative to the registered sample", which is not true for the start year. 1,211 − 1,006 = 205 observations come from 1980–84.
- The descriptive mean (85.6) and SD (28.6) come from a different sample (1985–2010, N = 1,006) than the one the effect is scaled against. The text puts the 22 pp effect against the 85.6 mean, so the denominator is not the estimation-sample mean.
- Report the estimation-sample mean, and state which window the NER sample (684) uses. 684 exceeds 46.8% of the 1,274 country-years in 1985–2010, so it must also include 1980–84.

**D4. Count inconsistencies across sections (minor).**
- The intro says 39 comparison countries; the data section says "the other 41 economies". The 2 without GER are never named.
- 49 economies appear in the panel, but the dictionary labels the list "48".
- The draft says 9 outliers flagged (GER > 150 or < 10). The data summary lists 5 in 1985–2010 (MWI 1995, RWA 2007–10). The extra 4 must lie in 1980–84 and are not identified.

**D5. Timing convention and Malawi (major, verify).**
- The plan codes treatment to the calendar year in which the school year begins and asserts that this is the UIS convention. I believe UIS usually dates a school year by the year in which it ends. Please verify.
- If so, Malawi (school year 1994/95) and Ghana (2005/06) have their first treated observation at g+1. The data summary shows the Malawi jump in 1995 (GER 152.6, flagged as an outlier), which supports this.
- The draft says the MWI and UGA jumps "coincide with abolition". For Malawi, 1995 ≠ 1994.
- The event-study shape (e=0: 11.9; e=1: 23.2; e≥1 plateau) is consistent with partial or mistimed exposure at e=0. The draft interprets it as an "immediate jump".
- No ±1 recoding of Malawi or Ghana is reported, and the TZA 2001 alt-year check promised in the data summary is not in the paper.

**D6. Treatment dating evidence (major).**
- The identification strategy required at least two published sources per country. Each date rests on one abstract fragment; the researcher confirmed them against abstracts only.
- The sources for MWI (Chimombo), LSO, RWA and ZMB are not cited in the paper. The draft says the dates are "recorded in the data dictionary", but the dictionary lists the table as "NOT YET BUILT".
- Zambia's source is a 2020 concept paper. Malawi's quote is "1994/95".

**D7. Treatment definition contradicts pre-specified rules (major).**
- The identification strategy says partial or regional abolitions and capitation-grant-only reforms are not treated.
- Ghana (capitation grant only), Lesotho (phased from grade 1) and Uganda (initially capped at four children per family) are all in the main treated set. Three of the eight breach the stated rule.
- Only the Zambia/Ghana drop is a robustness check (24.35). A drop of Ghana, Lesotho and Uganda together, and a separate drop of Lesotho, are missing.
- The headline "abolition" effect is a package-of-reforms effect. The draft states this in §Background, but the abstract and conclusion do not.

**D8. Outcome measurement (minor-to-major).**
- GER is subject to UN population revisions; the RWA outliers of 154–157 appear after 2007. Outlier-dropping removes only post-treatment observations in treated countries, so it is not a neutral robustness check.
- Pre-registered count outcomes (SE.PRM.ENRL) and winsorizing at 1/99% are not reported. Log GER is the only transformation.

## Estimation Implementation

**E1. Bootstrap and degrees of freedom (major).**
- The draft says "multiplier bootstrap, clustered by country". The specification says a country-level bootstrap with SE equal to the SD of the draws, which reads as a pairs bootstrap. These are different procedures; the draft should name the one used.
- If it is a pairs bootstrap over 47 countries, a given single-country cohort is absent from about 36% of draws, since (46/47)^47 ≈ 0.36. Four cohorts (1994, 1997, 2000, 2005) are single-country. Most draws therefore change the estimand or drop cells. The SE then reflects cohort-composition variability, which is not the sampling variance of the ATT. Explain how missing cohorts are handled.
- "t with 46 df since only 8 of the 47 clusters are treated" is not a coherent justification: df = G−1 ignores that only 8 clusters carry treatment variation. With few treated clusters, size distortion is typically severe. The TWFE cluster p of 0.020 against the wild p of 0.062 illustrates the problem.
- The headline "p < 0.001" and "1% level" are therefore not credible. The pre-registered randomization-inference p-values, or Conley–Taber-style inference, were not run and should be.
- Sun-Abraham (5.7) and BJS (10.3) use a 499-draw pairs bootstrap, and the wild bootstrap is run for TWFE only. The strategy document required it for Sun-Abraham too.
- The BJS SE is almost twice the CS SE. BJS is meant to be the efficient estimator under homogeneity, so a wider SE points to an implementation or bootstrap problem (country FE not estimable in resampled draws, very few pre-periods). It needs investigation, not a passing mention.
- SA ≈ CS to two decimals (22.03 vs 22.04) despite different weighting and FE structure. This may be coincidence; please confirm the two are not the same computation.

**E2. Base period description conflicts (minor-to-major, documentation).**
- The specification says the main spec uses a varying base for pre-periods. The draft and Results say the universal base period g−1.
- The listed pre-coefficients (0.08 at −2, −0.34 at −3, −3.6 at −4) and M = 3.27 = |−0.34 − (−3.6)| are consistent with a universal base. Fix the specification text, and state which base the Wald test and the HonestDiD bound use.

**E3. HonestDiD implementation (major for interpretation).**
- It is a closed-form conservative bound, not the Rambachan–Roth procedure, as the draft admits. M = 3.27 is the largest consecutive change among point estimates whose SEs are 5–8. M is therefore mostly noise, so the breakdown value of 0.98 has little meaning. A different draw of the same data could give an M several times larger or smaller.
- The bound ignores the covariance of the estimates, and the CI endpoints are shifted rather than re-derived. Use the actual HonestDiD routine, with Mbar and smoothness-restriction variants (SD), plus the pre-registered Mbar = 2. The draft cites no Mbar = 2 result, although the Results report [−11.7, 55.8].
- Numbers reproduce. The half-width grows linearly (16.5, 22.3, 33.7 at Mbar 0.5, 1, 2; slope about 11.6, intercept about 10.7), and breakdown = (22.04 − 10.7)/11.6 ≈ 0.98.

**E4. Pre-trend and placebo evidence is read too favourably (major).**
- Wald W = 0.76 on 5 df gives p = 0.98, which is arithmetically right. The test has almost no power with SEs of 5–8 and a bootstrap covariance from 8 treated clusters.
- The placebo estimate is 3.9 (SE 4.7). It is the same size as the maximum pre-period change M and is about the drift between e=−4 and e=−1. The draft calls it "small relative to the main effect". That is the rising-pre-trend signature, not reassurance. Also, a placebo that moves the date 3 years earlier is weak when the real e=0 effect is only 12 pp.
- Pre-trends at e=−6…−4 use a changing set of cohorts. Report the number of treated countries observed at each event time.

**E5. Estimand mismatch between estimators (minor).**
- CS ATT averages e = 0…5. Static TWFE (23.4) uses all post years through 2010, so the two numbers are not comparable. The Goodman-Bacon decomposition uses a 13-country subsample (3 treated: LSO, TZA, UGA) whose TWFE coefficient is 17.07, versus 23.37 on the full sample.
- The statement that "the static estimator is not distorted much by forbidden comparisons" cannot be extended to the full sample; the draft says "in this subsample" but then draws the conclusion without that caveat. The 6-point gap between 17.07 and 23.37 deserves a sentence.

**E6. Window robustness is tautological (minor).** The [−5,5] window gives an identical ATT because the overall ATT uses e ≥ 0 only (the draft lists it as a robustness result without saying so). Remove it from the list of checks or replace it with a check that changes the estimand window (e.g. e = 0…3, 0…8).

**E7. Covariate and mechanism specifications (minor).**
- The covariate-adjusted ATT (19.1) is outcome-regression CS, not doubly robust, with covariates fixed at g−1. N is not reported. GDP per capita is missing for 4.4% of rows, so the sample may differ. A drop of 3 pp is described only as "remains significant".
- Aid per capita was dropped from the data (the API metadata failed). The draft's identification section lists aid as a control but says nothing about its absence.

**E8. Correlation in the regional structure (major, design).** 7 of 8 treated countries are in East or Southern Africa; controls are mostly West and Central Africa. Region-specific shocks (post-conflict recovery in UGA and RWA, HIV, common EAC policies, cross-border spillovers between KEN, UGA and TZA) are not removed by year FE. The pre-registered regional comparison restriction was not run.

## Results Reporting

Consistency check summary (approximate, based on the Results section of the specification; the tables were not available):
- Total claims checked: about 85.
- Consistent: about 76 (89%).
- Inconsistent or ambiguous: 5 (6%): outlier count 9 vs 5; comparison group 39 vs 41; base period (universal vs varying); "no exclusions" vs 1980 start; "pre-period flat" (abstract) vs leads −3.6 to −5.3.
- Unverifiable: about 4 (5%), plus every table cell (tables not provided).
- Verdict: PASS on arithmetic, no critical discrepancy. The inconsistencies above are major or minor in wording rather than numeric transcription errors.

Specific checks that pass: t-statistics and p-values for CS level and log (3.98, 3.49), TWFE level (2.41, p = 0.020) and log (1.39, p = 0.17), BJS (2.22, p = 0.032), NER (3.42, p = 0.001), completion (1.52, p = 0.136), gender difference (0.074, p = 0.94), H3 slope (1.48, p ≈ 0.18, df 6) and the GER − NER difference (14.78 − 13.45 = 1.33). The event-time average (11.9, 23.2, 23.8, 22.0, 24.7, 27.5 → 22.2) is consistent with the 22.0 overall ATT. Leave-one-out values are consistent with the country ATTs under near-equal weights ((22.04×8 − 51.8)/7 ≈ 17.8 vs 17.46 reported; (176.3 − 8.9)/7 ≈ 23.9 vs 24.06).

Interpretation issues:
- **Abstract, "flat before the reform" and "stable" (major).** Leads at −4 to −6 are −3.6 to −5.3, not flat. The intro restricts "no divergence" to the two years before, which is a convenient window. "Stable" refers to point estimates only. Precision varies from SE 5.5 to 10.3 (BJS p = 0.032), the TWFE log estimate is insignificant (p = 0.17, wild p = 0.21), and TWFE in levels has wild p = 0.062.
- **Abstract, "pre-reform data are sparse" (minor).** The data summary shows 9–19 observed pre-years for each treated country. The real limitation is imprecise leads at −4…−6, not sparse data.
- **NER inference (major).** The claim that the gain "is a genuine increase in participation among children of primary-school age" rests on a 684-observation selected sample. The GER effect on that sample is 14.8, against 22.0 on the full sample, so composition drives about 7 points. The gross-minus-net CI is roughly [−3.6, 6.2], so up to about 40% of the GER gain could be over-age. The discussion should use the "cannot rule out" wording of the results section, not "a large part reflects additional children".
- **Completion (minor).** A completion rate for a 6–7 year cycle cannot move within a 5-year window for the first cohorts. The null is uninformative about quality dilution. The conclusion should not use it as a policy argument.
- **Gender (minor).** Equal absolute gains (21.6 vs 21.4) from a lower base imply a larger relative gain for girls. Say so, or report the log specification.
- **Supply constraints (minor).** The discussion says fee removal "can move enrolment substantially even where governments cannot immediately expand supply". No supply data (pupil–teacher ratios, classrooms) were analysed, so this is not tested. Persistence is only shown through year 5.
- **H3 (minor).** The H3 country ATTs regressed on pre-reform GER share noise in the base level (mechanical regression to the mean). The draft hedges correctly.
- **Literature claims (minor).** The novelty claim ("whereas most existing evidence consists of single-country case studies") was not searched exhaustively according to the literature review. Several sources the review names (Lucas and Mbiti 2012, Al-Samarrai and Zaman 2007, Deininger 2003) are not in the bib.

Robustness assessment: the checks that were run (not-yet-treated, anticipation, drop outliers, drop ZMB and GHA, leave-one-out) vary the sample, not the identifying assumption. They do not address contamination of the comparison group (D1), region-specific trends (E8) or timing (D5). The covariate check is the only one that targets confounding, and it moves the estimate by 3 pp.

## Red Flags

- **Selective reporting by omission.** The strategy document pre-registers many checks that have no result in the paper or the Results section, and the paper does not say so. They are: announcement-year dating and TZA 2001; leave-one-cohort-out; drop conflict years; enrolment counts and winsorizing; balanced-panel re-run; Gardner estimator; wild bootstrap for Sun-Abraham; never-treated fake-date placebos; randomization inference; aid covariate; window 1990–2012; regional restriction; the drop of small islands; and the drop of countries with fewer than 15 observations. The specification admits only two not-run items (randomization-inference p-values, never-treated fake dates). Please list all omissions.
- **Post-hoc design changes.** The sample window, comparison-group rule (undated vs never-treated) and event window changed after earlier did_design failures. This is documented and acceptable, but the estimation phase should say that the sample was set after the dates were found.
- **P-value pattern.** No unusual clustering below thresholds. Reported p-values range widely (0.0002, 0.001, 0.032, 0.062, 0.136, 0.17, 0.18, 0.42, 0.59, 0.94).
- **Magic numbers.** GER thresholds of 150 and 10, a 20-point jump rule, a 5-year pre-GER mean for H3, and M computed from point estimates. They are mostly documented; the M choice is not justified.
- **Suspiciously clean items.** Sun-Abraham equals CS to two decimals; BJS SE is almost double; Wald p = 0.98. None is conclusive, each deserves a check.

## Strengths

- Modern estimator set (CS, SA, BJS, TWFE benchmark with Goodman-Bacon), reported with TWFE explicitly demoted to a benchmark.
- Fixed seed, 999 draws, registered specification written before estimation, with traceable `% src:` comments for almost every number in the text.
- Honest handling of low-confidence cases (Zambia), of the "undated, not never-treated" label, and of the partial HonestDiD implementation.
- Reports the unflattering evidence: the negative imprecise leads, the 0.98 breakdown value, the wild-bootstrap p for TWFE, the insignificant TWFE log result, and the insignificant completion and gender results.
- No imputation of missing outcomes, and a sample-flow description (1,519 → 1,211; 47 countries; 8 treated and 39 comparison).
- Gross versus net enrolment on a common sample is a good idea.

## Recommendations

**Data stage**
1. Build a dated-uncertain set and re-estimate after dropping likely abolishers (ETH, CMR, MOZ, BDI, MDG, BEN, SLE and others from the plan) from the comparison group. Drop or flag always-free and small-island countries as the dictionary says.
2. Document the UIS year convention. Recode MWI and GHA (and check the others) at g+1 as an alternative. Run TZA 2001 and announcement-year dating.
3. Reconcile 39 vs 41, 49 vs 48, and 9 vs 5 outliers. List the four 1980–84 outliers. Report estimation-sample summary statistics.
4. Cite the sources for MWI, LSO, RWA and ZMB in the paper, add a second source per country if possible, and fix the dictionary entry.

**Estimation stage**
5. Name the bootstrap, report how absent cohorts are handled in draws, and run wild cluster bootstrap-t and randomization inference for the CS, SA and BJS estimates. Replace t(46) in the headline by these p-values or by Conley–Taber inference.
6. Investigate the BJS SE and the SA equals CS coincidence.
7. Use the exact HonestDiD procedure with the full covariance, and report Mbar = 2 and smoothness-restriction results.
8. Run the omitted pre-registered checks (see Red Flags), at least leave-one-cohort-out, balanced panel, conflict years, regional restriction, drop UGA, GHA and LSO together, and region-by-year trends or a West-Africa-only control.
9. Replace the [−5,5] "robustness" with a real window check. State the number of treated countries per event time.
10. Fix the base-period description (universal) in the specification.

**Draft stage**
11. Change the abstract: leads are not flat; "stable" applies to point estimates; drop "pre-reform data are sparse" or restate it as imprecise leads.
12. Drop "p < 0.001" as the headline; report CIs from the small-cluster procedure.
13. Qualify the NER interpretation, the completion argument and the supply-constraint claim.
14. Add a paragraph listing which pre-registered checks were not run.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
