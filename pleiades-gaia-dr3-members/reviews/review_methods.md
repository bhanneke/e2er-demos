# Methods review: Pleiades membership and distance from Gaia DR3

Scope: fit of method to question, computation against the specification and `run_estimation.py`, claims within the design, sensitivity, and reproducibility. The study is descriptive: counts, percentiles, binned medians and a re-count grid. No estimate, test or causal claim is made, and the review does not judge astronomy beyond what the method supports.

## Summary

The procedure is simple, transparent and mostly well reported. The arithmetic I could check from the stated values is consistent (11.2% = 1,112/9,970; 7.9% and the 1,024 and 1,135 grid rows; the median of 1,112 over the ten one-at-a-time counts; 1000/7.3666 = 135.7 pc; the 0.13 pc distance uncertainty; the 5.66 mag modulus). The main problems are in the classification logic, one incorrect inference in the Discussion, a citation practice that the researcher has ruled out, and a bin-width statement that the cited rule does not support. Several claims rest on the figures and the grid in ways the text does not state.

## Must change

1. Results, Sensitivity, and Conclusion (classification of the base as "clear"). The pre-declared "ambiguous" rule says the result is ambiguous "if the count varies by more than 25% across the grid". The 48-row full cross runs from 913 to 1,184 with median 1,055.5. Its spread is (1,184 − 913)/1,055.5 = 25.7% of the median, which exceeds 25%. The "clear" verdict holds only if the rule is read as applying to one-at-a-time rows alone, which is the reading the "clear" condition uses but not the "ambiguous" condition. Fix: state the reading that was applied, report the full-cross verdict as ambiguous or borderline, and say that the base is clear under the one-at-a-time rule only. Do not present the 25% test as passed for the grid as a whole.

2. Discussion, paragraph 1. The text says that unrelated stars sharing the parallax and proper motion "would spread across the diagram and would not concentrate on one sequence." This is wrong. A field star with the same parallax lies at the same distance, so it sits on the same main sequence. A continuous CMD locus therefore cannot distinguish members from contaminants, and it is not evidence of membership. Remove the claim, or replace it with a test that can fail. Limitations ("the study has no independent test of contamination") is the accurate statement.

3. Membership contamination can be estimated and should be before the paper says it cannot be. Limitations says "the data cannot estimate the contamination rate." A standard descriptive control is available with counts only: count quality stars that pass the parallax window but lie in a proper-motion annulus well outside 5 mas/yr (for example 10 to 15 mas/yr from the centre), and scale by area. This gives an approximate contamination count that the paper can report. Add it as a row in `estimation_results.json`, or drop the claim that it is not possible.

4. Literature use. The researcher instructed that only references verified by the literature scanner be cited. The literature review states that none of the Pleiades or Gaia-membership entries has a verified quote ("Quote: none"). The draft nevertheless cites `cantatgaudin2022milky` and `cantatgaudin2024how` for "Gaia-based censuses now cover much of the open-cluster population", and `chelli2016pseudomagnitude` for "Pleiades distances determined before Gaia DR2". Fix: remove these claims, or verify the sentences first. The Gaia DR3 entries are supported by the data dictionary. The freedman1981 entry is cited for a bin rule that it does not support (see item 5).

5. Histogram bin rule (Section 3, "Data organisation" paragraph). The draft says bins are of equal width, 0.25 mas in parallax and 5 pc in distance, and cites Freedman and Diaconis (1981) for this. The Freedman–Diaconis width is 2 × IQR × n^(−1/3), which the descriptive specification also gives as the default. For the members, the parallax IQR is 0.247 mas, giving a width of about 0.046 mas. The distance IQR is 4.5 pc, giving about 0.8 pc. The chosen widths are therefore five to six times coarser than the cited rule. At 0.25 mas, nearly all members fall in one or two bins, so the histogram cannot show a second peak. Fix: use the Freedman–Diaconis width, or give a reason for the coarser bins and show a second width (as the descriptive specification §4 requires). Also state that the 0.1 mas histogram used for the mode is a different bin choice.

6. Parallax histogram is missing. The research plan (§5.3) and the descriptive specification call for a parallax histogram with the base window marked, plus a distance panel. The draft has no such figure. Its claims about the unimodality of the parallax distribution, the mode, and the single peak rest on the text alone, and the reader cannot check them. Add the figure (Figure 2 or a panel of the existing figure), and show the distance histogram that `estimation_results.json` and the data summary name as a figure.

7. Parallax centre depends on the seed, and the text says it does not. The naive clip on the full quality sample converges to 3.19 mas, which is the field. The paper therefore starts the clip from a proper-motion seed chosen from stars with parallax between 5 and 10 mas, a range that already encodes knowledge of the cluster's parallax. The text then says "the seed does not enter the result", but this is not shown. Also, the seed was chosen after the naive run had been seen, so "fixed before the results were read" does not hold for the seed. Fix: (a) disclose the order of events; (b) run the centre procedure from a set of seeds across the proper-motion plane (or a range of parallax start values) and report how many converge to the cluster and to the field, and whether the converged centre is the same; (c) state that the 5–10 mas range is a choice.

8. Figure orientation conflicts with the researcher's instruction. The instruction says BP−RP against G with G increasing downwards. The draft's caption and text state that G increases upwards, so the brightest stars lie at the bottom. The data summary says the renderer does not invert the axis. This is an unmet requirement, not a stylistic one. Either invert the axis in the figure (the data summary calls this a limitation of the spec) or raise it with the researcher before the caption is finalised. The caption must describe the figure as drawn, whichever way it is resolved.

