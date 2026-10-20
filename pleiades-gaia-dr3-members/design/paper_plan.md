# Paper plan: Pleiades membership and distance from Gaia DR3

Paper ID: 09bc8be0-20c4-4a5d-8241-282ccd2a45b1
Pipeline: descriptive-study · Methodology: empirical · Stage: idea

## 1. Research question

Which stars within 3 degrees of the Pleiades centre are cluster members by Gaia DR3 parallax and proper motion, and what do their colour-magnitude diagram (CMD) and parallax distance distribution show about the cluster's distance and main sequence?

Scope: descriptive only. No causal claim, no identification strategy, no regression. Theory and identification specialists are not dispatched.

## 2. Phenomenon and why it matters

The Pleiades is one of the nearest open clusters and a standard reference for the main sequence and distance scale. Gaia DR3 gives parallaxes and proper motions for most of its bright members, so a simple, transparent selection should recover a clean member sample and a distance. The paper asks whether a plain cut on astrometry reproduces the cluster's known distance and main-sequence locus. Its value is as a transparent, replicable reference exercise, not as a new physical result.

## 3. Data

**No data is present locally.** `data/` is empty and `.study_inputs.json` has `data.chosen: false` with no files. The `literature/` corpus in this workspace covers unrelated topics (crypto markets, AI governance) and must not be cited for this paper.

Required source: Gaia DR3 `gaiadr3.gaia_source` table, via the ESA Gaia archive (TAP/ADQL or the web query form).

Query specification (data_architect to finalise and record in the data-plan file):

- Cone: centre RA ≈ 56.75°, Dec ≈ +24.12° (Pleiades/Melotte 22 centre; confirm against a literature value and record the exact value used), radius 3.0°.
- Columns: `source_id, ra, dec, parallax, parallax_error, parallax_over_error, pmra, pmra_error, pmdec, pmdec_error, ruwe, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp, astrometric_params_solved, phot_g_mean_flux_over_error, visibility_periods_used`.
- Pull the full cone, not a pre-filtered subset. All cuts are applied afterwards in the analysis, so the raw pull is archived for replication.
- Save the raw extract to `data/` as CSV plus the exact ADQL text and the retrieval date (2026-10-13 or later).

Units: `ra`, `dec`, `pmra`, `pmdec` are in degrees and mas/yr (pmra already includes cos δ); `parallax` in mas; magnitudes in mag. Distance in pc is 1000/parallax (uncorrected) and must be labelled as such.

Known caveats to state in the paper:

- Parallax zero-point (Lindegren et al. 2021) is about −0.02 to −0.04 mas for these magnitudes. The main analysis uses the uncorrected parallax; the corrected parallax is a sensitivity row only.
- Photometry is not extinction-corrected. Pleiades reddening is small (E(B−V) about 0.04 mag, to be confirmed from a cited source). The CMD is shown uncorrected, with the offset noted.
- Bright-star and crowding effects matter at G < 6 and in the cluster core. Report counts with and without a G > 6 floor as a sensitivity row.

## 4. Membership criteria (to be tested, fixed before looking at results)

Base specification (pre-declared, reported first):

1. **Quality cuts:** `ruwe < 1.4`; `parallax_over_error > 10`; `astrometric_params_solved` ∈ {31, 95} (5- or 6-parameter solutions); non-null astrometry.
2. **Parallax window:** `|parallax − π₀| < 3σ_π`, with π₀ the iteratively clipped median of the quality-cut sample (about 7.3 mas expected; recompute, do not hard-code), σ_π taken as the clipped standard deviation. Fallback window to test: fixed ±1.0 mas around π₀.
3. **Proper-motion radius:** distance in proper-motion space from the clipped cluster mean (μ₀, expected near pmra ≈ +20, pmdec ≈ −45 mas/yr; recompute) less than **5 mas/yr** (`sqrt((pmra−μα₀)² + (pmdec−μδ₀)²) < r`).

Sensitivity grid (descriptive re-counts only, no estimation):

| Dimension | Values |
|---|---|
| Proper-motion radius r | 3, 5, 7, 10 mas/yr |
| Parallax window | 2σ, 3σ, fixed ±1 mas |
| Quality cut RUWE | < 1.2, < 1.4 |
| parallax_over_error | > 5, > 10 |
| Zero-point correction | none (base), Lindegren 2021 |

The base specification is the headline result. The other rows are reported in full, whether or not they agree with the base, so no specification is chosen after seeing the answer.

