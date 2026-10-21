# Literature Review: Weather Vocabulary in English Novels by Author-Birth Cohort

Scope note: only works with keys that resolve in literature.bib are cited. The literature search was thin (one to three queries per strand, OpenAlex only). Some well-known canonical works are NOT citable yet and are listed in "Uncited but expected" so the drafter can either run `e2er-lit search` for them or drop them. Nothing below is cited from memory.

## 1. Weather and climate in the Victorian novel (close-reading tradition)

- \cite{waugh2008talking}: "Talking about the weather: climate and the Victorian novel" (2008). Directly on topic, but a qualitative study. It offers no cohort-level frequency evidence. Summary is from the title only; the drafter should check the content before characterising it.
- \cite{laughlin2020fog}: "Fog, Coal, Capitalism: Dickens's Energy Atmospherics and the Anthropocene" (2020). Reads Dickensian fog as an index of coal-based energy regimes. This supports hypothesising a mid-Victorian peak of *fog*, *smoke* and *mist* for cohorts born around 1800-1840.
- \cite{jw2012the}: the child in the fog in *Bleak House* and *The Mill on the Floss* (2012). Fog as a motif in two single novels.
- \cite{lis2014containment}: legal and literary treatments of pollution in the Victorian fin de siecle (2014).
- \cite{hanlon2018london}: Hanlon (NBER, 2018), "London Fog: A Century of Pollution and Mortality, 1866-1965". This is the external, non-literary measure of fog and pollution intensity. It gives a historical series against which a fog-word series could be compared descriptively, with no causal claim.
- \cite{wood2024climate}, \cite{wood2025climate}: "Climate and the Little Ice Age" (handbook chapter, two editions). A background source for the climatic context. No source found that links Little Ice Age cooling to novelistic vocabulary. A search for a direct link returned only tangential items (e.g. \cite{oster2004witchcraft} on witchcraft and weather in Renaissance Europe).

## 2. Pathetic fallacy and Romantic vs. Victorian vs. modernist nature description

- Ruskin's term and its critique: \cite{morris1955ruskin} (1955), \cite{burns1984john} (1984), \cite{lichtenstein2020artistic} (2020), \cite{weinfield2025ruskin} (2025, on Ruskin, Wordsworth and Stevens). Ruskin coined the term in *Modern Painters* III (1856) to disparage the attribution of human feeling to nature. The term is therefore a Victorian critical category that also describes Romantic practice.
- Continuities and ruptures: \cite{hambly2020perpetual} (continuities between Romantic and modernist nature poetry), \cite{hopps2015the} (pathetic fallacy reconsidered), \cite{soper2023the} (legacy of the pathetic fallacy in "The Wanderer"), \cite{earnhardt2016the} (avian poetry, 1856-1945, a period that spans the Victorian-modernist divide), \cite{widger2017walking}.
- Limits: this literature is almost entirely about poetry and about individual authors, not about novels at corpus scale. Weather words in a bag-of-words design cannot detect pathetic fallacy itself. They can show whether weather terms are used more or less often by cohort. Interpretive claims about pathetic fallacy need a hand-validated sample, which the text_validation check already requires.

Working expectations drawn from this strand (stated as hypotheses, to be reported whichever way the data fall): (a) Romantic-era cohorts (born 1770-1799) show high frequencies of storm and cloud vocabulary; (b) mid-Victorian cohorts show elevated fog and smoke; (c) modernist cohorts (1880-1899) show a shift away from set-piece weather description. All three are untested expectations, not findings.

## 3. Computational literary studies and distant reading

