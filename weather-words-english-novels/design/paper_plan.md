# Paper Plan: The Vocabulary of Weather in English-Language Novels by Author Birth Cohort, 1770–1899

Template: text analysis (descriptive; no causal claims). Keywords only, no JEL codes: *weather vocabulary; English-language novel; author cohorts; keyness; lexical diversity; Project Gutenberg; computational literary studies*.

## 1. Phenomenon and question

**Phenomenon.** Weather is a staple of the English novel, from the storm in a Gothic romance to the London fog in a Victorian city novel. Literary scholars often assert that weather writing changed over the nineteenth century, for example that fog and pathetic-fallacy storms became more prominent while sun and rain turned into everyday background. These claims are usually made from a few canonical texts. It is not established whether they show up as shifts in vocabulary across a broad set of novels, or whether they are artefacts of which books get discussed.

**Research question.** How did the vocabulary of weather (rain, wind, storm, fog, snow, sun, cloud and related words) vary across English-language novels by authors born in six cohorts, 1770–1799 to 1880–1899?

**Scope statement.** The paper describes patterns and associations in a bounded corpus. It makes no causal claims: it does not say that climate, urbanisation, literary movements or editorial fashion caused any change. Where interpretation is offered, it is flagged as hypothesis for future work.

**Why it matters.** (i) It tests literary-historical claims against corpus evidence. (ii) It shows how much a "trend" in a word family depends on measurement choices (normalisation, polysemy, cohort definition, length). (iii) Weather words are a clean, concrete lexical field, so the paper can serve as a worked case for cohort-based lexical comparison.

**Positioning (to be confirmed by the literature search, `e2er-lit search`).** Closest work to check before drafting: distant-reading studies of word-family trends in nineteenth-century fiction (e.g., Underwood's and Piper's work on literary change; Heuser and Le-Khac on abstract/concrete vocabulary in the nineteenth-century novel), the Google Books ngram-based literature on word-frequency change, and ecocritical/literary-history work on weather and climate in the novel. None of these citations is verified yet; the drafter must retrieve and cite them from search, not from memory. Expected contribution type: new descriptive fact plus measurement (a documented cohort profile of a lexical field, with polysemy-aware validation), not a new theory.

## 2. Data

**Source.** `gutenberg` (Project Gutenberg catalogue and full texts) is the only text source available. No other corpus may be planned.

**Unit and sampling frame.** One row per Gutenberg ebook that is (a) English-language, (b) classified as fiction/novel by Gutenberg subject headings or bookshelf (e.g., "Fiction", "Novel", bookshelves for adventure, historical, detective, etc.), (c) has one author with a recorded birth year 1770–1899, (d) length ≥ 30,000 words after boilerplate removal (excludes short stories and collections; the threshold is fixed before analysis and varied only in the robustness section).

**Required metadata and what Gutenberg holds.**
- Author birth year: from the Gutenberg catalogue (author birth/death years). Authors without one are dropped and counted.
- Author name, language, subjects/bookshelves, ebook id: from the catalogue.
- Author gender and nationality: **not reliably in the catalogue.** Plan: derive nationality from Gutenberg subject/author strings where present and otherwise code from a documented external reference (authority file such as VIAF/Wikidata, retrieved with `e2er-lit search` or documented URL), recorded with source for each author. Gender is coded at author level from the same external source; unresolved authors are labelled "unknown" and kept as a category. If external coding cannot be completed, gender and nationality analyses are dropped and reported as unavailable in `data_dictionary.json` (`unavailable`).
- **Publication year: not in the Gutenberg catalogue** (only the Gutenberg release date, which is irrelevant). First-publication year is a fact no listed source holds. Plan: do not fill it from memory. Either (i) obtain it from a cited bibliographic source for a validation subsample, or (ii) use the author's age at 20/30/40 (birth year + k) as a proxy and say so. The primary analysis uses birth cohort as the RQ requires; publication-period analysis is a secondary check restricted to the subsample with sourced years.

**Cohorts (author birth year, fixed before looking at any outcome).**
C1 1770–1799; C2 1800–1819; C3 1820–1839; C4 1840–1859; C5 1860–1879; C6 1880–1899. Widths are 30, 20, 20, 20, 20, 20 years; the unequal first window is a stated design choice from the RQ and is handled by reporting cohort sizes and by a robustness split of C1 into 1770–1784 / 1785–1799.

**Deduplication and cleaning.** Remove Gutenberg headers/footers/licence text and front matter (prefaces, editor notes, tables of contents where detectable); collapse multiple editions/volumes of one title to one work (prefer the single-volume complete text); merge multi-part ebooks for the same novel; drop translations (authors writing in another language) and anthologies; hash each cleaned text (SHA-256) and record counts at every filter step (the corpus check requires sources, hashes and counts).

