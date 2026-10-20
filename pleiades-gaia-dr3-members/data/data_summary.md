# Data summary: Gaia DR3 extract around the Pleiades

## Source and retrieval

- Table `gaia_dr3` in `data.db`, loaded from `gaiadr3.gaia_source` (Gaia DR3) with the ADQL recorded in `data_dictionary.json` (`load_command`). Raw CSV: `data/gaia_dr3.csv`.
- Cone: CIRCLE('ICRS', 56.75, 24.12, 3 deg). Centre RA 56.75°, Dec +24.12°. This is a catalogue approximation of Melotte 22 / M45 and is not yet checked against a cited literature position.
- Pre-filter in the ADQL: `parallax > 2` mas and `parallax_over_error > 5`. The full cone holds 255,553 DR3 sources (count on 2026-10-13); the anonymous archive returns at most 50,000 rows, so the cone cannot be pulled whole. The field background in the CMD is therefore limited to parallax > 2 mas (closer than 500 pc). Every cut of the sensitivity grid lies inside this extract.
- Retrieval date 2026-10-13. Terms: Gaia data under CC BY-NC 3.0 IGO, credit to ESA, Gaia DPAC.

## Tables used by the figures

- `gaia_dr3` (14,066 rows): the raw extract, loaded by the data step.
- `gaia_clean` (9,970 rows): the quality sample, re-loaded into `data.db` by `load_members.py` from `gaia_dr3` with the base quality cut (`astrometric_params_solved` in {31, 95}, `ruwe < 1.4`, `parallax_over_error > 10`, duplicate `source_id` removed). It holds every column of `gaia_dr3` plus `cmd_group`, which is `Member` for the stars of the existing membership definition and `Field` for the rest. The same rows are written to `data/gaia_clean.csv`.
- `pleiades_members` (1,112 rows): the members of the existing membership definition (`run_estimation.py`, functions `quality`, `pm_seed`, `membership`, `clip_stats`, copied unchanged into `load_members.py`), with `source_id`, `bp_rp`, `phot_g_mean_mag`, `parallax`, `pmra`, `pmdec`.

The membership selection is not changed here. The parallax window (3 sigma of the clipped parallax around the clipped centre) and the proper-motion radius (5 mas/yr around the clipped proper-motion centre) are those of `estimation_results.json`, and the sensitivity grid is not re-run.

## Sample construction

The data step applies the base-specification cuts in this order, logging each row count (`prepare_gaia.py`, log in `data/gaia_clean_steps.json`):

| Step | Filter | Rows kept | Rows dropped |
|---|---|---|---|
| 0 | raw extract (`gaia_dr3`) | 14,066 | 0 |
| 1 | remove duplicate `source_id` | 14,066 | 0 |
| 2 | `astrometric_params_solved` in {31, 95}; non-null parallax and proper motion | 14,066 | 0 |
| 3 | `ruwe < 1.4` | 12,722 | 1,344 |
| 4 | `parallax_over_error > 10` (quality sample, `gaia_clean`) | 9,970 | 2,752 |
| 5 | membership: parallax window and proper-motion radius (`pleiades_members`) | 1,112 members | 8,858 field stars |

Membership is an estimation-stage output. The step 5 count is taken from the existing definition, and the load confirms it by recomputation (see the check below).

Missing values are not filled. Rows with null `bp_rp` stay in `gaia_clean` and `pleiades_members`; the CMDs use only the rows that have `bp_rp`. Rows are dropped by the cuts above, never coded to zero.

## Variables and units

- `ra`, `dec`: degrees (ICRS, epoch 2016.0).
- `parallax`: mas, uncorrected for the zero point (Lindegren et al. 2021 correction is a sensitivity check only).
- Distance: 1000 / parallax pc, uncorrected, and labelled as such wherever it appears.
- `pmra`, `pmdec`: mas/yr; `pmra` includes cos δ.
- `phot_g_mean_mag`, `phot_bp_mean_mag`, `phot_rp_mean_mag`, `bp_rp`: mag (Vega), not extinction-corrected.
- `ruwe`, `parallax_over_error`: unitless. `astrometric_params_solved`: 3 = two-parameter (position only), 31 = five-parameter, 95 = six-parameter.

## Data check

