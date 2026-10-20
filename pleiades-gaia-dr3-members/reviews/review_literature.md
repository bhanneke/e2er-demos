# Literature Review: Which Stars within 3 Degrees of the Pleiades Centre Share Its Astrometry?

Reviewer role: literature_reviewer (referee simulation, descriptive data study)
Scope: the draft, the literature scan (`literature/` coverage summary, Section 2 bib table), the data dictionary citations, and the paper plan's reference list. The membership, grid and CMD numbers were not re-derived; they are taken from `estimation_results.json` as quoted in the econometric specification.

## DIMENSION SCORES

- Contribution: 5/10
- Identification: 6/10 (the study makes no causal claim; scored on whether the membership and distance claims are supported by the stated procedure and its sensitivity)
- Empirics: 7/10
- Writing: 7/10
- Literature: 3/10

## MAJOR CONCERNS

1. **The paper has no verified Pleiades literature, so its central comparison cannot be made.** The scan found no verbatim claim on Pleiades membership, Gaia parallax selection, Pleiades distance or the Pleiades main sequence. The 43 corpus claims come from unrelated papers (crypto markets, DeFi, AI governance). The Pleiades-specific entries in `literature.bib` (`cantatgaudin2022milky`, `cantatgaudin2024how`, `chelli2016pseudomagnitude`, `palmer2014an`) are bibliographic entries only, with no quote and no value. The draft's Discussion sets up the distance benchmark ("the natural benchmarks") and then says the comparison "requires the verified figures ... which have not been extracted for this paper." The headline claim of a 135.7 pc distance is therefore reported with no reference point. The fix is to extract, with exact sentences, the Pleiades distance and proper-motion values from at least one Gaia DR2 or DR3 membership or distance paper (for example the Gaia DR2 HR-diagram paper and a Gaia-based Pleiades membership study, both still to be added), record release, table and selection cuts, and then state where 135.7 pc and the proper-motion centre (19.87, -45.42) mas/yr sit against them. Until then, the Abstract's and Conclusion's wording about the distance should be limited to "parallax-based, uncorrected".

2. **The draft cites Gaia release papers that the scan says are absent from the bibliography.** `paper` cites `\citep{GaiaMission_Prusti2016,GaiaDR3_Vallenari2023}` in the Introduction, and the data dictionary states that the load adds these keys. The literature scan states that "No Gaia DR2/DR3 data-release paper is in `literature.bib`" and lists Gaia EDR3 and DR1 only as dropped titles. These two statements cannot both hold for the same bibliography. The researcher must confirm that both keys resolve to verified entries (Gaia Collaboration, Prusti et al. 2016, A&A 595, A1; Gaia Collaboration, Vallenari et al. 2023, A&A 674, A1) before the draft is compiled. The Lindegren et al. (2021) zero-point reference is discussed in the Data section and the Limitations but has no citation key at all. The DR2 and EDR3 papers named in the plan, and the RUWE reference (Lindegren et al. 2018), are not cited in the text, although the RUWE < 1.4 cut relies on them.

3. **Several uncited factual claims carry the paper's framing.** These are stated as fact with no citation:
   - "The Pleiades is one of the nearest open clusters and a familiar reference for the distance scale and the main sequence of young stars" (Introduction).
   - "Gaia ... gives parallaxes and proper motions for most of the bright stars in such clusters" (Introduction).
   - "the cluster's brightest stars, the named B stars several magnitudes brighter" (Results, Limitations). This is the basis of the bright-end gap that the paper reports as a limitation. It needs a source for the spectral types and magnitudes of the named B stars, or the wording must be made to rely only on the extract's own data.
   - "The approximate correction ... is negative at these magnitudes" and "the Gaia zero-point, which is negative at these magnitudes" (Limitations). This needs the zero-point citation in concern 2.
   - "a field star with a similar parallax and proper motion can be included" and the contamination statement. This is a generic claim and is acceptable, but it should cite the membership-method literature (`leeuwen1985proper` or a Gaia-era membership paper) if kept.
   Each of these should either carry a verified citation or be reworded as a statement about this extract.

4. **Citations attached to methods do not always support the sentence they follow.** `freedman1981histogram` is cited for "Histograms use bins of equal width, 0.25 mas in parallax and 5 pc in distance ... so that the counts in the bins sum to the sample size." Freedman and Diaconis (1981) is a rule for choosing bin width from the data, not a source for fixed-width bins or for the sum-to-n property. Replace it with a source that supports the stated choice, or cite it only for the rule the paper does not follow, and say why a fixed width is used. `wickham2014tidy` supports the "one observation per row" principle as cited; that is fine. `hyndman1996sample` supports the type-7 quantile statement; that is fine.