**Sample-size target and caps.** Expected usable corpus: several hundred to a couple of thousand novels, unevenly distributed across cohorts (Gutenberg is thin for C6 because of copyright, and skewed to canonical and popular authors). To stop prolific authors dominating, cap at N novels per author (default 5, random with fixed seed; sensitivity: cap 1, cap 10, no cap) and report author counts per cohort alongside novel counts.

**Representativeness caveat (to be stated in the paper).** Gutenberg is a convenience sample driven by volunteer digitisation and copyright, not a sample of all published novels. Findings describe this corpus; generalisation is limited.

## 3. Preprocessing

1. Normalise Unicode, lowercase, convert long-s and ligature variants, handle hyphenation across line breaks and dialect spellings listed in the lexicon.
2. Tokenise on word characters with apostrophes; keep original-case token alongside lowercase (needed for the proper-noun checks below).
3. Token count N_d per novel = number of alphabetic tokens after boilerplate removal. All frequencies use N_d as denominator.
4. No stemming for the primary analysis (stems conflate senses); lexicon lists explicit inflections. Lemma-based matching (spaCy or equivalent) is the robustness check.
5. Record the tokenizer, lexicon version and random seeds; fix them in a config file for replication.

## 4. Weather lexicon

Built before inspecting cohort outcomes; frozen and versioned. Each entry lists headword plus inflections/variants (matching on whole tokens).

**Core set (primary analysis; high precision, unambiguous weather reference in most contexts).**
- rain: rain, rains, rained, raining, rainy, raindrop(s), rainfall, rainstorm
- wind: wind (noun, see polysemy), winds, windy, gale(s), breeze(s), blast(s) only in extended
- storm: storm, storms, stormy, thunder, thunderstorm, lightning
- fog: fog, fogs, foggy, mist, mists, misty
- snow: snow, snows, snowed, snowing, snowy, snowfall, snowflake(s), sleet, hail (extended, polysemous)
- sun: sun, suns, sunny, sunshine, sunlight, sunbeam(s), sunset/sunrise (extended)
- cloud: cloud, clouds, clouded, cloudy, clouding, overcast

**Extended set (secondary analysis; broader or more ambiguous).** weather, climate, tempest, squall, drizzle, shower(s), downpour, deluge, frost, frosty, ice, icy, freezing, hail, haze, hazy, gloom/gloomy (ambiguous: mood), heat, hot, cold, chill, warm, wet, damp, dew, rainbow, wind-related (blow, blew, blowing, blast, gust, draught).

**Subfamilies for reporting.** Precipitation (rain, snow, hail, sleet, drizzle), air/wind, storm/lightning, obscuring (fog, mist, haze, cloud), light/sun, temperature (extended only).

**Why a core/extended split.** Core terms support the headline results; extended terms add coverage at the cost of precision. Every headline result must be shown for both, so conclusions cannot hinge on lexicon breadth.

**Polysemy and false-positive handling (documented, then validated).**
- *Sun*: Sun as proper name or surname (e.g., newspaper "The Sun", "Sun Yat-sen", "Sunday" excluded by whole-token matching); "sun" in compounds ("sunday" not matched); capitalised mid-sentence "Sun" is excluded unless followed by "rose/set/shone" (rule list in appendix).
- *Storm*: figurative uses ("storm of applause", "storm of passion", "take by storm"); military "storm the castle" (verb). Primary analysis counts all tokens (the lexical field), with validation estimating the literal/figurative/other share per cohort; secondary analysis applies a rule-based filter.
- *Wind*: verb "wind" (wind a watch, winding road), "wound", "windows" excluded by whole-token matching; "wind up". Disambiguate by POS tag (noun vs verb) in the lemma-based robustness check.
- *Cloud*: figurative ("a cloud of dust/smoke", "cloud of suspicion").
- *Snow, Frost, Hail, Mist, Gale, Rains*: surnames and place names (Snow, Frost, Rains, Gale, Hale/Hail as greeting "hail!"), capitalised-token rule plus manual check.
- *Heat/cold/warm* (extended): mostly non-weather (emotional warmth, "catch cold"); kept only in the extended set and always reported separately.
- *Sunday, Sunderland, snowdon, windsor, Stormont*: handled by whole-token matching and a stop-list.

Hand validation (text_validation check): stratified random sample of dictionary hits, by term × cohort (target ≥ 40 hits per core family, ≥ 20 per cohort within each, or all hits if fewer), coded for (a) literal weather, (b) figurative, (c) proper name, (d) other. Report precision by family and cohort; if precision differs across cohorts, apply precision-adjusted frequencies as a sensitivity analysis. Sample, labels and coding rules are saved so another coder can repeat it; a second coder codes a 20% subsample and Cohen's κ is reported.