- Duplicates: `source_id` is the key; 0 duplicate rows in the raw extract (14,066 distinct of 14,066).
- Coverage: the parallax lower bound is open (`parallax > 2`); the smallest clean parallax is 2.00016 mas.
- Missing values, raw extract (`summary_statistics.json#missing_values_raw`): `phot_g_mean_mag` 2, `phot_g_mean_flux_over_error` 2, `phot_bp_mean_mag` 169, `phot_rp_mean_mag` 167, `bp_rp` 169 (1.2%). Astrometry, `ruwe` and `parallax_over_error` have no missing values.
- Missing values, clean sample (`summary_statistics.json#missing_values_clean`): `bp_rp` 107 rows null, not filled; `phot_g_mean_mag` 1 row null.
- Units: `parallax` minimum 2.00016 mas; `parallax_over_error` minimum 10.00045, consistent with the cut.
- `astrometric_params_solved` in the clean sample: 8,031 with 31 (five-parameter), 1,939 with 95 (six-parameter).

## Realised sample

- 9,970 quality sources (`summary_statistics.json#n_observations`), 1,112 of them members (`pleiades_members`, `gaia_clean` rows with `cmd_group = 'Member'`).
- `bp_rp` present for 9,863 quality sources (`summary_statistics.json#cmd_rows_with_bp_rp`): 1,095 members and 8,768 field stars (see the member check below).
- Parallax (mas), quality sample: 2.00 to 69.51, median 3.26 (`summary_statistics.json#ranges.parallax_mas`).

## Member and field CMD check (this load)

Counts are re-read by `load_members.py` from `data.db` and written to `summary_statistics.json#members`:

- Members: 1,112 (recomputed; equal to `estimation_results.json#membership.stage_counts.pm_radius`).
- Members with `bp_rp` and G: 1,095 (`summary_statistics.json#members.cmd_rows_members`); 17 members have no `bp_rp` and are left out of the CMD.
- Field stars with `bp_rp` and G: 8,768 (`summary_statistics.json#members.cmd_rows_field`). Members and field together give the 9,863 quality rows with `bp_rp`.
- Brightest member G is 5.20 (`summary_statistics.json#members.phot_g_min`). The cluster's brightest named B stars, several magnitudes brighter, are not among the members, a gap at the bright end. The cause is not identified here.
- Member `bp_rp` range: −0.40 to 4.22 mag (`summary_statistics.json#members.bp_rp_min`, `bp_rp_max`).

## Figures

- `fig_cmd.pdf`: the members and the field of the quality sample as two groups (`Member`: 1,095 points of the 1,112 members with `bp_rp`; `Field`: 8,768 points of the 8,858 quality-cut stars that are not members, with `bp_rp`). Both series are read from `gaia_clean` by `cmd_group`, in one scatter source (`groups` = `cmd_group`, condition `cmd_group IN ('Member','Field') AND bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL`). The figure check re-reads the points from `data.db`; the spec's 9,863 points match the table row for row.
- `fig_cmd_members.pdf` carries the same two groups and is still in the spec; it duplicates `fig_cmd.pdf` and is named by `make_figures.py`, `run_estimation.py` and `estimation_results.json`, so it is left for the orchestrator to remove or keep.
- Plotting convention: the figure spec has no option to invert an axis and the renderer does not invert `y`, so the vertical axis is `phot_g_mean_mag` with larger values higher (fainter stars at the top). The field series is drawn in the renderer's default colour, not grey. The caption states the axis as drawn. The conventional CMD inverts the axis; this is not done here.

## Flags for the next stage (not corrected here)

1. `data_dictionary.json` does not yet declare `gaia_clean` and `pleiades_members`; the data architect should add them with their definitions before the data contract is re-run.
2. `estimation_results.json#figures` lists only `fig_vpd_pm.pdf` and `fig_cmd.pdf`; it does not name `fig_distance_hist.pdf` or `fig_cmd_members.pdf`. This file is estimation output and is not changed here.
3. The member count and the grid come from the estimation stage. No membership or grid value is re-estimated by this load.

All numbers above are in `summary_statistics.json`, and the step log is in `data/gaia_clean_steps.json`. The cleaned table is `data/gaia_clean.csv` and the member table is `pleiades_members` in `data.db`.
