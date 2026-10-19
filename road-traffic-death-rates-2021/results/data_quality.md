# Data quality

Written by e2er's data check from data.db and data_dictionary.json, before the analysis. A column may miss up to 5% of its values without a note.

## who_rs198_2021

- Rows: 204
- Duplicate rows on the key (location, year): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| indicator | TEXT |  | 0 | 0.0% |  |
| spatial_type | TEXT | none | 0 | 0.0% |  |
| location | TEXT | none | 0 | 0.0% |  |
| parent_location | TEXT | none | 9 | 4.4% |  |
| time_type | TEXT |  | 0 | 0.0% |  |
| year | INTEGER | year | 0 | 0.0% | 2021 to 2021 |
| period | TEXT |  | 0 | 0.0% | 2021 to 2021 |
| dim1_type | TEXT |  | 204 | 100.0% |  |
| dim1 | TEXT |  | 204 | 100.0% |  |
| dim2_type | TEXT |  | 204 | 100.0% |  |
| dim2 | TEXT |  | 204 | 100.0% |  |
| dim3_type | TEXT |  | 204 | 100.0% |  |
| dim3 | TEXT |  | 204 | 100.0% |  |
| value | REAL | deaths per 100,000 population | 2 | 1.0% |  |
| low | REAL | deaths per 100,000 population | 204 | 100.0% |  |
| high | REAL | deaths per 100,000 population | 204 | 100.0% |  |
| value_text | TEXT |  | 0 | 0.0% |  |
| comments | TEXT |  | 204 | 100.0% |  |
| updated | TEXT | none | 0 | 0.0% |  |

low, missing values: the GHO API returned no lower bound for the first rows checked (e.g. AFG, AGO, ALB); the share with a bound is reported, not assumed. Source check: confirm whether WHO publishes uncertainty bounds for RS_198 at all.

high, missing values: same as low: the first rows checked carry no upper bound. Source check: confirm whether WHO publishes uncertainty bounds for RS_198 at all.

## country_names

- Rows: 242
- Duplicate rows on the key (adm0_a3): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| adm0_a3 | TEXT | none | 0 | 0.0% |  |
| iso_a3_eh | TEXT | none | 0 | 0.0% |  |
| iso_a3 | TEXT |  | 0 | 0.0% |  |
| name | TEXT | none | 0 | 0.0% |  |
| name_long | TEXT | none | 0 | 0.0% |  |
| continent | TEXT |  | 0 | 0.0% |  |
| region_un | TEXT |  | 0 | 0.0% |  |
| subregion | TEXT |  | 0 | 0.0% |  |
| pop_est | REAL |  | 0 | 0.0% |  |
| geometry | TEXT |  | 0 | 0.0% |  |

## who_region_lookup

- Rows: 6
- Duplicate rows on the key (region_code): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| region_code | TEXT | none | 0 | 0.0% |  |
| region_name | TEXT | none | 0 | 0.0% |  |
| value | REAL | deaths per 100,000 population | 0 | 0.0% |  |

## Notes

- who_rs198_2021.low: 100% missing (the GHO API returned no lower bound for the first rows checked (e.g. AFG, AGO, ALB); the share with a bound is reported, not assumed. Source check: confirm whether WHO publishes uncertainty bounds for RS_198 at all.)
- who_rs198_2021.high: 100% missing (same as low: the first rows checked carry no upper bound. Source check: confirm whether WHO publishes uncertainty bounds for RS_198 at all.)
