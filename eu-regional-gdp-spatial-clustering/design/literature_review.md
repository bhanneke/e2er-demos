# Literature Review: Regional Income Disparities and Spatial Autocorrelation in the EU

**Paper:** GDP per capita in PPS across EU NUTS-2 regions in 2024 and the spatial clustering of high- and low-income regions.
**Template:** spatial analysis (descriptive, no causal claim).

## 0. Status and citation rules

- **Citable now (in `literature.bib`):** `moran1950notes`, `anselin1995local`, `anselin1988spatial`, `getis1992analysis`, `openshaw1984modifiable`, `pourpakdelfekr2026multispeed`, `Eurostat_Database`, `Eurostat_GISCO_NUTS`.
- **Section 7 entries are NOT yet citable.** I compiled them from my own knowledge of the literature and did not verify them against a database in this run. Volume and page details should be checked. Before the drafter cites any of them, run `e2er-lit search "<title>"` so the key is recorded. Entries I am less sure of are marked `[verify]`.
- Regulation numbers and region counts in section 5 are likewise from memory and need checking against EUR-Lex and Eurostat.

## 1. Convergence and divergence

**Beta and sigma convergence tradition.**
- Barro and Sala-i-Martin (1991, 1992) established absolute and conditional beta-convergence across US states and European regions. They reported a speed of about 2% per year.
- Sala-i-Martin (1996) summarised the evidence on regional cohesion.
- Magrini (2004) is the standard Handbook survey of regional (di)convergence.
- Eckey and Türck (2007) review the EU-specific literature.

**Distributional and club approaches.**
- Quah (1996) found "twin peaks" and convergence clubs among European regions. Aggregate beta-convergence hides polarisation, so mean-reversion regressions do not describe the cross-sectional shape.
- Corrado, Martin and Weeks (2005) and Fischer and Stirböck (2006) identify clubs. Phillips and Sul (2007) provide the log-t club test.
- Pourpakdelfekr (2026, in `.bib`) applies convergence clubs to subnational human development. It is the most recent citable anchor for "multispeed Europe" framing.

**Convergence across Europe.**
- Boldrin and Canova (2001) argue that EU regional policy has had little effect on convergence.
- Petrakos, Rodríguez-Pose and Rovolis (2005) find that integration raised national convergence but widened within-country disparities.
- Lopez-Bazo et al. (1999) and Badinger, Müller and Tondl (2004) show that spatial dependence is relevant for EU convergence.
- Bosker (2009) documents that regional GDP disparities in the old and new member states evolved differently. Between-country convergence coexists with within-country divergence, driven by capital and metropolitan regions in the east.
- Iammarino, Rodríguez-Pose and Storper (2019) give the synthesis: national convergence, rising within-country inequality, and metropolitan growth poles.
- Rodríguez-Pose (2018) and Dijkstra, Poelman and Rodríguez-Pose (2020) link stagnating regions to political discontent. This motivates why spatial patterns of income matter.
- Beugelsdijk, Klasing and Milionis (2018) attribute regional income differences largely to total factor productivity.
- Gennaioli et al. (2013) stress human capital.
- Lessmann and Seidel (2017) use night-light data to study regional inequality and convergence.

**Implication for this paper.** A 2024 cross-section cannot test convergence. It describes the end-point distribution that these studies are about. The paper should say so and avoid language of "convergence" or "effects".

## 2. Core-periphery and geography

- **New economic geography.** Krugman (1991) and Fujita, Krugman and Venables (1999) predict agglomeration and core-periphery gradients through market access, increasing returns and trade costs.
- **Policy implications.** Puga (2002) discusses what these models imply for European regional policy.
- **Empirical stylised facts.** The classical "blue banana" belt, a capital-region premium in the east and south, and a persistent south-Italian and eastern-periphery low-income cluster appear in Le Gallo and Ertur (2003), Ertur, Le Gallo and Baumont (2006) and Bosker (2009).
- **Pattern to expect, as a hypothesis from the literature, not a result:** high-high clusters in a belt from southern Germany, Austria, northern Italy, the Netherlands and Belgium. Low-low clusters in Bulgaria, Romania, Poland's east, Greece, southern Italy and parts of Spain and Portugal. Isolated high-low outliers at capital regions (Bucharest, Sofia, Warsaw, Budapest, Bratislava, Prague, Lisbon).

