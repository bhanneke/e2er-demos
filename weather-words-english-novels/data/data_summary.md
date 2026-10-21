# Data summary: weather vocabulary in English-language novels by author birth cohort

Data preparation only. No cohort comparison, keyness score or test statistic is computed here. Numbers trace to `summary_statistics.json`, `corpus_manifest.json` and `data.db`; the build is `build_data.py` (run with `e2er-run`), the exclusion step is `draw_refill.py`, the first seeded draw is `draw_sample.py`.

This is the corrected version: the researcher's instruction removed all translations, books on non-English-literature bookshelves and four non-novels, and cut every cohort to the smallest remaining n.

## Source and loaded tables (actual row counts in data.db)
Project Gutenberg (catalogue via Gutendex, texts from the Project Gutenberg mirror), loaded with `e2er-data gutenberg books|text`, accessed 2026-10-14/15. Texts are not restricted by copyright in the U.S.; the connector removed Gutenberg's header, footer and licence.

- Catalogue tables (popularity-sorted rows of a `--topic fiction`, `--languages en` search with an author-alive window per cohort; `copyright` and `download_count` are empty in the extract and are not used):
  - gutenberg_books_c1: 320 rows
  - gutenberg_books_c2: 320 rows
  - gutenberg_books_c3: 320 rows
  - gutenberg_books_c4: 320 rows
  - gutenberg_books_c5: 320 rows
  - gutenberg_books_c6: 320 rows
- Full-text tables (128 texts in all):
  - gutenberg_texts_c1: 20 rows
  - gutenberg_texts_c2: 19 rows
  - gutenberg_texts_c3: 20 rows
  - gutenberg_texts_c4: 20 rows
  - gutenberg_texts_c5: 20 rows
  - gutenberg_texts_c6: 20 rows
  - gutenberg_texts_c3_refill: 9 rows (one `e2er-data gutenberg text` call, ids 993, 6102, 750, 1684, 6113, 2374, 840, 5700, 693, the next unloaded ranks of the seeded draw order for c3; the texts already in data.db were not loaded again). Author fields are non-null for 8 of 9 rows: pg750 (The High History of the Holy Graal) is anonymous in the catalogue, has no birth year, and is not in `corpus` (0 rows). The dictionary entry declares `min_non_null` 0.85 for `authors`, `author_birth_year` and `author_death_year` of this table.
- Derived tables (raw tables not overwritten): `corpus` 84 rows, `corpus_token_counts` 84 rows, `weather_dictionary_hits` 2,311 rows (10,540 hits), `corpus_cohort_summary` 6 rows.
- Extra catalogue searches saved as CSV under `data/` (not in data.db) to widen thin cohorts: extra_c1_novel, extra_c2_novel/fiction/romance, extra_c6_fiction/novel/adventure. `data/sample_ids_v2.csv` holds the draw order with the exclusion reason per id.

## Sample construction (sample_flow in summary_statistics.json)
| step | n | dropped |
|---|---|---|
| catalogue rows read (frames + extra searches, with repeats) | 4,160 | 0 |
| unique ebook ids | 1,409 | 2,751 |
| language en; one catalogue person; birth year 1770-1899; plain text, not copyrighted; fiction-type subjects, non-novel forms and collections removed; title+author de-duplication | 632 | 777 |
| seeded draw (seed 20261014), at most 2 per author per cohort, first 20 per cohort | 120 | 512 |
| full texts loaded (six text tables + c3 refill, reserves included) | 128 | 0 |
| drop translations, non-English-literature bookshelves, non-novels (20 ids, listed in the JSON) | 108 | 20 |
| drop novels under 30,000 tokens after cleaning (ids 581, 693, 2695) | 105 | 3 |
| de-duplicate by text SHA-256; by normalised title + author | 105 | 0 |
| cut every cohort to the smallest n (14; lowest draw ranks kept) | 84 | 21 |
| final corpus | 84 | 0 |

