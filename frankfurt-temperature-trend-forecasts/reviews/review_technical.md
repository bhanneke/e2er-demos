# Technical Review

Paper: Monthly mean 2 m air temperature, Frankfurt am Main (NASA POWER), trend and 36-month forecast evaluation. Template: time series and forecasting.

Scope and limits. I checked the draft against the econometric specification, data dictionary, data summary and plan. I did not have `estimation_results.json`, `summary_statistics.json`, the `tables/*.tex` files or the figures. Numbers were therefore checked for internal arithmetic consistency and against the numbers quoted in the specification, not cell by cell against the source files. Table cells and figures are unverifiable here.

## Summary Assessment

**Concerns.** The pipeline is sound and the reported numbers are internally consistent. The training sample is 504 months, the hold-out is 36 months, and the fixed origin is 2022-12. All diagnostics have `sample_end` 2022-12, and model selection by AICc uses the training window only. I found no leakage. The recomputable numbers (MASE, RMSE ratios, DM p-values, the full-sample mean, the CI) agree with each other.

The problems lie in inference and interpretation:

1. The headline gain over seasonal naive is almost exactly what noise-averaging alone predicts (ratio about 1/√2). It is attributed in the Discussion to "trend-aware" modelling, which the paper's own results do not support.
2. The DM test rests on one forecast origin whose baseline errors repeat the same 2022 noise at lags 12 and 24, beyond the HAC bandwidth, so the p-values are overstated.
3. The interval comparison is partly an artefact of the seasonal-naive interval formula, and the hold-out is an unusually quiet window.
4. The H2 narrative is loosened relative to the pre-registered statement.

All are fixable without new data. Several are about wording and added disclosure, not re-estimation.

## Data Pipeline

**Sound.**
- 540 raw rows is 45 years × 12. Zero missing, zero fill values, zero duplicates, zero gaps. The split is 504 + 36 = 540.
- The full-sample mean is consistent with the parts: 9.83 + (36/540)(11.46 − 9.83) = 9.94.
- The decade means (9.09 to 11.19) imply about 0.56 °C/decade across decade midpoints, consistent with the trend estimates.
- The 1981–2010 climatology lies inside the training window.

**Issues.**
1. **Grid-cell description is wrong.** The Introduction says "the grid cell centred at 50.11°N, 8.68°E". The data dictionary describes a MERRA-2 cell of 0.5° × 0.625°, which has fixed centres. By my calculation they are near 50.0°N, 8.75°E, so verify this. The requested coordinates are a query point. Say "the cell containing" (as Section 2.1 does) and state whether POWER interpolates or applies an elevation correction. The data summary gives a grid elevation of 171.6 m.
2. **Reanalysis homogeneity is not discussed.** The plan flagged changes in the assimilated observing system and MERRA-2 stream changes, and planned a "from 1991" sensitivity run. The draft neither runs it nor mentions it, yet interprets a 0.5 °C/decade trend and a 2023–2025 level. At minimum, add it as a limitation. Preferably report the 1991–2022 trend.
3. **Seasonal means (DJF) are undocumented.** The draft does not say how December is assigned to a season year. The training window starts in 1981-01, so DJF 1981 lacks December 1980. State the rule and the number of seasons per estimate.
4. **Selected specifications are not reported.** The draft never gives the SARIMA orders chosen by AICc, the number of harmonics K, the ETS smoothing and damping parameters, or software versions. These are needed to reproduce the study and to interpret Issue 2 under Estimation Implementation.
5. **Hold-out years enter the descriptives.** The decade mean 2021–25 and the decade-mean statement use hold-out years. This is acceptable for description because the paper marks it as descriptive, but note it explicitly where the 2021–25 mean appears.

## Estimation Implementation

**Specification match.** The trend equations, the HAC lag formula, the drift model and the model list agree with the specification.
- Annual HAC lag is floor(4·0.42^(2/9)) = 3.
- Monthly HAC lag is floor(4·5.04^(2/9)) = 5.
- The CI 0.34 to 0.67 equals 0.50 ± 1.96 × 0.083, so the intervals use normal critical values.

