# Literature Review: Global M>=5 earthquake counts 1976-2025 and Gutenberg-Richter b-value stability

Scope (researcher instruction, review_design): descriptive study. ComCat preferred magnitude; decade means of counts; Aki-Utsu MLE with bin correction (dM = 0.1); Shi & Bolt (1982) standard error; bootstrap intervals; Mc per decade by maximum curvature (+0.2) and goodness-of-fit (90/95%); Utsu pairwise decade test; Mw-only and shallow checks. Declustering, ETAS, Poisson simulation, b-positive and mb-to-Mw conversion are dropped, so no references for them are recorded.

## 0. Verification status (read first)
`e2er-lit search` returned only local-library items for the two queries that ran (Aki 1965, Utsu 1965); it then hit its 8-call search budget. The remaining references were recorded with `e2er-lit save --doi`, which resolves through OpenAlex/Crossref. Only items whose returned title matched the intended paper count as verified.

**Verified and recorded in literature.bib (citable):**
| Key | Reference | Role in the paper |
|---|---|---|
| `shi1982the` | Shi & Bolt 1982, BSSA, "The standard error of the magnitude-frequency b value", doi 10.1785/bssa0720051677 | Standard error of b: sigma_b = 2.30 b^2 sqrt(sum (M_i - mean M)^2 / (N(N-1))) |
| `wiemer2000minimum` | Wiemer & Wyss 2000, BSSA, "Minimum Magnitude of Completeness in Earthquake Catalogs: Examples from Alaska, the Western United States, and Japan", doi 10.1785/0119990114 | Mc estimation; goodness-of-fit (90/95%) and the link between Mc and b |
| `woessner2005assessing` | Woessner & Wiemer 2005, BSSA 95(2), "Assessing the Quality of Earthquake Catalogues: Estimating the Magnitude of Completeness and Its Uncertainty", doi 10.1785/0120040007 | Maximum curvature (+0.2 correction), GFT, bootstrap Mc uncertainty |
| `shearer2011global` | Shearer & Stark, PNAS, "Global risk of big earthquakes has not recently increased", doi 10.1073/pnas.1118525109 | Closest prior work on global rate stationarity |

Caveats on these entries (bib metadata is as returned by OpenAlex): (i) author fields list only one author for `woessner2005assessing` (Woessner) and `wiemer2000minimum` (Wiemer); the true author lists are Woessner & Wiemer and Wiemer & Wyss, and the bib should be corrected before the final reference list. (ii) `shearer2011global` carries year 2011 (online publication); the print issue is 2012 (PNAS 109(3)), the year the researcher gave. Use the key as is and state the year consistently. (iii) `shi1982the` has no volume or pages in the bib; the researcher's citation is BSSA 72(5) 1677-1687.

**Not resolved; NOT in literature.bib; do not cite (unverified):**
- Aki 1965 (Bull. Earthquake Res. Inst. Univ. Tokyo 43, 237-239). The local search returned nothing relevant. The paper must not cite it by key.
- Utsu 1965 (Geophys. Bull. Hokkaido Univ. 13, 99-103). Same outcome.
- Utsu 1992 or 1999 (b-value comparison test; the 1999 item is "Representation and analysis of the earthquake size distribution: a historical review and some new approaches", Pure Appl. Geophys. 155). Not searched before the budget ran out; no DOI was tried. Unverified.
- Michael 2011 (GRL, "Random variability explains apparent global clustering of large earthquakes"). The guessed DOI 10.1029/2011GL049351 resolved to an unrelated paper (`wong2011oxidation`, oxidation chemistry). **That entry is off-topic and should be removed from literature.bib; do not cite it.** Michael 2011 is unverified.

The paper may describe the Aki-Utsu estimator and Utsu's test in the text, but it cannot cite them until they are recorded. Action for the next run: `e2er-lit search` again with a fresh budget, or `e2er-lit save --doi` with a DOI confirmed from the publisher, for Aki 1965, Utsu 1965, Utsu 1999 and Michael 2011.

## 1. Tiers for this study