- \cite{bories2022the}: "The Polite Revolution of Computational Literary Studies" (2022), a disciplinary account.
- \cite{krautter2023the}: scalable reading (Mueller's concept) in theory and practice (2023).
- Case studies show the genre of work: \cite{baghiu2020the} (Romanian nineteenth-century novel), \cite{jing2026a} (topic modelling of marriage discourse in Austen), \cite{ferguson2018literary}.
- Not found in the search and not citable: Moretti's *Graphs, Maps, Trees* and *Distant Reading*, Jockers's *Macroanalysis*, Underwood's work on gender and genre, Heuser and Le-Khac on abstract and concrete vocabulary in the novel, and the Stanford Literary Lab pamphlets. These are the closest prior work for a cohort-based design and should be searched before drafting.

## 4. Google Books / Ngram-style lexical change

- \cite{michel2010quantitative} (Science 2010) is the foundational culturomics paper; \cite{aiden2011culturomics} is a companion version.
- Applications: \cite{hills2019historical} (national subjective wellbeing from the Google Books corpus), \cite{juola2013using} (cultural complexity).
- Methodological caution: \cite{koplenig2015why} argues that quantitative analysis of diachronic corpora is misleading when the temporal aspect is ignored. This is directly relevant to our design. Ngram series index publication year, mix genres (fiction, science, travel, almanacs), and are sensitive to corpus composition. A cohort design that fixes genre (novels) and indexes author birth year differs in two ways: it holds genre constant, and it groups by generation rather than by calendar year.

## 5. Methods literature available for the study (method sources)

Cite only what the analysis uses.
- Keyness and frequency comparison: \cite{dunning1993accurate} (log-likelihood), \cite{rayson2000comparing} (frequency profiling), \cite{hardie2014log} (Log Ratio effect size), \cite{church1990word} (pointwise mutual information; collocation of weather words).
- Topic models: \cite{blei2003latent} (LDA), \cite{lee1999learning} (NMF), \cite{greene2014many} (topic-number stability).
- Framing: \cite{grimmer2013text}, \cite{gentzkow2019text} (text as data: validation, and the caution that topic outputs are not findings by themselves).

## 6. Gap and positioning for a cohort-based, author-birth-year design

Established in the search:
1. Close-reading work on weather in the Victorian novel exists (\cite{waugh2008talking}, \cite{laughlin2020fog}) but is selective, and it is organised by author or text.
2. Ngram-style work (\cite{michel2010quantitative}) measures lexical change by publication year across mixed genres, with known diachronic-composition problems (\cite{koplenig2015why}).
3. Pathetic-fallacy scholarship is about poetry and theory (\cite{hambly2020perpetual}, \cite{lichtenstein2020artistic}), not about corpus-scale prose.

Gap: none of the retrieved works compares weather vocabulary in novels across author-birth cohorts (1770-1799 to 1880-1899, six cohorts). Author-birth cohorts separate generational formation from the date of publication, and they reduce the confounding of period and age that affects year-of-publication series. The Romantic-to-modernist span lets one test the periodisation claims (Romantic, Victorian, modernist) against frequencies. Caveat: this gap claim rests on a limited search. It should be worded as "we found no study that..." and should be re-checked with further searches (distant-reading and Stanford Literary Lab work, stylometry, and nature or concrete-word studies of the novel).

Design implications for the drafter:
- Cohorts are author-based, so one author's novels cluster within a cohort. Variance estimates must account for author clustering, and results should be reported per author as well as pooled.
- Normalise by tokens, with document length and genre (e.g. gothic, sensation, domestic) as stated limits.
- Dictionary hits are polysemous (*sun* in a name, *storm* as metaphor, *fog* as figurative). The hand-checked sample is therefore essential. Note that the word-list definition is itself a design choice and should be fixed before the data are seen.
- Associations only: no causal link to the Little Ice Age or to coal smoke is claimed. Hanlon's series and climate reconstructions give context for interpretation, not identification.

## 7. Uncited but expected (not in literature.bib; search before use)
Moretti (distant reading), Jockers (Macroanalysis), Heuser and Le-Khac (Stanford Literary Lab), Underwood (distant horizons), Ruskin (*Modern Painters* III, primary text), Lamb's Little Ice Age climatology, Brimblecombe (*The Big Smoke*), Thorsheim (*Inventing Pollution*), Gale/Project Gutenberg/HathiTrust/Chadwyck-Healey corpus sources.
