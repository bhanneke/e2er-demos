# Paper Plan: Monthly Mean 2 m Air Temperature in Frankfurt am Main, 1981 to Present: Trend, Seasonality, and 36-Month-Ahead Forecast Skill

Paper ID: ad0dbdfc-655c-424a-bd3a-e01575743567 | Template: Time series and forecasting | Stage: idea -> data/forecast design
Claim type: descriptive and predictive only. No causal claims; no identification strategy.

## 1. Phenomenon and motivation (Step 0)

**Phenomenon.** Central European winters and summers have warmed visibly since the 1980s. Frankfurt am Main recorded some of Germany's highest temperatures in recent summers, and the Rhine-Main region is a recognised urban heat hotspot. Yet month-to-month temperature is dominated by a strong, nearly deterministic annual cycle plus large irregular anomalies. A forecaster therefore faces a concrete puzzle: at horizons of 1 to 36 months, does anything beat "same month last year" (seasonal naive)? Or does a warming trend add only a small, hard-to-detect gain against noise of roughly 1.5 to 2 °C in monthly anomalies?

**Why it needs explaining.** Trend-adjusted climatology is a known benchmark, but many users (utilities, municipal heat planning, energy demand, agriculture) use last-year or recent-average heuristics. The size of the forecast gain from modelling the trend is an empirical question that depends on the signal-to-noise ratio at a single grid cell.

**Who cares.** Applied forecasters and planners get a calibrated statement of how much skill a simple statistical model adds at a 3-year horizon. Climate-statistics readers get a transparent, reproducible local trend estimate with honest uncertainty. A reverse insight is also possible: if no model significantly beats seasonal naive, that tells us the trend is too small relative to interannual variability to be exploited at this horizon.

**Honest positioning.** This is a modest, applied descriptive-plus-forecast-evaluation paper (target: applied or regional climate and statistics outlets such as *Theoretical and Applied Climatology*, *Meteorologische Zeitschrift*, *International Journal of Forecasting* (applications), *Weather and Climate Extremes* or a data-science venue). It is not a top-5 contribution; the contribution is careful, reproducible out-of-sample evaluation.

## 2. Research questions

- **RQ1 (descriptive).** How has the monthly mean T2M in Frankfurt changed since 1981: overall trend, season-specific trends, and change in the amplitude and phase of the seasonal cycle?
- **RQ2 (predictive).** Over a 36-month hold-out and in rolling-origin evaluation, do ETS, seasonal ARIMA, trend-plus-harmonics regression (and optionally an ML model) beat the seasonal naive baseline in MAE, RMSE and MASE, and are differences statistically significant (Diebold-Mariano)?
- **RQ3 (horizon structure).** How does relative skill vary with horizon (1 to 36 months) and with target season?

Pre-specified expectations (stated before seeing results; not to be revised after):
- H1: the linear trend in annual mean T2M is positive, on the order of +0.3 to +0.5 °C/decade (prior from regional literature; the estimate itself is data-driven).
- H2: models with an explicit trend or level adjustment beat seasonal naive on RMSE at long horizons mainly because seasonal naive carries one year of noise; averaging over many years in the seasonal component reduces variance. Gains are modest (MASE about 0.75 to 0.95).
- H3: ETS and SARIMA with unconstrained adaptive level will not clearly beat the harmonic regression; DM tests will often be insignificant for pairs among the non-naive models.

These are hypotheses, not a search target; all models and specifications attempted will be reported.

## 3. Closest literature (to be verified by literature_reviewer; citations to be checked, not assumed)

| Area | Reference (to verify) | Relevance and limitation |
|---|---|---|
| Forecast methodology | Hyndman and Athanasopoulos, *Forecasting: Principles and Practice* (3rd ed.); Hyndman and Khandakar (2008, JSS), auto.arima / ETS | Model classes and selection. Not climate specific. |
| Accuracy measures | Hyndman and Koehler (2006, IJF), MASE | Scaled metric used here. |
| Forecast comparison | Diebold and Mariano (1995, JBES); Harvey, Leybourne and Newbold (1997, IJF) small-sample correction | Test of equal predictive accuracy; DM is for forecasts, not nested model inference (Clark and West caveat for nested models). |
| Rolling evaluation | Tashman (2000, IJF), out-of-sample tests; Bergmeir and Benitez (2012) on CV for time series | Rolling origin / time-series CV. |
| Data product | Stackhouse et al., NASA POWER; MERRA-2 (Gelaro et al. 2017) reanalysis underlying T2M | T2M is reanalysis-based (about 0.5 x 0.625 degree grid), not a station observation; this is a key caveat. |
| Local climate | DWD station Frankfurt/Main records; DWD climate reports for Hesse | Benchmark for trend magnitude; use as external plausibility check if retrievable. |
| Climate trend methods | Sen (1968) slope; Mann-Kendall; Cleveland et al. (1990) STL; Wilks, *Statistical Methods in the Atmospheric Sciences* | Descriptive trend estimation under autocorrelation. |
| Seasonal climate prediction | ECMWF SEAS5 / Copernicus C3S multi-system seasonal forecasts (6 to 7 months); decadal prediction literature (e.g., Smith et al. 2019, Boer et al. 2016 DCPP) | Dynamical systems reach 6 to 13 months (seasonal) or years (decadal); our statistical models are a benchmark, not a competitor. |

