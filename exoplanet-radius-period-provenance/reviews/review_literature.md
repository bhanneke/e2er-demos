# Literature Review of the Paper: "How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance"

Reviewer role: literature coverage, positioning, and citation accuracy. Simulated referee for a field journal; the paper is a descriptive catalogue study, so I weigh literature fit against that scope.

DIMENSION SCORES:
- Contribution: 4/10
- Identification: 6/10 (no causal claim; the descriptive design is internally honest, so I score the validity of the descriptive grouping rule)
- Empirics: 6/10
- Writing: 7/10
- Literature: 3/10

MAJOR CONCERNS:

1. **The draft engages almost none of the literature that its own review prepared.** The literature review lists the radius valley (Fulton et al. 2017; Fulton and Petigura 2018; Van Eylen et al. 2018), the photoevaporation and core-powered mass-loss explanations, and the short-period desert papers (Szabó and Kiss 2011; Mazeh et al. 2016; Lundkvist et al. 2016; Owen and Lai 2018). The draft cites none of them. The paper's headline object, the "two humps" at 2–4 and 8–15 Earth radii and the sparse 4–8 Earth radius region, is exactly what that literature studies. The reader cannot see how the catalogue-level humps relate to the known valley, desert, and sub-Neptune/giant bimodality. Add a short related-work section.

2. **The central claim is not tied to the mass-radius literature.** The provenance rule rests on the archive's CALCULATED_VALUE label and on the Chen and Kipping (2017) relation. The draft never cites Chen and Kipping, and it does not say which relation, in which mass regimes, produces the radii. Yet the key result depends on it: calculated radii are bounded at 14.3 Earth radii, and 846 of 1,529 planets in the 8–15 hump are calculated. A reader needs to know that the relation has a flat, near-Jupiter regime, so many giants get nearly the same radius regardless of mass. The weak mass-radius rank correlation (0.47) is explained in the text as "a relation that is not increasing over the full mass range" without a source. The paper should cite Chen and Kipping and the related relations (Weiss and Marcy 2014; Otegi et al. 2020; Zeng et al.), state the regime boundaries (after checking them in the source), and tie the 14.3 Earth-radius bound and the hump at 8–15 to them. Note also that the "giant-planet hump" being half calculated means part of that hump is a model artefact; this deserves explicit discussion against the literature on the Jovian radius plateau.

3. **No positioning against prior work on catalogue composition and selection.** The paper's own plan names Petigura et al., Hsu et al., and Kepler occurrence-rate work as closest relatives, but the draft cites none of them, and the literature review declares that no gap was claimed. A "contribution" paragraph (the draft lists three) needs a statement of what prior work did not do. At minimum, the draft should cite work that already warns against reading the archive diagram as a population map and that already treats transit and radial-velocity selection (e.g., Foreman-Mackey 2016 is cited once, only for a generic statement; Kepler completeness and RV detectability papers are absent). The claim that the decomposition is a "documented" contribution is weak without showing that no one has tabulated archive radii by provenance. Either search and cite, or soften.

4. **Citation use is thin and partly misdirected.** Examples:
   - `cloutier2024exoplanet` is cited in the first sentence for the claim that the radius-period diagram is the standard summary. I cannot verify from the supplied review that this reference supports that claim; it was not listed in the review's checked keys. Verify it, or remove it.
   - `berger2018revised` is cited for "requires an estimate of the stellar radius", which is acceptable, but the draft ignores the substantial effect of stellar radius revisions on the transit-radius group (Gaia DR2 radii shifted Kepler planet radii; this is the valley-location literature of Fulton and Petigura 2018).
   - `foremanmackey2016the` and `nielsen2019the` appear for selection statements. The review did not list them as checked, so their relevance must be confirmed. Detection-bias claims for RV (long baselines, mass sensitivity) cite a transit/occurrence paper that I cannot confirm covers them; cite RV detectability sources.
   - `little2019statistical` for "we do not impute" is a generic missing-data textbook; it adds nothing. Remove or replace with the archive documentation.
   - The archive documentation of the calculation (pscp_calc page, Akeson et al. 2013) is not cited at the point where the provenance rule is introduced. It is the primary source of the rule and must be cited there.

