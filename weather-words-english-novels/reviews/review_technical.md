# Technical Review

Scope and limits of this review: I had the draft text (with its `% src` comments), the specification, the data dictionary, the data summary and the plan. I did not have `estimation_results.json`, `text_validation.json`, `summary_statistics.json` or the `\input` tables. Source-traced numbers are therefore checked only where they can be re-derived from other numbers in the draft or the data summary. Everything else is marked unverifiable.

## Summary Assessment

**Concerns (borderline Fail on the interpretation layer; the counting layer looks sound).**

The counting layer is transparent and mostly internally coherent:
- Corpus totals, per-cohort hit counts, pooled rates and the keyness arithmetic all re-derive (details below).
- Hedging is generally good, and the draft states that tokens are treated as independent in keyness.

The inferential layer is weaker, for six reasons:
1. The headline "stable composite rate" is not reconciled with the paper's own finding that precision differs sharply by cohort (0.85 vs 0.55).
2. The fog-rise argument rests on four items, and the post-hoc robustness result barely weakens the rise in magnitude. The text and the numbers point in different directions.
3. The tokeniser splits hyphenated and possessive forms. This is a period-dependent measurement artifact that affects exactly the compound and sun/snow/storm terms the paper interprets.
4. Validation is a single-coder, oversampled-ambiguous design. The paper nonetheless reports corpus-level statements ("four to six in ten hits") and an overall 0.71.
5. Several analyses promised in the specification (author-clustered slopes, length-adjusted slopes, genre flags, precision adjustment, second coder) are not reported. Others (leave-one-out for families, keyness dispersion) were never run.
6. The "random sample" description does not fit cohorts 1 and 2, which are close to census draws of a small frame.

None of these is fatal for a descriptive paper that already calls most findings "suggestive". They do mean several sentences in the abstract and conclusion are stronger than the evidence.

## Data Pipeline

**What re-derives:**
- Tokens sum to 9,248,093 across the six cohorts.
- Hits sum to 10,540. Pooled rates: c1 1,933/1.743M = 11.09; c2 10.81; c4 13.32; c6 11.11. Corpus-wide rate 11.40.
- c3 (10.94) and c5 (11.99) are consistent with the "11 to 13" claim.
- Sample-flow counts are arithmetically consistent: 128 − 20 = 108; 108 − 3 = 105; 105 − 21 = 84.
- Per-cohort author counts (10+13+11+12+14+9) sum to 69.
- The median-length ordering supports "earliest two cohorts are longer".

**Issues:**

1. **"Not under copyright" filter versus the data summary.** The paper and `inclusion_rules` say eligibility required "not under copyright". The data summary says the `copyright` and `download_count` fields "are empty in the extract and are not used". If the field was empty, the filter could not have been applied as described. State how the copyright criterion was actually operationalised (the Gutenberg corpus is U.S.-public-domain by construction, which is a different thing). The same applies to "sorted by download count": the sort is the API's, and the field is unavailable for audit.

2. **"Random sample" is misleading for cohorts 1 and 2.**
   - Cohort 1 had 15 eligible novels (14 kept); cohort 2 had 14 (pool exhausted, even after extra searches).
   - Cohorts 3 to 6 drew from 18 to 20 eligible novels. So only the draw rank, not much randomness, decides membership everywhere.
   - The Introduction's "stratified random sample of 14 novels for each of the six cohorts" should say the sample is close to the entire eligible frame for c1/c2. The frame is the top-320 popularity list, and the eligible set shrank by hand-curated exclusions.
   - The exclusions (20 ids) were made by reading titles, authors and shelves *after* texts and word counts were loaded. Say so, and say that residual translations or non-novels cannot be ruled out. The data summary admits this; the paper does not. Known borderline residue includes Phantastes, The Country of the Pointed Firs (linked sketches, only just over 30k tokens) and some very short items near the 30,914-token minimum.

3. **Copyright truncation confounds the cohort axis with career stage and genre.** Authors born 1880–1890 enter Gutenberg only through works published before roughly 1930, i.e. early-career, pulp, Western, mystery and adventure books. Cohort 1 enters with whole careers. The paper discusses period/cohort/age overlap but not this systematic truncation or the genre shift (e.g. Mulford, Grey, Curwood, Rohmer, Merritt in c5/c6; Gothic and historical romance in c1). The plan promised genre flags and a genre-mix report; none appears. Without them, "cohort" differences cannot be separated from "genre mix of the surviving popular titles".