Contribution matrix (condensed): vs. generic forecasting texts, we apply a full rolling-origin plus DM protocol to a long climate series with a documented seasonal naive benchmark; vs. dynamical seasonal/decadal prediction, we provide a transparent statistical baseline at 36 months; vs. local climate reports, we give season-resolved trends with autocorrelation-robust intervals. Contribution type: quantification and a new-setting evaluation. Stress test: the derivative-answer risk is real (readers expect trend models to do slightly better than seasonal naive). The paper is worth writing only if it quantifies how much, at which horizons and seasons, and whether it is significant. We state this limitation openly.

## 4. Data

- **Source:** NASA POWER (Prediction Of Worldwide Energy Resources), monthly API, parameter T2M (MERRA-2 derived, °C), point 50.11 N, 8.68 E, community RE or AG, 1981-01 onward. Use the latest *complete* month at retrieval date (as of 2026-10-13 likely 2026-09; confirm API availability lag and record the retrieval date and API version).
- **Variables:** monthly mean T2M (°C). Optionally T2M_MAX / T2M_MIN as descriptive extras only if cheap; not needed.
- **Data cleaning rules (document):** treat the POWER fill value (-999) as missing; check for gaps, duplicates, and the annual-mean row ("13" month key) which must be dropped; confirm 12 x N rows; no imputation unless gaps are isolated (then linear/seasonal interpolation with a flag and a sensitivity run without).
- **Sample size:** about 1981-01 to 2026-09, around 549 months. 36-month hold-out leaves about 513 for the initial training.
- **Caveats to state:** grid-cell reanalysis, not a thermometer; reanalysis may have inhomogeneities due to changing assimilated observing systems (flag as a data_reviewer item); monthly means are not homogenised; urban-heat-island effects at point scale are not represented at grid resolution. Optional validation: compare with DWD Frankfurt station monthly means (CDC open data) for 1981 to 2025 if accessible (correlation, bias, trend difference). Report as robustness only.
- **Reproducibility:** save raw API JSON, a cleaned CSV, and a hash and retrieval timestamp.

## 5. Descriptive analysis (no causal claims; data_analyst)

1. Summary statistics: monthly mean by calendar month, SD, min/max; annual means by year.
2. Time series plot, seasonal subseries (month plot), annual-mean plot with LOESS, heatmap of year x month anomalies (anomalies relative to 1981-2010 or 1991-2020 climatology; state the choice, report both).
3. **Trend:** OLS linear trend on annual means with HAC (Newey-West) or AR(1)-adjusted standard errors; Theil-Sen slope with Mann-Kendall test (with Hamed-Rao or pre-whitening correction for autocorrelation); season-resolved trends (DJF, MAM, JJA, SON) and by calendar month, with multiplicity noted (12 months; report Holm-adjusted p-values as secondary). Decade means (1981-90 ... 2011-20, 2021-present partial).
4. **Seasonality:** STL decomposition (robust, seasonal window = periodic and sensitivity); strength-of-trend and strength-of-seasonality (Wang, Smith and Hyndman 2006); harmonic regression of the annual cycle with sub-period comparison (1981-2003 vs 2004-present, split fixed in advance as the midpoint, not chosen from the data) to describe changes in amplitude and phase.
5. **Diagnostics:** ACF/PACF of deseasonalised anomalies, Ljung-Box, ADF/KPSS on anomalies and on annual means (note low power; trends confound unit root tests), Chow-type or CUSUM check for level shifts reported descriptively as "pattern", not as cause.
6. Interpretation language: "associated with", "pattern", never "caused by".

## 6. Forecast design (forecast_designer; frozen after the check)

