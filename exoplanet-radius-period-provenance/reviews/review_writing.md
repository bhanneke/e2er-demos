# Writing Review: "How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance"

Scope: prose, argument flow, evidence-claim alignment, hedging, consistency. I did not see the compiled tables (`groups`, `radius_stats`, `period_stats`, `associations`) or the figures, so I checked the text only against the numbers quoted in the draft, the data summary and the data dictionary. The researcher's correction (the giant-planet hump at 8 to 15 R_E is 55% calculated radii, 846 of 1,529) is present in the abstract, results and conclusion, with the correct counts. I did not look for other changes.

## 1. Overall assessment

The paper is short, honest about its descriptive status, and the core structure works: question, data and rule, distributions, group comparison, diagnostic, limitations. Most numbers in the text are internally consistent. For example, 10^0.71 = 5.1, 10^1.65 = 45, 846/1,529 = 55%, and 1,537 + 4,810 + 48 + 50 = 6,445.

The weaknesses are of four kinds:
- (a) a few claims that go beyond, or contradict, the evidence the paper shows;
- (b) a few factual statements that conflict with the data summary;
- (c) a Data section that reads like a pipeline log instead of a methods section;
- (d) a results section that recites bin counts instead of interpreting them.

All are fixable in prose. None requires new analysis, except where flagged.

## 2. Priority issues: evidence-claim alignment and factual consistency

**2.1 "The groups overlap little" is not supported and is contradicted two sentences later (Abstract, Section 3.1, Intro finding).**
- The abstract says the two groups "overlap little in the radius-period plane". Section 3.1 says the KS distances of 0.53 (radius) and 0.61 (period) mean "the groups overlap little in either dimension".
- A KS distance of 0.53 is the maximum CDF gap. It does not mean little overlap. The paper itself reports that the 90th percentiles of radius differ by a factor of only 1.1 "because giant planets occur in both groups", and that 846 of 1,215 calculated planets lie at 8 to 15 R_E, where 683 transit-measured planets also sit.
- No joint (two-dimensional) overlap measure appears in the draft. The spec and plan list joint counts and cell shares, but the paper reports none.
- Fix: say that the groups overlap in radius (giants) and separate mainly in period. Quote the radius and period medians in the abstract. Either report the joint cell shares or delete "in the radius-period plane".

**2.2 "Almost entirely radial-velocity discoveries" is partly produced by the sample restriction (Intro contribution 3, Section 2.2, Limitations).**
- The data summary gives the calculated group as 1,133 RV, 292 microlensing and 52 imaging among all 1,537 planets, so RV is 74%. In the analysis sample it is 1,133 of 1,215 (93%).
- The 322 calculated planets dropped for a missing period are mostly microlensing. The paper never mentions microlensing or the 322 dropped planets. The sample-flow sentence treats the period filter as neutral across groups, yet it removes 0 of 4,810 transit-measured planets and 322 of 1,537 calculated ones (21%).
- Fix: report the 322 excluded calculated planets and their method mix in Section 2.1. Qualify the RV claim ("in the radius-period sample"). Confirm that the 1,133, 876 and 326 in Section 2.2 are in-sample counts. The arithmetic is consistent only if all 322 excluded planets carry a true mass.

**2.3 Contribution 3 contradicts the Limitations section.**
- The Intro says the non-overlap region is informative "about discovery method, not about planets".
- Limitations says the difference "combines the properties of planets with the properties of the two discovery methods".
- The paper never shows any within-method analysis, so it cannot say "not about planets". Use the Limitations wording: the comparison cannot separate provenance from method. The same applies to "informative about discovery method". Method composition is reported, but no analysis isolates method as the driver.

**2.4 Factual error in Section 2.2: "planets found by direct imaging or timing methods".**
- The data summary lists the 48 measured, non-transiting planets as imaging 41, radial velocity 5 and orbital brightness modulation 2. No timing planets are among them.
- Timing planets (TTV 25, ETV 15, pulsar timing 6) sit in the calculated group. Correct the sentence.

