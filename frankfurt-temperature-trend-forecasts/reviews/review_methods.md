# Methods Review: Monthly 2 m air temperature, Frankfurt (NASA POWER), trend and 36-month forecast skill

Scope and limits of this review: I reviewed the draft, the econometric specification, the data summary and dictionary, and the plan. `run_estimation.py` and `estimation_results.json` were not in my context, so "computation" findings are based on the specification and on arithmetic cross-checks of numbers quoted in the draft. Where I say "check the script", I could not confirm it.

## Overall assessment

The design is sound in its main structure. The setup is frozen before fitting. Training and hold-out are cleanly separated (504/36). Diagnostics use training data only. Every declared model is reported, including the naive one. Claims are associational, and the reanalysis-versus-station caveat is stated. The quoted numbers I could cross-check are internally consistent:
- Training mean 9.83 and hold-out mean 11.46 combine to the full-sample mean of 9.94.
- MASE scale 2.04 times 0.80 gives MAE 1.64.
- The HAC 95% interval is 0.50 ± 1.96 × 0.083.
- There are 20 annual origins from 2000-12 to 2019-12.

The weaknesses are in inference and interpretation, not arithmetic:
1. The forecast comparison is evaluated against a very weak baseline and with a Diebold–Mariano test that is poorly suited to one origin with 36 horizon-mixed errors.
2. The stationarity interpretation is not supported by the tests that were run.
3. The source of the forecast gain (noise averaging, adaptive level, or trend) is not isolated.
4. The interval comparison is partly an artefact of how the baseline's intervals are built.
5. Several conclusions are stated more strongly than the evidence allows.

## A. What must change

### A1. The forecast gain is not attributed to anything, and the key benchmark is missing
- Section 3.3 and Section 5 say the gain comes from "a slowly moving level or a linear trend" and from a "trend-aware seasonal model". But ETS(A,N,A) has no trend and performs the same as the damped and trend-based models.
- Seasonal naive copies a single year, so it carries one year of noise. A model that averages the seasonal pattern over 42 years wins largely by variance reduction, whether or not any trend is modelled.
- The plan (Section 6, item 2) and the literature review both call for a calendar-month climatology benchmark, with the all-years mean and a last-30-years mean. The frozen design dropped it. Without it, "beats seasonal naive" cannot be split into noise averaging and level/trend capture.
- Fix:
  - Add a seasonal-mean model and a seasonal-mean-plus-drift model as supplementary comparators. Label them post-freeze and exploratory, and do not use them to change any frozen result.
  - Report the bias (mean error) per horizon block for each model. The plan promised this. MSE = bias² + variance would show directly whether the gain in months 25–36 is a level effect.
  - Until then, rewrite "trend-aware" in the Introduction and Discussion. ETS(A,N,A) is not trend-aware.

### A2. Diebold–Mariano test: set-up is not justified, and the p-values are probably too small, not "limited power"
- The 36 hold-out errors come from one origin and run over horizons 1 to 36. They are not 36 draws of an h-step error. The loss differentials share one level shift (the warm 2023–2025 period). They are strongly dependent, heteroscedastic across horizons, and cover only about three seasonal cycles.
- The draft says the limitation is low power. The more likely failure is the opposite: HAC/HLN with h=12 and n=36 can understate the variance of a persistent differential, so p = 0.009 may be anti-conservative. The choice h=12 is arbitrary for horizons 1 to 36 and is not justified.
- Fix:
  - Report the DM statistic under several truncation lags (h = 1, 12, 24, 36), or use a moving-block or year-block bootstrap of the loss differential.
  - Report confidence intervals for the RMSE difference or ratio, not only p-values.
  - Add the Holm-adjusted p-values. By my calculation the four candidates still pass 5%, but only barely. This should be stated.
  - Harmonic trend regression nests the seasonal-mean structure, so state the nested-model caveat (Clark–West) as the plan did.
  - Give the numbers behind "Absolute-error loss gives the same ranking" (a table or a sentence with the statistics).
  - The pre-registered inference was meant to rest mainly on rolling origins. The draft now has no test at all on the rolling exercise, which is the stronger evidence. Add a DM test on the rolling-origin errors (overlap-aware), or say plainly that the only inference is the weak single-origin one.

### A3. Stationarity interpretation (Section 4.1) does not follow from the tests
- KPSS was run in its level form on a series that trends by about 0.5 °C/decade. A level-KPSS rejection is expected under trend stationarity. ADF was run with a constant only.
- "Rejection by both tests points to trend-stationary behaviour" is therefore not established. The usual reading of ADF rejecting together with KPSS rejecting is conflicting evidence, and it needs the trend-augmented versions to resolve.
- Fix:
  - Add ADF and KPSS with constant and trend (`ct`) on the seasonally adjusted training series, as a supplementary diagnostic. The frozen KPSS-level entry stays as it is.
  - State the ADF lag choice and the number of lags actually selected on 504 monthly observations.
  - Soften the sentence until this is done. Do not describe the result as consistent with the trend estimates, because the test result does not discriminate.

