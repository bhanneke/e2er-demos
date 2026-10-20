# Plausibility Review: Spatial Clustering of GDP per Inhabitant across EU NUTS-2 Regions, 2024

Scope: I checked whether the numbers and patterns make sense for regional GDP in PPS, for Moran's I and LISA on a 236-region map, and for Eurostat's provisional regional accounts. Traceability to the results files is handled elsewhere. Statements marked "(own knowledge)" come from me, not from the paper or its supporting documents. They need checking against the data.

## Overall impression

The internal arithmetic is coherent. Several headline numbers are consistent with each other:

- The Moran's I standard errors are consistent with the reported z scores. Queen: z of about 7.8 gives a permutation SD of about 0.047. This is the right order of magnitude for n = 236 with 4.4 neighbours. The demeaned case I = 0.020, z = 0.5, p = 0.6 is also consistent.
- The quadrant counts sum to 236 and the "three quarters" claim is correct (179 of 236 = 75.8%).
- The LISA counts add up (19 + 38 + 2 + 3 = 62; FDR 20 + 1 + 1 = 22). The expected false positives are 236 × 0.05 ≈ 12.
- The flag counts add up (134 + 33 + 69 = 236).
- CV = 14,246 / 37,976 = 0.375. The p90/p10 ratio is 53,550 / 22,750 = 2.35. The max/min ratio is 6.4.
- A Gini of 0.20 is what a CV of 0.37 implies for a roughly lognormal shape.
- 86 regions above the population-weighted mean of 40,077 is consistent with the reported percentiles. That mean sits at about the 64th percentile.
- A population of 444 million equals the EU27 total minus the roughly 5 million people in the outermost regions (own knowledge).

The problems are in four places. The first is the missing measurement caveats. The second is a few labels and classifications that look wrong. The third is the headline between-country result, which is counter-intuitive and not yet stress-tested. The fourth is some interpretive sentences that say more than the statistics support.

## A. Implausible or unexplained numbers and patterns

### A1. EL30 (Attiki) classified as high-low (Local clusters, p. on LISA outliers)
A high-low region must have income above the unweighted sample mean of 37,976 PPS. Attiki is normally well below the EU average (own knowledge: about 75–85% of the EU27 level, which is roughly 30–34k PPS here). It should fall in the low-low or low-high quadrant. An HL label would need a 2024 value above about 38k.
- Check: print the value, quadrant, spatial lag and p-value for EL30 and BG41 from the LISA table. Confirm that EL30 is above the mean. If it is not, there is a quadrant-assignment bug (for example the mean used in the lag or sign, or a population-weighted centring). Every quadrant count would then need re-checking.
- Also state which of the two HL outliers (BG41, EL30) is the one that survives FDR.

### A2. The within-country demeaned Moran's I of 0.020 is surprisingly low (abstract, Section 4.4, Discussion)
The paper's central claim is that clustering is "almost entirely" between-country. But 75% of queen links are within-country. Several large countries have well-documented internal gradients (own knowledge): Italy (north vs Mezzogiorno), Germany (east vs west and south), Spain (north-east vs south-west), France, and Poland (east vs Warsaw and west). Demeaning by country should leave a clearly positive I in those countries. An I near zero for the pooled data is possible only if peaks offset the gradients. It also fits the artefacts below.
- Nine or so single-region countries (EE, LV, LT, LU, CY, MT and others) become exactly zero after demeaning.
- Capital and metropolitan peaks (Prague, Bratislava, Bucharest, Hamburg, Madrid) dominate the within-country deviations and enter with negative local contributions.
- Demeaning by the population-weighted mean does not give the deviations an unweighted mean of zero.
- Checks that would settle it: (i) country-by-country Moran's I of within-country deviations for DE, IT, ES, FR and PL, using links within the country only; (ii) the demeaned I with capital and peak regions excluded; (iii) the demeaned I on ln GDP, which the plan specified and the paper reports only for the level; (iv) a stratified permutation (shuffle within countries); (v) the within-country share of the weighted variance.
- The sentence "This is consistent with the fact that only about one quarter of queen links cross a border" does not support the finding. A high share of within-country links means demeaning leaves most links intact. A near-zero I within countries is then the surprising result, not an expected one. The sentence reads as an explanation but explains nothing.

