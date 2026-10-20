# Writing Review: Spatial Clustering of GDP per Inhabitant across EU NUTS-2 Regions, 2024

Scope: I reviewed the LaTeX draft against the supplied specification, plan, data summary and literature notes. I could not see the contents of `tables/summary.tex`, `tables/moran.tex` and `tables/robust.tex`, or the figures. Comments on them are limited to how the text refers to them.

## Overall assessment

The paper is short and well organised, and it matches its own roadmap. It makes its descriptive scope clear and avoids causal language. The numbers I could check against the supplied documents are consistent:

- Quadrant counts: 74 + 105 + 31 + 26 = 236.
- Local cluster counts: 19 + 38 + 2 + 3 = 62.
- Flag counts: 134 + 33 + 69 = 236.
- Expected Moran's I: −1/235 = −0.004.
- Country counts among the low-low clusters sum to 38.

The researcher's seven corrections (title, abstract, 90/10 wording, deleted untested explanation, capital-region caveat, demeaned-I interpretation, dataset names and Eurostat disclaimer) are implemented.

The remaining problems are mostly claim–evidence alignment and omissions, not prose style:

1. The text never states the measurement caveats that the plan required (commuting, Irish profit shifting).
2. The introduction claims an island-treatment check that the Results do not report.
3. "Almost entirely between-country" sits uneasily next to the 36 percent Theil share.
4. The abstract leads with uncorrected local clusters.
5. The methods leave several statistics undefined.
6. There is essentially no literature positioning.

The sentence-level writing is generally clean and active. Details follow, ordered by importance.

## A. Evidence–claim alignment (highest priority)

**A1. Measurement caveats are missing from the text.**
- The plan (§2, §9) and the specification require three caveats:
  - GDP is workplace-based, so commuting inflates core regions and depresses their hinterland.
  - Irish values reflect multinational accounting.
  - PPS adjusts for national, not regional, price levels.
- None of these appears in the draft. The Discussion lists only provisional data, a single year, MAUP and the outermost regions.
- This matters for the claims made. The abstract and Section 4.3 present "the three Irish regions" as a high-income cluster. The paper's richest region (IE06) is probably the most distorted value in the sample. The low-high outliers (BE33, DK02, DEB2) and the high-low capitals are exactly where commuting effects bite.
- Fix: add two or three sentences in Section 2 and a limitation paragraph in Section 5. Say that Irish values are retained and that dropping them lowers I from 0.370 to 0.342.

