# Paper Plan: GDP per capita in PPS across EU NUTS-2 regions, 2024: distribution and spatial clustering

**Template:** spatial analysis (descriptive; no causal claim, no regression, no identification strategy).
**Keywords:** regional inequality; GDP per capita; purchasing power standards; NUTS 2; spatial autocorrelation; Moran's I; LISA; European Union; core-periphery. (No JEL codes anywhere.)

## 1. Phenomenon and research question

**Phenomenon.** After decades of EU cohesion policy, GDP per inhabitant in PPS still differs by a factor of about 6 between the richest and poorest EU NUTS-2 regions (2024: 107,200 in IE06 vs 16,700 in BG31, primary sample). A map of these values looks like a few bright cores (Ireland, Luxembourg, Hamburg/Munich-type regions, Prague, Brussels) and large contiguous dark areas (Bulgaria/Romania, southern Italy, Greece, eastern Poland). Whether this is mainly a between-country pattern, a regional core-periphery pattern, or a set of isolated metropolitan peaks is not obvious from a table.

**RQ.** How does GDP per capita in PPS vary across EU NUTS-2 regions in 2024, and how strongly do high- and low-income regions cluster in space?

**Sub-questions (descriptive only).**
1. What is the shape of the 2024 distribution (centre, dispersion, tails, top and bottom regions)?
2. Is there global positive spatial autocorrelation, and how large is it relative to its permutation distribution?
3. Where are the local clusters (high-high, low-low) and spatial outliers (high-low, low-high)?
4. Are the results driven by a few extreme or capital regions (Luxembourg, Irish regions, Inner London-type, Brussels, Hamburg, Prague, Bratislava), by the island/outermost-region treatment, or by the weights choice?

**Why it matters.** Cohesion-policy eligibility and the "regional convergence" debate rest on the regional income ordering; knowing whether poverty is spatially concentrated (clusters spanning borders) or scattered informs how spatial the descriptive picture of EU disparities is. Spatial structure is a descriptive fact here; no claim is made about why it arises or about policy effects. Reverse-insight value: if Moran's I largely vanishes within countries or after dropping a handful of metropolitan peaks, the clustering is a country-level and peak-driven pattern, not a smooth regional gradient. This is reported as an association, not tested causally.

## 2. Data (already built in data.db / project files; do not rebuild)

| Item | Source | Detail |
|---|---|---|
| GDP per inhabitant | Eurostat `nama_10r_2gdp`, unit `PPS_EU27_2020_HAB` | table `gdp_pps_nuts2`, 2015-2024, release 2026-02-10; 2024 slice: 276 regions, no missing values |
| Boundaries | GISCO NUTS 2024, 1:20m, EPSG:3035 | table `nuts2_boundaries`; join key `geo` = `nuts_id`; no recoding needed |
| Population 1 Jan 2024 | Eurostat `demo_r_d2jan` | table `pop_nuts2`; used only for region size and a population-weighted mean |

**Classification note.** The work order names NUTS 2021; the delivered Eurostat table and GISCO boundaries both use NUTS 2024 codes, which join with zero mismatches. The paper states "NUTS 2024 (as delivered by Eurostat for the 2024 reference year)" and flags that NUTS 2021 and 2024 differ in a few regions' codes/borders; no recoding is performed. The drafter must not write "NUTS 2021" unless the data_analyst verifies equivalence.

**Sample flow (2024).** 276 raw regions -> drop 32 non-EU27 (TR 26, RS 4, ME 1, MK 1) = 244 EU27 regions -> drop 8 outermost regions without land or short-sea neighbours (FRY1-FRY5, ES70, PT20, PT30) = **236 primary regions**. The 244-region sample is used in the kNN robustness run only. Values carry Eurostat flags (p provisional: 134; e estimated: 33; none: 69); they are kept and reported, not altered.

**Measurement caveats to state.** (i) GDP is workplace-based: commuting inflates GDP per head in core/capital regions (Inner London, Brussels, Hamburg, Luxembourg, Prague) and depresses it in surrounding dormitory regions, which mechanically sharpens high-low and low-high neighbours. (ii) Irish values are inflated by multinational profit shifting. (iii) NUTS 2 units vary widely in size and population, so the modifiable areal unit problem applies. (iv) The index base is the population-weighted mean of the sample regions (40,077), not Eurostat's official EU27 national-accounts value; label it "EU27 sample mean = 100".

