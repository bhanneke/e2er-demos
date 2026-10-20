# Replication package: Spatial clustering of GDP per inhabitant across EU NUTS-2 regions, 2024

Paper ID: 620f7e1f-43a0-4f27-b982-57099cbbc277. Descriptive spatial analysis; no regression, no causal claim.

**Status:** `estimation.py` was written to reproduce `run_estimation.py` and `build_data.py` (same seed, same order of random draws) but was not executed when this package was assembled (execution was not permitted in that session). Run it once and compare `output/estimation_results.json` with the workspace `estimation_results.json` (queen I = 0.370, kNN-5 0.266, kNN-8 0.265, inverse distance 0.089; LISA uncorrected 19 HH / 38 LL / 2 HL / 3 LH; BH-FDR 1 HH / 20 LL / 1 HL).

## 1. Data requirements
Data files are not included. Place them in `data/` (workspace root):
- `data/gdp_pps_nuts2.csv`: Eurostat `nama_10r_2gdp`, unit `PPS_EU27_2020_HAB`, NUTS 2, 2015-2024 (release 2026-02-10); only 2024 is used.
- `data/pop_nuts2.csv`: Eurostat `demo_r_d2jan`, total population on 1 January 2024 (region size and population-weighted statistics only).
- NUTS 2024 boundaries, GISCO 1:20m, EPSG:3035 (© EuroGeographics): `data/nuts2_boundaries.csv` or, if absent, table `nuts2_boundaries` in `data.db` (columns `nuts_id`, `cntr_code`, `name_latn`, `geometry` as GeoJSON text).

The queries that produced the tables are in `replication/data_queries.sql`. The statistics are computed by the authors from Eurostat data; Eurostat is not responsible for them.

## 2. Environment
`pip install pandas numpy matplotlib` (tested versions to be pinned from the run environment, e.g. `pip freeze > requirements.txt`). Python 3.10+. No geospatial libraries are needed: queen contiguity, centroids and maps are computed from the GeoJSON directly.

## 3. Steps
1. Put the data files in `data/` (or keep `data.db` at the workspace root for the boundaries).
2. Run `python replication/estimation.py`.
3. The script builds the sample (276 raw 2024 rows, minus 32 non-EU27 = 244, minus 8 outermost regions = 236), builds queen, kNN-5, kNN-8 and inverse-distance weights, then computes distribution statistics, global Moran's I (999 permutations, seed 20241014), Moran scatter data, LISA with BH-FDR, Getis-Ord Gi*, sensitivity checks, maps and figures.

Inference is by permutation; no standard errors are involved (no regression is estimated).

## 4. Output map (`replication/output/`)
| Paper item | File |
|---|---|
| Sample flow | `table_sample_flow.csv` |
| Table 1 summary statistics / distribution | `table1_summary.csv`, `table1b_distribution.csv` |
| Table 2 global Moran's I, four weights, level and log | `table2_global_moran.csv` |
| Table 3 LISA counts, by country, by region | `table3b_lisa_counts.csv`, `table3c_lisa_by_country.csv`, `table3_lisa_by_region.csv` |
| Table 4 sensitivity (drop LU, IE, top 5, capitals; demeaned; 244 regions) | `table4_robustness.csv`, `table4b_distribution_sensitivity.csv` |
| Figure 1 map, quintiles | `fig_map_gdp_pps_2024.png` |
| Figure 2 map, EU27 = 100 | `fig_map_gdp_index.png` |
| Figure 3 Moran scatterplot | `fig_moran_scatter.png`, `moran_scatter_data.csv` |
| Figure 4 LISA map | `fig_map_lisa.png` |
| Distribution histogram | `fig_dist_gdp_pps_2024.png` |
| All headline numbers | `estimation_results.json` |

Every map carries the notice "© EuroGeographics for the administrative boundaries". The paper's PDF figures are produced by a separate rendering step from `figure_spec.json`; the PNGs here are equivalent re-draws.

## 5. Audit trail
`replication/audit_log.csv` records the pipeline steps; `replication/data_queries.sql` records the data queries. Notes: the capital-region drop list contains PT17 and PT1A (only codes present in the sample are dropped); the demeaned-GDP Moran's I uses the same permutation null as the raw variable, which is not adapted to demeaned data.