4. **Cohort width.**
   - The nominal 1770–1799 cohort is 30 years wide (realised 1770–1797, 27 years). The others are about 16 to 19 years.
   - The Spearman statistics and any "trend" language treat the six as equally spaced.
   - The planned C1 split robustness (1770–1784 / 1785–1799) was dropped. With 10 authors this is understandable, but it should be listed as a limitation.
   - The plan's own minimum (30 authors per cohort for any comparison) is violated everywhere (9 to 14). Only the limitations paragraph hints at this.

5. **Tokenisation artifacts (substantive, untested).** The pattern `[a-z]+(?:['’][a-z]+)?` after lower-casing has three consequences.
   - **Hyphenated compounds split.** `snow-storm`, `thunder-storm`, `sun-set`, `sun-light`, `sun-shine`, `wind-mill`, `rain-bow`, `snow-ball`, `sun-flower` yield two tokens, each a dictionary hit.
     - Single phenomena are double-counted in the composite, and non-weather compounds (windmill, sunflower, snowball) become false positives.
     - The collocate "thunder storm" (12) may well be `thunder-storm` split by the tokeniser, not a two-word phrase.
     - Hyphenation conventions changed across the nineteenth and early twentieth century and vary by editor. Hyphen-versus-solid spelling therefore varies with cohort. This could contribute to the keyness results for *sunlight* (c1: 2 vs 164) and *sunshine*, because early texts may print `sun-light` and `sun-shine`, which are counted under *sun*.
   - **Possessives and clitics are single tokens.** `sun's`, `wind's`, `storm's`, `rain's` and `snow's` do not match the exact forms. They are a common construction ("the sun's rays") and are a recall loss that may vary by cohort. The paper's recall caveat lists `pouring`, `drenched`, `chilly` and `blew` but not this.
   - **Archaic or dialect spellings** are not normalised, and Gutenberg editions carry editor-dependent orthography.

   None of this is checked. A one-off rerun with hyphens split into separate tokens versus joined, and with possessives stripped, would show whether the sun, storm and snow profiles move.

6. **Provenance of two numbers.** The cohort-level precision (28/33, 18/33) and the "0 of 4 cohort-6 fog hits" are marked as hand-computed from `text_validation.md`/`.json`, not read from a results field. Put both in the results JSON so the number check can trace them.

## Estimation Implementation

**Specification versus what the paper reports.** The specification promised several things the draft does not report, or reports only in part. I cannot tell from the draft whether they were computed and omitted or never run.

