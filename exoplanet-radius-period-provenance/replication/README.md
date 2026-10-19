# Replication package

Paper: How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance (ID 29deb64e-4eb2-4135-979e-35327f8fd7ec).

Descriptive study: no regression and no causal claim. Uncertainty comes from a percentile bootstrap (2,000 resamples, seed 20261013), so heteroskedasticity-robust standard errors do not apply.

## 1. Data requirements
- `data/planets.csv`: NASA Exoplanet Archive, Planetary Systems Composite Parameters (`pscomppars`, DOI 10.26133/NEA13), 6,445 rows, one per confirmed planet, loaded 2026-10-13. The archive has no releases, so a later download will give different counts. Columns used: `pl_name`, `discoverymethod`, `pl_orbper`, `pl_orbperlim`, `pl_rade`, `pl_radelim`, `pl_rade_reflink`, `pl_bmasse`, `pl_bmassprov`, `tran_flag`.
- Source: TAP service `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`, table `pscomppars`. The load query is in `replication/data_queries.sql`. No Allium tables are used.
- The data file is not included in this package. `pl_controv_flag` is not loaded, so controversial planets are not excluded.

## 2. Environment
`pip install pandas numpy scipy matplotlib` (Python 3.10 or later). Versions used are not pinned in a requirements file. Record the output of `pip freeze` when you run the script.

## 3. Steps
1. Obtain `data/planets.csv` (step 1 above), with `data/` next to `replication/`.
2. Run `python replication/estimation.py`.
3. Read the tables and figures in `replication/output/`.

The script builds `radius_group` (rule: `calculated` if `pl_rade_reflink` contains `CALCULATED_VALUE`; otherwise `measured_transiting` if `tran_flag = 1`, else `measured_non_transiting`; `no_radius` if `pl_rade` is missing). It keeps planets with positive radius and period (6,045 in the load of 2026-10-13), then computes the statistics. `replication/analysis_prep.py` and `run_estimation.py` in the workspace are the original pipeline versions that work on `data.db`. This script reproduces them from the CSV.

## 4. Output map (all files in `replication/output/`)
| Paper item | File |
|---|---|
| Sample flow, data section | `table_sample_flow.csv` |
| Provenance by `tran_flag` / discovery method | `table_group_by_tranflag.csv`, `table_group_by_method.csv` |
| Group shares | `table_groups.csv` |
| Radius and period statistics tables | `table1_summary_by_group.csv` |
| Radius-bin and period-bin counts; hump composition (1,901 of 2,090; 846 of 1,529) | `table_radius_bins.csv`, `table_period_bins.csv`, `table_radius_bin_composition.csv` |
| Joint radius-period cells | `table_joint_cells.csv`, `table_cell_share_differences.csv` |
| Main comparison, calculated vs transit-measured | `table_comparison_main.csv` |
| Robustness: limit-flagged dropped; period ≤ 1000 d | `table_robust_excl_limit_flagged.csv`, `table_robust_period_le_1000d.csv` |
| Association table (Spearman) | `table_associations.csv` |
| Mass provenance of the calculated group | `table_calculated_mass_provenance.csv` |
| Figures 1 to 4 | `fig1_radius_period_all.png`, `fig2_radius_period_by_group.png`, `fig3_marginals_by_group.png`, `fig4_mass_radius_calculated.png` |
| Run summary | `estimation_results_replicated.json` |

Figure files are PNG here; the paper uses PDF versions from the pipeline.

## 5. Audit trail
- `replication/audit_log.csv`: log of pipeline steps and decisions.
- `replication/data_queries.sql`: queries used to load the data.
