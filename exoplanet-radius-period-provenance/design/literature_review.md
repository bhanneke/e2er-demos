# Literature Review: Exoplanet Radius-Period Distribution

## Scope and status

- Short, descriptive review. It makes no claim that the literature has a gap.
- The supplied corpus (crypto, market microstructure, information systems) and the "researcher's own papers" list are off-topic. None of them is cited.
- Every key below is in `literature.bib`. Each was registered through `e2er-lit save --doi`, which returned the record for that DOI. I checked the titles of the saved records against the intended papers. Three DOIs that I first tried returned unrelated papers; I deleted those entries from the bib. Page and volume details were not re-read against the publishers.
- Already in the bib before this pass and usable here: `Christiansen2025_NEA`, `NEA_PSCompPars`, `NEA_PS`, `berger2018revised`, `eylen2015eccentricity`, `eylen2019the`, and the method sources `freedman1981histogram`, `hyndman1996sample`, `spearman1904proof`.
- Note on `chen2016probabilistic`: the record carries year 2016 (the online date). The paper appears in ApJ 834, 17, in 2017. The bib year is 2016; the text may say "Chen and Kipping" without a year, or follow the bib.

## 1. The archive and its radii

- The NASA Exoplanet Archive is the source of the confirmed-planet table. Its current description is Christiansen et al. \cite{Christiansen2025_NEA}; the earlier description is Akeson et al. \cite{akeson2013the}. The tables used here are the Planetary Systems Composite table \cite{NEA_PSCompPars} and, for reference, the Planetary Systems table \cite{NEA_PS}.
- The archive documents that radii it calculates from mass are marked in `pl_rade_reflink` as "Calculated Value", with the mass-radius relation of Chen and Kipping \cite{chen2016probabilistic}. This is the provenance rule the study uses (the researcher's instruction and `data_dictionary.json`). It is a fact about the archive's documentation, taken from the researcher's notes, not a result of the literature review.
- Chen and Kipping \cite{chen2016probabilistic} give a probabilistic mass-radius relation in several regimes, built to forecast a radius from a mass or the reverse. A radius derived this way is a model output with scatter, not a measurement. I do not quote break points or exponents here, since I did not check them against the paper.
- Stellar radii enter every transit radius. Berger et al. \cite{berger2018revised} revise Kepler host and planet radii with Gaia DR2.

## 2. Radius valley

- Fulton et al. \cite{fulton2017the}, using the California-Kepler Survey, report a deficit of planets near 1.5 to 2.0 Earth radii, which separates smaller from larger small planets.
- Fulton and Petigura \cite{fulton2018the} use Gaia DR2 radii and report that the location of the gap depends on stellar mass.
- Van Eylen et al. \cite{eylen2018an} use asteroseismic stellar radii and report a sharper gap whose location depends on orbital period.
- Explanations in the literature include photoevaporation \cite{owen2013kepler,owen2017the} and core-powered mass loss \cite{ginzburg2018corepowered,gupta2019sculpting}.
- Relevance to this study: these papers measure the valley in samples with transit radii and precise stellar radii. They say nothing on radii calculated from mass.

## 3. Short-period desert of Neptune-size and hot-Jupiter planets

- Szabó and Kiss \cite{szabo2011a} report a short-period shortage of sub-Jupiter-mass planets.
- Mazeh, Holczer and Faigler \cite{mazeh2016dearth} describe a dearth of short-period Neptune-size planets in the period-mass and period-radius planes.
- Lundkvist et al. \cite{lundkvist2016hot} report that planets of intermediate radius are missing at high incident flux.
- Owen and Lai \cite{owen2018photoevaporation} discuss photoevaporation and high-eccentricity migration as shaping that region.
- Boundaries differ across these papers and between the mass and radius planes, so this study quotes none of them as numbers.

## 4. Methods used in the descriptive analysis

- Histogram bin width: \cite{freedman1981histogram}. Sample quantiles: \cite{hyndman1996sample}. Rank correlation: \cite{spearman1904proof}. Cite only those the analysis used.

## 5. Handoff

- The drafter may cite only the keys named above; all resolve in `literature.bib`.
- Eccentricity papers \cite{eylen2015eccentricity,eylen2019the} are in the bib but are not needed for this paper.
- Not registered, and so not to be cited: Petigura et al. 2022, Lopez and Fortney, Kepler occurrence-rate papers, the Weiss and Marcy mass-radius relation, and the radial-velocity detection papers. They are outside the short scope of this review. Register them with `e2er-lit save --doi` first if the draft needs them.
