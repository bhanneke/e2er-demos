# Descriptive specification: Pleiades membership and distance from Gaia DR3

Design type: descriptive. No regression, no significance test, no causal claim, no model-based distance. The outputs are counts, medians, percentiles, binned locus summaries, and a sensitivity grid of re-counts.

## 1. Sample

- Source: `gaia_dr3` table in `data.db`, loaded from the ADQL pre-filter in the work order (cone 3° around RA 56.75°, Dec +24.12°; `parallax > 2` mas; `parallax_over_error > 5`; 14,066 rows, pulled 2026-10-13). The archive's anonymous limit (50,000 rows) and the cone count (255,553 sources) make the full cone unavailable, so the extract is a pre-filtered subset. The extract limits the field background in the CMD to stars with parallax above 2 mas (closer than about 500 pc). Every grid cut lies inside this extract.
- Base quality sample (`data/gaia_clean.csv`, written by `clean_gaia.py`): duplicates removed; `astrometric_params_solved` in {31, 95} (five- and six-parameter solutions; 3 = two-parameter solutions are excluded); non-null parallax and proper motion; `ruwe < 1.4`; `parallax_over_error > 10`.
- Sample flow is logged at each filter (raw → duplicates → solution type and nulls → RUWE → parallax_over_error), with n kept and n dropped.
- Missing values are not filled. CMD rows drop only where `bp_rp` is null; the count of drops is reported.

## 2. Membership (base specification, fixed before the results were read)

1. Parallax centre π₀ and scatter σ_π: iterative 3σ clipping of parallax (clip at median ± 3·sd, repeat until stable). π₀ is the clipped median and σ_π the clipped sd. Nothing is hard-coded; the value 7.3 mas is not used.
2. Parallax window: |parallax − π₀| < 3σ_π.
3. Proper-motion centre (μα₀, μδ₀): iterative 3σ clipping of pmra and pmdec among stars in the parallax window; clipped medians.
4. Proper-motion radius: sqrt((pmra − μα₀)² + (pmdec − μδ₀)²) < 5 mas/yr.

Member = passes the quality cuts, the parallax window and the PM radius.

Seeding. A clip on the full quality sample converges to the field, not to the cluster (the naive run gives a centre of about 3.2 mas). The proper-motion iteration is therefore seeded from the densest 2 mas/yr proper-motion bin among quality stars with parallax between 5 and 10 mas. The seed is only a starting value: the centres and window are recomputed by clipping until the proper-motion centre is stable, and the naive full-sample centre is reported beside the result for transparency.

## 3. Sensitivity grid (descriptive re-counts only)

One-at-a-time rows vary one dimension from the base:

| Dimension | Base | Variants |
|---|---|---|
| PM radius (mas/yr) | 5 | 3, 7, 10 |
| Parallax window | 3σ | 2σ, fixed ±1 mas |
| RUWE cut | < 1.4 | < 1.2 |
| parallax_over_error | > 10 | > 5 |
| Zero point | none | approximate constant +0.03 mas offset (see §6) |
| Bright-star floor | none | G > 6 |

Full cross: PM radius (3, 5, 7, 10) × parallax window (2σ, 3σ, fixed ±1 mas) × RUWE (< 1.2, < 1.4) × parallax_over_error (> 5, > 10), giving 48 rows. The centres π₀ and μ₀ are recomputed inside each row with the same clipping rule and the same seed. The zero-point row is reported with the base cuts only. Every row is reported; the paper does not select the best row.

Reported grid statistics: the one-at-a-time member counts, their median, the largest one-at-a-time change relative to the base, and the minimum, median and maximum of the 48-row cross.

## 4. Outputs

1. Stage counts and the base sample flow.
2. Members: parallax median and quartiles, the mode (from a 0.1 mas histogram), the mode-minus-median difference, and the standard error of the median (σ/√n).
3. Distance, 1000/π (pc, uncorrected parallax): median with 16th and 84th percentiles, the IQR, and the distance modulus 5 log10(d) − 5.
4. CMD: members with bp_rp, against G (magnitude axis inverted), with quality-cut non-members as the field background. Locus summary: median and 16th–84th percentiles of bp_rp in 1-mag G bins from 6 to 18; brightest and faintest member G.
5. Figures from saved data: a proper-motion vector-point diagram, the CMD of the quality sample (`fig_cmd.pdf`), the members' CMD with members and field as two groups (`fig_cmd_members.pdf`, sourced from the `gaia_clean` table on `cmd_group`), and the distance histogram, all sourced from `data.db` and `estimation_results.json`. The scatter renderer draws larger G higher; G is not inverted, because the figure check re-reads the raw column.
6. Bright end: the brightest member's G and the number of extract stars brighter than it, with how many fail each quality cut (`bright_end` block). This records a gap in the member sample; it does not identify the cause.

## 5. Reading rules (fixed in advance)

