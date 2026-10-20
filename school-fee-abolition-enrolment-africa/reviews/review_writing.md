# Writing Review: "Did Abolishing Primary-School Fees Raise Enrolment? Evidence from Staggered Reforms in Sub-Saharan Africa"

Scope: prose, argument flow, evidence-claim alignment, hedging, consistency. The tables (`summary`, `main`, `robust_level`, `robust_log`, `mechanism`) and the event-study figure are not in the material I received, so I could not check them against the text. Methodological soundness is left to the technical and identification reviewers. I flag it only where the wording misstates the design.

## 1. Overall assessment

The paper is well organised and mostly direct. It states its limits openly, which is rare and valuable. The abstract, introduction and results follow one thread. Sentences are mostly active and the roadmap matches the sections.

Four problems keep it from being ready:

1. **Internal inconsistencies.** Country counts, outlier counts, the base period, the inference description and the covariate set differ across sections or against the supporting documents.
2. **Several claims go beyond the evidence.** The main ones are "flat before the reform", "genuine increase in participation", "did not close the gender gap", and the policy claim about supply.
3. **Numbers lack baselines and units.** The headline effect is judged against the wrong mean, and the key sensitivity result is never translated into plain units.
4. **Characterisations of the literature rest on titles only.** The literature scan states that relevance was "judged from titles only, not read". Several sentences in Section 2 describe what cited studies do or find.

## 2. Priority issues (fix first)

### 2.1 Country counts disagree
- The introduction says 8 treated countries and "39 countries for which we have no abolition date". The Data section says "The other 41 economies", and the Discussion says "the remaining 41 economies".
- The numbers are consistent only if the 41 includes two countries with no GER data. The paper never says so. The estimation sample has 47 countries (8 + 39).
- Fix: state once, in the Data section, "49 economies; 47 with GER; 8 treated and 39 comparison; 2 economies without GER dropped". Then use 39 wherever the comparison group in the estimation is meant.
- For the call for verified dates (Discussion), say "the remaining 41 economies" and note that 39 enter the estimation.

### 2.2 Outlier count disagrees with the data summary
- The paper says "Nine observations are flagged as outliers (GER above 150 or below 10)". `data_summary.md` lists 5 flagged country-years (MWI 1995 and RWA 2007–2010).
- The `% src` comment points to `sample_flow.rows_ger_outlier_flag`, which may be computed over a wider window. Reconcile the number or name the window.
- Nine is also the number of year-on-year jumps above 20 points. The sentence "Nine year-on-year changes ... Nine observations are flagged" invites confusion between the two sets.

### 2.3 Base period and inference are described inconsistently
- Section 4 says "the universal base period g−1". The econometric specification says "varying base for pre-periods and base g−1 for post-periods". The results document says "universal base" for the event study.
- Pre-period coefficients differ between the two choices, and the sensitivity analysis is built on them (M = 3.27). Use the choice the estimates actually use and say so once.
- The text says "multiplier bootstrap with 999 draws, clustered by country". The specification describes a country-level (pairs) bootstrap with SE equal to the standard deviation of the draws, and 499 draws for Sun–Abraham and BJS. The paper should name the procedure accurately and give the draws for each estimator.
- The sentence "we base inference on a t distribution with 46 degrees of freedom, since only 8 of the 47 clusters are treated" does not follow. 46 is G−1 for all 47 clusters. Having only 8 treated clusters is an argument for a more conservative reference distribution, not the justification for 46 df. Either justify 46 df correctly or report the result with fewer degrees of freedom as a sensitivity check. With 7 df the 95 percent interval widens from about [10.9, 33.2] to about [8.9, 35.1], still excluding zero.

### 2.4 Covariates and checks differ from the plan, and the paper does not say so
- The Data section lists "GDP per capita, urban share, and under-five mortality" as covariates. The controlled specification uses log GDP per capita and urban share only. Under-five mortality never appears again.
- Aid per capita, the most obvious confounder named in the plan and in the strategy ("Reforms were typically adopted alongside donor funding"), was dropped because the metadata endpoint failed. The paper never mentions this. The covariate check therefore cannot address the donor-funding threat it is introduced to address. State this where the threat is discussed.
- Several pre-registered checks were not run: randomization inference, never-treated fake-date placebos, Gardner two-stage, dropping conflict years, announcement-year re-dating, and a wild bootstrap for Sun–Abraham and BJS. The paper should list what was not run in one sentence. Silent omission reads as selective reporting.

