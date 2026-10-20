<!-- e2er:github begin -->
# Spatial Clustering of GDP per Inhabitant across EU NUTS-2 Regions, 2024

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** How does GDP per capita in purchasing power standards vary across the EU's NUTS-2 regions in 2024, and how strongly do regions with high and low GDP per capita cluster in space?

**Dossier:** https://e2er.org/d/7ba4c56d920388be (every step of the run, the models, the data loads and the checks; id `sha256:7ba4c56d920388be61b10b2b34a318226736f09e10b04d2bc6f74f830d110485`)

**Made with:** e2er 0.16.1; template spatial-analysis; model sonnet (claude_code)

## Data

- **Eurostat database (dissemination API), European Commission, release 2026-02-10T11:00:00+0100**
  - Terms: Eurostat copyright notice (https://ec.europa.eu/eurostat/en/help/copyright-notice): "Reuse of statistical data, metadata, publications, and other dissemination tools published on this website for commercial or non-commercial purposes is authorised provided the source is acknowledged. The reuse policy of the European Commission is implemented by the Decision of 12 December 2011." "The following Eurostat data and documents may not be reused for commercial purposes, but non-commercial reuse is possible without restriction: Data identified as belonging to sources other than Eurostat. […] Data for countries other than: Member States of the European Union (EU); Member States of the European Free Trade Association (EFTA); official EU acceding and candidate countries." "When reuse involves translations of publications or modifications to the data or text, this must be stated clearly to the end user of the information. A disclaimer regarding the non-responsibility of Eurostat shall be included."
  - Full terms: https://ec.europa.eu/eurostat/en/help/copyright-notice
  - Cite: Eurostat, Gross domestic product (GDP) at current market prices by NUTS 2 region (nama_10r_2gdp). Source: https://doi.org/10.2908/NAMA_10R_2GDP, 2026-10-14. Customised version: Source: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10r_2gdp?lang=en&unit=PPS_EU27_2020_HAB&geoLevel=nuts2&sinceTimePeriod=2015&untilTimePeriod=2024, 2026-10-14.
- **GISCO geographical data (NUTS regions, countries), Eurostat, release NUTS 2024**
  - Terms: GISCO download terms (https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units): "The Commission agrees to grant the non-exclusive and non-transferable right to use and process the Eurostat/GISCO geographical data downloaded from this page (the 'data'). The permission to use the data is granted on condition that: the data will not be used for commercial purposes the source will be acknowledged. A copyright notice, as specified below, must be visible on any printed or electronic publication using the data downloaded from this page." Notice: © EuroGeographics for the administrative boundaries.
  - Full terms: https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units
  - Cite: Eurostat, GISCO. Territorial units for statistics (NUTS), boundaries. European Commission. https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics. © EuroGeographics for the administrative boundaries.
- **Eurostat database (dissemination API), European Commission, release 2026-08-28T23:00:00+0200**
  - Terms: Eurostat copyright notice (https://ec.europa.eu/eurostat/en/help/copyright-notice): "Reuse of statistical data, metadata, publications, and other dissemination tools published on this website for commercial or non-commercial purposes is authorised provided the source is acknowledged. The reuse policy of the European Commission is implemented by the Decision of 12 December 2011." "The following Eurostat data and documents may not be reused for commercial purposes, but non-commercial reuse is possible without restriction: Data identified as belonging to sources other than Eurostat. […] Data for countries other than: Member States of the European Union (EU); Member States of the European Free Trade Association (EFTA); official EU acceding and candidate countries." "When reuse involves translations of publications or modifications to the data or text, this must be stated clearly to the end user of the information. A disclaimer regarding the non-responsibility of Eurostat shall be included."
  - Full terms: https://ec.europa.eu/eurostat/en/help/copyright-notice
  - Cite: Eurostat, Population on 1 January by age, sex and NUTS 2 region (demo_r_d2jan). Source: https://doi.org/10.2908/DEMO_R_D2JAN, 2026-10-14. Customised version: Source: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_r_d2jan?lang=en&sex=T&age=TOTAL&geoLevel=nuts2&sinceTimePeriod=2024&untilTimePeriod=2024, 2026-10-14.

## Files left out

These files of the study are not in this folder:

- `data/data.db`: the terms of Eurostat GISCO (GISCO) do not allow passing the data on; `e2er reproduce` loads the tables gdp_pps_nuts2, nuts2_boundaries, pop_nuts2 again from the sources with code/get_data.py; builds the tables gdp_pps_sample again with code/scratch/build_data.py.
- `results/figure_spec.json`: built from Eurostat GISCO (GISCO) data and holds them row by row (an array of 236 values at figures[4].y); its terms do not allow passing them on; `e2er reproduce` writes it again with code/run_estimation.py, a step of the rerun.
- `results/moran_scatter_data.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (236 rows); its terms do not allow passing them on; `e2er reproduce` writes it again with code/run_estimation.py, a step of the rerun.
- `results/spatial_units.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (236 rows); its terms do not allow passing them on; `e2er reproduce` builds it again with code/scratch/build_data.py from the data it loads again.
- `results/spatial_units_all244.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (244 rows); its terms do not allow passing them on; `e2er reproduce` builds it again with code/scratch/build_data.py from the data it loads again.
- `results/spatial_weights.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (1,039 rows); its terms do not allow passing them on; `e2er reproduce` builds it again with code/scratch/build_data.py from the data it loads again.
- `results/spatial_weights_invdist.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (55,460 rows); its terms do not allow passing them on; `e2er reproduce` writes it again with code/run_estimation.py, a step of the rerun.
- `results/spatial_weights_knn5.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (1,180 rows); its terms do not allow passing them on; `e2er reproduce` builds it again with code/scratch/build_data.py from the data it loads again.
- `results/spatial_weights_knn5_all244.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (1,220 rows); its terms do not allow passing them on; `e2er reproduce` builds it again with code/scratch/build_data.py from the data it loads again.
- `results/spatial_weights_knn8.csv`: built from Eurostat GISCO (GISCO) data and holds them row by row (1,888 rows); its terms do not allow passing them on; `e2er reproduce` writes it again with code/run_estimation.py, a step of the rerun.

`e2er reproduce .` runs the study's steps again in a copy of this folder, getting each of these files as its line says, and compares the results with the published ones. `e2er-package.json` lists every file here with its SHA-256 and what was left out.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# How does GDP per capita in purchasing power standards vary across the EU's NU...

**Research question:** How does GDP per capita in purchasing power standards vary across the EU's NUTS-2 regions in 2024, and how strongly do regions with high and low GDP per capita cluster in space?

**e2er's internal quality review:** 5.9 of 10 (weighted average): data 5.5, methods 6.0, plausibility 6.0, technical 5.5, writing 6.5

**Run:** governance=`full`, backend=`claude_code`, model=`sonnet`

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

_Exported as `how-does-gdp-per-capita-in-purchasing-power-standards-vary-a-20261015-01` from e2er._
