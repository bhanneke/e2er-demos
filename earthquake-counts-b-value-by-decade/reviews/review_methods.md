# Methods Review: yearly M>=5 counts and Gutenberg–Richter b-value by decade, ComCat 1976–2025

Scope of this review: I read the paper text, the analysis specification, the data dictionary, the data summary and the plan. I did not have `run_estimation.py`, `estimation_results.json` or the LaTeX tables in my context. Script-line checks are therefore replaced by checks of the paper against the specification and against the data summary. Anything I could not verify is marked as such.

## 1. Overall assessment

The study is descriptive, transparent about its limits, and it reports its sensitivity results, including those that complicate the story. The estimator (Aki–Utsu with bin correction), the Shi–Bolt standard error and the sample flow are correctly stated.

Four problems stand between the design and the conclusions the paper draws.

1. For three of five decades the "estimated" completeness magnitude is the load floor plus a constant, not an estimate.
2. The inference (Utsu test, bootstrap) treats clustered, aftershock-laden events as independent, yet the headline in the abstract is a count of rejections at the 1 percent level.
3. The Mw-only contrast, on which the discussion rests its open question, compares different thresholds. It can be settled with a check the data already allow.
4. The statements about M>=6 and M>=7 counts do not match the numbers the paper itself reports.

## 2. What must change

### M1. Decade-specific Mc is not identified in 1996–2025 (Sections 3, 4.2, 4.3; abstract; conclusion)

- The data are truncated at M4.5. Maximum curvature takes the mode of the 0.1-bin distribution, and in the last three decades that mode is the first bin (4.5). The "+0.2" rule then returns 4.7, which is the floor plus 0.2 and carries no information about completeness.
- The GFT rules at 4.5 are also the floor, so they are censored. The paper says this in two places.
- It nevertheless builds its headline "decade-specific Mc" series (4.9, 4.9, 4.7, 4.7, 4.7) on these values.
- The decade differences in the "own Mc" series therefore mix a decade effect with a threshold effect (4.9 against 4.7). The paper's own Table `mc_shift` shows how large the threshold effect is: 1996–2005 moves from 1.055 to 0.924 between 4.7 and 4.9.
- The justification in Section 3 is circular. It says Mc "turns out to be at or below about 5, so events down to 4.5 suffice". Data truncated at 4.5 cannot show that Mc is below 4.5.
- The research question asks for b "once the completeness magnitude is taken into account". That is not achieved for 1996–2025 with this load.

Fix, in order of preference:
- (a) Load M>=4.0 or 3.5 for 1996–2025 only, to estimate Mc where it can be seen. If the load is out of scope, say so and then:
- (b) Make the fixed thresholds the primary specification. These are 4.9 (common) and 5.0, with a grid up to 5.5. Present the "own Mc" results as secondary, and state that the three late-decade Mc values are floor-driven. The abstract's range "1.02 to 1.16 at decade-specific completeness magnitudes" should not appear as a finding.
- Delete the sentence that makes the load floor look like a result of the analysis.

### M2. Tests and intervals treat dependent events as independent, and the abstract headlines them (abstract; Sections 3.3, 4.3; Discussion)

- The data contain full aftershock sequences. The Shi–Bolt SE, the event-level bootstrap and Utsu's LR test all assume independent magnitudes. The paper concedes this in the limitations, yet the abstract reports "rejects equality at the 1 percent level in nine of ten pairs" and the conclusion repeats it.
- With N between 2×10^4 and 7×10^4 per decade, almost any difference rejects. The statistic ranges from 51 to 793, and the bootstrap half-widths are about 0.01.
- Within a single decade, b moves by 0.2–0.3 when the threshold moves by 0.2 (1996–2005: 1.055, 1.003, 0.924, 0.927). That variation, not the sampling error, is the real uncertainty of "the" decade b. Reading a 0.14 gap at p<0.01 as meaningful understates it.
- Fix:
  - Bootstrap by calendar year, resampling years within a decade. This needs no declustering and carries the between-year and between-sequence variation.
  - Report the bootstrap CI of the difference b_i − b_j for each pair, from the same resamples.
  - Drop the p-value counts from the abstract and conclusion, or qualify them there as conditional on independence.
- The bootstrap holds Mc fixed. It therefore cannot reflect the Mc uncertainty that dominates here. Either resample Mc as well or say that the interval is conditional on Mc.

### M3. "Overlapping intervals" is used as a second test, and it is not one (Methods 3.3; Results 4.3)

