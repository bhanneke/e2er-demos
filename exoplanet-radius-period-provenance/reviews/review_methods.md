# Methods Review: How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance

## Scope of this review

I had the draft, the analysis specification, the data dictionary, the data summary and the plan. I did not have `run_estimation.py`, `estimation_results.json` or the four `.tex` tables. So I could not check the code line by line. I checked the text against the specification and against itself.

- Most arithmetic in the text is internally consistent.
  - 10^0.71 = 5.1 and 10^1.65 = 45.
  - 12.6/2.46 = 5.1 and 358.6/7.97 = 45.
  - 10^1.07 = 11.7.
  - The group sizes add up: 1,215 + 4,810 + 20 = 6,045.
  - 4,810 + 1,537 + 48 + 50 = 6,445.
- Findings that depend on the script are flagged as "verify in script".

Overall, the design is appropriate for a descriptive question. The paper is honest about its limits and avoids causal language. The problems are:

- one headline claim (the groups "overlap little in the radius-period plane") is not backed by a joint statistic;
- one reported number (rho = 0.93 for transit-measured planets) is probably circular;
- the interpretation of the calculated group's radius distribution is partly an artefact of the mass-radius relation;
- the sensitivity analysis is thin;
- a few reproducibility details are missing from the paper.

## What must change

### M1. The "overlap little in the radius-period plane" claim has no joint evidence (Abstract; Results, Figure 4 paragraph)

- The abstract says the two groups "overlap little in the radius-period plane". The only support is two *marginal* KS distances (0.53 radius, 0.61 period).
- Small marginal overlap does not establish small joint overlap, and the reverse is also possible.
- The specification (items 3 and 4) promised:
  - radius-bin × period-bin joint counts per group;
  - cell shares with the group n as denominator;
  - percentage-point differences between groups.
- The plan (Table 4) also promised a share of each group inside the other's support.
- None of these appears in the draft.
- The comparison that matches the research question is the radius distribution *within period bins*, for example 3–10, 10–30, 30–100, 100–300 and 300–1,000 d, by group.
  - Without it, "calculated radii are larger" cannot be separated from "calculated planets are on longer orbits".
  - The two differences are confounded in every marginal comparison.
  - The scatter figure shows this only by eye.
- Fix: add the joint table, or a stratified radius comparison with n per cell. Either drop the abstract claim or quantify it with a joint overlap statistic. Do not interpret cells with fewer than 5 planets.

### M2. The mass-radius diagnostic is probably circular for the transit-measured group (Results, "Mass-radius diagnostic")

- The text compares rho(log M, log R) = 0.47 for the calculated group with 0.93 for the 4,786 transit-measured planets that have a mass.
- The data dictionary itself says `pl_bmasse` can be "a mass from a mass-radius relation". Archive masses for transit-only planets are often derived from the measured radius.
- If so, the 0.93 mostly measures the relation, not physics. The contrast with 0.47 would then be an artefact.
- Fix:
  - Use `pl_bmasse_reflink` (already loaded) to drop masses that are themselves calculated, then recompute the 0.93.
  - If this cannot be done, state that the 0.93 may be circular and remove the comparison.
  - Say how many of the 4,786 masses are of which kind.
- The interpretation of 0.47 is also speculative: "consistent with a relation that is not increasing over the full mass range". This is untested.
  - The relation is probably flat or slightly decreasing in the Jovian regime, which is where most of the group sits (846 of 1,215 between 8 and 15 R⊕).
  - It is not shown that a deterministic relation produces 0.47 here.
  - Alternatively, radius and mass may come from different references in the composite table.
- Fix: show rho or a binned plot by mass regime, or test the claim directly by applying the stated relation to the calculated planets' masses. If that is not done, soften the sentence.

### M3. Calculated radii are model outputs, so radius comparisons between groups partly describe the relation (Abstract; Intro finding 2; Results; Conclusion)

- The paper states the caveat in Limitations. But the headline findings treat the radius difference as a descriptive contrast of planets.
  - "Typical calculated radius is about five times the typical measured radius."
  - "The giant-planet hump consists largely of calculated radii."
  - Calculated radii are "bounded above at 14.3 R⊕".
- In the flat Jovian regime, any mass above roughly 0.4 M_J maps to about 11–13 R⊕.
- So the calculated group's radius distribution is a push-forward of the Msini distribution through a saturating function.
  - The 8–15 R⊕ peak and the 14.3 cap are properties of that mapping.
  - They are not independent size information.
  - Part of the "hump" in the pooled histogram is therefore built by construction.
- The within-group rho(R, P) = 0.40 for calculated planets is the same kind of statement.
  - It is essentially rho(M, P) passed through the relation.
  - It is also shaped by RV selection, where massive planets are detectable at long periods.
- Fix:
  - Say this where the results are stated, not only in Limitations.
  - Make clear that "bounded by the relation" is an inference from the maximum of 14.3. Neither the relation nor its regime breaks are cited or checked (the literature review deliberately omitted them).
  - Name the exact relation and archive documentation version used.

### M4. The "two humps" description is thin and the second-bin-width check is not reported (Results, first subsection; Abstract)

- The humps are defined by fixed conventional bins (2–4, 4–8, 8–15 R⊕), chosen in advance, not by the data.
- The bins have similar log widths (0.30, 0.30 and 0.27 dex), so the dip at 4–8 is plausible.
- But the pooled distribution has about 2,000 planets outside those three bins, and the lower quartile is 1.79 R⊕.
  - The 1–2 R⊕ planets, the radius valley and the super-Earth peak are not mentioned.
  - "Two humps" may therefore be an incomplete or wrong description of the shape.