### 2.5 "Flat before the reform" overstates the pre-period
- The abstract says the event study is "flat before the reform". The introduction says "no systematic pre-reform divergence ... in the two years before abolition". The results show negative leads of −3.6 to −5.3 at e = −4 to −6 (SEs 5–8), and the paper itself says they are "compatible with a rising pre-reform trend".
- The two-year window is cherry-picked in the introduction. Use the same window the Wald test uses (e = −6 to −2).
- Replace in the abstract with: "Pre-reform coefficients are individually and jointly indistinguishable from zero, but the longest leads are negative and imprecise."
- The joint Wald statistic of 0.76 on 5 df (p = 0.98) is unusually small. Add one clause saying it reflects large bootstrap standard errors, not a close fit, and refer to the power point you already make.

### 2.6 The sensitivity result needs plain units
- "The breakdown value is 0.98, so a deviation slightly smaller than the largest observed pre-period change is enough to make the effect statistically insignificant" is correct but opaque. A reader will find it surprising, since the largest pre-period change (M = 3.27 points) is small against a 22-point effect.
- Say that the bound lets the post-period violation accumulate across the six post-treatment years, so a drift of about 3 points per year can erase most of the gain. State M in points.
- Say that M is large mainly because the early leads are imprecise, so sampling noise inflates it. This is the honest reading, and it pre-empts a referee's question.
- The abstract's "moderate violations" is vague. Replace with "violations as large as the largest pre-period change".
- The sentence "We use a conservative closed-form bound here, not the exact procedure, so the bound is likely wider than necessary" belongs in Section 4, where the method is introduced. It also undercuts the cautionary finding without saying by how much. Say that exact intervals could be narrower and that the breakdown value should be read as an upper bound on fragility.

## 3. Evidence–claim alignment

