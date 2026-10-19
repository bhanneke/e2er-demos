# Data summary

## Source
USGS ComCat (ANSS Comprehensive Catalog), FDSN event service, doi 10.5066/F7MS3QZH (`\cite{USGS_ComCat}`). Worldwide, 1976-01-01 to 2025-12-31 (UTC), magnitude >= 4.5, loaded in five decade requests (half-open windows) so that each stays under the service's window-split limit. No `--event-type` filter in the raw loads, so non-earthquake events are counted before removal. The Global CMT catalogue is not loaded (unavailable to this study). ComCat events are revised after review; the load reflects the catalogue as of the load date, and 2025 events may still change (reviewed share in 2025: 100%; lowest reviewed share in any year: 99.5%).

## Declared tables and actual row counts (as held in data.db)
- usgs_raw_1976_1985: 37,121 rows (first event 1976-01-01)
- usgs_raw_1986_1995: 42,573 rows
- usgs_raw_1996_2005: 50,984 rows
- usgs_raw_2006_2015: 73,394 rows
- usgs_raw_2016_2025: 74,436 rows (last event 2025-12-31T23:04:28Z)
- eq_clean_m45: 277,946 rows (cleaned catalogue, M >= 4.5)
- eq_annual_counts: 50 rows (1976-2025; counts at M >= 4.5, 5.0, 5.5, 6.0, 7.0, by magnitude class, shallow, maximum magnitude)
- eq_bvalue_windows: 5 rows (the five decades with n_total only: 36,781; 42,441; 50,975; 73,390; 74,359; Mc-dependent columns were removed from the table because Mc and b are estimated in the analysis step, not stored by the data step)

Raw total: 278,508 rows.

## Sample flow (Source: summary_statistics.json#sample_flow)
| Step | N remaining | Dropped |
|---|---|---|
| Raw rows, five tables, M >= 4.5 | 278,508 | 0 |
| Drop repeated ids | 278,508 | 0 |
| Keep type == 'earthquake' | 277,947 | 561 |
| Drop null magnitude / mag < 4.5 | 277,946 | 1 |
| Origin time within 1976-2025 | 277,946 | 0 |

The 561 removed non-earthquake events: nuclear explosion 470 (329 in 1976-85, 130 in 1986-95, 6, 2, 3 in later decades), volcanic eruption 71 (all 2016-25), explosion 11, mine collapse 4, rock burst 3, landslide 2. One earthquake row had no usable magnitude at or above 4.5 and was dropped (listwise; nothing was imputed or coded zero).

## Cleaning rules (in order)
1. Raw rows per table. 2. Drop repeated ids (none found). 3. Keep type == 'earthquake'. 4. Drop null magnitude / mag < 4.5. 5. Origin time inside 1976-2025; year = UTC year. 6. magType lower-cased, no conversion between magnitude types; ComCat's preferred magnitude is used as published (one per event). Near-duplicates (within 16 s, 100 km and 0.5 magnitude units) are flagged, not removed: 211 pairs, of which 192 are us-us, 6 ci-ci, 6 ak-us, 4 ak-ak, 1 ci-us, 1 nc-nc and 1 nn-nn.

## Variables
mag (magnitude units; scale given by magType), magType, mag_class (mw_family: mw, mww, mwc, mwb, mwr, mwp; mb: mb, mb_lg; ms; ml_md; other; missing), depth (km), latitude/longitude (degrees), net, status (reviewed/automatic). Missing values after cleaning: magType 1 event (0.00036%); time, latitude, longitude, depth, mag, net none. Range checks: no latitude/longitude out of range, no magnitude above 10 (maximum 9.1); depth runs from -3.0 to 700.9 km, 128 events have negative depth (kept; ComCat reports depth relative to the geoid for some events; this affects no count at the 70 km shallow cut-off).

