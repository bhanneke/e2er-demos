# Technical Review

**Paper:** Spatial Clustering of GDP per Inhabitant across EU NUTS-2 Regions, 2024 (descriptive spatial analysis, template: spatial analysis)

**Scope and limits of this review.** I had the draft, the econometric specification, the data dictionary, the data summary, the paper plan and the literature review. I did not have `run_estimation.py`, `estimation_results.json`, `summary_statistics.json`, the weights CSVs, the three `\input` tables (`summary.tex`, `moran.tex`, `robust.tex`) or the four figure files. Every check of code against paper is therefore a check of the specification text and the data summary against the draft. Cells in the tables and the figure contents are unverified.

## Summary Assessment

**Concerns (leaning Major Revision).**

The numbers I can trace are consistent. Every statistic that appears both in the draft and in the specification or data summary matches: the sample flow, the means and medians, Moran's I under all four weights, the capital-drop and demeaned results, and the LISA and FDR counts. Some internal arithmetic is also coherent (see Strengths). The pipeline from sources to the 236-region sample is clean, and the draft reports results that contradict the plan's expectations (H1 expected I of 0.5–0.8; the draft finds 0.37) instead of tuning them away.

The problems are in what the statistics can support, and in departures from the plan.

1. The headline conclusion, "spatial autocorrelation disappears within countries", rests on one test (country-demeaned I = 0.020). The permutation null for that test is not valid for demeaned data, and the test is probably biased toward zero. The paper's own capital-drop result shows that capital-versus-hinterland contrasts suppress I, and that is a second reason to doubt the demeaned result.
2. The descriptive local-cluster claims in the abstract and Section 4.3 are made on uncorrected results. The plan said such results would be labelled "suggestive" and not described as clusters.
3. Several checks the draft says it performs, or that the plan and data dictionary promised, are absent from the results: island treatment, flag-based robustness, k = 3, Geary's C, and 9,999 permutations.
4. The pre-specified measurement caveats (Irish profit shifting, workplace-based GDP and commuting, national-only PPS) are missing from the draft, although they affect the headline range and the high-low and low-high outliers.
5. One sentence in the Introduction misreports the Ireland result.

None of these requires new data. They require a handful of extra runs and a more careful reading of the existing ones.

## Data Pipeline

**Sound.**
- The sample flow is documented and arithmetically closed: 276 raw rows, 0 missing, minus 32 non-EU27 gives 244, minus 8 outermost gives 236.
- NUTS 2024 codes match across GDP and boundaries, with 0 unmatched in both directions.
- The CRS is EPSG:3035 throughout, and the weights are built from that projection.
- The 8 outermost regions are named and the exclusion rationale is stated.
- The flag counts are reported: 134 provisional + 33 estimated + 69 unflagged = 236.
- The population total of about 444m is plausible. EU27 had about 449m on 1 January 2024, minus about 5m for the outermost regions.

**Issues.**

1. **Island rule is only partly characterised.**
   - The draft says "13 island regions have no land border", but the 13 listed in the data summary include Ceuta (ES63) and Melilla (ES64). These are exclaves, not islands.
   - Ceuta and Melilla, like the excluded outermost regions, lie far from the continental neighbours the weights assume. Yet they are kept in the main sample on a centroid-nearest link. The exclusion logic for outermost regions ("no meaningful land neighbours") applies equally to them.
   - Cyprus is linked to EL42 (646 km), and Malta, Sicily and Ceuta are likewise weak substitutes for adjacency. The data summary and plan both flag these, but the draft's robustness section reports no island-rule variant. Plan item R3 (queen with zero rows for islands, and n = 223 without them) is missing.
   - Section 1 says "We check whether the results depend on ... the treatment of islands". Nothing in Section 4 supports this beyond the kNN weights, which have no islands by construction. Either run R3 or delete the claim.
   - The draft does not say whether the island links are one-directional (island to mainland) or symmetrised. A one-directional link makes the queen matrix asymmetric, and this should be stated.
