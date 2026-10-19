# Methods Review: Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021

Paper ID: 66f43096-d973-4dc0-afaa-d086434dd927
Reviewer: methods_reviewer
Design reviewed: descriptive cross-sectional study of GHO indicator RS_198, 2021. No regression, no causal claim.

## Overall assessment

The design fits the question. A descriptive question about the distribution of a published indicator needs the distribution, the regional summary and the extremes, and the draft supplies these. The draft is also honest about the central measurement problem: the values are WHO model estimates, the age-standardisation status is unknown, and the paper makes no causal claim.

Several things stand between the draft and acceptance. Two of them are contradictions in the record that the paper's numbers depend on: the WHO regional aggregates do not match the unweighted regional means for two regions (one by a large margin), and two excluded countries carry a published "0.0" in the raw text. The paper's headline claim that the bounds are absent may come from the pull rather than from WHO. The estimation method is described without a source. The cross-check against WHO's published aggregates, which the plan required, has not been done. Each is fixable, and none requires new estimation.

## Must change

**M1. Regional means are unweighted, and the paper does not say so; WHO's regional values disagree for two regions.**
Location: Section 3.2 (Regional differences), Table `regions`, Abstract, Introduction.
The draft reports the "regional average" as the mean across countries. The data summary records the WHO REGION rows: AFR 19.4, AMR 14.1, EMR 16.4, EUR 6.7, SEAR 16.1, WPR 15.2. The unweighted country means are AFR 19.44, AMR 14.1, EMR 16.7, EUR 6.70, SEAR 15.9, WPR 10.8. The gap for WPR is 4.4 points, and it changes the ordering. Under WHO's regional values WPR ranks fourth, ahead of AMR. Under the unweighted means it ranks fifth, and the draft calls it "in the middle of the range".
Fix: (a) state in the Data section that regional means are unweighted country means, with n per region; (b) report the WHO REGION values alongside, state how they differ and why (population weighting is the likely cause for WPR, where one large country dominates, but this must be checked, not assumed); (c) either drop the claim that WPR sits in the middle or qualify it by the weighting. The population-weighted mean the plan mentioned would settle this if population data are available; if not, say it is unavailable.

**M2. The Global Status Report cross-check required by the plan has not been run.**
Location: Section 2 (Data), no corresponding text; plan section 5 ("Cross-check").
The plan requires comparing the replicated global and regional aggregates with the GSRRS 2023 figures before drafting, with any discrepancy explained. The draft does not report this, and M1 shows that a discrepancy exists. This check is the natural place to resolve M1.
Fix: run the comparison, report the result and the cause of each difference in Section 2, and cite the edition used.

**M3. Hong Kong SAR and Macao SAR: the record says both "0.0" and "no value".**
Location: Section 2 (Sample construction), sentence "Two countries, Hong Kong SAR and Macao SAR, have no numeric value..."; data summary "Sample flow" and "Missingness" paragraphs; estimation summary "Sample flow".
The raw `value_text` for HKG and MAC reads "0.0" while the numeric `value` is null. The data summary says WHO "publishes no 2021 estimate" for these two. Both statements cannot describe the same record without an explanation. If WHO's text field says 0.0, the numeric null may be a parsing failure, and then the sample has two false zeros excluded, which is harmless for the exclusion but unsafe for the zero check in Section 3.3. If WHO suppresses the value, the text "0.0" is wrong and should not be read as a value.
Fix: inspect the raw JSON for HKG and MAC, establish what the text field carries, and state the finding in Section 2. Whichever the answer, state the rule applied.

**M4. The absence of uncertainty bounds may be a pull artefact, and the paper's second limitation rests on it.**
Location: Section 2 (Data, "carries no uncertainty bounds"), Section 4 (Limitations, second limitation), Abstract.
The data dictionary and the data summary report that `low` and `high` are null in all 197 rows, and that the bounds were not confirmed as published for RS_198. The draft nonetheless states as fact that the extract "carries no uncertainty bounds" and builds the limitation on it. An all-null result for two columns in a model-based indicator is a reason to check the query and the GHO metadata before asserting it. If WHO publishes intervals for this indicator and the pull dropped them, the paper's claim is wrong and the descriptive conclusions about ordering need a different caveat.
Fix: check the GHO indicator metadata and the raw JSON fields (including whether the endpoint returns bounds under other names). Then write either "WHO publishes bounds for RS_198 and they are reported as X" or "the GHO extract used here returned no bounds; we did not confirm whether WHO publishes them." The current text states the second as the first.

