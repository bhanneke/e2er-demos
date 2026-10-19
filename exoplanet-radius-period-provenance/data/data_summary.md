# Data Summary

## Source
NASA Exoplanet Archive, Planetary Systems Composite Parameters (`pscomppars`, DOI 10.26133/NEA13), loaded on 2026-10-13 with `e2er-data exoplanets planets` into `data.db` (also `data/planets.csv`). One row per confirmed planet; each column holds the archive's preferred value, so radius, mass and period of one planet can come from different papers. The archive has no releases; all counts refer to this load. Citations: Christiansen et al. (2025) and the table DOI. Acknowledgement text is in `data_dictionary.json`.

## Declared and derived tables
- `planets` (raw, not modified): 6,445 rows, disc_year 1992 to 2026, 21 columns.
- `planets_classified` (derived by `replication/analysis_prep.py`; adds `radius_group`, limit-flag indicators, `in_rp_sample`, `log10_rade`, `log10_orbper`): 6,445 rows.

> Source: summary_statistics.json#sample_flow

## Sample construction
| Step | N remaining | Dropped |
|---|---|---|
| Raw rows in `planets` | 6,445 | 0 |
| Remove duplicate `pl_name` (COUNT(*) = COUNT(DISTINCT pl_name) = 6,445) | 6,445 | 0 |
| `pl_rade` not missing | 6,395 | 50 |
| `pl_orbper` not missing | 6,045 | 350 |
| `pl_rade > 0` and `pl_orbper > 0`: radius-period sample | 6,045 | 0 |

Missing values are dropped from the radius-period sample, never filled. Planets without a radius or period are counted by group below. `pl_controv_flag` is not loaded, so controversial planets are not excluded. There is no `ps` default-solution table (its single `pl_refname` per solution cannot be classified by the CALCULATED_VALUE rule), no reference-level hand coding and no manual validation sample.

## Radius provenance (primary rule)
`calculated` = `pl_rade` not null and `pl_rade_reflink` contains `CALCULATED_VALUE` (archive label; mass-radius relation of Chen and Kipping 2017). Otherwise measured: `measured_transiting` if `tran_flag = 1`, `measured_non_transiting` if `tran_flag = 0` (not described as measured from a transit). `no_radius` if `pl_rade` is null.

| Group | All planets | In radius-period sample | Missing period (not in sample) |
|---|---|---|---|
| calculated | 1,537 | 1,215 | 322 |
| measured_transiting | 4,810 | 4,810 | 0 |
| measured_non_transiting | 48 | 20 | 28 |
| no_radius | 50 | 0 | 50 |

Cross-tabulation with `tran_flag`: all 1,537 calculated and all 48 measured_non_transiting have `tran_flag = 0`; all 4,810 measured_transiting have `tran_flag = 1`; of the 50 no_radius planets, 49 have `tran_flag = 0` and 1 has `tran_flag = 1`. The probe reproduces: 1,537 calculated, 0 with `tran_flag = 1`, among 1,634 planets with `tran_flag = 0`. The non-transiting planets with a radius not marked calculated number 48, not about 97: the 1,634 non-transiting planets split into 1,537 calculated, 48 measured and 49 without radius (1,537 + 48 + 49 = 1,634).

By discovery method (all planets): calculated: Radial Velocity 1,133, Microlensing 292, Imaging 52, Transit Timing Variations 25, Eclipse Timing Variations 15, Pulsar Timing 6, Astrometry 6, Orbital Brightness Modulation 3, Transit 2, Pulsation Timing Variations 2, Disk Kinematics 1. Measured_transiting: Transit 4,778, Radial Velocity 28, Transit Timing Variations 3, Orbital Brightness Modulation 1. Measured_non_transiting: Imaging 41, Radial Velocity 5, Orbital Brightness Modulation 2 (plus 20 of 48 in the sample, rest lack a period). Full table: `summary_statistics.json#crosstab_group_by_method`. Mass provenance of the calculated group: Msini 876, Mass 648, Msin(i)/sin(i) 13; none lacks a mass. The 876 Msini cases are radii computed from a minimum mass.

