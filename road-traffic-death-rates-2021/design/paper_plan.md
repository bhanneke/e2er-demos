# Paper plan: Estimated road traffic death rates across countries and WHO regions, 2021

Paper ID: 66f43096-d973-4dc0-afaa-d086434dd927
Methodology: empirical (descriptive data study)
Stage: idea

## 1. Research question

How do WHO-estimated road traffic death rates per 100,000 population (GHO indicator RS_198, "Estimated road traffic death rate") vary across countries and WHO regions in 2021?

The paper is descriptive. It reports the distribution of the rate across countries, summarises it by WHO region, ranks countries, and identifies the highest and lowest rates. It makes no causal claim. Where it describes associations between the rate and other measures, those are reported as correlations with explicit caveats and are not interpreted as effects.

## 2. Phenomenon and motivation

Road traffic deaths are a large cause of preventable mortality, and the rate differs several-fold between countries. The motivating puzzle is the size and persistence of the cross-country gap in 2021, a year in which the global picture was shaped by pandemic-era changes in traffic volumes. The paper asks how large the gap is, how it is structured by region, and which countries sit at the extremes. It does not ask why the gap exists.

## 3. Unit of analysis

- Unit: country, one observation per country in calendar year 2021.
- Sample period: 2021 only. No panel structure, no year-on-year comparison in the main text.
- Geography: WHO Member States with a published RS_198 estimate for 2021, grouped into the six WHO regions (AFR, AMR, SEAR, EUR, EMR, WPR).
- Measure: the RS_198 value as published by WHO (per 100,000 population). The data_architect must confirm from the GHO metadata whether the published series is age-standardised, and the paper must state which version is used. The unit stays per 100,000 population throughout.

## 4. Data

- Source: WHO Global Health Observatory API, indicator RS_198, year 2021, all countries.
- Supporting fields: country name, ISO3 code, WHO region, and the GHO low and high uncertainty bounds if the API returns them.
- Data availability: the Data Available field in the work order is empty. The data are not yet in the workspace. data_architect is responsible for pulling the series and writing a provenance note (query URL, retrieval date, record count).

## 5. Data check (before analysis)

data_quality checks, run after data_architect and data_analyst and before econometrics_specialist:

- Units: the value is in deaths per 100,000 population, with a plausible range (roughly 0 to 50). Any value outside that range is flagged and reported, not silently dropped.
- Duplicates: one row per ISO3 code for 2021. Duplicates are resolved by documented rule and the count is reported.
- Missing values: count of countries without an RS_198 value for 2021, with the names listed. Missing countries are not imputed. The paper reports N of countries analysed and N excluded.
- Regional mapping: every country with a value maps to exactly one WHO region. Unmapped countries are listed.
- Cross-check: the global and regional aggregates are compared against the figures in the WHO Global Status Report on Road Safety 2023 (the edition that reports 2021 estimates). Any discrepancy is reported with its likely cause, such as a different population weighting or a later data revision.

The check stops the run if units are wrong, duplicates remain, or the regional mapping is incomplete.

## 6. Descriptive outputs

All outputs are for 2021 and are reported with the number of countries (N) on which they are based.

1. Distribution: mean, median, standard deviation, min, max, interquartile range, and the 10th, 25th, 75th, and 90th percentiles across all countries. One histogram or density plot with a kernel density overlay.
2. Regional summary: for each WHO region, N, mean, median, SD, min, max, and the country with the minimum and maximum. Also a region-level population-weighted mean if population data are pulled from the same GHO source. If not, this is stated as unavailable. One box plot or strip plot by region.
3. Between- and within-region share: the share of total cross-country variance in the rate that lies between regions versus within regions. Reported as a descriptive decomposition, not as an inferential claim.
4. Rank ordering: a full ranked table of countries (rank, country, region, rate, and uncertainty bounds if available), delivered as an appendix table. The text reports the rank of notable countries only.
5. Top and bottom countries: the 10 highest and 10 lowest rates, with region and rate. Each listing is checked for data quality flags from step 5 before it is reported.
6. Association panel (optional, reported only if it adds to the description): pairwise correlations between RS_198 and a small number of GHO covariates that the work order approves, such as the regional grouping itself. Any such association is labelled "associated with" and the paper states explicitly that no effect is identified.

## 7. Contribution relative to existing presentations

The WHO Global Status Report on Road Safety presents the estimated rate by country, by region, and by income group, and it reports the global rate and trend. This paper does not replace that presentation. Its contribution is:

- A reproducible, code-level replication of the 2021 cross-country and regional distributions directly from the GHO API, with the full ranked table and the data-quality log published alongside it.
- Distributional detail that the report does not foreground: the full spread within each region, the share of variance that lies between versus within regions, and the uncertainty around the extremes.
- An explicit account of which countries drive the regional extremes, with a check on whether the extremes are sensitive to the data-quality exclusions.

The paper should not be framed as a new finding about road safety. It is a careful descriptive account of a published indicator, and it should say so.

## 8. What the paper does not do

- It makes no causal claim. No statement such as "X causes lower road deaths" or "region Y's rate is higher because of Z" appears in the text.
- It proposes no identification strategy and no theory model. identification_strategist and theory_specialist are not dispatched.
- It does not estimate a regression. econometrics_specialist writes estimation_results.json in the descriptive results schema, containing summary statistics and the rank table only.
- It does not analyse trends over years, since the unit is 2021 only.

## 9. Specialist sequence

1. data_architect: pulls RS_198 for 2021 from the GHO API, writes the provenance note, and records the age-standardisation status.
2. data_analyst: builds the country-year 2021 dataset, applies the documented cleaning rules, and assigns WHO regions.
3. Data check (data_quality): runs the checks in section 5. The run stops if they fail.
4. econometrics_specialist: computes the descriptive statistics, regional summaries, variance decomposition, rank table, and top and bottom lists. Writes estimation_results.json in the descriptive results schema.
5. Figure check (figure_data, run by data_analyst): re-reads the histogram, regional box plot, and any association panel against the summary tables. The run stops if a figure does not match its underlying data.
6. paper_drafter: drafts the paper from this plan, the cleaned data log, and estimation_results.json.
7. Review panel: literature_reviewer, writing_reviewer, data_reviewer, methods_reviewer, plausibility_reviewer.

## 10. Risks and open items

- Data not yet retrieved. Every number in the paper depends on step 1. If the API does not return a 2021 value for a country, that country is reported as missing.
- Age standardisation. If RS_198 is age-standardised, the paper must not describe it as a crude death rate. The wording is fixed after data_architect confirms the metadata.
- Estimate versus registration. The values are WHO model estimates, not vital registration counts. The paper must say so, and it must not present differences of a few units as meaningful without the uncertainty bounds.
- Cross-check mismatch with the Global Status Report. If the replicated aggregates differ from the report, the difference is explained in the data log before drafting, not smoothed over in the text.
- Regional population weights. Region-level weighted means need population data. If they are not available from the same source, the paper reports unweighted means and says so.
