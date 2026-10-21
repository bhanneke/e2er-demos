# Methods Review: Vocabulary of Weather in English-Language Novels by Author Birth Cohort

Scope and limits of this review. I read the draft, the specification, the data dictionary, the data summary and the researcher's instructions. `run_estimation.py` and `estimation_results.json` were not in the material I was given, so I could not check script lines. I did recompute from the draft's own numbers wherever they allow it. All keyness log ratios and G2-independent figures I could rebuild from the cohort token totals in the data summary agree with the paper. They are: tempest 2.09, sunlight -4.25, fog (c2) -2.83, mist 1.01, snow 1.04, tempest (c5) -2.64, misty 1.54, sunshine 1.19. The pooled rates also agree: 11.09, 10.81, 13.32, 11.11 and 11.40. The arithmetic is sound. The problems lie in design, inference and interpretation.

## Overall assessment

This is a careful, candid descriptive study. It reports its limits, flags the post hoc variant as post hoc, validates the dictionary by hand, and uses author-level resampling. For a six-point cohort profile with 84 books, though, the inferential layer does not carry what the abstract and contributions claim. The main problems are:

- The Spearman p-values are asymptotic and anti-conservative at n = 6.
- Several words are reported as cohort markers without any document or author dispersion.
- The validation sample is small, purposive and single-coder.
- The cohort contrasts are confounded with genre and setting, which the design cannot separate.
- A few sentences contradict the paper's own numbers.

## Must change

### M1. Spearman p-values with n = 6 are asymptotic, and they change the headline result
Section 4.1 and the Section 3.3 text report `p` values that match the t-approximation. For example ρ = 0.60 gives p = 0.208, ρ = 0.83 gives 0.042, ρ = 0.77 gives 0.072 and ρ = −0.94 gives 0.005. With six points the approximation is badly anti-conservative. By my calculation the exact two-sided permutation p is about 0.06 for ρ = 0.83 and about 0.017 for ρ = −0.94. For ρ = 0.77 it is about 0.10, and for ρ = 0.71 about 0.14 (reported 0.111). Consequences:

- The "snow and ice rise is suggestive (p = 0.042, one of two below 0.05)" claim loses its only statistical support. Neither snow profile reaches 0.05 on an exact test.
- The post hoc storm decline is reported at p = 0.005, which overstates the evidence by a factor of about three.
- Fix: compute exact p-values by enumerating all 720 permutations (`scipy.stats.permutation_test`), and state this in Section 3.3. Better, replace the cohort-level correlation by a test at the unit that is clustered (see M2).

### M2. The trend statistic ignores the uncertainty the paper itself documents
The Spearman ρ is computed on six pooled cohort rates. Those rates have author-bootstrap intervals as wide as 7.0 to 15.3 for the composite, and the leave-the-heaviest-novel-out check moves ρ from 0.60 to 0.09. A rank correlation of six point estimates treats them as exact.

- The specification (item 5) promised an OLS slope of the novel-level rate on cohort index with an author-clustered bootstrap CI, and a length-adjusted version. Neither appears in the paper.
- Report slope with an author-cluster bootstrap CI, or a permutation test that permutes authors across cohorts. A mixed model with an author random intercept is another option. Report the length-adjusted slope too.
- Say how the bootstrap behaves with 9 to 14 clusters per cohort. Percentile intervals under-cover with so few clusters. Add a jackknife or BCa/studentised check, or at least state the caveat. The c2 interval (7.01 to 15.32 around 10.81) is strongly asymmetric, which is a sign of influential clusters.

### M3. "Stable composite" is asserted from non-significance
The abstract and introduction call the composite "remarkably stable" and the cohort differences "small". That rests on two things: nearly equal point estimates for c1 and c6 (11.09 and 11.11), and overlapping intervals. Intervals of 7.0 to 15.3 are compatible with differences of a factor of two. Overlap is an absence of evidence, not evidence of stability.

