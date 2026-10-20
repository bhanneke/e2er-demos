# Plausibility Review: Pleiades membership, parallax distance and CMD from Gaia DR3

Scope: the numbers and patterns in the draft, read against what the Pleiades and Gaia astrometry should show. Every number was checked against the draft and `estimation_results.json` as quoted in the context. Points drawn from general knowledge of the field are marked **(knowledge, unverified here)** and need a cited source before the paper relies on them.

## 1. Checks that pass

- **Distance and modulus.** 1000 / 7.3666 mas = 135.75 pc, matching the median of 135.7 pc. The distance modulus 5 log10(135.7) − 5 = 5.66 mag matches.
- **Distance uncertainty.** Propagating the standard error of the mean, 0.00691 mas, gives 1000 × 0.00691 / 7.3666² = 0.127 pc. The draft's 0.13 pc is correct. The distance standard deviation of 4.3 pc matches 18.4 pc/mas × 0.230 mas.
- **Magnitude of the parallax and distance.** A parallax of about 7.37 mas (about 136 pc) is in line with the Pleiades distance from Gaia-era work **(knowledge, unverified here)**. The distance lies inside the 125–145 pc reference band, and the paper does not overstate the agreement.
- **Proper motion.** The centre (19.87, −45.42) mas/yr is close to the commonly quoted Pleiades motion of about (+20, −45) mas/yr **(knowledge, unverified here)**.
- **Internal velocity dispersion.** At 136 pc, 1 km/s corresponds to about 1.55 mas/yr. Member proper-motion standard deviations of 1.08 and 1.41 mas/yr therefore correspond to roughly 0.7–0.9 km/s. That is a plausible internal dispersion for a young open cluster, once measurement error is added **(knowledge, unverified here)**.
- **Field parallax.** The quality-sample median of 3.26 mas (about 300 pc) and the naive full-sample centre of 3.19 mas are consistent with a field dominated by stars at a few hundred parsecs at this latitude.
- **Grid arithmetic.** The minimum of 913 is −17.9% from 1,112, and the maximum of 1,184 is +6.5%. The one-at-a-time maximum of 7.9% (1,024) is correct.
- **Colour bins.** The 16th–84th spread at G = 6–7 is 0.075 mag, and the draft's 0.40 mag at G = 14–15 is correct as stated.
- **Locus against the modulus.** Converting the bin medians to absolute magnitude with the modulus 5.66 gives M_G ≈ 0.5 at BP−RP ≈ 0.0, and M_G ≈ 6.8 at BP−RP ≈ 1.4. At G = 17.5, M_G ≈ 11.8 at BP−RP ≈ 3.3. These fall where a young solar-metallicity main sequence should, with small reddening **(knowledge, unverified here)**.
- **Reddening.** E(B−V) ≈ 0.04 mag implies an E(BP−RP) of only about 0.05 mag, so leaving colours uncorrected shifts the locus very little. The draft's "slightly red" is correct.
- **Zero-point sign.** The Lindegren et al. (2021) offset is negative, so the correction increases the parallax and lowers the distance. A +0.03 mas shift lowers the distance by about 0.4%, as the draft says.

## 2. Implausible or unexplained patterns

### 2.1 Non-monotonic member counts at G = 13–16 (unexplained)
Member counts per one-magnitude bin, from the draft: 13–14: 65; 14–15: 59; 15–16: 142; 16–17: 250; 17–18: 228. Below G = 13 the counts rise steadily (10, 14, 18, 32, 37, 41, 46). A cluster mass function rises toward fainter magnitudes, and the parallax-over-error cut at 10 removes stars only near G ≈ 19–20, where the error reaches 0.7 mas. A drop by a factor of about 2.4 between G = 13–14 and 15–16 is not explained by either effect.
**Check:** tabulate, per G bin, the quality-sample count, the count with a null `bp_rp`, the count inside the parallax window only and the count inside the proper-motion radius only. Identify which cut or photometric gap produces the dip before the paper interprets the locus at those magnitudes.

### 2.2 The locus spread at G = 14–15 mixes slope with scatter
The bin medians rise steeply across the bin: 1.81 (G 13–14), 2.28 (14–15), 2.67 (15–16). The colour changes by about 0.4–0.5 mag per magnitude there, so a one-magnitude bin spans about 0.4 mag of colour before any scatter. The 16th–84th spread of 0.40 mag at G = 14–15 is therefore close to the bin's own slope and says little about the width of the sequence. The draft's statement that the locus is "widest" there is an artefact of the binning.
**Check:** report the spread of residuals from a smooth fit to the locus, or use narrower bins (0.5 mag), and state the within-bin slope next to each spread. Also report the median photometric error in `bp_rp` per bin, since it sets the expected width at the faint end.