| Location | Claim | Problem | Suggested fix |
|---|---|---|---|
| Abstract, Intro | "stable across heterogeneity-robust estimators, comparison groups, and leave-one-country-out samples" | The estimate is stable in the level specification. The log TWFE benchmark is 0.150 (wild p = 0.21), BJS has a standard error nearly twice the baseline (10.3 vs 5.5), and the level TWFE wild p is 0.062. | "The point estimate is stable (17.5 to 24.4) across ...; the BJS and TWFE estimates are less precise." |
| Results §5.1 | "Because the mean GER in the descriptive sample is 85.6 percent, this is a large effect." | The 85.6 mean is for the 1985–2010 sample (n = 1,006). The ATT comes from the 1980–2010 sample (n = 1,211). The relevant baseline is the pre-reform mean of the treated countries. | Report the treated group's pre-reform mean, then "equal to X percent of the pre-reform mean". |
| Intro, Results | "an increase of roughly 21 percent in log terms" | "In log terms" is ambiguous. 0.192 log points equals 21 percent after exponentiation. | "0.192 log points, equivalent to a 21 percent increase." |
| Intro, Results | Gross vs net: 22 vs 13 points | The two are on different samples. On the NER sample the GER effect is 14.8, not 22.0. The abstract and introduction put 22 and 13 side by side. | State in the abstract: "On the common sample the gross effect is 14.8 and the net effect 13.4." Treat the drop from 22.0 to 14.8 as a finding (sample selection or heterogeneity), not a footnote. |
| Results §5.4 | "the NER estimate suggests that the gain is a genuine increase in participation among children of primary-school age" | The difference GER−NER is 1.3 (SE 2.5). The 95 percent interval is roughly ±5 points. That rules out a large over-age share only if the effect is measured in comparable units, which a one-point difference in levels does not guarantee. The next sentence admits the estimate is imprecise. | Lead with the caveat: "We find no evidence that over-age enrolment accounts for much of the gain, though the interval does not exclude a gap of about 6 points." |
| Results §5.4 | "Fee abolition did not close the gender gap in gross enrolment on average." | A causal, definitive statement from a difference of 0.2 (SE 2.7). The data do not show that the gap was not closed. They show no differential gain. | "We find no evidence that girls gained more than boys (difference 0.2, SE 2.7)." |
| Results §5.2 | Placebo of 3.9 "is small relative to the main effect and not significant" | With an SE of 4.7, the placebo has little power and its sign matches the main effect. | Report the interval and call it uninformative at this precision. |
| Results §5.1 | "the static estimator is not distorted much by forbidden comparisons in this subsample" | The decomposition covers 13 countries and 3 treated units, and the balanced-panel TWFE coefficient is 17.1. The paper then relies on this to dismiss the problem. | Say explicitly that the result does not generalise to the full unbalanced sample, as the econometric document does. |
| Results §5.3 | "Restricting the event window to [−5,5] gives the same estimate as the baseline." | Not a robustness check. The overall ATT uses e ≥ 0 only, so the result is identical by construction. | Delete, or state that it is mechanically unchanged. |
| Discussion ¶1 | "fee removal can move enrolment substantially even where governments cannot immediately expand supply" | No supply variable (classrooms, teachers, pupil–teacher ratio) is observed. The paper's own strategy section notes that reforms "were often accompanied by new funding". | Remove, or restate: "enrolment rose even though class-size data suggest ...", which you cannot support. |
| Discussion ¶1 | "the insignificant completion effect ... suggest[s] that access gains should be paired with investment in teachers" | An insignificant coefficient (5.8, SE 3.8) is not evidence of lagging completion. Its interval [−1.7, 13.3] lies mostly below the enrolment effect but is also compatible with zero. The recommendation is not derived from the results. | Frame as motivation, not as a finding, and cite the Uganda evidence alone. |
| Discussion ¶1 | "roughly 22 percentage points on average over six years ... large amount ... in sub-Saharan Africa" and "Our evidence indicates" | The sample is eight self-selected reformers, and the effect is fragile to trend violations. The generalisation to the region and the verb "indicates" are under-hedged. | "Among the eight reforming countries, our estimates suggest ..." |
| Intro ¶3 | "the effect is statistically significant at the 1 percent level" | With 8 treated clusters and the pre-period concerns, this headline invites the criticism the paper later makes. | Add "under country-clustered inference with 46 degrees of freedom". |
| Intro ¶5, Strategy | The not-yet-treated comparison group is said to address "undetected abolishers" in the comparison group | The not-yet-treated group still contains the 39 undated countries. It cannot address contamination from unknown abolishers. | Say that this check addresses the use of already-treated units as controls, not undated abolishers. The latter remains a limitation, as the Discussion says. |

### Treatment definition and framing
- The strategy document excludes capitation-grant-only reforms from treatment. Ghana (2005) is nonetheless treated, and the text says "weaker form of abolition" in one place and "not strictly an abolition" in another. The introduction and abstract say all eight countries "abolished" fees.
- State the departure from the identification strategy once, early, and say how it enters the results (the drop-ZMB-and-GHA estimate is 24.4). Otherwise a referee will see an unflagged protocol deviation.
- Lesotho is phased, and Uganda initially capped eligibility at four children per family. The paper says "package of national fee-removal policies" in Section 3 but "abolition" elsewhere. Pick one term for the estimand and use it consistently, or use "fee-removal reforms" throughout.

## 4. Literature claims (verify before submission)

