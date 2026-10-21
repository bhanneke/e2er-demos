# Data Review: The Vocabulary of Weather in English-Language Novels by Author Birth Cohort, 1770–1899

Reviewer role: Data Reviewer. Scope: source documentation, sample construction, tokenisation and dictionary measurement, validation sample, corpus composition, and whether the data support the claims. The supporting documents (data dictionary, data summary, specification, plan) were read against the draft.

## 1. Overall assessment

The paper is careful and well hedged. It makes no causal claim, it reports a hand check of its own dictionary, and it discloses several weaknesses. Hashes, seeds, a sample flow and per-document front-matter cuts are recorded, which is good practice.

The data problems below still limit what the headline claims can bear. Five stand out:

1. The corpus composition changes visibly across cohorts (genre, region, length, copyright truncation). The analysis does not address this.
2. The sampling frame was built differently for different cohorts.
3. Tokenisation and orthography create measurement artefacts that run along the time axis.
4. The hand-check sample is small, oversamples ambiguous terms, has no second coder, and cannot support the corpus-level precision statements made in the abstract.
5. Several statements in the text are not supported by the paper's own numbers: the leave-one-author-out claim, the "flat vs rising" lexicon contrast, and the "unchanged" capitalisation check.

I recomputed the headline figures from the data summary and they are internally consistent. I did not find any arithmetic errors in the core numbers.

**Recomputed and consistent:**
- Token total: 9,248,093.
- Hit total: 10,540.
- Pooled cohort rates: 11.09, 10.81, 10.94, 13.32, 11.99, 11.11.
- Corpus rate: 11.40.
- Keyness log ratios: tempest 2.09, sunlight −4.25, fog (c2) −2.83, mist 1.01, snow 1.04, tempest (c5) −2.64, misty 1.54.
- Precision counts: 140/198, 22/30, 21/24, 20/24, 14/24, 12/24, 10/24. Cohort precision: 28/33 and 18/33.
- Spearman p-values for n = 6, which match the exact permutation values.
- The flow from 128 loaded texts to 84 is consistent with the exclusion lists (c1 15, c2 14, c3 18, c4 18, c5 20, c6 20 eligible).

## 2. Major issues

### M1. Corpus composition is confounded with cohort and is not handled
The analysis spec dropped the plan's genre flags, nationality/gender stratification, dialogue/narration split and negative-control lexical fields. What remains is a cohort contrast on a convenience corpus whose composition visibly shifts.

- **Cohort 1–3 vs 5–6.** From the titles and authors listed in `data_dictionary.json`, c1–c4 are dominated by canonical and literary novels. c5 and c6 contain many Westerns, adventure, sea and pulp titles: Bar-20, Hopalong Cassidy, The Call of the Canyon, Her Prairie Knight, The Patrol of the Sun Dance Trail, Tarzan, Moran of the Lady Letty, Cappy Ricks, The River's End, The Moon Pool, The Metal Monster, Under the Andes.
- **Region.** By my reading of the titles, most c5–c6 authors appear to be North American, while c2–c4 are mostly British. I did not verify this, and no nationality coding was done per the researcher's instruction.
- **Consequence.** "Snow rises to c5", "sun plateau", "fog rise in c6" and "storm decline" cannot be separated from a shift towards outdoor-adventure genres and North American settings. Snow and ice are good candidates for setting and genre effects (Curwood, Connor, White, Grey, Norris).
- **Recommendation.** Do not code nationality or gender against the researcher's instruction. Do two things instead:
  - State plainly in the abstract and limitations that the corpus is not stratified by genre or region and that the later cohorts contain a visibly different mix of popular genres.
  - Add an appendix table listing all 84 novels (author, birth year, cohort, tokens, weather rate), so readers can see which single books drive a family rate. The same table makes the "author differences exceed cohort differences" claim checkable.

