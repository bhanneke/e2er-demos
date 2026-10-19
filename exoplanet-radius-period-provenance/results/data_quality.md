# Data quality

Written by e2er's data check from data.db and data_dictionary.json, before the analysis. A column may miss up to 5% of its values without a note.

## planets

- Rows: 6445
- Duplicate rows on the key (pl_name): 0
- Coverage of disc_year: 1992 to 2026 (declared 1992 to 2026)

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| pl_name | TEXT | none | 0 | 0.0% |  |
| hostname | TEXT | none | 0 | 0.0% |  |
| discoverymethod | TEXT | none | 0 | 0.0% |  |
| disc_year | INTEGER | year | 0 | 0.0% |  |
| pl_orbper | REAL | days | 353 | 5.5% |  |
| pl_orbperlim | INTEGER | none | 353 | 5.5% |  |
| pl_orbper_reflink | TEXT | none | 353 | 5.5% |  |
| pl_rade | REAL | Earth radii | 50 | 0.8% |  |
| pl_radelim | INTEGER | none | 50 | 0.8% |  |
| pl_rade_reflink | TEXT | none | 50 | 0.8% |  |
| pl_radj | REAL | Jupiter radii | 50 | 0.8% |  |
| pl_bmasse | REAL | Earth masses | 31 | 0.5% |  |
| pl_bmassj | REAL | Jupiter masses | 31 | 0.5% |  |
| pl_bmassprov | TEXT | none | 0 | 0.0% |  |
| pl_bmasse_reflink | TEXT | none | 0 | 0.0% |  |
| tran_flag | INTEGER | none | 0 | 0.0% |  |
| rv_flag | INTEGER | none | 0 | 0.0% |  |
| sy_snum | INTEGER | none | 0 | 0.0% |  |
| sy_pnum | INTEGER | none | 0 | 0.0% |  |
| st_teff | REAL | K | 307 | 4.8% |  |
| sy_dist | REAL | pc | 28 | 0.4% |  |

pl_orbper, missing values: a few planets (mostly imaged or microlensing) have no period; period statistics use rows with a value, share reported

pl_orbperlim, missing values: empty where the archive gives no flag; treated as 0 only after the count of empty cells is reported

pl_orbper_reflink, missing values: empty exactly where pl_orbper is empty (353 of 6,445 planets: 280 microlensing, 71 imaging, 1 pulsar timing, 1 disk kinematics), because no period has been published for them. The column is a provenance label only; it is not analysed. Period statistics use the planets with a period, with n and the share missing reported; nothing is filled in.

pl_rade, missing values: no radius for most radial-velocity-only, microlensing and astrometry planets; radius statistics use the planets with a radius, share reported

pl_radelim, missing values: empty where the archive gives no flag; rows with a limit flag are reported and handled as stated in the plan

pl_rade_reflink, missing values: empty exactly where pl_rade is empty

pl_radj, missing values: as pl_rade

pl_bmasse, missing values: no mass for most transit-only planets; mass statistics use the planets with a mass, share reported

pl_bmassj, missing values: as pl_bmasse

pl_bmassprov, missing values: empty where pl_bmasse is empty

pl_bmasse_reflink, missing values: empty where pl_bmasse is empty

st_teff, missing values: a few hosts (e.g. brown dwarfs, pulsars) lack a temperature; used only for host-type splits with rows that have a value

sy_dist, missing values: uses rows with a value

## Notes

- planets.pl_orbper: 5% missing (a few planets (mostly imaged or microlensing) have no period; period statistics use rows with a value, share reported)
- planets.pl_orbperlim: 5% missing (empty where the archive gives no flag; treated as 0 only after the count of empty cells is reported)
- planets.pl_orbper_reflink: 5% missing (empty exactly where pl_orbper is empty (353 of 6,445 planets: 280 microlensing, 71 imaging, 1 pulsar timing, 1 disk kinematics), because no period has been published for them. The column is a provenance label only; it is not analysed. Period statistics use the planets with a period, with n and the share missing reported; nothing is filled in.)
