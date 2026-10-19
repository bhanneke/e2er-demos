# Writing Review: Monthly 2 m Air Temperature in Frankfurt (NASA POWER) and 36-Month Forecast Skill

Reviewer: writing_reviewer. Scope: clarity, argument flow, evidence-claim alignment, hedging, voice, concision, consistency. I could not see the `\input` tables or figures, so comments on them are limited to captions and text references.

## 1. Summary assessment

The draft is short, mostly active, and numerically disciplined. Nearly every figure in the text traces to the results file. The paper states its limitations openly: reanalysis rather than station data, a 36-month hold-out, and no causal claim. The weaknesses are of three kinds.

1. **Unfinished front and back matter.** There is a placeholder title and author, no abstract, and a duplicated bibliography block.
2. **Interpretive claims the evidence does not carry.** The main ones are "trend-aware" gains, "trend-stationary", "stable seasonal cycle", "calibration", and a hold-out versus rolling-origin comparison that mixes horizon blocks.
3. **Pre-stated hypotheses reported more favourably than the results file supports.**

Fixing these is a matter of rewriting and re-labelling, not new analysis. The one exception is the missing climatology benchmark (item 3.1).

## 2. Structure and argument flow (first-sentence pass)

Reading only the topic sentences, the argument runs: a seasonal naive heuristic is common; Frankfurt has warmed about 0.5 °C per decade; models beat the heuristic by about 30 percent; the candidates are indistinguishable; the gain is likely overstated by the warm hold-out. This logic is clear. Problems:

- **No abstract, and the title is "Untitled Paper".** The author line reads "Produced by the e2er pipeline", and the page headers repeat both. A referee sees this first. Write a title that states the finding, for example "Warming and Forecast Skill in Monthly Temperature: Frankfurt, 1981–2025".
- **Duplicate bibliography commands.** The file has two `\bibliographystyle` and two `\bibliography` lines (`apalike`/`literature`, then `plainnat`/`refs`). This produces errors or a doubled reference list. Keep one. Note that `literature.bib` mixes 28 unrelated crypto and neuroscience papers, so make sure none are printed.
- **The Introduction states results in the same words as the Results and Discussion.** The "findings" paragraph (Intro), the opening of Section 5, and the Results repeat the numbers 0.50, 30 percent and "indistinguishable" almost verbatim. Keep the Introduction version short and let the Discussion add the interpretation (see 3.1 and 3.5).
- **No related-literature paragraph.** The Introduction cites only the data source. There is nothing on observed warming in Central Europe, on reanalysis trend reliability, on statistical versus dynamical forecasts at multi-year horizons, or on the finding that simple benchmarks are hard to beat in forecasting competitions. The literature review lists these sources, so the paper currently positions itself against nothing. The sentence "a heuristic that practitioners commonly use" has no support. The cited sources should be registered in the bib first, as the literature review itself says.
- **Hard-coded roadmap.** "Section~2 describes…" should use `\ref`. The roadmap sentence is acceptable, but "The remainder of this study is structured as follows" is boilerplate; cut it or compress it.
- **Section 4.5 is a stub.** "Forecasts beyond the data" reports one parameter (0.054 °C per year) and says the forecasts are "stored in the results file". Paper readers cannot access the results file. Either add a table or figure of the 2026–2028 forecasts with intervals, or cut the subsection and mention the exercise in one sentence in Section 3.3. A forecast-versus-actual figure for the hold-out (planned in the paper plan) is also missing and would help more than most of the text.
- **Possible confusion about the end of the data.** The paper says the data end in 2025-12 because POWER loads whole years. The data were accessed in October 2026, so the reader will know that observations for 2026 exist. Add one sentence saying that 2026 months are excluded by design, and why that keeps the 2026–2028 forecasts unevaluated.

## 3. Evidence-claim alignment (most important)

**3.1 "Trend-aware" gain is not demonstrated.** The Discussion says "a trend-aware seasonal model delivers a lower error" and that the 0.5 °C-per-decade trend "is large enough relative to interannual variability to be exploited at a three-year horizon". The evidence points elsewhere:
- ETS(A,N,A) has no trend component and ties with ETS(A,Ad,A) (RMSE 1.30 each; DM 2.75, p = 0.009 each).
- The plan's own H2 rationale was that seasonal naive "carries one year of noise" and that averaging reduces variance.
- The design contains no climatological-mean benchmark, although the paper plan (item 2) and the literature review both call for one. Without it the paper cannot say whether the 30 percent comes from averaging out last year's noise or from the trend.

