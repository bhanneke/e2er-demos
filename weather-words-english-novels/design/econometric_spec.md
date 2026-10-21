# Analysis specification: weather vocabulary in English-language novels by author birth cohort

Descriptive text analysis. No causal claim, no regression, no publication year (the only time axis is the author's birth year as the Gutenberg catalogue records it; cohorts overlap in publication years, so period and cohort cannot be separated). Specification written from `corpus_design.json` before the analysis script was run.

## Data and preprocessing
- Source: data.db table `corpus` (one row per novel; `doc_id`, `text`, `author`, `author_birth_year`, `cohort` c1..c6), built by `build_data.py` and verified by the corpus check. 14 novels per cohort (84 in all, after translations and non-novels were excluded and all cohorts cut to the smallest n), at most two per author.
- Tokens: lower-cased NFC text, regex `[a-z]+(?:['’][a-z]+)?`, no lemmatisation, no wildcards. Counts use every token; stop words (`stopwords.txt`) only leave key-term lists and collocate lists.
- Dictionary: exact word forms exactly as frozen in `corpus_design.json` (`weather_all` and its six categories: precipitation, wind, storm, fog/mist, snow/ice, sun, cloud). "hail" and "storming" excluded.
- Core lexicon = the twelve headline words and inflections: rain, wind, storm, fog, snow, sun, cloud (plus mist, thunder, frost, breeze, sunshine) with their plural/verbal forms in the dictionary; extended lexicon = the full `weather_all` list.

## Estimands (all descriptive)
1. Per-cohort frequency per 10,000 tokens (and per million) for each headline term, each category and the aggregate; share of novels containing the term; number of authors using it.
2. Equal-weight rate: mean of per-novel rates (each novel counts once) per cohort.
3. Bootstrap intervals (seed 20261014, 2,000 draws): resample authors with replacement within cohort, take all of a drawn author's sampled novels (author-clustered, novel-level); recompute the pooled rate and the mean per-novel rate; 95% percentile interval.
4. Keyness of each cohort against the other five (Dunning G2, log ratio with 0.5 for zero counts, p from chi-squared 1 df), stop words excluded; threshold G2 > 15.13. Reported for all unigram types (top terms) and separately for the weather dictionary terms. Token-based keyness treats tokens as independent and overstates certainty; document-level dispersion is reported beside it.
5. Cohort trend: descriptive Spearman correlation between cohort index (1–6) and the cohort rate, and the OLS slope of the novel-level rate on the cohort index with author-clustered bootstrap CI, as description of monotonic drift only. Descriptive adjustment: the same slope with novel length (log tokens) as a covariate. No publication year anywhere.
6. Dispersion across authors: for each cohort and aggregate, the per-author rate distribution (min, p25, median, p75, max, SD, coefficient of variation) and the share of the cohort's hits contributed by its top author.
7. Collocates: adjacent (window 1) pairs containing fog, storm, rain, wind, snow, sun, cloud, count >= 5 (pooled corpus), PMI; stop-word partners removed from the displayed list.
8. Robustness: (a) core vs extended lexicon; (b) excluding polysemous hits — dropping forms flagged ambiguous (shower(s), thunder forms, icy, cloud forms, wind, sun, storm figurative) via an "unambiguous" sub-lexicon, and dropping capitalised surname hits Snow/Rain/Frost/Sunday-type tokens counted from the raw text; (c) leave-one-author-out range of the aggregate rate by cohort; (d) the aggregate trend with each cohort's single heaviest novel removed.
9. Post-hoc robustness (defined after the hand check, not in the design): the composite and the storm, fog and cloud families recomputed without the forms the validation judged unusable (thunder, thunders, thundered, thundering, hurricane, haze, hazy, clouded, cloudy, overcast) and without capitalised mid-sentence hits; cohort rates per 10,000 tokens, author-bootstrap intervals and the Spearman/slope summary as for the other variants. Stored as `robustness.post_hoc_reduced_lexicon`.

Figure sources: the corpus bar figures read `corpus.cohort_summary` in the results (cohort ids c1..c6 as categories); the cohort-trend figure plots the group ids c1..c6 as in `models.cohort_trend.outputs.series`, with birth-year ranges given in the axis title.

## Validation
`validation_sample.json`: seeded (20261014) stratified sample of up to 30 hits per dictionary analysis, passages cut verbatim from the corpus text, to be judged by the text validator; ambiguous forms are oversampled to be covered.

## Outputs
`estimation_results.json` (text results schema): corpus block, term_frequencies per cohort and `all`, models (keyness_c1..c6, collocation, dictionary per category, diachronic, robustness, dispersion), `limits.sampling_bias`. All numbers computed in `run_estimation.py`.