**2.5 "Directly measured radii" (Intro, third finding) overstates what the label implies.**
- The group is defined as "radius not labelled CALCULATED_VALUE and tran_flag = 0". Of its 48 planets, 41 are imaging detections, whose radii typically come from evolutionary or atmospheric models rather than a direct measurement.
- Use "radii not labelled as calculated" and avoid "directly measured". The same caution applies, more mildly, to "transit-measured". That label rests on tran_flag = 1 plus the absence of the calculated label, not on reading each reference. Say so once, in Section 2.2.

**2.6 The mass-radius diagnostic (Section 3.3) is under-interpreted and partly circular.**
- (i) The text compares rho = 0.47 for calculated radii with rho = 0.93 for the 4,786 transit-measured planets "with a mass". The data dictionary says `pl_bmasse` can itself be a mass computed from a radius via a mass-radius relation (see `pl_bmassprov`). If so, 0.93 is partly circular. The paper must report the mass-provenance split for this group, or restrict to planets with measured masses.
- (ii) A calculated radius is a deterministic function of the mass used, so rho = 0.47 is surprising. It points to the flat Jovian regime of the relation, or to a composite-table mismatch between the mass in `pl_bmasse` and the mass used for the radius. "Consistent with a relation that is not increasing over the full mass range" is an untested hypothesis, so state it as one or test it, for example by reporting rho within mass bins.
- (iii) The sentence "the calculated radii cluster below the upper bound of 14.3 Earth radii" says nothing as written. If you mean a pile-up near 12 to 14 R_E (median 12.6, upper quartile 13.4, maximum 14.3), say that. That pile-up is the interesting result: more than half of the giant-planet hump consists of radii compressed by the relation's plateau, so the hump's shape is partly an output of the assumed relation. This links the diagnostic to the researcher's key finding, and the draft currently does not make that link.
- (iv) The sample sizes disagree: the correlation uses 1,215 planets, while the figure (per the figure check) plots 1,537. State the n in the caption. The 0.93 also lacks the interval given for the other coefficients.
- (v) The Conclusion's "their radii are bounded by the mass-radius relation" is a mechanism claim that this section only gestures at, and the Limitations section itself says the diagnostic "does not validate" the radii. Hedge it: "are bounded at 14.3 R_E, as expected if the relation flattens at high mass".

**2.7 "Within the range that transit surveys cover" (Section 3.2) is unsupported.**
- The 1,000-day cap is a convenience, not a documented survey limit. The paper gives no source for it, and Kepler-type baselines make detections near 1,000 days rare (only 26 transit-measured planets lie between 300 and 1,000 days).
- Rephrase to "within the 1,000-day range that holds almost all transit-measured planets (4,804 of 4,810)", or cite a source.
- Possible count inconsistency: 1,215 − (186 + 176) = 853, but the text gives 855 calculated planets at P ≤ 1,000 d. This is explainable if two planets sit at exactly 1,000 d and the bins are left-closed. Confirm, and state the closure convention for all bins.

**2.8 The limit-flag robustness check is almost vacuous.**
- Only 5 planets are removed, so "unchanged at 0.71 and 1.65" is guaranteed by construction. Present it in one clause as a sanity check, not as robustness.
- The plan and spec promise a second bin width (check 7c), and the hump claims rest on coarse, unequal-ratio bins (2–4, 4–8, 8–15). The draft reports no such check. Add one sentence saying whether the two humps and the 4–8 trough survive the finer 0.1-dex histogram, or drop the word "humps".

**2.9 The final questions in the Conclusion are incoherent with the paper's own rule.**
- Question 1 asks what happens "if replaced by transit-measured radii for planets that have both". Section 2.2 shows that all 1,537 calculated planets have tran_flag = 0, apart from two transit discoveries, so no calculated planet has a transit radius in this archive.
- The Limitations suggestion (planets with a measured transit radius and a mass) is the workable version: apply the same relation to the masses of transiting planets and compare. Rewrite the question that way.
- Question 2 (match on discovery method) is not feasible at scale. The method overlap is 28 RV planets in the transit-measured group against 1,133 in the calculated group. Say this, or drop the question. Both questions are very long sentences. Keep one, in one sentence.

## 3. Argument flow and structure