| Specified | In draft |
|---|---|
| Item 5: OLS slope of novel-level rate on cohort index with author-clustered bootstrap CI | Not reported; only 6-point Spearman |
| Item 5: same slope with log novel length as covariate (the plan's key confound) | Not reported |
| Item 4: keyness for all unigram types and document-level dispersion beside it | Only dictionary-term keyness; no novel/author dispersion for any key term |
| Plan §4: precision-adjusted frequencies if precision varies by cohort | Not done, although precision is shown to vary (0.85 vs 0.55) |
| Plan §4: second coder on a 20% subsample, Cohen's κ | Not mentioned |
| Plan §5: share of novels using each term; diversity measures | Only "share_docs_with_hit" for the composite |
| Spec item 8(a): "core lexicon = the twelve headline words and inflections" | Paper: "23 forms … focal terms and their plurals"; unclear which is right |

"Extended lexicon" appears in the robustness text without definition. I infer it is `weather_all`; say so. If items were computed and dropped, the paper should state "we report all families and lexicon variants we computed" more carefully. That sentence in the Limitations is only true for the lexicon variants.

**Inference.**

- **Spearman on six aggregate points.**
  - The p-values re-derive correctly for n = 6. For example ρ = 0.83 gives p ≈ 0.042, ρ = −0.94 gives p ≈ 0.005, ρ = 0.60 gives p ≈ 0.21.
  - They take the six cohort rates as exact and ignore author clustering, so they are descriptive only. The paper already says this.
  - A novel-level or author-level permutation test (permute cohort labels across authors) would give a defensible p-value.
- **Multiplicity count.**
  - "Two of 15 profiles below 0.05, both snow-related; one expected by chance" is fine as arithmetic (0.75 expected).
  - The two are the same signal (family and its dominant term), so effectively one hit in about 15 independent-ish tests.
  - The post-hoc storm test (p = 0.005) and the robustness variants (about 8 more profiles) are not in the denominator. The total search over lexicons, families and cohort summaries is larger than 15.
  - A footnote giving the full count of profiles examined would be more honest.
- **Author-bootstrap intervals.** With 9 to 14 clusters per cohort, percentile intervals under-cover. Cohort 6 resamples 9 authors. Report bias-corrected or studentised versions, or acknowledge anti-conservatism. The interval widths (e.g. 7.01–15.32 for c2) already show how little the data constrain cohort differences.
- **"Stability" is asserted from non-rejection.**
  - The abstract and Introduction say "remarkably stable". The Introduction's own fourth finding says only large differences can be distinguished.
  - The cohort 4 rate is about 20% above cohort 2's, and the intervals overlap broadly. This is absence of evidence of a difference, not evidence of equivalence.
  - Replace "remarkably stable" with "no difference distinguishable from noise", or report an equivalence-type bound.
- **Between-author versus between-cohort variance.** "Differences between authors are larger than between cohorts" is backed by min/max/median over 69 authors. A variance decomposition or ICC would substantiate it; min–max over many authors will always exceed the range of six pooled means.

**Keyness arithmetic.** I recomputed log ratios from the counts in the draft and the token totals in the data summary. All matched:

| Term | Counts | Log ratio |
|---|---|---|
| tempest (c1) | 75 vs 76 | 2.09 |
| sunlight (c1) | 2 vs 164 | −4.25 |
| fog (c2) | 9 vs 184 | −2.83 |
| sunshine (c2) | 141 vs 177 | 1.19 |
| mist (c4) | 69 vs 217 | 1.01 |
| sunlight (c4) | 44 vs 122 | 1.19 |
| snow (c5) | 137 vs 529 | 1.04 |
| tempest (c5) | 3 vs 148 | −2.64 |
| misty (c6) | 25 vs 58 | 1.54 |

I also recomputed G² for sunlight in c1 (≈ 53.6, matching the 53.52 reported). Minor wording slips:
- "the reference is five times as large" for tempest in c1 is 4.3 times (7.5M vs 1.74M tokens).
- "Cohort 1 favours … clouds … and later cohorts the vocabulary of light" generalises from two terms (sunlight, sunshine) while the sun family itself rises only from 1.98 to a plateau near 3.

## Results Reporting

1. **Differential precision undermines the composite-stability claim (most important).**
   - Precision is 0.85 in cohort 4 and 0.55 in cohort 6 (33 items each).
   - The raw composite is 13.32 in c4 and 11.11 in c6. Scaling by those precisions gives roughly 11.3 versus 6.1 true weather hits per 10,000 tokens.
   - So the "stable" raw rate is compatible with a substantial decline in true weather vocabulary.
   - The intervals on cohort precision are wide and the sample is oversampled on ambiguous forms, so this is only a plausibility bound. It still shows the stability claim and the precision finding cannot both stand unqualified.
   - The plan promised a precision-adjusted sensitivity analysis. The draft substitutes a post-hoc term-list reduction instead. At minimum report precision-adjusted rates with propagated uncertainty, or drop "stable" from the abstract's lead.

2. **Fog: text and numbers disagree.**
   - Original fog/mist family: 0.73 (c1) → 1.53 (c6), a ratio of 2.1.
   - Post-hoc reduced lexicon: 0.65 → 1.26, a ratio of 1.9. The rise in magnitude is nearly unchanged. Only the Spearman p-value moves, from 0.072 to 0.266, and that is mostly a non-monotone-profile artifact of 6 points.
   - "Weakens the fog rise" in the abstract and Section 4.2 reads as if the rise were largely an artifact of unusable forms. It is not.
   - The "0 of 4" claim comes from a stratified-with-ambiguous-first sample. The four c6 fog items are probably *haze/hazy* or other flagged ambiguous forms. They are not a representative draw of c6 fog/mist hits (which, per keyness, are driven by *misty* and *mist*). The paper reports no precision for *mist* or *misty* at all.
   - Conclusion "cannot be read as more fog description" is therefore stronger than the evidence. Say instead that the fog/mist rise is of unknown validity, and report mist/misty precision from the existing or an enlarged sample.
   - Report the fog/mist family's leave-one-author-out range in c6 (9 authors; two Rohmer novels are plausible London-fog contributors). I raise this as a hypothesis to check, not a claim.

3. **Snow and ice.**
   - The headline rise (0.82 → 2.06 → 1.44) is called "suggestive". The paper gives no author/novel dispersion for the family, though it does so for the composite.
   - The c5 peak plausibly rests on a few northern-setting novels (e.g. titles with Canadian or lumber-camp settings are in c5). Setting, not literary vocabulary change, may be the driver. Report leave-one-out by novel/author and the contribution of the top three novels.
   - The "capitalised mid-sentence" robustness covers surnames only.

4. **Leave-out statements.**
   - "No single author reverses a cohort's position": in cohort 1 the leave-one-author-out minimum is 9.42, below the full-sample c2 rate of 10.81. Dropping that author would move c1 from above c2 to below it. Cohort 1's range (9.42 to 12.29) also brackets other cohorts' point estimates.
   - The statement should be restricted to cohort 4, and even there the heaviest-novel removal (13.32 → 11.92) shows one novel carries the bump.
   - "Brings it close to the cohort 5 rate of 11.42" compares c4-without-heaviest with c5-without-heaviest. The full c5 pooled rate derives to 11.99. Clarify.
   - Two reported values coincide, which I flag for verification against the JSON: the c4 leave-one-author-out minimum is 12.29 and the c1 maximum is 12.29. Also |ρ| = 0.09 (p = 0.872) appears both for the heaviest-novel-removed trend and for the post-hoc reduced composite, with opposite signs. These are arithmetically possible, since n = 6 allows only 35 ρ-values in steps of 1/35, but check for copy errors.

5. **Core lexicon description.** "flat to slightly rising from 8.36 … to 8.03" is not rising: c6 is below c1. "Flat" is correct, and the conclusion should not carry "slightly rising".

6. **Unambiguous lexicon is not a like-for-like robustness check.**
   - It drops wind, storm, sun and cloud forms. These are four of the seven focal words in the research question.
   - Its rising profile (ρ = 0.71) and the post-hoc reduced profile (ρ = −0.09) contradict each other on the composite. The paper handles this honestly ("we do not choose").
   - The more natural conclusion is that the composite's cohort shape is not identified at this sample size. The abstract's "flat" lead paragraph should say that.

7. **Capitalised-hit robustness.** "Leaves the picture unchanged" is loose: the extended composite ρ moves from 0.60 to 0.31, and the unambiguous one from 0.71 to 0.77. Quote the before/after values.

8. **Collocates.**
   - The collocate paragraph contains no counts for most pairs, and cites a path rather than values. It is unverifiable for the pair list.
   - The sentence "consistent with the high precision we find for rain and wind families" does not follow. Adjacent-pair PMI for top-ranked pairs (min count 5, PMI favours rare pairs) says nothing about corpus-level precision. The very next sentence concedes it. Delete the earlier link.
   - Check whether "thunder storm" is a hyphen artifact (see Data Pipeline 5).

9. **Validation reporting.**
   - **Overall 0.71.** It pools a composite sample (30) with seven family samples (24 each). The composite hits are a mixture of the same families, and the stratification is by cohort, ambiguous-first, and unweighted by frequency. The pooled share of 198 items has no population interpretation. Do not headline it in the abstract. Report per-family values only, with Wilson intervals (e.g. 21/24 = 0.875 has interval about 0.69 to 0.96).
   - **Corpus-level claims.** "Between four and six in ten hits in these three families are not weather" and "the dictionary is a good measure of precipitation, wind, snow and sun" are statements about corpus hits. They contradict the paper's own caveat that sampled mix, not corpus-weighted precision, is estimated. Corpus-weighted precision can be computed by post-stratifying the sample by term frequency. That is the number the cohort rates need.
   - **Single coder; coding rule.** The judge appears to be a single coder, and the paper does not say who. The plan required a second coder and κ. The rule "names a weather or sky phenomenon" counts "the sun as a god or cosmic body" as wrong. That is a coding decision with direct effect on the sun-family precision and should be justified.
   - **Cell sizes.** Cohort-by-family precision rests on n = 4 per cell. The cohort-precision contrast of 0.85 versus 0.55 is the maximum-minimum over six cohorts, which overstates the between-cohort difference. The ±0.16 interval ignores clustering of items within novels.
   - **Recall.** It is not estimated. A small random sample of weather passages from the text (not dictionary-based) would estimate it.

## Red Flags

- **Selective use of the p-value rule.** p = 0.042 (snow) is called suggestive and p = 0.005 (post-hoc storm) a pattern worth testing. Both are defensible and honestly labelled. The risk is the garden of forking paths: the lexicon was changed after viewing the validation, the storm family then yields the smallest p in the paper, and the conclusion already recommends a follow-up on it. Keep it labelled as hypothesis-generating, and list how many reduced-lexicon variants were considered.
- **Specification searching.** There is a spread of composite profiles by lexicon: ρ = 0.60 (full), 0.14 (core), 0.71 (unambiguous), 0.31 (extended minus capitalised), 0.77 (unambiguous minus capitalised), −0.09 (post-hoc), 0.09 (heaviest removed). The paper reports them all. That is good practice, and the instability itself is the finding. Say so in the abstract.
- **P-value clustering.** There is no unusual clustering just below 0.05 (the near-threshold values are 0.042, 0.072, 0.111, 0.156). Nothing to report here.
- **Magic numbers.** The following are documented: G² = 15.13, minimum count 10 for keyness, minimum collocate count 5, 30,000-token floor, seed 20261014 (reused for the sample draw and the bootstrap). The threshold G² = 15.13 is a per-test cutoff over roughly 80 terms × 6 cohorts and takes no clustering into account. The paper says so, but the keyness lists remain framed as "markers" in the abstract and Introduction. The section itself says "candidates for reading and not established cohort markers". Make the abstract and Introduction consistent with that: *tempest* is not shown to be an "earliest-cohort marker" until its distribution across novels and authors is reported.
- **Unverifiable share.** Counting only the source-comment items, most in-text claims could not be checked here because the JSON and the tables were not supplied. I could verify about a third (all derived totals and rates, keyness arithmetic, validation count sums and rounding). The Section 4.1 per-family and per-term values and the Section 5 robustness values are unverifiable by me.

## Strengths

- Preprocessing and dictionary are frozen, exact-form and documented. The explicit exclusion of *hail* and *storming* and the avoidance of wildcards (wind ≠ window) are sound and well argued.
- Sampling flow is fully accounted for and reconciles at each step. The paper reports the front-matter cut, seed and equal-n rule.
- Author-clustered bootstrap, per-novel and pooled rates, top-author shares and the heaviest-novel and leave-one-author-out checks go beyond what most dictionary studies do.
- Honest limits: no causal claim, no publication year, cohort/period/age confounding, popular-frame bias, G² overstating certainty, rank-only role of keyness.
- The validation finding on storm, fog and cloud words (figurative use, steam, faces) is specific and useful, with term-level false-positive patterns.
- The post-hoc robustness is flagged as post hoc rather than folded into the main analysis, and the storm decline is correctly demoted to "pattern worth testing".

## Recommendations

**Data stage**
1. State how "not under copyright" was applied given the empty `copyright` field. Disclose that translation/non-novel exclusions were by manual reading and may leave residue. Rephrase "random sample" for c1/c2 (near-census of a 14–15-book eligible pool).
2. Rerun counts with hyphenated compounds split versus joined, and with possessive `'s` stripped (or `sun's`, `wind's`, `storm's`, `rain's`, `snow's` added). Report the effect on the sun, storm and snow profiles and on the sunlight/sunshine keyness. Check whether "thunder storm" is `thunder-storm`.
3. Add a genre and setting description by cohort (even coarse, from the Gutenberg bookshelves) and discuss copyright truncation of c5/c6 careers.
4. Note the unequal c1 width and the dropped C1 split; list the 9 to 14 author cohort sizes as below the plan's own minimum.

**Estimation stage**
5. Report the specified novel-level OLS slope with author-clustered bootstrap CI, with and without log length. Or state they were not run. Use an author-level permutation test for cohort trends. Report the full count of profiles examined, including the robustness and post-hoc variants.
6. Report document/author dispersion (number of novels and authors, top-author share) for every key term and for the snow and fog families by cohort. Report leave-one-author-out for family-level profiles, not only the composite.
7. Reconcile the core-lexicon definition (12 headline words versus 23 forms) and define "extended lexicon". Quote before/after ρ in the capitalised-hit check.

**Validation stage**
8. Drop the overall 0.71 from the abstract. Give per-family precision with Wilson intervals; compute corpus-weighted precision by post-stratifying on term frequency. Add precision for *mist*/*misty*.
9. Get a second coder on at least a 20% subsample and report κ, or state that only one coder was used and who/what it was. Justify the "sun as a god or cosmic body = wrong" rule.
10. Add precision-adjusted cohort rates for the composite and the three weak families, with propagated uncertainty, as the planned sensitivity analysis. Estimate recall on a small random weather-passage sample.

**Draft stage**
11. Replace "remarkably stable" with non-rejection wording. Remove the claim that no single author reverses a cohort's position, or restrict it to cohort 4.
12. Revise the fog statement: the post-hoc rise is 0.65 → 1.26 (ratio 1.9 versus 2.1), so only the monotonicity weakens. Present the 0-of-4 finding as a four-item, ambiguous-first, uncertain datum, not as evidence the rise is not weather.
13. Delete the collocate-to-precision link. Fix "five times as large" (4.3), "slightly rising" for the core lexicon, and the cohort 5 comparison sentence in Section 4.1.
14. Put the cohort-level precision and the cohort-6 fog counts into the results JSON so the number check can trace them.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