**Tier A: methods the study uses, verified** (cite in the methods section).
- b standard error: `shi1982the`. Per the researcher's instruction, b/sqrt(N) is Aki's formula and must be labelled as such if reported; Shi & Bolt's expression is the one used for sigma_b.
- Mc by maximum curvature (+0.2) and goodness-of-fit at 90/95%: `woessner2005assessing`, `wiemer2000minimum`. Mc is estimated from events down to M4.5. Woessner & Wiemer also supply the bootstrap logic for Mc uncertainty.
- Estimator and test: the Aki-Utsu MLE with bin correction and Utsu's two-sample comparison have no verified key (see Section 0). Describe them without citation, or wait until they are recorded.

**Tier A: positioning, verified.**
- `shearer2011global`: no statistically significant evidence that the rate of the largest global earthquakes has increased. Reported pairs of apparent clusters are consistent with random variability. This paper counts M>=5 events including aftershocks, so the claim differs in scope: the contribution is a descriptive audit of M>=5 counts and per-decade b, not a test on great earthquakes. Position against it carefully and do not claim the same result.

**Tier B: topical library items usable with care** (already in literature.bib; found on the web, abstracts not re-read here beyond titles).
- `kamer2014minimum`: minimum sample size for detecting a b-value. Relevant for the number of M>=Mc events per decade.
- `varty2021inference`: extreme-magnitude inference with a time-varying measurement process. Relevant to magnitude-type inhomogeneity in ComCat.
- `srivastava2021sundaarc`: regional increase of high-magnitude events in the Sunda arc since 2004. A regional counter-example; globally confounded by aftershock sequences.
- `wang2025estimating`, `li2025unifying`, `godano2023evaluating`: recent Mc and completeness work. Candidates for a sentence on alternative Mc methods; the study uses only maximum curvature and goodness-of-fit.
- `martinsson2018a`, `prabowo2026is`, `pisarenko2002rigorous`, `sornette1999general`: b-value estimation under incompleteness and deviations from G-R at large magnitudes. Peripheral; cite only if the discussion needs them.

**Tier C: off-topic or unrelated; do not cite.**
- `emerson1983statistical`, `jagla2013a`, `maslov2012derivation`, `serino2010gutenbergrichter`, `guglielmi2019global`, `guglielmi2021dependence` (named by the researcher as off-topic).
- Also not relevant to a descriptive study with these methods: `apostol2023timemagnitude`, `apostol2026mechanism`, `nandan2019magnitude` (triggering), `lippiello2024a`, `petrillo2023verifying` (b-positive line, dropped), `varotsos2012order`, `nanjo2021changes`, `zhou2026spatiotemporal` (regional or precursory b studies).
- `wong2011oxidation`: accidental off-topic entry created by a wrong DOI guess; remove from the bib.
- Template method keys `freedman1981histogram`, `hyndman1996sample`, `spearman1904proof`, `little2019statistical`, `wickham2014tidy`: use only where the analysis uses them (histogram bin width, quantiles, a rank correlation, missing data, tidy data). Cite none unless a corresponding step appears in the paper. None concerns seismology.

## 2. Data citation
USGS ComCat, doi 10.5066/F7MS3QZH, is cited for the data. It is not a literature.bib item here; the data_architect supplies it. Global CMT (Ekstrom, Nettles & Dziewonski 2012; Dziewonski et al. 1981) is not used as the data source (GCMT recorded as "unavailable"), so those references are not needed and remain unverified and unrecorded.

## 3. Points the paper should make (from the researcher's scope, no new citations needed)
- Counts include aftershocks; they are overdispersed. State that aftershocks are kept and that no declustering is done.
- Report the magnitude-type mix by decade, since ComCat gives one preferred magnitude per event. A change in the mix can shift counts at fixed M threshold.
- A difference between M>=5 and M>=5.5 counts is not a detection share.
- Incompleteness below Mc lowers the estimated b; it does not raise it.
- Report Utsu pairwise comparisons as computed, stating which decade pairs overlap and which do not.

## 4. Gaps and handoff
- Four of the eight requested references resolve and are in the bib. Aki 1965, Utsu 1965, Utsu 1992/1999 and Michael 2011 are unverified and stay out of the paper's citations.
- Fix author lists of `woessner2005assessing` and `wiemer2000minimum`, and add volume/pages to `shi1982the`, before the final reference list; remove `wong2011oxidation`.
- The paper_drafter should cite only: `shi1982the`, `woessner2005assessing`, `wiemer2000minimum`, `shearer2011global`, plus the Tier B items where used.
