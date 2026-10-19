# Literature Review Referee Report

Paper: Yearly number of M>=5 earthquakes and stability of the Gutenberg-Richter b-value, 1976-2025 (USGS ComCat)

Basis: the draft and the supporting literature review, as supplied. I did not run external searches.

## Assessment of literature coverage

The draft cites eleven works: ComCat, Shearer & Stark (as `shearer2011global`), Wiemer & Wyss, Woessner & Wiemer, Shi & Bolt, Kamer & Hiemer, Varty et al., Srivastava et al., Wang et al., Godano et al., plus two template references (Spearman, Hyndman & Fan). The methods are described correctly, and the draft is candid about their limits. The coverage is thin for a paper whose core claims concern the b-value and catalogue homogeneity, and it is thin in the places where the paper's conclusions are most exposed.

## MAJOR CONCERNS

1. **The estimator and test are used but not attributed.** The paper says "due to Aki and Utsu", "Aki's b/sqrt(N)" and "Utsu's likelihood-ratio test", and the results hinge on that test. None of these has a citation. The pipeline's own note explains that Aki 1965, Utsu 1965 and Utsu 1992/1999 could not be resolved, so this is a tooling failure rather than a choice. A referee will still read it as missing core references.
   - Fix: verify the DOIs by hand and add Aki (1965), Utsu (1965, 1999), and Gutenberg & Richter (1944).
   - Also add Bender (1983) or Marzocchi & Sandri (2003) for the binned-magnitude MLE. The plan named Marzocchi & Sandri, but the paper drops it.
   - Until these are added, the "Utsu test" cannot be reproduced from the text. The paper also never states which form of the test it implements (Utsu 1992 versus 1999).

2. **The central problem in the paper is magnitude homogeneity and Mc estimation in heterogeneous catalogues, and that literature is missing.** This is the most consequential gap. The paper's own finding is that b varies with magnitude type. The literature that bears on this is absent:
   - mb-to-Mw and Ms-to-Mw conversion and saturation (for example Scordilis 2006; Di Giacomo et al. 2015, the ISC-GEM work; Storchak et al.). These would explain why 4.7-5.2 events move between scales.
   - Mc estimators beyond maximum curvature and goodness-of-fit, namely Cao & Gao (2002), Mignan & Woessner (2012), and Clauset-type KS-based Mc. The paper cites only Wang et al. (2025) and Godano et al. (2023) for these.
   - Magnitude binning, rounding and heaping effects on b (Marzocchi & Sandri 2003; Tinti & Mulargia 1987). The draft itself reports 909 two-decimal magnitudes without engaging this work.
   - Estimating Mc and b jointly: Mc uncertainty feeds into b uncertainty (Woessner & Wiemer 2005 covers this, but the paper does not use it).
   - The standard error and test treat Mc as known. A literature-grounded caveat is needed.

3. **The statistical independence problem is acknowledged but not grounded in literature.** The draft concedes that aftershocks violate the independence assumptions of the Shi-Bolt SE and Utsu's test. It then still reports "nine of ten pairs rejected at 1 percent" in the abstract and headline.
   - It cites no work on clustering and b-value inference. Candidates are Gardner & Knopoff (1974), Zaliapin & Ben-Zion (2013), Marzocchi, Spassiani et al. on declustering and b, and Kagan's work on aftershock-dominated catalogues.
   - Declustering is out of scope by the researcher's instruction. But the paper cannot both drop declustering and place the headline claim on tests it concedes are invalid. At least the literature on this should be cited, and the abstract should not lead with p-values.

4. **Positioning against the closest prior work is incomplete and partly miscalibrated.**
   - The paper treats Shearer & Stark (2012) as the closest work. It cites the 2011 online date, not the 2012 print issue. The researcher's brief used 2012, so the text and bib are inconsistent.
   - It omits the directly relevant debate that Shearer & Stark engaged with: Michael (2011), Bufe & Perkins (2005), Kagan & Jackson, Kagan (2010) and Daub et al. (2012). The planning document named all of these. Michael (2011) could not be resolved.
   - There is also no engagement with the literature on b-value variation with time or stress (Schorlemmer et al. 2005; Scholz 2015; Gulia & Wiemer 2019). The paper's own framing (stable or unstable) rests on it.
   - The claim of "no first claim" is honest, but the contribution cannot be assessed without these anchors.

5. **Several cited works are used loosely.**
   - Varty et al. (2021) is used for "extreme magnitudes with a time-varying measurement process". That is a different problem, extreme-value inference, from b-value stability in a heterogeneous catalogue, and it is not a close precedent.
   - Srivastava et al. (2021) is a regional study. It is used as a counterweight to a global-count claim but does not test the same hypothesis.
   - Kamer & Hiemer (2014) is cited as "the precision depends on N". That is the minimum-sample-size paper, and the paper then uses it to dismiss precision as a concern while also saying the SEs are too narrow. The two statements should be reconciled.
   - The Spearman (1904) and Hyndman & Fan citations are template material. They add nothing here and make the reference list look padded.

## MINOR CONCERNS

1. Author lists in `wiemer2000minimum` and `woessner2005assessing` are incomplete in the bib, as the supporting review already flagged. The text uses the correct pairs, but the bib must match, and `shi1982the` still lacks volume and pages. `shearer2011global` should have the 2012 print year (PNAS 109(3)). The key says 2011 and the text will print 2011.
2. `wong2011oxidation` is off-topic and should be removed from the bib, as the supporting review already says.
3. Cite the ComCat data source with both the DOI and the access date. ComCat is cited, but the paper does not point to documentation of how its preferred magnitudes are chosen. That is needed for the key finding on magnitude types. Candidates are the NEIC/ComCat magnitude-selection documentation and the contributing-network literature (ISC-GEM, GCMT: Ekstrom et al. 2012). GCMT is relevant because the paper states it was unavailable, so this limitation needs a citation.
4. The Related Literature section is structured around three strands but mostly lists cited items. It would be more useful if it said what each strand implies for the paper's own design, for example why +0.2 is a conservative correction.
5. Public-discourse claim ("earthquakes are becoming more frequent") is asserted without any source. Cite one example or the USGS FAQ.
6. The cited recent Mc papers (Wang 2025, Godano 2023) are only mentioned as "indicating that the choice remains consequential". Describe what they find or drop them.
7. Caution about timing: "Wiemer and Wyss showed that Mc varies in space and time" is a fair reading. But the paper then applies a single global Mc per decade, which the same literature warns against. State the global-versus-regional point explicitly with a citation. The plan raised this risk, and the draft omits it.

## POSITIVE ASPECTS

1. The cited methods are described accurately. The Shi-Bolt formula is given correctly, and Aki's b/sqrt(N) is labelled as Aki's, as the researcher required.
2. The paper uses only references that resolved, and it does not invent citations. This is an honest handling of an unverified literature, though it leaves the list short.
3. Positioning is modest and truthful. The paper declines a "first to show" claim and separates its scope (all M>=5 events) from Shearer & Stark's (great earthquakes).
4. The correct reading of incompleteness (it lowers b) matches Wiemer & Wyss and Woessner & Wiemer.
5. The limitations section matches the real structure of the literature on catalogue heterogeneity and censoring at the load floor, even though it does not cite it.

## Scores

DIMENSION SCORES:
- Contribution: 5/10
- Identification: n/a (descriptive; scored 6/10 for the appropriateness of the inference claims)
- Empirics: 6/10
- Writing: 7/10
- Literature: 4/10

OVERALL SCORE: 5.3/10
RECOMMENDATION: Major Revision
