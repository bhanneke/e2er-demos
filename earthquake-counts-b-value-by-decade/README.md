<!-- e2er:github begin -->
# How Has the Yearly Number of Magnitude 5 and Larger Earthquakes Changed, 1976–2025? Counts and the Stability of the Gutenberg–Richter $b$-Value Across Decades

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** How has the yearly number of magnitude 5 and larger earthquakes worldwide changed from 1976 to 2025, and is the Gutenberg–Richter b-value stable across decades once the catalogue's completeness magnitude is taken into account?

**Dossier:** https://e2er.org/d/3777eb6cfb5dfd27 (every step of the run, the models, the data loads and the checks; id `sha256:3777eb6cfb5dfd277b1ec6d9938bd8fd85b31c3b8bc1426ecc7135aea8ae0301`)

**Made with:** e2er 0.16.1; template descriptive-study; model sonnet (claude_code)

## Data

- **ANSS Comprehensive Earthquake Catalog (ComCat), U.S. Geological Survey**
  - Terms: U.S. public domain (https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits): "USGS-authored or produced data and information are considered to be in the U.S. Public Domain." USGS asks "that proper credit be given". Cite the catalogue: U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS) Comprehensive Catalog. U.S. Geological Survey. https://doi.org/10.5066/F7MS3QZH
  - Full terms: https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits
  - Cite: U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS) Comprehensive Catalog. U.S. Geological Survey. https://doi.org/10.5066/F7MS3QZH

## Files left out

None: every file of the study is in this folder.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# How has the yearly number of magnitude 5 and larger earthquakes worldwide cha...

**Research question:** How has the yearly number of magnitude 5 and larger earthquakes worldwide changed from 1976 to 2025, and is the Gutenberg–Richter b-value stable across decades once the catalogue's completeness magnitude is taken into account?

**e2er's internal quality review:** 5.8 of 10 (weighted average): data 6.0, literature 5.3, methods 5.0, plausibility 6.5, writing 6.0

**Run:** governance=`full`, backend=`claude_code`, model=`sonnet`

## Folder guide

- `paper/` — the manuscript (`paper.tex`, `abstract.tex`, `refs.bib`, compiled `paper.pdf`)
- `code/` — the estimation script (`code/scratch/` holds exploratory scripts and logs); `requirements.txt` pins the packages it runs with
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

_Exported as `how-has-the-yearly-number-of-magnitude-5-and-larger-earthqua-20261015-01` from e2er._
