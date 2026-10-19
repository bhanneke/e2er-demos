# Plausibility Review: yearly M>=5 counts and Gutenberg-Richter b-value, ComCat 1976-2025

Scope: I read the draft as a seismologist would. I did not redo the mechanical number tracing. I did recompute a few relations between reported numbers to see whether they hang together. Statements that come from my own knowledge, not from the paper, are marked "(own knowledge)".

## 1. What is plausible (checked)

- **Annual M>=5 count, about 1,670 per year (range 1,077 to 2,701).** This is in the usual range for a global catalogue with aftershocks. (Own knowledge: USGS summary tables list roughly 1,300 to 1,600 events per year in M5-5.9 and about 130 to 150 per year at M6 and above.) The M>=6 means of 106 to 165 per year and the M>=7 mean of 13.9 per year are also reasonable. Both are slightly below the long-run "about 15 per year" for M7+, which fits a preferred-magnitude catalogue that is mb-dominated early on.
- **Dispersion indices.** I recomputed them from the reported SDs: 93.1² / 1617 = 5.4, 371.4² / 1993 = 69.2, and 307.8² / 1669 = 56.8. They match. Values far above 1 are expected for a catalogue that keeps aftershocks.
- **Magnitude and depth summaries.** The maximum of 9.1 is Tohoku or Sumatra. The magnitude mean (4.87) and SD (0.405) are what an exponential tail with b of about 1.1 above about 4.45 gives. A shallow share of 77 percent at 70 km or less is normal.
- **Standard errors.** Aki's b/sqrt(N) is 1.055/sqrt(31,143) = 0.0060. This matches the reported 0.0059 to 0.0063. The bootstrap widths (for example 1.151 to 1.173) are consistent with the Shi-Bolt SEs.
- **Equality tests.** A difference of 0.013 between 1.149 and 1.162 with SEs of 0.006 to 0.007 gives z² of about 2, matching the reported 2.4. A difference of 0.026 gives z² of about 7, matching the reported 7.6. So the tests are internally coherent.
- **Magnitude-type shares.** Weighting the Mw shares by the decade M>=5 counts gives about 42,950 Mw-family events. The paper reports 42,956, which is 51 percent. This is coherent.
- **Rows removed.** The 329 nuclear explosions in 1976-85 and 130 in 1986-95 fit the Cold War testing record. Removing them is correct.
- **Mc at 5.0.** The goodness-of-fit values of 94 to 98.8 percent are plausible for the main threshold.

## 2. Implausible, unexplained or over-interpreted patterns

### 2.1 Mw share falls after 1996-2005 (77, 63, 59 percent)
- **Where:** Section 3, magnitude-type mix.
- **Problem:** The paper treats the rise in Mw share as the story but never explains the decline afterwards. (Own knowledge: NEIC routinely computes Mww for M5+ events from about 2000 onwards, so I would expect the share to stay high or rise. A fall suggests that more M5.0-5.4 events carry mb in the later decades, or that the 1990s Mw labels come from a different source such as GCMT-derived "mw".)
- **Why it matters:** The 1996-2005 dip in counts and the 1996-2005 dip in b coincide with the Mw peak. Both observations are exactly where a label-source change would act, and the paper cannot interpret them without knowing the source.
- **Check:** Tabulate magType by net, by year, and by 0.1 magnitude bin for 4.5-5.5. Report counts of events in 5.0-5.4 by type per decade.

### 2.2 Median depth of exactly 33.0 km
- **Where:** Data section.
- **Problem:** A median of exactly 33.0 km is a sign of a default or fixed depth. (Own knowledge: NEIC fixes poorly constrained depths at 10 or 33 km.) The depth variable is therefore partly an artefact, and the "shallow" cut at 70 km is only a weak proxy for tectonic setting.
- **Interpretation:** The statement that the shallow check shows "the mix of shallow and deep events does not explain the variation" is only as strong as this proxy. The check is also close to uninformative: 77 percent of events are shallow, so the subsample overlaps the full sample heavily.
- **Check:** Report the share of events at 10 km and at 33 km by decade. Use a subsample with free-depth solutions only, if the field exists.

