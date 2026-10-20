# Data Review: Did Abolishing Primary-School Fees Raise Enrolment? (Staggered DiD, WDI GER, SSA)

Reviewer role: data_reviewer. Scope: source documentation, sample construction, missingness, variable definitions, outliers, measurement, timing, panel structure, and consistency between the draft, the data summary and the estimation results. Identification and econometric choices are covered only where they depend on the data.

## 0. Summary verdict

The data work is more transparent than is typical for this kind of paper. Each number carries a source comment, the sample flow is traceable, no values are imputed, and the paper is honest about the undated comparison group. The paper has four serious data problems:

1. The treatment table rests on one abstract per country, and three treated cohorts depart from the registered coding rules.
2. The comparison group is probably contaminated by abolishers inside the window. The remedy the paper offers (the not-yet-treated group) does not address this.
3. The outcome is a ratio with a modelled, revised denominator. The registered checks that would address this (enrolment counts, winsorizing, announcement-year dating) were not run.
4. Several numbers do not reconcile across the draft, data summary and estimation results. The NER sample size, the outlier count, the number of countries and the "sparse pre-period" claim are the main cases.

The headline of about 22 pp is plausible, since the raw cohort means move in the same direction. Its inference, timing and interpretation are weaker than the abstract implies.

---

## 1. Source documentation

**Strengths.** WDI series codes are given in the dictionary (SE.PRM.ENRR, ENRR.MA, ENRR.FE, NENR, CMPT.ZS). The dictionary records a vintage (release 2026-10-08, UIS Feb 2026), SHA-256 checksums of the API pulls, and the licence. The unit of observation is a country-year.

**Problems.**

- **No vintage in the paper.** The paper cites only `WorldBank_OpenData`. It gives no release date, no series codes, and no mention that the underlying source is UNESCO UIS administrative data. UIS series are revised retroactively, and denominators come from UN population estimates. Add the vintage, the codes and the UIS provenance to Section 4.
- **The treatment table is only partly documented.**
  - The text says "the remaining dates are recorded in the data dictionary with their references". The dictionary states the table is "NOT YET BUILT" and has `rows: []`. The real table appears only in `data_summary.md`.
  - The sources named in the text cover four countries. Malawi (Chimombo 2009), Lesotho, Rwanda and Zambia are not cited in the paper. Lesotho and Rwanda are given only as DOIs, and Zambia as an uncited "2020 concept paper".
  - Put the full table (country, year, quote, source, scope, confidence) in an appendix and in the replication package.
- **One source per country.** The dictionary required `verified_two_sources` or `verified_one_source`, and the identification strategy required at least two sources per country (Kattan and Burnett 2004, Grogan 2009, Morgan et al. 2014 and others). The dates were taken from a single published abstract each, and the status was set to a generic "published source". An abstract phrase such as "in 1994/95" or "introduced in 2003" does not establish the school year in which fees were first abolished nationally. The paper should say this plainly instead of calling the dates "published".
- **Dictionary mismatches.** The dictionary says "48 economies" but lists 49 ISO3 codes. The identification document speaks of 48 countries and 43 comparison units. The data summary has 49 rows. The paper says 49. The data dictionary also lists tables (`wdi_primary_enrolment`, `wdi_controls`) that differ from the table names used in the estimation (`wb_primary_enrolment`, `fee_abolition_dates`). Harmonize them.
- **Dropped aid control.** `DT.ODA.ODAT.PC.CD` was dropped because the metadata endpoint failed. The identification strategy pre-registered aid per capita as a covariate and as a concurrent-shock control. The paper does not disclose this deviation. It uses log GDP per capita and urban share only.
- **Series not loaded.** Several series the plan or the pre-registration relied on were never loaded: enrolment counts (SE.PRM.ENRL), pupil-teacher ratios, school-age population share, the secondary GER placebo, and out-of-school children. See Section 6.

## 2. Treatment coding (data side)

- **Three treated cohorts depart from the registered rules.** The dictionary and the identification strategy say partial abolitions and capitation-grant-only reforms are "not coded as treated in the main specification" and are robustness only.
  - Ghana 2005 is a capitation grant, a weaker form of abolition. Ghana's FCUBE intent of 1996 is not discussed.
  - Lesotho 2000 is phased in from grade 1, and the data summary itself says the national GER effect is likely diluted early on.
  - Zambia 2002 is a low-confidence date.
  - All three are in the main treated set, and the exclusion check (24.35, SE 7.08) is the only treatment of this. That check raises the estimate by 2.3 pp. The paper should call this a deviation from the registered protocol and not describe it as a robustness choice.