**M5. The estimation method is described without a source.**
Location: Section 2.1 ("WHO derives such estimates by modelling the available information... combine observed data with model assumptions"); Section 4 ("corrects for underreporting" is not in the draft but is the implied mechanism behind "where registration is incomplete, the estimate reflects the modelling assumptions").
The literature review returned no methods source for RS_198 (no WHO technical documentation, no GSRRS edition describing the model). The draft makes methodological claims about WHO's model without citing anything. The literature review is explicit that these must not be cited from memory.
Fix: obtain and cite the WHO technical documentation and the GSRRS edition that describes the current estimate, or reduce the Section 2 description to what the GHO metadata states and mark the rest as unverified.

**M6. Age standardisation is unknown, but the paper compares countries on the rate.**
Location: Section 2.1 (last sentences), Section 4 (third scope condition), Conclusion.
The draft handles this honestly in the text. The data summary and data dictionary, however, require the paper to state which version is used "once the metadata check is done", and the check has not been done. The draft still uses "rate" throughout the Introduction and Results as if the series were understood. Cross-country comparisons of crude rates are confounded by age structure, so the status of the series is the single most important measurement fact for the paper's interpretation.
Fix: resolve from the GHO metadata (or the GSRRS methodology note). Until then, the Abstract and Introduction should say "an estimated rate of unconfirmed standardisation" rather than "the rate".

**M7. The explanation for the two zero values is unsupported, and the sensitivity of the lower tail is not reported.**
Location: Section 3.3 ("both are very small populations, where a zero in one year is more plausible...").
The claim that a zero is "more plausible" for small populations is a substantive assertion without a source, and it is not a method. A zero in a model-based series is more likely a model or reporting artefact (see M3). The draft also says "the lower tail depends on them" but does not show it. Sensitivity was in the analysis plan and is missing.
Fix: report the minimum and the 5th percentile with and without MCO and NIU (the analysis spec already requires a with/without-tails sensitivity), state that the zeros are treated as published, and remove the population-size explanation or source it.

**M8. Skewed distribution reported with mean and SD, without skewness-appropriate statistics.**
Location: Section 1 (Introduction, "mean of 13.3"), Section 3.1 (Table `summary`).
The draft describes the distribution as right-skewed but reports no skewness measure, and the only evidence for the skew is that the mean is 1 point above the median. The descriptive guidance for skewed positive quantities asks for the statistics of the logarithm or the geometric mean, with the choice stated. Mean and SD are reported as headline values for a distribution the paper calls skewed.
Fix: report the median and quartiles as headline values, add the geometric mean or the log-scale mean and SD with a statement of which, and either report a skewness statistic or drop the word "right-skewed" in favour of what the histogram shows.

**M9. Variance decomposition: eta-squared is biased upwards and is described causally.**
Location: Section 3.2 ("Regional membership accounts for about 39 percent of the total variation"), Abstract ("accounts for about 39 percent").
Eta-squared rises mechanically with the number of groups and is biased upwards in small samples. With six regions of sizes 9 to 53, the bias is not negligible. "Accounts for" also reads as an effect. The draft's own caveat ("a description of how countries cluster, not a test") is correct, but the wording in the Abstract is not.
Fix: report epsilon-squared or the bias-adjusted eta-squared alongside the 0.391, and replace "accounts for" with "the share of total variance lying between regions is" in the Abstract, Section 3.2 and Conclusion.

## Should change

**S1. Histogram bin width: state the rule and show a second width.**
Location: Section 3.1 ("equal-width bins of 3.74").
3.74 is the Freedman–Diaconis width for these data (2 × IQR × n^(−1/3) = 2 × 10.85 × 195^(−1/3) ≈ 3.74). The draft should say so and cite the rule, since the descriptive guidance asks for the bin rule. The draft also says "Most countries lie between 3.7 and 18.7" without a count or share. Give the share, and check the conclusion (the four countries above 30, and the apparent gap) at a second bin width, such as 2.5 or log-spaced bins as the guidance recommends for quantities spanning orders of magnitude.

