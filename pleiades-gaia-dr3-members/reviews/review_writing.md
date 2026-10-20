# Writing review: Which Stars within 3 Degrees of the Pleiades Centre Share Its Astrometry?

Reviewer: Writing Reviewer
Scope: prose, structure, claim-evidence alignment, citations as used in the text, and figure captions. The membership selection, grid and numbers were taken as given from `estimation_results.json` and the data summary. Where I cite a number, I checked it against those sources.

## Overall assessment

The paper is clear, short in its sentences, and honest about its descriptive scope. The numbers in the text match the JSON (1,112 members, 11.2%, 7.367 mas, 135.7 pc, 132.3–139.3 pc, distance modulus 5.66, grid minimum 913 and maximum 1,184, −18% and +6% against the base, 7.9% largest one-at-a-time change). The arithmetic I rechecked holds: 1,345 − 1,112 = 233; 0.230/√1112 = 0.0069; 1000/7.367 ≈ 135.7; 0.03/7.367 ≈ 0.4%; the G 6–7 and G 14–15 spreads (0.075 and 0.400 mag).

The main problems are not in the numbers. They are (i) a seeding decision that is described as made in advance but was made after the naive clip was seen to fail, (ii) a circular claim about the unimodal parallax peak that the Discussion then uses as evidence of a coherent sequence, (iii) a Discussion argument that a CMD sequence distinguishes members from field stars, which it cannot, (iv) internal process notes left in the manuscript body, (v) an observed fact about the five bright stars that the results omit, and (vi) a figure whose axis does not match the researcher's latest instruction. Each is fixable in the text or the figure spec.

## Major issues

1. **The seed is described incorrectly and is not "fixed before the results were read".** Section 3 says that "the clip is started from the densest proper-motion bin among stars with parallax between 5 and 10 mas", in the sentence about the parallax centre and scatter. The spec (§2) and the JSON (`seed_pm_mas_yr` = (19.0, −45.0)) say the seed starts the proper-motion iteration, not the parallax clip. The paper also says the seed "does not enter the result", but the seed was chosen after the naive full-sample clip (3.19 mas) had shown the field centre. That is a data-informed choice. The paper should say so plainly, state which iteration the seed starts, and say that a different seed was not tried (or report it if it was). Fix: rewrite the paragraph so that the parallax clip and the proper-motion clip are described separately, and add one sentence: "The seed was chosen after the naive clip returned the field centre."

2. **The unimodality check is circular, but the Discussion uses it as evidence.** Section 4 correctly notes that the window is built from the peak, so "a single peak inside it holds by construction". The Discussion then says "The narrow parallax peak ... [is] consistent with the members forming a single coherent sequence". The Results' reading rule (mode and median within 0.1 mas) therefore cannot count as a test of coherence, because a ±3σ window truncates the distribution by design. The Abstract ("narrow peak") and Conclusion ("narrow peak at 7.367 mas") repeat the word without that caveat. Fix: drop "narrow peak" as evidence in the Discussion and Conclusion, or state that it is a property of the clip. Describe the unimodality check as a consistency check on the clipped sample, not as a test.

3. **The Discussion's argument about field stars does not follow.** The sentence "Unrelated stars that happened to share these values would spread across the diagram and would not concentrate on one sequence" is wrong as written. Field stars at about 135 pc also lie on a main sequence, and a field star with a similar parallax and proper motion would fall on it. The CMD can show that the members are consistent with a single sequence. It cannot show that they are members. Fix: replace the sentence with the correct claim (the CMD shows a sequence; it does not discriminate membership), and point to the isochrone test already named in Future research as the check that would.

4. **Internal process notes appear in the manuscript body.** These sentences are working notes and should not appear in a submitted draft:
   - Section 2: "This centre is a catalogue approximation ... it has not yet been checked against a cited literature value."
   - Section 4: "No verified source for the cluster's reddening is yet in place."
   - Section 4: "The comparison with a published main sequence is left to a verified source."
   - Section 5 (Discussion): "Setting the present median against those values requires the verified figures and their releases, which have not been extracted for this paper."
   - Abstract last sentence and Conclusion: "await comparison with verified published values."
   Each is an honest statement of a gap. Each should be a limitation sentence written for a referee (what is missing, why it matters, what would close it), and the process wording ("not yet", "have not been extracted") should go. The reader needs the consequence, not the status of the work.