Fix: either add the calendar-month-mean benchmark (and a trend-free alternative) so the claim is testable, or rewrite the claim as "candidates that average over several years beat the single-year heuristic; this design does not separate trend from noise averaging". The same fix applies to the contribution sentence in the Introduction.

**3.2 ETS(A,N,A) and ETS(A,Ad,A) are reported as two results but behave as one.** Identical RMSE (1.30), identical RMSE ratio (0.68), identical DM statistic and p-value. Tell the reader why. If the damping and slope parameters collapse to the no-trend model, report the estimated parameters in one sentence; the two models should not count as separate evidence. As written, "all four candidates" and "four tests" overstate the independent information.

**3.3 Hypotheses H1 and H2 are described more favourably than the results file does.**
- H1. The text says the point estimate "lies marginally above" 0.3 to 0.5, while the specification says it is "at the upper edge". The rounded 0.50 cannot lie above 0.5. Report the unrounded slope and say which it is. "The lower end of the confidence interval nevertheless lies inside the stated range" is a non-argument for a 0.34 to 0.67 interval: the whole interval partly overlaps the range, and the upper half does not. Say "the interval overlaps the range but extends to 0.67".
- H2. The text states H2 only as "the candidate models improve on the seasonal naive baseline", then declares "support". The pre-registered statement said gains would be modest, with MASE about 0.75 to 0.95. The realised MASE of 0.48 to 0.50 is far outside that range, and the specification says so explicitly ("the pre-registered MASE range is not met"). The paper must state the original H2 in full, including the magnitude, and report that the direction holds while the magnitude does not.
- H3. The text defines H3 as "trend-based models and the exponential smoothing and ARIMA models do not differ", which is muddled because the harmonic regression and the damped ETS are both trend-based. The specification's version is clearer: ETS and SARIMA do not clearly beat the harmonic regression. Use it. Also say that three pairwise tests against one reference were run, and that "no significant difference" with 36 months means low power, not evidence of equivalence. "The four candidates are statistically indistinguishable" (Intro) and "does not matter for accuracy" (Discussion) are absence-of-evidence claims stated as findings. Use "we find no evidence that they differ".

**3.4 Significance claims are given without any multiple-testing statement.** Four Diebold-Mariano tests against one baseline give p = 0.009, 0.009, 0.019 and 0.037. The paper plan promised Holm-adjusted values; the text reports none and does not say they were dropped. The Introduction says the differences "are statistically significant at the 5 percent level" in the same sentence as the power caveat; the SARIMA result (p = 0.037) would not survive adjustment for four tests. Also state the DM details the reader needs: loss horizon h = 12 and the lag used for the variance, and that the 36 errors come from one origin and mix horizons 1 to 36, so they are not iid. The nested-model caveat (Clark-West) from the plan is not mentioned.

**3.5 The hold-out versus rolling-origin comparison is inconsistent.** The Discussion says the hold-out gain is "likely larger than in an average three-year window" and offers the rolling RMSE ratio "near 0.72 at the longest horizons" as the conservative reference. But:
- The hold-out RMSE ratio over all 36 months is 0.68 to 0.71, close to 0.71 to 0.73 for horizons 25 to 36 in the rolling exercise. The gap is two to four points, which on this evidence is not distinguishable from noise.
- The block that differs is the hold-out's final year (ratio 0.43 to 0.46), and the paper compares it with a different block (rolling h25 to 36). Compare like with like, or say plainly that the two exercises give similar full-window ratios.
- The Introduction's "roughly 30 percent" matches the rolling result as well as the hold-out. If so, the warm-hold-out story is weaker than the Discussion implies. Quantify "larger" rather than assert it.

The explanation "consistent with the level shift that the baseline… cannot track" is plausible, and is correctly hedged ("we cannot separate this from chance"). Keep that hedge.

