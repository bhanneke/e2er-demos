# Literature review: Pleiades membership, Gaia distances and the cluster CMD

Work order: survey prior work on Pleiades membership and distance from Gaia (DR2 and DR3), membership selection by parallax and proper motion, and published CMD and main-sequence analyses. Report key references with verbatim sentences or values, citable from `literature.bib`. Flag published Pleiades distance and proper-motion values to check against.

Scanner: Literature Scanner specialist. Sources: `literature/corpus_evidence.md` (verbatim-verified claims from the local corpus), `literature/web_search.json` (discovery log), `literature.bib`.

## Coverage summary (read first)

- The local corpus contains **no verbatim claim on Pleiades membership, Gaia DR2/DR3 parallax or proper-motion selection, Pleiades distance values, or the Pleiades CMD/main sequence.** All 43 claims in `corpus_evidence.md` come from 17 papers that are the researcher's own bibliography (crypto markets, DeFi, NFTs, econometrics, graph experiments, coupon marketing) plus one AI-governance paper. None addresses the research question.
- The corpus search matched on the full research question. `web_search.json` kept 12 hits and dropped 20 on a content-word rule. Several dropped titles are relevant (see Section 3). The filter, not the corpus, is the reason they lack bib keys or quotes.
- Consequence: the Pleiades-specific references in `literature.bib` (Section 2) are present as **bibliographic entries only**. No verbatim sentence or value has been extracted from them. The paper must not quote or attribute any Pleiades number to them until the sentence is verified.
- No Gaia DR2/DR3 data-release paper is in `literature.bib`. Gaia EDR3 and DR1 appear only as dropped titles in the discovery log.

## 1. Key findings (verifiable from the corpus)

None of the corpus findings bears on Pleiades membership, distance, or CMD. They are listed only so the deliverable worker can see what was checked and rejected. Do not cite them for this paper.

- Governing hyperobjects (Potts, 2025): governance "must happen from within, using imperfect, partial models and localized feedback." Not relevant.
- Barbon, Ranaldo (2024): CEX triangular price deviations "below 5 bps"; Binance "below 3 basis points". Not relevant.
- Bhattacharya, Gong, Wattal (2023): poaching effectiveness rises as distance falls, home bias in search advertising. Not relevant.
- Spiekermann, Rothensee, Klafft (2020): redemption rates "5 times as high" at 10 m as at 800 m. Not relevant.
- Lyons, Viswanath-Natraj (2020): off-chain transactions "are not recorded". Not relevant.
- Corbet, Lucey, Urquhart (2019): Kodak's blockchain announcement share price rise "from over $3 per share to over $12 in less than one week". Not relevant.
- Li, Hai (arXiv 2607.23931): committee-size loss changes by domain (fact verification 0.245 to 0.194). Not relevant.

Attribution: all of the above come from the corpus extraction pass. None came from a worker that read the Pleiades literature.

## 2. Pleiades and Gaia-relevant references in literature.bib (bibliographic entries only, no verified quote)

Status column: **Quote: none** means no verbatim sentence was extracted. Do not cite a value from these papers until someone reads the source and records the exact sentence.

| Key | Year | Title (as in bib) | Relevance to the question | Quote status |
|---|---|---|---|---|
| `\cite{cantatgaudin2022milky}` | 2022 | Milky Way Star Clusters and Gaia: A Review of the Ongoing Revolution | Review of Gaia-based cluster membership and parameters; likely source for the DR2/DR3 membership context | Quote: none |
| `\cite{cantatgaudin2024how}` | 2024 | How Gaia sheds light on the Milky Way star cluster population | Gaia-based cluster census; membership method context | Quote: none |
| `\cite{chelli2016pseudomagnitude}` | 2016 | Pseudomagnitude distances: Application to the Pleiades cluster | Pleiades-specific distance determination (pre-DR2 era). Check any distance value against the source | Quote: none |
| `\cite{palmer2014an}` | 2014 | An updated maximum likelihood approach to open cluster distance determination | Method for cluster distance from parallaxes; relevant to the distance-distribution analysis | Quote: none |
| `\cite{leeuwen1985proper}` | 1985 | Proper Motion Studies of Stars in and Around Open Clusters | Classic proper-motion membership method; pre-Gaia baseline | Quote: none |
| `\cite{white2017beyond}` | 2017 | Beyond the Kepler/K2 bright limit: variability in the seven brightest members of the Pleiades | Pleiades membership of bright stars; useful for cross-checking the bright end of the CMD | Quote: none |
| `\cite{jackson2012why}` | 2012 | Why do some young cool stars show spot modulation while others do not? | Young-star context for the CMD; not a distance or membership source | Quote: none |
| `\cite{rees2016longlived}` | 2016 | Long-lived discs in T associations: Pre-main-sequence ages for low-mass stars | Pre-main-sequence context for the low-mass CMD; discuss only if the paper reaches that regime | Quote: none |
| `\cite{alexander2024the}` | 2024 | The frequency and mass-ratio distribution of binaries in clusters – III | Binary contamination of the main sequence; relevant to interpreting the CMD offset | Quote: none |
| `\cite{negueruela2025massive}` | 2025 | Massive Clusters and OB Associations as Output of Massive Star Formation in Gaia Era | Gaia-era cluster review; background only | Quote: none |
| `\cite{quintana2025quantifying}` | 2025 | Quantifying the scale of star formation across the Perseus spiral arm using young clusters around Cas OB5 | Gaia-era young cluster distances; background only | Quote: none |
| `\cite{pflammaltenburg2024asymmetry}` | 2024 | Asymmetry in the tidal tails of open star clusters from direct N-body integrations in Milgrom-law dynamics | Tidal-tail membership context; background only, probably not needed | Quote: none |