### A3. "Almost entirely between-country" versus a Theil between-country share of 36%
The paper reports that 36% of inequality is between countries and 64% is within. It also calls the clustering "almost entirely" between-country. These measure different things, but a reader will read them as contradictory. The reconciliation is presumably that within-country inequality is mostly capital-versus-hinterland, which is not spatially clustered. That is plausible, but the paper should say so and show it. The Theil figure is population-weighted and the Gini is unweighted, which is another source of confusion in the same paragraph.
- Check: report the Theil between-share on ln GDP. Also report the between-country share of variance for the unweighted variable, which is the one Moran's I is computed on.

### A4. "Poorest region" and the 6.4 ratio exclude the outermost regions (abstract, introduction)
The abstract and introduction speak of the poorest and richest region in the EU ("GDP per inhabitant in PPS in 2024 ranges from 16,700 in BG31 …"). The sample excludes the eight outermost regions. Mayotte (FRY5) and probably Guyane are well below BG31 (own knowledge: Mayotte is near the bottom of the EU ranking at roughly a third of the EU average).
- Check: report the min and max in `spatial_units_all244.csv`. State the range as "among the 236 continental and island regions", or give both ranges.

### A5. "Unchanged or stronger" is not true for the Irish exclusion (introduction, third finding)
Dropping the three Irish regions gives I = 0.342 against 0.370, which is lower. The Results section says "leaves it at 0.342", but the introduction says all three exclusions leave I "unchanged or stronger". The difference of 0.028 is within the permutation SD of about 0.047, so the drop is probably noise. The sentence should say "lowers it slightly".

### A6. Ireland is a disconnected component, and its "high-high cluster" is partly an artefact
Ireland has no land border with any other sample region, and the island rule lists 13 regions that do not include IE04–IE06. They are linked only to each other. The same applies to Zealand (DK01/DK02) and perhaps others. Three mutually adjacent regions, each with two neighbours, produce an HH cluster that rests on very little information.
- Ireland's headline values are inflated by multinational profit shifting. The analysis spec states this, but the paper does not mention it anywhere. The abstract and introduction nonetheless present Ireland as a leading "high-income cluster" and IE06 as the richest region.
- Check: add a robustness column "Ireland linked to Great Britain/continent nearest region" or use GNI-style indicators. At minimum, add a sentence on the profit-shifting caveat.

### A7. Absence of the expected capital outliers in the HL class
Only BG41 and EL30 are flagged as HL. Prague, Bucharest, Warsaw, Budapest, Bratislava, Luxembourg and similar regions are not, although the literature review set these up as the expected outliers. The likely cause is low power: peak regions have one or two queen neighbours, so the conditional permutation distribution is wide. If so, "The few spatial outliers are …" misreads the evidence. It is a statement about the test's power, not about the absence of outliers.
- Check: list the HL and LH quadrant assignments (not only the significant ones) for the 27 capital regions, with their number of neighbours.

### A8. Ceuta and Melilla called "island regions" (Data section)
The paper says "13 island regions have no land border". Ceuta and Melilla (ES63, ES64) are Spanish exclaves on the African mainland, not islands. Ireland and Zealand are islands but are not on the list. Say "13 regions without a shared vertex".

### A9. Outermost-region robustness is weak evidence
Including the eight outermost regions changes kNN-5 I from 0.266 to 0.276. That is a small rise, but the eight regions are far from everything else, and in EPSG:3035 they sit at arbitrary projected positions. They mostly link to each other or to the Iberian Atlantic islands. They are also very poor (own knowledge). A tiny increase may therefore reflect an artificial low-income block rather than the absence of influence. The sentence "the robustness check suggests this choice matters little" is acceptable, but the mechanism should be stated. Distance weights from LAEA are not meaningful for French overseas territories.

