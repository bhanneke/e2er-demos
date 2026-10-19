# Plausibility Review: Monthly 2 m air temperature, Frankfurt (NASA POWER), trend and 36-month forecast skill

Scope: do the numbers and interpretations make sense for what is measured (a MERRA-2 reanalysis grid-cell value, not a station record). Number tracing to the results files is done elsewhere. Statements from my own knowledge are marked "(own knowledge)" and need verification. I did not run any code.

## Overall assessment

The reported numbers are mutually consistent and, for the trend and the seasonal cycle, plausible for Central Europe. I could re-derive the following from the paper's own figures:
- Training mean 9.83 and hold-out mean 11.46 give the full-sample mean 9.94.
- The four seasonal slopes average to the annual 0.50 °C per decade.
- The decade means follow roughly 9.83 + 0.05 × (year − 2001.5).
- The MASE scale of 2.04 is consistent with the seasonal-naive MAE of 1.64 (MASE 0.80).
- The DM p-values match t(35) for the reported statistics.

The main plausibility problems are in interpretation, not arithmetic:
1. The forecast gain is read as a trend effect and as larger than usual because of a warm hold-out. The paper's own ratios contradict the second reading, and the design cannot support the first.
2. The reanalysis level and seasonal amplitude are never checked against known Frankfurt climate.
3. The hold-out looks unusually easy.
4. The inference on the 36 errors is weaker than stated.

## Findings

### 1. The "warm hold-out inflates the gain" claim is contradicted by the paper's numbers (Section 4.4, Discussion)
- **Where.** Section 4.4 says the rolling-origin gain is "smaller than on the 2023–2025 window". The Discussion says "the size of the gain is likely larger than in an average three-year window".
- **What the numbers show.** Hold-out RMSE ratios are 0.68–0.71. Rolling-origin RMSE ratios at h25–36 are 0.71–0.73, and the MASE ratio is 0.72/1.02 = 0.71.
- **Reading.** The ratios are essentially identical. Only the absolute errors differ: seasonal naive MAE is about 1.64 on the hold-out against about 2.08 in the rolling exercise. That is a difference in noise level, not in relative skill.
- **Why it is expected.** A ratio near 0.71 ≈ 1/√2 is what theory predicts when a forecast carries one extra year of independent anomaly noise (error variance 2σ² against σ²). The literature review makes the same point. The "30 percent" gain is therefore close to the textbook value for any smoothed-seasonal-mean forecast, not something specific to 2023–2025.
- **Only the final-year ratio is unusual.** The 0.43–0.46 ratio in months 25–36 is a single-year realisation. It should not be generalised or tied to a "level shift" without a bias-by-horizon table.
- **Check.** Report the mean error (bias) by horizon block for all models, and rewrite the "larger than average" sentence.

### 2. The gain is attributed to the trend, but the design cannot separate trend from noise averaging (Discussion, Intro)
- **Where.** The Discussion says "a trend-aware seasonal model delivers a lower error" and that the 0.5 °C per decade trend "is large enough… to be exploited at a three-year horizon".
- **Evidence against.** ETS(A,N,A) has no trend and ties with ETS(A,Ad,A) at RMSE 1.30. The two also have identical DM statistics (2.75, p = 0.009), which suggests the damped trend collapses to zero.
- **Missing benchmark.** The literature review and the paper plan both listed a calendar-month climatology benchmark, and it is absent from the frozen design. A 30-year calendar-month mean forecast, and the same mean plus a linear trend, would show how much of the gain comes from noise averaging and how much from level or trend adjustment.
- **Back-of-envelope (own estimate).** A plain training-window climatology would be biased by about 1.6 °C on the hold-out (11.46 − 9.83). Its RMSE would then be at or above that of the seasonal naive forecast. So level adaptation clearly matters here, but this is a statement about level, not about a 0.5 °C per decade trend.
- **Check.** Report ETS smoothing parameters (α, β, φ) and the hold-out bias. At minimum, soften the "trend-aware" wording. If the freeze allows, add the climatology benchmark as a descriptive reference.
- **Also.** "Modestly so" in the Discussion sits oddly with a roughly 50 percent reduction in MSE.