### M2. The sampling frame was built differently for different cohorts
- `data_summary.md` says extra catalogue searches (c1: novel; c2: novel, fiction, romance; c6: fiction, novel, adventure) were added "to widen thin cohorts". c3–c5 were drawn from the single 320-row frame.
- Each frame is a "popularity-sorted" search over authors alive in a window. Many rows are authors born outside the cohort: c1 window 1770–1840 catches authors born before 1770 or after 1799; c6 window 1880–1960 catches authors born after 1899. Those rows are discarded at the birth-year step.
- The effective frame depth and the degree of popularity selection therefore differ by cohort. c2 is effectively a census of its eligible pool (14 of 14, with 19 of 20 first-rank texts loaded), while c5 and c6 are random 14 of 20 and c3 and c4 are 14 of 18.
- The paper describes a uniform "stratified random sample of 14 novels per cohort from a frame of popular catalogue entries". That is not accurate for c1, c2 and c6.
- **Requests.** Report per cohort: rows read, rows with a birth year in the cohort, eligible pool size, and whether extra searches were used. State that c2 is the complete eligible pool.
- **Loading gap.** c2 loaded 19 texts, not 20. Say which id failed and whether the failure could be non-random.

### M3. The frame's popularity and eligibility fields are empty or unverifiable
`data_summary.md` states that `copyright` and `download_count` are "empty in the extract and are not used". The paper says:
- the frame is "sorted by download count";
- eligibility includes "not under copyright".

Neither condition can be checked in the data. Popularity ordering rests on the connector's server-side sort. The rule "copyright is not true" passes every row with an empty field. Reword the paper to say this, or document how it was verified.

### M4. Copyright truncation and age at writing differ by cohort
- Gutenberg holds mainly pre-1931 US-public-domain texts, so c5–c6 novels are necessarily early-career or early-century works. c1 novels span whole careers.
- Together with c6 ending at birth year 1890 (the paper notes the realised range) and the absence of any publication year, the cohorts differ systematically in age at writing and in the span of publication years.
- The paper's statement that cohorts "overlap in publication years" is true for adjacent cohorts but not for c1 vs c6. c4–c6 are near-contemporaneous publications, while c1 vs c6 are roughly a century apart.
- State both facts, and state that the unequal width of the c1 window (30 years) and the narrow c6 (about 11 years) make the cohorts non-comparable units.
- The plan's "birth year + 30" proxy was properly dropped. But a descriptive note on the publication window is needed. For example: "c6 authors can only appear through works first published by about 1930".

### M5. Tokenisation creates time-correlated measurement artefacts
The regex `[a-z]+(?:['’][a-z]+)?` has three consequences for exact-form matching.

1. **Possessives are lost.** "sun's", "wind's", "storm's", "snow's", "rain's", "cloud's" and "fog's" are single tokens and cannot match the exact forms. Possessive use ("the sun's rays") is not uniform across periods and authors. Report how many such tokens exist per cohort, or add them to the dictionary.
2. **Hyphenated compounds are split.** "snow-storm", "thunder-storm", "sun-light", "sun-shine", "rain-drops" and "snow-flakes" become two tokens, and each part may hit.
   - A "snow-storm" counts once in the snow family and once in the storm family.
   - "Thunder-storm" counts as two storm hits.
   - Hyphenated spellings are more common in nineteenth-century editions than in 1910s–1920s texts.
   - The headline keyness result that c1 is "poor in *sunlight*" (2 vs 164) and "*sunshine*" is probably an orthographic artefact. The paper's reading ("the later cohorts favour the vocabulary of light") is not supported without checking "sun-light" and "sun-shine".
   - The reduced-lexicon storm decline (1.68 to 0.96, Spearman −0.94) has the same exposure to split compounds and to the archaic term *tempest* (75 of 151 occurrences in c1). Check whether it is a lexical-replacement or orthography effect.
   - The collocate "thunder storm" (12) probably includes hyphenated forms.
3. **Dialect and elision spellings** ("rainin'", "snowin'", Scots forms in Hogg, Galt and Scott; Western dialect in Mulford and Bower) are not matched. Orthographic variation by edition and transcriber is not controlled.

**Recommended robustness:** a version that joins hyphenated weather compounds into single tokens, counts each once and adds possessives. Also report per-cohort counts of weather-word hyphen and possessive tokens.

### M6. Hand-check validation: sample design, uncertainty, and over-reading
- **Oversampling of ambiguous terms.** Ambiguous terms are "placed first within each cohort cell" and the sample is not weighted by term frequency. Family precision (storm 0.42, fog 0.50, cloud 0.58) is therefore biased downward for the corpus, and the pooled 0.71 is a precision of the sampled mix, not of the dictionary.
  - The abstract and introduction nevertheless state "precision of the dictionary is 0.71 overall" and "between four and six in ten hits … are figurative or have another sense".
  - The pooled figure also double-counts: the 30 composite items overlap the family items in word type.
  - Provide weighted estimates. Re-weight the 198 judgements by term × cohort frequency strata, or draw a probability-proportional-to-size sample, and give Wilson or bootstrap intervals for every precision. With n = 24 per family the Wilson interval is roughly ±0.19 to ±0.20.