2. **Rounding inconsistency in the contiguity construction.** The data dictionary says queen vertices are "rounded to 6 decimals". The data summary and plan say "rounded to metres". In EPSG:3035 these differ by six orders of magnitude, and the former is effectively no rounding. The queen link count (1,039 directed links, mean 4.40) depends on which rule was used. The `spatial_design` check should state the rule once and confirm it.
3. **Edge effects are unmentioned in the draft.** The data dictionary promised to report neighbour counts for EU-border regions. The draft does not discuss that Switzerland, Norway, the UK, the Western Balkans and Türkiye are absent, so border regions have truncated neighbourhoods. The Alpine and Balkan borders are exactly where the HH and LL contrast is largest. One sentence in the limitations is enough.
4. **Provisional and estimated flags.**
   - About 71% of the sample (167 of 236) is provisional or estimated; the plan wrote "about two thirds".
   - The data dictionary committed to a robustness run excluding flagged values, or using 2023. The draft mentions revisability only as a scope condition and runs neither check.
   - Dropping 167 of 236 regions is not workable for Moran's I. Using 2023, or at least a leave-flagged-out sensitivity of the region ranks, is.
5. **Index label.** The Data section says "the index version of the variable (EU27 = 100)". The data summary and plan §2(iv) say the base is the population-weighted mean of the 236-region sample (40,077), not Eurostat's official EU27 value. The draft must say "sample population-weighted mean = 100", and the map caption or table notes must agree. If the index is mapped, this is a mislabelling.
6. **Mixing weighted and unweighted measures.**
   - Gini, CV, percentiles and Moran's I are unweighted. The Theil decomposition and the demeaning use population weights.
   - The draft never says whether the Gini is population-weighted. The spec lists a population-weighted CV but the draft reports only the unweighted 0.37.
   - State the weighting of each statistic explicitly.

## Estimation Implementation

