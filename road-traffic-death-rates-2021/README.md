<!-- e2er:github begin -->
# Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** How do estimated road traffic death rates per 100,000 people vary across countries and WHO regions in 2021? A descriptive study with the WHO Global Health Observatory indicator RS_198.

**Dossier:** https://e2er.org/d/c655a736c75bf6bb (every step of the run, the models, the data loads and the checks; id `sha256:c655a736c75bf6bbca0227142bc52b9270b7ca1c5ee0f79fb91bd84d527b8e2a`)

**Made with:** e2er 0.16.0; template descriptive-study; model haiku (claude_code)

## Data

- **Global Health Observatory (GHO) data repository, World Health Organization, release 2024-04-15**
  - Terms: WHO, Terms and conditions of use for WHO data compilations, aggregations, evaluations and analyses (https://www.who.int/about/policies/publishing/data-policy/terms-and-conditions): "Licensed Use. Subject to these Terms and Conditions, WHO grants to you the royalty-free, worldwide, non-exclusive right to use, reproduce, extract, download, copy, distribute, display or include the Datasets and data contained therein in other products for public health purposes." "Any other alteration or modification of the Datasets (including abbreviations, additions, or deletions) may be made only with the prior written authorization of WHO." "You will not sell or otherwise transfer the Datasets and/or data contained therein to any third party, except within the Licensed Use." Attribution "in the following format: WHO, title of dataset, year, date of access, acknowledgement of the country or countries having provided the underlying data."
  - Full terms: https://www.who.int/about/policies/publishing/data-policy/terms-and-conditions
  - Cite: WHO, Global Health Observatory: Estimated road traffic death rate (per 100 000 population) (RS_198), 2026, accessed 2026-10-13. Underlying data provided by the countries concerned (all WHO Member States reporting it).
- **Natural Earth vector data: Admin 0 – Countries, release v5.1.2**
  - Terms: Public domain (https://www.naturalearthdata.com/about/terms-of-use/): "All versions of Natural Earth raster + vector map data found on this website are in the public domain. You may use the maps in any manner, including modifying the content and design, electronic dissemination, and offset printing. ... No permission is needed to use Natural Earth. Crediting the authors is unnecessary." Suggested credit: Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.
  - Full terms: https://www.naturalearthdata.com/about/terms-of-use/
  - Cite: Natural Earth (release v5.1.2). Admin 0 – Countries. https://www.naturalearthdata.com/. Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

## Files left out

These files of the study are not in this folder:

- `data/data.db`: the terms of the WHO Global Health Observatory (WHO GHO) do not allow passing the data on; `e2er reproduce` loads the tables country_names, road_deaths_2021, who_rs198_2021 again from the sources with code/get_data.py; builds the tables who_region_lookup, who_rs198_2021_clean again with code/scratch/clean_rs198.py.

`e2er reproduce .` runs the study's steps again in a copy of this folder, getting each of these files as its line says, and compares the results with the published ones. `e2er-package.json` lists every file here with its SHA-256 and what was left out.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# How do estimated road traffic death rates per 100,000 people vary across coun...

**Research question:** How do estimated road traffic death rates per 100,000 people vary across countries and WHO regions in 2021? A descriptive study with the WHO Global Health Observatory indicator RS_198.

**e2er's internal quality review:** 5.7 of 10 (weighted average): data 6.0, literature 5.1, methods 5.0, plausibility 6.0, writing 7.0

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

_Exported as `how-do-estimated-road-traffic-death-rates-per-100-000-people-20261015-01` from e2er._