## Descriptive statistics (n = 277,946 events, M >= 4.5)
Magnitude: mean 4.870, SD 0.405, min 4.5, quartiles 4.6 / 4.8 / 5.0, max 9.1. Depth: mean 70.8 km, median 33.0 km, SD 117.1. Annual number of M >= 5 events (50 years, total 83,469): mean 1,669.4, SD 307.8, median 1,648.5, min 1,077 (1998), max 2,701 (2011).

By decade (annual M >= 5 counts):
| Decade | Events M>=4.5 | Events M>=5 | Mean/yr | SD | Min | Max | Mean/yr M>=6 |
|---|---|---|---|---|---|---|---|
| 1976-1985 | 36,781 | 15,959 | 1,595.9 | 187.9 | 1,259 | 1,790 | 106.4 |
| 1986-1995 | 42,441 | 16,174 | 1,617.4 | 93.1 | 1,495 | 1,757 | 153.7 |
| 1996-2005 | 50,975 | 13,906 | 1,390.6 | 227.5 | 1,077 | 1,844 | 145.3 |
| 2006-2015 | 73,390 | 19,928 | 1,992.8 | 371.4 | 1,571 | 2,701 | 164.5 |
| 2016-2025 | 74,359 | 17,502 | 1,750.2 | 251.2 | 1,450 | 2,227 | 133.2 |

The full annual M >= 5 table is eq_annual_counts (n_m50). Mean annual M >= 5.5 counts by decade: 396.1, 493.1, 484.4, 524.2, 458.3. The difference between the M >= 5 and M >= 5.5 counts is not a detection share.

## Magnitude-type mix by decade (share of events, Source: summary_statistics.json#magclass_share_by_decade_m45 and _m50)
Preferred-magnitude class, M >= 4.5: Mw family 4.5%, 18.4%, 23.1%, 21.1%, 18.3%; mb 88.6%, 77.6%, 74.6%, 77.6%, 81.3%; ms 5.8%, 2.7%, 0.8%, 0.04%, 0%; ml/md 1.1%, 1.2%, 1.4%, 0.9%, 0.5% (decades in order 1976-85 to 2016-25).
M >= 5 only: Mw family 10.3%, 48.0%, 76.6%, 63.4%, 58.6%; mb 77.5%, 47.6%, 22.0%, 36.2%, 41.0%; ms 11.6%, 3.8%, 1.0%, 0.1%, 0%. The preferred magnitude type therefore changes strongly over the 50 years; counts are not on one magnitude scale. Counts by type per decade (all magType values) are in summary_statistics.json#magtype_counts_by_decade.

## Limits
Aftershocks are kept and not removed. ComCat's preferred magnitude type mixes over time (mb dominating early, Mw family later). A catalogue of what ComCat records, not a complete census: completeness below about M5 is not assumed and is the subject of the analysis step. No estimation (b-values, Mc, trends, tests) is done in this step.

## Figures (figure_spec.json)
Three figures are specified, each re-readable from data.db or the sidecar: fig_annual_counts_m5.pdf (M>=5 and M>=6 per year, eq_annual_counts.n_m50 and n_m60), fig_annual_counts_m7.pdf (M>=7 per year, n_m70; separate panel because of the scale) and fig_magtype_mix.pdf (Mw-family share of M>=5 events by decade, summary_statistics.json#magclass_share_by_decade_m50).
Not produced: frequency-magnitude plots per decade with Mc marked, b-value by decade with confidence intervals, and Mc over time. `estimation_results.json` did not exist when this step ran (the econometrics step had not run), and this step does not estimate. These figures must be added from `estimation_results.json` once it exists; no placeholder values were written. Rolling-window b-values are dropped by the researcher's scope.

## Coverage declaration
Each decade table is loaded for its full period. The first recorded event of a decade falls a few hours after midnight (e.g. 1976-01-01T00:04:05Z, 1986-01-01T04:37:24Z) because the catalogue holds no earlier event. The dictionary now declares coverage on `time` as full UTC timestamps (T00:00:00Z on the first day to T23:59:59Z on the last day). No rows were added or removed.