- Report the width of the plausible cohort differences, for example CIs for c_k minus c_1, and an equivalence bound if the claim is "stable".
- "Differences between authors are larger than differences between cohorts" compares the range of 60-odd author rates (2.10 to 31.35, including authors with a single short book) against the spread of six cohort means. This is not a like-for-like comparison. Replace it with a variance decomposition: the share of novel-level variance of log rates lying between cohorts, between authors within cohorts, and within authors (ICC).
- A stability finding needs a negative control. The plan (Q7) and the specification (item 4) called for whole-vocabulary keyness and a control lexical field such as kinship or colour terms. Neither is reported. Without them one cannot tell whether weather is unusually stable or whether every large lexical field looks like this at n = 84.

### M4. Keyness "markers" are reported without dispersion
The paper itself says single novels can contribute dozens of occurrences. Yet it states in the abstract and conclusion that "*tempest* is concentrated in the earliest cohort", and it gives a Section 4.3 narrative about "the sky in motion" against "the vocabulary of light". It gives no information on how many novels or authors carry each term.

- Report, for each key term, the number of novels and authors in the target cohort that use it, and the share of the target count from its top novel and top author. The specification (item 6) promised this and the template requires dispersion.
- The planned author-clustered check (Wilcoxon or permutation over authors or per-novel rates, with Benjamini–Hochberg across terms) was dropped. Run it, or downgrade every keyness statement to "candidate for reading", including in the abstract.
- The contrast "tempest, gale, clouds in c1" against "sunlight, sunshine in later cohorts" draws a trend out of cohort-versus-rest contrasts. These contrasts do not show "later cohorts favour light". In the paper's own results, c2 and c4 are marked by sunshine and sunlight, while c3, c5 and c6 are not. The c1 sample contains sea and frontier romances (*The Pilot*, *Tom Cringle's Log*, *The Prairie*) where tempest and gale are expected on setting and register grounds, not on cohort grounds.
- The reference group is pooled tokens of the five other cohorts. This weights long early novels heavily: c2 alone is 2.39M tokens against 1.04M for c5. Say so, or add adjacent-cohort contrasts as the plan intended.
- Small wording slip: the c1 reference is 4.3 times the target (7.5M against 1.74M tokens), not "five times".

