# Plausibility Review

Paper: "How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance"

## Overall assessment

Most of the numbers in this paper are plausible for the NASA Exoplanet Archive (NEA) and internally coherent. I checked several of them by arithmetic from the counts and quantiles given in the draft.

- The group sizes add up: 4,810 + 1,215 + 20 = 6,045. The 80/20 split is also right (79.6 percent and 20.1 percent).
- The radius medians and period medians give ratios of 5.1 and 45, which match the log differences of 0.71 and 1.65 (10^0.71 = 5.1, 10^1.65 = 45).
- The radius-bin counts are consistent with the pooled quartiles:
  - Planets below 2 R⊕ come to about 29 percent (6,045 − 4,040 − 220 = 1,785).
  - The median then falls in the 2 to 4 bin, as reported.
  - The third quartile (10.9 R⊕) falls in the 8 to 15 bin, as reported.
- The calculated group has 276 + 186 + 176 = 638 planets above 300 days, which is 52.5 percent of 1,215. That agrees with a median period of 358.6 days. The 29.8 percent above 1,000 days agrees with a third quartile of 1,277 days.
- The 189 planets above 3,000 days are the 176 calculated, 1 transit-measured, and about 12 of the 20 non-transiting planets. That matches the median period of 15,958 days for the last group.
- The mass-provenance split (876 + 326 + 13 = 1,215) and the method split (4,778 + 32 = 4,810) are consistent. The 322 calculated planets with no period are mostly microlensing, which explains why "Mass" drops from 648 to 326.
- The raw-sample count of 6,445 and the 4,778 transit discoveries are plausible for an October 2026 archive snapshot (my own knowledge: the archive held roughly 6,000 planets in late 2025).

The problems are in how some numbers are produced, labelled and interpreted. One is a probable circularity that would invalidate a stated comparison. The others are largely tautological or overstated readings.

## Implausible or unexplained numbers and patterns

### 1. Rank correlation of 0.93 for "transit-measured planets with a mass" (Section 3.3, Mass-radius diagnostic). Most serious.

The draft sets a rank correlation of 0.47 for calculated radii against 0.93 for "the 4,786 transit-measured planets with a mass". The data dictionary says `pl_bmasse` may be "a mass from a mass-radius relation" (see `pl_bmassprov`). The count is also suspect: 4,786 of 4,810 transiting planets have a mass. In reality only a minority of transiting planets have a dynamically measured mass (a few hundred to about a thousand; my own knowledge). The archive fills the rest with relation-derived masses computed from the radius.

A rho of 0.93 is therefore very likely the same Chen and Kipping relation applied in the opposite direction, not a physical mass-radius correlation. The comparison would then be circular and could mislead the reader about the 0.47.

Check that would settle it: split the 4,786 by `pl_bmassprov` and by whether `pl_bmasse_reflink` is "Calculated Value" or a mass-radius paper. Report rho for planets with an observed mass only. The number "4,786" is also not in the cited results as a measured-mass count and needs a caveat.

### 2. "Directly measured radii" for non-transiting planets (Introduction; Section 2.2).

The 48 measured, non-transiting planets are 41 imaging, 2 orbital brightness modulation and 5 radial velocity (data summary). Radii of directly imaged planets are normally inferred from evolutionary cooling models and luminosity (my own knowledge), not measured. The text "directly measured radii" is therefore not warranted. Their median radius of 13.0 R⊕ is what such models give for young, massive objects.

The draft also lists "timing methods" as an example, but the data summary shows no timing planets in this group. The examples contradict the data.

Check: look at the radius references of these 48 planets.

### 3. Periods of imaged planets, up to 4×10^8 days.

Dictionary range: `pl_orbper` 0.0907 to 4.02×10^8 days. The latter is about 1.1 million years, which is not a measured period. It is a value derived from projected separation and an assumed stellar mass.