### A4. Interval comparison is partly an artefact (Section 4.3, Introduction, Discussion)
- Per the specification, the seasonal naive interval uses the standard deviation of seasonal-lag differences scaled by sqrt(cycles ahead). This is a random-walk-in-the-seasonal-difference assumption. It is wrong for a stationary-anomaly series, so the width inflates with horizon. The resulting 100% coverage and 14.2 °C width follow from this construction, not from the baseline's quality.
- The Discussion draws a practitioner conclusion from it ("intervals about half as wide at comparable coverage"). This is a comparison against a strawman interval.
- Coverage is 100% for the baseline and 35/36 for the candidates. With about three effective independent years and no information on which month was missed, this says almost nothing about calibration.
- Fix:
  - Give seasonal naive a non-inflating interval (sd of one-year differences, with no sqrt(k) factor) as an alternative.
  - Report an interval score (Winkler) or the pinball loss, not only coverage and width.
  - Name the month that fell outside.
  - Remove or heavily qualify the practitioner sentence.

### A5. Duplicate ETS results suggest a degenerate fit
- ETS(A,N,A) and ETS(A,Ad,A) have identical RMSE (1.30), identical DM statistics (2.75) and identical p-values (0.009), and the draft reports "both exponential smoothing variants" with a ratio of 0.68.
- This usually means the damped-trend model collapsed to no trend (beta at 0, or phi at a boundary), or the optimiser hit a local optimum in statsmodels `ETSModel`. In that case there are three distinct candidates, not four.
- Fix: report the fitted smoothing parameters (alpha, beta, gamma, phi), AICc and convergence status for both models. If they coincide, say so in the text and drop "four candidates" from the Introduction and Abstract-level claims.

### A6. The paper's hypotheses are stated more weakly than the pre-registered ones
- Section 3.3 gives H2 as "candidates improve on seasonal naive". The pre-registration says: trend/level-adjusted models beat seasonal naive at long horizons, with MASE about 0.75 to 0.95 and gains "modest". The specification itself states that the MASE range is not met (realised 0.48 to 0.50).
- H3 is phrased in the draft in a different form from the pre-registered one.
- Fix: quote the pre-registered statements verbatim, and say that H2's direction holds but its magnitude is clearly outside the stated range ("support for H2" should become "direction supported, magnitude not as predicted").
- On H1: the point estimate is at the edge of the range. "The lower end of the confidence interval lies inside the stated range" is not an argument for support. Report the unrounded estimate against the 0.5 bound, and drop that sentence.
- On H3: failing to reject with n=36 is not evidence of equivalence. State it as "no detectable difference". Show the RMSE-difference intervals so the reader sees what size of difference the test could have found.

### A7. "The four candidates are statistically indistinguishable" is over-stated
- Only three pairwise tests were run, each against the harmonic regression. ETS versus SARIMA and ETS versus ETS were not tested.
- Fix: either run all pairs, or write "none of the three candidates tested against the harmonic regression differed significantly".

### A8. Selected model specifications and diagnostics are not reported
- The text never reports the chosen SARIMA orders, the number of harmonics K, AICc values, or residual diagnostics (Ljung–Box on the training residuals).
- The paper says "stepwise search in the spirit of Hyndman and Khandakar". The specification describes a search over p,q ≤ 3, P,Q ≤ 2, d,D ∈ {0,1}. State which one was run (a grid or a stepwise search, in Python via statsmodels, not R `auto.arima`).
- The template requires decomposing the training series first (STL or classical). No decomposition is shown. Add a model table and an STL figure, or a seasonal-strength statistic.

### A9. The seasonal naive definition for horizons 13 to 36 must be stated
- "The value twelve months earlier" is ambiguous. The flat block RMSEs (1.92, 1.94, 1.89) imply that the forecast repeats the last observed year (2022) for all three years. That is the right fixed-origin definition, but the text must say it. If the 2023 actuals were used for 2024, the result would be leakage.
- The same applies to the naive forecast (December 2022 repeated). Its RMSE of 12.06 is a trivial result. The paper should not present it as a competitive baseline; one line is enough.

### A10. Rolling-origin exercise is under-described
- It covers only the harmonic, ETS and seasonal naive models (per the specification). SARIMA is absent, but the text says "the candidate models reach MASE values between 0.71 and 0.73" without saying which.
- State whether K, ETS form and the SARIMA orders were re-selected at each origin. If K was taken from the full training window, then origins before 2022 use information from after the origin.
- The rolling-origin sample is also the evidence the Discussion calls "more conservative". If it is the main generalising evidence, it deserves its own table (by horizon block and by season, as the plan promised).

## B. Trend and seasonal-cycle claims

