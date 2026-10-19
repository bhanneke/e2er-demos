# Writing Review: "How Has the Yearly Number of Magnitude 5 and Larger Earthquakes Changed, 1976–2025? Counts and the Stability of the Gutenberg–Richter b-Value Across Decades"

## Summary assessment

The paper is clear, restrained and honest about what a descriptive catalogue study can show. Most paragraphs open with a topic sentence, the active voice dominates, and the numbers I checked against the supplied summary statistics are consistent. Examples: the decade event totals, the dispersion indices 56.7, 5.4 and 69.2, the 0.14 and 0.30 spreads, and the Mw-share percentages.

The weaknesses are mostly evidence–claim alignment and redundancy. Three headline statements go further than the evidence presented:

1. The Mw-sample "variation largely disappears" (Conclusion).
2. The record is "a combined product of the Earth and the measurement process" (Conclusion).
3. A headline rejection rate (nine of ten pairs) rests on a test the paper itself says is invalid for this sample (aftershock dependence).

The same results are also stated four times in near-identical wording (Abstract, Introduction, Results, Conclusion). Several method details used in Results are missing from Methods.

## 1. Evidence–claim alignment (highest priority)

1. **The Conclusion says the b-value variation "in the moment-magnitude sample, largely disappears."** The Results report Mw-only b = 0.835, 0.975, 1.032, 0.921, 0.995. That is a range of about 0.20, larger than the 0.14 range in the full sample at decade-specific Mc. What differs is the absence of the late-decade *increase*, not the absence of variation. The Mw-only decades are also never tested pairwise, and 1976–1985 rests on N = 857. Replace "largely disappears" with a precise statement: "the rise to 1.15–1.22 in the two latest decades does not appear (0.921, 0.995), but the Mw-only estimates still range from 0.84 to 1.03." Report N for all five Mw-only decades, and say whether pairwise tests were run.

2. **The Conclusion says "The record is therefore best read as a combined product of the Earth and of the measurement process."** This asserts that both contribute. The Abstract, Results and Discussion say the data cannot separate the two, and both readings are "open". Rewrite as "the record cannot distinguish Earth-side from catalogue-side contributions; it shows neither a secular rise nor a stable b-value."

3. **The headline "nine of ten pairs" test rejections sit in the Abstract and Conclusion without caveat.** The Discussion then concedes that aftershock dependence makes the standard errors and Utsu's test "too narrow." The test also ignores uncertainty in Mc. The Discussion says the choice of Mc "moves estimates by amounts comparable to the differences between decades", and the Mc-shift results support this: 2016–2025 falls from 1.220 to 1.150 between +0.2 and +0.3. Taken together, these admissions undercut the sentence "the instability survives". Put the caveat in the Abstract (for example, "p-values are descriptive because events are dependent and Mc is estimated"). Reconcile the Discussion explicitly: say which differences exceed the Mc-rule spread and which do not. At the common threshold the spread is 0.30, which is large. At decade-specific Mc it is 0.14, which is comparable to the Mc-shift effects.

4. **"Neither the counts nor the b-value is stable" (Abstract).** "Stable" is never defined for the counts, and no stability test is run for them. The Results describe a "dip and peak" in decade means. Define what instability means for counts, or write "decade means of the counts do not follow a monotone path."

5. **"No persistent direction" (Discussion) versus the trend summary (Results).** The Poisson slope is 0.40 percent per year, with a robust interval excluding zero (0.13 to 0.68). The negative-binomial interval also excludes zero (0.06 to 0.73), and Spearman's p is 0.053. The text dismisses these with "interval widths understate uncertainty", which is sensible. But the Discussion should say "no monotone path in decade means" and should not suggest that the summaries show nothing. Give the slope a baseline and units: 0.40 percent per year compounds to roughly 22 percent over the 49 years from 1976 to 2025, against the 25 percent decade-to-decade difference already quoted.

6. **Completeness claim at M5.0.** The text says that at 5.0 the goodness-of-fit ranges from 94.0 to 98.8 percent, "so the catalogue is complete at the level used for the yearly counts in each decade under these rules." A 94.0 percent fit fails the 95 percent rule that the same section defines. State which decade has 94.0 and reconcile with the 95 percent rule. "The conclusion is comfortable" is informal; say what is concluded.

7. **Magnitude-scale reading of the M6/M5 contrast.** The text says counts at different thresholds not moving together "is what a change of magnitude scale, and not a common change of the rate, would produce." This leans toward the catalogue reading, which the researcher's instructions asked to keep open, and it is not tested. Either delete the clause or state the alternative that the physical rate of M5–6 events also varies.

