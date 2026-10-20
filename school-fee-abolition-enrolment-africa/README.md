<!-- e2er:github begin -->
# Did Abolishing Primary-School Fees Raise Enrolment? Evidence from Staggered Reforms in Sub-Saharan Africa

> **Demonstration: published as is, not endorsed.** This study was produced with e2er as a demonstration or test run and is published as is. It is not presented as a research contribution, and its author does not vouch for its findings.

**Question:** Did abolishing primary-school fees in sub-Saharan African countries (staggered between the mid-1990s and the mid-2000s) raise gross primary enrolment? A difference-in-differences with World Bank enrolment data, comparing countries that abolished fees with countries that had not (yet) abolished them.

**Dossier:** https://e2er.org/d/984a090d8f324fe1 (every step of the run, the models, the data loads and the checks; id `sha256:984a090d8f324fe1a4355c95643417adbbcf997b476841604c37aaff97d884f5`)

**Made with:** e2er 0.16.0; template policy-evaluation; model sonnet (claude_code)

## Data

- **World Bank Open Data (Indicators API v2), The World Bank, release 2026-10-08**
  - Terms: CC BY 4.0 with the World Bank's additional terms (https://www.worldbank.org/ext/en/legal/terms-conditions/datasets): "Unless specifically labeled otherwise, these Datasets are provided to you under a Creative Commons Attribution 4.0 International License (CC BY 4.0)". "You agree to provide attribution to The World Bank and its data providers in the following format: The World Bank: Dataset name: Data source (if known)." "Some datasets and indicators are provided by third parties, and may not be redistributed or reused without the consent of the original data provider, or may be subject to terms and conditions that are different from those described above. Where applicable, these conditions are included in the dataset or indicator metadata."
  - Full terms: https://www.worldbank.org/ext/en/legal/terms-conditions/datasets
  - Cite: The World Bank: World Development Indicators: Data API, UN Educational, Scientific and Cultural Organization (UNESCO), uri: https://databrowser.uis.unesco.org/resources, note: The data are obtained through the UIS API. Detailed documentation is available at: https://api.uis.unesco.org/api/public/documentation/, publisher: UNESCO Institute for Statistics (UIS), type: Bulk file (csv), date accessed: 2026-03-19, date published: 2026-02; Stat Bulk Data Download Service, UN Educational, Scientific and Cultural Organization (UNESCO), uri: https://uis.unesco.org/bdds, publisher: UNESCO Institute for Statistics (UIS). World Bank Open Data, https://data.worldbank.org (last updated 2026-10-08). Licence: CC BY 4.0.
- **World Bank Open Data (Indicators API v2), The World Bank, release 2026-10-08**
  - Terms: CC BY 4.0 with the World Bank's additional terms (https://www.worldbank.org/ext/en/legal/terms-conditions/datasets): "Unless specifically labeled otherwise, these Datasets are provided to you under a Creative Commons Attribution 4.0 International License (CC BY 4.0)". "You agree to provide attribution to The World Bank and its data providers in the following format: The World Bank: Dataset name: Data source (if known)." "Some datasets and indicators are provided by third parties, and may not be redistributed or reused without the consent of the original data provider, or may be subject to terms and conditions that are different from those described above. Where applicable, these conditions are included in the dataset or indicator metadata."
  - Full terms: https://www.worldbank.org/ext/en/legal/terms-conditions/datasets
  - Cite: The World Bank: World Development Indicators: Country official statistics, National Statistical Organizations and/or Central Banks; National Accounts data files, Organisation for Economic Co-operation and Development (OECD); Staff estimates, World Bank (WB); UN Inter-agency Group for Child Mortality Estimation, UN Children's Fund (UNICEF), uri: www.childmortality.org, publisher: UNICEF, WHO, World Bank, United Nations Population Division; World Health Organization (WHO), uri: www.childmortality.org, note: UN Inter-agency Group for Child Mortality Estimation; World Bank (WB), uri: www.childmortality.org, note: UN Inter-agency Group for Child Mortality Estimation; United Nations (UN), uri: www.childmortality.org, note: UN Inter-agency Group for Child Mortality Estimation, publisher: UN Population Division; World Population Prospects, United Nations (UN), uri: https://population.un.org/wpp/, publisher: UN Population Division; Statistical databases and publications from national statistical offices, National Statistical Offices (NSOs), uri: https://unstats.un.org/home/nso_sites/, publisher: National Statistical Offices; Eurostat: Demographic Statistics, Eurostat (ESTAT), uri: https://ec.europa.eu/eurostat/data/database?node_code=earn_ses_monthly, publisher: Eurostat; Population and Vital Statistics Report (various years), United Nations (UN), uri: https://unstats.un.org, publisher: UN Statistics Division; World Urbanization Prospects, United Nations (UN), uri: https://population.un.org/wup/, note: United Nations Population Division's World Urbanization Prospects, National definitions, publisher: UN Population Division. World Bank Open Data, https://data.worldbank.org (last updated 2026-10-08). Licence: CC BY 4.0.

## Files left out

None: every file of the study is in this folder.

## Licence

No licence was set for the study's code and text when it was published. Without one, copyright applies: you may read the files, but reusing them needs the authors' permission. The data keep their sources' terms (above).

## Check it

`e2er verify .` checks every file against `provenance.json`; `e2er reproduce .` runs the study's code again (https://github.com/bhanneke/E2ER-project).
<!-- e2er:github end -->

---

# Did abolishing primary-school fees in sub-Saharan African countries (staggere...

**Research question:** Did abolishing primary-school fees in sub-Saharan African countries (staggered between the mid-1990s and the mid-2000s) raise gross primary enrolment? A difference-in-differences with World Bank enrolment data, comparing countries that abolished fees with countries that had not (yet) abolished them.

**e2er's internal quality review:** 4.9 of 10 (weighted average): data 5.0, identification 4.0, methods 5.0, technical 5.0, writing 6.0

**Run:** governance=`full`, backend=`claude_code`, model=`sonnet`

## Headline estimates

| term | estimate | p-value |
| --- | --- | --- |
| `att` | 22.04 | 0.000242 |

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

_Exported as `did-abolishing-primary-school-fees-in-sub-saharan-african-co-20261015-01` from e2er._
