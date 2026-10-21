<!-- e2er:github begin -->
# How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** How are confirmed exoplanets distributed in planet radius and orbital period, and how does that distribution change when radii measured from transits are separated from radii calculated from planet mass?

**Dossier:** https://e2er.org/d/3f3a95d2a49b0c71 (every step of the run, the models, the data loads and the checks; id `sha256:3f3a95d2a49b0c71e9445ca5c86f2088f5835c1ad3be7d762ea1c130faa1f621`)

**Made with:** e2er 0.16.0; template descriptive-study; model sonnet (claude_code)

## Data

- **NASA Exoplanet Archive (NASA Exoplanet Science Institute, IPAC/Caltech): Planetary Systems tables**
  - Terms: No licence stated. The acknowledgement page (https://exoplanetarchive.ipac.caltech.edu/docs/acknowledge.html) asks: "Please include the following standard acknowledgment in any published material that makes use of the NASA Exoplanet Archive's services. This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program." and "if you use data from a specific literature reference, please acknowledge that reference directly", and to "cite Christiansen et al. (2025)". The TAP page (https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html) asks: "If you use any of the following data sets for your research, please cite the archive's DOI for the data."
  - Full terms: https://exoplanetarchive.ipac.caltech.edu/docs/acknowledge.html
  - Cite: Christiansen, J. L., McElroy, D. L., Harbut, M., et al. (2025). The NASA Exoplanet Archive and Exoplanet Follow-up Observing Program: Data, Tools, and Usage. The Planetary Science Journal, 6(8), 186. https://doi.org/10.3847/PSJ/ade3c2. Data: NASA Exoplanet Science Institute (2020), Planetary Systems Composite Table, IPAC, https://doi.org/10.26133/NEA13, or Planetary Systems Table, https://doi.org/10.26133/NEA12. Acknowledgement: This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

## Files left out

None: every file of the study is in this folder.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# How are confirmed exoplanets distributed in planet radius and orbital period,...

**Research question:** How are confirmed exoplanets distributed in planet radius and orbital period, and how does that distribution change when radii measured from transits are separated from radii calculated from planet mass?

**e2er's internal quality review:** 5.9 of 10 (weighted average): data 6.5, literature 4.6, methods 6.0, plausibility 6.0, writing 6.0

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

_Exported as `how-are-confirmed-exoplanets-distributed-in-planet-radius-an-20261015-01` from e2er._