**3.6 Stationarity paragraph misreads the tests.** The text says ADF rejects a unit root and KPSS rejects level stationarity, calls this "mixed but interpretable", and concludes that "rejection by both tests points to trend-stationary behaviour". Three problems:
- Both tests rejecting is a conflict, not a "mixed" picture, and the label is vague.
- A level-KPSS rejection on a series with a drift is expected. The conclusion "trend-stationary" requires a trend-KPSS (or ADF with trend) that the paper does not report.
- The inference is not used anywhere else. Either report the trend-version test and state the conclusion, or cut the claim to "the tests are consistent with a deterministic upward drift and no unit root".

**3.7 "The seasonal cycle itself is stable" overclaims.** The amplitude change of −0.15 °C and the phase shift of −1.6° come with p = 0.76 for the joint test. That supports "we find no evidence of drift". Give the confidence intervals for the amplitude and phase change so the reader can see what drift the data could detect. The Introduction's "no evidence" is the right wording; the Results sentence should match.

**3.8 Seasonal trend wording.** The Introduction says warming is largest "in winter and summer", while the Results say the intervals overlap and the data do not support different rates. The Introduction invites exactly the reading the Results rule out. Say "all four seasons warm by 0.4 to 0.6 °C per decade; the seasonal differences are within sampling error". Give standard errors or intervals in the text for at least winter and summer, because "warming appears in every season" needs intervals that exclude zero. The Discussion's "all four seasons contributing" is decomposition language; use "in all four seasons".

**3.9 Prediction-interval claims.** The Introduction lists as a contribution that "model-based intervals… maintain near-nominal coverage". The Results then say 35 of 36 "cannot be distinguished from 95 percent". The same holds for the baseline, which has 36 of 36: under nominal 95 percent coverage the chance of 36 of 36 is about 16 percent, so "conservative for the baseline" is not established either. Drop "calibration" as a contribution, or restate it as "the intervals contain 35 and 36 of 36 values; the sample is too small to test calibration". Note also that the intervals are serially dependent, so the effective sample is smaller still. The width comparison (14.2 versus 7.2 to 7.3 °C) is the solid finding.

**3.10 "Mann-Kendall confirms a monotone upward trend."** The test rejects no trend; "confirms" is strong. The statement that the variance inflation factor "equals one" is surprising for autocorrelated annual means. Say whether it was floored at one or estimated, otherwise a referee will doubt the correction.

**3.11 Other claims.**
- "A defensible but costly heuristic" (Discussion): "costly" is not quantified, and "defensible" and "costly" pull in opposite directions. State the average error in °C.
- "The naive last-value forecast is unsuitable for monthly temperature" is true but trivial; the 12.06 °C RMSE needs no test. Shorten it.
- The decade means list "2021–2025" beside full decades; call it a five-year period.
- The inference for H1 uses the training window (n = 42). Say whether the CI uses normal or t critical values (0.34 to 0.67 matches 1.96 times 0.083, whereas t with 40 df would give a slightly wider interval).

## 4. Hedging and voice

- Hedging is mostly well calibrated. Appropriate: "the p-values should be read as indicative", "we cannot separate this from chance". Under-hedged: items 3.1, 3.6, 3.7 and 3.9 above.
- Replace slop: "mixed but interpretable picture", "Reading both tests together is informative", "The paper makes a modest contribution of three kinds", "For scholars, the study documents that…". State the actual contribution instead ("We estimate X; we show Y"). "Modest" as self-description is not needed; the Discussion already says what the evidence limits.
- "Future research could ask whether…" is a specific suggestion, so it passes the standard, but write "We leave … to future work" and drop the second suggestion (several grid cells) unless you have a concrete reason.
- Voice is active almost throughout. Acceptable passives: "All diagnostics are computed on data up to December 2022". Change "The forecast setup was fixed before estimation and frozen together with the hold-out" to "We fixed the forecast setup…", and say who froze it and where (the lock file). Also cite the pre-registration lock when you say hypotheses were stated "before seeing the results".

## 5. Paragraph and sentence level