Methods sources already in the bib (use only if the paper describes the method): `\cite{freedman1981histogram}` (histogram bins for the parallax distribution), `\cite{hyndman1996sample}` (sample quantiles), `\cite{spearman1904proof}` (rank correlation), `\cite{little2019statistical}` (missing data), `\cite{wickham2014tidy}` (data organisation), `\cite{emerson1983statistical}` (descriptive statistics reporting). None of these is a Pleiades source.

## 3. Dropped by the discovery filter but relevant (no bib key yet)

These titles appeared in `web_search.json` and were removed by the content-word filter. They have **no bib key**, so they cannot be cited until added with `e2er-lit search`.

- "The initial conditions and initial mass functions of Alpha Persei, Pleiades and Praesepe" (two spellings, same title). Directly on the Pleiades initial mass function and cluster structure. Highest priority to add.
- "Gaia Early Data Release 3". Gaia EDR3 astrometry is the likely source for DR3 parallax and proper-motion selection. Add before citing any DR3 quality cut.
- "Gaia Data Release 1". DR1 background for the release history. Lower priority.
- "Weighing stars from birth to death: mass determination methods across the HRD". Background on mass from the HRD; relevant if the paper discusses main-sequence mass.
- "Inverse dynamical population synthesis". Possibly relevant to membership contamination models; uncertain.

## 4. Values to check against (flagged; not verified here)

The work order asks for published Pleiades distance and proper-motion values. **No such value was verified from a source in this pass.** The following are items the analysis should check against once the source sentence is in hand. None may be cited as stated below.

- Pleiades distance from Gaia DR2 and DR3 parallaxes. Compare the analysis's parallax-based distance with the published values in `\cite{cantatgaudin2022milky}`, `\cite{cantatgaudin2024how}`, and any distance from `\cite{chelli2016pseudomagnitude}`. Record the exact value, the release, and the table or section for each.
- Mean Pleiades proper motion (RA and Dec components). Compare the analysis's selected-member proper-motion centroid with the value in the membership papers. Record which release and which selection cuts the value uses.
- Parallax zero-point. Gaia DR2 and DR3 parallaxes carry a known zero-point offset. Any distance from a raw inverse parallax should be checked for whether the cited value applies the correction. No source for this is in the bib yet; add a Gaia parallax-zero-point reference first.
- Pleiades distance from pre-Gaia methods. `\cite{chelli2016pseudomagnitude}` and `\cite{palmer2014an}` give method-based distances. Their values predate Gaia DR2/DR3 and should not be compared directly with DR3 numbers without noting the release.

Important: from general knowledge, the Pleiades distance is commonly quoted near 135 pc and the proper motion near (+20, -45) mas/yr. These are **not** sourced in this pass, are not citable from the bib, and must be checked against a verified source before use.

## 5. Gaps and open questions

- **No Pleiades source quote.** The main gap. Read the membership and distance papers in Section 2 and record exact sentences and values, or the paper cannot support its literature section.
- **No Gaia data-release reference.** Add Gaia DR2 and DR3 papers (and EDR3, per Section 3) before describing the selection cuts.
- **No CMD or main-sequence literature.** No paper on the Pleiades CMD or main-sequence location appears in the corpus or the bib. This needs a targeted search.
- **Corpus is off-topic.** The 17 corpus papers are the researcher's bibliography and do not address astronomy. Their inclusion in the deliverable should be limited to the methods sources in Section 2, which are the only ones the template calls for.
- **Filter sensitivity.** The discovery filter dropped relevant titles (Section 3). Rerun discovery with terms such as "Pleiades", "initial mass function", and "Gaia" rather than the full question text.
- **Human decision.** Whether to keep the Gaia-review papers (`cantatgaudin2022milky`, `cantatgaudin2024how`) as the primary membership references, or to rely on an original DR2/DR3 membership paper, is for the researcher to decide.

## 6. Sources and references

Bib keys (all in `literature.bib`; use exactly as written):

- Pleiades and Gaia-relevant: `cantatgaudin2022milky`, `cantatgaudin2024how`, `chelli2016pseudomagnitude`, `palmer2014an`, `leeuwen1985proper`, `white2017beyond`, `jackson2012why`, `rees2016longlived`, `alexander2024the`, `negueruela2025massive`, `quintana2025quantifying`, `pflammaltenburg2024asymmetry`.
- Methods sources: `freedman1981histogram`, `hyndman1996sample`, `spearman1904proof`, `little2019statistical`, `wickham2014tidy`, `emerson1983statistical`.
- Corpus-derived (not relevant to this question; do not cite for it): all `e2er_source = {researcher}` entries in `literature.bib`.

Discovery log: `literature/web_search.json` (12 kept, 20 left out, rule in `src/modules/literature/discovery.py`, `is_relevant`).
Corpus evidence: `literature/corpus_evidence.md` (43 claims from 17 papers, all verbatim-checked against source text).