## 3. Spatial econometrics of regional GDP per capita

**Exploratory spatial data analysis (ESDA).**
- Le Gallo and Ertur (2003) is the closest antecedent. They use ESDA on European regional per capita GDP, 1980–1995. They find strong positive global spatial autocorrelation (Moran's I rising over time), a stable pattern of local clusters, and non-stationarity across space. The paper uses Moran scatterplots and LISA.
- Rey (2001) and Rey and Janikas (2005) integrate ESDA with convergence and inequality analysis.
- Rey and Montouri (1999) estimate spatial-error models for US regions.

**Models with spatial effects.**
- Ertur, Le Gallo and Baumont (2006) estimate spatial regimes and spatial dependence in the European convergence process.
- Fingleton and López-Bazo (2006) and Ertur and Koch (2007) give growth models with spatial externalities.
- Dall'Erba and Le Gallo (2008) and Ramajo et al. (2008) estimate structural-fund effects with spatial models.
- Foundational texts: Cliff and Ord (1981), Anselin (1988, in `.bib`), LeSage and Pace (2009), Elhorst (2014).
- This study is descriptive, so these papers are context for what a future regression would require (SAR/SEM/SDM, spatial regimes). They are not methods to claim.

**Tobler's first law.** Tobler (1970): near things are more related than distant things. This is the usual motivation for spatial weights.

**Weights matrices.**
- Choices are queen or rook contiguity, k-nearest neighbours, and distance bands. Contiguity leaves islands (Malta, Cyprus, Canary Islands, Azores, Madeira, French overseas regions, Greek and Italian islands) without neighbours, so k-NN or a distance threshold is often needed.
- Report sensitivity to the weights choice.
- Rey and Anselin (2007) and Anselin, Syabri and Kho (2006) document the PySAL and GeoDa implementations.

## 4. Moran's I and LISA in EU cohesion-policy research

- **Global Moran's I.** Moran (1950, in `.bib`) is the original statistic. Cliff and Ord (1981) provide inference, using permutation or the normal approximation.
- **Local statistics.** Anselin (1995, in `.bib`) defines LISA and the Moran scatterplot quadrants HH, LL, HL, LH. Anselin (1996) introduces the Moran scatterplot. Getis and Ord (1992, in `.bib`) and Ord and Getis (1995) give G and G* statistics, a complement for hot and cold spots.
- **Multiple testing.** Local statistics are many correlated tests. Report the pseudo-p-value count, the permutation number, and a correction (Benjamini and Hochberg 1995; Caldas de Castro and Singer 2006 for spatial dependence). Uncorrected 5% LISA maps overstate cluster counts.
- **Use in cohesion research.**
  - Le Gallo and Ertur (2003), Ertur et al. (2006) and Dall'Erba and Le Gallo (2008) use Moran's I and LISA on EU NUTS-2 and NUTS-3 data.
  - Moran's I is the standard first diagnostic in this literature. Positive and significant Moran's I on per capita GDP is the near-universal finding.
  - Cohesion-policy evaluation uses spatial autocorrelation to justify spatial models. It also bears on whether Objective 1 and convergence-region eligibility, which is defined on NUTS-2 GDP per capita in PPS relative to the EU average (below 75% for "less developed regions"), cluster geographically. (Eligibility thresholds: 75% and 90–100% under the 2021–2027 rules. [verify].)
- **MAUP.** Openshaw (1984, in `.bib`) and Fotheringham and Wong (1991): results depend on zoning and scale. NUTS-2 is an administrative, not functional, partition, so Moran's I will differ at NUTS-1 or NUTS-3. The paper should state this as a limitation.
- **Sensitivity checks that the literature expects:** alternative weights, Moran's I with and without the capital or outlier regions, within-country versus between-country components of spatial autocorrelation, and Moran's I on ln(GDP) versus levels.

## 5. Eurostat regional GDP methodology

**Definition and measure.**
- Regional GDP is compiled under ESA 2010 (Regulation (EU) No 549/2013).
- The data table `gdp_pps_nuts2` uses unit `PPS_EU27_2020_HAB`, i.e. GDP per inhabitant in purchasing power standards with EU27 (from 2020) as the reference. PPS removes price-level differences between countries but not within countries, because the PPP is national. Regional price differences (e.g. Paris, London, Milan versus rural areas) are not captured. This biases cross-region comparison within a country.
- The `gdp_index` column in `gdp_pps_sample` is presumably the EU-average-based index (EU27 = 100). Check how it was built.
- Provisional values are flagged `p`, estimates `e`. The 2024 sample carries `p` flags. These are provisional and revised.

**Workplace-based measure and commuting.** Regional GDP is allocated to the region where production occurs, while population is by residence. Regions with net in-commuting (Brussels, Inner London, Hamburg, Prague, Bratislava, Vienna, Luxembourg, Île-de-France in part) show inflated GDP per capita, and surrounding residential regions look poorer. This produces spurious high-low or low-high neighbour pairs, and it affects LISA outcomes near capital regions. Eurostat itself warns about it in its regional GDP documentation ("Statistics Explained: Regional GDP"). Mitigations: NUTS-3 or functional urban area analysis, GDP per employed person, or merging the capital with its commuting hinterland as a robustness check.

**Capital-region effects.** Capital regions in the east (Bucharest-Ilfov, Sofia, Praha, Bratislavský kraj, Warszawski stoleczny, Budapest) are very high relative to their national hinterland. Iammarino et al. (2019) describe a metropolitan-growth-pole pattern. Small, single-city NUTS-2 regions (Brussels, Hamburg, Vienna, Luxembourg, Bremen, Inner London) are statistical outliers. Moran's I is sensitive to them.

**NUTS versions.**
- NUTS is set by Regulation (EC) No 1059/2003. Amendments take effect 2008, 2013, 2016, 2021 and 2024 [verify the legal act numbers, e.g. Commission Regulation (EU) 2016/2066; Regulation (EU) 2019/1755; Delegated Regulation (EU) 2023/674].
- The number of EU27 NUTS-2 regions changed between versions (about 242 in NUTS 2021 and 244 in NUTS 2024 [verify]).
- Boundary changes (for example Poland, Ireland, Lithuania, the Czech Republic, Croatia, Germany) break time comparability. The 2024 cross-section is unaffected, but the NUTS vintage of the GDP table and the GISCO boundaries must match.
- The warehouse has `nuts2_boundaries` with 299 rows. This exceeds the EU27 set because it includes non-EU countries (EFTA, candidates, UK). Filter to EU27 and check that `gdp_pps_nuts2.geo` and `nuts_id` use the same NUTS vintage. Unmatched IDs signal a version mismatch.
- Boundaries come from GISCO (`Eurostat_GISCO_NUTS`). The coordinates in the table appear to be in a projected CRS (values around 4.3e6, 2.5e6), consistent with EPSG:3035 (ETRS89-LAEA). Verify before computing distances.

**Other data caveats for the drafter.**
- The `gdp_pps_nuts2` table has 2,826 rows for 2015 to 2024. Rows with missing 2024 values and French overseas regions, Cyprus, Malta and other single-region countries need an explicit treatment.
- GDP values are rounded (to hundreds of PPS) in the sample.
- Population is from `pop_nuts2` (2024). Per capita GDP could be weighted by population for weighted inequality measures.
- Cite the data as `Eurostat_Database` and `Eurostat_GISCO_NUTS`.

## 6. Gaps in the literature this paper can address, and cautions

- Most ESDA work covers the 1980s to 2000s (Le Gallo and Ertur 2003 ends in 1995). A current PPS-based cross-section for the EU27 after Brexit and with the eastern enlargement is a modest update. The contribution is descriptive and should not be oversold.
- The paper can quantify how much of the spatial autocorrelation is between-country (national price and productivity levels) versus within-country, for example by Moran's I on residuals from country fixed effects. This is a descriptive decomposition, not a causal claim.
- Treat commuting and capital-region distortion explicitly.
- Do not use "convergence", "effect" or "impact" language for a 2024 cross-section.

## 7. BibTeX (not yet in literature.bib; run `e2er-lit search` before citing)

```bibtex
@article{barro1991convergence,
  author = {Barro, Robert J. and Sala-i-Martin, Xavier},
  title = {Convergence across States and Regions},
  journal = {Brookings Papers on Economic Activity},
  year = {1991}, volume = {1991}, number = {1}, pages = {107--182}
}
@article{barro1992convergence,
  author = {Barro, Robert J. and Sala-i-Martin, Xavier},
  title = {Convergence},
  journal = {Journal of Political Economy},
  year = {1992}, volume = {100}, number = {2}, pages = {223--251}
}
@article{salaimartin1996regional,
  author = {Sala-i-Martin, Xavier},
  title = {Regional Cohesion: Evidence and Theories of Regional Growth and Convergence},
  journal = {European Economic Review},
  year = {1996}, volume = {40}, number = {6}, pages = {1325--1352}
}
@article{quah1996regional,
  author = {Quah, Danny T.},
  title = {Regional Convergence Clusters across {Europe}},
  journal = {European Economic Review},
  year = {1996}, volume = {40}, number = {3--5}, pages = {951--958}
}
@incollection{magrini2004regional,
  author = {Magrini, Stefano},
  title = {Regional (Di)Convergence},
  booktitle = {Handbook of Regional and Urban Economics},
  editor = {Henderson, J. Vernon and Thisse, Jacques-Fran{\c{c}}ois},
  publisher = {Elsevier}, year = {2004}, volume = {4}, pages = {2741--2796}
}
@article{corrado2005identifying,
  author = {Corrado, Luisa and Martin, Ron and Weeks, Melvyn},
  title = {Identifying and Interpreting Regional Convergence Clusters across {Europe}},
  journal = {The Economic Journal},
  year = {2005}, volume = {115}, number = {502}, pages = {C133--C160}
}
@article{fischer2006panEuropean,
  author = {Fischer, Manfred M. and Stirb{\"o}ck, Claudia},
  title = {Pan-{European} Regional Income Growth and Club-Convergence},
  journal = {The Annals of Regional Science},
  year = {2006}, volume = {40}, number = {4}, pages = {693--721}
}
@article{phillips2007transition,
  author = {Phillips, Peter C. B. and Sul, Donggyu},
  title = {Transition Modeling and Econometric Convergence Tests},
  journal = {Econometrica},
  year = {2007}, volume = {75}, number = {6}, pages = {1771--1855}
}
@article{boldrin2001inequality,
  author = {Boldrin, Michele and Canova, Fabio},
  title = {Inequality and Convergence in {Europe's} Regions: Reconsidering {European} Regional Policies},
  journal = {Economic Policy},
  year = {2001}, volume = {16}, number = {32}, pages = {205--253}
}
@article{petrakos2005growth,
  author = {Petrakos, George and Rodr{\'i}guez-Pose, Andr{\'e}s and Rovolis, Antonis},
  title = {Growth, Integration, and Regional Disparities in the {European Union}},
  journal = {Environment and Planning A},
  year = {2005}, volume = {37}, number = {10}, pages = {1837--1855}
}
@article{badinger2004regional,
  author = {Badinger, Harald and M{\"u}ller, Werner G. and Tondl, Gabriele},
  title = {Regional Convergence in the {European Union}, 1985--1999: A Spatial Dynamic Panel Analysis},
  journal = {Regional Studies},
  year = {2004}, volume = {38}, number = {3}, pages = {241--253}
}
@article{bosker2009spatial,
  author = {Bosker, Maarten},
  title = {The Spatial Evolution of Regional {GDP} Disparities in the 'Old' and the 'New' {Europe}},
  journal = {Papers in Regional Science},
  year = {2009}, volume = {88}, number = {1}, pages = {3--27}
}
@article{iammarino2019regional,
  author = {Iammarino, Simona and Rodr{\'i}guez-Pose, Andr{\'e}s and Storper, Michael},
  title = {Regional Inequality in {Europe}: Evidence, Theory and Policy Implications},
  journal = {Journal of Economic Geography},
  year = {2019}, volume = {19}, number = {2}, pages = {273--298}
}
@article{rodriguezpose2018revenge,
  author = {Rodr{\'i}guez-Pose, Andr{\'e}s},
  title = {The Revenge of the Places That Don't Matter (and What to Do about It)},
  journal = {Cambridge Journal of Regions, Economy and Society},
  year = {2018}, volume = {11}, number = {1}, pages = {189--209}
}
@article{dijkstra2020geography,
  author = {Dijkstra, Lewis and Poelman, Hugo and Rodr{\'i}guez-Pose, Andr{\'e}s},
  title = {The Geography of {EU} Discontent},
  journal = {Regional Studies},
  year = {2020}, volume = {54}, number = {6}, pages = {737--753}
}
@article{beugelsdijk2018regional,
  author = {Beugelsdijk, Sjoerd and Klasing, Mariko J. and Milionis, Petros},
  title = {Regional Economic Development in {Europe}: The Role of Total Factor Productivity},
  journal = {Regional Studies},
  year = {2018}, volume = {52}, number = {4}, pages = {461--476}
}
@article{gennaioli2013human,
  author = {Gennaioli, Nicola and La Porta, Rafael and Lopez-de-Silanes, Florencio and Shleifer, Andrei},
  title = {Human Capital and Regional Development},
  journal = {The Quarterly Journal of Economics},
  year = {2013}, volume = {128}, number = {1}, pages = {105--164}
}
@article{lessmann2017regional,
  author = {Lessmann, Christian and Seidel, Andr{\'e}},
  title = {Regional Inequality, Convergence, and Its Determinants -- A View from Outer Space},
  journal = {European Economic Review},
  year = {2017}, volume = {92}, pages = {110--132}
}
@article{krugman1991increasing,
  author = {Krugman, Paul},
  title = {Increasing Returns and Economic Geography},
  journal = {Journal of Political Economy},
  year = {1991}, volume = {99}, number = {3}, pages = {483--499}
}
@book{fujita1999spatial,
  author = {Fujita, Masahisa and Krugman, Paul and Venables, Anthony J.},
  title = {The Spatial Economy: Cities, Regions, and International Trade},
  publisher = {MIT Press}, year = {1999}
}
@article{puga2002european,
  author = {Puga, Diego},
  title = {{European} Regional Policies in Light of Recent Location Theories},
  journal = {Journal of Economic Geography},
  year = {2002}, volume = {2}, number = {4}, pages = {373--406}
}
@article{legallo2003exploratory,
  author = {Le Gallo, Julie and Ertur, Cem},
  title = {Exploratory Spatial Data Analysis of the Distribution of Regional per Capita {GDP} in {Europe}, 1980--1995},
  journal = {Papers in Regional Science},
  year = {2003}, volume = {82}, number = {2}, pages = {175--201}
}
@article{ertur2006european,
  author = {Ertur, Cem and Le Gallo, Julie and Baumont, Catherine},
  title = {The {European} Regional Convergence Process, 1980--1995: Do Spatial Regimes and Spatial Dependence Matter?},
  journal = {International Regional Science Review},
  year = {2006}, volume = {29}, number = {1}, pages = {3--34}
}
@article{ertur2007growth,
  author = {Ertur, Cem and Koch, Wilfried},
  title = {Growth, Technological Interdependence and Spatial Externalities: Theory and Evidence},
  journal = {Journal of Applied Econometrics},
  year = {2007}, volume = {22}, number = {6}, pages = {1033--1062}
}
@article{fingleton2006empirical,
  author = {Fingleton, Bernard and L{\'o}pez-Baz{\'o}, Enrique},
  title = {Empirical Growth Models with Spatial Effects},
  journal = {Papers in Regional Science},
  year = {2006}, volume = {85}, number = {2}, pages = {177--198}
}
@article{rey1999us,
  author = {Rey, Sergio J. and Montouri, Brett D.},
  title = {{US} Regional Income Convergence: A Spatial Econometric Perspective},
  journal = {Regional Studies},
  year = {1999}, volume = {33}, number = {2}, pages = {143--156}
}
@article{rey2001spatial,
  author = {Rey, Sergio J.},
  title = {Spatial Empirics for Economic Growth and Convergence},
  journal = {Geographical Analysis},
  year = {2001}, volume = {33}, number = {3}, pages = {195--214}
}
@article{rey2005regional,
  author = {Rey, Sergio J. and Janikas, Mark V.},
  title = {Regional Convergence, Inequality, and Space},
  journal = {Journal of Economic Geography},
  year = {2005}, volume = {5}, number = {2}, pages = {155--176}
}
@article{dallerba2008regional,
  author = {Dall'Erba, Sandy and Le Gallo, Julie},
  title = {Regional Convergence and the Impact of {European} Structural Funds over 1989--1999: A Spatial Econometric Analysis},
  journal = {Papers in Regional Science},
  year = {2008}, volume = {87}, number = {2}, pages = {219--244}
}
@article{ramajo2008spatial,
  author = {Ramajo, Julian and M{\'a}rquez, Miguel A. and Hewings, Geoffrey J. D. and Salinas, Mar{\'i}a M.},
  title = {Spatial Heterogeneity and Interregional Spillovers in the {European Union}: Do Cohesion Policies Encourage Convergence across Regions?},
  journal = {European Economic Review},
  year = {2008}, volume = {52}, number = {3}, pages = {551--567}
}
@article{becker2010going,
  author = {Becker, Sascha O. and Egger, Peter H. and von Ehrlich, Maximilian},
  title = {Going {NUTS}: The Effect of {EU} Structural Funds on Regional Performance},
  journal = {Journal of Public Economics},
  year = {2010}, volume = {94}, number = {9--10}, pages = {578--590}
}
@book{cliff1981spatial,
  author = {Cliff, Andrew D. and Ord, J. Keith},
  title = {Spatial Processes: Models and Applications},
  publisher = {Pion}, address = {London}, year = {1981}
}
@book{lesage2009introduction,
  author = {LeSage, James and Pace, R. Kelley},
  title = {Introduction to Spatial Econometrics},
  publisher = {Chapman and Hall/CRC}, year = {2009}
}
@book{elhorst2014spatial,
  author = {Elhorst, J. Paul},
  title = {Spatial Econometrics: From Cross-Sectional Data to Spatial Panels},
  publisher = {Springer}, year = {2014}
}
@article{tobler1970computer,
  author = {Tobler, Waldo R.},
  title = {A Computer Movie Simulating Urban Growth in the {Detroit} Region},
  journal = {Economic Geography},
  year = {1970}, volume = {46}, number = {sup1}, pages = {234--240}
}
@article{ord1995local,
  author = {Ord, J. Keith and Getis, Arthur},
  title = {Local Spatial Autocorrelation Statistics: Distributional Issues and an Application},
  journal = {Geographical Analysis},
  year = {1995}, volume = {27}, number = {4}, pages = {286--306}
}
@incollection{anselin1996moran,
  author = {Anselin, Luc},
  title = {The {Moran} Scatterplot as an {ESDA} Tool to Assess Local Instability in Spatial Association},
  booktitle = {Spatial Analytical Perspectives on {GIS}},
  editor = {Fischer, Manfred and Scholten, Henk J. and Unwin, David},
  publisher = {Taylor and Francis}, year = {1996}, pages = {111--125}
}
@article{caldasdecastro2006controlling,
  author = {Caldas de Castro, Marcia and Singer, Burton H.},
  title = {Controlling the False Discovery Rate: A New Application to Account for Multiple and Dependent Tests in Local Statistics of Spatial Association},
  journal = {Geographical Analysis},
  year = {2006}, volume = {38}, number = {2}, pages = {180--208}
}
@article{benjamini1995controlling,
  author = {Benjamini, Yoav and Hochberg, Yosef},
  title = {Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing},
  journal = {Journal of the Royal Statistical Society: Series B},
  year = {1995}, volume = {57}, number = {1}, pages = {289--300}
}
@article{fotheringham1991modifiable,
  author = {Fotheringham, A. Stewart and Wong, David W. S.},
  title = {The Modifiable Areal Unit Problem in Multivariate Statistical Analysis},
  journal = {Environment and Planning A},
  year = {1991}, volume = {23}, number = {7}, pages = {1025--1044}
}
@article{anselin2006geoda,
  author = {Anselin, Luc and Syabri, Ibnu and Kho, Youngihn},
  title = {{GeoDa}: An Introduction to Spatial Data Analysis},
  journal = {Geographical Analysis},
  year = {2006}, volume = {38}, number = {1}, pages = {5--22}
}
@article{rey2007pysal,
  author = {Rey, Sergio J. and Anselin, Luc},
  title = {{PySAL}: A {Python} Library of Spatial Analytical Methods},
  journal = {The Review of Regional Studies},
  year = {2007}, volume = {37}, number = {1}, pages = {5--27}
}
@article{eckey2007convergence,
  author = {Eckey, Hans-Friedrich and T{\"u}rck, Matthias},
  title = {Convergence of {EU}-Regions: A Literature Report},
  journal = {Investigaciones Regionales},
  year = {2007}, volume = {10}, pages = {5--32}
}
@article{lopezbazo1999regional,
  author = {L{\'o}pez-Baz{\'o}, Enrique and Vay{\'a}, Esther and Mora, Antonio J. and Suri{\~n}ach, Jordi},
  title = {Regional Economic Dynamics and Convergence in the {European Union}},
  journal = {The Annals of Regional Science},
  year = {1999}, volume = {33}, number = {3}, pages = {343--370}
}
@misc{eurostat2013esa,
  author = {{European Parliament and Council}},
  title = {Regulation ({EU}) No 549/2013 on the European System of National and Regional Accounts in the European Union ({ESA} 2010)},
  year = {2013}
}
@misc{eurostat2003nuts,
  author = {{European Parliament and Council}},
  title = {Regulation ({EC}) No 1059/2003 on the Establishment of a Common Classification of Territorial Units for Statistics ({NUTS})},
  year = {2003}
}
```

## 8. Handoff

- Data specialists: filter `nuts2_boundaries` to EU27, align NUTS vintage with the GDP table, confirm the CRS (appears to be EPSG:3035), and choose a weights matrix that handles islands.
- Analysis: Moran's I, Moran scatterplot, LISA with multiple-testing correction, sensitivity to weights and to capital or commuting outliers, and a between- versus within-country decomposition.
- Drafter: cite only keys in `literature.bib` unless new ones are registered through `e2er-lit search`.
