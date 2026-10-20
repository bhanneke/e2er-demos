# Data review: Pleiades membership and distance from Gaia DR3

Reviewer: data_reviewer. Scope: the data pull, sample construction, missingness, variable units, the sensitivity-grid counts, the distance and CMD summaries, and whether each data claim in the draft is supported by the stored results. Estimation choices (the membership rule itself) are discussed only where they bear on what the data can show.

## Summary

The arithmetic is sound. I recomputed the sample flow, the stage counts, the parallax-window width, the standard error, the distance, the distance modulus, the grid extremes and the colour-missingness accounting from the figures in the draft and the data summary, and they agree. The data check (no duplicate `source_id`, complete astrometry, documented missing photometry) is adequate for a descriptive study.

The problems are in what the draft says about the data, not in the counts. The most serious are: (1) the literature cited for the data and methods claims has no verified quotes, against the researcher's instruction; (2) the reading rules are stated but never applied to the results; (3) the locus summary covers 942 of the 1,095 members with a colour, and the draft does not say where the other 153 sit; (4) the histogram bin widths are cited to Freedman–Diaconis but are several times wider than that rule gives; and (5) the draft says the contamination rate cannot be estimated and that the continuous CMD locus argues against contamination, which neither the data nor the design supports.

## Findings, ranked

### 1. High: cited references for data and method claims have no verified content

The researcher's instruction at design review was to cite only references that the literature scanner verified. The literature review states that every Pleiades and Gaia reference in the bib (`cantatgaudin2022milky`, `cantatgaudin2024how`, `chelli2016pseudomagnitude`) has "Quote: none", and that the bib contains no Gaia DR2 or DR3 release paper and no Lindegren et al. (2021) zero-point paper. The draft nonetheless uses these works for specific claims:

- Introduction: "Gaia-based censuses now cover much of the open-cluster population" (`cantatgaudin2022milky`, `cantatgaudin2024how`). This is a factual claim about a source that has not been read.
- Discussion: `chelli2016pseudomagnitude` and the Cantat-Gaudin papers are named as "the natural benchmarks" for the distance. The paper then says the comparison is not made. That is acceptable only if the benchmark values are not quoted; the citation should be kept as a pointer, not as support for a claim.
- Section 2: "Gaia data release 3 \citep{GaiaMission_Prusti2016,GaiaDR3_Vallenari2023}" is the one citation the data dictionary supports directly, with its DOI and acknowledgement.
- Section 2 and Section 3: the methods sources `freedman1981histogram`, `hyndman1996sample`, `little2019statistical`, `wickham2014tidy` are cited for general statements. These are standard references, but the literature review also lists them as unverified against source text. Check the sentence each one supports before the final version.
- Section 4 (zero point): "Parallax zero-point ... is negative at these magnitudes" has no citation. The design specification and the data summary cite Lindegren et al. (2021) for the correction. The draft should cite it, and the bib must contain it.

Fix: either verify each claim against the source and record the quote, or remove the claim and keep only the bib pointer. Add the Gaia acknowledgement text from the data dictionary (the draft gives only "credit to ESA/Gaia/DPAC"), since the licence requires it.

### 2. High: the reading rules are stated but their outcome is never reported

Section 3 says "The reading rules are stated here before the results." Section 4 reports the numbers but never applies the rules. The specification (§5) and the plan (§6) set four criteria for a clear result, and the draft does not say which are met:

- base count within 10% of the grid median: met (1,112 against a median of 1,112);
- no one-at-a-time row moves the count by more than 25%: met (largest 7.9%);
- unimodal parallax histogram with mode and median within 0.1 mas: met (mode 7.35, median 7.367), but see finding 4 on the bin width;
- continuous locus over at least 8 mag: met for G 6 to 18;
- plan criterion "no member locus visibly displaced from the field": not assessed anywhere in the draft.

The draft also gives the failure rule (base count below 100, or median distance outside 110–160 pc) but omits the 125–145 pc reference band that the plan uses for "clear". Fix: add a short paragraph in Section 4 that applies each rule to the result and states the verdict, and either assess the displacement criterion from the figure or drop it from the plan's list.

### 3. High: the locus summary covers 942 of the 1,095 members with a colour

The twelve locus bins (G 6 to 18) hold the following member counts, from the realised results: 10, 14, 18, 32, 37, 41, 46, 65, 59, 142, 250, 228. They sum to 942. That leaves 153 of the 1,095 members with `bp_rp` outside the G 6–18 range. The faint end matters most: the faintest member is at G = 20.16, and the bins for G 15–18 hold 620 stars, so the members beyond 18 mag are a sizeable group.

The abstract and conclusion say the locus is "continuous from G = 6 to G = 18" and the limitations discuss the bright end only. The draft should state the count outside the range (G below 6, and G from 18 to 20.16), and say whether the faint members follow the same sequence. The poe > 10 cut removes faint stars with large parallax errors, so the faint tail is selected; the draft should say so in the locus paragraph, not only in the limitations.

