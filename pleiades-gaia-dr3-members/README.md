<!-- e2er:github begin -->
# Which Stars within 3 Degrees of the Pleiades Centre Share Its Astrometry? A Descriptive Reading of Gaia DR3 Membership, Parallax Distance and the Colour–Magnitude Diagram

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** Which stars within 3 degrees of the Pleiades centre are cluster members by Gaia DR3 parallax and proper motion, and what do their colour-magnitude diagram and parallax distance distribution show about the cluster's distance and main sequence?

**Dossier:** https://e2er.org/d/ed64be6914a73236 (every step of the run, the models, the data loads and the checks; id `sha256:ed64be6914a73236947710ac05e258595632a9bf598ec58e3fbe04926866a8d1`)

**Made with:** e2er 0.16.0; template descriptive-study; model haiku (claude_code)

## Data

- **Gaia Data Release 3 (ESA/Gaia/DPAC), Gaia ESA Archive, release DR3**
  - Terms: CC BY-NC 3.0 IGO (https://creativecommons.org/licenses/by-nc/3.0/igo/). The Gaia licence page (https://www.cosmos.esa.int/web/gaia-users/license): "Gaia data are distributed under the CC BY-NC 3.0 IGO license." The ESA archives' terms (https://www.cosmos.esa.int/web/esdc/terms-and-conditions): data "are open and free to use by the User subject to proper acknowledgment to be given in accordance with the credit lines provided below" (Gaia: "Credit: ESA, Gaia DPAC"), and "Prior to any commercial use by the User of any Data or Data Product, including any use or application that directly or indirectly generates a financial gain, a detailed request for authorisation/licence shall be made". Acknowledgement: This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium). Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.
  - Full terms: https://www.cosmos.esa.int/web/gaia-users/license
  - Cite: Gaia Collaboration, Vallenari, A., Brown, A. G. A., Prusti, T., et al. (2023). Gaia Data Release 3: Summary of the content and survey properties. Astronomy & Astrophysics, 674, A1. https://doi.org/10.1051/0004-6361/202243940; and Gaia Collaboration, Prusti, T., de Bruijne, J. H. J., Brown, A. G. A., et al. (2016). The Gaia mission. Astronomy & Astrophysics, 595, A1. https://doi.org/10.1051/0004-6361/201629272. Acknowledgement: This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium). Funding for the DPAC has been provided by national institutions, in particular the institutions participating in the Gaia Multilateral Agreement.

## Files left out

These files of the study are not in this folder:

- `data/data.db`: the terms of ESA Gaia Data Release 3 (Gaia) do not allow passing the data on; the study's code does not read it, so a rerun does not need it.
- `data/gaia_clean.csv`: built from ESA Gaia Data Release 3 (Gaia) data, whose terms do not allow passing it on; `e2er reproduce` builds it again with code/scratch/clean_gaia.py from the data it loads again.
- `results/figure_spec.json`: built from ESA Gaia Data Release 3 (Gaia) data and holds them row by row (an array of 9,863 values at figures[2].y); its terms do not allow passing them on; the study's code does not read it, so a rerun does not need it; no recorded step builds it again from the data a rerun loads.

`e2er reproduce .` runs the study's steps again in a copy of this folder, getting each of these files as its line says, and compares the results with the published ones. `e2er-package.json` lists every file here with its SHA-256 and what was left out.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# Which stars within 3 degrees of the Pleiades centre are cluster members by Ga...

**Research question:** Which stars within 3 degrees of the Pleiades centre are cluster members by Gaia DR3 parallax and proper motion, and what do their colour-magnitude diagram and parallax distance distribution show about the cluster's distance and main sequence?

**e2er's internal quality review:** 5.9 of 10 (weighted average): data 6.0, literature 5.7, methods 5.0, plausibility 7.0, writing 6.0

**Run:** governance=`full`, backend=`claude_code`, model=`haiku`

## Folder guide

- `paper/` — the manuscript (`paper.tex`, `abstract.tex`, `refs.bib`, compiled `paper.pdf`)
- `code/` — the estimation script (`code/scratch/` holds exploratory scripts and logs); `requirements.txt` pins the packages it runs with; `get_data.py` loads the inputs the folder does not ship
- `data/` — the study's data (`data.db`, SQLite) with the data summary and dictionary; `data_sources.json` records where each input came from and under which terms
- `results/` — estimation/robustness JSON + figures
- `design/` — research plan, identification strategy, econometric spec
- `reviews/` — the six reviewer reports and the combined score (`review_aggregation.json`)

## Reproduce

`reproduce.json` says how to run the study's code again. With e2er installed:

```bash
e2er reproduce .
```

This runs the code in a folder of its own, in a new environment with the pinned packages, and compares every result value and every table with the ones in this folder.

_Exported as `which-stars-within-3-degrees-of-the-pleiades-centre-are-clus-20261015-01` from e2er._