- **Thin cells.** Per cohort the families have about 4 items each. "None of four sampled fog hits in cohort 6 was weather" is a 0/4 result.
  - The 95% Wilson upper bound is about 0.49, which includes the overall fog precision of 0.50.
  - The statement "the fog rise cannot be read as more fog description" is a reasonable caution, but it is stated as an established fact in the abstract, introduction, results and conclusion. It needs more items for cohort-level fog hits, and the *mist* and *misty* forms behind the c6 keyness result should be checked specifically.
- **Cohort-level precision.** The variation in precision by cohort (0.85 vs 0.55, 33 items per cohort) is the most important validation finding for a cohort design, because it means raw cohort differences are partly measurement.
  - The paper notes this but does not adjust.
  - The plan promised a precision-adjusted sensitivity analysis; it is missing.
  - Provide one, even if it is rough, or at least bound the range of the cohort differences.
- **Coder and reliability.** The paper does not say who made the judgements. The plan promised a second coder on 20% of items with Cohen's κ. None is reported. State the coder, the coding rules and whether the coder saw the cohort labels, and report κ or state that it is unavailable.
- **No hold-out.** The post-hoc reduced lexicon was designed from the same 198 judgements, and its storm family was not re-checked. The researcher-mandated hedging ("pattern worth testing") is appropriate. A fresh 40–60 item hand check of the reduced storm family is the minimum before the conclusion's future-research sentence can be called a pre-specified test.

### M7. The leave-one-out claim is contradicted by the paper's own numbers
The paper says: "Leave-one-author-out rates show that no single author reverses a cohort's position." The numbers it reports:
- c1 leave-one-author-out range: 9.42 to 12.29. The full c1 rate is 11.09.
- Other cohorts' pooled rates: 10.81 (c2), 10.94 (c3), 13.32 (c4), 11.99 (c5), 11.11 (c6).
- Dropping one c1 author can therefore move c1 below every other cohort (9.42) or above c2, c3 and c6 (12.29).
- One author supplies 30.9% of c1 hits, 26.9% of c6 hits and 23.4% of c4 hits.

The claim should be removed or replaced by a table of leave-one-out ranges for all six cohorts together with the resulting ranks.

Related inconsistencies:
- The c4 leave-one-author-out minimum (12.29) is above the c4 rate without the heaviest *novel* (11.92). Explain how, for example whether the heaviest novel's author has two novels.
- The text compares the c4 "bump" with the c5 rate of 11.42, which is the c5 rate without its heaviest novel. The full c5 rate is 11.99. Compare like with like.
- The claim that author differences exceed cohort differences rests on the author range (2.10 to 31.35) set against the range of cohort means. Extremes against means is not a like-for-like comparison. With at most two novels per author, the author extremes also include sampling noise. Report the share of variance between cohorts (an intra-class correlation or variance decomposition) with an author-clustered bootstrap.

### M8. "Flat vs rising" lexicon contrast is overstated
- The text calls the full dictionary "flat" (Spearman 0.60, p = 0.21) and the unambiguous lexicon "rising" (Spearman 0.71, p = 0.11). The two correlations are statistically indistinguishable.
- The contribution claim ("the same data yield a flat or a rising composite profile depending on which terms are retained") is made without any uncertainty on the difference between lexicon variants.
- The capitalisation check is described as leaving the picture "unchanged", yet the extended-lexicon Spearman falls from 0.60 to 0.31 (p from 0.21 to 0.54).
- Provide an author-clustered bootstrap CI for (c6 − c1) and for the Spearman difference between lexicon variants. Otherwise soften the claim.

### M9. Dictionary and variant definitions are inconsistent or not reproducible
- The 90 forms are not printed in the paper. Add an appendix listing every form, its family and its ambiguity flag. Say that it was frozen before the cohort results were seen (the design was revised at the design-review step before the analysis was run).
- The core lexicon is described in three ways:
  - The spec says "twelve headline words and inflections" (rain, wind, storm, fog, snow, sun, cloud plus mist, thunder, frost, breeze, sunshine).
  - The paper says "23 forms … from the focal terms named in the research question and their plurals". Seven terms with plurals would give about 14 forms.
  - The code defines it differently again.
  - Reconcile and list the 23 forms.