5. **The results withhold an observed fact about the bright stars.** The Results say "The cut that removes them is not identified here", and the Limitations say "the paper does not identify which cut removes them." The bright-end block in the JSON records that all five extract stars brighter than G = 5.203 fail the quality cuts and that all five have RUWE of 2.31 or more. The researcher asked that the paper not guess the cause. Reporting the observed RUWE values is not a guess. Fix: state the observation in the Results ("All five stars brighter than the brightest member fail the quality cuts; all five have RUWE ≥ 2.31"), and keep the causal statement open ("the data do not establish that the RUWE cut is the only cause").

6. **"The named B stars" is unsourced.** The Results, Limitations and data summary all say the cluster's brightest stars, "the named B stars several magnitudes brighter", are absent. The literature review found no verified source for the Pleiades' B-star content and no verified Pleiades magnitudes. Either cite a verified source for the claim, or describe the gap in terms of the data only (stars with G < 5.2 in the extract).

7. **The figure does not match the researcher's latest instruction.** The rerun note asks for BP−RP against G "with G increasing downwards". The caption of `fig_cmd` and the Results text both say "G increasing upwards, so the brightest stars lie at the bottom". The data summary confirms that the renderer does not invert the axis. The text is accurate to the figure as drawn, but the figure does not meet the requirement. The figure spec needs an inverted G axis, and then the caption and the Results sentence must be rewritten to match. Also check the colour claim: the caption says the field is "drawn in blue", but the data summary says the field is in the renderer's default colour. The caption must match the rendered colours.

8. **The research question's distance distribution has no figure.** The question asks what the parallax distance distribution shows, and the plan calls for a distance histogram. The text describes the distribution in detail, but no figure is included, and `fig_distance_hist.pdf` is not named in `estimation_results.json`. Add the parallax and distance histogram with the base window marked, or justify its absence.

9. **The reading rules are stated but never applied.** Section 3 sets out the failure and stability rules "before the results", but the Results never say which rules were met. The JSON supports a clear statement: the base count is within 10% of the grid median (1,112 vs 1,112); the largest one-at-a-time change is 7.9% (below 25%); the mode and median agree within 0.017 mas; the median distance (135.7 pc) lies in 110–160 pc; no failure. Add one paragraph in the Results that reports each rule and its outcome. Also reconcile the rules in the paper with the spec, which has a "clear" band (125–145 pc) and a continuous-locus criterion (8 mag) that the paper does not mention.

10. **The contribution and motivation are vague.** The Introduction calls the work "a replicable reference exercise", and the Discussion calls its value "transparency". A referee will ask why a member list for the Pleiades is needed when published Gaia membership catalogues exist (the Introduction cites two of them). The paper never states how its selection differs from those catalogues, or why a single cut is informative. State the difference in one or two sentences, and drop "the value of the result lies in its transparency", which says nothing a reader can check.

11. **Citations are attached to claims the text has not verified.** The literature review states that no verbatim claim from any Pleiades or Gaia membership source was extracted. Yet the Introduction says that Gaia "gives parallaxes and proper motions for most of the bright stars in such clusters" and that "Gaia-based censuses now cover much of the open-cluster population" (cantatgaudin2022milky, cantatgaudin2024how). The Discussion says the Pleiades distance comparison is with "the natural benchmarks" (cantatgaudin2022milky, cantatgaudin2024how, chelli2016pseudomagnitude). Until those sentences are checked, either remove the citations for those specific claims or mark them as unverified in the working notes, not in the text. Also, "The Pleiades is one of the nearest open clusters and a familiar reference for the distance scale" has no citation.

12. **Missing citation for the zero-point.** The paper says the parallaxes are "uncorrected for the Gaia zero-point, which is negative at these magnitudes", and gives an approximate offset of 0.03 mas. No Lindegren et al. (2021) entry is in `literature.bib`, and the spec cites that paper for the offset. Add the reference (after verifying it) and cite it at the first use.

