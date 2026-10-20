# Data Summary (design written before the analysis script; realized numbers are filled in after the run)

## Sources and tables (all in data.db, loaded by the data architect; none rebuilt by hand)

- `gdp_pps_nuts2`: 2,826 rows, Eurostat `nama_10r_2gdp`, unit `PPS_EU27_2020_HAB` (GDP at current market prices, PPS per inhabitant, EU27 from 2020), NUTS 2, 2015 to 2024. Release 2026-02-10. 2024 slice: 276 regions, value non-null in all 276.
- `nuts2_boundaries`: 299 rows, GISCO NUTS 2024, 1:20 million, already in EPSG:3035 (ETRS89-LAEA, metres). Boundaries credit: © EuroGeographics for the administrative boundaries.
- `pop_nuts2`: 292 rows, Eurostat `demo_r_d2jan`, population on 1 January 2024 (total). Used only to describe region size and for a population-weighted descriptive mean.

Modification notice: Eurostat figures are summarised and re-scaled (indexed to the EU27 mean); Eurostat is not responsible for these derived figures.

## Variable definitions

- `gdp_pps` = Eurostat value for time = 2024 (PPS per inhabitant). Eurostat flags are kept (`p` provisional, `e` estimated).
- `gdp_index` = `gdp_pps` / EU27 reference * 100, where the reference is the population-weighted mean of the regions in the EU27 sample (descriptive; Eurostat's official EU27 national-accounts figure is not loaded).
- `ln_gdp_pps` = natural log of `gdp_pps`.

## Sample construction

Code harmonisation: data and boundaries both use NUTS 2024 codes (verified by SQL join, key `geo` = `nuts_id`, no recoding needed). Greece is `EL`, as in both tables.

1. 2024 rows in `gdp_pps_nuts2`: 276 (all values present).
2. Drop non-EU27 regions (TR 26, RS 4, ME 1, MK 1 = 32): 244 EU27 NUTS 2 regions. This is every EU27 NUTS 2024 region.
3. Drop outermost regions without a land or short-sea neighbour (FRY1 to FRY5, ES70, PT20, PT30 = 8): 236 regions = primary sample (queen contiguity and kNN).
4. Robustness sample: all 244 EU27 regions, kNN weights only.

Missing values: none in the 2024 value column, so nothing is dropped or imputed. Regions in the boundaries but not in the data (23 non-EU27 / EFTA / candidate units: CH, NO, IS, LI, AL, BA, XK) are outside the EU frame and not used. Data regions without geometry: 0.

## Spatial weights (constructed here, not tested here)

- Queen contiguity from shared vertices of the EPSG:3035 polygons (coordinates rounded to metres), row-standardised. Islands (no shared vertex) are linked to their nearest region by centroid distance and listed in `data_quality_log` in summary_statistics.json.
- kNN (k = 5) on area-weighted centroids in EPSG:3035 metres, row-standardised, asymmetric, no islands.
- Outputs: `spatial_units.csv`, `spatial_weights.csv` (queen), `spatial_weights_knn5.csv`, `spatial_weights_knn5_all244.csv`.
- No Moran's I, LISA or regressions were computed in this step.

## Realized results

Produced by `build_data.py` (run with `e2er-run`); all numbers trace to `summary_statistics.json`. Table row counts as held in data.db: gdp_pps_nuts2: 2,826 rows (2015 to 2024); nuts2_boundaries: 299 rows; pop_nuts2: 292 rows (2024); derived `gdp_pps_sample`: 236 rows.

**Sample flow (2024):** 276 raw rows -> 0 missing values -> drop 32 non-EU27 (TR 26, RS 4, ME 1, MK 1) = 244 EU27 regions -> merge to geometry, 244 matched, 0 unmatched -> drop 8 outermost regions -> **236 primary regions** (Source: summary_statistics.json#sample_flow).

**Merge coverage:** all 244 EU27 data regions match a GISCO NUTS 2024 geometry; 0 data regions lack geometry. The 299 boundary units include 55 with no EU27 data (CH, NO, IS, LI, AL, BA, XK and the non-EU27 units that Eurostat reports, e.g. TR, RS, ME, MK); they are unused. No NUTS code recoding was needed. Population for 2024 matches all 236 regions.

**GDP per inhabitant, PPS (EU27 2020), 2024, N = 236:** mean 37,976; SD 14,246; min 16,700 (BG31); p5 20,150; p10 22,750; p25 28,375; median 35,050; p75 44,175; p90 53,550; p95 64,375; max 107,200 (IE06). Max/min ratio 6.4; p90/p10 ratio 2.35. Population-weighted mean 40,077 (the index base of 100); 86 of 236 regions lie above it. Lowest five: BG31, EL41, BG42, BG32, EL54. Highest five: IE06, LU00, IE05, DE60, CZ01. Statistics for `gdp_index` and `ln_gdp_pps` are in the JSON.

**Eurostat flags (primary sample):** 134 provisional, 33 estimated, 69 without flag. Irish regions' very high values reflect multinational profit shifting in GDP; this is a measurement caveat for interpretation, not a data error, and no region was altered or winsorised.

**Spatial weights:** queen contiguity, 1,039 links, mean 4.40 neighbours, maximum 11. Thirteen regions have no shared vertex and are linked to their nearest region by centroid distance (EPSG:3035): Voreio Aigaio (EL41), Notio Aigaio (EL42), Kriti (EL43), Ionia Nisia (EL62), Illes Balears (ES53), Ceuta (ES63), Melilla (ES64), Corse (FRM0), Sicilia (ITG1), Sardegna (ITG2), Kýpros (CY00), Malta (MT00), Åland (FI20); distances are in the JSON (largest: Cyprus to EL42, 646 km). Several of these links (Cyprus, Malta, Sicily, Ceuta) are weak substitutes for adjacency and should be examined in robustness. kNN (k = 5): 1,180 links for the 236 regions; 1,220 links for the 244-region robustness sample that retains the outermost regions. All weights are row-standardised.

**Files for the analysis step:** `spatial_units.csv` (236 rows), `spatial_units_all244.csv` (244 rows), `spatial_weights.csv`, `spatial_weights_knn5.csv`, `spatial_weights_knn5_all244.csv`, and figure specs for a quintile map and a histogram.

**Provenance queries:** `SELECT time, unit, COUNT(*), COUNT(value), COUNT(DISTINCT geo) FROM gdp_pps_nuts2 GROUP BY time, unit`; anti-joins of 2024 `geo` against `nuts2_boundaries.nuts_id` in both directions (0 data regions unmatched; 23 boundary units without 2024 data, all non-EU27); country prefix counts of the 2024 slice.
