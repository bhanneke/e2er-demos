# Data summary: WHO estimated road traffic death rate (RS_198), 2021

## Design (written before any data were loaded or analysed)

### Data source

- Source: WHO Global Health Observatory (GHO) OData API, indicator `RS_198`
  ("Estimated road traffic death rate"), year 2021, all locations.
- Unit: deaths per 100,000 population. The unit stays per 100,000 throughout.
- Load command (declared in `data_dictionary.json`):
  `e2er-data who_gho data --indicator RS_198 --start 2021 --end 2021 --table who_rs198_2021`
- Tables declared: `who_rs198_2021` (main, one row per location), `country_names`
  (Natural Earth 50m, ISO3 name lookup), `who_region_lookup` (six WHO regions).
- Terms: WHO data, reuse for public health purposes; the study does not ship GHO
  data in the replication package and loads them again. GHO citation
  `WHO_GHO` will be added on the first load.
- Age standardisation: the GHO response carries no age-standardisation field. The
  paper will state which version is used once the metadata check is done.
- The values are WHO model estimates, not vital registration counts.

### Intended sample construction (raw N -> filters -> final N)

Planned steps, to be filled with realized counts:

1. Raw rows returned for RS_198, 2021 (all `spatial_type`).
2. Keep `spatial_type = 'COUNTRY'` (drop REGION and GLOBAL aggregate rows).
3. Drop duplicate `location` rows for 2021 (a documented rule; none expected).
4. Drop rows with missing `value` (not imputed; counted and listed by name).
5. Join country name from `country_names` on ISO3; list unmatched codes.
6. Final country-level analysis sample (N countries).

### Data-quality checks planned (the gate)

- Units: `value` in 0 to 50 deaths per 100,000; out-of-range values flagged, not dropped silently.
- Duplicates: one row per ISO3 code for 2021.
- Missingness: count by column and by WHO region; names of countries without a value.
- Region mapping: every country maps to exactly one WHO region (`parent_location`),
  and the country codes agree with the `who_region_lookup` table.
- Uncertainty bounds `low` and `high`: share non-null reported; if WHO publishes none
  for RS_198, the bound columns are dropped from the analysis and this is stated.

### Variable definitions

- `location`: ISO3 code (key with `year`).
- `value`: WHO point estimate of the road traffic death rate, per 100,000.
- `parent_location`: WHO region name of the country.
- `low`, `high`: lower and upper uncertainty bounds, if published.

## Realized numbers

### Tables in data.db (actual row counts)

- `who_rs198_2021`: 204 rows (raw load, 2021, indicator RS_198; record `updated` 2024-04-15). Loaded with `e2er-data who_gho data --indicator RS_198 --start 2021 --end 2021 --table who_rs198_2021`. Not overwritten.
- `who_rs198_2021_clean`: 195 rows (analysis sample, derived by `clean_rs198.py`).
- `who_region_lookup`: 6 rows (AFR, AMR, EMR, EUR, SEAR, WPR), derived from the REGION rows of the same load.
- `country_names`: 242 rows (Natural Earth 50m, ISO3 join key).
- A table `road_deaths_2021` (204 rows) from an earlier import is in data.db. It has the same content, is not a declared table, and is not used.

### Sample flow

| Step | Rows | Dropped |
|---|---|---|
| Raw rows, RS_198, 2021 (`who_rs198_2021`) | 204 | 0 |
| Keep `spatial_type = 'COUNTRY'` (drop 6 REGION rows and 1 GLOBAL row) | 197 | 7 |
| Drop rows with no `value` (HKG, MAC; no parent region) | 195 | 2 |
| Final analysis sample (`who_rs198_2021_clean`) | 195 | 0 |

Missing values were dropped, not coded zero or imputed. HKG and MAC are excluded because WHO publishes no 2021 estimate for them. The other countries with a value are kept without change.

### Data-quality report

- **Units.** All 197 country values lie between 0 and 50 deaths per 100,000 population (raw range 0.0 to 37.4). No row fails the unit check. The GHO response carries no unit field; the unit is taken from the declared dictionary entry and the GHO indicator metadata.
- **Duplicates.** No duplicate (location, year) rows among the country rows. The check passes.
- **Zero values.** Two countries report 0.0: Monaco (MCO) and Niue (NIU). Both are kept and flagged. Both are very small populations, where a zero in one year is plausible.
- **Missingness by column (COUNTRY rows, n = 197).** `value`: 2 missing. `parent_location`: 2 missing (HKG, MAC). `low`: 197 missing. `high`: 197 missing.
- **Missingness by WHO region (COUNTRY rows).** Africa 47 of 47 with a value; Americas 36 of 36; Eastern Mediterranean 22 of 22; Europe 53 of 53; South-East Asia 9 of 9; Western Pacific 28 of 28; no region 2 of 2 without a value (HKG, MAC).
- **Uncertainty bounds.** The API returned no `low` or `high` for any row. The bounds are dropped from the analysis, and the paper does not report intervals. Whether WHO publishes bounds for RS_198 at all is not confirmed from the API; the paper should say so.
- **Country codes and names.** All 197 COUNTRY codes join to `country_names` on ISO3 (`iso_a3_eh` or `adm0_a3`), each matching exactly one name. No code is unmatched.
- **Region mapping.** Each analysis country's `parent_location` maps to one of the six region codes (Africa to AFR, Americas to AMR, South-East Asia to SEAR, Europe to EUR, Eastern Mediterranean to EMR, Western Pacific to WPR). The codes from the countries equal the codes of the six REGION rows. Every country maps to exactly one region.
- **Region lookup source check.** The six codes and names come from the REGION rows and the `parent_location` text of this load. They were not checked against an external WHO list in this run; the paper should do that before naming the regions.
- **Aggregates.** The REGION values (AFR 19.4, AMR 14.1, EMR 16.4, EUR 6.7, SEAR 16.1, WPR 15.2) and the GLOBAL value (15.0) are kept in the raw table and not used in the country analysis. Their weighting method is not stated in the response; they are not recomputed here.

### Counts by WHO region (analysis sample, n = 195)

AFR 47; AMR 36; EMR 22; EUR 53; SEAR 9; WPR 28.

### Age standardisation

The GHO response carries no age-standardisation field. The paper must not describe the series as a crude rate until the metadata is checked.

### Queries used for provenance

- `e2er-data query tables`
- `SELECT spatial_type, COUNT(*), COUNT(value), COUNT(DISTINCT location) FROM who_rs198_2021 GROUP BY spatial_type`
- `SELECT COUNT(low), COUNT(high), COUNT(comments) FROM who_rs198_2021`
- `SELECT parent_location, COUNT(*), COUNT(value) FROM who_rs198_2021 WHERE spatial_type='COUNTRY' GROUP BY parent_location`
- `SELECT COUNT(*), COUNT(DISTINCT adm0_a3) FROM country_names`
- The cleaning, checks and table writes are in `clean_rs198.py`, run with `e2er-run`.

### Excluded from this stage

No estimation: no means, medians, quantiles, regressions, tests or figures. Those belong to the analysis step.