## B. Known facts of the field the paper passes over

- **Commuting and workplace-based GDP** (own knowledge, and flagged in the paper's own literature review). The paper's LH outliers BE33 (Liège), DEB2 (Trier) and DK02 (Sjælland) are textbook commuter hinterlands of Luxembourg, Luxembourg and Copenhagen. Luxembourg's GDP per head is inflated by about 200,000 cross-border workers. The same holds for Hamburg and Brussels. The draft's limitation paragraph mentions provisional values, a single year and MAUP, but not commuting. A reader will take the LH labels as findings about neighbourhood economics when they are an accounting mismatch between place of work and place of residence.
- **Regional price levels.** PPS uses national price levels. Within-country price differences (Paris vs rural France, Prague vs the rest) are not removed. Income peaks in capitals are therefore overstated in real terms. This weakens any reading of capital regions as "income peaks".
- **Irish and Luxembourgish accounting.** The paper's range (a factor of six) and the Gini are partly driven by IE06, IE05 and LU00. Note the effect of dropping them on the ratio, not only on I. The drop-capitals variant removes five whole single-region countries, so it mixes two things: removing peaks and removing whole countries. A comparison removing the 27 richest regions or 27 random regions would separate them.
- **Provisional and estimated regional data.** About 71% of values are flagged `p` or `e`. National statistical offices often regionalise first estimates with distribution keys from earlier years (own knowledge). Estimated 2024 regional shares can therefore be smoother and more spatially persistent than final data. This could inflate Moran's I. A robustness run on the 69 unflagged regions, or a comparison with 2022, would help. The data dictionary promised an unflagged-only robustness check, and the paper does not report it.
- **Comparison with the literature.** Le Gallo and Ertur (2003) and later ESDA work find Moran's I of roughly 0.5–0.7 for EU regional per capita GDP at similar queen-type weights (own knowledge; the review file names the paper but gives no values, and the numbers are from memory). The paper's plan expected 0.5–0.8. The draft's 0.37 is lower than both. The lower value is plausible given Ireland, Luxembourg and the larger number of units, but the paper does not remark on the difference. One sentence on how 0.37 compares with earlier work would help.
- **Southern Italy and Spain in the cluster list.** Southern Italy is a textbook low-low block, yet only "some" southern Italian regions appear among the 38 low-low regions. Spain and France are not mentioned in either the low-low or high-high lists. The paper should say which regions of Campania, Puglia, Calabria, Sicilia and Andalucía are significant. Island links for Sicily and Sardinia (linked by the nearest-centroid rule) can change their LISA results.

## C. Selection and measurement

- **Index label.** The Data section says the index is "EU27 = 100". The data summary defines it as the population-weighted mean of the sample regions (40,077) and says Eurostat's official EU27 figure is not loaded. The plan required the label "EU27 sample mean = 100". The sample excludes the outermost regions, so this base is not Eurostat's. Fix the wording wherever the index appears, including figures.
- **Generalised boundaries.** 1:20m GISCO boundaries are used. The weights spec says vertices were rounded to "6 decimals" in one place and "metres" in another. Check that the 1,039 links and the 13 zero-neighbour regions are the same under 1:1m boundaries. A generalised border could drop a true neighbour. Mean 4.40 neighbours and a maximum of 11 look normal.
- **Edge effects.** Non-EU polygons are removed, so border regions (for example in the Baltic, Finland, Croatia and Greece) have fewer neighbours than they would have. That should be said when interpreting LISA at the eastern and south-eastern border, where most low-low regions lie.
- **Permutations.** 999 permutations are used, whereas the plan specified 9,999. Reporting "p = 0.001" for almost everything carries little information. With 999 permutations the FDR step is also coarse. The statement that "the uncorrected high-high clusters rest on weaker evidence than the low-income ones" is an inference from counts (1 of 19 versus 20 of 38). It may equally reflect the right-skewed distribution and the low power of the conditional test near extreme values. Give the p-value distribution of the HH regions, and rerun with 9,999.
- **Getis–Ord.** The z-scores are analytic (normal approximation), the plan asked for permutation p-values, and the distribution is right-skewed. The counts of 24 hot and 30 cold spots are uncorrected and approximate. The sentence "points the same way" is acceptable, but give the overlap with LISA (how many of the 24 are among the 19 HH regions).
- **Weights.** kNN-5 (0.266) and kNN-8 (0.265) are almost identical, whereas inverse distance gives 0.089. The explanation ("distant regions receive non-negligible weight") is plausible. The distance-decay correlogram the plan listed (item 5) would show it directly and would also show whether the signal is at the national scale (which would match the between-country result).

## D. Interpretation: sentences that say more than the numbers support

1. "Spatial autocorrelation disappears" / "high-income regions are thus not systematically adjacent to other high-income regions" (abstract, Section 4.4). An I of 0.020 with p = 0.6 means the test cannot distinguish it from zero, with the caveats in A2. "Is statistically indistinguishable from zero" (used in the introduction) is the correct wording. The abstract should use it as well.
2. "Inequality is partly a matter of extreme regions: dropping Luxembourg lowers the Gini only from 0.197 to 0.194, whereas dropping all capital regions lowers it to 0.174." Removing 27 regions (11% of the sample), several of them at the top, lowers any dispersion measure. That does not show that "extreme regions" matter. The Luxembourg result points the other way.
3. The reading that capital regions "lower autocorrelation instead of creating it" is correctly marked as a reading. It is partly wrong in the data: ITI4 (Lazio), DE30 (Berlin) and ES30 (Madrid) are not clear income peaks relative to their neighbours (own knowledge). The 27-region list is administrative capitals, not peaks.
4. "Because large regions are on average richer than small ones" (population-weighted mean). "Large" here means more populous, which is a statement about population, not area. The population-weighted mean is also pulled up by a few large rich regions (Île-de-France, Bavaria, Lombardy, Catalonia/Madrid). Say "populous".
5. "The national level absorbs most of the spatial signal": acceptable as a description. "Regional rankings cannot be separated from country membership" (Discussion) is stronger than the evidence, since the paper did not rank regions or test separation.
6. "Even after decades of convergence in national averages" (introduction) is stated without a source or a figure. The paper's own data cannot support it. Either cite or remove.
7. The Results claim that the lowest quintile covers "Hungary outside Budapest" and "Greece" should be checked against the quintile breaks. The lowest-quintile cut is about 26,000 PPS (between p10 at 22,750 and p25 at 28,375). Western and Central Transdanubia and Attiki are probably above it (own knowledge). Read the claims off the map data.

## E. Checks that would settle the main questions, in priority order

1. Print the EL30/BG41 rows (value, z, lag, quadrant, p) and verify the quadrant logic (A1).
2. Run country-by-country within-country Moran's I and a demeaned run without capitals, on ln GDP, with within-country permutation (A2).
3. Report the min/max of the 244-region file and fix "poorest/richest" wording (A4).
4. Add the Irish, Luxembourgish and commuting caveats to the data and limitations sections. Reword the LH/HL discussion for BE33, DEB2 and DK02 (B).
5. Run the unflagged-only robustness (69 regions) and a 9,999-permutation rerun (C).
6. Correct the introduction sentence on Ireland (A5), the "island" label (A8) and the index label (C).
7. Add a drop-27-richest or random-27 control to the capital exclusion, and a distance correlogram (B, C).

## Score

Numbers are internally consistent and of plausible magnitude, and the global Moran's I values and z-scores are credible for n = 236. The main doubts are the unchecked EL30 classification, the counter-intuitive within-country result that carries the paper's main message, and the absence of well-known measurement caveats (profit shifting, commuting, regional price levels, provisional regionalisation). Most can be settled by checks on existing outputs and by text changes.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