- Clear: base count within ±10% of the one-at-a-time grid median; no one-at-a-time row changes the count by more than 25%; parallax histogram unimodal with mode and median within 0.1 mas; median distance in the 125–145 pc reference band; continuous locus over at least 8 mag in G.
- Ambiguous: count varies by more than 25% across the grid, a bimodal parallax histogram, or a broken CMD locus. The paper reports the spread, not the best row.
- Null or unexpected: base count below 100, or median distance outside 110–160 pc. The paper reports the failure and checks the cone centre and the pull first.

## 6. Caveats to state

- The main analysis uses the uncorrected parallax. The zero-point row adds a constant +0.03 mas. This approximates the Lindegren et al. (2021) offset; it is not the per-star correction, which needs `nu_eff`, pseudocolour and ecliptic latitude, none of which are in the extract. The row is a sensitivity only.
- Photometry is not extinction-corrected; the CMD is shown uncorrected.
- Crowding and bright-star effects at G < 6 and in the cluster core: counts are reported with and without the G > 6 floor.
- The parallax > 2 mas extract limits the field background to stars closer than about 500 pc. Field statements in the CMD apply only to that range.
- The member count is a selection outcome, not a population estimate. The grid shows its sensitivity to the cuts.

## 7. Implementation

- `run_estimation.py` reads `data/gaia_dr3.csv` (the raw extract) for the sensitivity grid, because the RUWE < 1.2 and parallax_over_error > 5 rows need cuts that `gaia_clean.csv` has already applied. It asserts that its base quality sample equals `gaia_clean.csv` row for row in count.
- It writes `estimation_results.json` in the descriptive results schema.

## 8. Realised results

Run with `e2er-run run_estimation.py` (exit clean). Every number below is read from `estimation_results.json`.

- Sample flow: raw extract 14,066 → duplicates removed 0 → solution type and nulls 14,066 → RUWE < 1.4 leaves 12,722 (1,344 dropped) → parallax_over_error > 10 leaves 9,970 (2,752 dropped). Base quality sample N = 9,970.
- Seed: (19.0, −45.0) mas/yr. Naive full-sample parallax centre 3.189 mas (sd 1.797), the field, not used.
- Converged centres: π₀ = 7.367 mas, σ_π = 0.230 mas, window ±0.691 mas; PM centre (19.867, −45.416) mas/yr.
- Stage counts: quality 9,970 → parallax window 1,345 → PM radius (5 mas/yr) **1,112 members** (11.2% of the quality sample).
- Member PM dispersion: pmra sd 1.08 mas/yr, pmdec sd 1.41 mas/yr.
- Parallax of members: median 7.367 mas (IQR 7.243–7.490); mode 7.35 mas (mode − median = −0.017 mas); one local peak; standard error of the median 0.007 mas.
- Distance (1000/π, uncorrected): median 135.7 pc; 16th–84th percentile 132.3–139.3 pc; IQR 4.5 pc; distance modulus median 5.66 mag.
- CMD: 1,095 members with bp_rp (17 without); G from 5.20 to 20.16 mag. Median bp_rp by G bin (n in brackets): G 6–7: 0.02 (10); 7–8: 0.17 (14); 8–9: 0.40 (18); 9–10: 0.70 (32); 10–11: 0.89 (37); 11–12: 1.08 (41); 12–13: 1.39 (46); 13–14: 1.81 (65); 14–15: 2.28 (59); 15–16: 2.67 (142); 16–17: 2.99 (250); 17–18: 3.25 (228). The 16th–84th percentile ranges are in `main_sequence_locus`.
- One-at-a-time grid (members): base 1,112; PM radius 3 → 1,024; 7 → 1,124; 10 → 1,127; parallax window 2σ → 1,025; fixed ±1 mas → 1,135; RUWE < 1.2 → 1,053; parallax_over_error > 5 → 1,125; zero-point row (+0.03 mas) → 1,112; G > 6 floor → 1,106. Median 1,112. Largest one-at-a-time change from base: 7.9%.
- Full cross (48 rows): members min 913, median 1,055.5, max 1,184. Relative to the base (1,112): −18% at the minimum, +6% at the maximum.
- Bright end: the brightest member has G = 5.203 (second brightest 5.428). The extract holds 5 stars brighter than G = 5.203, with G from 3.62 to 4.26. All 5 fail the quality cuts, and all 5 have RUWE of 2.31 or more (`bright_end` block). The RUWE failure is observed; the paper does not establish which cut removed these stars from the member sample.
- Zero-point sensitivity: the distance of the zero-point row is not reported in the JSON; the count is unchanged at 1,112 and the centre moves from 7.367 to 7.397 mas, a shift of +0.03 mas, which lowers the median distance by about 0.4%.

Reading against §5: the base count is stable, the parallax histogram is unimodal with mode and median within 0.1 mas, the median distance (135.7 pc) lies in the 125–145 pc reference band, and the locus is continuous over more than 8 mag in G. The result is therefore **clear** for the base specification. The full cross spreads counts from −18% to +6% around the base; the paper reports this in full, not only the base row.