- **Year convention for GER.** The plan assumes a WDI value for year t refers to the school year starting in t. UIS convention, as far as I know, assigns spanning school years to the calendar year in which they end. This needs checking against UIS metadata.
  - If I am right, Malawi (school year starts September, FPE 1994/95) and Ghana (2005/06) are coded one year too early. The Malawi GER jump to 152.6 sits in 1995, which is consistent with this.
  - Mis-dated cohorts would also shape the event study. A "jump of 11.9 at e=0 and 23.2 at e=1" is what partial-year or mis-dated treatment looks like.
  - Run ±1 coding for all cohorts (a registered check, §3.1 of the plan) and report it. At present only Tanzania 2001 is mentioned in the text, and no result for it appears in the estimation output.
- **Announcement dating.** The identification strategy registered `announce_year` and re-dating by announcement (check d). That check was not run. Uganda's UPE was an election promise in 1996, so anticipation matters there. Only the "anticipation = 1" run appears.
- **Reintroduction and earlier abolition.** Kenya abolished fees in 1974 and reintroduced cost-sharing in the 1980s. Kenya has the smallest effect (8.9 pp) and starts near the ceiling (GER about 100). Reintroductions are not coded, and the dictionary registered a robustness run dropping them.

## 3. Comparison group: the main data threat

- **The 41 "undated" countries are probably not clean.** The paper acknowledges this and says contamination biases towards zero. The size of the problem is under-stated for three reasons.
  - The paper's own plan lists further likely abolishers in the window: Ethiopia, Cameroon, Mozambique, Burundi, Madagascar, Benin and Senegal, with "many 2000–2008 dates". From my own knowledge (to be verified, not taken from memory into the study), Burundi (2005), Mozambique (2005), Cameroon (2000), Sierra Leone (2001) and Madagascar (2002) are strong candidates.
  - The data support this. `ger_jumps.csv` lists a Burundi 2006 GER jump of more than 20 points in a comparison country, and Burundi has a candidate date of 2005. Check each of the nine jump cases (BDI 2006, COG 1999/2000, ERI 1992, MWI 1995, RWA 2000, STP 1999, UGA 1997, ZAF 1989) against policy chronologies.
  - The end-of-panel rule (2010 = last cohort + 5) is presented as protecting the comparison group. It protects only against post-2010 abolitions. It does nothing about abolitions before 2010, and those are the ones that matter.
- **The not-yet-treated group does not fix contamination.** Section 4 says the contamination concern is addressed "with a not-yet-treated comparison group". In this design that group consists of the undated countries plus later treated cohorts. An undated abolisher stays in it forever, so the check cannot detect contamination. The result (22.12 against 22.04) is nearly identical, which is what you would expect, and it carries no information about the problem. The text should be corrected, and a verified chronology for at least the likely abolishers should be built. The comparison group could also be trimmed to countries with documented fees through 2010.
- **Ceiling and composition.** The comparison group includes high-GER or high-income states: South Africa, Mauritius, Seychelles, Botswana, Cabo Verde and Eswatini. The dictionary registered dropping small island states as a robustness check, and the paper does not report it. There is no baseline balance table (pre-reform GER, GDP per capita, conflict status) for treated against comparison. A level-DiD on a ratio that is above 100 for some units and near-ceiling for others needs that table. A restricted comparison (regional, low-GER) was pre-registered under "regional comparison restriction" and was not run.
- **Post-conflict recoveries.** Several comparison countries (Angola, Liberia, Sierra Leone, DRC, Burundi) and treated countries (Rwanda, Uganda, Malawi) saw large enrolment recoveries in the period. The Rwanda GER jump of more than 20 points in 2000, three years before the 2003 reform, is an example, and it falls inside Rwanda's pre-period. The registered "drop conflict country-years" check was not run.

## 4. Sample construction

- **The sample windows differ.**
  - The descriptive window is 1985–2010 (1,006 country-years), and the estimation panel is 1980–2010 (1,211). The identification strategy registered 1985–2015, and the dictionary says the analysis window is 1985–2015.
  - The mean (85.6) and SD (28.6) quoted in the paper are for 1985–2010 and are then used to judge the size of an effect estimated on a different sample. The 205 extra rows (1980–84) are not described anywhere.
  - Report the descriptives for the estimation sample, or restrict the estimation to 1985.
  - Record the truncation from 2018 to 2010 and from 2015 to 2010 as a deviation. The event window shrinks to [-6, 5] from the registered [-6, 8], so persistence beyond five years cannot be assessed.