**Specification versus draft.**
- **Moran's I:** the formula in Eq. (1) matches the spec. E[I] = −1/(n−1) and the z-score from the permutation moments match.
- **Permutation inference:** the pseudo-p is (1 + #{|I_perm − E| ≥ |I − E|})/1000 in the spec, with a floor of 0.001 stated in the draft. These match.
- **Local I:** the spec and draft agree on conditional permutation (999) and HH/LL/HL/LH classification at p < 0.05.
- **Multiplicity:** the Benjamini–Hochberg q = 0.05 correction is applied in both.
- **Getis–Ord G*:** row-standardised with the own value in both, z-scores from the analytic expectation.
- **Unmentioned in the draft:** the distance metric and units for the inverse-distance weights (1/d, km, all pairs, no cut-off); centroid definition (area-weighted, EPSG:3035); whether LISA p-values are one-sided or two-sided; the software, version and seed.

**Departures from the plan, none disclosed in the draft.**

| Plan item | Draft |
|---|---|
| 9,999 permutations | 999, so every global p is 0.001 and carries no information beyond z |
| Geary's C | absent |
| kNN with k = 3 | absent |
| Island variants (R3) | absent |
| Trimmed and winsorised variants (R7) | replaced by dropping the top five |
| p < 0.01 LISA counts | absent |
| "Suggestive" label for uncorrected LISA | not applied |
| Other years (R11) | absent |
| Distance correlogram | absent |
| Country table, top/bottom-10 table | not visible (tables not provided) |

The draft should either run these or say they were not run. The "no variant is dropped after seeing results" rule in the plan makes silent omission a pre-registration issue.

**Substantive problems in the estimation design.**

1. **The permutation null for the demeaned test is not valid.**
   - Values are shuffled across all 236 regions. After country-demeaning, the data carry a built-in constraint: each country's population-weighted deviations sum to zero.
   - Single-region countries (EE, LV, LU, CY, MT and others) have deviation exactly 0. Two- and three-region countries have deviations of opposite sign.
   - Within-country neighbours are 75% of all links. These links therefore connect values that are mechanically negatively correlated. This pushes the observed I below what a global shuffle implies, and below the true within-country spatial dependence.
   - The permutation SD (about 0.048, implied by I = 0.020 and z = 0.5) is calibrated for unconstrained data.
   - A valid null shuffles demeaned values within countries (or uses a country-block permutation). Only then is I = 0.020 interpretable.
   - Population-weighted demeaning feeding an unweighted I adds a further mismatch.
2. **Low power, treated as evidence of absence.**
   - "Statistically indistinguishable from zero" (abstract, Section 1) becomes "Within countries, high-income regions are thus not systematically adjacent to other high-income regions" (Section 4.4) and "vanishes" (Section 5). The test has an implied standard error of about 0.05 and is run on about 8.7 regions per country.
   - Large countries with well-known internal gradients are pooled with tiny ones: Italy (north–south), Germany (east–west), Spain, Poland. A within-country I near zero is hard to reconcile with those gradients.
   - The capital result points to the likely reason. Dropping capitals lifts I from 0.37 to 0.62, so capital–hinterland contrasts strongly reduce measured autocorrelation. The same contrasts will depress the demeaned I, because capitals are exactly where within-country deviations are large and of opposite sign to their neighbours.
   - The demeaned I should be re-run with capitals (and Hamburg-type city regions) excluded, and reported country by country for the larger countries, with intervals.
3. **"Almost entirely between-country" is not what the evidence shows.**
   - The Theil decomposition attributes only 36% of inequality to between-country differences, so 64% is within-country. The abstract says the clustering is "almost entirely a between-country phenomenon". The two statements concern different objects (dispersion versus spatial arrangement), and the draft never reconciles them.
   - The numbers are in fact coherent: I ≈ 0.36 × (about 0.75 of links within the same country) plus a cross-border contribution is roughly 0.37. That is, I mostly mirrors the between-country variance share times the within-country link share. This is worth saying explicitly. It also means the "national" finding is close to mechanical: any country-level mean difference with 75% intra-country links produces positive I.
   - The more informative decomposition is I of the country-mean vector and I of the residual, together with the share of variance explained by country (the R² the plan promised), not a single demeaned I.
4. **The significance test against complete spatial randomness is nearly uninformative.** With national levels differing by a factor of three, rejecting random placement of values over regions at p = 0.001 is expected. The z-score tells us little beyond the magnitude of I. A country-constrained null (shuffle within countries) is the test that addresses the paper's actual question.
5. **The capital-drop result is confounded.**
   - The 27 dropped regions include EE00, LV00, LU00, CY00 and MT00 (whole countries), and several are broad regions that merely contain the capital (NL32 Noord-Holland, ITI4 Lazio, SI04, IE06, BG41).
   - Dropping them also removes the island-linked units Cyprus and Malta, and it leaves three regions with zero neighbours.
   - The rise to 0.623 therefore mixes a capital effect, an island-link effect, a single-region-country effect and an isolated-unit effect. The draft acknowledges the isolates and single-region countries but still presents the number as capital regions "raising" I.
   - A placebo is needed: drop 27 randomly chosen regions, or 27 size-matched non-capitals, repeatedly, and place 0.623 in that distribution. Dropping capitals while keeping CY, MT, EE and LV would also separate the components.
6. **LISA on the skewed level variable.**
   - Regional income is right-skewed. In a conditional permutation test the null distribution of the neighbour lag has a long upper tail and a short lower tail.
   - A high-high cluster must therefore be more extreme to be significant than a low-low cluster, which makes the asymmetry (19 HH versus 38 LL uncorrected; 1 versus 20 after FDR) partly mechanical. The draft says the high-income clusters "rest on weaker evidence", an interpretation the data cannot separate from skewness.
   - LISA on ln GDP (for which global I rises to 0.482) or on ranks is the obvious check. It is cheap and not reported.
7. **Ireland.** The three Irish regions have no land neighbour outside Ireland (Northern Ireland is not in the sample). Each is the other two's only neighbour, so the HH label for Ireland describes a closed three-region island whose values are inflated by multinational accounting. Dropping Ireland lowers I from 0.370 to 0.342, which confirms a non-trivial contribution.
8. **Getis–Ord G*.**
   - z-scores come from the analytic expectation, which assumes normal-theory inference. That is poor for a skewed variable with irregular neighbourhoods, and it is inconsistent with the permutation inference used everywhere else.
   - The counts (24 hot and 30 cold at |z| > 1.96) are not cross-tabulated against LISA. The statement that G* "points the same way" is therefore unquantified. The plan said disagreement of more than a handful of regions should be discussed.
9. **FDR with 999 permutations.** Pseudo-p values come in steps of 0.001, so many strongly clustered regions sit at the floor and tie. The BH threshold at rank k is 0.05·k/236. The set of 22 survivors depends on how many regions sit at p ≤ 0.004, and so on permutation resolution. Re-run LISA with 9,999 permutations and check whether the 22 changes. State which regions form the single HH and the single HL survivor.

## Results Reporting

**Significance and statistics.**
- Reported stars or z-scores are internally consistent. The demeaned test has z = 0.5 and p = 0.6 (the normal tail at 0.5 is about 0.62), and the implied permutation SD (about 0.048) matches that of the queen test (7.8 → (0.374)/7.8 ≈ 0.048). The inverse-distance z of 12.5 with a small I is plausible for dense weights.
- Quadrant counts sum to 236 (74 + 105 + 31 + 26). LISA counts sum to 62 (19 + 38 + 2 + 3). FDR counts sum to 22 (20 + 1 + 1). The expected false positives (0.05 × 236 = 11.8) are right.
- The cluster-membership listing sums correctly: 5 + 5 + 3 + 3 + 2 + 1 = 19 HH. The low-low country counts (10 + 7 + 5 + 5 + 5 = 32 of 38) leave 6 for five further countries.

**Interpretation problems.**

1. **Introduction misreports the Ireland sensitivity.** Section 1 says excluding Luxembourg, the Irish regions "or the five richest regions leaves it unchanged or stronger". Dropping the Irish regions gives 0.342, which is lower than 0.370 (a fall of 7.6%). The Results section reports this correctly ("leaves it at 0.342"). Change the Introduction to say that Luxembourg and the top five raise I, and Ireland lowers it slightly.
2. **Abstract and Section 4.3 describe uncorrected clusters as findings.**
   - "Local indicators locate low-income clusters in Poland, Greece, Bulgaria, Romania and Hungary and high-income clusters in Germany, the Netherlands, Ireland and northern Italy" is an uncorrected statement, and the FDR sentence follows afterwards. Only one HH region survives FDR. The high-income clusters named in the abstract's first clause essentially do not survive.
   - The plan said regions significant only before correction are "suggestive" and not to be described as clusters.
   - The draft never reports the country composition of the 22 survivors. Whether Poland (10) and Hungary (5) remain among the FDR clusters is unknown. A table of FDR survivors by country, and a LISA map using the FDR set in the main text, would settle it.
3. **"National blocks" is asserted, not shown.** The Discussion calls the high-income cores in Germany, the Netherlands and Ireland "largely national blocks". The uncorrected HH set combines German, Dutch, Belgian, Austrian and Italian regions, so that cluster spans several borders. The 24.8% cross-border share of links is evidence about the weights matrix, not about clusters. Count, for each local cluster, the number of countries it contains.
4. **Wording of the dropping-extremes inference.** "Inequality is partly a matter of extreme regions: dropping Luxembourg lowers the Gini coefficient only from 0.197 to 0.194" reads as the opposite of the number it reports: the change is negligible. Dropping the 27 capitals (0.174) is not dropping "extreme" regions either.
5. **The cause given for the low inverse-distance I.** "Smaller because distant regions receive non-negligible weight" is plausible but untested. Say "presumably" or run a banded distance weights version.
6. **Right skew and "only 86 of 236".** 86 regions exceed the population-weighted mean (40,077). Per the quadrant counts, 105 exceed the unweighted mean. The 86 figure reflects both skew and the fact that large regions are richer. Attributing it to skew alone, as the text does, is incomplete.
7. **Positioning.** "which is rarely reported together" is an unsupported novelty claim. Le Gallo and Ertur (2003) and the ESDA literature cited in the literature review report Moran's I, LISA and sensitivity to weights on EU regional GDP. They are absent from the draft, partly because they were not registered as citable. Soften the claim, or register and cite them.

**Robustness assessment.**
- The weights, outlier and outermost-region checks address real threats and are well chosen.
- The ln GDP check addresses skew for the global test only.
- The checks missing for the main conclusion are the ones above: a valid within-country null, an island variant, a flag or alternative-year check, and LISA on a non-skewed variable.
- The within-country result is the claim the paper stakes most on, and it has the thinnest support.

**Measurement caveats absent from the text.**
- The plan (§2, §9) and the specification require these caveats, and the draft contains none of them. The "Caveats" paragraph covers provisional values, a single year and the modifiable areal unit problem only.
  - **Irish GDP and profit shifting.** The maximum (IE06, 107,200) and the headline "factor of more than six" depend on it. The ratio excluding Ireland (LU00 is the next highest) would be informative.
  - **Workplace-based GDP and commuting.** This inflates GDP per head in Luxembourg, Hamburg, Prague and Brussels and depresses neighbours. It mechanically produces the LH outliers (BE33, DK02, DEB2) and affects the capital results.
  - **PPS adjusts national, not regional, price levels.** This matters for within-country comparisons, which are the paper's key contrast.
- The listing of BG41 and EL30 as "spatial outliers" and the "capital regions as income peaks" reading both need the commuting and boundary-size caveat.

## Red Flags

- **P-value patterns.** None suggestive of p-hacking. The few p-values reported are either at the floor (0.001) or far from thresholds (0.6). The floor itself is an artefact of 999 permutations, not a signal.
- **Specification searching.** None apparent. The reverse risk is that unfavourable planned checks were dropped without being reported (see the plan-departure table).
- **Magic numbers.** The 5% LISA level, |z| > 1.96, q = 0.05, k = 5 and k = 8, 999 permutations, and the 27-capital list are all stated. The list of capitals is not defined in the draft: "capital regions" includes broad regions merely containing the capital (NL32, ITI4, SI04, IE06, BG41).
- **Unverifiable share.** Roughly 30–40% of the quantitative claims in the draft cannot be traced to the artefacts supplied to me (see the check log). That is partly my access limit (JSON and tables not supplied), but the draft's `% src:` comments cite `estimation_results.json` keys that the reviewer cannot open.
- **Suspiciously clean results.** None. The results run against the plan's expectations in several places, including a weaker I than predicted and capital regions raising rather than lowering I when removed. That counts in favour of the analysis.

## Strengths

- A pre-written spatial design, a documented sample flow, and `% src:` comments linking text to result keys.
- Appropriate and transparent statistic choices for a descriptive paper: Moran's I with permutation inference, LISA with an explicit multiple-testing correction, G* as a secondary cross-check, and an explicit statement that no causal claim is made.
- Sensible sensitivity design (weights family, outermost regions, extreme regions, ln GDP, country level). The finding that dropping capitals raises I is reported straight, against the plan's H3.
- The numbers I could check against the spec and data summary all agree (see log), and internal arithmetic is coherent: quadrant, LISA, FDR and sample counts sum; the implied permutation SDs are consistent across tests; I ≈ 0.37 is close to the between-country share (0.36) times the within-country link share (0.75), plus a cross-border contribution.
- The draft is candid about provisional data, a single cross-section, the modifiable areal unit problem and the exploratory status of the cluster maps. The researcher's corrections (title, 3 alternative weights, FDR in the abstract, capital-region caveats, the demeaned-I wording, Eurostat disclaimer) have been applied; the demeaned-I sentence now correctly says it "does not test for gradients across borders".

## Recommendations

**Data stage**
1. Fix the vertex-rounding rule in the data dictionary versus data summary, and state the rule actually used.
2. Reword "13 island regions". Ceuta and Melilla are exclaves. Justify keeping them while excluding the outermost regions, or move them to the robustness set.
3. State the direction of the island links (symmetric or not) and report the edge-effect neighbour counts.
4. Relabel the index base as "sample population-weighted mean = 100", or load the official EU27 value.

**Estimation stage**
5. Re-run with 9,999 permutations. Report z with p, and recheck the 22 FDR survivors.
6. Replace the global-shuffle test for demeaned income with a within-country permutation. Report I for country means and for residuals, the R² of country on ln GDP, and the demeaned I excluding capitals and for the large countries separately, with intervals.
7. Add a placebo for the capital drop (random or size-matched 27 regions), and a variant that drops capitals but keeps CY, MT, EE, LV.
8. Run LISA on ln GDP or ranks, and report whether the LL/HH asymmetry survives.
9. Add the planned island variants (R3), k = 3, Geary's C, a flag/2023 sensitivity, and a cross-tabulation of G* against LISA. Use permutation-based inference for G*.
10. Name the HH and HL FDR survivors and give the FDR set by country.

**Draft stage**
11. Correct the Introduction sentence on Luxembourg, Ireland and the top five (Ireland lowers I to 0.342).
12. In the abstract and Section 4.3, put the FDR result first or label the uncorrected clusters "suggestive", as the plan requires. Soften "high-income clusters in Germany, the Netherlands, Ireland and northern Italy".
13. Replace "almost entirely a between-country phenomenon" with a statement tied to the specific decomposition (for example, "country-demeaned autocorrelation is close to zero under a global shuffle; this test has limited power").
14. Reconcile the 36% Theil between-country share with the "national" finding, and state the weighting of each inequality measure.
15. Add the omitted measurement caveats: Irish profit shifting, commuting, national-only PPS, edge effects. Give the range excluding Ireland.
16. Delete or support "the treatment of islands" in the Introduction, and "rarely reported together". Define "capital region" for the 27-region list.
17. State software, versions, seed, the inverse-distance form and the centroid definition.
18. Supply the three tables and the figure files for the next review so the table cells can be checked.

## Consistency Check Log

Counts are approximate; the tables and figures were not supplied.

- **Total claims checked:** about 70
- **Consistent:** about 40 (57%)
- **Inconsistent:** 1 (1%); Introduction on Irish exclusion, minor-to-major wording
- **Unverifiable:** about 29 (42%), see below
- **Overall verdict:** PASS on numerical consistency (no discrepancy in a reported value); FAIL on one interpretive misstatement (item 11)

| Claim in draft | Source checked | Result |
|---|---|---|
| N = 236, 244, 8 outermost, 276, 32 non-EU27 | spec, data summary | consistent |
| Flags 134 / 33 / 69 (sum 236) | data summary | consistent |
| Mean 37,976; median 35,050; pop-weighted 40,077; 86 above | data summary | consistent |
| Min 16,700 (BG31); max 107,200 (IE06); ratio 6.4 | data summary | consistent |
| p90/p10 = 2.4 | 53,550 / 22,750 = 2.35 | consistent (rounding) |
| CV 0.37 | 14,246 / 37,976 = 0.375 | consistent |
| Population 444m | 449m minus about 5m outermost | plausible |
| Queen I = 0.370, E = −0.004, z = 7.8, p = 0.001 | spec | consistent |
| kNN-5 0.266; kNN-8 0.265; inverse distance 0.089 | spec | consistent |
| Capital drop 0.623; demeaned 0.020, p = 0.60 | spec | consistent |
| LISA 19 / 38 / 2 / 3 = 62; false positives about 12 | spec; 236 × 0.05 | consistent |
| FDR 1 / 20 / 1 = 22 | spec | consistent |
| Quadrants 74 / 105 / 31 / 26 = 236; about three quarters share sign | arithmetic (75.8%) | consistent |
| "Between 0.09 and 0.27" under kNN and inverse distance | spec | consistent |
| Demeaned z = 0.5 and p = 0.6 | normal tail 0.62 | consistent |
| Excluding LU, Ireland, top 5 leaves I "unchanged or stronger" | 0.411 / 0.342 / 0.429 vs 0.370 | **inconsistent for Ireland** |
| ln GDP I = 0.482; kNN-5 on 244 = 0.276; drop LU 0.411; drop IE 0.342; top-5 0.429 | not in spec | unverifiable |
| Gini 0.20 (0.197 → 0.194 → 0.174); Theil between = 36% | not in spec | unverifiable |
| 24.8% of links cross borders; 24 hot and 30 cold spots | not in spec | unverifiable |
| Region lists (top 5, bottom 5, LISA by country, outliers) | not in spec | unverifiable |
| All table cells; all figures | not supplied | unverifiable |

OVERALL SCORE: 5.5/10
RECOMMENDATION: Major Revision
