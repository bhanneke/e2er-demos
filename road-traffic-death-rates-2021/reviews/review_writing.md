# Writing review: Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021

Reviewer: writing_reviewer
Scope: prose, argument flow, evidence-claim alignment, hedging, consistency, and the researcher's two pending changes. Numbers were checked against the figures quoted in estimation_results.json and the data summary, not against the raw data. Citation keys were not verified against literature.bib.

## Summary

The paper is short, descriptive, and mostly disciplined about causal language. Its numbers agree with the realized outputs: the regional counts (5 AFR, 3 EMR, 1 AMR, 1 SEAR in the top ten; 7 EUR in the bottom ten), the four countries above 30, and the 39 percent between-region share. The main problems are (1) causal-sounding verbs for a variance share, (2) process notes written as paper text, (3) a few unsupported claims stated as fact, and (4) one sentence in the Limitations section that is a run-on. None of these changes the findings. All are fixable in the prose.

## Researcher's pending changes

1. Histogram in Section 3.1: done. `\includegraphics` with `fig:death_rate_hist` and a caption naming WHO GHO RS_198, 2021 is in the draft, and the text refers to `Figure~\ref{fig:death_rate_hist}`. The ten bin counts are not listed in the prose.
2. "four countries exceed 30": done. The text says "four countries exceed 30", which matches Guinea (37.4), Libya (34.0), Haiti (31.3), and Guinea-Bissau (30.5).

Both changes are already in the draft. No further edits are needed for them.

## Major issues (fix before submission)

1. **Causal verbs for a variance share.** The Abstract says "WHO region membership accounts for about 39 percent of the variation in national rates." The Introduction says "WHO region membership explains about 39 percent of the total variance." The Results define this figure as the between-region share of the total sum of squares (eta-squared), which is a description of how variance is partitioned. "Accounts for" and "explains" both imply an explanatory relation the paper disclaims. Use: "The between-region share of the total sum of squares is 39 percent" (Results), and in the Abstract "Regions separate 39 percent of the variation in national rates." The Introduction should follow the same wording.

2. **Process notes written as paper text.** Several sentences describe the analyst's checking process, not the research:
   - Data section: "The paper therefore does not describe the rates as crude or as age-standardised until the GHO metadata has been checked." This is an open source check. Either resolve it (state which series is used) or state the status as a limitation.
   - Limitations: "Whether WHO publishes uncertainty bounds for RS_198 at all has not been confirmed from the API, and the paper does not state that they exist." Rewrite as a fact about the extract: "The extract used here contains no lower or upper bounds. We do not know whether WHO publishes bounds for this indicator."
   - Data section: "The data check finds no duplicate keys, no unmatched country codes, and no value outside the plausibility range." Keep the result as a data fact, and drop the reference to a check. The check report should be cited as a deliverable, or the sentence should describe the rule applied.
   - Data section: "The sample flow and the full data-quality results are reported in the accompanying data quality report." No such report is in the package. Include it or remove the reference.

3. **Sample description is inaccurate.** The Abstract and Introduction call the 195 analysed units "countries." The data summary notes that Hong Kong SAR and Macao SAR are associate members, not Member States, and the sample also includes Niue, which is a WHO associate member. The Introduction says RS_198 reports "for each Member State." Use "WHO reporting locations" or "countries and areas," and state the membership status of the non-Member States in the Data section. The 195 count should be stated as "195 WHO reporting locations, of which N are Member States."

4. **Unsupported claims stated as fact.**
   - Zeros for small populations: "a zero in one year is more plausible than in a large country." No source or data supports this. A modelled rate of exactly zero is unusual for any country with road deaths. Replace with "Both are very small populations. A model output of exactly zero for a country this size should be checked against the source, and we do so below." Then either check it or say the check is pending.
   - "Where registration is complete, estimates and counts should agree closely; where it is incomplete, the estimate reflects the modelling assumptions." This is a plausible claim about the estimation method, but it has no citation, and the literature review found none. Mark it as an expectation ("we would expect") or cite the WHO method documentation once it is available.
   - "WHO derives such estimates by modelling the available information on road traffic deaths for each country." The method is central to the paper and currently has no citation. The literature review states that no WHO technical source is in literature.bib.
   - "Estimates of the death rate per 100,000 population are the usual basis for comparing countries." Add a citation or soften to "a common basis."
   - "Road traffic injuries kill a large number of people each year." Quantify with a cited figure from WHO, or remove.
   - "Missing values are listed and dropped... following the standard practice for descriptive samples with missing data \citep{little2019statistical}." The citation supports handling missing data in general, not dropping units with missing outcomes as standard practice. Reword: "We drop units without a value and do not impute, which is the simplest option in a descriptive sample with two missing units (see \citealp{little2019statistical} for the general treatment)."

