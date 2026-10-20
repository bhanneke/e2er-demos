# Data Summary

Script: `build_panel.py` (reads data.db only). Sidecars: `summary_statistics.json`, `figure_spec.json`. No treatment effects or regressions were estimated.

## Treatment dates (revised 2026-10-13)
`fee_abolition_dates` (49 rows, data/fee_abolition_years.csv) now holds researcher-supplied first years for eight countries. The researcher checked them against published abstracts (OpenAlex, 2026-10-13). They have `verification_status = 'published source'`, and the new column `source_doi` records the DOI or reference:

| iso3 | first_year | source_doi / reference | note |
|---|---|---|---|
| MWI | 1994 | doi:10.1080/03050060902921003 (Chimombo 2009, Compare) | |
| UGA | 1997 | doi:10.1111/rode.12725 (Kan and Klasen 2020) | |
| TZA | 2002 | Lindsjo 2017, Int. J. Educational Development (no DOI recorded) | first fee-free school year, January 2002; `alt_year` = 2001 (PEDP declared) |
| KEN | 2003 | Oketch and Somerset 2010, CREATE Pathways to Access 37 (no DOI) | |
| GHA | 2005 | doi:10.20448/journal.522.2017.31.53.63 (Pajibo and Tamanja 2017) | capitation grant |
| LSO | 2000 | doi:10.1080/09751122.2013.11890101 | phased from grade 1 (`abolition_scope`) |
| RWA | 2003 | doi:10.1155/2012/396019 | |
| ZMB | 2002 | 2020 concept paper, no DOI | confidence low (`confidence` column) |

The other 41 countries keep `first_year` empty and `verification_status = 'unverified'`. They are comparison units not known to have abolished fees, not verified never-abolishers. Columns of the table: iso3, country, first_year, alt_year, abolition_scope (`unknown` where not stated), verification_status, source_doi, confidence, provisional_first_year (now empty everywhere), notes.

## Panel end rule
`wb_primary_enrolment` ends in 2010 (the last cohort, 2005, plus five years), so abolitions after the last cohort do not enter the comparison group. The table has 1,519 country-years (49 economies, 1980-2010). The descriptive window is 1985-2010. The rule is applied in `build_panel.py` (`END = 2010`). The raw tables `wdi_primary_enrolment` and `wdi_controls` still run to 2018 and are not overwritten.

## Tables loaded (WDI via `e2er-data worldbank`, CC BY 4.0, long format; actual rows in data.db)
- wdi_primary_enrolment: 9,555 rows, 1980-2018, 49 economies. Indicators: SE.PRM.ENRR, ENRR.MA, ENRR.FE, SE.PRM.NENR, SE.PRM.CMPT.ZS.
- wdi_controls: 7,644 rows, 1980-2018, 49 economies. **Deviation:** DT.ODA.ODAT.PC.CD (aid per capita) was dropped because the World Bank metadata endpoint returned non-JSON on two attempts. The table holds SP.POP.TOTL, NY.GDP.PCAP.KD, SP.URB.TOTL.IN.ZS and SH.DYN.MORT only.
- Derived (raw tables not overwritten): wb_primary_enrolment (1,519 rows, 1980-2010), fee_abolition_dates (49), ger_cohort_means (177), ger_event_time_means (15).

## Sample flow (GER; source: summary_statistics.json#sample_flow)
1,911 country-years (49 x 39, 1980-2018) -> 1,519 after ending the panel in 2010 (392 dropped) -> 1,274 in 1985-2010 (245 dropped) -> 1,006 with non-null GER (268 dropped, no imputation). Final descriptive sample: 1,006 observations, 47 countries (summary_statistics.json#n_observations). The panel is unbalanced. Treatment-related exclusions (abolition before 1985, too few pre-period observations, partial or reintroduced abolition) are left to the estimation stage.

## Missingness (share non-null, country-years 1985-2010; see summary_statistics.json#missingness)
GER 79.0% (80.4% 1985-94, 76.9% 1995-2004, 79.9% 2005-10); male/female GER 76.9%; NER 46.8% (36.5% before 1995); completion 56.4%; GDP per capita 95.6%; population, urban share and under-5 mortality 100%. Four countries have no GER observation before 1995. The median country has 24 GER observations. There are 61 gaps in country GER series (non-consecutive years).

## Breaks and outliers
- Flagged (GER > 150 or < 10), kept: 5 country-years: MWI 1995 (152.6) and RWA 2007-2010 (154.7-156.6). Listed in data/ger_outliers.csv.
- Year-on-year GER changes above 20 points between consecutive years: 9 cases (data/ger_jumps.csv): BDI 2006, COG 1999/2000, ERI 1992, MWI 1995, RWA 2000, STP 1999, UGA 1997, ZAF 1989. The MWI 1995 and UGA 1997 jumps coincide with the abolition years. Others look like UIS revisions or denominator breaks, which affects any GER-based inference.

## Raw descriptives by cohort (illustrative; not effects)
Mean GER before vs. from first_year, observed years 1985-2010 (pre-years / post-years): MWI 72.4 -> 135.4 (9/15); UGA 71.0 -> 125.9 (12/14); LSO 101.0 -> 120.5 (15/11); TZA 68.6 -> 102.6 (17/9); KEN 100.5 -> 105.0 (16/7); RWA 83.4 -> 145.3 (14/8); ZMB 89.7 -> 108.4 (14/8, low confidence); GHA 72.5 -> 94.8 (19/5). These are raw means with no comparison group. Event-time means (t = -6..8) are in `ger_event_time_means` and fig_ger_event_time.pdf; composition changes across t. Cohort series are in fig_ger_cohort_trends.pdf (group "undated comparison" holds the other countries; it is not a verified never-abolisher group).

## Next steps for the econometrics stage
Use not-yet-treated and undated comparison units with this caveat; run robustness with TZA at 2001 (`alt_year`) and without ZMB; treat LSO as phased; treat NER-based results as a reduced sample; handle GER breaks and the RWA/MWI outliers with the winsorized and log specifications.