## Data quality
- Duplicates: none (6,445 distinct `pl_name`).
- Missing: `pl_orbper` 353 of 6,445 (5.5%; microlensing and imaging mostly), `pl_rade` 50 (0.8%), `pl_bmasse` 31 (0.5%), `st_teff` 307 (4.8%), `sy_dist` 28 (0.4%). `pl_orbperlim` is empty in the same 353 rows and `pl_radelim` in the same 50 rows as the value; no empty flag is treated as zero for a row that has a value.
- `pl_orbper_reflink` is empty in exactly the 353 rows where `pl_orbper` is empty (280 microlensing, 71 imaging, 1 pulsar timing, 1 disk kinematics): no period is published, so no reference exists. It is a provenance label, not analysed; period statistics use the 6,092 planets with a period.
- Limit flags: 5 radii and 6 periods carry a nonzero flag; they stay in the sample (flag columns kept for sensitivity).
- Units: `pl_rade / pl_radj` has median 11.209 (min 10.83, max 11.54; 11 rows outside 11.0 to 11.4, rounding of small radii in `pl_radj`); `pl_bmasse / pl_bmassj` median 317.83. Periods in days, radii in Earth radii.
- Plausibility: 6 radii above 25 Earth radii (kept, flagged), none at or below 0 or below 0.3; no period below 0.09 d; 5 periods above 10^6 d (kept, flagged); no mass above 13,000 Earth masses.

## Descriptive statistics of the radius-period sample (N = 6,045)
Group sizes: calculated 1,215; measured_transiting 4,810; measured_non_transiting 20. Medians: radius 12.6 Earth radii (calculated), 2.46 (measured_transiting), 13.0 (measured_non_transiting); period 358.6 d, 7.97 d and 15,958 d. The calculated group is dominated by radial-velocity and microlensing discoveries, the measured_transiting group by transit surveys; the groups differ in method, so group differences are not physical differences. Full quantiles and 0.25-dex histogram bins (counts add to group n) are in `summary_statistics.json` (`by_group`, `distributions`). Quantiles are type 7 (linear interpolation). No estimation was done.

## Selection and limits
Transits favour short periods and large planets; radial velocity favours massive planets; imaging favours wide, young, massive ones; microlensing planets mostly lack periods. The table describes the confirmed-planet catalogue, not the planet population.

## Figures prepared (figure_spec.json)
Radius against period for all (scatter by group), two-panel by group, marginal histograms of the two main groups, and radius against mass for the calculated group. Each names its data.db table or `summary_statistics.json` bins as source.

## Figure verification
`replication/chk_fig.py` re-reads every figure's values and compares them with the source. Scatter panels match `planets_classified` row for row: all groups 6,045 points (calculated 1,215; measured_transiting 4,810 in the two-panel figure); mass-radius diagnostic 1,537 points. Histogram bins equal those in `summary_statistics.json` and their counts add to 1,215 and 4,810 for radius and for period. Axes: period in days and radius in Earth radii (mass in Earth masses), log scales.

### Re-check against `estimation_results.json` (2026-10-13)
- Sample: `estimation_results.json#sample` gives 6,445 raw, 50 without radius, 353 without period, 6,045 in the radius-period sample; the scatter figures plot 6,045 points (groups: measured_transiting 4,810; calculated 1,215; measured_non_transiting 20), equal to `groups.*.n`. The mass-radius diagnostic plots 1,537 calculated planets, equal to the calculated count in `radius_group_by_tran_flag_all6445` (calculated | tran_flag=0: 1,537).
- Mismatch found: the marginal histograms were drawn from 0.25-dex bins in `summary_statistics.json` (10 radius bins, 39 period bins), while `estimation_results.json` reports coarser bins (`radius_bins_*`: 7 bins; `period_bins_*`: 9 bins) and fine log10 bins (`log10_radius_fine_*`: 0.1 dex, 22 bins; `log10_period_fine_*`: 0.25 dex, 39 bins). Totals agreed (1,215 and 4,810) but bin edges and radius counts did not.
- Fix: the four histogram panels now use the `log10_*_fine_*` bins from `estimation_results.json` (log10 axes), with `source.results` pointing there. Counts add to 1,215 (calculated) and 4,810 (measured_transiting) for radius and period. Nothing was estimated; group labels equal `radius_group` values.
