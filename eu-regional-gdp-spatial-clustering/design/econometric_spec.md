# Econometric Specification: spatial statistics of GDP per inhabitant (PPS), EU NUTS-2, 2024

Descriptive spatial analysis. No regression, no causal claim. Script: `run_estimation.py`; results: `estimation_results.json`.

## Units and variable
- Units: EU27 NUTS 2 regions (NUTS 2024, GISCO 1:20m, EPSG:3035). Primary sample N = 236 (244 EU27 regions minus 8 outermost regions: FRY1-5, ES70, PT20, PT30). Robustness sample N = 244 with kNN weights.
- Variable: `gdp_pps` = GDP per inhabitant, PPS (EU27 2020), 2024 (Eurostat `nama_10r_2gdp`). Moran's I is computed on the level (`gdp_pps`) and, as a check, on `ln_gdp_pps`.
- Sample flow: 276 raw 2024 rows -> 0 missing -> drop 32 non-EU27 -> 244 -> drop 8 outermost -> 236. Read from `spatial_units.csv`, `spatial_weights*.csv` (built in the data step).

## Spatial weights
- Main: queen contiguity (shared vertex), row-standardised; 13 island regions linked to the nearest region by centroid distance (`spatial_weights.csv`).
- Robustness: kNN k = 5 (file), kNN k = 8 and inverse distance (1/d on centroid distance in km, all pairs, no truncation, row-standardised). Realised: queen I = 0.370 (z 7.8, p 0.001), kNN-5 0.266, kNN-8 0.265, inverse distance 0.089 (all p = 0.001); dropping capital regions raises I to 0.623 while within-country demeaned GDP gives I = 0.020 (p 0.60), i.e. the clustering is largely between-country. Local clusters (p<0.05, uncorrected): 19 HH, 38 LL, 2 HL, 3 LH; under BH-FDR 1 HH, 20 LL, 1 HL. Details in `estimation_results.json`., computed from area-weighted centroids in EPSG:3035. The kNN-5 run is also repeated on all 244 regions.

## Statistics
1. Global Moran's I = (n/S0) sum_ij w_ij z_i z_j / sum z_i^2; E[I] = -1/(n-1). Inference: 999 random permutations of values over units (seed fixed), two-sided pseudo p = (1 + #{|I_perm - E| >= |I - E|}) / 1000; z = (I - mean(I_perm)) / sd(I_perm).
2. Moran scatterplot data: z_i and spatial lag Wz_i per region, quadrant label; slope of Wz on z equals I for row-standardised W.
3. Local Moran's I (LISA): I_i = z_i sum_j w_ij z_j / (sum z^2 / n), conditional permutation (999) per unit, classification HH/LL/HL/LH at pseudo p < 0.05, else not significant. Multiple-testing caveat: with 236 tests about 12 false positives are expected at 0.05; counts are also reported under Benjamini-Hochberg FDR (q = 0.05) applied to the pseudo p-values.
4. Getis-Ord Gi* (row-standardised weights including the own value), z-scores from the analytic expectation; hot/cold spots at |z| > 1.96, secondary to LISA.
5. Distribution: mean, SD, coefficient of variation, population-weighted CV, Gini, Theil T index, and Theil between-country / within-country decomposition (population-weighted).
6. Sensitivity: Moran's I (queen) after dropping (a) Luxembourg (LU00), (b) Irish regions (IE04-IE06; profit-shifting distortion), (c) top-5 by value, (d) national capital regions (BE10, BG41, CZ01, DK01, DE30, EE00, IE06, EL30, ES30, FR10, HR05, ITI4, CY00, LV00, LT01, LU00, HU11, MT00, NL32, AT13, PL91, PT17, RO32, SI04, SK01, FI1B, SE11). Weights are rebuilt by dropping rows/columns and re-row-standardising (a unit left without neighbours keeps zero row). Also Moran's I of within-country demeaned GDP (deviation from national population-weighted mean) to separate a between-country from a regional pattern.

## Maps and figures
Choropleth of GDP per inhabitant (quintiles) and of the EU index; Moran scatterplot; LISA cluster map (categories). Maps are specified in `estimation_results.json` and `figure_spec.json`; they carry the GISCO attribution.

## Caveats
Spatial autocorrelation is a description, not a cause. Results depend on weights and on the MAUP (NUTS 2 level fixed). Irish values reflect multinational accounting. Provisional/estimated Eurostat flags are retained. Realised numbers are in `estimation_results.json` and are not typed here.