### 4. Medium: histogram bins are cited to Freedman–Diaconis but do not follow that rule

Section 3 says "Histograms use bins of equal width, 0.25 mas in parallax and 5 pc in distance ... \citep{freedman1981histogram}." The Freedman–Diaconis width is 2 × IQR × n^(−1/3). With n = 1,112 (n^(−1/3) ≈ 0.097):

- parallax: IQR 0.247 mas gives a width of about 0.048 mas, against the 0.25 mas used (about five times wider);
- distance: IQR 4.5 pc gives about 0.9 pc, against the 5 pc used (about five times wider).

The bins may be a reasonable choice for display, but the draft must not attribute them to the rule. Either say they were chosen for display and why, or use the rule. The mode is taken from a 0.1 mas histogram, which is a third bin width the draft does not mention; a mode from a histogram depends on the bin width, so the unimodality claim needs a check at two widths (the descriptive guidance in §4 asks for this). Report the parallax distribution at a second bin width, or state that the single-peak statement is from one width.

Also, the draft has no histogram figure. The plan and the figure specification call for a parallax histogram with a distance panel, and the data summary mentions `fig_distance_hist.pdf`, which the draft does not include. The distribution claims therefore rest on text and a table only. Include the figure or remove the references to the histogram from Section 3.

### 5. Medium: the contamination claims overreach, and the grid already bounds the contamination

Two statements in the draft go beyond the evidence.

- Discussion: "Unrelated stars that happened to share these values would spread across the diagram and would not concentrate on one sequence." Field stars at a similar distance (about 135 pc) also form a main sequence in the CMD. A continuous locus therefore does not discriminate members from field stars at the same parallax. The field series in Figure 2 should be used for this comparison, not the locus alone.
- Limitations: "the data cannot estimate the contamination rate." The grid gives an order-of-magnitude bound under a smooth-field assumption. Using the PM-radius rows (base 1,112; radius 7: 1,124; radius 10: 1,127), the 5–10 mas/yr annulus holds about 15 stars inside the parallax window, which implies roughly 5 field stars inside the base 5 mas/yr disk if the field density is flat in PM space. The 5–7 mas/yr annulus holds 12 stars, which implies about 12 in the disk if density falls off more slowly inside. The two assumptions give roughly 5 to 12 stars, under 1% of the 1,112 members. This is a rough, assumption-dependent bound, and the draft should state it as such rather than say the rate is unknowable.

Fix: report the annulus counts from the grid, state the flat-density assumption, and remove the sentence that a continuous locus argues against contamination.

### 6. Medium: captions and text say "within 3 degrees" but the field is the parallax > 2 mas extract

Section 2 states that the extract is limited to parallax > 2 mas and that the field background is limited to stars closer than 500 pc. The captions of Figure 1 (vector-point diagram) and Figure 2 (CMD) say "the quality-cut Gaia DR3 sample within 3 degrees of the Pleiades centre" with no parallax limit. A reader who reads only the caption will take the field to be the full cone. Add "(extract with parallax > 2 mas)" to both captions.

The figure is also to be redrawn with G increasing downwards, per the researcher's latest instruction. The text ("The vertical axis shows G increasing upwards, so the brightest stars lie at the bottom") and the caption must then be changed to match the redrawn figure as drawn. Do not carry the old orientation into the new version.

### 7. Medium: the proper-motion seed was chosen after the naive run failed

The design section says the seed is "the densest proper-motion bin among stars with parallax between 5 and 10 mas", chosen because the naive full-sample clip converges to the field (3.19 mas). The choice of the 5–10 mas band was made after the naive run and encodes the expectation that the cluster is near 7 mas. The specification says the seed "does not enter the result", which is true only if the iteration converges to the same centre from any reasonable seed. The draft does not show this. Two things are needed: state that the seed rule was adopted after the naive run, and report the converged centre from at least one seed outside the 5–10 mas band (for example, the full-sample densest PM bin without the parallax restriction, if it converges to the field, that should be said). The claim in the design section should not say the rule was fixed before the results were read.

### 8. Medium: JSON key for the standard error mislabels the quantity

The draft now says the 0.007 mas value is the standard error of the mean, σ/√n, as the researcher asked. The stored key is `membership.parallax_median_se_mas` (cited as `estimation_results.json#membership.parallax_median_se_mas` in the draft). Its name says it is a standard error of the median, which would be about 1.25 times larger. I recomputed σ/√n = 0.230/√1,112 = 0.0069 mas, so the value is the mean's, and the draft's text is correct. The key name is wrong. Rename the key (in the analysis output) to `parallax_mean_se_mas`, or add a note in the JSON, so that a reader who follows the citation does not take it as the median's error.

The distance uncertainty of 0.13 pc from propagating 0.0069 mas through 1000/ϖ is also correct (1000 × 0.00691 / 7.367² ≈ 0.127 pc).