- The "unambiguous" lexicon removes *wind*, *storm*, *sun* and *cloud* forms, which are four of the seven research-question words. Yet the validation found wind and sun at 0.88 and 0.83 precision. The ambiguity flag is a prior, not an empirical result. Say so, and consider an "empirically validated" subset.
- The post-hoc variant changes two things at once: it drops forms and drops capitalised mid-sentence hits. The two effects cannot be separated. Report them separately.
- **Capitalisation heuristic.** It also removes legitimate hits in sentence-initial quoted speech, headings, verse, and older texts that capitalise common nouns. The latter are likely more common in c1 editions. Report the number of hits removed by cohort.

### M10. Sample size, planned thresholds and unreported specified outputs
- The plan set a minimum of 30 authors per cohort for any comparison. The corpus has 9 to 14 authors per cohort and 84 novels, against "several hundred to a couple of thousand" planned. The paper notes that the sample is small, but it does not say the planned threshold was missed. State the departure.
- With 9–14 clusters, percentile bootstrap intervals are unreliable (under-coverage is likely). The c2 interval (7.01 to 15.32) already shows how unstable it is. Use BCa intervals or state this caveat.
- The Spearman p-values treat the six cohort rates as exact. The spec promised an OLS slope on the novel-level rate with an author-clustered bootstrap CI and a length-adjusted slope; neither appears in the paper. These would address the point directly and are cheap to add.
- Other specified or planned outputs are absent:
  - the share of novels using each term and the number of authors using each term;
  - whole-vocabulary keyness and a negative-control lexical field. Without a control, "weather is stable" cannot be separated from a general shift in the density of concrete vocabulary or in dialogue share;
  - lexical diversity (planned Q5);
  - robustness to the length threshold, the per-author cap and alternative cohort splits (e.g. c1 halved).
- The sentence "We report all families and lexicon variants we computed" is accurate for what was run, but readers should be told that the planned specification table was not produced.

## 3. Moderate issues