- The paper reports a median period of 15,958 days for the 20 non-transiting planets with a period, and "5 periods above 10^6 d" are kept in the sample.
- The draft never gives the maximum period or the maximum radius in the sample. Please state them, since the period statistics, the bins above 3,000 days and the rho of 0.63 (n = 20) depend on such values.
- The 87.2 R⊕ maximum radius (7.8 R_J) in the dictionary is plausibly an imaged, brown-dwarf-like object without a period, so it is outside the sample. This should be confirmed.

### 4. Largest transit-measured radius, 32.6 R⊕ (2.9 R_J), and 220 transit-measured planets above 15 R⊕.

The largest well-constrained transiting giants are about 2 R_J (about 22 R⊕; my own knowledge). A radius of 2.9 R_J is beyond any inflated hot Jupiter. It points to a poorly constrained fit, a brown-dwarf or low-mass-star companion, or a unit error in a source paper.

The data summary flags 6 radii above 25 R⊕ but keeps them.

- The share of 220 of 4,810 (4.6 percent) above 15 R⊕ (1.34 R_J) is plausible for inflated hot Jupiters.
- Without a check of the extreme values, "transit-measured radii reach 32.6" is reported as a fact about planets.

Check: list the planets above 22 R⊕ with host, reference and radius uncertainty, and say whether they were left in on purpose.

### 5. The 8 to 15 R⊕ hump in the calculated group is largely produced by the relation, not observed (Abstract, Results, Conclusion).

The headline is that 846 of the 1,529 planets in the giant hump (55 percent) are calculated. The sentence on the "calculated radii bounded at 14.3 R⊕" shows the cause. The Chen and Kipping relation maps every mass above roughly 0.4 M_J (hundreds of Earth masses; my own knowledge, not checked against the paper) to a near-constant Jovian radius of about 1 R_J, with a very shallow slope. Almost any RV giant therefore lands at 8 to 15 R⊕, whatever its true radius. A calculated radius above 15 R⊕ cannot occur, whereas 220 transit-measured planets exceed it.

- The "hump" in the calculated group is thus an output of the mapping, and the 55 percent share partly reflects the radius cap, not a measured radius.
- Section 5 of the plan expected this ("smoother and more tightly structured in R than the true radii"), but the abstract and conclusion read the counts as a feature of the hump itself.
- The limitations say calculated radii "inherit assumptions", yet no sentence says the hump position is imposed by the relation.

Check: report the calculated-group radius histogram together with the mass histogram. State how many calculated planets sit in the Jovian regime of the relation.

### 6. "The groups overlap little in the radius-period plane" (Abstract; Section 3.1).

The paper only reports marginal Kolmogorov-Smirnov distances (0.53 for radius, 0.61 for period). A distance of 0.53 is moderate, not "little overlap". The paper itself says giant planets occur in both groups, and the 90th percentile radius differs by a factor of only 1.1.