The 20 exclusions: translations by catalogue-listed single authors (Dumas 1258, 2759, 1608; Gautier 1235; Muehlbach 4067; Gaboriau 1748, 547; Verne 1353, 83; Flaubert 1290); a book on a French-literature bookshelf (Reade, White Lies, 2472); the medieval-text translation 750 (High History of the Holy Graal); and non-novels (Sartor Resartus 1051, Our Village 2496, Nature and Human Nature 6112, A Dream of John Ball 357, Bulfinch 4926 and 4927, Criminal Sociology 477, Book of Pirates 973). The draw order also held further ids whose bookshelves name a non-English literature or whose subjects say "Translations into English"; they were never loaded and are flagged in `data/sample_ids_v2.csv`. Cohort pools after the exclusions: c1 15 eligible novels, c2 14 (pool exhausted: no further eligible ranks in the catalogue frames and extra CSVs), c3 18, c4 18, c5 20, c6 20; c2 therefore sets n = 14 per cohort.

Missing values: books without a recorded birth year or with several catalogue persons were dropped at the catalogue stage (never coded as zero). Title, author, birth year and language are complete in the final corpus.

## Corpus description (84 novels, 69 authors, 9,248,093 tokens, 78,344 types)
Tokenisation as in `corpus_design.json`: lower-case, regex `[a-z]+(?:['’][a-z]+)?`, no lemmatisation; stop words (`stopwords.txt`, scikit-learn, 318 words) leave term lists only, never token counts. Front matter cut by `build_data.py` (contents lists, illustration markers, "Produced by" lines, transcriber notes): 48,466 characters in total, at most 5,026 in one text. Mean novel length 110,096 tokens (median 87,639; range 30,914 to 320,232).

| cohort | birth years | novels | authors | tokens | median tokens/novel | weather-dictionary hits |
|---|---|---|---|---|---|---|
| c1 | 1770-1797 | 14 | 10 | 1,742,991 | 122,327 | 1,933 |
| c2 | 1803-1819 | 14 | 13 | 2,389,137 | 157,540.5 | 2,582 |
| c3 | 1820-1838 | 14 | 11 | 1,626,578 | 96,250.5 | 1,779 |
| c4 | 1840-1859 | 14 | 12 | 1,259,938 | 81,698 | 1,678 |
| c5 | 1860-1878 | 14 | 14 | 1,036,163 | 76,644 | 1,242 |
| c6 | 1880-1890 | 14 | 9 | 1,193,286 | 82,498.5 | 1,326 |

The hit counts are raw counts for data preparation; they are not normalised and not compared.

Time axis: the author's birth year only. No publication year was looked up or used (researcher's instruction), so the spread of publication years is not described. Cohorts overlap in publication years, and period and cohort cannot be separated. c6 birth years end in 1890 (no 1891-1899 author met the rules). Raw counts must be normalised per 10,000 tokens because cohort size and novel length differ.

Dictionary: 90 exact word forms (no wildcards) in seven categories (precipitation, wind, storm, fog and mist, snow and ice, sun, cloud), frozen in `corpus_design.json`; 86 distinct forms occur in the final corpus. 'hail' and 'storming' are excluded. Ambiguous forms the hand-checked sample must cover: shower(s), thunder forms, icy, cloud forms, wind (verb), sun (Sunday), storm (figurative), and the surnames Snow, Rain, Frost.

## Limits and flags
- Frame: the 320 most popular catalogue rows per cohort search, so it favours books popular on Gutenberg today; it is not a random draw of the cohort's novels. The 30,000-token rule is applied after loading; c2 ran out of eligible novels at 14, so all cohorts were cut to 14 (surplus novels are those with the highest draw rank). The design planned about 120 novels; the realised corpus is 84.
- Translations: all books with a translator in the catalogue record, on a non-English-literature bookshelf, or with "Translations into English" in the subjects were excluded. The extract has no translator field, so a translated book that the catalogue lists under one person with an English-language shelf could remain undetected; the exclusion list above came from reading titles, authors and shelves. No nationality coding was done, per instruction.
- Non-novel residue: the subject filter is loose; borderline forms remain (e.g. Phantastes, a fantasy romance; The Country of the Pointed Firs, linked sketches; Frankenstein as epistolary novel). Exclusions are listed above.
- Author clustering: authors have up to 2 novels per cohort (c6: 14 novels by 9 authors); document-level dispersion must be reported beside token counts.
- Gutenberg editions carry editors' prefaces in places; only detectable patterns were cut.