- The paper frames the pairs where the LR p-value is small but the 95% intervals overlap (p = 0.006 for 1976–85 against 2006–15) as a disagreement that needs reporting. Overlap of two 95% intervals does not imply that equality is not rejected. Non-overlap corresponds to a test far stricter than 5 percent, so the disagreement is expected and says nothing.
- Replace the overlap flag by the CI of the difference (M2).
- The ten pairwise comparisons have no multiplicity treatment. For the marginal pairs (p = 0.036, 0.064, 0.106, 0.119, 0.220) say that no correction was made, or apply Holm.
- The pairs compared "at each decade's own Mc" differ in truncation point (4.9 against 4.7). Utsu's test then compares different parts of the FMD. Only the common-threshold pairs are clean comparisons. State this next to the "nine of ten" result.

### M4. The Mw-only contrast is a threshold contrast, and the Discussion's reasoning depends on it (Section 4.5; Discussion para. 2; abstract; conclusion)

- The Mw sample has Mc 5.2–5.6 and varies by decade (N = 857 in 1976–85). The full sample is evaluated at 4.7–4.9.
- Sections 4.4 and 4.5 already show that b in the full sample depends on the threshold. A drop in the Mw-only b in the late decades (0.921, 0.995) is exactly what a high threshold plus a finite upper tail (the M9.1 events in 2004 and 2011) would produce. The Discussion's argument runs: "a physical change would affect every magnitude type, yet is absent from the Mw sample". That argument is invalid when the thresholds differ. A change in the 4.7–5.2 range would not need to show above 5.2.
- Cheap decisive checks with the data already loaded:
  - Compute the full-sample b at fixed thresholds of 5.2, 5.4, 5.5 and 5.6 for each decade. The shift table stops at +0.3 above baseline.
  - Compute the Mw-only b at one common threshold that is complete in all decades (about 5.6), together with the full-sample b at the same threshold.
  - If the two agree, the "Mw contrast" disappears. If they differ, the type effect is real at equal thresholds.
- The paper's own constraint (no Mw-only b at 4.9) is sound. It does not forbid a common threshold above the Mw sample's Mc.
- Until this is done, take the Mw-only sentence out of the abstract and conclusion ("largely disappears").
- Selection into the Mw type depends on event size. The Mc and mode rules assume an unselected FMD. Note this when reporting the Mw-only Mc values.

### M5. Statements on M>=6 and M>=7 counts contradict the reported numbers (Section 4.1; Discussion para. 1)

- Decade means at M>=6 are 106, 154, 145, 165, 133. At M>=7 they are 11.2, 13.6, 14.6, 16.8, 13.4. At M>=5 they are 1596, 1617, 1391, 1993, 1750.
- All three series peak in 2006–2015 and fall in 2016–2025. They differ in the first decades (lower at M>=6 and M>=7) and in the 1996–2005 dip, which is present at M>=5 only.
- The Discussion says "the counts at magnitudes 6 and 7 do not share this shape", and Section 4.1 says the thresholds "do not move together". Both overstate the difference.
- The inference "which is what a change of magnitude scale, and not a common change of the rate, would produce" is not supported. A common rate change is equally compatible with a peak at all thresholds. Differences between thresholds also arise from aftershock clustering, which weights thresholds differently.
- A concrete mechanism that could be tested is missing. The low M>=6 and M>=7 counts in 1976–85 fit mb saturation, since mb is the preferred type for 77.5 percent of events then. The M>=5 dip in 1996–2005 coincides with the maximum Mw share, which fits Mw being lower than mb near M5. Report the M>=5 counts by type (`n_m50_mw`, `n_m50_mb`, `n_m50_ms` already exist) per decade and say which reading they favour. Keep the caveat that type assignment is not random.

### M6. "No persistent direction" is stronger than the evidence (abstract; Sections 4.1, 5; conclusion)