## 5. Descriptive outputs

1. **Member count table:** number of members per specification in the grid, with the total number of sources entering the cuts at each stage (cone, quality cut, parallax window, PM radius). Written to a table file.
2. **CMD:** `bp_rp` on the x-axis, `phot_g_mean_mag` inverted on the y-axis, for members (base spec) and for all cone sources passing quality cuts as a grey background. State the uncorrected-extinction caveat in the caption.
3. **Parallax histogram:** members' parallax with the base window marked; a second panel shows distance (1000/π, pc) with median and interquartile range.
4. **Main-sequence summary:** median `bp_rp` in magnitude bins (for example 1-mag bins from G ≈ 6 to G ≈ 18) for members, giving a locus table; the brightest-member and faintest-member G values; and the apparent turn-off region if present.
5. **Distance summary:** median, IQR, and the 16th–84th percentile range of 1000/π for members; a distance-modulus value (5 log10(d) − 5) with the same statistics. Give the median parallax with its bootstrap-free standard error (σ/√n) as a descriptive dispersion, not as an inference claim.

Only summary statistics, counts, percentiles, and medians are computed. No fitting of isochrones, no regression, no tests of significance, no model-based distance estimate.

## 6. What counts as a clear result

The result is **clear** if all of the following hold for the base specification:

- Member count is stable across the sensitivity grid: the base count lies within ±10% of the median count across the grid, and no single row changes the count by more than 25%.
- The member parallax histogram is unimodal, and its mode and median agree within 0.1 mas.
- The median distance from members, 1000/π, lies within 125–145 pc. This range is a reference band, not a test; the paper reports where the median falls relative to the literature value it cites.
- The CMD shows a continuous main-sequence locus for members over at least 8 magnitudes in G, with no member locus that is visibly displaced from the field.

The result is **ambiguous** if the count varies by more than 25% across the grid, or if the parallax histogram is bimodal (possible contamination or a second group), or if the CMD locus is broken. In that case the paper says so and reports the spread, without choosing the best-looking row.

The result is **null / unexpected** if the base specification yields fewer than 100 members, or if the median distance falls outside 110–160 pc. In that case the paper reports the failure and checks the data pull and the cone centre before any interpretation.

## 7. Pipeline sequence and hand-offs

1. **data_architect:** write `data/` pull instructions and the exact ADQL; retrieve the cone; record the query, date, and row count. Hand-off: raw CSV in `data/`.
2. **data_analyst:** data check (units, duplicate `source_id`, missing values in astrometry and photometry, `bp_rp` nulls, RUWE and flux-error distributions). Record every cleaning decision. The data-quality check runs here and stops the run on failure.
3. **econometrics_specialist:** compute the descriptive outputs in section 5 and the grid in section 4. Write `estimation_results.json` in the descriptive-results schema. No regression.
4. **data_analyst:** re-read figures and tables against the schema before the draft (figure check). Stops the run on failure.
5. **paper_drafter:** draft the paper following this plan. Report all grid rows. Do not describe the base spec as the only result.
6. **Review panel:** literature_reviewer (verify Gaia DR3 and Pleiades references, see section 8), writing_reviewer, data_reviewer, methods_reviewer, plausibility_reviewer (check the distance and PM values against the literature).

Not dispatched: identification_strategist, theory_specialist.

## 8. Literature to cite (to be verified by literature_reviewer)

The local corpus does not cover this topic, so each reference must be sourced and checked before use. Candidates:

- Gaia Collaboration, Vallenari et al. (2023), *Gaia Data Release 3: Summary of the content and survey properties*, A&A.
- Lindegren et al. (2021), astrometric solution (Gaia EDR3), A&A, and the parallax zero-point paper, A&A.
- Lindegren et al. (2018 / 2021) on RUWE and the astrometric-quality cuts used here.
- Gaia Collaboration, Babusiaux et al. (2018), the Gaia DR2 Hertzsprung–Russell diagram, A&A, including the Pleiades as a reference cluster.
- Lodieu et al. (2019) and Melis et al. (2014) on the Pleiades distance and kinematics.

Each citation must be checked against the source before entry in `literature.bib`. Claims about the Pleiades distance and proper motion in the paper are compared with these values, not taken from memory.

## 9. Replication

Store with the paper: the exact ADQL, retrieval date, the cone centre used, the quality-cut code, the sensitivity-grid table, and the descriptive-results JSON. Another researcher should be able to re-run the pull and reproduce every count in section 5 from these files alone.
