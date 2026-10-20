# Data Review: Spatial Clustering of GDP per Inhabitant across EU NUTS-2 Regions, 2024

Scope: source documentation, sample construction, missing values, variable definitions, outliers, measurement, spatial-weights data structure, and internal numerical consistency. I reviewed the draft against the data dictionary, data summary, specification, plan and literature notes. The `.tex` tables, the figures, `estimation_results.json` and `summary_statistics.json` were not supplied, so I could only check numbers against the text and the supporting documents.

## Overall assessment

The data foundation is sound. The sources are public Eurostat and GISCO products. Keys match with zero unmatched regions. The sample flow is explicit (276 → 244 → 236) and no values are missing. The draft states its provisional/estimated flags, which most papers of this type omit.

Three problems matter:
1. The within-country "demeaned" test uses a null distribution that does not fit the transformed variable. The headline claim that clustering "disappears" is therefore not established.
2. Several measurement caveats from the plan and literature notes (commuting, Irish profit shifting, regional price levels, index base) are missing or mislabelled in the draft.
3. The weights graph has disconnected components, and the island rule does not cover them. Some reported clusters and outliers may be artefacts of this.

The researcher's seven corrections are applied in the draft. I confirm items 1–7, including the EuroGeographics notice in both map captions. Residual issues are below.

## 1. Source documentation

**Adequate.**
- Datasets are named: `nama_10r_2gdp`, unit `PPS_EU27_2020_HAB`; `demo_r_d2jan`; GISCO NUTS 2024 at 1:20m in EPSG:3035.
- The unit of observation, geography and year are clear. The Eurostat non-responsibility sentence is present.

**Gaps.**
- **Data vintage is missing.** The dictionary records the GDP release as 2026-02-10 and the population release as 2026-08-28, plus DOIs, access date 2026-10-14 and SHA-256 hashes. None of this appears in the paper. Because about 71% of 2024 values are provisional or estimated, the release date is essential for replication. Add a data-availability footnote with DOI, release dates and access date.
- **Both Eurostat datasets share one citation key (`Eurostat_Database`).** Cite `nama_10r_2gdp` and `demo_r_d2jan` separately with their DOIs.
- **The key is also cited in the Introduction for a policy claim** ("NUTS-2 is the reference unit for cohesion policy"). A statistical database is not a source for that. Cite the NUTS or cohesion regulation instead, or drop the citation.
- **NUTS vintage is not stated for the GDP data.** The plan requires the sentence "NUTS 2024 as delivered by Eurostat". The paper says only that identifiers match across sources. State the vintage explicitly. The literature note marks the count of 244 NUTS-2 regions as "[verify]". Confirm it against Eurostat metadata.
- **Inconsistent description of the GDP table.** The dictionary describes "gdp_pps_nuts2" with 276 regions including TR, RS, ME and MK. The paper correctly restricts to EU27, but the non-EU drop (32 rows) is not shown in the text. Add a sample-flow table (see §2).
- **Replication details are absent.** No software or library versions, no seed (the plan names 20241014), no code or data availability statement.

## 2. Sample construction

The flow of 276 → 244 → 236 is clean and consistent across documents. Population 444 million is plausible: roughly 450 million for the EU27 less about 5 million in the eight outermost regions.

**Issues.**
- **The paper has no sample-flow table.** The checklist expects N at each step. The text gives only 244 and 236. Add the table: raw 276, non-EU27 (TR 26, RS 4, ME 1, MK 1) dropped, outermost regions (8) dropped, merge matches.
- **The outermost-region rationale is inconsistent.**
  - Regions are excluded because they are "separated by thousands of kilometres". Cyprus (646 km link to EL42), Malta, Ceuta and Melilla are retained and linked by an ad hoc nearest-centroid rule.
  - Ceuta and Melilla are tiny enclaves linked to the nearest region. Canarias is dropped while Baleares is kept.
  - The cut is defensible (the 244-region kNN run shows little change), but the rule should be stated as a convention. The plan's R3 variant (queen without island links, and n = 223 without the islands) is not reported. It is the direct test of this choice.
- **Edge effects are not discussed.** The EU27 frame cuts off CH, NO, UK and the Western Balkans. The dictionary notes that border regions have fewer neighbours. GDP data for CH and NO are not in the delivered table. Moran's I is therefore conditional on the EU27 frame. Say so.
- **The weights graph has disconnected components.** The 13-island rule applies only to regions with no shared vertex.
  - Ireland (IE04–IE06) share borders with each other, so they receive no link to any other EU region. DK01 and DK02 on Zealand are probably in the same position. Please verify.
  - Consequences: the "HH" cluster of the three Irish regions is a cluster only of Irish regions with each other. DK02's "low-high" status may arise only because its sole neighbour is the Copenhagen region.
  - These are mechanical consequences of the graph, not evidence about spatial structure. Report the number of connected components, and list isolates and small components.
  - The claim "every region has at least one neighbour" is true but does not imply connectivity.