- **Sample flow is incomplete in the paper.** The prose gives 4,160, 1,409 and 632. The numbers 120, 128, 108, 105, 84 and the counts dropped (20 translations/non-novels, 3 for length, 21 cut to equal n) are in the data summary but not in the text. Add a flow table.
- **Manual exclusions.** Translations and non-novels were identified by reading titles, authors and shelves after loading, and only for books in the loaded sample. The unloaded part of the eligible pool was not screened the same way. Say so. The catalogue has no translator field, so undetected translations are possible. The loose subject filter let non-fiction through (*Criminal Sociology*, *Book of Pirates*, *Sartor Resartus*). Residual borderline items remain (*Tom Cringle's Log*, *The Country of the Pointed Firs*, *Phantastes*, *Moby-Dick* with its extracts). Give the final corpus list with a one-line genre note.
- **Anonymous authors.** The rule "single catalogue person with a recorded birth year" removes anonymous and pseudonymous works. These were common in early nineteenth-century fiction, so c1 and c2 are likely thinned in a non-random way. Mention it.
- **Title and place-name contamination.** Titles containing weather words (*After the Storm*, *The Patrol of the Sun Dance Trail*) and place names ("Sun Dance", newspaper "the Sun") inflate sun and storm counts in individual books. Running heads and chapter headings may add hits. The paper mentions "Sun Dance" only within the validation discussion. Report the effect on the c5 sun family.
- **Front matter.** Only 48,466 characters were cut across 84 texts (about 580 per text). Editorial introductions, footnotes, indexes and appendices are probably largely retained. The paper says "where they can be detected". Quantify what remains, for example by reporting the largest per-book cut and a spot check of five books.
- **Keyness reporting.** In c1 the text cites term indices 0, 1, 2, 3 and 5. Index 4 is not mentioned, so one qualifying term appears to be omitted. Report all qualifying terms in a table with the sign of each. For c6 the text says the "next terms, *tempest* and *fog*, fall below the threshold". It does not give the direction of *tempest*, which is later described as rare in c5 and c6. State the sign.
- **Reference size.** "The reference is five times as large" for the c1 tempest contrast; the reference is about 4.3 times the target (7.5M vs 1.74M tokens).
- **Weak descriptive statements.** "Every one of the 84 novels contains at least one weather word" has no information given 30,000+ tokens and a 90-form list. Replace with the share of novels with at least 3 hits, or the distribution of per-novel rates.
- **Sub-family claims.** The statements about wind ("no ordered drift"), sun ("plateau near 3") and precipitation rest on pooled rates without intervals shown in the text. Add the intervals from the tables.
- **Hanlon/Laughlin framing.** c2 includes Dickens-era authors, yet *fog* is nearly absent (9 of the 193 fog tokens). The sample contains no famous fog novel. Say that the null for fog in c2 reflects which novels were sampled, and that the sample cannot test claims about Dickens.

## 4. Minor issues

- State the realised cohort boundaries once in a table (min/max birth year, authors, novels, tokens), including that c6 is 1880–1890.
- Report median per-novel tokens and the range by cohort in the main table. The text says earlier cohorts have longer novels, but normalisation by tokens does not remove a length–density relationship. Show the weather rate against novel length, or stratify by terciles.
- The sentence "A document is one novel" conflicts with multi-work files. Confirm that no file contains more than one work.
- Cite the corpus manifest (`corpus_manifest.json`, SHA-256 of the analysed texts) and state that the Gutenberg mirror files are mutable, so the recorded hashes identify the version used.
- The Gutenberg catalogue's birth years are volunteer-entered and sometimes uncertain. Spot-check a sample against an authority file and report the error rate.
- Say whether intervals in the tables are for pooled or per-novel rates, and which draw count and seed they use.

## 5. Checklist summary

| Checklist item | Status |
|---|---|
| Source, version, licence, access documented | Good (catalogue/text sources, release date, SHA-256). Download-count and copyright fields empty (M3). |
| Unit of observation, population, geographic scope | Partly. Unit clear; population is "popular Gutenberg novels"; region and genre composition unknown and visibly shifting (M1). |
| Sample flow | In summary files only; incomplete in the paper (Section 3). |
| Cohort-specific frame construction | Not uniform; undisclosed (M2). |
| Missing values | Not an issue for metadata (complete); anonymous/no-birth-year exclusions not discussed. |
| Variable definitions | Dictionary not printed; core lexicon inconsistent (M9); tokenisation artefacts (M5). |
| Outliers / influence | Leave-one-novel and leave-one-author reported, but the interpretation is contradicted by the numbers (M7). |
| Measurement quality | Hand check exists but is small, biased towards ambiguous terms, single coder (M6). |
| Clustering | Author bootstrap for rates; keyness and Spearman p ignore it (M10). |
| Planned vs delivered | Many planned outputs and thresholds missing (M10). |
| Replication | Seeds, hashes and scripts recorded. Appendix with the term list and per-novel table needed. |

## 6. Priority requests to the authors

1. Add a per-novel appendix table and a cohort-level frame table (M1, M2). Disclose the uneven frame construction, that c2 is a census, and the missing c2 text.
2. Replace the abstract's "0.71 overall precision" with frequency-weighted precision estimates and intervals, or label it explicitly as the precision of the validation sample (M6). Report coder identity, κ, and a precision-adjusted sensitivity analysis.
3. Correct or remove the leave-one-author-out sentence, and report ranks under leave-one-out (M7).
4. Run and report a tokenisation robustness check: hyphenated compounds joined, possessives added, no double counting (M5). Revisit the sunlight/sunshine and storm-decline interpretations afterwards.
5. Provide author-clustered bootstrap CIs for the slope, the (c6 − c1) difference and the differences between lexicon variants (M8, M10). Soften "flat vs rising".
6. Print the 90-form dictionary with flags and reconcile the core-lexicon definition (M9).
7. Add the missing flow numbers and a control lexical field if feasible (Sections 3 and 2.M10).
8. State the copyright-truncation and age-at-writing limitations and the genre/region shift explicitly in the abstract and limitations (M1, M4).

## 7. Verdict

The descriptive claims are mostly hedged, and the headline numbers reproduce. The data foundation is thin for cohort-level inference: 9–14 authors per cohort, uneven frame construction, visible genre and region shifts, tokenisation artefacts that correlate with period, and a validation sample that cannot yield corpus-level precision. The paper's most distinctive contribution, a validation template and a demonstration of measurement sensitivity, needs the weighted precision estimates, the coder reliability and the lexicon-difference uncertainty to be credible. These are repairable with the existing data.

OVERALL SCORE: 5.5/10
RECOMMENDATION: Major Revision