## 5. Outcome measures

All computed at the novel level, then aggregated to cohort (novel-weighted and author-weighted).

1. **Frequency per million words.** f_{d,t} = 10^6 × count of term t (or family) in novel d / N_d. Cohort estimate: (a) pooled (sum of counts / sum of tokens × 10^6) and (b) mean and median of novel-level rates, with bootstrap confidence intervals resampling authors (cluster bootstrap, 2,000 draws, seed fixed). Reported for the full core set, each family, and each headword.
2. **Share of novels using each term.** Proportion of novels in cohort with ≥ 1 token (and, as a robustness, ≥ 3 tokens, because ≥ 1 depends on length). Wilson intervals, clustered by author in bootstrap.
3. **Keyness by cohort.** For each cohort versus all other cohorts combined (and adjacent-cohort contrasts C_k vs C_{k+1}): log-likelihood (G²) and log-ratio effect size (Hardie 2014) on pooled counts for weather terms, plus an author-clustered check using per-author rates (Wilcoxon / permutation over authors), since pooled G² overstates significance when words cluster within a few books. Keyness is run (i) restricted to the weather lexicon (which weather words characterise each cohort), and (ii) over the whole vocabulary (are weather words among the most key words at all, compared with other lexical fields; a negative-control field such as kinship or colour terms is reported alongside). Multiple-testing: Benjamini–Hochberg across terms, with the number of terms tested stated.
4. **Lexical diversity of weather vocabulary.** Within the weather lexicon only: number of distinct weather types (richness), Shannon entropy and inverse Simpson over weather-term counts per novel, computed on a **fixed-size resample of weather tokens** (or rarefied at k = 20 weather tokens per novel; novels with fewer are excluded from this measure and counted) to avoid length/count dependence. Also report type-token ratio of the weather vocabulary per 100,000 tokens (standardised-window approach, not raw TTR) and, at cohort level, the pooled distribution (Zipf-style rank frequency) of weather terms. Whole-text lexical diversity (MTLD or moving-average TTR) is a control, not an outcome.

**Descriptive display.** Cohort-by-term heatmap of per-million rates; line/point plots of cohort means with intervals; ranked keyness tables; distribution plots (violin or ECDF) of novel-level rates to show spread, since cohort means hide heavy tails.

## 6. Descriptive questions (fixed before the analysis; no hypotheses about direction are tested)

- **Q1 Overall level.** Does total core-weather frequency per million words differ across the six cohorts, and how large is the cohort difference relative to the spread among novels and among authors within a cohort?
- **Q2 Composition.** Which families (precipitation, wind, storm, fog/obscuring, snow, sun/light, cloud) gain or lose share of the weather vocabulary across cohorts? Is the pattern monotonic or does it peak in a middle cohort?
- **Q3 Breadth of use.** Does the share of novels using each term change across cohorts, separately from how often it is used when present (extensive vs intensive margin)?
- **Q4 Distinctive terms.** Which weather words are key for each cohort relative to the others, and do keyness patterns survive author-clustered testing and polysemy filters?
- **Q5 Diversity.** Is the weather vocabulary of later cohorts more or less varied (richness, entropy) than that of earlier cohorts, holding the number of weather tokens fixed?
- **Q6 Heterogeneity.** Do the cohort patterns look similar within subgroups (author gender, British vs American authors, genre labels) or are they driven by one subgroup or a few prolific authors?
- **Q7 Reverse-insight check.** Which of the cohort patterns are absent for the negative-control lexical field (e.g., kinship terms) and for the extended temperature words? An absence helps show whether any cohort contrast is specific to weather or part of a general vocabulary shift.

Associations are summarised with cohort contrasts and, if the plan calls for it, a descriptive count-model adjustment (negative binomial with log(N_d) offset, author-clustered standard errors) used only to show whether cohort differences persist after conditioning on the confounders below; coefficients are described as conditional associations. The econometrics/analysis specialist writes results in the text results schema (`estimation_results.json`); no regression is estimated beyond this descriptive adjustment.

## 7. Confounds and how each is handled