- The literature scan says its topic papers were judged "from titles only, not read". Section 2 nonetheless asserts what several do, for example: Kan and Klasen "relate it to subsequent educational outcomes"; Oketch and Somerset and Wallström examine Kenya's programme "and its consequences for school choice"; Lindsjö and Pajibo emphasise "capitation grants and school-level funding". Each such sentence needs the cited paper's abstract or text checked.
- "These studies ... typically lack a comparison group of countries that did not reform at the same time" is misleading. The single-country studies use within-country comparison groups (for example, cohort exposure designs in Uganda). The accurate statement is that they cannot speak to cross-country generalisation.
- The paper omits the closest empirical work named in the literature scan: Deininger (2003), Grogan (2009), Al-Samarrai and Zaman (2007), Lucas and Mbiti (2012), Avenstrup et al. (2004). Lucas and Mbiti on Kenya is the most important omission. None is in the bibliography yet. Add them after verification, or acknowledge the omission.
- The scan also records that the gap claim has not been checked by exhaustive search. The paper nonetheless states it as fact: "most of the existing evidence consists of single-country case studies" and "rarely examined for its implications for inference". Either support these with a search statement or soften.
- Citations are missing for the factual claims in Section 3 (Jomtien, Dakar, Malawi 1994/95, Uganda's four-child cap, Lesotho's grade-by-grade phase-in, Ghana's capitation scheme). Only the abolition years in Section 4 carry cites.
- For Malawi, Lesotho, Rwanda and Zambia the paper says the dates "are recorded in the data dictionary with their references". A reader cannot see the data dictionary. Cite the sources (Chimombo 2009; the Lesotho and Rwanda DOIs; the Zambia concept paper) in the text or a table.
- Introduction, first paragraph: "governments reported that millions of children enrolled within a year" is cited to Kan and Klasen and Oketch and Somerset. State the figure and its original source (ministry or World Bank report), or cite the report directly.
- The two Fermah et al. 2026 entries (`fermah2026school`, `fermah2026effect`) look like duplicates or a preprint/published pair. Confirm and keep one. The keys `pajibo2017influence`, `nishimura2011the` and `lindsjo2017everybody` do not appear in the literature scan's citable list, so check that they resolve.
- The Discussion says the results "provide national-level support for the cross-country syntheses". A synthesis of enrolment effects supported by your point estimate is not independent corroboration. Say whether your 22 points is smaller or larger than the pooled estimate.

## 5. Structure and flow

- **Introduction.** The first paragraph is strong, but the third and fourth sentences join independent clauses with commas ("Yet fees were only one component ..., classrooms and teachers could not expand overnight, and gross enrolment ratios rise mechanically ..."). Split into two sentences. "Few education policies have produced headlines as dramatic as ..." is an unsupported superlative; delete "as dramatic as" or cite.
- **Contributions.** The third contribution ("we document how fragile inference is") is a limitation, not a contribution. The second ("separate gross from net enrolment on a common sample") is a robustness check, and its result is weaker than the framing suggests (see §3). Reduce to one precise contribution statement: a common-design estimate across eight reforms with an explicit sensitivity bound.
- **Repetition.** The 22-point result and the pre-trend caveat are restated at nearly identical length in the abstract, introduction, results and discussion. The introduction's third paragraph repeats the full numbers of the results section. Keep the headline number and the single most important qualification in the introduction, and move event-study detail to Section 5.2.
- **Related Literature.** Mostly a catalogue of citations. The first paragraph ends with the useful point (single-country work cannot show generalisation) but buries it. Lead each paragraph with its claim. The final sentence of Section 2 ("rarely examined for its implications for inference") is a claim without support.
- **Data section.**
  - Two samples appear (1,211 in 1980–2010 for estimation; 1,006 in 1985–2010 for description). The reader meets both before learning which one is used where. Present the estimation sample first and move the descriptive window to the Table 1 note.
  - The panel ends in 2010 "so that later abolitions do not enter the comparison group" is a non-obvious claim. Truncation drops post-2010 years but does not remove countries that abolished later. Explain: the comparison group is observed only up to five years after the last treated cohort.
  - The paragraph beginning "Three features of the data deserve emphasis" is a single block of seven or more sentences with embedded comment lines. Split it by feature.
  - The pre-period coverage statement ("four countries have no GER observation before 1995") does not say whether any treated country is among them. Report pre-reform observation counts for the eight treated countries, the quantity that matters for the design.
- **Section 5.2 (pre-trends).** The pre-period paragraph carries about ten sentences and four ideas (leads, composition, power, placebo). Split into pre-trend evidence, composition at long leads, and placebo. Order the subsection so the reader meets the caveats before the sensitivity numbers, which then follow naturally.
- **Section 5.3.** The sentence "although Uganda and Malawi, the two early adopters with the largest country-level effects, contribute the most" implies a leave-out for Malawi that is not reported. Report the Malawi leave-out or drop the claim.
- **Section 5.4.** The final sentence about capitation grants ("We also cannot estimate ...") is a one-sentence paragraph placed under completion. Move it to the limitations and note that hypothesis H5 was not testable.
- **Transitions.** The sections end without a bridge, except the Data section. Add one sentence at the end of Section 3 stating that the two heterogeneity features (scope and supply constraints) are what Section 5 will probe.

## 6. Sentence-level and style points

- **Slop and filler to cut or sharpen**
  - "Our study makes three contributions" → state them.
  - "These results come with an important qualification" → "Three qualifications apply".
  - "consistent with the broad pattern reported in country studies" (Results 5.2) → name the pattern and cite.
  - "we examine sensitivity to the most heterogeneous cases" (Section 3) → "we drop Zambia and Ghana in a robustness check".
  - "Several threats are specific to this setting." → delete and begin with the first threat.
  - "Future research should address two specific questions." is acceptable because it is specific. Keep.
- **Passive constructions.** Mostly acceptable. Candidates for active voice: "Pre-trend tests are reported but not relied upon" → "We report pre-trend tests but do not rely on them"; "Treatment is the first year of national fee abolition" → "We code treatment as ...".
- **Terminology**
  - Treatment status: "undated comparison group", "never-treated", "never-abolishers", "controls", "comparison countries". The first and last are intended. "Never-treated" appears in the Goodman–Bacon sentence ("treated with never-treated countries") and in the strategy ("never dated as treated"). Use "undated comparison countries" consistently, with one definition of the Callaway–Sant'Anna "never-treated" role.
  - Effect size units: "points", "percentage points", "pp". Define "points" once as percentage points of GER.
  - "Fee abolition", "fee removal", "fee-free", "free primary education": pick one for the policy and use a qualifier for variants.
- **Spelling and typography**
  - British (enrolment, labour, programme) and American (summarizes, emphasizes, harmonized, analyze) are mixed. Choose one; Oxford -ize with British roots is acceptable if applied consistently.
  - "p-value" and "$p$-value" are both used; "(p-value 0.98)" is set in text mode.
  - "t = 3.98, p < 0.001" and "p = 0.0002" (in the supporting document) are not in conflict, but pick one reporting convention.
  - "10 percent" style is used consistently ("percent"), which is good. Keep.
- **Tense.** Methods are in the present ("We estimate"), results in the present ("Table shows"), and literature in the present ("evaluate"). Past tense is used for the placebo and reforms. Acceptable, but keep literature findings in the past tense in the Related Literature section ("found") as suggested in the checklist, or choose present throughout.
- **Leftover pipeline artefacts.** The `% src:` and `% computed:` comment lines are in the manuscript. They are useful for provenance, but strip them from any submitted version. `\author{}` is empty.
- **Hedging.** Generally calibrated. Under-hedged: "Our evidence indicates", "the increase is persistent" (observed over five post-years only), "genuine increase". Over-hedged: none material.
- **Numbers.** Add a baseline whenever an effect appears (treated pre-reform mean), and give the confidence interval for secondary outcomes in the text. Currently NER, gender and completion are given as point estimates with SEs only.

## 7. Items to check once the tables and figure are available

- Every number in the text against the corresponding table cell (22.0, 5.5, 19.1, 24.4, 21.2, 13.4, 14.8, 5.8).
- The event-study figure: label the horizontal axis as event time in years with the reference period at −1, and mark which cohorts contribute at each lead and lag, since the text says composition changes at the longest leads.
- Table notes: sample, clustering, bootstrap draws, degrees of freedom, base period, covariates.
- Whether Table 1 reports under-five mortality, and whether summary statistics are shown separately for treated and comparison countries by treatment status.

## 8. Recommended edits (ordered)

1. Reconcile counts (39 vs 41, 5 vs 9 outliers), the base period, the bootstrap description and the degrees-of-freedom rationale.
2. Replace "flat before the reform" and "two years before abolition" with the five-lead test plus the negative-lead caveat.
3. Report the treated pre-reform mean and recompute "large effect" against it.
4. State, in the abstract and introduction, the common-sample GER (14.8) vs NER (13.4) comparison, and soften "genuine increase" and "did not close the gender gap".
5. Translate the breakdown value into points per year and note that M is inflated by imprecise leads.
6. Disclose the omitted aid control, the unrun pre-registered checks, and the treatment of Ghana as a departure from the written strategy.
7. Verify and correct the literature characterisations; add the missing key Kenya, Uganda and Malawi studies; cite the sources of all eight dates and the background claims.
8. Remove the policy claim about supply and the completion-based recommendation, or tie them to evidence.
9. Cut repetition across abstract, introduction, results and discussion; restructure the contributions paragraph; split the long paragraphs in Sections 4 and 5.2.
10. Standardise terminology and spelling, and strip the provenance comments.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