- The Poisson log-linear slope is +0.40 percent per year with a robust 95% interval excluding zero (0.13–0.68). The NB interval also excludes zero (0.06–0.73). The text dismisses both because of serial clustering, but then does not offer a serial-correlation-robust interval.
- At the common threshold of 4.9, the Spearman correlation with year is 0.51. With n = 50 that is p of about 0.0002. The paper reports the correlation without a p-value or CI and gives no slope for 4.9. The text offers no explanation for 0.51 against 0.27, and none is needed. But it follows that "no steady rise" depends on whether the threshold is 4.9 or 5.0.
- Compare the means of the first two and last two decades. At 5.0 they are 1607 and 1871 (+16 percent). At 4.9 they are 2029 and 2542 (+25 percent).
- The rule "describe a change only where decade means show it" is applied selectively. Decade means rise 1976→2015 apart from one dip, and they fall in the last decade.
- Fix:
  - Give decade means with intervals (bootstrap over years).
  - Give a trend interval that accounts for autocorrelation (HAC, or year-block bootstrap), at both 5.0 and 4.9.
  - Rewrite the conclusion as: non-monotone, with a dip in 1996–2005 and higher levels after 2006, a pattern that depends on the threshold.
  - "The popular statement that earthquakes are increasing is therefore not supported" should become a statement about the catalogue.

### M7. The completeness claim at M5 is misread (Section 4.2)

- The text says that GFT at 5.0 ranges from 94.0 to 98.8 percent, "so the catalogue is complete at the level used for the yearly counts in each decade under these rules".
- 94.0 is below the 95 percent criterion the paper itself uses for one of its rules. Under that rule, 1996–2005 fails at 5.0.
- The GFT also measures the fit of a straight line, not completeness. A good fit is compatible with an incomplete catalogue, and a poor fit with a kinked FMD.
- Rephrase: the 90 percent rule is met; the 95 percent rule is not in one decade.
- Mc is estimated from the FMD and cannot show completeness for events that were never recorded, which is why the M4.5 floor matters (M1).

### M8. No figure shows the frequency–magnitude distribution

- The paper's two figures are the annual counts and the Mw share. The data summary says that FMD plots with Mc, b with intervals, and Mc over time are "not produced".
- For a paper about b-values and Mc, the reader cannot see linearity, kinks near M5, heaping at x.0 or x.5, or where each Mc sits. The central claims (slope change near 5 in 1996–2005, floor-driven Mc) are therefore not inspectable.
- Add, saved from `estimation_results.json`:
  - the non-cumulative and cumulative FMD per decade, on a log scale, with Mc marked and the GR line overlaid;
  - b against threshold per decade, with the year-block intervals.
- The shift table is the numerical form of the second plot but is hard to read.

## 3. Should change

- **S1. Counts of events near the threshold.** The 0.1 binning and the published magnitude are used for different parts of the analysis. The paper discloses this and the counts match `eq_annual_counts`. Two points remain. Report b's N and the count's N side by side at each shared threshold. The reported N of 20,023 against 20,020 events at M>=4.9 in 1976–85 looks consistent, but the difference should be explained as arising from the two-decimal magnitudes. State the rounding rule (half-up or half-even) for the 909 events with two decimals, because floating-point rounding at x.x5 is ambiguous.
- **S2. Upper-magnitude truncation.** Estimated at Mc of 5.2–5.6 with M up to 9.1, the b-value is sensitive to the few giant events. The Mw-only b-values of 0.84–1.03 may reflect this. Say that no truncated-GR likelihood is used, and give b with the M>=8 events excluded for the Mw-only sample. This is an easy sensitivity check.
- **S3. Suspicious equal values.** In the text, b for 1996–2005 is 1.055 under the maxc+0.2 rule at Mc 4.7, and also 1.055 under the GFT 95 and GFT 90 rules, which the text says return Mc 4.5. A b of exactly 1.055 at two different thresholds, while the shift table gives 1.003 at 4.8, is improbable. Either the GFT Mc for 1996–2005 is actually 4.7 (then the text "4.9, 4.7, 4.5, 4.5, 4.5" and the statement that three decades are censored need correcting) or a table cell is copied. Check this against `estimation_results.json`.
- **S4. Level-off claim for 1976–85.** "Levels off between +0.2 and +0.3" rests on 1.191 against 1.175. With N around 10^4 the SE is about 0.01, so this is a 1.5 SE difference, and it is not a plateau test. Show the intervals or soften the sentence.
- **S5. The slope change near M5 in 1996–2005.** Currently offered as a "distribution whose slope changes near magnitude 5". Name the competing explanation (the splice of mb below about 5.5 and Mw above it) and test it with the FMD by type in that decade, if the data allow.
- **S6. The shallow check is weak.** Shallow events are about 77 percent of the sample, so this subsample is nested and highly overlapping. It can only show that the shallow part reproduces the whole. The conclusion that "the mix of shallow and deep events does not explain the variation" would be better tested with the deep events (>70 km) separately, or with a note about the limited power.
- **S7. Bootstrap description.** Give the actual seed (20260101 in the specification), the number of replicates and the resampling unit in the Methods. State the version of the NB estimator and its dispersion parameter.
- **S8. Dispersion index.** The overall index of 56.7 pools the between-decade shifts in the mean with the within-decade variation, and the index is not a test. A test statistic or bootstrap p-value would replace "far larger than a Poisson process would produce". The per-decade values (5.4 to 69.2) are more informative than the pooled one.
- **S9. Attribution of 2010 and 2011.** "Coincide with the aftershock sequences ... we do not test this" is acceptable as stated. A simple check with no declustering would be to report the number of M>=5 events within, say, 1000 km and 1 year of the M>=8.5 events, or the count with those events removed. It is within the researcher's cuts only if no declustering algorithm is used.
- **S10. Decade boundaries.** The dip and peak are located by decade edges. Add five-year means in a table or in the figure so the reader can see whether the pattern depends on where the windows are cut. This is not a sliding-window analysis.

