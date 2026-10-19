# Data Summary: Monthly 2 m air temperature, Frankfurt am Main (NASA POWER), 1981-2025

Scope: loading, cleaning and description only. No trend tests, models, forecasts or test statistics are computed here. Numbers below are cited from `summary_statistics.json`.

## Source and tables

- Source: NASA POWER Monthly and Annual API v2.10.0 (MERRA-2 reanalysis, grid-cell estimate, 0.5 deg lat x 0.625 deg lon; not a station record), community RE, accessed 2026-10-13. Point 50.11 N, 8.68 E (grid elevation 171.61 m). Citation: `\cite{NASA_POWER}`; the loader's data reference is recorded in `data_sources.json`.
- Declared table `frankfurt_t2m_monthly` (raw, never overwritten): **540 rows**, 1981-01 to 2025-12, columns lat, lon, elevation_m, year, month, date, T2M.
- Derived table `frankfurt_t2m_clean` (built by `clean_describe.py`): same 540 months plus clim_1981_2010, anomaly, split.
- Derived table `frankfurt_t2m_annual`: annual means computed from the 12 monthly values (45 rows).

## Sample construction (sample flow)

1. Raw monthly API request, 1981-2025: 540 monthly rows were returned in `frankfurt_t2m_monthly` (45 years x 12). No month-13 row is present in the loaded table (the loader keeps months 1-12 only); month 13 is POWER's annual mean and is not an observation of the monthly series. Annual means used here are recomputed from the monthly values, so the monthly series and the annual series are consistent.
2. Fill codes: POWER's -999 fill value: 0 rows. Missing (NULL) T2M: 0 of 540.
3. Duplicates in date: 0. Gaps in the 1981-01..2025-12 calendar: 0.
4. Final analysis sample: 540 months, 504 training (1981-01 to 2022-12) and 36 hold-out (2023-01 to 2025-12). No observations dropped, no imputation.

## Variables

- T2M: monthly mean air temperature at 2 m, degrees C.
- clim_1981_2010: mean of T2M per calendar month over 1981-2010 (30 values per month), inside the training period.
- anomaly = T2M - clim_1981_2010 (same calendar month).
- Annual means: arithmetic mean of 12 monthly values per year. 2023-2025 lie in the hold-out and are shown for description only; all training-period summaries are marked as such.

## Descriptives, climatology, figures

Full-sample and training-sample summary statistics, the 12-month climatology (1981-2010 and 1981-2022), annual means and decade means are in `summary_statistics.json`. Figure specs (`figure_spec.json`): monthly time series with the hold-out shaded, seasonal profile (climatology), annual means, and monthly anomalies. Each figure carries a `source` pointing to a data.db table.

## Realized values (from `summary_statistics.json`)

- Completeness: 540 of 540 months present, 0 missing, 0 fill values, 0 month-13 rows in the loaded table, 0 calendar gaps, 45 complete years.
- Full sample T2M: mean 9.94 C, SD 7.54, min -7.03 (training and full), max 24.67. Training (504 months) mean 9.83 C.
- Decade means of annual T2M: 1981-90 9.09; 1991-2000 9.55; 2001-10 9.87; 2011-20 10.62; 2021-25 11.19 C (descriptive only).
- Climatology 1981-2010: January -0.54 C, July 20.11 C (coldest and warmest months).

## Caveats

- Modelled grid-cell values smooth urban heat and local extremes; one cell only.
- POWER revises data between versions; rerun results may differ slightly.
- The hold-out (2023-2025) is described in the file but must not inform any model choice.
- Mention to the researcher: POWER asks to be notified of publications using its data (larc-power-project@mail.nasa.gov); nothing is sent by this pipeline.
