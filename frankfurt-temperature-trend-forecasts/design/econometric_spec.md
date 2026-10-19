# Econometric specification: monthly 2 m air temperature, Frankfurt am Main (NASA POWER)

Claim type: descriptive and predictive. Trend estimates are associations with calendar time, not causal effects. No identification strategy.

## Data and sample
- Table `frankfurt_t2m_monthly` (data.db): 540 monthly values, 1981-01 to 2025-12 (POWER monthly load covers whole years, hence the end in 2025-12). Unit: degrees C.
- Training window 1981-01 to 2022-12 (504 months). Frozen hold-out 2023-01 to 2025-12 (36 months). Forecast beyond the data: 2026-01 to 2028-12, from models refitted on all 540 months (own model entries, not evaluated).
- No transformation. No missing values expected (verified in the script). Sample flow: 540 raw -> 504 train + 36 hold-out.
- The optional ML model and the DWD station comparison are dropped (researcher decision); the station comparison is future work.

## Trend estimation (association)
1. Annual means 1981-2022 (training) and 1981-2025 (full): OLS of annual T2M on year, Newey-West (HAC) standard errors, bandwidth L = floor(4 (T/100)^(2/9)); slope in degrees C per decade.
2. Deseasonalised monthly series: subtract month-of-year means (estimated on the sample used), OLS on a time index (years), HAC errors with lag floor(4 (T/100)^(2/9)) and a longer-lag check (24). Reported for training and full samples.
3. Season-specific trends (DJF, MAM, JJA, SON) from seasonal means with HAC errors.
4. Mann-Kendall with Sen's slope on training annual means, plus a Hamed-Rao-style autocorrelation-corrected variant.

## Diagnostics (training periods only, sample_end 2022-12)
KPSS (level) and ADF (constant, AIC lag) on the seasonally adjusted training series; Mann-Kendall as above.

## Models (fit on training window only, fixed origin 2022-12)
- Baselines: seasonal naive (lag 12; interval from seasonal-lag difference sd scaled by sqrt(number of cycles ahead)), naive (random-walk interval).
- ETS(A,N,A) and ETS(A,Ad,A) (statsmodels ETSModel; additive error, seasonal 12), SARIMA(p,d,q)(P,D,Q)[12] chosen by AICc on the training window (p,q<=3; P,Q<=2; d,D in {0,1}), harmonic trend regression (linear trend plus K=1..4 annual harmonics, K by AICc, OLS normal intervals).
- Model selection only by AICc / training information; never by hold-out error.

## Evaluation
- Hold-out RMSE, MAE, MASE (scale: in-sample seasonal-naive MAE, lag 12, on training), by horizon 1..36 (error table by horizon and by 12-month blocks), and 95% interval coverage.
- Diebold-Mariano test vs seasonal naive on hold-out loss differentials (squared and absolute error), with Harvey-Leybourne-Newbold correction, t(n-1) reference. Two-sided; 36 overlapping multi-step errors give low power (stated).
- Supplementary rolling origins (annual origins 2000-12 to 2019-12, 36-month horizon, inside training) for the harmonic, ETS and seasonal naive models to report horizon/season skill relative to seasonal naive.

## Robustness
HAC lag sensitivity; trend on training vs full sample; coverage vs nominal; seeds fixed (no randomness in estimators).

## Pre-registered hypotheses (preregistration.lock.json) and where they are tested
Results are in `estimation_results.json` under the top-level dictionaries `h1_result`, `h2_result` and `h3_result`, each with a `hypothesis` field.
- H1 (positive annual trend, about +0.3 to +0.5 C/decade): OLS with Newey-West errors on annual means 1981-2022 (n = 42). Realized: +0.50 C/decade (HAC se 0.083), positive, at the upper edge of the prior range; an association with calendar time, not a causal effect.
- H2 (trend/level-adjusted models beat seasonal naive at long horizons, MASE about 0.75 to 0.95): hold-out RMSE/MASE ratios and rolling-origin relative RMSE at horizons 25-36, with DM tests vs seasonal naive. Realized: all four non-naive models beat seasonal naive (hold-out MASE 0.48 to 0.50 against 0.80 for seasonal naive; DM p between 0.009 and 0.037). The direction holds, but the gain is larger than the pre-registered "modest" range, and the pre-registered MASE range is not met.
- H3 (ETS/SARIMA do not clearly beat the harmonic regression; DM often insignificant): pairwise DM (squared error, HLN, h = 12) of each of ETS(A,N,A), ETS(A,Ad,A), SARIMA against harmonic_trend. Realized: 0 of 3 pairs significant at 5% (p = 0.19, 0.18, 0.91); supported, with low power on 36 months.

## Output
`estimation_results.json` (result_kind "timeseries"): series, diagnostics, models, forecasts, out_of_sample (with predictions), plus extra blocks `trend`, `dm_tests`, `horizon_errors`, `rolling_origin`. All numbers computed in `run_estimation.py`.