**S2. Quantile set differs from the plan.**
Location: Section 3.1. The plan promised the 10th and 90th percentiles and a kernel density overlay; the draft reports the 5th and 95th percentiles and no density. Either report what the plan promised or amend the plan in the paper's data note. Both are cheap.

**S3. Uncertainty statement on the regional and ranking claims.**
Location: Section 3.3 (ranking), Section 4 (second limitation). The draft says ordering differences smaller than one point should not be read as reliable. That is right and should be applied consistently: "Kenya and Nepal tie at 28.2" and "the Maldives (1.3), Norway (1.5), Malta and Singapore (both 1.9)" are ordered by differences that the paper itself calls unreliable. Use "tie" and "within one point of" language where the order is not robust.

**S4. "Member States" versus the sample.**
Location: Section 1 ("for each Member State"), Section 2 ("195 countries"). The sample includes Niue, which is a WHO associate member, and excludes HKG and MAC, which are also associate members. Use "reporting locations" or "countries and areas" and state the inclusion rule.

**S5. "Roughly three times" is 2.9.**
Location: Abstract and Section 3.2. The draft's computed ratio is 2.9. "Roughly three times" is fine as prose but the Abstract should give 2.9 or "about 2.9 times" so the reader can check it against the table.

**S6. Figure and table provenance.**
Location: Figure 1 and `tables/summary.tex`, `tables/regions.tex`. Neither the table files nor `run_estimation.py` are in the context, so the numbers in the tables cannot be checked against the script here. The reviewer checked the in-text numbers against the stated results summary only. Confirm that the table cells are generated from `estimation_results.json`.

**S7. Consistency of the sample description with the plan.**
Location: Section 2.2. The plan promised a full ranked table as an appendix and a regional box or strip plot. Neither is in the draft. The ranked table is useful for a descriptive paper, since readers cannot otherwise check the regional and rank claims, and the appendix would also hold the 197-row sample flow.

## Reproducibility

- The GHO extract is identified by URL, release date (2024-04-15) and SHA-256 hash, which is good practice. The replication package should contain the raw JSON or CSV itself, not just the URL. The live API can change, and the paper's data would otherwise depend on the web at run time.
- The analysis uses no randomness, so no seed is needed. If any bootstrap interval is added (M4 may require one for a correlation), state the seed.
- Country names come from Natural Earth 50m; the join is on ISO3 and unmatched codes are reported. This is reproducible from the public release.
- The region names and codes come from the REGION rows and `parent_location`. They were not checked against an external WHO list. Do this before naming the regions in print (see M1 and M2).
- Dependence on the web: the GHO API and the Natural Earth download. Both are pinned by hash in the data dictionary, which covers the requirement.

## Sensitivity and alternative choices

| Choice | Alternative | Changes the conclusion? |
|---|---|---|
| Unweighted regional means | WHO population-weighted REGION values | Yes for WPR (10.8 vs 15.2) and for the order of WPR relative to AMR. Must be reported (M1). |
| Keep MCO and NIU zeros | Exclude them | Affects the minimum and lower tail only. Report (M7). |
| Equal-width histogram, 3.74 | Second width or log bins | Not checked. Report (S1). |
| Eta-squared | Epsilon-squared | Magnitude only. Report (M9). |
| Mean and SD | Median, IQR, geometric mean | Changes the reading of the distribution. Report (M8). |
| Country rows only | Include the REGION rows | No effect on country statistics; the aggregates are used only as a cross-check (M2). |

## Closing summary

The paper answers a descriptive question with a descriptive design and says so. Its main results (the median, the spread, the top and bottom countries, the 2.9-fold regional ratio between Africa and Europe) are supported by the stated data and computations. Its weaknesses are concentrated in the record: the WHO regional values disagree with the paper's regional means for WPR and EMR and SEAR, the HKG and MAC values conflict, the absence of bounds may be a pull problem, and the method and age standardisation are unresolved. These need checking before the paper's wording can be trusted. The required cross-check is not done.

Scored 5 of 10. Major revision: the design is sound, and the number of open measurement questions and the unreported WPR gap are what keep the score there.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