### B1. HAC with few observations
- The annual regression has 42 observations and bandwidth L=3 (Equation 2 gives floor(4 × 0.42^(2/9)) = 3). HAC standard errors with this T are known to be biased downward.
- The 95% interval uses normal critical values (0.50 ± 1.96 × 0.083). Use t(40) or fixed-b critical values, or confirm the result with a prewhitened or AR(1) GLS slope.
- The Mann–Kendall autocorrelation correction left the statistic unchanged (variance inflation exactly 1). This is by construction when no autocorrelation lag is significant, but say so. At n=42 the test for significant lags has little power.
- The OLS and Sen slopes agree (0.50), which is reassuring.

### B2. Linearity of the trend
- Decade means (9.09, 9.55, 9.87, 10.62, 11.19) and the full-sample slope (0.54 vs 0.50 on training) suggest some acceleration. A single linear slope is a summary, not a description of the path.
- Add a piecewise or quadratic check, or a LOESS curve on the annual-mean figure. Say "average linear trend".

### B3. Seasonal trends
- Say how December is assigned to DJF (December of the preceding year, or the same year). State the number of years used per season.
- The draft says warming is "largest in winter and summer" in the Introduction, while Section 4.1 says the confidence intervals overlap and the data do not support different rates. Remove the ranking from the Introduction.
- Four seasons were tested; note multiplicity or present them as descriptive.

### B4. "No evidence of a change in amplitude or phase"
- This rests on a non-rejection (p=0.76) of a Wald test at HAC lag 5 for monthly data. Seasonal residual autocorrelation is not removed by a single harmonic, and the harmonic model in Equation 3 has only the first harmonic.
- Report confidence intervals for the amplitude change and the phase shift (−0.15 °C, −1.6°). Without them the reader cannot judge what size of change would have been detected.
- Check the sensitivity to a longer HAC lag (the specification mentions a 24-lag check for the deseasonalised regression; do the same here) and to adding a second harmonic.

### B5. Reanalysis inhomogeneity
- The plan listed a sensitivity run from 1991 onward because of changes in the assimilated observing system in MERRA-2. It is not in the paper. The literature review also flags it.
- Because the trend is the paper's first headline result, either run the 1991–2022 trend as a robustness check or state it as an untested limitation in Section 5. Add "of the reanalysis cell" wherever "Frankfurt" is warming.

## C. Reporting and reproducibility

- Section 4.5: forecasts for 2026–2028 are "stored in the results file" and nothing is shown. The research question asks about forecasting the next 36 months. Add one table or figure with the six models' forecasts and intervals, even if unevaluated, and say how much they differ across models.
- The hold-out result is shown only as aggregates. A figure of forecasts versus actuals for 2023–2025 and a plot of monthly errors by model would show the reader whether the gain comes from a few months.
- Reproducibility: the data are in `data.db` with a SHA-256 of the source file, API version and access date, which is good. But POWER revises data between versions, so a rerun from the API may differ. Name the software versions (Python, statsmodels) in the script. The fits have no randomness except possibly optimiser starting values; state that seeds and optimisers are fixed. I could not check the script itself.
- Several derived claims have no number in the text, for example "Absolute-error loss gives the same ranking" and the rolling-origin coverage. Add them.
- LaTeX: two `\bibliographystyle` and two `\bibliography` calls at the end will conflict. The title and author are still placeholders. These are not methods issues but should be fixed before submission.

## D. Nice to have

- Per-season hold-out errors (the plan promised these) and bias per horizon.
- A mean/drift baseline in the formal design, in future work.
- A combination forecast (ETS, SARIMA and harmonic regression), since the candidates are similar.
- A second climatology reference period (1991–2020) for the anomaly statistics; the plan said both would be reported.
- A short note that dynamical seasonal systems do not reach 36 months, so a statistical comparison is the relevant one (from the literature review).

## E. Sensitivity summary

| Choice | Could it change the conclusion? | Checked? |
|---|---|---|
| DM truncation lag / test form | Significance of the 5% results could change | No |
| Seasonal naive interval construction | Width and coverage comparison would change | No |
| Climatology benchmark added | Size and source of the gain would change | No |
| Level vs trend KPSS/ADF | Stationarity reading would change | No |
| HAC lag / critical values in the trend | CI widens modestly; sign unchanged | Partly (lag 24 for the monthly series) |
| Trend start year (1991) | Trend magnitude could change | No |
| Hold-out window | Gain is larger than in the rolling origins | Yes (rolling origins) |

## Score

The core design and execution are honest, and I found no number that is inconsistent with the others I could check. The score is held back by an under-powered, possibly anti-conservative single-origin DM test, a trivially weak benchmark with no climatology reference, an unsupported stationarity reading, an interval comparison driven by the baseline's construction, a probably degenerate ETS pair, and conclusions stated more strongly than these results support.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