### 3. The hold-out looks unusually easy in absolute terms (Section 4.2)
- **Numbers.** Candidate RMSE is 1.30 and MAE is about 1.0 (MASE 0.48–0.50). The in-sample anomaly SD is 1.90, and the SD around the trend is about 1.8 (own estimate). Rolling-origin MASE is 0.71–0.73, i.e. MAE ≈ 1.5.
- **Reading.** The hold-out error is about 30 percent below what the rolling exercise and the anomaly SD imply. The same holds for the seasonal naive forecast (RMSE 1.92 against an expected 2.5–2.7 for a 12-month difference of anomalies with SD 1.9).
- **Cause.** The three hold-out years are warm and fairly persistent: the 2021–25 decade mean of 11.19 and the hold-out mean of 11.46 imply 2021–22 averaged about 10.8. This favours both the baseline and the candidates.
- **Consequence.** The absolute errors, the MASE values (0.48–0.50) and the miss of the preregistered MASE range (0.75–0.95) should be attributed to a quiet window. The rolling-origin figures (0.71–0.73) lie close to the preregistered range.
- **Disclosure.** The paper says "we therefore find support for H2" but does not state that the preregistered MASE range was missed. The econometric specification states this explicitly. The paper should too.

### 4. The reanalysis level and amplitude are not checked against known Frankfurt climate (Sections 2.1, 2.2)
- **Reported values.** Climatology 1981–2010: January −0.54 °C, July 20.11 °C. Minimum monthly mean −7.03 °C. Decade means 9.09–11.19 °C. Grid elevation 171.61 m.
- **Comparison (own knowledge, verify against DWD Klimareport).** The Frankfurt-area station annual mean is roughly 10.5 °C for 1991–2020, and January is roughly +1 °C in 1981–2010. The grid cell appears about 0.5 °C cold on the annual mean and about 1.5 °C cold in January, with July close to station values.
- **Consequences.**
  - The seasonal amplitude of the cell (about 20.6 °C peak-to-peak) looks larger than a station's (about 18.5 °C).
  - This pattern would be a winter cold bias, which fits the known MERRA-2 behaviour over continental Europe only loosely (own knowledge).
  - The minimum of −7.03 °C is probably January 1987 or February 1986 and would be cold relative to station records.
- **Cell size.** The cell is 0.5° × 0.625°, about 55 × 40 km. It contains the Taunus, parts of the Odenwald and the Rhine-Main plain. "Urban heat island only partly represented" is generous: at this size it is essentially diluted. The label "Frankfurt am Main" should be used with care.
- **Check.** State the bias and amplitude differences against published DWD climatology (a literature number is enough, no station data needed). Identify the months of the minimum (−7.03) and maximum (24.67); if the maximum falls in 2023–2025, the hold-out contains the series record.

### 5. Possible inhomogeneity in the reanalysis trend (Sections 2.1, 4.1)
- **Concern.** MERRA-2 uses several production streams, and the observing system changed over 1981–2025 (own knowledge; the literature review flags it too). A 2.1 °C rise in the decade means (about 0.56 °C per decade) is large and in line with, if on the high side of, observed warming for Hesse (own knowledge).
- **Paper's treatment.** The paper does not mention possible stream or observing-system breaks. The plan listed a "from 1991" sensitivity run, but it is not reported.
- **Check.** Report the trend from 1991 onward, or compare with the published DWD Hesse or Germany trend as a plausibility anchor. Say that the trend is a property of the product.

### 6. Prediction intervals: width logic and homoscedasticity (Section 4.3)
- **Seasonal naive width.** The mean width of 14.2 °C follows from the design: the SD of the 12-month difference scaled by √(cycles ahead). Anomalies are close to stationary, so a 24- or 36-month-lag difference has about the same variance as a 12-month one. The paper's own flat RMSE by horizon (1.92, 1.94, 1.89) shows this. The width is an artefact of the interval construction, so 100 percent coverage says little about baseline calibration. The sentence "conservative for the baseline" should say so.
- **Model intervals.** A width of 7.2–7.3 °C corresponds to an SD of about 1.85 °C, which matches the residual SD. But a single constant SD ignores that winter monthly variability is roughly double summer's (own knowledge: about 2.5 against 1.3 °C). The one miss out of 36 is likely a winter month.
- **Check.** Report in which month the miss falls. A seasonal-variance interval would be more plausible but cannot be added after the freeze, so mention it as a limitation.