### 2.3 Standard errors of 0.006 to 0.008 and "nine of ten pairs reject at 1 percent"
- **Where:** Abstract, Results (b-value by decade).
- **Problem:** A relative precision of 0.6 percent for a global b-value, from a catalogue of heavily clustered aftershocks, is not credible as a measure of uncertainty. Effective independent sample size is far smaller than N. Mc selection error alone moves b by 0.05 to 0.1 in the sensitivity table. Magnitudes with heaping and mixed types add more.
- **Interpretation:** The paper mentions the dependence in the limitations, but the abstract and conclusion state the rejections as a result. A reader of the abstract will take them as evidence of a real instability.
- **Check:** Put the dependence caveat into the abstract. Show the b-value spread caused by Mc choice next to the sampling error. Compare the observed between-decade spread with the spread from year-block bootstrap (resampling whole years), which respects the clustering at no extra method cost.

### 2.4 Full-sample b of 1.15 to 1.22 versus a global benchmark of about 1
- **Where:** b-value results, Discussion.
- **Problem:** (Own knowledge: global b-values from Mw-based catalogues such as GCMT are close to 1.0, with common estimates of 0.9 to 1.05.) The Mw-only estimates here (0.84 to 1.03) agree with this. The full-sample values of 1.15 to 1.22 in the later decades do not. The paper never states the benchmark, so the reader cannot see which sample behaves normally.
- **Missing mechanism:** The most common reason for b above 1 in an mb-dominated sample is mb saturation and the mb-Mw relation at M5-6 (own knowledge). Mb compresses the upper tail, which steepens the distribution. The paper leaves this unmentioned, though it is the leading candidate for the "catalogue change" reading.
- **Check:** Report b separately for mb-only events at a common threshold, if the sample is large enough. State the benchmark of about 1.0 and say which sample agrees with it.

### 2.5 Raw counts imply a non-Gutenberg-Richter shape near 4.9-5.0
- **Where:** Mc sensitivity, counts at 4.9 versus 5.0.
- **Problem (a):** For 2016-2025 the ratio of mean counts at M>=4.9 and M>=5.0 is 2,449/1,750 = 1.40. A Gutenberg-Richter slope with b = 1.22 gives 10^0.122 = 1.32, and b = 1.15 gives 1.31. The local slope between 4.9 and 5.0 is therefore near 1.46. The excess in the 4.9 bin is a sign of rounding, heaping or a magnitude-type seam at 5.0.
- **Problem (b):** For 1996-2005, the ratio N(M>=4.5)/N(M>=5) is 3.67, which implies b of about 1.13 over 4.5-5.0. Above 4.9, b is only 0.92. The frequency-magnitude distribution is concave there. The paper's inference of "a slope change near magnitude 5" is well supported by its own raw counts. It should say so and show it.
- **Check:** Plot the non-cumulative frequency-magnitude distribution per decade with the bin counts from 4.5 to 5.5, by magnitude type. This figure was in the first plan and was dropped; it is the figure most needed here.

### 2.6 1976-85 baseline Mc of 4.9 looks too low
- **Where:** Mc sensitivity.
- **Problem:** In 1976-85 b rises from 1.123 at 4.9 to 1.191 at +0.2 (5.1), then falls to 1.175 at +0.3. By the paper's own rule that rising b means incompleteness, the baseline at 4.9 is still within the incomplete range. A plateau is reached at about 5.1, not at 4.9. This agrees with the large deficit in M>=4.5 counts in that decade (36,781 events at M>=4.5 against 15,959 at M>=5, ratio 2.3, which would mean b of about 0.4 over 4.5-5.0).
- **Interpretation:** The common-threshold comparison at 4.9 therefore puts a probably incomplete first decade next to complete later ones. The "dip moves to 1996-2005" statement and the spread of 0.30 are affected.
- **Check:** Redo the common-threshold table at 5.1 and report the decade ranking.

### 2.7 Counts at M6 and M7 "do not move together" with M5
- **Where:** Counts section, Discussion.
- **Problem (a):** The decade means for M7 (11.2, 13.6, 14.6, 16.8, 13.4) peak in 2006-15 and fall in 2016-25, the same as M>=5 for the last two decades. M6 also peaks in 2006-15. Only the 1996-2005 dip is not shared. "Do not share this shape" is too strong.
- **Problem (b):** The conclusion that divergence "is what a change of magnitude scale would produce" does not discriminate. Clustering alone produces it: M5 counts are dominated by a few aftershock sequences, while M7 counts are close to independent mainshocks. A decade mean of 11 to 17 M7 events per year has Poisson noise of roughly 10 percent, comparable to the movement in the table.
- **Check:** Add the decade-mean SE for M7. Report the share of the yearly M5 count contributed by the largest single sequence, or at least check the top five years by hand against known sequences (2004/2005 Sumatra, 2010 Maule, 2011 Tohoku, 2025 Kamchatka).

