# Literature Review: Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021

Referee role: literature. Scope: coverage, appropriate citation, and whether the paper positions its contribution against the existing measurement and descriptive literature. The data pipeline and results were read only where they bear on citation accuracy.

## DIMENSION SCORES

- Contribution: 4/10
- Identification: 6/10
- Empirics: 6/10
- Writing: 6/10
- Literature: 3/10

Weighted overall: 0.25(4) + 0.25(6) + 0.20(6) + 0.15(6) + 0.15(3) = 5.05

## Summary

The paper is careful and modest about what it claims. It makes no causal statements, flags that the RS_198 values are model estimates, and says so in the limitations. The arithmetic I could check against the stated sources is consistent. The main problem is that the paper hardly sits in the literature at all. It cites four keys (WHO_GHO, NaturalEarth, little2019statistical, hyndman1996sample). None of them is a source for the thing the paper actually measures. The estimation method, the WHO report that publishes the 2021 figures, and the existing presentations of the same distribution are all absent. The paper's own plan says its contribution is to replicate and extend what the Global Status Report on Road Safety already presents. The draft never mentions that report. Until it does, a reader cannot tell what the paper adds.

## MAJOR CONCERNS

1. **The source of the data is not cited.** Section 2 says WHO "derives such estimates by modelling the available information on road traffic deaths," and it describes the figures as combining observed data with model assumptions. No source is given for either statement. The only data citation is the GHO API key WHO_GHO, which is a database citation and not a methods citation. The paper needs (a) the WHO technical documentation for the RS_198 estimation model and (b) the Global Status Report on Road Safety edition that publishes the 2021 country estimates. Per the literature-review file, neither is yet in `literature.bib`, and the literature search returned no methods source. The fix is to verify the exact report titles, editions, and DOIs or URLs, record them, and cite them in Section 2 at the point where the estimation method is described. Do not cite from memory.

2. **The contribution is not positioned against existing presentations.** The paper plan (section 7) says the WHO Global Status Report presents the estimated rate by country, region, and income group, and that this paper "does not replace that presentation." The draft does not say this. The introduction does not mention the report, or any prior descriptive account of cross-country road death rates. A referee would ask immediately what is new relative to the report. The paper's claimed contributions (full ranked table, within-region spread, variance share, reproducible code path) can be stated in the introduction only after the report is cited and the paper says which of its contents it extends. Income-group comparison is in the plan and absent from the draft. The paper should either add it or state that it is out of scope and why.

3. **The benchmark against WHO's published aggregates is missing and the gap is large.** The data summary lists the GHO REGION values: AFR 19.4, AMR 14.1, EMR 16.4, EUR 6.7, SEAR 16.1, WPR 15.2. The paper reports unweighted country means: AFR 19.4, AMR 14.1, EMR 16.7, EUR 6.7, SEAR 15.9, WPR 10.8. Four of the six agree closely. The Western Pacific difference is about 4.4 deaths per 100,000 (15.2 against 10.8), which is not a rounding issue. The draft does not say whether its regional figures are unweighted or population-weighted. It also does not reconcile them with the published aggregates. The plan required this cross-check before drafting, and the data summary states that it was not done. The paper must (a) state that its regional summaries are unweighted country means, (b) show the published WHO regional values alongside its own, and (c) explain the Western Pacific gap or state that it is not explained. Population weights would be the obvious check, and the plan notes they may not be in the same source. If they are not available, say so.

4. **Citation of Little (2019) does not support the sample decision.** The draft says that dropping the two countries with no value follows "the standard practice for descriptive samples with missing data \citep{little2019statistical}." Little and Rubin's work on missing data is about the conditions under which complete-case analysis is unbiased, and it argues against casual listwise deletion. The two excluded units (HKG and MAC) are not missing at random in any sense that matters here. WHO does not publish a 2021 estimate for them because they are associate members, not Member States. Their exclusion is a sample-definition choice, not a missing-data mechanism. The citation should be removed from that sentence, and the sentence should say that the exclusion follows from the definition of the sample. If a missing-data reference is still wanted, it should be paired with a sentence on the mechanism.