5. **Zero values: the claim about the lower tail is overstated.** Results: "the lower tail of the distribution depends on them." Two zeros out of 195 move the 5th percentile only a little. The data summary planned a sensitivity check of the extremes, but the paper does not report it. Either report the 5th percentile with Monaco and Niue excluded, or drop "depends on them."

## Minor issues

6. **Vague sentence about the African region.** "The African region's concentration in the top group is consistent with its high regional mean, although the Eastern Mediterranean region contributes more of the top group than its share of countries would suggest." The first clause says nothing. Replace with the counts and shares: "Five of the ten are African. The Eastern Mediterranean accounts for three of the ten but only 22 of 195 countries (11 percent)."

7. **Run-on sentence in Limitations, paragraph 1.** "...and its findings describe WHO's estimates, and they speak to the underlying road safety outcome only to the extent that the estimates track it." Split into two sentences: "Its findings describe WHO's estimates. They speak to the underlying road safety outcome only to the extent that the estimates track it."

8. **Median and mean wording.** "The mean of 13.3 lies slightly above it, which is consistent with a right tail." A mean above the median is consistent with a right tail, but also with other shapes. Say "which indicates a right tail" or "the gap is consistent with a right-skewed distribution." Then the Conclusion can say "right-skewed" with the same support.

9. **"Most countries lie between 3.7 and 18.7."** No count is given. The reader cannot check "most." Give the share: "X of 195 countries lie between 3.7 and 18.7."

10. **"Several-fold" in the Conclusion.** The text correctly reports a 5th to 95th percentile ratio of about 11.6. "Several-fold" understates this. Use "more than tenfold between the 5th and 95th percentiles" to match the Results.

11. **Abstract last sentence and "no causal claims".** The sentence "The paper makes no causal claims" is accurate but reads as a disclaimer, not a finding. Move it to the end of the Introduction, where the Introduction already says the same thing, and drop it from the Abstract. Keep "The values are model-based estimates" in the Abstract, since that is the key caveat.

12. **Expletive and passive constructions.** Some passive sentences can be active without loss: "Two countries... are excluded" becomes "We exclude two countries"; "Missing values are listed and dropped" becomes "We list and drop units with missing values." Limited number; fix when editing the Data section.

13. **Future work sentence.** "Future work could establish whether the same ordering holds for registered deaths..." It is specific enough to keep, but it should name the data source (for example, the countries with complete vital registration) so it is clearly a suggestion, not a hedge.

14. **Terminology.** The paper uses "estimated rate," "death rate," "road traffic death rate," and "road traffic deaths" in the same passages. Pick "estimated road traffic death rate" for the measure and "deaths" for counts, and use each consistently.

15. **Roadmap.** The Introduction's roadmap matches the sections (2 Data, 3 Results, 4 Limitations, 5 Conclusion). No change needed.

16. **Spelling.** The paper uses British spelling consistently ("analysed," "summarise," "standardisation," "neighbouring"). Keep it.

## Citations to verify

I did not check these against literature.bib. The literature review states that the local library holds no methods source for RS_198, the WHO estimation model, or the Global Status Report. Confirm each key resolves to a real entry before submission:
- `WHO_GHO` (data citation; the data dictionary gives the full citation text, which can be used directly)
- `NaturalEarth` (data citation)
- `little2019statistical` (missing data; see item 4)
- `hyndman1996sample` (quantile definition; this is the correct reference for type 7 quantiles)

The paper currently cites no WHO methods document for the estimation model, no Global Status Report edition, and no source for the estimated versus registered gap. Items 2 and 4 depend on these.

## Anti-slop check

No banned phrases from the reference list appear. The phrases "plays a crucial role," "it is worth noting," "interestingly," and "this paper contributes to" are absent. The draft does contain "explains" and "accounts for" (item 1), and "consistent with its high regional mean" (item 6), which are the same problem in other words.

OVERALL SCORE: 7/10
RECOMMENDATION: Minor Revision