13. **Freedman–Diaconis is cited for the wrong point.** Section 3 says that bins of equal width "so that the counts in the bins sum to the sample size" are justified by `freedman1981histogram`. That reference is about choosing bin width, and the equal-width sentence is not a claim it supports. Either cite it for bin-width choice (and say the 0.25 mas and 5 pc widths were chosen by the author) or drop the citation.

## Claim–evidence alignment (checked against the JSON)

- **Membership-grid stability.** "Membership counts move by less than 8%" (Abstract) is correct for one-at-a-time changes (7.9%). The Results sentence "The counts are stable ... they vary more under combined changes" is correct, but the Abstract and Conclusion should not present "stable" without the full-cross range (−18%). Use the same wording everywhere: "under one-at-a-time changes, counts move by at most 7.9%; under the full 48-row cross, counts range from −18% to +6%."
- **Explanation of the cross spread.** "The wider spread therefore arises when several cuts move together." The extract shows only the two extreme rows, not the decomposition. Write "The extreme rows combine several changes" and drop the causal wording.
- **Locus continuity.** "Every bin from G = 6 to G = 18 holds at least 10 members, so the locus is continuous over that range." A count of at least 10 per bin is a precondition for a median, not evidence of continuity. Write what was checked: the median colour rises monotonically across all twelve bins, each with at least 10 members. Then say that the faint bins are noisy.
- **Widest spread.** "...widest between G = 14 and G = 15, where it reaches 0.40 mag." The text verifies only two bins (G 6–7 and G 14–15). The JSON has all twelve. Check all twelve before claiming the widest.
- **Null and contamination statements.** "The field stars in the extract do not share the cluster's proper motion, but the data cannot estimate the contamination rate." This is confused. Field stars that fail the cuts are not members by definition; the contamination concern is about members selected by the cuts that are not cluster stars. Rewrite: "Stars that pass the cuts but are not cluster members cannot be identified with these data, so the contamination rate is unknown."
- **Faint-end counts.** The count jumps from 59 (G 14–15) to 142 (G 15–16), and to 250 and 228 in the next two bins. The Results do not mention this. A referee will ask whether the faint bins are dominated by field stars that pass a 5 mas/yr radius, where the proper-motion errors are large. Either report the per-bin field counts from the CMD figure or add one sentence on the jump.
- **"Turn-off".** The Results and Limitations refer to "the faint-end turn-off" and "a precise turn-off measurement". No turn-off is measured in the paper, and the bright end where a turn-off would lie is missing. Remove the word, or say "the bright end of the locus".
- **Extinction.** "The colours are not corrected for extinction, so the locus is shifted slightly red" is true for the observed colours, but the paper gives no value for the shift. Say "shifted red by an amount proportional to the (unquantified) reddening."

## Structure and flow

- **Repetition.** The headline numbers (1,112; 11.2%; 7.367 mas; 135.7 pc; 132.3–139.3 pc) appear in the Abstract, Results, Discussion and Conclusion. The first Discussion paragraph restates the Results almost word for word. Cut the Discussion's first paragraph to one sentence that states what the reader should take away.
- **Roadmap.** The Introduction's roadmap omits Section 7 (Future research). Either add it or fold the paragraph into the Discussion or Conclusion. A one-paragraph section with a single suggestion is better folded in.
- **Section 3 mixes design and data description.** The data-organisation paragraph ("This follows the principle that a dataset should hold one observation per row ...") is not a design choice and can go, or move to Section 2.
- **Section 4 starts with the membership count and then gives the grid.** The reading rules and the zero-point result come before the grid, which reads more naturally than the current order (rules → results → grid). Keep the order but move the reading-rule outcome (Major issue 9) to the start of Section 4.
- **Table placement.** `tables/grid.tex` is input before the parallax subsection, and the locus table is input after the figure. The summary table is input last in the Results. The reader sees the grid table before the paragraph that introduces it. Move the `\input` so that each table follows its first mention.
- **Caption length.** The CMD caption is long and repeats the Results. Shorten it to: what is plotted, the axis convention, the colour convention, and the uncorrected colour.

