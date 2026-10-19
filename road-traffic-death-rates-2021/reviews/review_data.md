# Data review: Estimated road traffic death rates across countries and WHO regions, 2021

## Scope and what I could verify

I checked the draft's data section, results section, and limitations against the realized numbers in `data_summary`, `data_dictionary.json`, and the "Realized numbers" block of the econometric specification. I did not have `estimation_results.json`, `tables/*.tex`, or the figure files in my context. Statements that cite only those files (regional medians and SDs, the 5th and 95th percentiles, the bin counts, the region ranges) are therefore unverified here. Everything listed below as "consistent" was checked against figures I could see.

## What checks out

- National distribution: N = 195, median 12.3, mean 13.3, SD 7.8, min 0.0, max 37.4, IQR 7.3 to 18.1 all match the realized numbers.
- Between-region share of 39 percent matches eta-squared = 0.391.
- Top ten: the names and order match the ranking. The region counts (five AFR, three EMR, one AMR, one SEAR) are correct. Kenya and Nepal are tied at 28.2 at the cut-off, and the draft says so.
- Bottom ten: the names match, and seven of ten are EUR, which is correct. The Maldives (SEAR) and the two WPR entries are also correct.
- Region counts (AFR 47, AMR 36, EMR 22, EUR 53, SEAR 9, WPR 28) sum to 195.
- Sample flow 204 to 197 to 195 matches the data summary.
- The regional ratio of 2.9 (19.44 / 6.70) is arithmetically correct.

## Findings

1. **Major: regional means in the draft are unweighted country means, but the paper does not say so, and they disagree with WHO's own regional estimates in the same load.** The data summary lists WHO's REGION rows: AFR 19.4, AMR 14.1, EMR 16.4, EUR 6.7, SEAR 16.1, WPR 15.2. The draft reports AFR 19.4, AMR 14.1, EMR 16.7, EUR 6.7, SEAR 15.9, WPR 10.8. The WPR gap is large (10.8 against 15.2), and it changes the middle of the ranking. Section 3.2 calls these "regional averages" without a weighting statement. The paper needs to (a) state that the means are unweighted across countries, (b) report WHO's regional values next to them, and (c) explain the WPR difference, most likely a population-weighting effect from large WPR countries. The plan's cross-check against the Global Status Report 2023 was also not carried out or reported. Without it, the reader cannot tell whether the sample reproduces WHO's published aggregates.

2. **Major: the treatment of Hong Kong SAR and Macao SAR is inconsistent across the documents.** The data summary says WHO publishes no 2021 estimate for them. The estimation specification says their `value_text` reads "0.0" while the numeric value is null. A raw "0.0" is exactly the coded-zero problem the checklist warns about. Either WHO published a zero-like placeholder or the text field is a parsing artefact. The draft says only that they have "no numeric value", so it hides this. Verify the raw GHO record and state in Section 2 what the text field shows and why it is not a zero.

3. **Major: the description of the population is inaccurate.** The draft says "Member States" and "195 countries". The data summary says Hong Kong and Macao are associate members, not Member States. Niue, which is included, is also an associate member of WHO. The sample therefore is not "WHO Member States with a published estimate". It is "countries and territories in the GHO RS_198 country rows with a numeric 2021 value". Correct the wording in the abstract, introduction, and data section, and in the citation text.

4. **Major: the vintage and access details are missing from the paper.** The data dictionary records release 2024-04-15, the source URL, the SHA-256 hash, and an access date. The draft gives none of these, only "the GHO API ... for calendar year 2021". The checklist requires the vintage, the access route, and a persistent identifier. Add the release date, the access date, and the URL or a pointer to the replication package.

5. **Major: the zero-value claim is unsupported.** Section 3.2 says a zero "is more plausible" for very small populations. Nothing in the data or the sources shows this. Monaco and Niue may be real zeros or a model floor. The draft's own limitations section says a zero carries no information about precision. Either cite evidence for the reading or state it as an open question. Confirm the raw records for both countries, since the value and the text should agree.

6. **Moderate: age standardisation is still unresolved.** The draft is honest that the series is not described as crude or age-standardised, and the limitations discuss the age-structure confound. But the data dictionary, the data summary, and the spec all list this as a source check still open. It must be resolved from the GHO metadata before submission. Until then, the abstract and the title should not imply a crude rate.

7. **Moderate: the missingness mechanism is not discussed.** The two excluded territories are missing because WHO does not publish an estimate for them. That is structural, not random. The draft cites Little and Rubin for dropping missing values, but a reader needs the mechanism stated: the sample excludes these places for a reason tied to their status, not at random.

8. **Moderate: the WHO region names are not verified.** The data summary and the dictionary say the six region names were read from the `parent_location` text and not checked against an external WHO list. The draft names the regions as final. Either check against the WHO list or note in the text that the names come from the GHO load.

9. **Minor: the intro says "explains" for the 39 percent.** An eta-squared is a description of how variance is partitioned, not a model that explains it. Section 3.2 uses "accounts for", which is the right wording. Use it in the introduction too.

10. **Minor: the phrase "most countries lie between 3.7 and 18.7" is vague.** The bin counts are in the results file, which I could not check. Give the count (for example, "N of 195 countries") rather than "most".

11. **Minor: the rank table in the plan's appendix is not in the draft.** This is not an error, but the plan promised a full ranked table with data-quality flags. The reader cannot check the top and bottom lists against the full ranking without it.

## Items I could not verify

- Regional medians, SDs, and ranges (for example, the African range 6.6 to 37.4 and the EMR range 4.7 to 34.0).
- The 5th and 95th percentiles (2.4 and 27.9) and the bin counts.
- The regional table file and the figure file. The draft's `\input{tables/regions.tex}` and `fig_death_rate_hist.pdf` were not in my context.

## Overall

The numbers that I could check agree with the realized statistics, and the sample flow is documented. The data section, however, understates three things: what the regional aggregates are and how they compare with WHO's own, what the excluded territories' raw values show, and what population the sample describes. Those need fixing before the paper is credible on its own terms. The unresolved age-standardisation question and the un-run Global Status Report cross-check also block a clean data check.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