- The joint overlap that the plan promised (joint counts, share of each group inside the other's range) is not reported in the draft. The sentence in the abstract has no joint statistic behind it.
- Either report the joint cell shares, or say "marginal distributions differ clearly, with partial overlap among giant planets".

### 7. The Spearman rho of 0.40 between radius and period in the calculated group (Section 3.2).

The intro calls this association "clearly positive". With radius computed from mass, this is a mass-period association (detection effect: radial-velocity amplitude is larger for massive planets at longer periods, and long baselines favour massive companions) pushed through a relation. Section 3.3 states the radii mirror the masses, but Section 3.2 and the introduction do not connect the 0.40 to it. In the Jovian regime the relation is nearly flat or slightly decreasing, which also lowers the rho. The statement that the pooled association "describes neither" group is fine, but "clearly positive among calculated" cannot be read as a size-period relation.

### 8. "The true mass and radius may be larger" (Limitations).

A minimum mass is a lower bound on mass, so the true mass is larger. The true radius is not necessarily larger: in the Jovian regime the relation is flat to slightly decreasing, so a larger mass can give the same or a slightly smaller radius. The statement is correct for Neptunian and sub-Neptunian masses only. Please restrict it, or say "mass".

### 9. "A gap remains within the range that transit surveys cover" (Section 3.2, period ≤ 1,000 days).

Transit surveys have very low completeness beyond about 100 to 300 days for small planets and typically only a few transits at longer periods (my own knowledge: Kepler's baseline of about 4 years). The restricted transit-measured group is still concentrated at about 8 days (4,804 planets), while the 855 calculated planets within 1,000 days have a median about 12 times higher (1.07 dex). That difference is expected from transit probability (≈ R★/a) and the survey windows, so it is a difference in what each method records, not a gap in planets. The wording "gap" and "range that transit surveys cover" suggests more completeness than exists. Compare at 100 days or at 300 days as an additional cut, or drop the sentence.

### 10. Differential missingness between groups (Data, "about 20 percent").

All 4,810 transit-measured planets have a period, but 322 of the 1,537 calculated planets (21 percent) do not. These are mostly microlensing planets, plus some imaging planets. The 20 percent share, the median period and the period comparison therefore describe the calculated planets that have a period. Microlensing (292 of the calculated planets) is a significant method in the calculated group but is not mentioned in the Limitations. The draft should say that the 1,215 sample is a subset that was selected on having a period, and that the 20 percent share would be 25 percent (1,537 of 6,395) with all planets that have a radius.

## Smaller points

- **Robustness check on limit flags is trivially weak.** Only 5 radius flags and 6 period flags exist (7 planets in the sample). The unchanged medians (0.71 and 1.65) follow mechanically. This should not be presented as a robustness result.
- **Bootstrap intervals.** Resampling planets as independent ignores multi-planet systems and radii from the same paper or survey. The very narrow interval for the radius median difference (0.70 to 0.72) reflects the pile-up of calculated radii near 11 to 13 R⊕ and is likely too narrow. A cluster bootstrap by host is the natural check.
- **Radius valley.** The 2 to 4 R⊕ hump is the well-known sub-Neptune peak. The bins of the paper skip the valley near 1.5 to 2 R⊕ and the dearth of 4 to 8 R⊕ planets (421), both known features of the transit-measured sample (my own knowledge, and the literature review lists Fulton et al. 2017). The paper does not compare its fine histogram (the 0.1 dex bins exist) to them. One sentence would show that the transit-measured group reproduces known structure; at present nothing in the draft shows that the numbers agree with, or depart from, established features.
- **Chen and Kipping year.** The bib year (2016) differs from the publication year (2017). This is a citation issue, not a number issue.
- **Number of significant digits.** "A factor of 5.1 / 45 / 68 / 102" come from log differences with intervals up to ±0.08 dex; they should carry the intervals, not point values only.
- **"Median radius 12.6 R⊕ (1.12 R_J)"** for the calculated group is plausible for an RV-dominated sample. The Q1 of 4.43 R⊕ is plausible for low-mass RV planets.

## What is plausible and needs no change

- Sample flow, group counts and cross-tabulation (the 1,537 calculated all non-transiting; 48 + 50 + 1,537 = 1,635 non-transiting or radius-free planets, in line with 1,634 non-transiting planets plus 1 transiting planet without a radius).
- The statement that provenance and discovery method are nearly the same split (1,133 RV among 1,215 is plausible; the 322 microlensing/imaging planets without period are the remainder).
- The period distribution of the pooled sample (median 10.6 days, concentration at 3 to 30 days) is typical for a transit-dominated catalogue.
- The main message is sound: the catalogue is not a map of planets, and the two radius sources must be kept apart.

## Score

The numbers trace and the arithmetic holds. The gaps are one probable circular comparison (item 1), two mislabelled quantities (items 2 and 3), an extreme-value check that is missing (item 4), and several interpretive sentences that read the relation or the detection method as a property of planets (items 5, 6, 7, 8, 9). All can be fixed by a check of the archive columns and by changes to the wording, not by a new analysis.

OVERALL SCORE: 6/10
RECOMMENDATION: Minor Revision