### 9. Medium: bright-end statement uses an unsourced claim and understates what the data show

The draft says "the cluster's brightest stars, the named B stars several magnitudes brighter, are not among the members." The claim that named B stars lie several magnitudes brighter than G = 5.2 is general knowledge and is not sourced. The data show the number that matters: the extract holds five stars brighter than G = 5.203 (G from 3.62 to 4.26), and all five have RUWE of at least 2.31, so all five fail the RUWE < 1.4 cut.

The researcher asked that the paper not guess which cut removed them. The observed RUWE values are not a guess, so the draft can say that in the extract all five bright stars have RUWE ≥ 2.31 and therefore fail the RUWE cut, while it still does not establish that this cut alone determines the gap. The sentence "The cut that removes them is not identified here" should be replaced by that observed statement. Confirm with the researcher before the final version, since the instruction was explicit.

### 10. Low: distance IQR does not match the parallax quartiles

Distance is a monotone transform of parallax, so the distance quartiles are the transformed parallax quartiles. The parallax quartiles 7.243 and 7.490 mas give distances of 138.1 and 133.5 pc, an IQR of about 4.6 pc. The draft reports 4.5 pc. This may be rounding in the stored quartiles, but it should be checked against `distance_summary.distance_pc_iqr` and the rounding stated.

### 11. Low: the grid extremes are described but the rows are not shown

The draft says the lowest full-cross count comes from "a 3 mas/yr proper-motion radius with a 2 sigma window and RUWE below 1.2" and the highest from "a 10 mas/yr radius with a fixed ±1 mas window and a parallax over error cut of 5." The results summary gives the minimum (913), median (1,055.5) and maximum (1,184), but not the rows that produce them. Confirm the row identities against `grid_full_cross` before publication. The percentages (−18% and +6%) are correct: 1 − 913/1,112 = 17.9%, and 1,184/1,112 − 1 = 6.5%, which rounds to 6%.

### 12. Low: items I could not check

The tables (`tables/grid.tex`, `tables/locus.tex`, `tables/summary.tex`) are not in the context. I could not verify the p16 and p84 values per bin, the claim that the spread is widest at G 14–15 (0.40 mag, which I did confirm from the bin values quoted) or narrowest at G 6–7, or the table entries. Check these against the rendered tables.

### 13. Low: missing-value description

The draft says two rows lack a G magnitude; the clean sample has one row with G null (data summary). The data dictionary describes G as "not expected" to be missing. Both are consistent with the data, but the draft should say which population each count refers to. The draft also reports the 169 BP-missing rows in the raw extract but does not give the clean-sample count (107), which is the figure that enters the CMD. Add it.

### 14. Low: sample-flow table missing from the paper

The sample flow is given in prose. The descriptive guidance and the plan call for a flow table with n kept and dropped at each stage. The data summary already has the table; add it to Section 2.

### 15. Low: author placeholder

The author line reads "[author details to be completed by the researcher]". Leave it for the researcher to complete, and do not submit with the placeholder.

## What I checked and found consistent

- Sample flow: 14,066 − 1,344 = 12,722; 12,722 − 2,752 = 9,970; solution codes 8,031 + 1,939 = 9,970.
- Colour missingness in the quality sample: members 17 without `bp_rp` plus field 90 without (107 in total); 9,970 − 107 = 9,863, matching the stated count with a colour (1,095 members and 8,768 field).
- Stage counts: 9,970 → parallax window 1,345 → PM radius 1,112; 1,345 − 1,112 = 233.
- Parallax window: 3 × 0.230 = 0.690 (stated 0.691 with unrounded sd).
- Standard error of the mean: 0.230 / √1,112 = 0.0069 mas.
- Distance: 1000 / 7.367 = 135.7 pc; modulus 5 log10(135.7) − 5 = 5.66 mag. The distance sd of 4.3 pc is consistent with the parallax sd (about 4.2 pc by linear propagation).
- Distance range 124.1 to 149.4 pc corresponds to parallaxes 8.06 and 6.69 mas, both inside the window of 6.68 to 8.06 mas.
- Grid: largest one-at-a-time change (1,024 against 1,112) is 7.9%; the grid median of the 10 values is 1,112.
- Zero-point row: centre 7.397 mas, distance 1000 / 7.397 = 135.2 pc, a change of −0.4%, as the draft says.
- Missing BP photometry in the raw extract: 169 rows, 1.2% of 14,066, below the 5% threshold for the missing-value rule.
- PM centre (19.867, −45.416) rounds to the stated (19.87, −45.42).

## Recommendation

The data and the counts are sound and the descriptive design is appropriate. The draft needs the citation work in finding 1, the verdict paragraph in finding 2, the locus and contamination corrections in findings 3 and 5, and the binning and caption fixes in findings 4 and 6 before the next review. None of these changes the headline counts. The draft is not ready for submission.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
