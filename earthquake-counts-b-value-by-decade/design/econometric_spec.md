# Analysis specification (descriptive study)

No regression is estimated for inference and no causal claim is made. All numbers are computed by `run_estimation.py` from table `eq_clean_m45` in data.db (USGS ComCat, doi 10.5066/F7MS3QZH, 1976-2025, M>=4.5, one preferred magnitude per event, aftershocks kept) and written to `estimation_results.json` (`result_kind: descriptive`).

## Sample
Unit: one catalogued earthquake with ComCat's preferred magnitude. Sample flow: raw rows in the five loaded files, then the cleaned table `eq_clean_m45` (277,946 events; all type `earthquake`, no missing depth). Decades: 1976-85, 1986-95, 1996-2005, 2006-15, 2016-25.

## (a) Yearly counts
- Annual counts for M>=5, M>=6, M>=7 and for one common threshold equal to the largest decade Mc (rounded to 0.1).
- Decade means and SDs of annual counts; dispersion index (variance/mean) per decade and overall.
- Trend as a description: Poisson and negative-binomial log-linear slope on year (percent per year, with 95% CI), labelled as an association with calendar time. Decade means decide whether a change is described.
- Mix of magnitude types by decade (share of M>=5 events per magType family).

## (b) Completeness and b-value per decade
- Mc by maximum curvature (mode of the 0.1-binned non-cumulative distribution, +0.2 correction) and by goodness-of-fit (smallest Mc with 90% / 95% fit, Wiemer & Wyss 2000), estimated from events with M>=4.5.
- b by Aki-Utsu ML with bin correction: b = log10(e) / (mean(M) - (Mc - dM/2)), dM = 0.1. SE by Shi & Bolt (1982): 2.30 b^2 sqrt(sum (M_i - mean M)^2 / (N(N-1))). Aki's b/sqrt(N) is reported as a labelled alternative. 95% bootstrap interval (1,000 resamples of events, seed 20260101).

## (c) Equality across decades
Utsu's (1965) two-sample likelihood-ratio test, reported exactly as computed, for all ten decade pairs, using each decade's own Mc and the common threshold; each pair is flagged as overlapping or non-overlapping in 95% intervals. Sensitivity: Mc shifted by -0.3 ... +0.3 in steps of 0.1 (b per decade).

## (d) Fixed versus window-specific Mc
b per decade at fixed Mc = 5.0 versus decade-specific Mc (maxc+0.2 and GFT 95%).

## Counting rule and censoring
Counts use the published magnitude (mag >= threshold, e.g. 5.0), identical to `eq_annual_counts.n_m50` (83,469 events at M>=5); the 0.1 binning (integer tenths) is used only for Mc and b. Mc = 4.5 (maxc raw, gft90, gft95 in 1996-2025) equals the load floor M>=4.5: those estimates are censored at the floor and Mc may be lower; `completeness.mc_censored_at_load_floor` records this.

## Checks
Mw-family-only sample (mw, mwc, mww, mwr, mwb, mwp) and shallow sample (depth <= 70 km), repeated for b and Mc. The Mw-only check reports b at its own Mc only: no b at the common threshold and no pair tests there, since moment magnitudes are assigned mainly to larger events and the sample is not complete at that threshold. The shallow check keeps the common-threshold b and pair tests. Dropped by instruction: declustering, ETAS/Poisson simulations, regional exclusions, sliding windows, magnitude conversion.

## Interpretation notes
Incompleteness below Mc lowers the estimated b. A difference between M>=5 and M>=5.5 counts is not a detection share. Patterns are descriptions of the catalogue, not of the Earth's rate.