## 3. Descriptive statistics (Section "Distribution")

Computed on the 236-region primary sample (and reported also for the 244-region sample in a footnote or appendix table).

- Level (PPS): mean (37,976), median (35,050), SD (14,246), min, max, p5/p10/p25/p75/p90/p95, max/min ratio, p90/p10 ratio, IQR.
- Dispersion: coefficient of variation (SD/mean), the same for ln GDP (SD of logs), Gini coefficient, and a population-weighted CV and SD of logs as a check against small-region dominance.
- Index: `gdp_index` = GDP_pps / population-weighted sample mean x 100. Report the share of regions above 100 (86 of 236), above 75 and above 125 (the 75% line is the conventional cohesion-policy threshold; mention as a reference line only, without evaluating eligibility).
- Decomposition (descriptive): variance of ln GDP between versus within countries (one-way variance decomposition, i.e. an R-squared from country groups, reported as a share, not a regression result of interest). This quantifies how much of the dispersion is national and gives context for Moran's I.
- Tables: top 10 and bottom 10 regions with code, name, country, PPS, index, population, flag. Country summary table (n regions, median, min, max, within-country CV).
- Figures: histogram/density of GDP_pps (with mean and median marked); rank (caterpillar) plot of all regions coloured by country group is optional.

## 4. Spatial design

**Projection.** EPSG:3035 (ETRS89-LAEA Europe) for all geometry operations and for map display.

**Weights matrices (row-standardised, W).**
1. *Primary: queen contiguity* on shared vertices (coordinates rounded to metres) on the 236-region sample. 1,039 links, mean 4.40 neighbours, max 11. **Island handling:** 13 regions have no shared vertex (EL41, EL42, EL43, EL62, ES53, ES63, ES64, FRM0, ITG1, ITG2, CY00, MT00, FI20). Each is linked to its nearest region by centroid distance (a documented ad hoc rule; links listed with distances in `summary_statistics.json`, largest Cyprus-EL42 at 646 km). Several of these links are weak substitutes for adjacency (Cyprus, Malta, Sicily, Ceuta); this is tested rather than assumed, see robustness.
2. *Robustness: k-nearest neighbours, k = 5*, on area-weighted centroids in EPSG:3035 metres; asymmetric, no islands by construction, row-standardised (1,180 links on 236 regions; 1,220 on 244 regions). Additional k = 3 and k = 8 as sensitivity to k.
3. *Robustness: inverse-distance band* (distance threshold = smallest value giving every region at least one neighbour, row-standardised) as an optional third family; drop if the analysis step finds it uninformative.
4. Queen contiguity with islands left as zero-neighbour rows (no nearest-neighbour link), implemented with row-standardisation that leaves those rows at zero, and the 223-region result without the 13 islands. This shows how much the island rule matters.

**Outermost regions** (FRY1-FRY5, ES70, PT20, PT30) have no meaningful neighbours and are excluded from the primary sample; the kNN run on all 244 regions shows they do not drive the result.

## 5. Spatial statistics (Section "Spatial clustering")