### 7. DM inference on 36 errors is weaker than the p-values suggest (Section 4.2)
- **Reading of the p-values.** The statistics are arithmetically correct. But the 36 errors come from one origin, so they share the same level error and are strongly dependent. The effective sample is close to three seasonal cycles, or even one level offset. The HLN correction uses h = 12, while the errors run over h = 1–36. The p-values of 0.009–0.037 are likely too small.
- **Claims that go beyond the test.**
  - "The four candidates are statistically indistinguishable from one another" rests on 3 of 6 pairs (each against the harmonic model only).
  - Non-rejection at n = 36 is not evidence of equivalence.
  - Nested-model caveats apply (Clark-West, from the plan).
- **Check.** Report the rolling-origin DM, which was the planned primary evidence. Otherwise word the abstract and intro as "no detectable difference".

### 8. Stationarity interpretation (Section 4.1)
- **Statement.** "Rejection by both tests points to trend-stationary behaviour."
- **Problem.** ADF with a constant and KPSS for level stationarity are both biased by the trend. Both rejecting is consistent with trend-stationarity but also with a level shift or a break. The proper check is KPSS with a trend ('ct') and ADF with trend. The ADF statistic of −6.87 is plausible for a noise-dominated seasonally adjusted series and says little about the trend.
- **Check.** Report the trend variants.

### 9. Smaller items
- **Mann-Kendall variance inflation exactly one.** This probably reflects a clamp at 1 when the residual autocorrelation of annual means is close to zero. Plausible, but state that it is truncated.
- **H1 wording.** The paper says the estimate lies "marginally above" the range, while the specification says "at the upper edge". Check the unrounded value and use the same wording. The argument that the lower CI end lies inside the range is a weak basis for support.
- **"Decade means" for 2021–2025.** This is a five-year period that includes the hold-out. Label it a partial period, and do not read the 9.09 → 11.19 rise as a decade-to-decade comparison.
- **Seasonal trends.** DJF 0.62 and JJA 0.61 against 0.38 and 0.39 are described correctly as not distinguishable. The "largest in winter and summer" line in the Introduction should carry the same caveat, because winter interannual variability is much larger and its CI should be wider. Check how December is assigned to a winter and how the incomplete first and last winters (1981, 2025) are handled.
- **Amplitude and phase drift.** −0.15 °C and −1.6° (about 4 days) over 42 years are small and plausible. Equal winter and summer slopes imply no amplitude change, so this is consistent. The Wald test with 4 drift parameters and HAC errors has low power; "no evidence" is the right phrase, "stable" is slightly stronger.
- **Naive RMSE of 12.06 and MASE 4.79.** The numbers are plausible for a flat December 2022 value (about 2 °C) against a 36-month mean of 11.46 °C and a seasonal SD of 7.5 °C.
- **"Data end in 2025-12 because POWER loads whole years".** As of October 2026, months of 2026 are probably available in the monthly API (own knowledge; verify). The 2026 months already observed could give a genuinely new out-of-sample check of the stored 2026–2028 forecasts. If unavailable, keep the sentence; otherwise present it as a design choice, not a data limitation.
- **Stored 2026–2028 forecasts.** Spot-check that the annual means are plausible (around 11.0–11.5 °C) and that the intervals are not nonsensical. Not shown in the paper.

## Plausibility score reasoning

- **Strong.** Trend magnitude, seasonal pattern, MASE scale and naive-forecast behaviour are consistent with each other and with domain knowledge.
- **Weak.**
  - The "larger than average gain" claim is contradicted by the paper's own ratios (1).
  - The trend attribution is unsupported (2).
  - The hold-out is unusually quiet (3).
  - There is no sanity check of the reanalysis level or amplitude against known climate (4).
  - The interval and DM readings are too optimistic (6, 7).
- All are fixable by rewording and by reporting extra diagnostics already available in the results.

OVERALL SCORE: 6.5/10
RECOMMENDATION: Minor Revision