- The specification required a finer equal-log-width histogram "to check that features are not bin artefacts" (item 2 and robustness item c).
  - The fine bins exist in the results file. They were used for the figures.
  - The text never says whether the humps persist at the finer width.
- Fix: report in one sentence that the two features appear at both widths, with the fine width given. Describe the lower end of the distribution, or restrict the claim to "at least two features". If the comparison with the valley literature is intended, say so. The literature review lists Fulton et al. 2017 and others, but the draft does not cite them.

### M5. The sensitivity analysis does not address the main confound, and one robustness check is nearly vacuous (Results, "Calculated versus transit-measured")

- Provenance and discovery method are almost the same split: 1,133 of 1,215 calculated planets are RV discoveries.
  - The paper says so.
  - But no analysis separates the two.
- Excluding limit-flagged values removes 2 + 3 planets. The unchanged medians are guaranteed. This should not be presented as sensitivity.
- The P ≤ 1,000 d restriction is described as "common period support". That is not accurate.
  - 99.9% of transit-measured planets are already below 1,000 d, so the restriction mainly trims the calculated group.
  - It still tells us something, since the gap shrinks from a factor of 45 to a factor of 11.7.
  - A stratified comparison (M1) would be more informative. A restriction to a window where both groups have coverage, such as 10–1,000 d, would also help.
- Other sensitivity analyses that the data in hand already allow:
  - excluding the 876 Msini-based radii, which was in the plan but is not reported;
  - RV discoveries only: the 28 RV-discovered transit-measured planets against the RV calculated planets (small, so descriptive only);
  - one alternative quantile summary, for example p95, so that the "largest at the upper-middle period" statement is not tied to the five quantiles computed.
- Fix: add at least the Msini exclusion and the stratified comparison. Describe the limit-flag check as a data-quality check.

### M6. Reproducibility details missing from the paper (Data; Methods)

- The bootstrap seed (20261013 in the specification) is not in the paper. Only "2,000 resamples" is stated.
- The load date (2026-10-13) and the file hash (sha256 in the data dictionary) are not given.
  - The archive changes weekly and the data come from a live TAP service.
  - Counts will not reproduce from a later query.
  - The paper should say that the analysis uses a stored snapshot and name it.
- Bin edge convention: state whether bins are left-closed or right-closed.
  - The text gives 855 calculated planets with P ≤ 1,000 d.
  - The period bin counts 186 (1,000–3,000) and 176 (>3,000) imply 1,215 − 362 = 853.
  - The 2-planet difference is consistent with two planets at exactly 1,000 d falling in the 1,000–3,000 bin. The transit counts do match (4,810 − 5 − 1 = 4,804).
  - Check and state the convention. The checking is for the script.
- The script itself was not available to me. Please confirm the cited `% src:` keys all exist in `estimation_results.json`.

## What would be nice

1. **Bootstrap independence.**
   - The percentile bootstrap resamples planets as if independent.
   - Planets in the same system share a host star, a discovery paper and a reference.
   - The intervals (0.70–0.72 for the median log radius) are very narrow and describe only sampling variation of the catalogue rows.
   - Say this, or resample by host star (`hostname` is loaded).
2. **The n = 20 group.** A percentile bootstrap interval for rho (0.16–0.87) from 20 planets is unreliable. Report it as a count and a rank correlation without an interval, or label it unreliable.
3. **Validation of the calculated radii.**
   - The paper's future-work question is answerable now: take transiting planets that have a measured mass and compare their measured radius with the radius the relation gives.
   - This tests the relation directly and would make the paper much stronger.
   - It requires the same mass-circularity filter as M2.
4. **Sample flow.**
   - Show it sequentially: 6,445 → 6,395 with a radius → 6,045 with a period.
   - The current "drop 50 and drop 353, some lack both" is correct but harder to read.
   - Also note that requiring a period removes 322 of the 1,537 calculated planets (21%), mostly microlensing, against 0 of the transit-measured planets.
   - The period requirement therefore makes the calculated group more RV-dominated, and the 80/20 shares are conditional on having a period.
5. **Imprecise wording.** "Imaging or timing methods" for the 48 measured non-transiting planets: the data summary shows imaging 41, brightness modulation 2 and RV 5.
6. **Citation keys.** `cloutier2024exoplanet`, `foremanmackey2016the`, `nielsen2019the` and `little2019statistical` are not in the literature review's list of keys. Confirm that they resolve in `literature.bib` and support the sentences they are attached to. Remove the `% src:` comments from the submitted version.
7. **Descriptive standards.** The tables were not available to me. Please confirm that each statistic has its n, that skewed variables (period) are summarised on the log scale, and that mean and SD are not the headline for them.

## Assessment against the checklist

- **Fit of method to question:** mostly good.
  - Distributions, quantiles, counts and group comparisons suit a descriptive question.
  - The joint structure that the question names ("distributed in radius *and* period") is only partly described (M1).
- **Computation:** consistent with the specification as far as I can see. Not checked against the script.
- **Claims within the design:** good. There are no causal claims, and the catalogue-versus-population distinction is made clearly. Two spots over-read the data: the "overlap" claim (M1) and the explanation of rho = 0.47 (M2).
- **Sensitivity:** weak (M4, M5).
- **Reproducibility:** depends on a live web service and an unreported seed in the paper (M6).

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