### 2.8 The 1996-2005 dip despite Sumatra 2004 and Nias 2005
- **Where:** Counts section.
- **Problem:** This decade contains the 2004 Sumatra-Andaman and 2005 Nias sequences, yet it has the lowest decade mean (1,391) and the minimum year (1,077 in 1998). Aftershocks are used in the paper to explain the 2010 and 2011 peaks but cannot explain a low decade that contains giant sequences. This points to a catalogue effect (processing, magnitude type) in the 1990s, which the paper only hints at.
- **Check:** Show the yearly series with mainshock years labelled. Look for a step in 1996-1998 and compare with the magnitude-type mix by year, not by decade. Decade averages hide the date of any change.

### 2.9 Counts "not stable" is not evidence of a physical instability
- **Where:** Abstract, Conclusion.
- **Problem:** With dispersion indices of 5 to 69, decade means differ by several hundred events per year from clustering alone. (Own knowledge: Shearer and Stark found annual counts of the largest events consistent with random variability.) The abstract's "neither the counts nor the b-value is stable" invites a physical reading that the paper elsewhere disclaims.
- **Fix:** Say that the decade means differ by more than annual Poisson noise but that no clustering-aware null is available in this scope, so the size of the differences cannot be judged against expected clustering.

### 2.10 The Mw-only contrast is used for more than it can bear
- **Where:** Discussion.
- **Problem:** "A physical change in the size distribution would affect every magnitude type, yet it is absent from the Mw sample" assumes that a change in b is the same at 4.7-5.2 as above 5.2-5.6. A scale-dependent change in the frequency-magnitude distribution is physically possible. The Mw sample has Mc of 5.2 to 5.6 and far fewer events (857 in 1976-85, so SE about 0.03), and its decade-to-decade spread is within a plausible range of sampling and Mc noise. The paper does hold both readings open, but this sentence leans on one of them.

### 2.11 Smaller points
- **Unexplained sign of Mc shifts at -0.3.** The paper handles this correctly (nominal Mc below the load floor), but the first-decade values at -0.3 (0.912) are plotted beside the others as if comparable.
- **Event-type removals.** 71 "volcanic eruption" rows in 2016-2025 are removed. Confirm none is a tectonic earthquake mislabelled by type; M>=4.5 volcanic events at this number are unusual.
- **Unlabelled explosions.** Early-decade explosions that are not typed as such stay in the 1976-85 count, in an mb-dominated, explosion-heavy period (own knowledge). The effect is probably small at M>=5 in the total count, but it is not quantified.
- **2025 completeness.** The "100 percent reviewed" claim for 2025 should be stated with the load date, since magnitude revisions still occur.
- **The 4.9 versus 4.95 threshold.** Counts use mag >= 5.0 on published values while Mc and b use 0.1-rounded magnitudes. The paper notes this. The 96 events between 4.9 and 5.0 with two decimals are too few to matter for the main results.
- **Global Mc.** A single global Mc per decade mixes regions with different detection. The maximum-curvature mode sitting at the load floor (4.5) is also a sign of censoring, not of an observed peak. The paper states the censoring but still reports the corresponding b-values at 4.7 as "decade-specific" estimates.

## 3. Statements that are well calibrated
- The point that incompleteness lowers b and does not raise it is used correctly.
- The sentence that the 5.0 versus 5.5 count difference is not a detection share is right.
- The explicit refusal to attribute the 2010-2011 peaks without a test is appropriate.
- Reporting both the likelihood-ratio test and the bootstrap overlap for the disagreeing pairs is honest.

## 4. Summary of checks that would settle the main questions
1. Per-decade non-cumulative frequency-magnitude plot, 4.5-5.5, split by magnitude type.
2. Magnitude-type and network mix by year (not decade) in the 5.0-5.4 range; explain the fall in Mw share after 2005.
3. Common-threshold b and counts at 5.1.
4. Year-block bootstrap for the b-value and the decade means.
5. Share of default depths (10 and 33 km) by decade.
6. A hand check of the five largest yearly counts against known sequences.

## 5. Plausibility score
The reported numbers are physically reasonable and internally coherent, and the paper is cautious in its conclusions. The scientific weaknesses are interpretive: the unexplained Mw share decline, an under-stated dependence problem for the SEs, a 1976-85 baseline that is probably incomplete, a missing benchmark for b near 1, and a count argument (M5 versus M7) that is not diagnostic. These can be fixed with text and a few extra tables without new modelling.

OVERALL SCORE: 6.5/10
RECOMMENDATION: Minor Revision