5. **"Countries" and "Member States" are used interchangeably, and the sample may not match the definition.** The draft says the sample covers "195 countries" and, in Section 2, that GHO covers "each Member State." The data summary describes HKG and MAC as associate members. Niue, which is in the sample with rate 0.0, is also a WHO associate member. The WHO has 194 Member States. The count of 195 therefore probably includes at least one associate member, which conflicts with the sentence in Section 2. The paper should describe the sample as "WHO-reported countries and territories with a 2021 RS_198 value," cite the WHO membership list, and state how many entries are Member States. Do not change the N until the membership status has been checked against that list.

6. **The zero values are asserted without a source.** The draft says Monaco and Niue are "very small populations, where a zero in one year is more plausible than in a large country," and that this makes zero "an unusual model output." Neither claim is cited. The paper should either cite a source for the model's treatment of low-count or small-population countries, or remove the explanation and report the zeros as a fact of the published series. A reader will ask how WHO's model produces a zero, and the paper cannot answer from its current references.

7. **Age standardisation is an open question that the literature can settle.** The draft says the series' age standardisation is unknown and that the paper "does not describe the rates as crude or as age-standardised until the GHO metadata has been checked." This is the correct posture for now. But it is a checkable fact about a published indicator. The indicator definition in the GHO metadata, or the WHO methods documentation from item 1, should state it. Once it is checked, the answer should be cited in Section 2, and the Limitations paragraph on age composition should be rewritten to say what is known rather than what is unknown. The current text reads as if the paper has not yet done the reading that it needs.

8. **Citation year and version disagree.** The data dictionary gives the WHO_GHO citation as "2026, accessed 2026-10-13," and the provenance as "release 2024-04-15." The paper's bibliography key WHO_GHO should carry the year of the release actually used (2024) and an access date. A 2026 publication year for a 2024 release would be wrong to a referee who checks it.

## MINOR CONCERNS

1. Hyndman and Fan (1996) do not describe type 7 as the default in "most statistical software." They recommend type 8 and note that several packages, including R's default and NumPy's default, use type 7. The sentence should say "the default in R and NumPy" or similar.

2. The introduction says that rates per 100,000 are "the usual basis for comparing countries." This is a general claim about practice and should be cited, or softened to describe what this paper does.

3. The limitations section cites nothing for the claim that registration and estimates "should agree closely" where registration is complete. Either cite the WHO estimation documentation (item 1 above) or describe it as a property of the model that the paper does not test.

4. The draft says the African region's concentration in the top group is "consistent with its high regional mean," and that the Eastern Mediterranean contributes "more of the top group than its share of countries would suggest." Both are descriptive and correct against the counts (AFR 5 of 10 top countries against 47 of 195 countries; EMR 3 of 10 against 22 of 195). The paper should give these shares explicitly and drop the word "consistent."

5. Figure 1's source line names WHO GHO RS_198 but not the release date. Add the release (2024-04-15) so the figure is traceable to the same version as the text.

6. The reference list uses the apalike style with a natbib \bibliography. Confirm that every key cited (WHO_GHO, NaturalEarth, little2019statistical, hyndman1996sample) resolves in `literature.bib`. The literature-review file says the library does not yet contain the WHO sources, so the other keys are not verified here.

7. The abstract says "the national median is 12.3 deaths per 100,000 population." It should say that the median is across countries and unweighted, to match item 3 of the major concerns.

8. Trailing reminder for the drafter, from the researcher's instruction at review_draft: the sentence "about four countries exceed 30" should read "four countries exceed 30," and the histogram is already in Section 3.1 with its caption. These are not literature issues, and I have not checked them further.

## POSITIVE ASPECTS

1. The paper is explicit about what it does not claim. It states that the analysis is descriptive, that no causal reading is intended, and that the values are model estimates. This is the right posture for a descriptive study on a modelled indicator, and it avoids the most common failure of papers in this area.

2. The limitations section names the three real threats to the reading: the gap between estimated and registered deaths, the absence of uncertainty bounds, and the unknown age standardisation. A referee would otherwise raise each of these, so naming them is useful.

3. The arithmetic in the top-ten and bottom-ten listings matches the country-to-region counts stated in the text (for example, five African, three Eastern Mediterranean, one American, one South-East Asian among the top ten; seven European among the bottom ten). The rankings are consistent with the data summary.

4. The data documentation (data dictionary and data summary) is unusually complete. It records the raw and clean row counts, the two exclusions, the lack of uncertainty bounds, and the region-mapping checks. The paper can cite that documentation as a reproducibility appendix, and the literature section can point to it when describing sample construction.

OVERALL SCORE: 5.1/10
RECOMMENDATION: Major Revision
