# Paper Plan: How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period, and What Changes When Transit-Measured Radii Are Separated from Mass-Derived Radii?

Study type: descriptive data study. Stage: idea → data. Author handoff: data_architect → data_analyst → (data_quality check) → econometrics_specialist → data_analyst (figure_data check) → paper_drafter → review panel.

## 1. Statement of scope

**No causal claim is made and no regression is estimated.** The paper reports distributions, quantiles, counts and group comparisons of catalogued planet properties. The catalogue is not a random sample of planets, so every pattern is a pattern *in the confirmed-planet table*, not in the galactic planet population. Selection effects are listed as limits on interpretation (Section 7); they are not corrected, modelled or estimated. No identification strategy and no theory specialist are needed. The sections of this plan fix the analysis before the data are inspected (pre-specification of samples, bins, and outputs); any deviation is logged in the replication notes.

## 2. Phenomenon and motivation

The archive lists several thousand confirmed planets, and the headline picture (radius against period) shows a few well-known structures: a dense cloud of short-period planets between roughly 1 and 4 Earth radii, a population of hot Jupiters, and a sparse region at long periods. A reader looking at that picture will take it as a map of where planets are. But the radii behind the picture come from two different routes. Most are measured from transit depth (given a stellar radius). A smaller group, mostly planets found by radial velocity, has no transit; their radius in the table is calculated from a measured mass (or minimum mass) through an assumed mass–radius relation. The question: how much of the apparent structure belongs to each route, and how different are the two groups? The motivation is the observable pattern and its mixed provenance, not a gap in the literature.

Contribution type: **new fact / quantification** (a documented decomposition of the catalogue by radius provenance), plus a reverse insight: where the two groups do *not* overlap in (R, P), the combined picture is informative about detection method, not about planets.

Target outlet: field-appropriate astronomy/data-science venue (e.g., a research-note or data-descriptor style journal, or a field journal that accepts catalogue-descriptive work). Honest note: as a pure descriptive study this is not a top-journal paper; the value is a clean, reproducible reference decomposition.

## 3. Data

**Source:** NASA Exoplanet Archive, TAP service (`https://exoplanetarchive.ipac.caltech.edu/TAP/sync`), table `pscomppars` (Planetary Systems Composite Parameters; one row per confirmed planet, values pulled from different references to fill gaps). As a robustness input also download `ps` (all parameter sets) with `default_flag = 1` (one default reference per planet), because composite values can mix references, which matters for provenance.

**Primary sample (S0):** all rows of `pscomppars` (confirmed planets, archive default parameter set). Record the download date and archive row count; the archive changes weekly, so the data file with a timestamp and the query string are stored in the replication folder.

**Fields to request (verify names against the live schema at download; if a name differs, record the substitution):**
`pl_name, hostname, default_flag, discoverymethod, disc_year, disc_facility, pl_orbper, pl_orbpererr1, pl_orbpererr2, pl_orbperlim, pl_rade, pl_radeerr1, pl_radeerr2, pl_radelim, pl_radj, pl_bmasse, pl_bmasseerr1, pl_bmasseerr2, pl_bmasselim, pl_bmassprov, pl_orbsmax, tran_flag, sy_dist, st_rad, st_teff, pl_controv_flag, pl_refname` and any radius-reference link field (e.g., `pl_rade_reflink`) if present, plus reference fields for the radius value in `ps`.

**Derived analysis samples:**
- S1 (radius–period sample): S0 with non-missing `pl_rade` and `pl_orbper`, both > 0, and `pl_controv_flag = 0` (controversial planets excluded; their count is reported, and S1 is also reported without this exclusion in a robustness table).
- S1T (transit-measured radius) and S1M (mass-derived radius): a partition of S1 by radius provenance (Section 4).
- S2: planets with mass but no radius (to report how many planets are *not* in S1 at all, by method; this is a coverage statement, not an analysis sample).

## 4. Radius provenance: the key measurement decision

The archive does not, to my knowledge, publish a single clean "radius derived from mass" flag in the composite table. Provenance therefore has to be *constructed* and then *validated*; this step carries the largest risk to the paper and gets its own check.

**Classification rule (pre-specified, applied in order):**
1. Use the radius reference of each planet's radius value (reference field in `ps`/composite metadata). Where the reference's published method (reading the reference abstract/table note for each distinct reference) states that the radius is computed from mass with a mass–radius relation (e.g., Chen & Kipping 2017 "Forecaster", or other relations such as Weiss & Marcy 2014 or Zeng et al.), label **mass-derived**. Where it reports a transit-depth based radius with a stellar radius, label **transit-measured**.
2. If reference-level coding is infeasible for some references (count to be reported), fall back to a proxy: `tran_flag = 1` → transit-measured; `tran_flag = 0` with a non-missing `pl_rade` → mass-derived (non-transiting planets cannot have a transit depth). Planets with `tran_flag = 1` whose radius reference is coded mass-derived are kept as mass-derived and reported separately as a cross-check cell.
3. Anything unresolved is labelled **unclassified** and kept out of the group comparison; the count and the share of S1 is reported. If unclassified exceeds 10% of S1, the paper reports the comparison under both bounds (all unclassified as transit; all as mass-derived).