**A2. "Income" is used for GDP per inhabitant.**
- The text switches among "regional income", "high-income clusters", "GDP per inhabitant" and "GDP per capita" (the last in the Introduction's RQ sentence).
- GDP per inhabitant is production per resident, not household income. Given the commuting and profit-shifting issues, the distinction matters.
- Fix: define the variable once and use "GDP per inhabitant" or "regional GDP" consistently. Use "high-GDP" and "low-GDP" regions, or define "income" as shorthand explicitly.

**A3. The Introduction claims an island check that is not reported.**
- It says: "We check whether the results depend on … the treatment of islands." The Contribution paragraph lists "weights, outermost regions, and extreme regions".
- The Results contain no variant that changes the 13 nearest-region links (the plan's R3). They test only the inclusion of the outermost regions.
- The data summary itself calls the Cyprus (646 km), Malta, Sicily and Ceuta links weak substitutes for adjacency. Either report the check or delete the claim and state it as a limitation.
- Also, "13 island regions" is inaccurate. Ceuta (ES63) and Melilla (ES64) are exclaves, not islands. Write "13 regions without a shared border vertex".

**A4. "Almost entirely a between-country phenomenon" versus 36 percent.**
- The abstract says clustering is "almost entirely" between-country. Section 4.1 says only 36 percent of (population-weighted) Theil inequality lies between countries.
- Both can hold, but the paper never reconciles them. A reader will see a conflict.
- Two further points need stating:
  - Because 75 percent of queen links are within a country, a pure national step function would produce a large positive I mechanically. The demeaning result is therefore close to expected under a national-blocks pattern. It is not a surprising empirical discovery. Say this explicitly.
  - The paper does not say how much I the between-country component accounts for. The jump from 0.37 to 0.02 also reflects the removal of all cross-border contrast. The Discussion now says this correctly, but the abstract and the Introduction (contribution 2: "absorbed by country membership") do not.
- Also note that demeaning is noisy for countries with one to three regions. For the five single-region countries the demeaned value is exactly zero. State how these are handled and whether they bias I towards zero.
- Fix: soften the abstract to "once each region's value is expressed relative to its national mean, spatial autocorrelation is no longer detectable". Add a sentence on the mechanical link between the within-country share of links and the national component.

**A5. The link-share sentence is a non sequitur.**
- Section 4.4 says "This is consistent with the fact that only about one quarter of queen links … cross a national border, so most neighbours belong to the same country and the national level absorbs most of the spatial signal."
- The first half of the sentence is a fact about adjacency. The second half is the conclusion. The link-share does not show that the national level absorbs the signal; the demeaned I does.
- Fix: state the demeaned result first, then give the link-share as the reason why national blocks generate positive I.

**A6. The Introduction overstates the robustness to dropping regions.**
- It says excluding Luxembourg, the Irish regions or the five richest regions "leaves it unchanged or stronger".
- Section 4.4 reports 0.342 for Ireland against a baseline of 0.370. That is lower, by about 8 percent.
- Fix: write "changes it little or raises it (0.34–0.43)". In Section 4.4, "dropping the three Irish regions leaves it at 0.342" should read "lowers it to 0.342".

**A7. Local clusters: the abstract leads with the uncorrected result.**
- It names Poland, Greece, Bulgaria, Romania and Hungary as low-income clusters and Germany, the Netherlands, Ireland and northern Italy as high-income clusters. Only then does it mention that after FDR correction one high-high region survives.
- The reader is told about "high-income clusters in four countries", then learns that a single region survives. The paper never says which country that region is in, or which countries host the 20 surviving low-low regions.
- Fix: report the FDR-surviving set by country, in the text or a small table. Lead the abstract and the Introduction's fourth finding with it. Describe the remaining uncorrected high-high regions as suggestive, as the plan intended ("not described as clusters").

**A8. Untested explanations remain.**
- "Which is smaller because distant regions receive non-negligible weight" (inverse-distance I = 0.089) is plausible but untested. Write "presumably smaller because…" or drop the reason.
- "Because large regions are on average richer than small ones" (weighted mean 40,077 versus 37,976) is a statement of covariance. It is arithmetically fine but should be phrased as "large regions are on average richer".
- "Only 86 of 236 regions exceed the population-weighted mean, which reflects the right skew" confounds two things. Weighting raises the mean, and skew puts the mean above the median. Report the share above the unweighted mean (or the median) to isolate the skew, or drop the causal clause.
- "The uncorrected high-high clusters thus rest on weaker evidence than the low-income ones" is fine as a description. It sits next to no explanation, which is correct.
- "Inequality is partly a matter of extreme regions" is followed by evidence that dropping Luxembourg barely matters (0.197 to 0.194). Only the capital drop moves the Gini (0.174). Rewrite: "Dropping Luxembourg barely changes dispersion (Gini 0.197 to 0.194); dropping all 27 capital regions lowers it to 0.174."

**A9. Getis–Ord claim.**
- "Points the same way, with 24 hot spots and 30 cold spots" gives no overlap with the LISA results. Local Moran gives 19 high-high and 38 low-low.
- The specification says G* z-scores are analytic, while everything else uses permutation inference. The Methods do not say this. Give the overlap count or drop the sentence, and state the inference basis.

**A10. The contribution claim is unsupported.**
- "Rarely reported together" has no citation or evidence.
- The Introduction cites only Pourpakdelfekr (2026) as prior work, and says it "does not quantify the spatial structure of regional income itself". That reads as a characterisation of a neighbouring paper; verify it.
- The citation of `Eurostat_Database` for the claim that NUTS-2 is the reference unit for cohesion policy eligibility is a data citation, not a source for that claim. Cite the regulation or Commission documentation, or drop the citation.
- "Even after decades of convergence in national averages" is asserted without a reference.

## B. Literature positioning

- The draft has no literature discussion. The literature notes identify Le Gallo and Ertur (2003) as the closest antecedent (ESDA of EU regional GDP per capita with Moran scatterplots and LISA).
- The notes also list Bosker (2009), Iammarino et al. (2019) and Petrakos et al. (2005) on national convergence alongside within-country divergence. These bear directly on the paper's main finding.
- These keys are not in `literature.bib`, so the drafter correctly did not cite them. Register them (the notes say to run `e2er-lit search`) and write a three- to five-sentence positioning paragraph. It should say what is new relative to the 1980–1995 ESDA work (the current NUTS map, 2024, PPS, a national-component decomposition).
- Without it, "two contributions" reads as a description of the analysis, not a contribution. Keep the claim modest, as the plan advises.

## C. Methods exposition

- Several quantities are used but not defined in Section 3:
  - The Gini coefficient (unweighted?), the coefficient of variation, and the Theil index with its between/within decomposition appear only in the Results.
  - The local Moran statistic is described in words but its formula is not given.
  - The G* statistic has no formula or weights description.
  - The k-nearest-neighbour definition (distance on area-weighted centroids) and the inverse-distance definition (1/d in km, all pairs, no truncation) appear only in the specification. Add them to Section 3.
- The dispersion measures mix unweighted statistics (CV, Gini, p90/p10) with a population-weighted Theil decomposition. Say so, and say which weighting the 0.20 Gini uses.
- The p-value floor of 0.001 is repeated four times ("the smallest attainable"). Say it once in Section 3 and write "p = 0.001 (floor)" in tables. A z of 12.5 beside p = 0.001 looks inconsistent unless the reader remembers the floor. Consider 9,999 permutations, which the plan specified, or explain the departure.
- Rename Section 3 "Empirical Strategy" to "Methods". "Strategy" suggests identification, which the template explicitly excludes.
- Replace passive constructions with the active voice, for example "values are shuffled across regions 999 times" becomes "we shuffle values across regions 999 times". Passive voice is fine for "weights are row-standardised".
- Add a one-sentence statement of the Moran null, since permutation assumes exchangeability of a skewed variable. The ln(GDP) check partly addresses this and should be named in Section 3 (it is mentioned only in Section 2 and the Results).

## D. Structure and flow

- **Section 4.4 is the weakest passage.**
  - The capital-region sentences are in the wrong order. The caveat about single-region countries and isolated regions comes before the result it qualifies.
  - "These two variants" has no clear referent, because the sentence mentions the capital drop and the top-five drop in different clauses.
  - The reading ("income peaks surrounded by poorer neighbours") then interrupts the flow.
  - A stray one-sentence paragraph-ending, "In every case the pseudo p-value is 0.001", contradicts the next paragraph, where the demeaned p-value is 0.6.
  - Suggested order: (i) the drop variants and their I values; (ii) the isolated-region caveat (which says the 27 capital regions include EE00, LV00, LU00, CY00 and MT00, so three regions lose all neighbours, one in the top-five variant); (iii) all of them have p = 0.001; (iv) the labelled reading, which the statistics do not test.
- **Section 4.2 has a long closing paragraph** that packs the log variant, three weights, an explanation and a conclusion into one sentence-chain. Split it, and put the weights comparison in a sentence that points to Table 2 instead of repeating every value.
- **The Discussion repeats the Results nearly verbatim** (I = 0.37, 0.020, p = 0.6, national blocks). Each section should add something. Trim the first paragraph and keep the interpretation.
- **The policy sentence is vague.** "National and regional disparities should be read jointly and … regional rankings cannot be separated from country membership" is a claim that goes beyond the evidence and is not a recommendation anyone can act on. Say what a reader should do (for example, compare regions within a country and report national and within-country components separately) or delete it.
- **"Finding is an association between co-location and income"** is imprecise. Moran's I measures the similarity of neighbouring values, not an association between location and income. Rewrite: "The finding describes similarity between neighbouring regions; we make no claim about why it arises."
- **The Introduction's first sentence** ("Regional income differences are a defining feature…") is throat-clearing. Start with the 6.4 ratio. "Yet the answer determines how spatial a description of EU disparities must be" is also vague. Say what the answer would change for the reader.
- **Section numbers** in the roadmap are hard-coded. Use `\ref`.
- **The last paragraph** ("Two questions follow directly…") is acceptable because the suggestions are specific. Check that 2015 NUTS vintage differences (flagged in the data dictionary) can be handled before promising the panel "already available".

## E. Local presentation issues

- Region codes (BG31, EL41, IE06, DEB2, BE33, DK02) are used without names. A reader cannot interpret DK02 or DEB2. Give names at first mention or add a table of the top and bottom regions (the plan promised one).
- The index version (EU27 = 100) is said to be used "for mapping", but the Figure 2 caption shows PPS quintiles. Either use it or remove the sentence. If kept, label it "sample mean = 100", as the plan says, because it is not Eurostat's official index.
- Consistency:
  - "kNN", "k-nearest-neighbour", "nearest-neighbour" and "five-nearest-neighbour" all appear. Pick one.
  - "paper", "study" and "analysis" vary for the same referent.
  - "I = 0.37" appears next to "0.370" and "0.020". Use two or three decimals consistently.
  - "Percent" is consistent; spelling is British throughout (neighbouring, artefact), which is fine if kept.
- The `% src:` comments should be stripped before submission. The author line is empty; fill it before circulation.
- There is no data or code availability statement, although the contribution is described as "replicable". Add one line.
- Hedging is mostly well calibrated. Descriptive numbers are stated plainly, and the exploratory status of local clusters is flagged. Two places over-claim ("confirms what maps suggest" is fine; "shows … vanishes" should be "is no longer detectable").

## F. Priority list for revision

1. Add the commuting, Irish and regional-price caveats, and use "GDP per inhabitant" consistently (A1, A2).
2. Report the island-rule sensitivity or remove the claim; fix "island regions" (A3).
3. Reconcile "almost entirely between-country" with the 36 percent Theil share, and add the mechanical-link point (A4, A5).
4. Lead the abstract and the Introduction with the FDR-surviving clusters, listed by country (A7).
5. Correct the Ireland and "unchanged or stronger" wording (A6) and remove the remaining untested explanations (A8).
6. Define Gini, Theil, local I, G*, kNN and inverse distance in Section 3, and state the weighting (C).
7. Restructure Section 4.4 and trim the repetition in the Discussion (D).
8. Add a short literature positioning paragraph using registered references, and fix the cohesion-policy citation (B, A10).

OVERALL SCORE: 6.5/10
RECOMMENDATION: Minor Revision
