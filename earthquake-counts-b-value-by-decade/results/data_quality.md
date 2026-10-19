# Data quality

Written by e2er's data check from data.db and data_dictionary.json, before the analysis. A column may miss up to 5% of its values without a note.

## usgs_raw_1976_1985

- Rows: 37121
- Duplicate rows on the key (id): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 1976-01-01T00:04:05.400Z to 1985-12-31T22:56:33.100Z |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units (scale given by magType) | 0 | 0.0% |  |
| magType | TEXT | none | 1 | 0.0% |  |
| nst | REAL |  | 36802 | 99.1% |  |
| gap | REAL |  | 36803 | 99.1% |  |
| dmin | REAL |  | 36872 | 99.3% |  |
| rms | REAL |  | 17635 | 47.5% |  |
| net | TEXT | none | 0 | 0.0% |  |
| id | TEXT | none | 0 | 0.0% |  |
| updated | TEXT |  | 0 | 0.0% |  |
| place | TEXT |  | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| horizontalError | REAL |  | 36820 | 99.2% |  |
| depthError | REAL |  | 28429 | 76.6% |  |
| magError | REAL |  | 36841 | 99.2% |  |
| magNst | REAL |  | 19128 | 51.5% |  |
| status | TEXT | none | 0 | 0.0% |  |
| locationSource | TEXT |  | 0 | 0.0% |  |
| magSource | TEXT |  | 0 | 0.0% |  |

## usgs_raw_1986_1995

- Rows: 42573
- Duplicate rows on the key (id): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 1986-01-01T04:37:24.880Z to 1995-12-31T22:42:33.550Z |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units (scale given by magType) | 0 | 0.0% |  |
| magType | TEXT | none | 0 | 0.0% |  |
| nst | REAL |  | 42275 | 99.3% |  |
| gap | REAL |  | 42274 | 99.3% |  |
| dmin | REAL |  | 42444 | 99.7% |  |
| rms | REAL |  | 221 | 0.5% |  |
| net | TEXT | none | 0 | 0.0% |  |
| id | TEXT | none | 0 | 0.0% |  |
| updated | TEXT |  | 0 | 0.0% |  |
| place | TEXT |  | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| horizontalError | REAL |  | 42397 | 99.6% |  |
| depthError | REAL |  | 27781 | 65.2% |  |
| magError | REAL |  | 42524 | 99.9% |  |
| magNst | REAL |  | 8182 | 19.2% |  |
| status | TEXT | none | 0 | 0.0% |  |
| locationSource | TEXT |  | 0 | 0.0% |  |
| magSource | TEXT |  | 0 | 0.0% |  |

## usgs_raw_1996_2005

- Rows: 50984
- Duplicate rows on the key (id): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 1996-01-01T01:34:16.000Z to 2005-12-31T19:08:45.530Z |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units (scale given by magType) | 0 | 0.0% |  |
| magType | TEXT | none | 0 | 0.0% |  |
| nst | REAL |  | 18882 | 37.0% |  |
| gap | REAL |  | 32417 | 63.6% |  |
| dmin | REAL |  | 50892 | 99.8% |  |
| rms | REAL |  | 1091 | 2.1% |  |
| net | TEXT | none | 0 | 0.0% |  |
| id | TEXT | none | 0 | 0.0% |  |
| updated | TEXT |  | 0 | 0.0% |  |
| place | TEXT |  | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| horizontalError | REAL |  | 50836 | 99.7% |  |
| depthError | REAL |  | 40037 | 78.5% |  |
| magError | REAL |  | 50939 | 99.9% |  |
| magNst | REAL |  | 12577 | 24.7% |  |
| status | TEXT | none | 0 | 0.0% |  |
| locationSource | TEXT |  | 0 | 0.0% |  |
| magSource | TEXT |  | 0 | 0.0% |  |

## usgs_raw_2006_2015