5. **Literature on the archive's own provenance and reliability is missing.** The paper's rule is only as good as the archive label. The draft admits there is no validation against references and no `ps` robustness table. The literature should at least be used to describe how composite parameters are assembled (Christiansen et al. 2025 is cited but not for this mechanism) and to discuss prior verification of the archive's composite table.

6. **Mis-framed interpretive statements that need support or removal.** (a) "the calculated group consists almost entirely of radial-velocity discoveries" is stated as an "informative" finding about discovery method, but the data summary shows 292 microlensing and 52 imaging planets among the 1,537 calculated radii, and 1,133 RV of 1,215 in the sample is 93 percent, so "almost entirely" is acceptable only for the analysis sample; say so, because the dictionary notes microlensing planets mostly lack periods. (b) The statement that the true mass and radius "may be larger" for minimum-mass planets needs the sin i literature cited; for a radius from a mass-radius relation the direction is not monotone (a larger mass can give a smaller or equal radius in the Jovian regime). (c) The limit sentence that "imaging surveys probe wide orbits" cites a single review for a group of 20 planets; fine, but the 15,958-day median period should be placed in that context.

MINOR CONCERNS:

1. Chen and Kipping appears in the bib with year 2016 (online date) while the paper is ApJ 834, 17 (2017). The draft should use 2017 consistently with the data dictionary, which says "Chen and Kipping 2017".
2. Method citations are listed in the review (Freedman and Diaconis; Hyndman and Fan; Spearman) but the draft cites only Hyndman and Fan and Spearman. Binning is decade-based and a 0.25-dex fine grid, so say which choice is justified by Freedman-Diaconis or drop that reference. The bootstrap is used throughout, but no bootstrap reference (e.g., Efron) is cited.
3. The Kolmogorov-Smirnov distance is used without citation, and the plan also announced Wasserstein distance; if dropped, say so.
4. The introduction says the diagram "has become the standard summary". Give two or three examples of papers that use it that way, or temper the statement.
5. The text mixes "calculated" and "mass-derived"; the plan used the latter. Be consistent, and say that "calculated" is the archive's term.
6. The acknowledgement and data-citation requested by the archive (standard acknowledgement; Christiansen et al. 2025; DOI 10.26133/NEA13) should appear in the paper.
7. The closing questions (replacing calculated radii with measured radii for planets that have both) point to existing literature on radius-mass comparisons for transiting planets with RV masses; cite it, since the answer partly exists (e.g., tests of the Chen and Kipping forecasts against measured radii).
8. The conclusion's advice "report the group when a radius is quoted from the archive" is a recommendation without a cited precedent; say whether others already do this.
9. The abstract and conclusion now correct the hump statement (1,901 of 2,090; 846 of 1,529). The introduction's third finding still reads "pooled association mixes two provenances"; consistent, but consider cross-referencing the humps there too.

POSITIVE ASPECTS:

1. The scope is stated honestly: the paper repeatedly says the patterns describe the catalogue, not the planet population, and it makes no causal claim.
2. The provenance rule uses a label supplied by the archive itself, which makes the decomposition reproducible; the draft states plainly what it did not do (controversial flag, hand validation, `ps` table).
3. The description of the data source is clear, with sample flow, group definitions, and a cross-tabulation with the transit flag; sources are cited at the numbers through comments.
4. The correction of the hump statement (giant hump more than half calculated) is a useful point that a reader of the pooled diagram would otherwise miss.
5. The data citation (Christiansen et al. 2025; the composite table) is correct and the method references for quantiles and rank correlation are appropriate.

Summary judgment: as a literature matter, the manuscript is under-referenced relative to its own prepared review. Using the radius valley, desert, and mass-radius relation literature to interpret the humps and the 14.3 Earth-radius bound, and positioning against catalogue-selection work, would lift it from an unreferenced tabulation to a useful reference note. The novelty is modest and the paper should say so.

OVERALL SCORE: 4.6/10
RECOMMENDATION: Major Revision
