# Identification Review

Paper: "Did Abolishing Primary-School Fees Raise Enrolment? Evidence from Staggered Reforms in Sub-Saharan Africa"
Design: staggered DiD (Callaway–Sant'Anna), 8 treated countries, 39 undated comparison countries, WDI GER, 1980–2010.

## 1. Summary assessment

The paper is candid about several weaknesses: few treated units, sparse pre-reform data, an undated rather than never-treated comparison group, and a conservative sensitivity bound. The estimator choice is appropriate for staggered timing. The headline claim, a roughly 22 pp effect "significant at the 1 percent level", is nonetheless not yet credibly identified or credibly inferred. The main reasons:

1. The comparison group is probably contaminated, and the panel-end rule does not fix this.
2. Treatment is heterogeneous, and the draft deviates from the pre-specified coding.
3. Parallel trends in GER levels is doubtful in this setting, given ceilings, convergence, post-conflict rebounds and election-driven timing. The pre-trend evidence is weak and mixed.
4. Inference with 8 treated clusters is probably too optimistic. The CS standard error is about half the BJS and TWFE standard errors, and the log-TWFE estimate is insignificant.
5. Several pre-registered robustness checks that address these threats were not run, and some reported checks are cosmetic.

The abstract and introduction overstate the evidence (see 2.5 and 4). Taken together, the paper supports "GER rose substantially in reforming countries after abolition, with suggestive but fragile causal content". It does not support "abolition raised GER by 22 pp".

## 2. Threats to identification

### 2.1 Comparison group: undated is not untreated (severe)
- The 39 comparison countries are "countries without a known date". They were not checked. Many SSA countries abolished or cut fees within 1994–2010, often with the same donor push. From memory (to be verified, and exactly what the missing chronology would settle), candidates include Ethiopia, Mozambique, Burundi, Cameroon, Madagascar, Sierra Leone, Benin, Senegal, Niger, Burkina Faso and Mali. I do not rely on these specific cases. The point is that the base rate of undetected abolition among 39 countries in this era is high, not low.
- The draft says contamination biases the estimate toward zero. That holds only if contaminated controls rise after their own reform and the effect is positive. Contaminated controls also add post-period noise and trend variation, and they distort the pre-trends (leads) because the "control" path contains its own treatment dynamics. The sign argument is not a safe bound.
- The "panel end rule" (end 2010 so "later abolitions do not enter the comparison group") addresses only post-2010 reforms. Undated abolitions between 1994 and 2010 lie inside the estimation window. The rule gives a false sense of protection.
- The not-yet-treated check (22.12 vs 22.04) is not independent evidence. With undated controls the not-yet-treated group is the same 39 countries plus later cohorts, so near-equality is mechanical. It does not address contamination at all.
- Recommendation: build the chronology for all 47 countries (the draft itself lists this as future work). Do it now, because it is the central identification input. At minimum, run (i) an exclusion of countries with plausible 1994–2010 abolition, and (ii) a bounding exercise that assigns random or plausible fake dates to a share of the comparison units.

### 2.2 Treatment definition and timing (severe/major)
- **Deviation from the pre-registered rule.** The identification strategy states that "capitation-grant-only reforms are not treated" and that phased/partial reforms are not treated. The main spec treats Ghana (capitation grant 2005; the paper itself says "not strictly an abolition") and Lesotho (phased from grade 1) as treated. Ghana is also the only 2005 cohort and uses the 5-year tail e=5. Only drop-ZMB-GHA is a robustness check, and it moves the estimate up (24.4). It should instead be the main specification or a prominently reported alternative. As coded, "abolition" is not a single treatment, and the estimand is a mixture.
- **Dates come from abstracts.** The researcher checked dates against published abstracts via OpenAlex, not against legal or ministerial documents. Zambia rests on a single 2020 concept paper. Announcement vs. implementation year is not systematically separated (the pre-registered `announce_year` is only used for Tanzania as an alternative).
- **Calendar vs. school-year mapping.** WDI year vs. start of the school year is ambiguous (Malawi 1994/95, Uganda announced for 1997, Tanzania 2001 declared / Jan 2002 implemented). The event-study profile (11.9 pp at e=0, 23.2 pp at e=1) looks like a half-year-exposure pattern in several cohorts, which is what a one-year dating mismatch would produce. The ±1 year coding is called an "explicit robustness check" in the plan, but the only alternative reported is anticipation=1. The Tanzania 2001 alt_year run, the announcement-year re-dating and ±1 coding are not reported. Report all of them.
- **Adoption is not random.** Reforms were election-driven or tied to political transitions: Malawi 1994 (first multiparty election), Uganda 1996–97, Kenya 2003 (Kibaki campaign), Tanzania 2001, Ghana 2004–05. Rwanda (treated 2003) and Uganda are post-conflict, with rebound enrolment in the pre-period. Democratisation, post-conflict recovery, HIPC relief, FTI funding and the EFA/Dakar push are all correlated with timing. Year effects remove common shocks only. The "controls" are limited to log GDP per capita and urban share. Aid per capita was dropped because of a data-loading failure, even though donor funding is the main confounder named in the identification strategy.

### 2.3 Parallel trends in GER levels (major)
- Treated and comparison countries differ in baseline GER and ceiling. The comparison group includes high-GER countries (e.g. Mauritius, Seychelles, South Africa, Botswana) that cannot rise much. Kenya, Lesotho and Zambia were near 100 before the reform. SSA GER exhibits convergence: low-GER countries grew faster in the 1990s–2000s regardless of fee policy. Reforming countries had GER mostly below the comparison mean (e.g. MWI 72, UGA 71, TZA 69, GHA 72 vs. sample mean 85.6). A differential convergence path is therefore exactly the violation to worry about, and the estimand in levels is not invariant to this. Country-level ATT correlates negatively with baseline GER (slope −0.71).
- Adoption timing could reflect stagnation (mean reversion upward) or a boom. The draft notes that the leads at −4 to −6 are negative (−3.6 to −5.3 pp), which is consistent with a rising pre-reform path. That is the direction that biases the ATT upward.
- Recommendation: restrict the comparison group to countries with similar baseline GER and GER growth; include baseline-GER × year (or pre-trend) interactions; use log GER or a ratio-based outcome as the main specification; and use the shape of the pre-period (not only a Wald test) as a diagnostic.

### 2.4 Pre-trend evidence and sensitivity (major)
- **Pre-trend Wald test (p = 0.98) is uninformative.** The covariance matrix comes from a bootstrap with 8 treated units and composition that changes across event times (only some cohorts are observed at e=−4..−6). W = 0.76 on 5 df is below its expectation under the null, which is consistent with a poorly estimated, near-degenerate covariance. The draft correctly does not rely on it, but then uses the "flat before the reform" wording in the abstract (see 4).
- **Base period inconsistency.** The econometric specification says varying base for pre-periods; the paper describes a universal base g−1. These give different lead coefficients and different values of M. Specify and report one, and report both.
- **The relative-magnitude bound is driven by noise.** M = 3.27 is the largest absolute change between consecutive pre-period estimates, which have SEs of 5–8 pp. M is therefore mostly sampling noise and is itself uncertain; the bound is both ad hoc and non-monotone in the information in the data. The result (breakdown Mbar = 0.98) should be read as indicative only. Run the actual Rambachan–Roth procedure (including the smoothness restriction, which suits a visible drift in leads). Also report the bound by cohort, since composition varies across e.
- **Placebo** (fake date −3): 3.9 pp, SE 4.7. Calling this "small relative to the main effect" overlooks that it has no power to exclude drift of the size needed (a placebo of 4–8 pp is within its CI). The pre-registered never-treated fake-date placebo and randomisation inference were not run. They are the natural tests for few treated clusters.
- **The only available pre-trend-robust statement** is the one the authors make: the effect is not robust beyond deviations about the size of the largest pre-period change. That statement should be in the abstract's first lines, not at the end.

### 2.5 Inference with 8 treated clusters (major)
- The CS standard error (5.5, "multiplier bootstrap" in the paper; unit resampling in the specification, an inconsistency) is about half that of BJS (10.3) and TWFE (9.7), and the TWFE wild-bootstrap p is 0.062. Differences of this size between estimators with nearly the same point estimate indicate that the bootstrap SE for CS is underestimated or that the other two are overestimated. In either case the reader cannot take "p < 0.001" at face value. With 8 treated clusters, pairs bootstrap draws often include few treated units and the bootstrap distribution is unreliable.
- The t reference distribution uses 46 df "since only 8 of the 47 clusters are treated". The effective degrees of freedom in this design are governed by the number of treated clusters (about 7), not by the total. Sun–Abraham and BJS also rely on the pairs bootstrap, with no wild-bootstrap version (the plan promised it for SA).
- The log TWFE estimate is 0.150 with wild-bootstrap p = 0.21, while CS log is 0.192 (SE 0.055, significant). The gap between a 5.5-SE CS and an insignificant TWFE cannot be explained by Goodman-Bacon weights (the decomposition covers only 13 countries / 3 treated cohorts, which cannot characterise the full unbalanced sample).
- Sun–Abraham equals the CS estimate to the second decimal (22.03 vs 22.04) despite differing in control-group handling and FE structure on an unbalanced panel. This coincidence deserves checking before it is presented as independent confirmation.
- Recommendation: report randomisation-inference or permutation p-values over adoption years (pre-registered, not run), wild bootstrap-t for CS (or cohort-level aggregation), and a conservative CI. Present results as conditional on few treated units.

### 2.6 Outcome measurement and sample selection (major)
- GER depends on UN population denominators, revised by UIS, with documented breaks. Nine year-on-year jumps over 20 pp exist, two of them (Malawi 1995, Uganda 1997) coincide with treatment, and Rwanda's GER exceeds 150 in 2007–10. Treated countries with the largest effects (Uganda 51.8, Malawi 41.5, Rwanda) are the ones with breaks and outliers. Leaving out Uganda reduces the ATT to 17.5. A study of WDI GER cannot separate real enrolment from administrative reclassification. Per-pupil capitation grants create reporting incentives (plan §8), which would mechanically raise post-policy GER in treated countries only.
- The pre-registered checks using enrolment counts (SE.PRM.ENRL), winsorising at 1/99%, dropping flagged breaks and countries with fewer than 15 observations, and a balanced-panel rerun were not run. Run them.
- **Base-period problem.** CS with base g−1 needs a GER observation in g−1 for each treated unit (balanced pairs). The paper says four countries have no GER before 1995 and 61 gaps exist. It does not state whether any treated cohort lost observations at g−1, or how it was handled (e.g. fallback to the nearest earlier year). This matters most for Malawi (1994) and Uganda (1997), which drive the result. Report pre-period GER counts by treated country and the effective base year used.
- **Sample inconsistencies.** The estimation panel starts in 1980 (so 1980–84 pre-years enter), whereas the pre-registered window is 1985–2015 and descriptives use 1985–2010. The paper reports "39" comparison countries in the introduction but "41" undated economies in the data section. Align them.

### 2.7 Spillovers and SUTVA (minor/moderate)
Cross-border spillovers (e.g. Ugandan and Kenyan fee abolition affecting Tanzania and Rwanda flows, refugee schooling) and common donor programmes make the control group partially treated. This is acknowledged but not examined. A regional-restriction check (planned) was not run.

## 3. Mechanism: gross vs. net enrolment
- NER is observed in 684 country-years, mostly after 2000, with few pre-period observations for early cohorts. The NER sample is therefore dominated by later cohorts. The like-for-like GER on the same sample is 14.8 vs. 22.0 on the full sample, which shows the composition difference. The NER result is not evidence about Malawi and Uganda, the largest-effect countries.
- The gross-minus-net difference is 1.3 pp (SE 2.5); the 95% CI is roughly [−3.6, 6.2]. The paper interprets it as "the gain is not driven mainly by over-age enrolment". The estimate is compatible with a moderate over-age component, as the paper acknowledges in one sentence. The abstract and introduction state the stronger claim. Pre-registered H2 (GER effect > NER effect) is neither confirmed nor rejected.
- Also, NER is measured with the same population denominators. It does not escape the denominator/reporting concern in 2.6.
- The "no differential gain for girls" result is a gross-ratio result subject to the same issues; the plan expected a gender-gap closure (H4) which is not found. Fine to report. The gender-gap statement ("did not close the gender gap in gross enrolment") is not shown, since the paper reports no gap measure or GPI.

## 4. Claims versus evidence
- The abstract says the event study is "flat before the reform", but the text reports leads of −3.6 to −5.3 at e=−4..−6 and says treated countries "may have been on a rising path". Revise the abstract.
- "Stable across heterogeneity-robust estimators, comparison groups, and leave-one-country-out samples": the estimators share the same comparison logic, the comparison groups are essentially identical (see 2.1), and the leave-one-out range is 17.5–24.1. The claim should be narrowed.
- The [−5,5] window check returns the identical ATT by construction (the overall ATT uses e≥0 only). It is not a robustness check and should be removed or replaced by a check that varies the post window (e.g. 0–3, 0–8).
- "Significant at the 1 percent level" (introduction and abstract) should be tempered given 2.5.
- The discussion says the results "imply that fee removal can move enrolment substantially even where governments cannot immediately expand supply". This interprets a package effect (abolition plus donor funding, grants, new classrooms) as a price effect. The paper acknowledges the package interpretation in the background section; the conclusion should be consistent with it.
- Heterogeneity (H3) with 8 countries and p = 0.185 is rightly labelled as imprecise. The text "consistent with larger gains where initial enrolment was lower" is acceptable if flagged as descriptive; note also the regression-to-the-mean concern from the plan.

## 5. Pre-registered checks not run or not reported
Announcement-year dating; ±1 year coding (including Tanzania 2001); conflict-year exclusion; never-treated fake-date placebos; randomisation-inference p-values; Gardner two-stage; wild bootstrap for Sun–Abraham; leave-one-cohort-out (only leave-one-country-out reported; cohorts 2002 and 2003 have two countries each); enrolment counts; winsorised GER; dropping countries with fewer than 15 observations; balanced-panel rerun; regional comparison restriction; aid per capita as covariate; the covariate-adjusted specification with pre-abolition GER level and trend (only log GDP and urban share used, outcome-regression rather than doubly robust). The paper should state which pre-registered items are missing and why.

## 6. Strengths
- Uses a heterogeneity-robust estimator and treats TWFE as a benchmark only, with Bacon decomposition (though on a small subsample).
- Sources every treatment date, flags Zambia as low-confidence, and names the undated group as such.
- Reports a placebo, leave-one-out, and a (conservative, self-labelled) Rambachan–Roth-type bound and its breakdown value instead of relying on a non-rejected pre-test.
- Candid about few treated clusters, sparse pre-data, GER breaks and the gross/net issue; limitations are sensible.
- Reports unfavourable estimates (TWFE wild p, BJS SE, log TWFE) rather than hiding them.

## 7. Recommendations (priority order)
1. Build and verify the fee-policy chronology for all comparison countries. Re-estimate with a cleaned comparison group, and bound the effect under assumed contamination.
2. Make the treatment definition match the registered rule: main spec excluding capitation-only (Ghana) and phased (Lesotho) cases, with Ghana/Lesotho/Zambia as alternatives. Report ±1 year, announcement-year and Tanzania 2001 re-datings.
3. Address level-based parallel trends: comparison group matched on baseline GER/growth, baseline-GER × time interactions, log GER as the primary outcome.
4. Replace the closed-form relative-magnitude bound with the actual Rambachan–Roth (RM and smoothness) procedure; state the base period convention; report cohort-specific event studies.
5. Fix inference: randomisation inference over adoption years, wild bootstrap-t for CS/SA, effective df tied to treated clusters; reconcile the CS vs BJS/TWFE SE gap and verify the SA = CS coincidence.
6. Report pre-period GER availability and base-year handling by treated country; rerun on balanced, winsorised, breaks-dropped and enrolment-count versions; check that Malawi/Uganda results do not depend on break years.
7. Rewrite the abstract and introduction so claims match the evidence (pre-trend wording, "significant at 1%", "not driven by over-age", "stable across comparison groups"). Report the sensitivity result in the opening abstract sentences.
8. Add aid per capita (or an alternative donor-funding measure), election/transition indicators and conflict flags as pre-treatment covariates or heterogeneity splits.

## 8. Verdict
The design is sensible in outline, but identification is currently fragile on five fronts that the authors only partly acknowledge: contaminated controls, a heterogeneous treatment definition at odds with the registered plan, level-based parallel trends in a convergence setting, 8-cluster inference, and GER measurement breaks coinciding with treatment. The estimates are best read as an upper-bound-flavoured descriptive association, with a credible range that includes values close to zero under moderate trend violations.

OVERALL SCORE: 4/10
RECOMMENDATION: Major Revision