- **Intro, paragraph 2 to Intro, paragraph 4.** The three "findings" and the three "contributions" overlap heavily. Contribution 2 ("quantify where the groups differ, with bootstrap intervals") restates finding 2 and is a method, not a contribution. Merge the two lists. State the contribution once: a reproducible decomposition of the archive by its own label, and the finding that both radius humps carry different provenance mixes.
- **Intro omits the researcher's main finding.** The hump-composition result (1,901 of 2,090 versus 846 of 1,529) is in the abstract and conclusion but not among the three Intro findings. Add it, since it is the clearest answer to the research question.
- **Roadmap.** "In the next section… Afterward… Then…" is clunky and omits the mass-radius diagnostic that Section 3 contains. Use numbered sections, or cut the roadmap to one sentence.
- **Known structures never revisited.** The Intro invokes "a dense cloud… a population of giant planets… a sparse region", but the Results never connect the humps and the 4–8 trough to anything known. The literature review supplies the radius-valley and desert papers (Fulton et al. 2017, Mazeh et al. 2016, among others), and none is cited. Even one paragraph in Section 3.1 would orient readers. Say that the 2–4 R_E hump lies above the valley region studied with precise transit radii, and that the paper makes no occurrence claims. Without this the paper has almost no engagement with literature on its own topic.
- **Chen and Kipping is never cited in the text.** The archive's relation is the central object, so name it in Section 2.2 and cite the paper (`chen2016probabilistic`). Note the year caveat from the literature review: the paper appeared in 2017, the bib says 2016.
- **Data section as pipeline log.** Section 2.1 contains five negative disclosures in a row: "We did not load…", "We also report no robustness table…", "we did not code radius references by hand or validate…". The Limitations section then repeats two of them. Consolidate them into one short paragraph in Limitations. In Section 2.1 keep only what a reader needs to replicate the sample.
- **Missing from the Data section:** the snapshot date (13 Oct 2026; the archive changes weekly), the table DOI, and the archive's requested acknowledgement. "Several thousand confirmed planets" in the Intro should be the actual count and date (6,445).
- **Results paragraphs open with announcements or are number dumps.** Examples: "Figure 1 shows…", "We compare quantiles of…", "Figure 3 compares…". Lead with the finding and cite the figure parenthetically. The paragraph beginning "Separating the groups changes this picture considerably" carries about 25 numbers in nine sentences, most duplicated in the tables. Keep the 6 to 8 that carry the argument (medians, the 8–15 R_E counts, the share of each group above 300 days) and let the tables hold the rest. Binned counts such as "2,085… 1,430… 189 above 3,000 days" need a denominator or percentage; counts without totals are hard to read.

## 4. Hedging, precision and consistency

