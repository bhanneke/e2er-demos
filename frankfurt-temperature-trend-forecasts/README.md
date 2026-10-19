<!-- e2er:github begin -->
# Warming and Forecast Skill in Monthly Temperature: Frankfurt am Main, 1981–2025

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** How has the monthly mean air temperature at 2 metres in Frankfurt am Main (NASA POWER, 50.11 N, 8.68 E) changed since 1981, and how well do seasonal forecasting models predict the next 36 months compared with a seasonal naive baseline?

**Dossier:** https://e2er.org/d/c985731bebd41662 (every step of the run, the models, the data loads and the checks; id `sha256:c985731bebd416627892828103bd10b1f5c56b65ab97a6b399f143696a425c80`)

**Made with:** e2er 0.16.0; template time-series-forecasting; model sonnet (claude_code)

## Data

- **NASA Prediction Of Worldwide Energy Resources (POWER), NASA Langley Research Center, release v2.10.0**
  - Terms: No licence stated by POWER; NASA's Earth science data use guidance (https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance): "Unless the content is marked with a use restriction or license, data provided from a NASA-led mission are licensed as Creative Commons Zero (CC0). While there are no restrictions on the use of these data, data users are very strongly urged to cite the data used in their work products." POWER's referencing guide (https://power.larc.nasa.gov/docs/referencing/): "When POWER data products are used in a publication include both POWER's Reference and POWER's Data Reference in any work product or publication" and "the Project requests notification if POWER data is transmitted to other researchers."
  - Full terms: https://power.larc.nasa.gov/docs/referencing/
  - Cite: NASA Langley Research Center (LaRC) POWER Project. Prediction Of Worldwide Energy Resources (POWER), https://power.larc.nasa.gov/. The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division. Data reference: The data was obtained from the POWER Monthly and Annual API version 2.10.0 on 2026/10/13.

## Files left out

None: every file of the study is in this folder.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# How has the monthly mean air temperature at 2 metres in Frankfurt am Main (NA...

**Research question:** How has the monthly mean air temperature at 2 metres in Frankfurt am Main (NASA POWER, 50.11 N, 8.68 E) changed since 1981, and how well do seasonal forecasting models predict the next 36 months compared with a seasonal naive baseline?

**e2er's internal quality review:** 5.9 of 10 (weighted average): data 6.5, literature 4.6, methods 6.0, plausibility 6.5, technical 6.0, writing 5.5

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

_Exported as `how-has-the-monthly-mean-air-temperature-at-2-metres-in-fran-20261015-01` from e2er._