8. **Sentence on 1996–2005 slope change.** "This indicates a distribution whose slope changes near magnitude 5" is asserted and then immediately "we cannot attribute it." Hedge the first clause: "is consistent with a slope change near magnitude 5."

9. **Aftershock attribution of 2010 and 2011.** The text names no events (Maule, Tohoku) and says "we do not test this attribution." That is acceptable, but the 2011 value could be given as the share above the decade median and the sequences named. Either support it or move it to the Discussion as conjecture.

10. **Mc-shift description.** "In the first decade the estimates level off between +0.2 and +0.3" describes a fall from 1.191 to 1.175, and the 2016–2025 fall of 0.07 is not mentioned in the same light. Describe both falls and say whether they are within the bootstrap interval.

11. **Practical implications paragraph.** Advice to "hazard analysts" goes beyond the evidence in a paper with no hazard application. Reduce it to what the paper shows: b depends on threshold and magnitude type.

12. **Literature claims.** The statement that recent Mc comparisons (wang2025estimating, godano2023evaluating) "indicate that the choice of rule remains consequential" was not checked against the papers (the literature review notes only titles were read). Verify or soften it. "Regional studies report increases" cites a single study; use the singular. The literature review flags year inconsistencies for shearer2011global (2011 vs 2012) and incomplete bib authors; fix them before submission.

## 2. Methods–Results consistency

- **The fixed-threshold M5.0 specification** appears in Results (estimates 1.166, …, 1.150, with pair tests) and in the Mc-shift table, but Methods never introduces it. Add it to the Methods paragraph on Mc and the b-value.
- **Utsu's test is not defined.** No formula or description is given beyond "likelihood-ratio statistic" and "ΔAIC (the statistic minus two)". Results report only "statistic, p" and never say whether the statistic is the LR or ΔAIC, or its degrees of freedom. State the null, the statistic, its reference distribution and the unit (χ² with 1 df?). State that no multiplicity adjustment is used for ten pairs (the plan mentioned Holm), or justify this.
- **The "Checks" subsection** mentions Mc shifts and subsamples, but the 1,000-resample bootstrap is described only under the b-value. Say whether Mc is re-estimated inside bootstrap replicates (it appears not; the intervals are conditional on Mc). This matters for the claim that intervals are "narrow."
- **Three near-synonymous threshold names:** "focus threshold" (5.0), "common threshold" (4.9) and "fixed threshold" (5.0). Define each once in Methods, and consider "decade-specific Mc", "common threshold 4.9", and "fixed threshold 5.0" as the only labels.
- **Sample-size rationale in Data** ("completeness magnitude in every decade turns out to be at or below about 5, so events down to 4.5 suffice") is circular. Mc is later reported as censored at 4.5 in three decades. Rewrite as a design choice with its consequence stated: "we load from 4.5; for 1996–2025 the estimate coincides with this floor."
- **Counting versus binning mismatch.** Counts use the published magnitude (mag ≥ 5.0) while b uses magnitudes rounded to 0.1. A two-decimal event at 4.97 is excluded from the count but enters the b-value as 5.0. Say once whether this affects anything beyond the 96 events noted.
- **The 211 near-duplicate pairs** flagged in the data summary are not mentioned in the Data section. One sentence would suffice.
- **The roadmap does not match the structure.** It says "The final sections discuss limitations and conclude", but there is no limitations section; limitations are in the Discussion. It also omits the Related Literature section's placement in the text relative to Data and Methods. Reduce the roadmap to one sentence (or delete it).
- **The phrase "under the rule that a change is described only where decade means show it"** (Methods and Results) is an internal pipeline instruction. Rephrase as a design principle: "We call a change real only if decade means show it."

## 3. Redundancy and flow