- **Country counts.**
  - The paper says "49 economies", then 47 countries with GER, 8 treated and "39 comparison" (introduction). The data section says "the other 41 economies" are undated. The difference is the two countries with no GER at all, but the paper does not say so.
  - Name those two countries and say why they have no data. South Sudan before 2011 and Somalia are likely, but this is a guess.
  - Also say what happens to units that did not yet exist as countries in part of the window (Namibia, Eritrea, South Sudan).
- **No sample flow table.** The text gives the numbers (1,519 → 1,211) but there is no table. The template in the checklist (step, N observations, N countries) would take little space. Add the filtering steps and the N per outcome (GER, NER, gender, completion, controls).
- **The outlier count does not reconcile.** The data summary lists 5 flagged country-years (Malawi 1995 and Rwanda 2007–2010). The paper and the estimation results say "nine observations are flagged" and drop nine. Nine is the number of year-on-year jumps. Either the flag rule differs between the 1980–2010 and 1985–2010 windows, or the paper conflates the two counts. Reconcile, and list the dropped rows.
- **The NER sample size does not reconcile.**
  - 46.8% non-null NER in 1985–2010 implies about 596 observations (0.468 × 1,274). The estimation reports 684, which is 54% of that window.
  - NER before 1995 is only 36.5% non-null, and it is almost certainly sparser before 1985. The extra 88 rows cannot plausibly come from 1980–84.
  - Either the share is computed on a different base or the estimation sample differs. Resolve this before the mechanism result is relied on.
- **Pre-period sparsity is described inconsistently.**
  - The abstract and conclusion say "the pre-reform data are sparse". The cohort descriptives show 9 to 19 observed pre-years for every treated country, and the identification strategy requires three or more.
  - What is sparse is NER, plus the leads at e = −4 to −6 ("only a subset of cohorts is observed"). With 9 or more pre-years for every cohort, it is unclear which cohort is missing at those leads. Report for every event time the number of countries and cohorts contributing and the number of observations. A missing base year g−1 drops a country-cohort from the group-time estimate silently.
  - Revise the abstract wording to match.
- **Unbalanced panel, 61 gaps.** Missingness is not analysed. The dictionary expects it to be correlated with conflict and low capacity, and the identification strategy registered a balanced-panel re-run of the main sample. The only balanced analysis is the Goodman-Bacon subsample, which is 13 countries with 3 treated, selected for complete data. That subsample reproduces a TWFE coefficient of 17.07 against 23.4 for the full sample, so it is not representative. Its 95.6% weight statement says nothing about the full panel, and the text should say so. The proper registered check is to run the main CS estimator on the balanced panel.
- **Selection of the secondary samples.** NER (684), completion (56% coverage) and male/female GER (76.9% against 79.0% for total) are subsamples. The paper does say the NER sample is reduced. It then treats the gross-minus-net difference as comparable (see Section 6).

## 5. Variables and units

- **Outcome.** GER is correctly defined (UIS, % of official-age population, can exceed 100). The paper does not say that the denominator is a UN population estimate, which is where much of the measurement error enters.
- **Log GER.** The log specification is fine, and there are no zeros. The 21% figure (exp(0.192) − 1 = 0.211) is correct. The comparison with the level effect is not like for like: 22 pp on a treated pre-reform mean of roughly 80 would be about a 27% increase. Say which baseline is used, or explain the gap.
- **Completion rate.** The completion rate cannot register the surge within an event window of five years. For Uganda (1997), the first entrants reach the last grade after six or seven years, so e = 6 or later. The data cannot show whether higher enrolment turned into completion, and the null in Section 5.4 is mechanically uninformative. The discussion uses the "insignificant completion effect" as a policy argument for investing in teachers and classrooms. This should be removed, or the window extended. SE.PRM.CMPT.ZS also counts new entrants to the last grade regardless of age, so it shares the over-age problem and can exceed 100.
- **Gender.** Gender results use GER levels. Girls start from lower GER in many cohorts, so an equal increase in percentage points is a larger proportional gain for girls, and the registered gender parity index (H4 and the plan §7.1) was not used. Male/female GER also have a slightly different sample from total GER.
- **Covariates.** Log GDP per capita and urban share are measured at g−1. GDP per capita is available for 95.6% of rows. The number of observations in the covariate-adjusted run is not reported. Under-five mortality and population were loaded but are not used in any specification, although the summary table lists under-five mortality.
- **Units.** GER, NER and completion are all percent; the paper is consistent about percentage points. State the GDP base year (constant 2015 US$) in the data section.