**Issues.**
1. **DM test dependence is understated (most important).**
   - The seasonal-naive forecast at a fixed origin repeats the same twelve 2022 values for all three years. Each baseline error is therefore (2022 noise for month m) minus (target noise), and the 2022 component recurs at lags 12 and 24.
   - The specification and draft use h = 12, which means a Bartlett or rectangular truncation at lag 11, plus the HLN factor. That factor is about 0.68 at n = 36, h = 12. Lags 12 and 24 are outside the bandwidth.
   - The effective number of independent loss differentials is closer to 12 than 36, and the result depends on how noisy one year (2022) was.
   - The statement "limited power, indicative" is right but understates the problem. The p-values (0.009 to 0.037) are probably too small.
   - The plan promised rolling-origin DM as the "main inference". The draft reports no rolling DM test.
   - Recommended actions: (a) compute DM on the twenty rolling origins with a dependence-robust variance (block bootstrap or clustered by origin); (b) report a lag-24 sensitivity on the hold-out; (c) call the hold-out result suggestive.
2. **The two ETS variants may be one model.**
   - ETS(A,Ad,A) and ETS(A,N,A) have the same RMSE (1.30) and DM statistic (2.75, p = 0.009). Their ordering ("lowest", "followed closely") is not resolvable at two decimals.
   - If the damped trend collapsed (φ near 1 or 0, or a trend component near zero), the paper has three effective candidates, not four. Report the fitted parameters and the unrounded RMSEs.
3. **The "trend-aware" interpretation is not identified.**
   - Seasonal-naive errors have variance ≈ 2σ², since they combine last year's noise and the target's noise. Any model that averages the seasonal level over many years has variance ≈ σ². The expected RMSE ratio is therefore about 1/√2 = 0.71.
   - The observed ratios are 0.68 to 0.71. The noise-averaging explanation, which is also the mechanism the pre-registration states for H2, accounts for nearly all of the gain.
   - The trend adds almost nothing at this horizon. At 0.05 °C/yr the baseline's drift bias is at most 0.15 °C over three years, so bias² ≈ 0.02 against MSE ≈ 1.7 to 3.7. ETS(A,N,A), which has no trend, ties the trend models.
   - The Discussion's sentence that "a trend-aware seasonal model delivers a lower error" and "the trend of roughly 0.5 degrees per decade is large enough ... to be exploited at a three-year horizon" is not supported.
   - A seasonal-mean (climatology) baseline and a seasonal-mean-plus-drift baseline are needed to separate the two effects. The plan and the literature review both recommended a climatology benchmark. The frozen design dropped it.
   - Because the design is frozen, add these as clearly labelled post-freeze exploratory benchmarks, or confine the claim to "multi-year averaging beats one-year persistence".
4. **Hold-out error is not comparable with training noise.**
   - Seasonal-naive rolling MASE is 1.02 (MAE ≈ 2.08), against hold-out MAE 1.64. Candidates' rolling MASE of 0.71–0.73 corresponds to MAE ≈ 1.5, against about 1.0 on the hold-out.
   - The hold-out is roughly 30% quieter than the training-window average, as the anomaly SD of 1.90 also suggests. Absolute accuracy figures overstate typical skill.
   - The ratio to the baseline is more stable than the levels. Say this, and do not describe the rolling result as "smaller" without numbers: the overall RMSE ratio is 0.68–0.71 on the hold-out and 0.71–0.73 at h25–36 in the rolling exercise.
5. **Rolling-origin coverage is incomplete.**
   - SARIMA is not in the rolling exercise: the draft cites only the harmonic and ETS(A,Ad,A) rolling MASE.
   - The paper says "the candidate models" while four are declared, and does not state whether order or K selection was re-done per origin.
   - The naive baseline is also absent. Report all declared models, or state which are missing and why.