- **Dropping capital regions also changes the sample composition.** The 27 capitals include five whole countries (EE, LV, LU, CY, MT).
  - The 0.623 result is computed on a different sample and graph, with three regions left with zero-weight rows. This changes S0 and the effective n.
  - It is not comparable with 0.370 without that caveat. The draft notes it as a caveat, which is good, but the Introduction still says it "raises it considerably" without qualification.
  - A cleaner variant drops capitals only in multi-region countries, or keeps zero-row regions out of the denominator explicitly.

## 3. Missing values

No missing 2024 values for EU27. This is documented consistently and needs no further action.

**Provisional and estimated flags.** 134 provisional and 33 estimated of 236 (167, or 71%, flagged). The draft reports this, which is good.
- The dictionary promised a robustness check excluding flagged values or using 2023. The paper does not report it. At 71% flagged, "excluding flagged values" leaves only 69 regions. A version restricted to the unflagged regions would be too small and non-random, so I recommend the 2023 comparison instead.
- The plan's R11 (earlier years, same NUTS vintage) is also absent. At minimum run 2023 as a vintage-stability check. This would also support the Discussion's statement on revisions.

## 4. Variable definitions and measurement

- **The index is mislabelled.** The Data section says "the index version of the variable (EU27 = 100)". The data summary defines `gdp_index` as GDP divided by the population-weighted mean of the 236 sample regions (40,077) times 100. That base excludes the outermost regions and is not Eurostat's official EU27 figure. The plan says to label it "EU27 sample mean = 100". Fix this in the text, and in the map and table labels if the index is mapped.
- **Irish profit shifting is not mentioned in the paper.** The plan, specification and data summary all flag it. IE06 is the maximum, so the headline ratio of 6.4 and the Gini depend on it. State in the Data section that Irish values (and, to a lesser degree, Luxembourg's) reflect multinational accounting. Then justify the Irish robustness check there, not only in the Results.
- **Commuting and workplace-based GDP are not discussed.** GDP is allocated by workplace and population by residence. Net in-commuting inflates Luxembourg, Brussels, Hamburg and Prague, and depresses surrounding regions. This directly affects the "outlier" classes (HL and LH) in the LISA results. Add it to the limitations.
- **PPS adjusts for national, not regional, price levels.** This matters for the paper's own conclusion. The between-country component of the clustering is partly constructed by national PPS conversion. The draft reads the national blocks as a feature of income. Say that PPS makes national and regional price levels non-comparable inside countries.
- **Mixed denominators.** Regional GDP per head uses Eurostat's own population denominator. The population weights use 1 January 2024 counts. This is minor, but state it.
- **Log and level.** The level is primary and the log is a robustness check. The Moran result on the log (0.482) is higher than on the level, so the level result is the conservative one. That is fine as presented.

## 5. Outliers

The treatment is better than usual, with LU, IE, the top five and the capitals each dropped. Remaining points:
- **Wording on the Gini is confusing.** "Inequality is partly a matter of extreme regions: dropping Luxembourg lowers the Gini only from 0.197 to 0.194" reads as evidence against the first clause. Rephrase: dropping LU changes it little; dropping all 27 capitals lowers it more, partly because that drops five whole countries.
- **Irish drop is described inconsistently.** The Introduction says dropping Luxembourg, the Irish regions or the five richest "leaves it unchanged or stronger". The Results give 0.342 for the Irish drop, which is lower than 0.370. Say "slightly lower" for that case.
- **Dropping the top five leaves one isolated region** (probably IE04). The abstract and Introduction cite this variant as evidence that clustering "raises" when peaks are removed. The isolated region's zero row should be mentioned in that sentence as well, not only in the robustness section.
- **The planned trim and winsorise variants (R7) are not reported.** Leave-one-country-out results would address the checklist item on cross-country influence. Poland (17 regions), Greece, Romania and Bulgaria drive the LL counts.

## 6. Within-country demeaning: the central data-construction concern

The headline claim is that spatial autocorrelation "disappears" after subtracting each country's population-weighted mean (I = 0.020, z = 0.5, p = 0.6). I see three problems.

1. **The null distribution is wrong for the transformed variable.**
   - Demeaned values sum to zero (population-weighted) within each country. About 75% of queen links are within-country.
   - Under a within-country null, the expected Moran's I of such data is negative, roughly −1/(n_c − 1) per country, so about −0.06 for Poland and −0.3 to −0.5 for two- to three-region countries. This is larger in magnitude than the −0.004 used.
   - The test permutes demeaned values across all 236 regions. That breaks the structure the transformation created and compares I = 0.020 with an expectation of about −0.004.
   - A within-country permutation (shuffle regions within each country) would give the proper reference. If the proper null is negative, 0.020 may be significantly positive. That would reverse the abstract's claim.
   - The paper should run this test before concluding that "spatial autocorrelation disappears".
2. **The five single-region countries contribute exact zeros** (EE, LV, LU, CY, MT). Regions in two- or three-region countries have heavily constrained deviations. Report the result separately for countries with at least five regions.
3. **Weighting is inconsistent.** The demeaning is population-weighted, but Moran's I is unweighted. A region-count (unweighted) demean, or demeaning the log as the plan specifies, should be shown as a variant. The plan specified ln GDP, whereas the draft appears to use the level.

Related framing issue: the Theil decomposition attributes only 36% of inequality to between-country differences. The abstract nonetheless says the clustering is "almost entirely a between-country phenomenon". These statements are not contradictory (one concerns dispersion, the other co-location), but the paper should reconcile them. The 24.8% share of cross-border links is also computed on a graph that may miss cross-border links. The dictionary says coordinates are rounded to 6 decimals while the data summary says metres. Verify the rounding, because at 1:20m a rounding difference could drop cross-border shared vertices. Report the rounding that was used.

## 7. Spatial statistics: data-related checks

- **Permutation count.** The paper uses 999 permutations. The plan specified 9,999. All reported p-values sit at the floor of 0.001, so they cannot discriminate. For the LISA step, a floor of 0.001 with Benjamini–Hochberg means the 22 survivors depend on resolution. Rerun with 9,999 or more. BH also assumes independence or positive dependence, which is questionable for spatially dependent local tests. The literature notes cite Caldas de Castro and Singer (2006), who address exactly this. Cite and discuss it.
- **Spot-check of a reported classification.** EL30 (Attiki) is reported as high-low. This needs a value above the sample mean of 37,976 PPS. My recollection is that Attiki's PPS value is well below that, but I could not verify it with the files provided. Please check `spatial_units.csv`. If it is below the mean, the HL label would come from a classification error, and the HL count and FDR HL count would change.
- **Czech low-low regions.** CZ01 is among the top five, while LL Czech regions are listed. That is plausible but should be checked against the data, because LL requires the region itself to be below the mean.
- **Gi\* inference** uses analytic z-scores (specification), while the plan said permutation p-values. The paper does not say which. State the method.
- **Planned but unreported items:** Geary's C, k = 3, the island-rule variants, the distance correlogram, R7 and R11. If dropped, say so. The plan's rule was "no variant is dropped after seeing results".
- **The plan expected I of 0.5–0.8 for the level.** The realised 0.37 is outside that range. The draft is right to report what the data show, but note it.

## 8. Numerical consistency checks I could perform

| Item | Check | Result |
|---|---|---|
| Quadrant counts | 74 + 105 + 31 + 26 | 236 ✓ |
| Share sharing neighbours' sign | (74 + 105) / 236 | 75.8% ✓ ("about three quarters") |
| LISA counts | 19 + 38 + 2 + 3 | 62 ✓ |
| Expected false positives | 0.05 × 236 | 11.8 ✓ |
| Flags | 134 + 33 + 69 | 236 ✓ |
| E[I] | −1/235 | −0.0043 ✓ |
| Max/min | 107,200 / 16,700 | 6.42 ✓ |
| P90/P10 | 53,550 / 22,750 | 2.35 ✓ |
| Coefficient of variation | 14,246 / 37,976 | 0.3751, which rounds to 0.38, not 0.37. Check the SD convention (sample vs population) and fix |

## 9. Other points

- **Unsupported claims about prior work.** "Rarely reported together" (contribution paragraph) and "does not quantify the spatial structure of regional income itself" (about Pourpakdelfekr 2026) are not supported by a search the paper documents. The literature review itself says the contribution is a modest update and should not be oversold. It also lists the closest antecedent (Le Gallo and Ertur 2003), whose bibliographic entry is not yet registered. The draft cites none of it. At minimum cite the closest ESDA papers.
- **Summary-statistics table.** The `.tex` was not supplied. Make sure it includes N, mean, SD, min, p10, median, p90, max, the population-weighted mean and the flag counts.
- **Unweighted Gini.** The Gini and CV are across regions of very different sizes (Malta/Luxembourg versus Île-de-France). The specification listed a population-weighted CV and the plan a weighted SD of logs; report them alongside.
- **Licence and attribution.** Both map captions carry the EuroGeographics notice. Add a "changed data" note (filtered, re-indexed) to the data statement, as the dictionary requires.

## Priority list

1. Re-run the demeaned test with a within-country permutation null and a size-restricted subset. Revise the abstract and Discussion according to the result.
2. Report graph connectivity (components, isolates). Reassess the Irish HH cluster, DK02 and any other cluster tied to a disconnected component.
3. Add the missing measurement caveats: Irish profit shifting, commuting, and PPS at national price levels only. Relabel the index as "sample mean = 100".
4. Increase permutations (≥ 9,999) and discuss BH under dependence. Verify the EL30 classification.
5. Add vintage, DOIs, release dates, a sample-flow table, seed and software versions. Report the 2023 or unflagged-value robustness.
6. Fix small items: CV rounding (0.375 → 0.38), the "unchanged or stronger" wording, and the Gini sentence.

OVERALL SCORE: 5.5/10
RECOMMENDATION: Major Revision