- Rows: 73394
- Duplicate rows on the key (id): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 2006-01-01T03:21:39.210Z to 2015-12-31T23:39:28.940Z |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units (scale given by magType) | 0 | 0.0% |  |
| magType | TEXT | none | 0 | 0.0% |  |
| nst | REAL |  | 18950 | 25.8% |  |
| gap | REAL |  | 1409 | 1.9% |  |
| dmin | REAL |  | 55708 | 75.9% |  |
| rms | REAL |  | 3839 | 5.2% |  |
| net | TEXT | none | 0 | 0.0% |  |
| id | TEXT | none | 0 | 0.0% |  |
| updated | TEXT |  | 0 | 0.0% |  |
| place | TEXT |  | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| horizontalError | REAL |  | 63198 | 86.1% |  |
| depthError | REAL |  | 30361 | 41.4% |  |
| magError | REAL |  | 56171 | 76.5% |  |
| magNst | REAL |  | 18439 | 25.1% |  |
| status | TEXT | none | 0 | 0.0% |  |
| locationSource | TEXT |  | 0 | 0.0% |  |
| magSource | TEXT |  | 0 | 0.0% |  |

## usgs_raw_2016_2025

- Rows: 74436
- Duplicate rows on the key (id): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 2016-01-01T02:00:39.950Z to 2025-12-31T23:04:28.213Z |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units (scale given by magType) | 0 | 0.0% |  |
| magType | TEXT | none | 0 | 0.0% |  |
| nst | REAL |  | 46579 | 62.6% |  |
| gap | REAL |  | 525 | 0.7% |  |
| dmin | REAL |  | 559 | 0.8% |  |
| rms | REAL |  | 109 | 0.1% |  |
| net | TEXT | none | 0 | 0.0% |  |
| id | TEXT | none | 0 | 0.0% |  |
| updated | TEXT |  | 0 | 0.0% |  |
| place | TEXT |  | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| horizontalError | REAL |  | 484 | 0.7% |  |
| depthError | REAL |  | 0 | 0.0% |  |
| magError | REAL |  | 1610 | 2.2% |  |
| magNst | REAL |  | 1536 | 2.1% |  |
| status | TEXT | none | 0 | 0.0% |  |
| locationSource | TEXT |  | 0 | 0.0% |  |
| magSource | TEXT |  | 0 | 0.0% |  |

## eq_clean_m45

- Rows: 277946
- Duplicate rows on the key (id): 0
- Coverage of year: 1976 to 2025 (declared 1976 to 2025)

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| id | TEXT | none | 0 | 0.0% |  |
| time | TEXT | UTC, ISO 8601 | 0 | 0.0% | 1976-01-01T00:04:05.400Z to 2025-12-31T23:04:28.213Z |
| year | INTEGER | calendar year (UTC) | 0 | 0.0% | 1976 to 2025 |
| latitude | REAL | degrees | 0 | 0.0% |  |
| longitude | REAL | degrees | 0 | 0.0% |  |
| depth | REAL | km | 0 | 0.0% |  |
| mag | REAL | magnitude units | 0 | 0.0% |  |
| magType | TEXT | none | 1 | 0.0% |  |
| mag_class | TEXT | none | 0 | 0.0% |  |
| net | TEXT | none | 0 | 0.0% |  |
| type | TEXT | none | 0 | 0.0% |  |
| status | TEXT |  | 0 | 0.0% |  |

## eq_annual_counts

- Rows: 50
- Duplicate rows on the key (year): 0
- Coverage of year: 1976 to 2025 (declared 1976 to 2025)

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| year | INTEGER | calendar year (UTC) | 0 | 0.0% | 1976 to 2025 |
| n_m45 | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50 | INTEGER | none (count) | 0 | 0.0% |  |
| n_m55 | INTEGER | none (count) | 0 | 0.0% |  |
| n_m60 | INTEGER | none (count) | 0 | 0.0% |  |
| n_m70 | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50_mw | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50_mb | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50_ms | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50_other | INTEGER | none (count) | 0 | 0.0% |  |
| n_m50_shallow | INTEGER | none (count) | 0 | 0.0% |  |
| max_mag | REAL | magnitude units | 0 | 0.0% |  |

## eq_bvalue_windows

- Rows: 5
- Duplicate rows on the key (window): 0

| Column | Type | Unit | Missing | Share | Range |
|---|---|---|---:|---:|---|
| window | TEXT | years, e.g. 1976-1985 | 0 | 0.0% |  |
| start_year | INTEGER | calendar year | 0 | 0.0% |  |
| end_year | INTEGER | calendar year | 0 | 0.0% |  |
| window_type | TEXT | none | 0 | 0.0% |  |
| n_total | INTEGER | none (count) | 0 | 0.0% |  |