6. **Interval formula conflicts with the paper's own diagnostics.**
   - The specification scales the seasonal-naive interval by √(cycles ahead), a seasonal random-walk assumption.
   - The paper finds trend-stationary behaviour and flat error across blocks (1.92 / 1.94 / 1.89). Interval width should therefore not grow with horizon.
   - The statement that candidate intervals are "about half as wide" at near-nominal coverage is partly an artefact of this formula. The baseline's 100% coverage then reflects over-wide intervals.
   - Candidate intervals are also wide relative to hold-out errors. A width of about 7.2 implies σ ≈ 1.85, against RMSE 1.30. The 97.2% coverage therefore reflects the quiet hold-out, not demonstrated calibration. 35/36 has an exact binomial 95% CI of about 85% to 99.9%, which cannot distinguish 90% from 99%.
   - Tone down "near-nominal" in the Introduction's third contribution, or add a rolling-origin coverage estimate.
7. **Stationarity reading is under-specified.**
   - ADF with constant and KPSS "level" on the seasonally adjusted series both reject. The rejection by KPSS-level in a trending series is expected. The "trend-stationary" conclusion needs KPSS with trend (ct) and ADF with trend as a check.
   - The draft calls the picture "mixed but interpretable". Both tests rejecting is not a disagreement in the usual sense. Reword.
   - The variance inflation factor equals exactly 1 in the Hamed–Rao-type correction. That is plausible if no lag is significant, but say so, and report the annual-residual ACF.
8. **Unreported robustness.** The specification lists a longer HAC lag (24) for the monthly deseasonalised trend, and the plan lists bias by horizon. Neither appears in the draft. Monthly HAC lag 5 is short for residual seasonal structure.
9. **Small-sample inference.** The annual regression has 42 observations and 3 HAC lags with a normal CI. A t(40) interval would be a few hundredths wider. State the choice.

## Results Reporting

**Arithmetic checks (all pass):**

| Claim | Check | Result |
|---|---|---|
| Seasonal naive MASE 0.80 | 1.64 / 2.04 = 0.804 | consistent |
| RMSE ratios 0.68 and 0.71 | 1.30/1.92 = 0.677; 1.36/1.92 = 0.708; 1.37/1.92 = 0.714 | consistent |
| "about 30 percent" lower RMSE | 29%–32% | consistent |
| DM p-values | t(35): 2.75 → 0.009; 2.47 → 0.019; 2.17 → 0.037 | consistent |
| HAC CI | 0.50 ± 1.96 × 0.083 = 0.34 to 0.66 | consistent |
| Season slopes vs annual | mean(0.62, 0.38, 0.61, 0.39) = 0.50 | consistent |
| Candidate coverage | 35/36 = 97.2% | consistent |
| Annual slope full vs training | 0.54 vs 0.50; harmonic trend 0.054/yr | consistent |

**Items to check or fix:**
- **Naive forecast RMSE 12.06 / MASE 4.79.** RMSE² should equal SD² of the hold-out around the constant, i.e. about 7.5² + (11.46 − c)². This implies the December 2022 value c ≈ 2 °C. Verify against `data.db`, since this is higher than I would expect for a constant forecast.
- **H1 wording.** The text says the point estimate is "marginally above" 0.3–0.5. The specification says "at the upper edge". Print the unrounded slope. The CI (0.34 to 0.67) contains nearly the whole pre-registered range, so H1 is neither confirmed nor rejected with precision. Say that.
- **H2 is reported more weakly than registered.**
  - The registered claim was that trend or level-adjusted models beat seasonal naive at long horizons, with modest gains (MASE about 0.75 to 0.95). Realised MASE is 0.48–0.50 against 0.80.
  - The specification states that the MASE range is not met and the gain is larger than "modest". The draft restates H2 as "the candidate models improve on the seasonal naive baseline" and concludes "support for H2" with no mention of the missed range. It also says the hypotheses are evaluated "without revision".
  - Report the registered statement verbatim, then "direction supported, magnitude outside the range".