| Confound | Concern | Handling |
|---|---|---|
| Novel length | Longer novels have more opportunities for weather tokens; share-of-novels-using is mechanically length-dependent; diversity grows with token count | Per-million normalisation; length ≥ 30k filter; share-using at ≥ 1 and ≥ 3 tokens; diversity measured on fixed-size weather-token resample; length stratified (tercile) results; length as covariate in the adjusted model; report length by cohort |
| Genre | Gothic, adventure, sea, Western, detective, domestic fiction differ in weather use; cohorts may differ in genre mix | Use Gutenberg subject/bookshelf labels to build coarse genre flags (multi-label); report genre mix by cohort; within-genre cohort comparison where cells are large enough; genre fixed effects in the descriptive adjusted model; admit that labels are crude |
| Publication year vs birth cohort | Birth cohort is not the period of writing; an 1840–1859 author may publish 1870–1910; period and cohort are not separable | Report birth cohort as primary (as in the RQ); the author's typical writing window is shown (birth + 30 ± 10 as a proxy, with sourced first-publication years for a subsample); cohorts overlap in publication years, so period effects and cohort effects are not distinguished and the paper says so; subsample comparison by publication decade |
| Author gender | Gender composition differs by cohort and may associate with vocabulary | Code gender with documented source; report share by cohort; gender-stratified results; gender in adjusted model; unknown category retained |
| Nationality / dialect | British, Irish, American, Canadian, Australian authors; weather and spelling conventions differ (e.g., "snow" in North American settings) | Code nationality; stratify British vs American at least; spelling variants in lexicon; setting is not coded (limitation) |
| Polysemy and proper names | Sun in names, storm as metaphor, wind as verb, cloud/clouded figuratively | Rules plus hand validation per Section 4; precision by cohort; sensitivity to filtered and unfiltered counts |
| Author dominance / clustering | Prolific authors (e.g., many novels per author) drive cohort means | Cap per author; author-weighted cohort means; cluster bootstrap by author; leave-one-author-out influence for top contributors |
| Corpus composition / digitisation | OCR errors, edition differences, spelling modernisation, abridgements; Gutenberg coverage uneven by cohort | Duplicate/edition control; OCR quality proxy (share of tokens in a reference word list) by cohort; report coverage; restrict to high-quality subsample as robustness |
| Dialogue vs narration | Weather words in dialogue ("fine day") vs description | Optional: quotation-mark heuristics to split dialogue/narration; reported as secondary |
| Small cohorts | C1 and C6 may be thin | Report N; wide intervals; no cohort comparison reported without a minimum of 30 authors (stated threshold; otherwise flagged) |

## 8. Robustness and reported specifications

All specifications run are reported: core vs extended lexicon; surface forms vs lemmas; filtered vs unfiltered polysemy; per-author caps (1, 5, 10, none); length thresholds (15k, 30k, 60k); alternative cohort splits (C1 halved; 10-year bins; 25-year bins); novel-weighted vs author-weighted; with and without genre labelled as adventure/historical/Gothic; negative-control lexical fields. A short "specification table" in the appendix lists every variant and its headline numbers.

## 9. Pipeline handoff

- **data_architect / data_analyst** (before analysis): build the `gutenberg` catalogue table (ebook id, title, author, birth year, language, subjects, bookshelves), the cleaned-text corpus with SHA-256 hashes and step-by-step counts; code gender and nationality from a cited external source or declare them `unavailable` in `data_dictionary.json`; publication year likewise only from a cited source, never from memory. Gutenberg birth years are the only guaranteed cohort variable.
- **Corpus design / corpus checks** (stop-gate): filters, cohort definitions, deduplication rules and hashes must match this plan; cohort counts reported.
- **econometrics_specialist (analysis)**: compute measures in Section 5 and write `estimation_results.json` in the text results schema; implement lexicon v1 exactly as in Section 4; cluster bootstraps with fixed seeds.
- **text_results check**: counts, keyness and topics recomputed independently.
- **text_validator**: hand-check a stratified sample of dictionary hits per Section 4, report precision by family and cohort, κ for the second coder.
- **paper_drafter**: only after the checks pass. Write cautiously: "cohort X shows higher frequency of Y", not "caused". Present limitations: convenience corpus, unobserved publication dates, crude genre labels, polysemy.
- No identification strategist or theory specialist is needed.

## 10. Risks and fall-backs

- *Too few authors in C1 or C6*: merge or flag; report as exploratory.
- *Gender/nationality coding incomplete*: drop the heterogeneity question Q6 to the available subgroups and state why.
- *Publication years unavailable*: rely on birth cohort alone; describe the cohort/period confound as an unresolved limitation.
- *Polysemy precision low for a term (< 70%)*: move it to the extended set or report only the filtered version.
- *Null differences*: a finding of stable weather vocabulary across cohorts is reported as a result (reverse insight: the weather lexicon appears stable while other fields shift).

## 11. Target outlet

Digital humanities / computational literary studies journals (e.g., Journal of Cultural Analytics, Digital Scholarship in the Humanities, Corpora). Not an economics paper; no JEL classification.