5. **The bibliography is padded with entries the text does not use or that are off-topic.** `palmer2014an`, `leeuwen1985proper`, `white2017beyond`, `jackson2012why`, `rees2016longlived`, `alexander2024the`, `negueruela2025massive`, `quintana2025quantifying`, `pflammaltenburg2024asymmetry`, `spearman1904proof` and `emerson1983statistical` are not cited in the draft, and most are of doubtful relevance to a Pleiades membership and distance description (spot modulation, tidal tails, Perseus spiral arm). The paper should either cite these where a specific claim needs them, after verification, or remove them from `literature.bib`. A reviewer reading the bibliography would see a list that does not match the argument. The `\bibliography` output prints only cited entries, so the printed list is not affected, but the file is misleading for replication.

6. **The "Future research" proposal and the missing reference to independent membership checks.** The paper proposes testing membership against an isochrone or spectroscopic criterion, but no Gaia-era membership comparison is cited to show what such a test has found elsewhere. Adding one verified membership comparison (for example a Gaia-based membership catalogue for the Pleiades, with its selection cuts) would both support the membership claim and give the reader a benchmark for the 1,112 count. The 1,112 count is currently compared only with the paper's own grid.

## MINOR CONCERNS

1. The Abstract says "The distance is $1000/\varpi$ from the uncorrected parallax" and cites the estimation results. Add the citation for the parallax-to-distance inversion (Bailer-Jones 2015 or equivalent) only if the paper goes on to discuss its bias, which it does not; otherwise the sentence is fine as it stands.

2. In the Introduction, the paper cites `\citep{cantatgaudin2022milky,cantatgaudin2024how}` for "Gaia-based censuses now cover much of the open-cluster population." These are reviews of the same programme. Check each title against its abstract before the sentence is retained, and cite the specific census used.

3. The Discussion cites `\citep{chelli2016pseudomagnitude}` for "Pleiades distances determined before Gaia DR2." The plan describes this as a method-based pre-Gaia distance. Record its distance value and its own zero-point treatment, since its number will be read against 135.7 pc.

4. The planning document lists Lodieu et al. (2019), Melis et al. (2014) and Gaia Collaboration, Babusiaux et al. (2018) as candidate references. None is in `literature.bib` and none has a verified quote. They should be added and checked, or dropped from the plan. The reviewer has not verified any of these titles or values, and they must not be cited from memory.

5. The paper's own statement that "the grid is reported in full" is well supported by the body and the table. No change is needed.

6. Key terms "RUWE", "five- or six-parameter solutions" and "Vega magnitudes" are used without a citation for their definitions. A single Gaia DR3 documentation citation would cover all three.

7. The literature scan notes that the discovery filter removed the title "The initial conditions and initial mass functions of Alpha Persei, Pleiades and Praesepe", which is directly relevant to the Pleiades main sequence and cluster structure. Add it to the bibliography after discovery is re-run with "Pleiades" and "Gaia" as search terms.

## POSITIVE ASPECTS

1. The paper is honest about its literature gap. It says that the distance comparison is left to a verified source and does not state an agreement or disagreement with published values. This is the correct stance for a descriptive study with no verified benchmark, and it is stated in the Abstract, the Discussion and the Conclusion.

2. The data source, the pre-filter and the archive limits are documented with the ADQL text, the row count, the retrieval date and the Gaia licence and acknowledgement. The citation of the Gaia data licence and the ESA/DPAC credit line in the data dictionary follows the terms the archive states.

3. The reading rules were fixed before the results, and the paper reports the full 48-row cross (913 to 1,184 members, median 1,055.5) rather than selecting the base row. This makes the membership count's sensitivity transparent.

4. The paper distinguishes clearly between the parallax-based distance, the star-to-star spread and any cluster depth, and it states that the standard error of 0.007 mas is for the mean parallax.

5. The bright-end gap (brightest member at G = 5.20, with five brighter extract stars all failing the RUWE cut) is reported as an observed gap, without a claimed cause. This is an appropriate reading of the data.

## Closing note on the literature scope

The paper's literature section cannot support its claims about Pleiades distance, proper motion or the main sequence until the sources in concern 1 and concern 2 are verified and their values recorded with exact sentences. The methodological citations (Hyndman, Wickham, Little) are usable as they stand, subject to concern 4 on the histogram reference.

OVERALL SCORE: 5.7/10
RECOMMENDATION: Major Revision