## Sentence-level points

- Title: "Parallax Distance" is awkward as a noun group. "Parallax-Based Distances" reads better.
- Abstract: "The distance is 1000/ϖ from the uncorrected parallax." Put it before the distance figures, not after.
- Section 2: "The data check passed, with no duplicate keys and no missing astrometry." This is process reporting. Keep the outcome, drop the phrase "the data check passed".
- Section 3: "The reading rules are stated here before the results." Replace with "The reading rules, set before the results, are as follows."
- Section 3: "The grid is reported in full, and no row is selected for its count." Fine. It is the strongest sentence in the paper; leave it alone.
- Section 4: "The mode, taken from a 0.1 mas histogram, ... That difference is well inside one bin width, so the mode adds little beyond the median, and the histogram shows one local peak." Shorten: "The mode (7.35 mas, from a 0.1 mas histogram) lies within one bin of the median."
- Section 4: "The standard error of the mean parallax ... Propagating this standard error of the mean parallax through 1000/ϖ gives ..." The phrase is repeated in one sentence. Keep one instance.
- Section 4: "The parallax distance distribution follows directly." Vague. Say what it follows from.
- Section 4: "Figure~\ref{fig:cmd} plots the members as one series, in orange, against the remaining stars ... drawn in blue." Use the caption's wording or delete the colour detail from the text.
- Section 5: "The spread is the star-to-star scatter of these distances and is not a measure of the cluster's depth, which the paper does not estimate." Good sentence; keep it.
- Discussion: "at the precision the astrometry allows" is vague. Give the precision (the standard error of the mean parallax, 0.007 mas) or delete the phrase.
- Limitations: "The sample therefore has a gap at the bright end, and the paper does not identify which cut removes them." See Major issue 5; rewrite.
- Limitations: "The floor at G = 6 removes only 6 members, which suggests the bright end does not drive the count." The inference is correct for the count, but not for the locus. Specify "the count".
- Conclusion: "The description is a reference for replication, not a physical result." Good; keep it.
- Future research: "A useful next step is to test ..." The suggestion is specific enough to stay. Keep it.
- Date: `\date{13 October 2026}` and the author line still contain the placeholder "[author details to be completed by the researcher]". Complete before any circulation.
- Acknowledgement: the Gaia credit appears in the Data section. The data dictionary specifies a standard acknowledgement sentence; add it to the end of the paper or to the Data section as written there.
- Spelling: the text uses British spellings ("centre", "colour", "renormalised") consistently. Keep them. "Gaia data release 3" and "Gaia DR3" are both used; use "Gaia DR3" throughout after the first full mention.
- Number format: "7.367 mas" and "7.35 mas" (the mode) carry different precision, and "5.20" and "5.203" both appear in different places. Use the same precision in each sentence where the two values are compared.

## Figures and captions

- `fig_vpd_pm` caption: "No member selection is drawn; the members are identified in Section 3." The members are identified by the selection rules, not by a figure. Say "the selection rules are set out in Section 3."
- `fig_cmd` caption: must match the rerun instruction (G increasing downwards) and the rendered colours. Once the figure is fixed, update the caption and the Results sentence ("G increasing upwards, so the brightest stars lie at the bottom"). See Major issue 7.
- `fig_cmd` caption: "The 17 members without a colour are not plotted." Good. Keep it.

## Priority order for the researcher

1. Fix the seed description and the reading-rule outcome (issues 1, 9).
2. Remove the circular "narrow peak" evidence and the field-star argument from the Discussion (issues 2, 3).
3. Replace internal process notes with referee-facing limitations (issue 4).
4. Report the observed RUWE failure of the five bright stars and drop "the named B stars" (issues 5, 6).
5. Regenerate the CMD with G increasing downwards, then update the caption and text (issue 7).
6. Add the distance histogram or justify its absence (issue 8).
7. Verify or de-cite the unverified literature claims and add the zero-point reference (issues 11, 12, 13).
8. Sharpen the contribution statement and cut repetition (issue 10 and the structure section).

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