All inference uses conditional permutation (9,999 permutations, fixed seed, e.g. 20241014). Variable: GDP_pps (level) as primary, ln GDP as a robustness check (the level distribution is right-skewed and Moran's I is sensitive to extreme values). Statistics are computed on the raw variable, not on residuals; no regression is estimated.

1. **Global Moran's I** for each weights matrix: I, expected value -1/(n-1), permutation mean and SD, pseudo-z, pseudo-p (two-sided and one-sided upper), plus the Moran scatterplot (z-scored GDP on x, spatial lag on y, with fitted slope, which equals I under row-standardised W).
2. **Global Geary's C** as a secondary global measure (sensitive to local differences), reported in one line.
3. **Local Moran's I (LISA)** with queen W: for each region the local I_i, pseudo-p from 9,999 conditional permutations, and quadrant (HH, LL, HL, LH). Significance at p < 0.05; also report the count at p < 0.01 and at the Benjamini-Hochberg false-discovery-rate threshold (q = 0.05) because 236 simultaneous local tests are run. Regions significant only before correction are marked as "suggestive" and not described as clusters. Output: table of regions per category by country; counts per quadrant.
4. **Optional: Getis-Ord Gi\*** (self-included, queen W with the self-weight) on GDP_pps, with z-scores and permutation p-values, reported as hot/cold spots at the 90, 95, 99% levels, as a cross-check on LISA. Reported in one figure or the appendix; if Gi\* and LISA disagree on the cluster map for more than a handful of regions, discuss as sensitivity of local statistics to the statistic choice.
5. **Distance profile (optional, one panel):** Moran's I on kNN weights for k = 1..20 or a correlogram in distance bands, to describe how fast spatial association decays. Descriptive.
6. **Within-country spatial structure (descriptive check):** Moran's I of the country-demeaned ln GDP (subtract country mean) with the same W. This is a transformation of the variable, not a regression; it indicates whether clustering extends beyond national averages. Report with the caveat that countries with few regions (CY, MT, LU, EE, LV, LT, SI, etc.) contribute little.

## 6. Robustness and sensitivity (all reported, including those that change the picture)

| # | Variation | Purpose |
|---|---|---|
| R1 | kNN k = 3, 5, 8 instead of queen | weights choice |
| R2 | 244 regions incl. outermost, kNN only | outermost-region exclusion |
| R3 | Queen without nearest-neighbour links for the 13 islands (n = 236 with zero rows, and n = 223 dropping them) | island rule |
| R4 | Drop Luxembourg (LU00) | extreme high-income small unit |
| R5 | Drop Irish regions (IE04-IE06 as classified in the data) | profit-shifting distortion in GDP |
| R6 | Drop capital-city regions (one per country: BE10, BG41, CZ01, DK01, DE30, EE00, IE06, EL30, ES30, FR10, HR05, ITI4, CY00, LV00, LT01, LU00, HU11, MT00, NL32, AT13, PL91, PT17, RO32, SI04, SK01, FI1B, SE11) and, jointly, Inner London-type metropolitan peaks as they appear in the EU sample | peak-driven clustering; Inner London itself is not in the EU27 sample after Brexit, so the analogues are Brussels, Hamburg, Prague, Bratislava, Paris (verify codes against the data) |
| R7 | Drop the top 5% and bottom 5% of regions by GDP_pps (trimmed sample), and also winsorise at p5/p95 as a separate variant | outlier leverage on I |
| R8 | ln GDP_pps instead of level | skewness |
| R9 | Country-demeaned ln GDP | within-country structure (Section 5.6) |
| R10 | Population-weighted check: report Moran's I with units weighted by population only descriptively (e.g. the correlation of local I with population), not as a different estimator | MAUP / size heterogeneity |
| R11 | Other reference year (2019, 2015) for global Moran's I only, from the already loaded table (only if the analysis step has the 2019/2015 slices on the same classification; otherwise skip and say so) | persistence of the pattern; not a trend or convergence claim |

Rule for reporting: a table with one row per variant giving N, W, I, pseudo-p; a figure of I with permutation intervals across variants; LISA cluster maps for R1, R4 and R6 in the appendix. If conclusions differ across variants, say so in the text. No variant is dropped after seeing results.

## 7. Map and figure design (for the figure specification)

- **Map 1 (choropleth of GDP_pps, 2024):** EPSG:3035; quantile classes (5 classes, quintiles) as the main map, with a second panel using the EU index classes (< 50, 50-75, 75-100, 100-125, 125-150, > 150) to tie to the "EU = 100" reading. Sequential single-hue colourblind-safe palette (e.g. viridis or ColorBrewer Blues/YlGnBu), light for low, dark for high; missing/outermost regions in light grey with hatching; thin white region borders, thicker national borders. Inset or side panel for the outermost regions (placement outside the main frame) is optional. Legend with class breaks in PPS and the number of regions per class. Source and attribution line: "Source: Eurostat nama_10r_2gdp; © EuroGeographics for the administrative boundaries."
- **Map 2 (LISA cluster map, queen W):** categorical palette: HH dark red, LL dark blue, HL light red, LH light blue, not significant light grey; only regions with p < 0.05 (and the FDR variant in an appendix map) coloured; note permutation count and seed.
- **Map 3 (Gi\* hot/cold spots)** if Gi\* is run: diverging palette with confidence bins.
- **Figure 4:** Moran scatterplot with labelled outliers (e.g. LU00, IE06, BE10 in the HH/HL zone; named cases in LH).
- **Figure 5:** Histogram/density of GDP_pps (mean/median marked); optionally rank plot.
- **Figure 6:** Robustness plot of I across variants (R1-R11) with permutation 95% intervals.
- No 3D, pie or bubble maps; maps must be legible in greyscale (monotone lightness).
- All figures reproducible from the analysis script, with fixed seed and software versions logged (libpysal/esda/geopandas or R spdep/sf).

## 8. Expected patterns (stated before estimation; hypotheses are descriptive, not causal)

H1. Global Moran's I is clearly positive and significant under queen and kNN weights (expected range 0.5-0.8 for the level). H2. LISA finds HH clusters in western/central core regions (southern Germany, Austria, the Benelux, northern Italy, Ile-de-France surroundings, Nordic regions) and LL clusters in Bulgaria/Romania, southern Italy, Greece and parts of eastern Poland and Hungary; HL outliers are the capitals of lower-income countries (e.g. Bucharest, Sofia, Bratislava, Prague, Warsaw) and LH outliers are the rural regions around Brussels, Hamburg or Paris (commuting artefact). H3. Moran's I falls when Luxembourg, Ireland and the capitals are dropped, but remains positive; the country-demeaned I is much smaller than the raw I, indicating that the clustering is largely national. If the data contradict H1-H3 the paper reports that. These are predictions, not claims about causes.

## 9. Interpretation limits (must be stated in the paper)

Descriptive associations only: no statement that proximity, spillovers or policies cause income levels. Moran's I measures similarity of neighbours given W; it does not identify spatial dependence mechanisms, and results depend on W and on regional unit definitions (MAUP). Workplace-based GDP per head overstates income of residents in commuter-attracting cores; PPS adjusts for national, not regional, price levels. Provisional/estimated values (p, e flags: about two thirds of the sample) may be revised. Single cross-section 2024; no convergence or trend inference.

## 10. Pipeline handoff

- **data_architect / data_analyst (already largely done):** `build_data.py` created `spatial_units.csv` (236), `spatial_units_all244.csv`, `spatial_weights.csv` (queen), `spatial_weights_knn5.csv`, `spatial_weights_knn5_all244.csv`, `summary_statistics.json`, `figure_spec.json`. Remaining: add k = 3 and k = 8 weights, the island-rule variants (R3), the country-demeaned and decomposition statistics, and the Gini; confirm the capital-region code list in R6 against the data and fill the NUTS classification note from Eurostat metadata; write `data_dictionary.json` with `unavailable` entries for any item the sources cannot supply (e.g. official EU27 index base, regional price levels).
- **spatial_design check (before analysis):** boundaries join (0 unmatched), CRS EPSG:3035, weights row-sums = 1, island list and link distances documented.
- **econometrics_specialist:** writes `estimation_results.json` in the spatial results schema: global I, Geary's C, permutation details, LISA table with p-values and FDR flags, Gi\* (optional), robustness table. **No regression.**
- **spatial_results check (after analysis):** Moran's I recomputed from the weights files matches the reported value; maps present with legend, CRS and source.
- **paper_drafter:** structure: 1 Introduction (phenomenon, RQ); 2 Data and measurement; 3 Distribution of GDP per capita in PPS; 4 Spatial weights and methods; 5 Global and local clustering; 6 Robustness; 7 Discussion and limits; descriptive wording throughout ("is associated with", "clusters"), keywords but no JEL line.

## 11. Positioning (closest prior work; literature to be verified by the literature step with `e2er-lit search`)

Closest strands: (1) Eurostat's regional yearbook/GDP releases (descriptive rankings, no spatial statistics); (2) the regional-convergence and spatial-econometrics literature on EU NUTS-2 (e.g. Le Gallo and Ertur 2003, "Exploratory spatial data analysis of the distribution of regional per capita GDP in Europe, 1980-1995", Papers in Regional Science; Rey and Montouri 1999 for US regions; Ertur and Koch 2007 on spatial spillovers in growth), which use earlier NUTS vintages and earlier years; (3) EU Commission cohesion reports (core-periphery narratives). The citations above are from memory and must be verified before use. The contribution is modest and empirical: a current (2024), reproducible measurement of spatial clustering on the present NUTS-2 map with explicit treatment of island/outermost regions and capital/outlier robustness. Target outlets: regional-science or regional-studies field journals (e.g. Regional Studies, Spatial Economic Analysis, Papers in Regional Science), or a data/research note.