## 4. Nice to have

- Heaping diagnostics for the last digit of the magnitude by decade, and a re-estimate of Mc with 0.2 bins (the descriptive skill asks to check a second bin width).
- Give the Aki-type SE column only in the table. The text paragraph comparing the two SEs adds little, since both ignore dependence.
- The 211 near-duplicate pairs are flagged and not removed. State their share (about 0.08 percent) and that a run without them leaves counts effectively unchanged, or run it.
- Report the p-value for the Spearman correlations at both thresholds, and the Spearman CI by bootstrap over years.
- Label the "robust" Poisson interval explicitly as heteroskedasticity-robust (HC), not serial-correlation-robust.

## 5. Checks of the numbers (what I could verify)

All of the following are consistent with the data summary.
- Sample flow: 278,508 raw rows, 562 removed, 277,946 retained; the decade totals sum to 277,946.
- M>=5 total: the decade counts sum to 83,469 and the mean is 1,669.4.
- Decade means: 1,595.9, 1,617.4, 1,390.6, 1,992.8 and 1,750.2.
- Minimum and maximum: 1,077 in 1998, in the 1996–2005 decade, and 2,701 in 2011, in the 2006–2015 decade.
- Mw share per decade, and the 51 percent overall (42,956 of 83,469).
- Dispersion indices: 5.4 for 1986–95, 69.2 for 2006–15, and about 56.8 overall.
- The +24.9 percent (2006–15 against 1976–85).
- The Aki and Shi–Bolt SEs: for 1996–2005, 1.055/√31,143 = 0.0060, close to the quoted 0.0059.
- The spread 1.2201 − 0.9236 = 0.2965.
- The LR p-values match chi-square(1): 2.4 gives 0.12, 7.6 gives 0.006, 4.4 gives 0.036, 2.6 gives 0.107, 1.5 gives 0.22. The paper's 3.4 gives 0.065 against 0.064 reported, which is rounding of the statistic.

Not verifiable: the tables, the cell values of the GFT results (see S3), the bootstrap intervals beyond those quoted, and the script itself. Claims about the table contents rest on the "src" comments only.

## 6. Reproducibility

- The analysis depends on a live web service. The catalogue is revised after the fact, and the paper does not give the access date. The data dictionary has SHA-256 hashes for the downloaded files, so state the access date and ship the CSVs, or state that the hashes are the reference.
- The bootstrap is seeded (20260101 per the specification), but the paper only says "a fixed seed". Give the value and the library versions (statsmodels for Poisson and NB).
- 2025 events may still be revised. The reviewed share is 99.5 percent or more, so the effect is small, but say it.
- I could not confirm that the script reproduces the counts at mag >= 5.0 as the researcher's instruction requires. The paper's numbers agree with `eq_annual_counts`, which is a good sign.

## 7. Claims within the design

The language is mostly descriptive, and no causal claim is made. Two exceptions:
- "A physical change in the size distribution would affect every magnitude type" (Discussion) is an inference about mechanism that rests on the invalid threshold comparison in M4.
- "which is what a change of magnitude scale ... would produce" (Section 4.1) is a causal reading of a pattern that other mechanisms produce as well (M5).

## 8. Sensitivity

The paper does well on sensitivity to the completeness rule, the fixed threshold and the Mc shift. It is weak on sensitivity to the resampling unit (M2), to thresholds above 5.2 in the full sample (M4), to the decade boundaries (S10), and to the count threshold (M6). The conclusion on b being "not stable" survives the sensitivity analyses in direction. Its size and the claim that Mw-only removes it do not.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