### 2.3 "Several magnitudes brighter" overstates the bright-end gap
The draft says the named B stars are "several magnitudes brighter" than the brightest member (G = 5.20). The extract's own numbers show the five excluded stars lie at G = 3.62–4.26, which is 0.9–1.6 mag brighter. Alcyone, if present, would be about 2.3 mag brighter. These are one to two magnitudes, not several.
**Fix:** state the measured offsets (0.9–1.6 mag for the five stars) and say that the brightest named members are not in the extract at all, if that is what the cross-match shows.

### 2.4 Bright-star identities are not checked
The five excluded stars all have RUWE of 2.31 or more. Saturation and nebulosity around the brightest Pleiades stars are known to degrade Gaia astrometry **(knowledge, unverified here)**, so the RUWE result is plausible. But the draft never says which named stars these five are. Alcyone (the brightest cluster star, G around 2.9 **(knowledge, unverified here)**) would fall outside the reported range of 3.62–4.26, so its absence from the extract is a separate question.
**Check:** cross-match the five stars and any named Pleiades B stars within the cone by position to a catalogue (for example, SIMBAD) and record their names, their astrometric solution codes and whether they are in the extract at all. Report the result in the bright-end paragraph.

### 2.5 Distance spread is attributed to scatter without a test
The paper says the 4.3 pc spread "is the star-to-star scatter ... and is not a measure of the cluster's depth." But the observed parallax standard deviation of 0.230 mas includes the members' measurement errors, and it may also include real depth. A depth of ±5 pc at 136 pc corresponds to about ±0.27 mas. The cluster's physical extent is of order 10 pc **(knowledge, unverified here)**, so depth could be a material part of the spread.
**Check:** compute the median and root-mean-square of the members' `parallax_error`, and report the intrinsic spread as √(σ² − mean(error²)). Then state how much of the spread is measurement error and how much might be depth. This test is also needed for the "depth" sentence to be checkable.

### 2.6 Omission of the Hipparcos–Gaia distance discrepancy
The Pleiades distance has a well-known history: Hipparcos gave about 120 pc, while VLBI and Gaia give about 133–136 pc **(knowledge, unverified here; see van Leeuwen 2009 and Melis et al. 2014, to be verified)**. The draft's distance of 135.7 pc sits with the Gaia and VLBI side of that discrepancy. A reader will expect the discussion to say so, and the paper's silence on it is the most visible gap in the distance comparison.
**Fix:** after verifying the sources, state the Hipparcos and VLBI values in the discussion and say which side the Gaia value supports. Keep the uncorrected-parallax caveat with it.

### 2.7 Contamination is said to be untestable, but an annulus test exists
The limitations say the data "cannot estimate the contamination rate." The draft already has the necessary inputs: 233 quality stars inside the parallax window fall outside the 5 mas/yr proper-motion circle. Counting window stars in a proper-motion annulus just outside the circle, and scaling by area, gives a field-density estimate that bounds contamination inside the circle.
**Fix:** run that annulus count and report the estimated contaminant fraction. If it is small (a few per cent), the limitation can be stated with a number. If not, the membership count needs qualifying.

### 2.8 Proper-motion anisotropy is not discussed
The dispersion is 1.08 mas/yr in right ascension and 1.41 mas/yr in declination. A 30% difference is mild and could come from projection or from the cluster's internal motion. The draft does not comment on it.
**Fix:** one sentence noting the anisotropy, or a check that it persists among bright stars with small errors.

## 3. Presentation points (plausibility of the figure)

- The CMD in `fig_cmd.pdf` shows G increasing upward, so the main sequence runs up and to the right. Readers expect bright stars at the top, and the draft's caption says it is non-standard. This does not change the numbers, but it is hard to read against the literature. Consider inverting the axis, or give the reason for not doing so in the caption.
- The distance histogram (`fig_distance_hist.pdf`) is not listed in the estimation results figure list. The parallax histogram is described in the text but cannot be checked against a file from the results.

## 4. Summary

The headline numbers are plausible for the Pleiades. The distance of 135.7 pc, the proper motion, the reddening-limited colours and the locus against the modulus all agree with what is expected. The arithmetic is correct throughout. The main weaknesses are interpretive. The unexplained count dip at G = 13–16 (2.1) needs a cut-by-cut check before the locus is described. The locus spread (2.2), the "several magnitudes" wording (2.3), and the depth statement (2.5) each claim more than the numbers support. The paper also omits the Hipparcos–Gaia discrepancy (2.6), and it understates what its own inputs can say about contamination (2.7).

Priority fixes, in order: (1) explain the G = 13–16 count pattern; (2) recompute the locus spread on residuals or narrower bins; (3) correct "several magnitudes" and identify the five bright stars; (4) add the intrinsic-depth estimate; (5) add the annulus contamination estimate; (6) add the Hipparcos and VLBI comparison once the sources are verified.

OVERALL SCORE: 7/10
RECOMMENDATION: Minor Revision