9. Bright-end attribution (Results, CMD; Limitations). The data summary records that all five extract stars brighter than the brightest member have RUWE of 2.31 or more, so each fails the RUWE < 1.4 cut. This is enough to say that the RUWE cut removes them. The text instead says that the cut "is not identified here" and that the paper "does not establish which cut removed these stars". The researcher asked not to guess; the data do not require a guess. State that every one of the five fails RUWE < 1.4, and that the RUWE cut is the cause for those stars. Also: the draft says "the named B stars several magnitudes brighter" are absent. The extract has no source identifiers for named stars and no cross-match, so the naming should be removed or backed by `source_id`s.

10. Interpretation of the RUWE cut as a limitation. Because the cut removes the five brightest sources, the sample has a systematic gap at the bright end, which the one-at-a-time grid does not test. The floor at G > 6 removes members, but not stars excluded by the quality cut, so it does not test this effect. The Limitations sentence "the floor at G = 6 removes only 6 members, which suggests the bright end does not drive the count" is a non-sequitur for this reason. Fix: add a sensitivity row that relaxes RUWE (for example to 2.5), or state that the count and the CMD's bright end are conditional on the RUWE cut.

## Should change

11. Reading rule for the mode. The mode-minus-median test uses a 0.1 mas histogram and a 0.1 mas threshold. The stated difference of 0.017 mas is one bin width or less, so the test cannot show more than that. A single histogram also cannot show unimodality. Give the mode at two bin widths, or drop the word "unimodal" and say what was checked.

12. Quantile and IQR rounding. The parallax quartiles 7.243 and 7.490 mas map to 138.07 and 133.51 pc, so the distance IQR is 4.56 pc, which rounds to 4.6. The paper and the JSON give 4.5. Check the source of the value and correct the rounding.

13. Standard error label. `parallax_median_se_mas` in the JSON is σ/√n, the standard error of the mean, as the paper now says. The key name says median. Rename the key. The distance-uncertainty sentence in Results should then refer to the mean, as the researcher asked.

14. Zero-point sensitivity is not reported in the JSON. The paper says the zero-point row lowers the median distance by about 0.4%. This value is derived in the text (135.7 × 7.367/7.397 ≈ 135.2 pc) and not stored. Store the zero-point distance in `estimation_results.json` so the figure is traceable.

15. Parallax quality cut selects on the outcome. The cut parallax_over_error > 10 uses the parallax that the window then clips. For members at 7.4 mas, it removes stars with parallax error above 0.74 mas, so the member parallax distribution is conditioned on precision, and faint members are removed. This is a selection effect and should be named as such in Limitations, together with its effect on the CMD's faint end.

16. CMD membership test. The "continuous locus" test shows only that members form a sequence, which any group of stars at one distance does. A useful check is to compare the spread of members' colour at each G with the field's spread at the same G, and to report the share of members within a fixed band around the locus. This is a count and is consistent with the descriptive design.

17. Locus bin counts. The G 6–7 bin has 10 members, and the spread-based statements ("narrowest", "widest") rest on bins of 10 to 250 members. Show n in Table 2 for every bin and qualify the "narrowest" statement.

18. Clear-result benchmark. The reference band of 125–145 pc was set from the plan's general-knowledge figure of about 135 pc, which the plan itself says is unsourced. The "clear" result therefore partly reflects the prior. Say so, or replace it with a verified value once the literature check is done.

19. Vector-point diagram (Figure 1). The caption says no member selection is drawn. A proper-motion diagram that does not mark the 5 mas/yr radius or the members does not show the cluster clump that justifies the membership cut. Mark the members (or the radius circle) in Figure 1.

20. Duplicated membership code. The selection is implemented in `run_estimation.py` and again in `load_members.py`, copied "unchanged". The data check confirms the count of 1,112 from the second copy. Keep one implementation and have the other import it, so that the two counts cannot drift apart.

## Nice to have

21. Cone radius sensitivity. The question fixes the radius at 3°, but the cluster's extent is not uniform. Count members at 1° and 2° as descriptive rows. This shows how much of the count depends on the cone.

22. Proper-motion dispersion is truncated. The sd of 1.08 and 1.41 mas/yr is computed on members already cut at 5 mas/yr, so it understates the spread. Say so, or report the spread of the stars within 3 mas/yr only.

23. Fixed-bin reporting. Give the bin edges in the JSON for every histogram, as the descriptive specification requires, so the figure can be re-read.

24. Reproducibility. The pipeline depends on the archived `data/gaia_dr3.csv` and the sha256 in the dictionary, which is good. Add the software versions (Python, numpy, and the percentile method name) to the replication files. No randomness is used, and that should be stated.

## What I checked and found consistent

- 1,112 / 9,970 = 11.2%. 1,345 − 1,112 = 233 stars removed by the proper-motion cut.
- One-at-a-time counts: the largest change from base is 1,024 vs 1,112, i.e. −7.9%. The median of the ten one-at-a-time counts, including the base, is 1,112.
- Full cross: 913 is −17.9% and 1,184 is +6.5% of the base, as the text states.
- 1000 / 7.3666 = 135.7 pc. The standard error of the mean, 0.230/√1,112 = 0.0069 mas, gives a distance uncertainty of about 0.13 pc. The distance modulus 5 log10(135.7) − 5 = 5.66 mag.
- The zero-point row adds +0.03 mas to the parallax, which moves the centre from 7.367 to 7.397 mas and lowers the distance by about 0.4%, as stated.

## Required closing lines

Methods score rationale: the procedure is transparent and its arithmetic checks, but the verdict logic is inconsistent with the pre-declared rule, one inference in the Discussion is invalid, the histogram rule is misattributed, the seed dependence is untested, and the citation practice conflicts with the researcher's instruction.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