## 6. Measurement quality

- **Denominator and reporting error.**
  - GER depends on UN population estimates that are extrapolated between censuses and revised. The data summary says several other breaks look like revisions. The pre-registration says denominator error biases the estimate only if it correlates with adoption timing, and that this cannot be verified. The registered check using enrolment counts (SE.PRM.ENRL), which would remove denominator error from the numerator-side effect, was not run, and counts were never loaded. This is the most important missing robustness check on the data side. It should also include a population-denominator vintage comparison (e.g. a fixed-population GER).
  - Fee abolition and the grants that accompanied it changed administrative reporting incentives. Capitation grants (Ghana, Uganda, Kenya) are tied to head counts, schools had to register previously informal pupils, and community schools were absorbed into the public system. This produces a mechanical post-policy rise in recorded enrolment that is not a rise in actual enrolment. The plan flagged this as an alternative explanation (§5.4, §8). The paper does not mention it at all, and the conclusion states that the evidence "indicates that abolishing fees raised enrolment by a large amount". A paragraph on reporting inflation and the limits of administrative data is needed, and the abstract should talk about recorded enrolment.
- **Over-age enrolment (H2).** The paper concludes that "the gain is not driven mainly by over-age enrolment" and that "the NER estimate suggests it is a genuine increase".
  - The gross-minus-net difference is 1.33 pp (SE 2.5), so the 95% interval is roughly −3.6 to 6.3. The data cannot exclude a gap of several points, and the sample is selected: on the NER sample the GER effect is 14.8, against 22.0 in the full sample.
  - A one-third lower GER effect suggests the NER sample is dominated by later cohorts or by countries with a different mix. The cohort composition of the NER sample (which treated countries, how many pre-period NER observations each) should be reported. The identification and data documents themselves say NER has few pre-period observations for several treated countries.
  - The NER ATT also needs the NER baseline level to be interpretable. NER is capped at 100, so a "13-point" gain has a different meaning at a baseline of 60 than at 85. The text should be softened, because the paper's own caveat ("we cannot rule out a moderate role") conflicts with the strong sentence in the introduction.
- **Breaks that coincide with treatment.** The two largest jumps among treated units (Malawi 1995, Uganda 1997) fall exactly at abolition and contribute most to the effect (Uganda 51.8, Malawi 41.5 pp). Dropping Uganda lowers the estimate to 17.5. Part of this is real policy response and part may be a series break. The paper cannot separate them, and should say that the estimate is sensitive to these two series. The drop-outlier check does not help here, because the Uganda 1997 observation is below the 150 flag.
- **Winsorizing.** The registered 1/99 winsorizing was not run. Only the drop of flagged rows is reported (21.17).

## 7. Inference, as it depends on the data

- **Few treated clusters.** The paper uses a t distribution with 46 degrees of freedom because there are 47 clusters, but the variation comes from 8 treated clusters in 6 cohorts, five of them with one or two countries. With degrees of freedom closer to 7, the critical value is about 2.4 against 2.0. The CI of 10.9 to 33.2 becomes roughly 9 to 35 for the same SE, which would still exclude zero. The bigger concern is the SE itself.
- **The standard errors differ widely across estimators with nearly the same point estimate.** CS 5.5, Sun-Abraham 5.7 (unit bootstrap), TWFE 9.7, BJS 10.3. A bootstrap on 8 treated units tends to understate uncertainty. The statement that the estimate is "stable across estimators" is true for the point estimate and not for inference: the TWFE wild p-value is 0.062 and the BJS p-value is 0.032. The registered wild bootstrap for Sun-Abraham and the registered randomization inference were not run. Both should be run, or the headline significance level ("at the 1 percent level") should be softened.
- **Sensitivity analysis.**
  - The relative-magnitude bound uses M = 3.27, the largest consecutive change among the estimated pre-period coefficients. Those coefficients have standard errors of 5 to 8 and so are mostly noise. M is therefore a noisy input, and the breakdown value of 0.98 is correspondingly uncertain.
  - The abstract says "moderate violations … would make the effect statistically indistinguishable from zero". The breakdown is at about the size of the largest pre-period change, and the 3.3 pp consecutive change is small relative to the 22 pp effect. The framing of this result as fragile or robust needs to be made consistent between the abstract (fragile), the results text, and the Section 5 note ("robust up to roughly the size of the largest pre-period change").