- **Target:** monthly mean T2M level (°C), horizons h = 1, ..., 36.
- **Final hold-out:** last 36 complete months of the sample (e.g., 2023-10 to 2026-09 if data run through 2026-09; exact dates fixed at data retrieval and written into the frozen design). Training set: all months before. Models fitted once on the training set for the fixed-origin test; point forecasts for h = 1..36 from the single origin.
- **Rolling-origin evaluation (primary evidence, since a single 36-month window is one realisation):** expanding window, first origin after a minimum 20 years (240 months; i.e., around 2001-01), origins stepped every 12 months (annual, seasonally aligned) as primary and every 1 month as a robustness run; each origin produces 1..36 step forecasts; last origin has full 36 months of subsequent actuals. Sliding-window (fixed 25-year training length) as robustness to check parameter drift. All origin information sets contain only data up to the origin (no leakage; model order selection re-done within each origin, or fixed in advance, both reported).
- **Note on overlap:** forecast errors at neighbouring origins overlap and are serially correlated; DM uses HAC variance with truncation lag h-1 at least, plus the HLN correction.

### Candidate models
1. **Seasonal naive (benchmark):** y_hat(t+h) = y(t+h-12*ceil(h/12)), i.e., the same calendar month from the most recent observed year.
2. **Climatological mean (seasonal mean) benchmark, extra:** calendar-month mean of all training years (no trend). Included as a second reference since it removes the single-year noise of seasonal naive; also report a seasonal mean over the last 30 years.
3. **ETS:** ETS(A,A_d?,A) family selected by AICc within each training window (error, trend, damped trend, seasonal; additive seasonal only since temperatures in °C may be negative or near zero; no multiplicative). Also with a restricted version ETS(A,N,A) as a pre-specified variant.
4. **Seasonal ARIMA:** SARIMA(p,d,q)(P,D,Q)_12 by AICc search (auto.arima style with stepwise = FALSE), with constraints d <= 1, D <= 1; plus a pre-specified airline-style benchmark SARIMA(0,1,1)(0,1,1)_12. Also ARIMA with Fourier terms and a drift (regression with ARIMA errors) as the better-posed variant for long seasonal period.
5. **Trend-plus-harmonics regression:** y_t = a + b*t + sum_{k=1}^{K}[ c_k sin(2*pi*k*t/12) + d_k cos(2*pi*k*t/12) ] + e_t, K = 2 pre-specified (K in {1,2,3} compared by AICc and rolling-origin errors as sensitivity). AR(1)/ARMA errors for the inference version; forecasts from OLS or GLS. Variant with an interaction of the trend with the first harmonic (season-specific trend). Forecast intervals via residual bootstrap, point forecasts evaluated.
6. **Optional ML / Prophet-style:** (a) Prophet-style additive model (piecewise-linear trend, yearly Fourier seasonality) - implement as in the Prophet package or the equivalent decomposable model; (b) gradient-boosted trees or random forest on lagged values, calendar month, and time index, direct multi-horizon (one model per h or horizon as a feature). ML models are included only as comparators, with a hyperparameter grid fixed in advance and tuned inside the training window by time-ordered validation. Trees cannot extrapolate a trend; this is a known limitation to be stated and tested by detrending first.
7. **Optional combination:** simple average of ETS, SARIMA and harmonic regression (forecast combination, often hard to beat).

No other models are added after the freeze. All models attempted are reported.

### Error metrics
- MAE and RMSE per horizon, per horizon-block (1-12, 13-24, 25-36), and per target season.
- **MASE** relative to seasonal naive: scaled by in-sample (training) seasonal-naive one-year-ahead MAE (Hyndman-Koehler seasonal scaling, m = 12), so MASE < 1 means better than the in-sample seasonal naive. Additionally report the **relative MAE / RMSE ratio vs. seasonal naive (out-of-sample)** (e.g., the Hyndman and Koehler relative measures), since the work order frames the benchmark as seasonal naive; and state which is called "MASE relative to seasonal naive" in the tables (the scaled MASE and the ratio are reported separately and not conflated).
- Bias (mean error) per horizon to separate the trend-capture problem from the variance problem.
- Optional: a skill score 1 - MSE_model / MSE_snaive; prediction interval coverage and the interval score for models giving intervals (secondary).