- **Population language.** The conclusion opens "Confirmed exoplanets are concentrated at short periods…". The plan's own language rule requires "in the archive" or "catalogued planets". The title may keep the research-question wording, but the abstract and conclusion should carry the scope qualifier in the sentence. Likewise "Readers tend to interpret this picture…" and "routinely read" are claims about readers with no citation. Cite an example, or soften to "can be read".
- **Normative conclusion.** "Readers… should therefore treat the two provenances separately" is a recommendation the paper does not test. Phrase it as "the pooled diagram combines two provenances; analyses that use archive radii for population statements should state the provenance."
- **Causal "because" and "thus" clauses.** "…because giant planets occur in both groups" explains a number by composition and is acceptable. "The period gap therefore partly reflects the long-period tail" is also a fair descriptive reading. "The pooled association thus mixes two groups" and "describes neither" assert a decomposition that is not shown. A pooled rho of 0.30 sits between 0.08 and 0.40, which is what a location shift between groups would produce, but the paper has not decomposed it. Also, "exceeds the association within the transit-measured group" is true of 0.08 but not of 0.40, and the sentence reads as if it covers both.
- **Interpretation of bootstrap intervals.** The intervals describe resampling variability of a non-random catalogue. One sentence should say what they cover, and that no population is implied. KS distances have no intervals; say so.
- **Internal tension on the 20 non-transiting planets.** They are "too few for distributional statements", yet the text then gives their medians (period 15,958 d, which is about 44 years) and a correlation of 0.63 with an interval of 0.16 to 0.87. Give the units a reader can use, or drop the statistics and leave the n.
- **Vague quantifiers.** "typical" (Intro, finding 2) means median; say so. "changes this picture considerably", "far above", "only 421" and "cluster" should be replaced by numbers or comparisons. "Only 421" should be compared with the neighbouring bins on a per-log-width basis.
- **Units.** Differences in log10 radius and period (0.71, 1.65) need "dex" on first use. Alongside a baseline, report each as a ratio, as the text does for most.
- **Terminology.** The same group is called "transit-measured", "measured, transiting", "measured transiting" and in the plan "S1T"/"mass-derived". Define two labels once ("calculated" and "transit-measured") and use them throughout. Also standardize "this paper", "this study", "our study", "the study".
- **Tense.** Section 2.1 mixes present ("We drop", "We use") and past ("We did not load", "we did not code"). Use present tense for what the paper does and the paper's methods; use the past only for completed external work.
- **Numbers.** "percent" is used consistently in text; keep it. Check spelled-out versus digit numbers at sentence starts. None found, but "Ten percent"-type starts should stay avoided.
- **Citations to verify.** `cloutier2024exoplanet`, `little2019statistical`, `foremanmackey2016the` and `nielsen2019the` are not among the keys the literature review released to the drafter. Check that each exists in `literature.bib`, and that the cited paper supports the specific sentence. `foremanmackey2016the` is a population-inference paper cited for "transit favours large short-period planets and RV favours massive planets". A selection-function reference would fit better, or cite the archive's discovery-method documentation. The Intro cite for "has become the standard summary" needs the same check.

## 5. Conciseness and sentence-level edits

- "The study is purely descriptive: it documents patterns in the catalogue, not in the planet population, and makes no causal claim." Good, but "purely" is redundant with "descriptive".
- "We use the planets with a value for each statistic and report the number of planets next to every statistic." Reword: "Each statistic uses all planets with a value; we report n throughout." Then make sure the tables do carry n for every statistic.
- "We keep values that the archive flags as limits in the main sample (a robustness check removes them)." Fine, but say how many (7).
- "A calculated radius is a function of mass and an assumed relation, so its distribution mirrors the distribution of masses and the shape of that relation." Strong sentence. Keep it, and move the idea up to Section 2.2, where the group is defined.
- "Our analysis yields three main findings" → "We find three things."
- "In counts, 846 of the 1,215…" → "By count, 846 of the 1,215…" or merge into the preceding sentence.
- The limits-versus-selection discussion is clear, and its first sentence is a topic sentence. Good. The paragraph is dense; split at "Imaging surveys…".
- "Calculated radii inherit the assumptions of the mass-radius relation and, for 876 planets, rest on a minimum mass, so the true mass and radius may be larger." In the flat Jovian regime a larger true mass need not give a larger radius, so qualify with "radius may be larger for planets below the plateau".

## 6. Checklist verdict

| Item | Status |
|---|---|
| Topic sentences / argument visible from first sentences | Partly. Method-announcing openers in Section 3 |
| Roadmap matches structure | Mostly; omits the mass-radius diagnostic |
| Claims match evidence | Several gaps: 2.1, 2.2, 2.3, 2.5, 2.6, 2.7 |
| Descriptive language, no causal claims | Good overall; population wording in the conclusion; "thus mixes" |
| Numbers with units and baselines | Mostly; add "dex", denominators for bin counts, n for 0.93 |
| Hedging | Over-claiming in 2.1 and 2.3; fine elsewhere |
| Redundancy | Findings vs contributions; three repetitions of 846/1,529 and 1,901/2,090; Data vs Limitations disclosures |
| Terminology consistency | Needs one pass |
| Literature engagement | Weak; no radius-valley, desert or mass-radius citations in the text |

If the fixes in section 2 are made (2.1 to 2.9), the paper will be clear and defensible as a short descriptive note. The remaining work is mostly trimming.

OVERALL SCORE: 6/10
RECOMMENDATION: Minor Revision