**Validation:** (a) hand-check a random sample of 50 planets per group against the cited reference; report the agreement rate; (b) cross-tabulate the label with `discoverymethod` (expected: transit-measured ≈ Transit; mass-derived ≈ Radial Velocity and some microlensing/astrometry/imaging); (c) for mass-derived planets, check whether the radius is a deterministic, monotone function of mass within a reference (plot R against M; a tight curve confirms the provenance; scatter indicates measured radii mislabelled). Cases with `pl_bmassprov = Msini` imply the "mass" is a minimum mass; flag them as a sub-group, because a radius computed from a minimum mass is a lower-bound-style quantity.

## 5. Descriptive outputs (the analysis step writes these into `estimation_results.json` in the descriptive results schema)

All distributions are on log10 scales for both radius (Earth radii) and period (days). Fixed binning decided here: radius bins of 0.1 dex from 0.3 to 30 R⊕ (≈ 20 bins); period bins of 0.25 dex from 0.3 to 10^5 days. Also report a coarser 2D grid (0.25 dex × 0.5 dex) for tables so cell counts stay readable. Cells with fewer than 5 planets are shown but not interpreted.

**Table 1: sample accounting.** S0 rows → missing radius → missing period → controversial → S1 → partition into S1T / S1M / unclassified; counts by `discoverymethod`; by `disc_year` decade.

**Table 2: marginal summaries.** For log10 R and log10 P in S1, S1T, S1M: N, mean, SD, min, 1st, 5th, 10th, 25th, 50th, 75th, 90th, 95th, 99th percentiles, max, in original units. Also shares in conventional radius classes (< 1.25 R⊕ rocky/Earth-size, 1.25–2 super-Earth, 2–4 sub-Neptune/mini-Neptune, 4–10 Neptune to Saturn size, > 10 Jupiter size; boundaries are conventions, stated as such) and period classes (< 1 d, 1–10 d, 10–100 d, 100–1000 d, > 1000 d).

**Table 3: joint distribution counts.** Count of planets per (radius class × period class) cell for S1, S1T and S1M, with row and column shares.

**Table 4: comparison of the two radius groups.** Differences in medians and quantiles of log R and log P (with bootstrap 95% intervals, 2,000 resamples, descriptive uncertainty of the quantile only, not an effect), two-sample Kolmogorov–Smirnov distance and Wasserstein distance on log R and log P as *descriptive distance measures* (p-values not interpreted as tests of an effect), Spearman correlation of log R with log P within each group (a descriptive association). Also the share of each group in each radius class and period class, and the overlap region: the share of each group lying inside the convex hull/box of the other (to show where comparison is meaningful).

