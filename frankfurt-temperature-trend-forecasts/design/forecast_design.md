# Forecast Design: Monthly Mean 2 m Air Temperature, Frankfurt am Main (NASA POWER)

Frozen before any model is fitted. Wording may change after the freeze; hold-out, horizon, interval level, models and diagnostics may not.

## Target and data
- Table `frankfurt_t2m_monthly` (columns `date`, `T2M`): 540 monthly values, 1981-01 to 2025-12, no missing values, no repeated periods. Unit: degrees C. Seasonal period 12. No transformation (temperature in degrees C can be negative, and the seasonal amplitude is additive).
- The derived tables `frankfurt_t2m_clean` and `frankfurt_t2m_annual` carry a `split` flag that agrees with this design (train through 2022-12, hold-out 2023-01 to 2025-12). The climatology column `clim_1981_2010` and the `anomaly` column are for description only; models and diagnostics use `T2M` and training-window statistics.

## Hold-out and training window
- Hold-out: the last 36 months, 2023-01 to 2025-12 (n = 36). Training: 1981-01 to 2022-12 (504 months, 42 full years).
- Why 36: it equals the 36-month horizon requested in the research question and gives three complete seasonal cycles. It was set by the horizon and the seasonality, not by how any model does on it.
- Limitation: 36 months at a single origin is a short hold-out. Monthly anomalies have a standard deviation near 1.5 to 2 degrees C, so tests of equal accuracy have little power. A single origin also covers one realisation of 2023 to 2025 (a very warm period). The paper must say this.

## Evaluation scheme
- **Primary (frozen, checked): single fixed origin.** All models are fitted on 1981-01 to 2022-12 and forecast 2023-01 to 2025-12 (horizons 1 to 36). Every `out_of_sample` entry covers exactly these 36 periods.
- **Supplementary: rolling origin inside the training window only** (Tashman 2000). Origins every 12 months from 2000-12 to 2019-12 (initial window of at least 20 years), each forecasting 36 months ahead, with the last origin's targets ending 2022-12. It is used to choose between model specifications (orders, components) and to report horizon-specific skill (h = 1 to 36) and skill by target season, without touching the hold-out. A rolling origin through the hold-out is not part of the frozen design; if reported, it is labelled exploratory.
- Model selection (ETS components, SARIMA orders, number of harmonics) by AICc on the training window, with rolling-origin RMSE as a tie-break. Never by hold-out error.

## Horizon and intervals
- Hold-out forecasts: horizons 1 to 36 from the origin 2022-12.
- Forecast beyond the data: 36 months ahead, 2026-01 to 2028-12, from models refitted on all 540 months (own `models` entry; not evaluated on the hold-out). The declared `horizon` in the setup is 36.
- Interval level 0.95. Model-based intervals for ETS, SARIMA and the regression. For the seasonal naive baseline, intervals from the seasonal-lag residual standard deviation, widened with the horizon by the number of seasonal cycles (Hyndman and Athanasopoulos, ch. 5.5). A residual-bootstrap interval is reported as a sensitivity check. Empirical coverage on the 36 hold-out values is reported for each model; a coverage far from 95% is reported as such.

## Baselines
- `seasonal_naive`: value 12 months earlier. The main benchmark.
- `naive`: last value. A weak reference: it ignores the seasonal cycle.
- `mean` is not included: the seasonal naive and naive baselines bracket what a no-model user does.

## Candidates
1. `ets_ana`: ETS(A,N,A), additive Holt-Winters without trend. Temperatures are additive, so no multiplicative form.
2. `ets_aada`: ETS(A,Ad,A) with damped trend, to see whether a trend term helps in exponential smoothing. The component set is chosen by AICc on the training window among {ANA, AAdA}; both are fitted and reported.
3. `sarima`: seasonal ARIMA(p,d,q)(P,D,Q)[12], orders chosen on the training window by AICc over a stated grid (p,q up to 3; P,Q up to 2; d in {0,1}; D in {0,1}), with a drift allowed when d + D = 1.
4. `harmonic_trend`: harmonic regression with a linear trend: T2M_t = a + b·t + sum_{k=1..K} [c_k sin(2π k t/12) + d_k cos(2π k t/12)] + e_t, K chosen by AICc (K = 1 to 4; K = 6 equals full monthly dummies). Errors: OLS with normal intervals, with an AR(1) error alternative reported if residuals are autocorrelated (Ljung-Box).

No machine-learning model is in the frozen design. The paper plan mentions one as optional; adding it later would change the frozen setup.

## Diagnostics (training periods only, `sample_end` 2022-12)
- `kpss_level` (stationarity): KPSS (level) on the seasonally adjusted training series (monthly means removed).
- `adf_seasonally_adjusted` (stationarity): ADF (null: unit root), lag by AIC, constant, on the same series. Read together with KPSS: agreement is informative, disagreement points to trend-stationary or near-unit-root behaviour.
- `mann_kendall_annual` (trend): Mann-Kendall with Sen's slope on the annual means of 1981 to 2022 (42 years). Autocorrelation is checked (lag-1 correlation of detrended annual means); if present, a variance-corrected version (Hamed and Rao) is reported next to the plain one.
- Season-specific trends (RQ1): Mann-Kendall with Sen's slope per calendar month and per season on training years. These are descriptive and are reported with a multiplicity note; they are not setup diagnostics.

## Accuracy metrics and comparison
- RMSE and MAE on the hold-out in degrees C; MASE = hold-out MAE divided by the in-sample MAE of the seasonal naive method on the training window (lag 12, Hyndman and Koehler 2006). A relative RMSE against seasonal naive is also given. MAPE is not used.
- Diebold-Mariano test of each candidate against `seasonal_naive` on the hold-out loss differences, squared-error and absolute-error loss, with the Harvey-Leybourne-Newbold small-sample correction, using h-step autocovariance truncation consistent with the horizon (the loss differences of a single-origin multi-horizon forecast are strongly serially dependent, so the bandwidth is stated). Two-sided at 5%. The comparison is stated to have little power with 36 observations. DM statistics from rolling-origin errors are given by horizon bucket (1 to 12, 13 to 24, 25 to 36) as supporting evidence.
- Claims of "better than seasonal naive" need both a lower error and a DM rejection; otherwise the paper writes "no detectable difference".

## What is expected (stated before seeing results)
- Trend-bearing models (harmonic_trend, SARIMA with drift) should have lower RMSE than seasonal naive, because seasonal naive carries the noise of a single year while the others average over 42 years. The gain may be small relative to the noise, and the DM test may not reject. Seasonal naive may do relatively better at short horizons only if anomalies persist, which for monthly temperature they hardly do beyond one or two months. If seasonal naive is not beaten significantly, that is a result.

## What would change the plan (before the freeze only)
- If the check shows a gap or a repeated period in the series, the hold-out would be reset.
- If researcher approval requests a longer hold-out (for example 48 months), it would move before freeze. After freeze nothing in the setup changes; deviations are recorded in the analysis as additional, labelled exploratory entries.

## Leakage guardrails for the analysis specialist
- Seasonal means, trend, detrending, scaling, order selection and every diagnostic use 1981-01 to 2022-12 only.
- The hold-out is evaluated once per frozen model. The full-series refit is used only for the 2026 to 2028 forecast.
- Set seeds for bootstrap procedures; record software versions in the script.

## Handoff
`forecast_design.json` holds the machine-readable setup for the `forecast_design` check. Keys for `models`, `out_of_sample` and `diagnostics` in the results file use the names given there.
