# Replication package: The Vocabulary of Weather in English-Language Novels by Author Birth Cohort, 1770–1899

Paper ID: 4b4d6a45-97cd-4a7f-870b-173551822e97. Descriptive text analysis; no regression, no causal claim.

## 1. Data requirements

No data files are shipped. The script reads three files from the workspace root (the parent of `replication/`):

- `data.db`, table `corpus` (84 novels: `doc_id, text, title, author, author_birth_year, cohort, language, source_id`; 14 novels per cohort c1–c6). It is built from Project Gutenberg (catalogue via Gutendex, full texts from the Gutenberg mirror; loaded with `e2er-data gutenberg books|text`, accessed 2026-10-14/15) by `build_data.py`, `draw_sample.py` and `draw_refill.py`. Translations, non-English-literature bookshelves and non-novels were excluded and all cohorts cut to the smallest n.
- `corpus_design.json`: token pattern, frozen exact-form weather dictionary (`weather_all` and its categories), headline terms, collocate nodes.
- `stopwords.txt`: stop-word list (used only for keyness and collocate lists).

The SQL used to assemble the local tables is in `replication/data_queries.sql`; no Allium tables are used. Publication year, gender and nationality are neither looked up nor used.

## 2. Environment

Python 3.10+ with: `pandas`, `numpy`, `scipy`, `matplotlib` (`sqlite3` is in the standard library). Pin the versions you test with, for example:

```
pip install "pandas>=2.0" "numpy>=1.24" "scipy>=1.10" "matplotlib>=3.7"
```

I did not run the final script in this session (command execution was not permitted), so no version pins have been verified. The analysis code is a copy of `run_estimation.py`, which produced the paper's `estimation_results.json`.

## 3. Steps

1. Place `data.db`, `corpus_design.json` and `stopwords.txt` in the workspace root.
2. `python replication/estimation.py` (any working directory; paths resolve from the script).
3. The script tokenises (lower-cased NFC, regex `[a-z]+(?:['’][a-z]+)?`, no lemmatisation), counts the exact-form dictionary, computes cohort rates with author-clustered bootstrap intervals (seed 20261014, 2,000 draws), Spearman and OLS trend summaries, Dunning G² keyness, PMI collocates and the robustness variants, then writes tables and figures to `replication/output/`.
4. Optional check: compare `replication/output/estimation_results.json` with the workspace `estimation_results.json`; they should be identical.

Standard errors: none of the models is a regression with analytic SEs. Uncertainty is the author-clustered bootstrap fixed in `econometric_spec.md`. Keyness p-values are token-based and overstate certainty.

## 4. Output map

| Paper item | File in `replication/output/` |
|---|---|
| Table 1, corpus by cohort | `table1_corpus_summary.csv` |
| Table 2, composite and category rates | `table2_dictionary_rates_by_cohort.csv` |
| Table 3, headline-term rates | `table3_headline_terms_by_cohort.csv` |
| Table 4, trend summaries | `table4_cohort_trends.csv` |
| Table 5, author dispersion | `table5_author_dispersion.csv` |
| Table 6, keyness | `table6_keyness_c1..c6.csv`, `table6_keyness_weather_c1..c6.csv` |
| Table 7, collocates | `table7_collocates_pmi.csv` |
| Table 8, lexicon robustness (incl. post-hoc reduced lexicon, defined after the hand check) | `table8_robustness_lexicons.csv` |
| Table 9, leave-one-out | `table9_leave_one_out.csv` |
| Appendix, term frequencies | `tableA1_term_frequencies.csv` |
| Figures 1–2, corpus size and length | `fig_corpus_tokens_by_cohort.png`, `fig_corpus_median_length_by_cohort.png` |
| Figure 3, headline trends | `fig_cohort_trend.png` |
| Keyness figures | `fig_keyness_c*.png`, `fig_keyness_weather_c*.png` |
| All numbers (JSON) | `estimation_results.json` |
| Hand-check sample (seeded) | `validation_sample.json` |

Table numbers follow the order of the script's comments; check them against the final paper's table numbering. The hand-judged precision figures (`text_validation.json`) come from manual judgement of `validation_sample.json` and are not recomputed by the script.

## 5. Audit trail

`replication/audit_log.csv` logs the data queries run against `data.db`; `replication/data_queries.sql` lists the SQL. Random draws of the corpus are seeded (`draw_sample.py`, `draw_refill.py`); `np.random.seed(42)` is set and all resampling uses generators seeded with 20261014.
