# Analysis Specification (descriptive study; no regression, no causal claim)

## Question
How are confirmed exoplanets distributed in planet radius (Earth radii) and orbital period (days), and how does the distribution differ between radii measured from transits and radii the archive calculated from planet mass?

## Data and unit
- Unit: one confirmed planet (row of NASA Exoplanet Archive `pscomppars`, loaded as `planets`; `planets_classified` adds the derived columns). Source: data.db, 6,445 rows, `pl_name` unique.
- Provenance rule (researcher decision, replaces Section 4 of paper_plan.md): `radius_group` from `pl_rade_reflink`: `calculated` (contains CALCULATED_VALUE), `measured_transiting` (other radius, tran_flag = 1), `measured_non_transiting` (other radius, tran_flag = 0; imaging etc.; never called transit-measured), `no_radius`.
- Descriptive sample: planets with both radius and period (`in_rp_sample = 1`). Sample flow: 6,445 raw -> drop no radius (50) -> drop no period (353 missing) -> 6,045. Missing values are dropped, never filled; counts reported per group.
- `pl_controv_flag` is not loaded, so controversial planets are not excluded. Limit-flagged values (`pl_radelim`, `pl_orbperlim` non-zero) are kept in the main sample and dropped in a sensitivity run.
- The catalogue is not a random sample of planets (transit/RV detection limits); all statements describe the catalogue.

## Statistics (all computed in `run_estimation.py`)
Groups: all (6,045), calculated, measured_transiting (main comparison), measured_non_transiting (separate, small).
1. For radius and period, per group: n, mean, sd, min, p5, p10, p25, median, p75, p90, p95, max (numpy type-7 quantiles), plus the same statistics of log10 radius and log10 period and the geometric mean.
2. Distributions: period bins equal width in log10 (decade-based edges 0.1-1, 1-3, 3-10, 10-30, 30-100, 100-300, 300-1000, 1000-3000, >3000 days) and radius bins (<1, 1-1.5, 1.5-2, 2-4, 4-8, 8-15, >15 Earth radii) with counts by group; counts add up to n. A second, finer equal-log10-width histogram checks that features are not bin artefacts.
3. Joint counts: radius-bin x period-bin table per group and the share of each group's planets in each cell (denominator = group n); cell-level percentage-point differences between calculated and measured_transiting.
4. Group comparisons (descriptions): differences in medians and in p10/p25/p75/p90 of log10 radius and log10 period between calculated and measured_transiting, with 95% bootstrap percentile intervals (2,000 resamples, seed 20261013); a Kolmogorov-Smirnov distance and Spearman rho(log radius, log period) per group with n and bootstrap interval. These are descriptions of the catalogue, not effects.
5. Discovery-method composition per group (counts and shares with denominators), and the cross-tab radius_group x tran_flag.
6. Mass-radius diagnostic for the calculated group: Spearman rho between log10 mass and log10 radius, mass-provenance split (Mass, Msini, Msin(i)/sin(i)), because calculated radii are derived from mass (mostly minimum mass, Msini) through an assumed mass-radius relation, so their radius distribution reflects the mass distribution and that relation, not an independent size measurement. The rank correlation is reported as realized, not assumed to be 1.
7. Robustness: (a) excluding limit-flagged values; (b) restricting both groups to P <= 1000 d (common period support); (c) second bin width.

## Figures (figure_spec.json, sourced from data.db / results)
fig_radius_period_all, fig_radius_period_by_group (scatter, log axes, groups), fig_marginals_by_group (histograms from results bins), fig_mass_radius_calculated (scatter). Values are written by the script from the same queries.

## Output
`estimation_results.json` with `result_kind: "descriptive"`, `sample`, `statistics`, `distributions`, `associations`, `groups`, `comparisons`, `figures`. Every number computed in code; none typed by hand.
