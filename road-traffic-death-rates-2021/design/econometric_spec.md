# Analysis specification: estimated road traffic death rates, 2021 cross-section

## Design

This is a descriptive cross-sectional study. It estimates no regression, no
effect and no causal parameter. The analysis reports the distribution of the
WHO-estimated road traffic death rate (GHO indicator RS_198, deaths per 100,000
population) across countries in 2021, its summary by WHO region, the countries
at the two extremes, and the association between the point estimate and the
width of its uncertainty interval, if the GHO bounds are available.

## Unit and sample

- Unit: country, one observation per ISO3 code, calendar year 2021.
- Source table: `who_rs198_2021` (raw GHO extract, all spatial types), filtered
  to `spatial_type = 'COUNTRY'`. The clean table `who_rs198_2021_clean` is the
  country-level series with ISO3, country name and WHO region attached.
- The sample-flow (raw rows, rows by spatial type, rows dropped by each filter,
  final N) is counted in SQL and reported in the output.
- Missing values: a country without a non-null `value` is excluded from every
  statistic and listed by name. Missing values are not imputed or coded as zero.

## Statistics (national distribution)

For the national distribution of `value` across analysed countries:
N, mean, standard deviation (sample, ddof = 1), minimum, 25th percentile,
median, 75th percentile, maximum. Quantiles use linear interpolation between
order statistics (numpy default, Hyndman & Fan type 7).

## Regional summary

For each WHO region (AFR, AMR, SEAR, EUR, EMR, WPR): number of countries,
mean, median, SD, min, max, and quartiles. The between-region share of variance
is the between-region sum of squares divided by the total sum of squares of
`value` across countries (the eta-squared of a one-way layout). This is a
description of how the variance is partitioned, not a test or an effect.

## Rankings

The ten highest and ten lowest countries by `value`, with ISO3, name, WHO region
and value. Ties are listed in full at the cut-off and the cut-off is stated.

## Associations

- Rank correlation (Spearman's rho) between the point estimate `value` and the
  uncertainty width `high - low`, computed only if the GHO `low` and `high`
  bounds are present for enough countries. If they are absent, the statistic is
  reported as null with the reason. No association is interpreted causally.

## Robustness and checks

- Plausibility: values outside [0, 50] deaths per 100,000 are flagged and
  reported; they are not dropped silently.
- Duplicates: one row per ISO3 code. Duplicate rows are counted and resolved by
  keeping the first occurrence in source order, with the count reported.
- Regional mapping: each country maps to exactly one WHO region; unmapped rows
  are counted and listed.
- Sensitivity: the national distribution is reported with and without the
  extreme tails (5th and 95th percentile statistics) so the reader can see how
  much the extremes drive the spread.

## Outputs

- `estimation_results.json` in the descriptive results schema
  (`result_kind = "descriptive"`), with `statistics`, `distributions`,
  `associations`, `groups` and `figures`.
- `figure_spec.json` holds one histogram of the national distribution,
  `fig_death_rate_hist.pdf`, sourced from `distributions.death_rate.bins` so it
  shows the counts the results report. `estimation_results.json` lists it in
  `figures`.

## Realized numbers

Computed by `run_estimation.py` (run with `e2er-run`) from the warehouse tables;
all values are in `estimation_results.json`.

- Sample flow: 204 raw rows; 197 COUNTRY rows; 2 dropped for no numeric value
  (HKG and MAC, whose `value_text` reads 0.0 but whose numeric value is null;
  both are associate members, not Member States, and are not imputed); 195
  analysed. No duplicate ISO3 codes, no unmapped regions, no value outside
  [0, 50], and no disagreement between the clean and raw tables.
- National distribution (N = 195): mean 13.29, median 12.30, SD 7.78, min 0.0
  (MCO, NIU), 25th percentile 7.25, 75th percentile 18.10, max 37.4.
- Between-region share of variance (eta-squared, WHO region): 0.391.
- Ten highest: Guinea, Libya, Haiti, Guinea-Bissau, Syria, Zimbabwe, Yemen,
  Comoros, Kenya, Nepal. Ten lowest: Monaco, Niue, Maldives, Norway, Malta,
  Singapore, Sweden, Denmark, Switzerland, United Kingdom.
- Rank correlation of the point estimate with interval width: not computed.
  The warehouse holds no GHO `low` or `high` bounds for any country, so the
  association is reported as null with that reason.