- **Single-sentence paragraphs.** "We therefore find support for H2 on the hold-out." and "Absolute-error loss gives the same ranking and conclusions." are stranded. The second gives no numbers; report the absolute-error DM statistics or the range of p-values, or fold the sentence into the previous paragraph.
- **Long paragraph.** The Section 3.1 trend paragraph carries three regressions, a nonparametric test, an autocorrelation variant, and the drift model with equations. Split at "We also test whether the amplitude and phase…". Add a one-line statement of the quantity each estimate describes.
- **Number sentences.** The hold-out accuracy paragraph strings 12 numbers with "followed closely by". A table already exists; keep three numbers in the text (baseline RMSE, best candidate RMSE, ratio) and refer to the table for the rest.
- **Units and baselines.** "Their MASE values lie between 0.48 and 0.50" needs the reading: errors are about half the in-sample seasonal naive MAE of 2.04 °C. Give the baseline for 0.50 °C per decade in plain terms (about 2.1 °C over 42 years versus anomaly SD 1.90 °C).
- **"Degrees Celsius".** The phrase appears dozens of times. Define "°C" once and use it.
- **Terminology.** "Seasonally adjusted" (Section 3.2, Results) and "deseasonalised" (Section 3.1) name the same object, as do "hold-out", "test" (in table names such as `_test`) and "out-of-sample". "Candidates" and "non-naive models" also vary. Pick one term for each. "Newey-West", "HAC" and "Bartlett kernel" should be introduced once as one estimator. "Harvey–Leybourne–Newbold" appears in Results but the text cites only "Harvey et al." in Methods; spell out the authors once.
- **Tense.** Methods mix "was fixed" with "is fitted"; settle on present tense for the design and past tense for the three hypotheses.
- **Wordy phrases.** "The point estimate lies marginally above the range of 0.3 to 0.5 degrees that we stated in advance for H1, so the hypothesis is supported in sign but not fully in magnitude" can read "The estimate (0.50) sits at the upper edge of the 0.3 to 0.5 range we stated for H1." "This is expected because its forecast does not depend on the horizon beyond the interval width" is clearer as "This is by construction: the point forecast does not depend on the horizon."
- **Grid-cell description is inconsistent.** The Introduction says the "grid cell centred at 50.11°N, 8.68°E"; Section 2 says the cell "containing" that point. MERRA-2 cells are 0.5° × 0.625°, so the query point is generally not the centre. Use "containing" in both places. Add the cell size and elevation (171.6 m, from the data summary), since the paper's reanalysis caveat hinges on them.
- **Data citation.** POWER's referencing guide asks for both the project reference and the data reference. The text cites only `NASA_POWER`. Add the API version (v2.10.0) and the access date (13 October 2026) in the Data section.
- **Figure captions.** Both captions only name the series. Say that the hold-out is shaded (if so), what any fitted line is, and the unit. The hold-out forecast figure is missing.
- **Residual comments.** The `% src:` lines are provenance markers; make sure they do not leak into the submitted source.

## 6. Limitations section

The scope conditions are honest and well placed. Add what is missing: (i) reanalysis inhomogeneity from changes in the assimilated observing system, which the paper plan flagged and the paper never mentions; (ii) multiple testing across four DM comparisons; (iii) the absent climatology benchmark (3.1); (iv) a single grid cell and a single forecast origin, so the hold-out ranking rests on one realisation. The urban heat island sentence is fine but should say in which direction the bias would run.

## 7. Priority fixes

1. Replace the title and author, add an abstract, and remove the duplicate bibliography commands.
2. Restate H1, H2 and H3 exactly as pre-stated, including the H2 magnitude (MASE 0.75 to 0.95) that the results miss.
3. Remove or test the "trend-aware" claim; add a climatology benchmark or reword the contribution and the Discussion.
4. Explain the identical ETS results, and stop counting them as two independent findings.
5. Add a multiple-testing statement and DM specifics; reword "indistinguishable" as "no evidence of a difference".
6. Correct the stationarity interpretation, the "stable" cycle claim, the interval-calibration claim, and the hold-out versus rolling comparison (compare the same horizon blocks).
7. Add a short related-literature paragraph, using sources registered in the bib, and cite POWER with version and access date.
8. Either show the 2026–2028 forecasts and a hold-out forecast figure or cut Section 4.5.
9. Sentence-level pass: terminology, the repeated "degrees Celsius", slop phrases, stranded one-sentence paragraphs.

OVERALL SCORE: 5.5/10
RECOMMENDATION: Major Revision