- **H3 and "statistically indistinguishable".** Insignificance at n = 36 is not equivalence. Replace the Introduction's "statistically indistinguishable" with "no significant difference detected".
- **Mechanism for the final-year advantage.** The text attributes the larger gain in 2025 to a "level shift the baseline cannot track". The baseline is anchored on 2022, itself a warm year. The pre-registered mechanism (baseline carries one year of noise) is the simpler explanation. The draft is right to add "cannot separate from chance". Add the noise-averaging alternative.
- **Rolling-origin numbers.** The statement "reproduced outside the hold-out" is fair. The comparison to the hold-out should be given as a ratio, per Issue 4.
- **Multiple testing.** Four candidates, two loss functions and no correction. The four squared-error p-values survive Holm (adjusted 0.036–0.038), so state that. The dependence concern in Issue 1 matters more.
- **Forecasts beyond the data.** The 2026–2028 forecasts and intervals are "stored in the results file" but not shown. Give a table or figure, or drop the subsection. Section 3.3 promises forecasts for all six models.
- **Unverifiable.** Table cells (seasons, diagnostics, accuracy, DM), the figures, and the "absolute-error loss gives the same ranking" statement.

## Red Flags

- **Narrative–evidence mismatch** (trend attribution, Issue 3). This is the main flag.
- **No multiplicity story.** P-values cluster between 0.009 and 0.037 and the sample is small. This is not evidence of p-hacking, since the setup was frozen. Do note that H1–H3 and all models are reported.
- **Draft LaTeX defects:** two `\bibliographystyle` commands (apalike and plainnat) and two `\bibliography` commands (literature, refs). This produces a LaTeX error or a duplicated bibliography. The title is "Untitled Paper".
- **Missing citations for stated facts.** Section 2.1 says POWER derives from MERRA-2, which should cite Gelaro et al. (2017). The literature review says the key is not yet in the bib, so register it first.
- **Magic numbers.** The 20-year minimum training length and origin spacing are declared in the specification. The sample-size reasoning for the 36-month hold-out is documented. I saw no undocumented hardcoded filters.

## Strengths

- A frozen design, with the optional ML model and the DWD comparison cleanly dropped and named as future work.
- No leakage found. Diagnostics, deseasonalisation, climatology, model selection and MASE scale are all training-only. The 2026–2028 forecasts come from separate refitted models and are not evaluated.
- All declared models are reported, including the naive baseline that loses badly.
- The seasonal-naive baseline is correctly defined as the same month of the last observed year, with MASE scaled by its in-sample MAE. The HLN small-sample correction is used.
- Honest caveats about reanalysis versus station data and about the low power of a 36-month hold-out.
- Pre-registered hypotheses are stated and checked against results. The partial miss on H1 is acknowledged.
- A rolling-origin supplement is included and is explicitly not used for model selection.
- The seasonal-cycle drift test is a sensible, falsifiable way to examine amplitude and phase.

## Recommendations

**Data stage**
1. Correct the grid-cell wording and state the interpolation and elevation treatment.
2. Add the reanalysis-homogeneity caveat. Report the 1991–2022 trend if cheap.
3. Document the DJF year assignment. Report the selected SARIMA orders, K, ETS parameters and software versions.

**Estimation stage**
4. Add a seasonal-mean baseline and a seasonal-mean-plus-drift benchmark, labelled exploratory because it is outside the frozen set. This separates noise-averaging from trend. Report bias by horizon.
5. Recompute DM with dependence that covers lags 12 and 24, or by block bootstrap, and add rolling-origin DM. Treat the hold-out p-values as suggestive.
6. Extend the rolling-origin exercise to SARIMA and the naive baseline, or state the omission. Say whether selection was repeated per origin.
7. Report fitted ETS parameters. If the damped trend collapsed, say the candidates reduce to three.
8. Add KPSS and ADF with trend, the HAC lag-24 sensitivity, and the verification of the naive RMSE.
9. Revisit the seasonal-naive interval scaling, or report an interval whose width does not grow with horizon as a sensitivity check. Add rolling-origin coverage.

**Draft stage**
10. Rewrite the Discussion and Introduction so the gain is attributed to multi-year averaging, with the trend contribution small and untested.
11. State H2 as registered and note that the MASE range is missed. Replace "statistically indistinguishable" with "no significant difference detected".
12. Describe interval calibration conservatively (97.2% on 36 points, wide relative to realised error, quiet hold-out).
13. Show the 2026–2028 forecasts or remove the subsection. Fix the duplicate bibliography commands, the title, and the missing MERRA-2 citation.
14. Give unrounded values where the text depends on a boundary (the H1 slope).

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
