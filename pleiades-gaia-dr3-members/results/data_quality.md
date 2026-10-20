# Data quality

Written by e2er's data check from data.db and data_dictionary.json, before the analysis. A column may miss up to 5% of its values without a note.

## gaia_dr3

- Rows: 14066
- Duplicate rows on the key (source_id): 0
- Coverage of parallax: 2.000156849807191 to 74.98865311008939 (declared 2.0002 to None)

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| source_id | INTEGER | none | 0 | 0.0% |  |
| ra | REAL | deg | 0 | 0.0% |  |
| dec | REAL | deg | 0 | 0.0% |  |
| dist_deg | REAL | deg | 0 | 0.0% |  |
| parallax | REAL | mas | 0 | 0.0% |  |
| parallax_error | REAL | mas | 0 | 0.0% |  |
| parallax_over_error | REAL | none | 0 | 0.0% |  |
| pmra | REAL | mas/yr | 0 | 0.0% |  |
| pmra_error | REAL | mas/yr | 0 | 0.0% |  |
| pmdec | REAL | mas/yr | 0 | 0.0% |  |
| pmdec_error | REAL | mas/yr | 0 | 0.0% |  |
| ruwe | REAL | none | 0 | 0.0% |  |
| astrometric_params_solved | INTEGER | none | 0 | 0.0% |  |
| visibility_periods_used | INTEGER | count | 0 | 0.0% |  |
| phot_g_mean_mag | REAL | mag | 2 | 0.0% |  |
| phot_g_mean_flux_over_error | REAL | none | 2 | 0.0% |  |
| phot_bp_mean_mag | REAL | mag | 169 | 1.2% |  |
| phot_rp_mean_mag | REAL | mag | 167 | 1.2% |  |
| bp_rp | REAL | mag | 169 | 1.2% |  |

source_id, missing values: never missing

ra, missing values: never missing for a Gaia source

dec, missing values: never missing for a Gaia source

dist_deg, missing values: never missing

parallax, missing values: never missing in this extract (the parallax > 2 condition drops rows without one)

parallax_error, missing values: never missing in this extract (same rows as parallax)

parallax_over_error, missing values: never missing in this extract (same rows as parallax)

pmra, missing values: null only for 2-parameter solutions, which have no parallax and so are not in this extract

pmra_error, missing values: missing together with pmra

pmdec, missing values: null only for 2-parameter solutions, which have no parallax and so are not in this extract

pmdec_error, missing values: missing together with pmdec

ruwe, missing values: null only for 2-parameter solutions, not in this extract; kept as null, not filled; the analysis reports the RUWE < 1.4 cut separately

astrometric_params_solved, missing values: never missing

visibility_periods_used, missing values: never missing

phot_g_mean_mag, missing values: missing only for sources without photometry; not expected in the extract

phot_g_mean_flux_over_error, missing values: missing together with G magnitude

phot_bp_mean_mag, missing values: missing for sources without BP photometry, mostly faint or crowded sources; the CMD uses only rows with bp_rp

phot_rp_mean_mag, missing values: missing for sources without RP photometry; same rows as phot_bp_mean_mag

bp_rp, missing values: missing for sources without BP and RP photometry; the CMD shows only rows with bp_rp, and the count dropped is reported