**Figures (log–log axes throughout; the data_analyst figure check re-reads each figure's plotted values against the tables):**
- Fig 1: scatter of log R vs log P, all of S1, with marginal histograms.
- Fig 2: same, two panels (or two colours with transparency, colour-blind-safe palette) for S1T and S1M, identical axes.
- Fig 3: 2D hexbin/count grid for each group, shared colour scale, plus a ratio panel (share of S1M in cell).
- Fig 4: marginal histograms and empirical CDFs of log R and log P by group.
- Fig 5: for mass-derived planets, R against M with the implied mass–radius curve (provenance diagnostic).
- Fig 6: by discovery year, median log R and log P by group (descriptive trend of the catalogue composition).

**Robustness tables (reported in full, not selected):** (i) `ps` default_flag=1 instead of composite; (ii) including controversial planets; (iii) excluding planets with only upper/lower limit flags on radius or period (`*lim` ≠ 0); (iv) excluding `Msini`-based mass-derived radii; (v) alternative bin widths (0.05 and 0.2 dex); (vi) radii with relative uncertainty < 20% only; (vii) the unclassified bounds from Section 4.

## 6. Data checks (to run before the analysis)

The data_quality check covers: units (radius in R⊕ vs `pl_radj` consistency, ratio ≈ 11.2; period in days); duplicates (one row per `pl_name` in the composite; in `ps` exactly one `default_flag = 1` per planet); missing values by field and by method; non-positive or implausible values (radius > 30 R⊕, period > 10^6 d flagged and inspected, not dropped silently); limit flags; consistency of the derived provenance label with `tran_flag` and `discoverymethod`; archive row count recorded against the web count on the download date. Any failure stops the run.

## 7. Limits on interpretation (flagged, not estimated)

1. **Transit detection bias.** The transit probability scales roughly as R★/a and the signal depth as (R/R★)²; so transit-measured planets are over-represented at short periods and large radii, and at long periods and small radii they are largely absent. The pile-up of transit-measured planets at short period is a feature of detection, not a population density. Different surveys (Kepler, K2, TESS, ground-based) add their own windows, and Kepler's field and duration set an upper period reach.
2. **Mass-derived radii are model outputs, not measurements.** They depend on the assumed mass–radius relation (probabilistic or deterministic, calibrated on a given sample, mostly on transiting planets), on the mass measurement or on a minimum mass, and on the relation's behaviour at the boundaries (e.g., the flat Jovian regime where radius is nearly independent of mass). A mass-derived group will therefore look smoother and more tightly structured in R than the true radii, partly by construction. Differences between groups cannot be read as physical differences between planet populations.
3. **Detection method confound.** Mass-derived radii come mostly from radial velocity, which favours massive planets and short-to-intermediate periods and long baselines; the two groups differ in method, in host stars, and in discovery era at the same time. The comparison is therefore a comparison of two catalogue subsets, with provenance and method inseparable in much of the data.
4. **Composite table.** Composite values may mix references with different assumptions; the `ps` default-flag check addresses this partly.
5. **Archive is a moving target.** Counts change weekly; all numbers refer to the dated download.
6. **No population claims.** Language rule for the draft: use "in the confirmed-planet table", "catalogued planets"; avoid "planets are distributed", "occurrence", "more common", and any "effect of" wording.

## 8. Positioning (closest work, to be verified by the literature reviewer)

Closest relatives (the literature reviewer must confirm citations and details; none is asserted here from memory beyond the topic):
- Catalogue-based demographic work on the radius distribution and the "radius valley" using Kepler/California–Kepler Survey data (e.g., Fulton et al. 2017) — corrects for selection and uses precise stellar radii; our study does neither, and does not claim occurrence rates.
- Occurrence-rate analyses of Kepler planets (e.g., Petigura et al. 2013; Hsu et al. 2019) — estimate corrected populations; ours describes the uncorrected catalogue.
- Mass–radius relation papers (Weiss & Marcy 2014; Chen & Kipping 2017; Otegi et al. 2020) — define the relations used to compute radii; ours documents how many catalogue radii rely on them and where they sit in (R, P).
- Archive documentation/descriptive pages (Akeson et al. 2013; NASA Exoplanet Archive data columns documentation).

Contribution matrix (to be completed by the literature reviewer): question (catalogue composition by radius provenance) / data (uncorrected archive) / method (descriptive) / finding (to be determined) / mechanism (none claimed) / implication (caution when using the archive's radius column for population statements).

Anticipated referee objection: "descriptive and obvious." Response built into the design: the paper's value is the quantified share and location of the mass-derived radii in the (R, P) plane, which the headline picture hides.

## 9. Pre-specified expectations (stated before seeing the data, not hypotheses to be tested)

- S1T will be the large majority of S1 and concentrated at short periods; S1M will be a small share, mostly radial-velocity discoveries, at longer periods and with a narrower radius range.
- The two groups will overlap only partly in (R, P); where they do not overlap, no comparison is drawn. If these expectations fail, the result is reported as found.

## 10. Task allocation and handoff

- **data_architect:** write the TAP queries, download `pscomppars` and `ps` (default_flag=1) into a fresh, empty data directory, keep scripts in a separate directory, record download date and row counts; build the radius-provenance coding table (Section 4) including reference-level coding and the proxy; run Python with `-I` when reading downloaded files.
- **data_analyst (pre-analysis):** run the Section 6 checks, produce the analysis samples S1, S1T, S1M, S2 and a cleaning log; write the data-quality report.
- **econometrics_specialist:** (no regressions) compute Tables 1–4, robustness tables, and write `estimation_results.json` in the descriptive results schema, with figure data attached.
- **data_analyst (post-analysis):** produce Figures 1–6 and re-read plotted values against the tables (figure_data check).
- **paper_drafter:** draft from the tables and figures, following the language rule in Section 7.6; the limitation section is the longest section of the discussion.
- **Review panel:** literature_reviewer (positioning), writing_reviewer, data_reviewer (provenance validation), methods_reviewer (binning, bootstrap, descriptive distances), plausibility_reviewer (no population or causal over-claiming).

## 11. Feasibility and scores

Data availability 5 (public, API); identification not applicable (descriptive, no claim); novelty 2–3 (a decomposition of a familiar catalogue; novelty rests on the provenance coding); importance 3 (guards users of the archive against over-reading its radius column); feasibility 5 (days of compute, the main labour is the provenance coding). Principal risk: the provenance classification (Section 4) — if reference-level coding cannot be completed for a large share of planets, the paper falls back to the `tran_flag` proxy and says so prominently.