### M5. Cohort effects are confounded with genre and setting, and the sampling design makes this worse
- Later cohorts are dominated by Westerns, northern wilderness adventure and pulp (Curwood, Bower, Connor, Mulford, Grey, Merritt, Burroughs). Early ones are Gothic, sea and historical romance. The snow and ice rise in c5 (*The River's End*, *The Blazed Trail*, *The Jungle*, northern settings) and the "tempest" marker in c1 are as consistent with genre and setting as with cohort. Name the top-contributing novels for every family and term discussed. The list is short and the reader can then judge.
- Fog is a case in point. c2 contains Dickens (*Barnaby Rudge*), yet shows the lowest fog rate. The canonical fog novels (*Bleak House*, *Our Mutual Friend*) are not in the draw. The c2 "near absence of fog" depends on which 14 titles were drawn. This is exactly the canonical-sample problem the introduction criticises.
- The Introduction calls the corpus a "stratified random sample". By the data summary it is not: c1 had 15 eligible novels and c2 had 14 ("pool exhausted"), so those two cohorts are close to a census of an arbitrary popularity-limited frame, while c5 and c6 draw 14 of 20 or more. The extra catalogue searches that widened thin cohorts were added only for c1, c2 and c6. Selection probabilities, and the degree of popularity bias, therefore differ by cohort. Describe the sampling honestly, per cohort, in Section 3.1 and in the Introduction.
- The plan set a minimum of 30 authors per cohort for any comparison. The final design has 9 to 14. The paper notes wide intervals, but the plan's own threshold is breached and this should be stated.
- Manual title-by-title exclusion of translations and non-novels (20 ids, by reading titles) is a researcher judgement applied after a random draw. Document the rule per excluded book in an appendix. Residual translations and non-novels (e.g. *Frankenstein* as epistolary fiction, *Phantastes*, *The Country of the Pointed Firs*) remain.

### M6. The validation sample cannot bear the weight put on it
- The sample was not random within family. Ambiguous terms were placed first within each cohort cell, so they are over-represented. The paper concedes the precisions are not corpus-weighted. It nevertheless then (a) pools 198 items into a single "precision of 0.71" for the abstract and the Section 5.1 opening, and (b) compares cohorts' precision (0.85 against 0.55). The pooled figure mixes a composite sample and seven family samples that may share hits and have different term mixes. It describes no population. Drop the pooled 0.71, or compute it as a corpus-weighted estimate: stratify by term, then weight by each term's corpus frequency. The cohort comparison is confounded with the term mix of the sampled cell.
- "None of 4 fog hits in cohort 6 was weather" rests on four items. A 0/4 result has a 95% upper bound of about 0.60. It cannot be featured in the abstract, introduction, results and conclusion as a finding about cohort 6. State the interval, or enlarge the sample (draw at least 30 per cell for the families and cohorts that carry an interpretive claim).
- Judging was by a single coder. The plan promised a second coder on a 20% subsample with Cohen's κ. There is none. Say who judged, using what written coding rules, and whether the judge saw the cohort label. If the judge was a model, state it. Add a second pass or at least a re-judgement of a subsample.
- The binary "correct" collapses three different questions: sense (weather versus other), literal versus figurative, and proper name. The reasons are stored but not tabulated. A three-way coding would show whether cohort 6's low precision comes from figurative use or from names and newspapers.
- Precision is used to qualify rates but never to adjust them. The plan's fall-back ("apply precision-adjusted frequencies as a sensitivity analysis if precision differs across cohorts") was not done. Given a precision gap of 0.85 against 0.55 across cohorts, a term-level adjusted rate, with propagated uncertainty, is the natural sensitivity analysis.

### M7. The post hoc reduced lexicon is circular and described more favourably than its numbers support
- The excluded forms were chosen from the same hand-checked sample, and the reduced storm family "was not re-checked by hand". The paper says so. The variant is therefore a fit to the validation sample, not a validation of it.
- "Weakens the fog rise" is overstated. Fog/mist words go from 0.73 to 1.53 under the full lexicon, a ratio of 2.1. Under the reduced lexicon they go from 0.65 to 1.26, a ratio of 1.9. The endpoints barely move. Only the Spearman ρ (0.77 to 0.54) changes, and with n = 6 that statistic is mostly rank noise. The reduced lexicon also leaves *fog* and *mist* untouched (it drops only *haze*, *hazy*), and these are the forms the hand check found figurative (smoke, steam, obscurity of mind). So it cannot address the very problem it is introduced for.
- The reduced variant changes two things at once: it removes forms and it removes capitalised mid-sentence hits. Report them separately.
- The variant also recomputed the cloud family. The paper reports the composite, fog and storm only, and omits cloud. Report all of them or say why not.
- The headline: storm words fall "steadily" at p = 0.005. That p is asymptotic (M1) and was chosen after the data were seen. It is flagged as a pattern worth testing, which is acceptable. It should not be in the abstract with a p-value attached.

### M8. Internal contradictions between text and numbers
- Section 5.2: "no single author reverses a cohort's position". For c1 the leave-one-author-out range is 9.42 to 12.29 around 11.09, and c2 and c3 sit at 10.81 and 10.94. Dropping the heaviest c1 author (30.9% of hits) moves c1 from the middle of the pack to the lowest. The range for c1 therefore does change the cohort's rank. Rewrite the sentence.
- Section 5.2: "excluding capitalised mid-sentence hits leaves the picture unchanged". The extended-lexicon ρ goes from 0.60 to 0.31, and the unambiguous-lexicon ρ from 0.71 to 0.77. State the changes, and note that with six points ρ is not informative anyway.
- Section 5.2 and contribution 2: the paper says "the same data yield a flat or a rising composite profile depending on which terms are retained". The "rising" variant (unambiguous, ρ = 0.71, p = 0.11, 4.43 to 6.57 to 5.60) is not distinguishable from flat. Four variants all fail to separate from flat, which shows no sensitivity of a distinguishable trend to the lexicon. It shows that the variants are noisy. The "unambiguous" lexicon also drops *wind*, *storm*, *sun* and *cloud*, the very words in the research question, so it measures a different construct (precipitation, snow, fog and mist, breeze). Do not present it as the same composite with less noise.
- Intro, finding 2 and the abstract call the tempest and snow patterns findings of the corpus, while Section 4.2 explains that of 15 profiles two reach 0.05 "by chance alone one is expected". The abstract's tone should follow Section 4.2: unresolved except as candidates.
- Section 4.4 infers that the collocates "are consistent with the high precision we find for the rain and wind families". Adjacent-pair PMI says nothing about precision. The paper says so one sentence later. Remove the inference. The "strongest pairs" are also not tied to a displayed table with counts and PMI, and the verbs "came, passed, tossed" are not among the listed pairs. Show the table.
- The data summary says the catalogue `download_count` is empty and "not used", yet Section 3.1 describes the frame as "sorted by download count". State the actual ordering (the catalogue's default popularity order) and that it cannot be recovered offline.

### M9. Specified analyses that are absent from the paper
The specification (items 2, 4, 5, 6) and plan list: per-novel (equal-weight) mean rates, whole-vocabulary keyness, slopes with length adjustment, and the dispersion table (min, p25, median, p75, max, SD, CV by cohort). The paper reports pooled rates only in text and gives author dispersion for the whole corpus plus top-author shares. Pooled rates over-weight long novels, and c1 and c2 novels are 1.5 to 2 times longer than c5. Show the equal-weight series next to the pooled series in the text, and show the length gradient (rate against log length) at least once.

## Should change

### S1. Tokenisation and the dictionary have undescribed recall and precision effects
- The regex keeps apostrophe words as single tokens, so *sun's*, *wind's*, *storm's*, *cloud's*, *fog's* are not matched by exact forms and are missed. Possessives and elisions (*rain'd*, *snow'd*) vary by era. State how many hits are lost, and add them, or test a lemma-style variant.
- Hyphenated compounds are split: *snow-storm* yields two hits (snow and storm), counting one event twice, while *snow-white*, *sun-bonnet*, *wind-mill* and *sun-dial* give false positives. Quantify, or count hyphenated compounds as a unit.
- The dictionary was written in the present from modern vocabulary. Forms that rose or fell by cohort (*blizzard*, *drizzle*, *downpour*, *chilly*, *tempest*, *gale*) may or may not be on the list. A fixed list has cohort-dependent recall. A tempest-to-storm substitution would appear as a decline in "tempest" with no change in weather. Report the full list of 90 forms in an appendix, and run the whole-vocabulary keyness to find weather words missing from it.
- The core lexicon is described as "23 forms from the focal terms in the research question and their plurals", but seven terms plus plurals gives at most 14, and the specification describes a different core (twelve headline words incl. *mist*, *thunder*, *frost*, *breeze*, *sunshine*). List the forms, and reconcile paper and specification.
- The capitalised mid-sentence rule is not defined in Section 3. How is sentence start detected? In all-caps headings and in eighteenth- and early-nineteenth-century capitalisation of nouns (*Storm*, *Wind*), the rule may drop genuine weather hits. Capitalised sentence-initial *Snow*/*Rain* surnames are retained. Give an audit count.
- "Weather" and "sky" are used interchangeably in the validation criterion. Time-of-day uses ("the sun was setting") and cosmic or mythic sun are different from weather. State and justify the boundary.

### S2. Multiplicity and forking paths
Fifteen profiles, plus about ten robustness variants and keyness for six cohorts, are all examined, and the paper adjusts for none. The paper acknowledges this once. Keep a single table listing every test performed with exact p, and apply a stated correction (Holm or Bonferroni) in the table. Under Bonferroni for 15 profiles nothing reported survives.

### S3. Cohort definition
The cohort index treats six cohorts as equally spaced, but realised birth years are 1770–1797 (28 years), 1803–1819, 1820–1838, 1840–1859, 1860–1878 and 1880–1890 (11 years). Use cohort mid-year, or state that the Spearman analysis is purely ordinal. The design range in the text (1800–1819) does not match the realised minimum (1803) in the caption. Say so once, as the instructions require. Author birth year is also a coarse proxy for writing date: a c4 author may publish from 1870 to 1930. The paper rightly says period and cohort cannot be separated. Avoid the word "generation" in the related-literature positioning as a benefit over year-based designs, since the design cannot show that cohorts do anything period does not.

### S4. Dialogue versus narration, and token denominators
Weather words occur in dialogue ("fine day") and in narration. Later novels have more dialogue. The denominator is all tokens, including front matter remnants and, in some texts, long non-narrative passages. A narration-only rate is a cheap and informative robustness check, and the plan listed it as optional.

### S5. Reproducibility
- Texts and their SHA-256 hashes are recorded and the texts are in data.db, which is good. Rerunning from the study folder should reproduce the counts. State this, and name the files: `data/sample_ids_v2.csv`, the extra catalogue CSVs, `draw_sample.py`, `draw_refill.py`, `build_data.py`, `run_estimation.py`. The Gutendex catalogue is a live, changing web service, and the frame cannot be rebuilt from it. Say that the saved tables are the frame.
- The same seed (20261014) is reused for the draw, the bootstrap and the validation sample. This is allowed, but record which generator (`random.Random` or `numpy.random.default_rng`) is used for each, and the Python, numpy and scipy versions. Report whether the 2,000 bootstrap draws are stable at a second seed (a Monte-Carlo error check on the interval endpoints).
- The sequence of manual steps (title-based exclusions, per-cohort "refill" from the next draw ranks, then "cut to the smallest n keeping the lowest draw ranks") should be a single scripted pipeline, or an appendix table that lets a reader redo each decision.

### S6. Presentation of method and results
- Section 3 should define every robustness variant (core, unambiguous, extended, capitalised, post hoc) before Section 5 uses them. The word "extended" is used for the full 90-form list in some places and appears undefined in others.
- The claim "every one of the 84 novels contains at least one weather word" is uninformative for books of 30,000 or more tokens. Replace it with the share of novels with a rate in the lower tail.
- Contribution 3 ("a validation template") is overstated for a single-coder sample of 24 items per family. Present it as a worked example.
- The related-literature claim "we found no study that" is correctly hedged. Several well-known works (Heuser and Le-Khac, Underwood, Moretti) are named as not citable but should be searched before the novelty statement stands.

## Sensitivity: what would change the conclusions
- Exact versus asymptotic p (M1) removes the one nominally significant family.
- Dropping the heaviest novel per cohort moves the composite trend from ρ = 0.60 to 0.09.
- Dropping the heaviest c1 author (30.9% of hits) changes c1's rank.
- Different title draws within c2 (Dickens's fog) and c5 (northern snow settings) could reverse the fog and snow comparisons. A resampling of novels within cohort from the frame (not only of authors from the drawn set) would show this directly. Run it with the remaining eligible books in c3 to c6, which have 18 to 20 eligible books, and report the spread of ρ across 1,000 re-draws of 14.
- A different cohort split (the plan's 10-year or 25-year bins, or halving c1) is listed in the plan but not run.

## What is sound
- Normalisation per 10,000 tokens, the tokeniser as recorded, and a documented token regex.
- Author-clustered resampling, as opposed to token-level intervals, and a seeded procedure.
- Keyness is paired with an effect size, a stricter G2 threshold (15.13), a minimum count and an explicit caveat about token independence.
- The validation is by hand, and the post hoc variant is labelled as post hoc.
- The language stays descriptive and non-causal throughout. The limitations section is honest about frame, cohort and period confounding and recall.

## Score

The measurements are traceable and reproducible in principle, and the writing is careful. The inferential claims (stability, snow rise, tempest marker, storm decline, lexicon sensitivity) are not yet supported at the strength they are stated, and the design leaves cohort confounded with genre and setting. These issues are fixable with analyses the data already allow.

OVERALL SCORE: 5/10
RECOMMENDATION: Major Revision
