# Replication package: monthly 2 m air temperature in Frankfurt am Main, 1981-2025

Paper ID: ad0dbdfc-655c-424a-bd3a-e01575743567. Descriptive and predictive analysis only: trends are associations with calendar time, not causal effects.

## 1. Data requirements

- `data/frankfurt_t2m_monthly.csv` (540 rows, columns `lat, lon, elevation_m, year, month, date, T2M`), the NASA POWER Monthly and Annual API v2.10.0 (MERRA-2 reanalysis, community RE), point 50.11 N, 8.68 E, parameter T2M, years 1981-2025. The data end in 2025-12 because the POWER monthly load covers whole years. Month 13 (POWER's annual mean) is excluded.
- Fallback: table `frankfurt_t2m_monthly` in `data.db`, which the script uses if the CSV is missing.
- The data are not included in this package. `replication/data_queries.sql` lists the queries run against the local warehouse; no Allium tables are used (the series is not blockchain data).
- The DWD station comparison and the optional ML model were dropped by researcher decision; the station comparison is future work.

## 2. Environment

Python 3.10+ with pinned minimum versions (use the versions recorded in `output/estimation_results.json` under `software` for exact reproduction):

```
pip install "numpy>=1.26" "pandas>=2.1" "scipy>=1.11" "statsmodels>=0.14" "matplotlib>=3.8"
```

## 3. Steps

1. Place the data file at `data/frankfurt_t2m_monthly.csv` (or keep `data.db` in the workspace root).
2. Run `python replication/estimation.py` from any directory. The script runs in a few minutes; most time goes to the stepwise SARIMA search and the 20 rolling origins.
3. Read the outputs in `replication/output/`.

The script runs in this order: load and check (540 rows, no gaps, 504 training + 36 hold-out); diagnostics on the training window (KPSS, ADF, Mann-Kendall); trend regressions (OLS with Newey-West errors; annual, deseasonalised monthly, seasonal, amplitude/phase drift); model selection by AICc on the training window only; fixed-origin hold-out evaluation (origin 2022-12) with Diebold-Mariano tests (Harvey-Leybourne-Newbold correction); rolling-origin evaluation inside the training window; refit on all 540 months and forecast 2026-01 to 2028-12; export. All standard errors are heteroskedasticity- and autocorrelation-robust (Newey-West, lag floor(4(T/100)^(2/9))), as in `econometric_spec.md`. No estimator is stochastic; `numpy.random.seed(42)` is set anyway.

## 4. Output map

| Paper item | File in `replication/output/` |
|---|---|
| Table 1, summary statistics | `table1_summary.csv` |
| Table 2, trends (annual, deseasonalised, seasonal; deg C per decade) | `table2_trends.csv` |
| Amplitude and phase drift of the annual cycle | `table2b_seasonal_cycle_drift.csv` |
| Table 3, stationarity and trend diagnostics | `table3_diagnostics.csv` |
| Table 4, hold-out RMSE, MAE, MASE, coverage, DM tests vs seasonal naive | `table4_holdout_accuracy.csv` |
| Table 5, hold-out error by 12-month horizon block | `table5_holdout_by_horizon_block.csv` |
| Table 6, rolling-origin relative RMSE by horizon block | `table6_rolling_origin_blocks.csv` |
| Table 7, rolling-origin skill by target season | `table7_rolling_origin_seasons.csv` |
| H3, pairwise DM against harmonic trend | `table8_pairwise_dm_vs_harmonic.csv` |
| Forecasts 2026-2028 (not evaluated) | `table9_forecasts_2026_2028.csv` |
| Climatology 1981-2010 (source of Figure 3 bars) | `table10_climatology_1981_2010.csv` |
| Figure 1, monthly series | `fig1_monthly_t2m.png` |
| Figure 2, annual means and trend | `fig2_annual_means.png` |
| Figure 3, seasonal profile | `fig3_seasonal_profile.png` |
| Figure 4, hold-out forecasts | `fig4_holdout_forecasts.png` |
| Figure 5, rolling-origin relative RMSE by horizon | `fig5_relative_rmse_by_horizon.png` |
| All numbers, incl. `h1_result`, `h2_result`, `h3_result` | `estimation_results.json` |

The CSV and PNG files are plain exports; the typeset paper tables and PDF figures were produced by the pipeline from `estimation_results.json`, so layout differs while the numbers agree. `run_estimation.py` in the workspace root is the pipeline's original estimation script; `estimation.py` here reproduces it with a relocatable data path and the exports above.

## 5. Audit trail

- `replication/audit_log.csv`: log of the data and analysis steps recorded by the pipeline.
- `replication/data_queries.sql`: the queries used to read the series from the local data warehouse.

The hold-out (2023-01 to 2025-12) is frozen before any model is fitted; model orders (SARIMA, number of harmonics) are chosen by AICc on 1981-01 to 2022-12 only. Every declared model is reported, including those that do not beat the seasonal naive baseline.

## Status note

The script was assembled from the pipeline's verified `run_estimation.py` but could not be executed in the session that wrote it (no code execution was available). Run it once and compare `output/estimation_results.json` with the workspace `estimation_results.json` before relying on it.