### Statistical comparison
- **Diebold-Mariano** with squared-error and absolute-error loss, for each model vs. seasonal naive, at horizon-specific level (h = 1, 12, 24, 36) and pooled over 1..36 (loss differentials averaged by origin); HAC variance (Newey-West, bandwidth at least h-1) with Harvey-Leybourne-Newbold small-sample correction and t(n-1) critical values; one-sided and two-sided versions reported.
- For the single fixed 36-month hold-out, DM with the 36 forecasts is indicative only (few independent observations; flag explicitly). The rolling-origin DM provides the main inference.
- Nested comparison caveat: when the model nests the benchmark (e.g., harmonic regression vs. seasonal-mean), complement with the Clark-West test or state the limitation.
- Multiple testing: 5 to 7 models x several horizons; report raw p-values and a Holm-adjusted set; optionally Model Confidence Set (Hansen, Lunde and Nason 2011) as an additional summary.
- Seasonal heterogeneity: DM within each target season, labelled exploratory.

### Expected pitfalls to pre-handle
- A 2023-2026 hold-out may include unusually warm months (record anomalies); the fixed-origin result may be unrepresentative, hence the rolling-origin evidence is primary.
- Trend extrapolation vs. damped trend: report both.
- Reanalysis changes (e.g., MERRA-2 stream changes) could produce spurious breaks; add a sensitivity analysis that estimates models from 1991 onward.

## 7. Analysis outputs (econometrics_specialist)

Writes `estimation_results.json` in the time-series results schema: descriptive trend estimates (slope, HAC SE, CI, Mann-Kendall / Sen), seasonal-decomposition summary, model specifications and AICc/selected orders, fixed-origin forecasts and errors, rolling-origin error tables by horizon and season, MASE and ratios, DM statistics with p-values (raw and Holm-adjusted), and robustness runs. No regression beyond the planned ones.

Figures: (1) series with trend; (2) month x year heatmap; (3) seasonal subseries; (4) STL components; (5) hold-out forecasts vs. actuals for each model; (6) error by horizon (RMSE and MASE) with rolling-origin bands; (7) DM p-value heat map by model and horizon. Tables: summary statistics; trend by season; model list; accuracy tables; DM table.

## 8. Specialist dispatch plan

Order: `data_analyst` -> `forecast_designer` -> (forecast_design check) -> `econometrics_specialist` -> (forecast_evaluation check) -> literature work and `paper_drafter`.
- `data_analyst`: retrieve and clean POWER data, descriptive analysis (Section 5), data-quality notes, optional DWD validation.
- `forecast_designer`: freeze Section 6 (hold-out dates, origins, models, metrics, tests) in the forecast-design artifact. Do not dispatch again afterwards.
- `econometrics_specialist`: run all models and tests, write `estimation_results.json`.
- `literature_reviewer` (before the draft, since paper_drafter reads it): verify the citations in Section 3, add recent work on statistical vs. dynamical seasonal and decadal temperature prediction and on reanalysis point-extraction caveats.
- Not dispatched: `identification_strategist`, `theory_specialist` (no causal or theoretical component).
- Review panel after drafting: technical, literature, writing, data, methods, plausibility reviewers. Anticipated reviewer attack points: (i) reanalysis vs. station data; (ii) single hold-out window; (iii) overlapping rolling errors and DM validity; (iv) derivative finding.

## 9. Scoring (framework)

Data availability 5; Identification not applicable (descriptive; treated as 5 for the formula since no causal claim); Novelty 2; Importance 2; Feasibility 5. Overall: a feasible, low-risk, low-novelty applied paper; value rests on execution quality and honest framing of null or modest results.

## 10. Risks and mitigation

| Risk | Mitigation |
|---|---|
| API outage or schema change | Cache raw JSON; fall back to the POWER CSV endpoint; record the retrieval date |
| Latest month incomplete | Cut at the latest complete month; freeze the date in the design |
| Seasonal naive not beaten | Report as a finding (reverse insight), not a failure |
| Model overfitting through selection | Re-select inside each origin; compare with fixed pre-specified specs |
| Over-claiming from trends | Language rule: pattern and association only; no attribution to climate forcing beyond citing the literature as context |
| Multiple comparisons | Holm adjustment, MCS, and clear primary vs. exploratory labelling |

## 11. Handoff

Primary artifacts expected next: cleaned monthly CSV and descriptive tables (data_analyst); frozen forecast design with exact dates (forecast_designer). Open decisions for the forecast_designer: exact hold-out dates after the retrieval of the latest complete month; whether annual-step or monthly-step rolling origins are primary (plan default: annual step primary, monthly robustness); the climatology reference period (plan default: report both 1981-2010 and 1991-2020).