- **The Introduction contains a complete results paragraph** (the sample, five decade means, b-ranges). The Abstract, Results, Discussion and Conclusion repeat much of it in nearly identical language. Keep the headline in the Introduction (mean about 1,670; no monotone path; b varies from 1.02 to 1.16; data cannot separate) and move the five-decade lists to the Results and tables.
- **Numbers lists in prose.** Several Results paragraphs enumerate five or more decade-level values already in tables (counts, Mc, b, GFT variants). Present them in the tables and discuss only the contrasts. The first b-value paragraph runs to about nine sentences, over the eight-sentence guideline, and mixes three claims (levels, precision, pairwise tests).
- **The Results repeat the overlapping pairs** twice ("The bootstrap intervals overlap for that pair and for…" then "For the second of these pairs…"). Merge the two.
- **Twelve tables** and two figures appear, yet there is no figure of b by decade with intervals and no frequency–magnitude plot with Mc marked. The data summary lists these as "not produced". For a paper about b and Mc, these two figures carry the argument far better than tables of estimates. Add them. Consider moving the GFT-95 and common-threshold tables to an appendix.
- **Contributions.** The "third contribution" ("states which features the data cannot resolve") is a limitation, not a contribution. Reduce to two contributions or reframe. The second contribution ("including the pairs for which the likelihood-ratio test and bootstrap intervals point in different directions") is a reporting practice; state what a reader learns.
- **Discussion structure.** "Several scope conditions apply. First…Second…Third… A fourth point" breaks the enumeration. The fourth point also repeats the second Discussion paragraph (Mw sample too small and high in Mc). A missing paragraph break precedes "Future work could answer two specific questions"; the two questions are specific and acceptable, but write "We see two follow-up questions" and give them as a single sentence each.
- **Uncited background in the Introduction.** "Seismological theory predicts a roughly stable long-run rate of large events with strongly clustered annual counts" has no citation, and the Poisson/Omori–Utsu background is not given a source. Either cite or flag as standard background.

## 4. Sentence-level and style points

- "The remainder of this study is structured as follows: In the next section, we…Afterward…Then…": the sequencing words are clumsy, and "In the next section" followed by a colon plus a capital is an error. Shorten to "Section 2 reviews…; Section 3 describes…".
- Nominalisations and filler: "a transparent, reproducible description" (state what is reproducible and where the code is); "the practical limit is therefore the set of assumptions behind the standard error"; "The conclusion is comfortable"; "tell a different story, which is informative about the role of the magnitude scale".
- "Significant" and "rejects equality": the paper uses "rejects at the 1 percent level" correctly. Keep avoiding "significant" for importance elsewhere.
- Number format: mix of "1 percent level", "one percent level" and "five percent"; choose one. Spell out numbers below ten in text consistently ("nine of ten" is fine; "two pairs" is fine). "N = 20,023" with and without math spacing varies.
- Term variation: "completeness magnitude" / "magnitude of completeness" / "completeness threshold" / "Mc"; "moment-magnitude sample" / "Mw-only" / "Mw-family" / "moment-magnitude family". Pick one each and define at first use. The Mw-only check is named "moment-magnitude" in prose, but the tables and the data summary use "Mw family".
- "Data" is correctly treated as plural. Tense is mostly consistent; the Methods mix "we estimate" with "we report".
- Notation: Eq. (2) is labelled `eq:sebolt` but the text says Shi–Bolt in one place and "Shi and Bolt" elsewhere; unify. Define ln 10 ≈ 2.30 once.
- Remove every `% src:` and `% computed:` comment before submission.
- Abstract: 190+ words and dense with figures. Cut the decade-level counts and add one sentence on the Mw check, Mc censoring and the dependence caveat. It currently omits that Mc is censored at the load floor in three decades, which affects the "once completeness is taken into account" framing of the title question.
- Title: long, with two questions. Consider "Counts of Magnitude 5+ Earthquakes and the Stability of the Gutenberg–Richter b-Value by Decade, 1976–2025."

## 5. What works well

- Hedging is mostly well calibrated; descriptive findings are stated confidently and causal language is absent.
- Null and ambiguous results are reported as computed, including disagreements between the likelihood-ratio test and the bootstrap intervals.
- The Data section is explicit about cleaning (562 rows, 909 two-decimal magnitudes) and the paper states that Mc is censored at 4.5.
- The caution on the −0.3 Mc-shift entries, where the nominal 4.4 lies below the smallest loaded event, is exactly the kind of explicit self-correction readers need.

## Priority fixes

1. Correct the Conclusion on the Mw-only sample ("largely disappears") and on the "combined product" claim.
2. Carry the dependence and Mc-uncertainty caveat into the Abstract and reconcile it with "nine of ten pairs".
3. Define Utsu's statistic and the fixed-5.0 specification in Methods; state the multiplicity treatment.
4. Resolve the 94.0 percent versus 95 percent goodness-of-fit statement.
5. Cut the repeated results (Introduction, Results, Conclusion), move numbers to tables, and add the frequency–magnitude and b-by-decade figures.
6. Unify the terminology (thresholds, completeness, Mw sample) and fix the roadmap and contribution list.

OVERALL SCORE: 6/10
RECOMMENDATION: Minor Revision