- **The event study is not flat.** The abstract says the profile "is flat before the reform". The pre-coefficients are −5.1, −5.3, −3.6 at leads −6 to −4, then −0.34 and 0.08 at −3 and −2. That is a drift of about 1 pp per year in the four years before treatment, all of it imprecise. The Wald p = 0.98 is not evidence of flatness, as the paper itself says elsewhere. Align the abstract.
- **Base-period inconsistency.** The econometric specification says the main run uses a varying base for pre-periods. The paper and the results use the universal base g−1. The pre-period coefficients depend on this choice, so state which one produced the figure.
- **Country-level effects (H3).** The country ATTs are described in the specification as "post minus pre". If the post-minus-pre version is used, they carry no comparison group. They are then regressed on the pre-reform mean GER, which is the same noisy quantity that enters the ATT through its base, so a negative slope arises mechanically (regression to the mean, flagged in the plan §7.2). With 8 observations, the slope of −0.71 (p = 0.185) adds nothing, and the text rightly calls it imprecise. Clarify how the country ATTs are computed.

## 8. Registered checks not reported (protocol compliance)

The following were registered in the identification strategy, the dictionary or the plan. They are not in the results, and the paper does not say so.

- Announcement-year dating (d).
- Dropping conflict country-years (f).
- Enrolment counts as an outcome (g).
- Winsorizing at 1/99% (g).
- Window variants such as 1990–2012 (h). The one reported variant, [-5,5], leaves the ATT unchanged by construction.
- Never-treated fake-date placebos (i).
- Gardner two-stage estimator (b).
- Wild bootstrap for Sun-Abraham (l).
- Randomization inference.
- Leave-one-cohort-out. Only leave-one-country-out was run, and since there are two two-country cohorts the two differ.
- Dropping late cohorts.
- Dropping small island states.
- The balanced-panel re-run of the main estimate.
- ±1 year coding, and the Tanzania 2001 alternative that Section 4 says is used.
- Aid per capita as a covariate (the series was dropped).
- Placebo on secondary GER.

A short table of "registered, run, not run, reason" in the appendix would settle this. The paper should also say that H5 (capitation grants) and H6 (pupil-teacher ratios) could not be estimated, as it does for H5 in the last paragraph of Section 5. The H6 gap is not disclosed.

## 9. Presentation and replication

- Remove the `% src:` comments before submission, or keep them in a replication log. They are useful for checking but they expose pipeline file names.
- `tables/summary.tex`, `main.tex` and the other tables are not visible in the draft I received, so I could not check the summary statistics against the code. Spot-checks I could do all agree: t = 22.04/5.54 = 3.98, the CI of 10.9 to 33.2 with t(46), exp(0.1917) − 1 = 0.211, 14.78 − 13.45 = 1.33, 5.83/3.84 gives p = 0.136, the mean of the event-time coefficients 0 to 5 is about 22.2, and the 8.9 to 51.8 range is consistent with the raw cohort means.
- The paper has no balance table, no sample flow table, and no figure showing treated against comparison raw GER by event time. The figures exist (`fig_ger_event_time.pdf`, `fig_ger_cohort_trends.pdf`) and should be included.
- Provide the treatment table, the exact WDI pull date and checksums, and the bootstrap seed (20261013) in a replication package. The hand-built date table is the part another researcher cannot reconstruct from the paper.

## 10. Priority actions

1. Verify and extend the treatment chronology: two sources per country, school-year conventions, and the likely abolishers among the 41 comparison countries. Either drop them or code them. Rerun everything with the result.
2. Check the UIS year convention and run ±1 coding, especially for Malawi and Ghana.
3. Run the main estimate with Ghana, Lesotho and Zambia excluded as the primary specification (as registered), and present the full set as the alternative.
4. Run the registered measurement checks: enrolment counts, winsorizing, and a balanced-panel run. Add a paragraph on reporting incentives.
5. Reconcile the counts: NER 684 against 596, outliers 9 against 5, the 39/41/43 comparison counts, 48 against 49 economies. Add a sample flow table and the number of contributing countries per event time.
6. Align the claims with the evidence in the abstract and conclusion: "flat" pre-trends, "sparse" pre-period, the strength of the over-age conclusion, and the completion-rate policy argument. Use a small-cluster procedure for the headline inference or report it alongside.
7. Add a baseline balance table and a comparison group restricted to similar countries.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
