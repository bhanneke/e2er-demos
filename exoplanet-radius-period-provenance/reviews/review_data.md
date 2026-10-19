# Data Review: "How Are Confirmed Exoplanets Distributed in Planet Radius and Orbital Period? A Descriptive Decomposition by Radius Provenance"

Reviewer role: Data Reviewer. Scope: source documentation, sample construction, missing values, variable definitions, outliers, measurement quality, units, integrity and replication. I checked the draft against `data_dictionary.json`, the data summary, the analysis specification and the paper plan. I could not see `estimation_results.json`, the `.tex` tables, the figures or the code, so I could not check numbers against them. The `% src:` comments show where each number should come from.

## Overall assessment

The data work is transparent and mostly internally consistent. The source is identified with a DOI, table name, TAP query and SHA-256. The sample flow reconciles. The provenance rule is mechanical and reproducible, and the draft states its limits (no controversial-planet flag, no `ps` table, no manual validation). Duplicates, units (`pl_rade/pl_radj` ≈ 11.209) and missingness were checked. I re-computed the headline ratios and shares and they agree with the reported medians, shares and counts.

The problems concern what the groups are called and how far the numbers can carry the claims:

1. The "measured" label is not as clean as the paper implies.
2. One diagnostic statistic (ρ = 0.93 for transit-measured planets) is probably circular.
3. Several statements ("overlap little in the radius-period plane") are not backed by any reported joint statistic.
4. A few denominators and sample definitions are inconsistent or unclear between documents.

None of these requires new data. All can be fixed with the columns already loaded.

## 1. Source documentation

Strengths: the archive, table, DOI (10.26133/NEA13), citation, acknowledgement, TAP query and file hash are all documented. The unit of observation and the 6,445-row snapshot are stated.

- **Load date is missing from the paper.** The archive changes weekly and has no releases. The load date (2026-10-13) appears only in the data summary and `data_sources.json`. The Data section should state the snapshot date and the row count together, and say that counts will differ in later downloads.
- **Access conditions and licence.** The dictionary notes "no licence stated" and the acknowledgement request. The paper should include the standard acknowledgement.
- **Provenance rule documentation.** The rule rests on the archive's own documentation page (`pscp_calc.html`) and on `pl_rade_reflink` containing `refstr=CALCULATED_VALUE`. The paper describes it as the application of a mass-radius relation "documented by the archive". It should cite the documentation URL and name the relation (Chen and Kipping). The literature review confirms this link, but the draft's Data section never names the relation. A reader cannot tell which relation produces the 14.3 R⊕ ceiling.

## 2. Sample construction

- **Sample flow is described confusingly.** The draft says it drops "50 planets without a radius and 353 planets without an orbital period; some planets lack both, so 6,045 remain". Sequentially, 6,445 − 50 = 6,395, then 350 more are dropped for no period, leaving 6,045 (the data summary shows this). The 353 is a marginal count and 3 of those planets already lack a radius. Give the flow as a table, or at least as a sequential sentence: 6,445 → 6,395 → 6,045. The draft's wording makes the arithmetic look like 6,445 − 50 − 353 = 6,042.
- **Selection into the sample differs by group.** Of the 1,537 calculated planets, 322 (21.0%) are lost to a missing period (mostly microlensing and imaging). None of the 4,810 transit-measured planets is lost. The in-sample calculated group is therefore even more radial-velocity dominated than the full calculated group (1,133 of 1,215 in the sample vs 1,133 of 1,537 in the full table). The paper mentions the restriction in general terms but never gives this group-specific loss. It matters for the headline comparison: the calculated group "sits on much longer orbits" partly because the group's members without periods are removed.
- **Denominator mix-up risk between documents.** The data summary reports the method split (RV 1,133, microlensing 292, imaging 52, …) and the mass-provenance split (Msini 876, Mass 648, Msin(i)/sin(i) 13) for all 1,537 calculated planets. The draft reports "1,133 of 1,215" and "876 / 326 / 13 of 1,215" for the sample. These are consistent only if all 1,133 RV planets and all 876 Msini planets have a period, and if 322 of the 648 "Mass" planets are the dropped ones (648 − 322 = 326, which does work). Please state explicitly that these in-sample splits were recomputed on the 1,215, not carried over from the full table.
- **Mass-radius figure and statistic use different samples.** The data summary says the mass-radius scatter plots 1,537 calculated planets, but the text reports ρ = 0.47 for "the 1,215 calculated planets". The figure should be restricted to the same 1,215, or the caption and text should say that the figure has 322 more points. The two microlensing-dominated groups differ in mass distribution.
- **Robustness sample sizes.** For the P ≤ 1,000 d restriction the draft gives 855 calculated planets. The period bins give 1,215 − 186 − 176 = 853 planets at or below 1,000 d. The transit-measured numbers reconcile (4,810 − 5 − 1 = 4,804). A two-planet difference in the calculated group is probably a bin-edge convention (periods of exactly 1,000 d, or closed vs open interval), but the draft should state the bin convention (left-closed or right-closed) and reconcile the two counts.
- **Limit-flag run.** Removing the 7 flagged planets in the sample (2 calculated, 3 transit-measured, 2 non-transiting) is consistent with the dictionary. Fine.

## 3. Missing values

Missing values are documented column by column, with "missing" explanations on every column above 5% (`pl_orbper`, 5.5%). No imputation is done. The 6.2% loss from the radius-period restriction is counted. Two additions:

- `pl_bmassprov` has no `missing` note, although 31 planets lack a mass. State how many of the 31 are in the sample and in which group.
- The paper says "we use the planets with a value for each statistic and report n next to every statistic". The mass-radius statistics report n (1,215 and 4,786). The association statistics should each report n in the text, and not only in the table.

## 4. Variable definitions and measurement quality (main concerns)

**4.1 "Measured" is a label by exclusion, not a verified measurement.**
The rule says: calculated if the reference carries CALCULATED_VALUE, otherwise "measured". Three kinds of "measured" radii are not what a reader will assume:
- Transit radii depend on the stellar radius and, for many TESS/Kepler planets, on validation-paper priors. This is acknowledged only by a citation in the Introduction (Berger et al.).
- The 41 imaging planets in the non-transiting group have radii that come from evolutionary models (luminosity, age) and not from a measurement of size. Calling them "measured" overstates their status. It is harmless for the 20 in the sample, but the word is wrong.
- Other references may themselves derive a radius from a mass with a different mass-radius relation (for example RV discovery papers that publish an "estimated radius"). Such radii would not carry the archive's CALCULATED_VALUE label, so they would sit in the "measured" group, which then is contaminated by calculated radii. The paper states that the label was not validated, but it should also state the direction of the possible error: the calculated group is probably a lower bound on the share of model-derived radii.

Recommendation: rename the groups "radius flagged as calculated by the archive" vs "radius reported by the source reference" (or keep the current names with a one-sentence caveat in the Data section), and describe the 41 imaging radii as model-based.

**4.2 The ρ = 0.93 for transit-measured planets is probably circular.**
The draft reports ρ(log M, log R) = 0.93 for 4,786 transit-measured planets "with a mass". 4,786 of 4,810 is 99.5%. That is implausible for measured masses: most Kepler and TESS planets have no RV or TTV mass. The dictionary describes `pl_bmasse` as "true mass, M·sin(i), or a mass from a mass-radius relation". The likely explanation is that the archive fills in masses for transiting planets from the radius with a mass-radius relation. `pl_bmasse_reflink` is already loaded, so this is easy to test: count how many of the 4,786 masses carry CALCULATED_VALUE. If most do, then ρ = 0.93 reflects the relation applied backwards and not a physical correlation. The comparison "0.47 vs 0.93" and the sentence "the weaker association in the calculated group is consistent with a relation that is not increasing over the full mass range" then compare unlike things. Restrict the transit-measured benchmark to planets with a measured mass (non-calculated `pl_bmasse_reflink`), or drop the benchmark.

**4.3 The giant-planet hump of the calculated group is a property of the relation.**
846 of 1,215 calculated radii lie in 8–15 R⊕, none above 15, and the maximum is 14.3. Together with ρ = 0.47 this shows a plateau: the relation is nearly flat in the Jovian regime, so radii from masses of 0.3 to 10 Jupiter masses pile up at the same value. The draft reports the ceiling but still presents "more than half of the giant-planet hump consists of radii calculated from mass" as a finding about the catalogue's radius distribution. It is correct as arithmetic, but the abstract and conclusion should say that this part of the hump is a product of the plateau of the assumed relation and not an observed pile-up in size. Add a sentence on the mass range these planets cover.

**4.4 Periods also have heterogeneous provenance.**
The paper treats radius provenance carefully but not period provenance. For directly imaged planets (and some timing and microlensing cases) the archive's `pl_orbper` is typically derived from a projected separation or semi-major axis and an assumed geometry, not from an observed orbit. Periods up to 4.0 × 10⁸ d (about one million years) and 5 periods above 10⁶ d are in the data (kept, flagged in the data summary, but not discussed in the paper). State this for the 20 non-transiting planets (median 15,958 d) and for the 189 planets above 3,000 d.

**4.5 Pooled definitions: "confirmed planets" includes objects at brown-dwarf masses.**
The dictionary's expected mass range runs to 13,000 M⊕ (about 40 M_J) and the observed radius maximum is 87.2 R⊕ (about 7.8 R_J). The paper says "confirmed planets" throughout. Transit-measured radii of up to 32.6 R⊕ (2.9 R_J) and 220 transit-measured planets above 15 R⊕ are not typical planets either; they are likely inflated giants, low-mass-star hosts or poorly constrained radii. The data summary flags 6 radii above 25 R⊕ as "kept, flagged". The paper has no outlier discussion at all. At least report p1/p99 and the maximum for each group, say which objects exceed 25 R⊕ and what the archive says about them, and check that the headline medians and quantile differences do not depend on them (they will not for medians, but p90 and the upper-tail statements could).

## 5. Statistics and distributions

- **Quantiles and bins.** The type 7 definition is stated. The radius bins (2–4, 4–8, 8–15) are roughly equal in log10 width (0.30, 0.30, 0.27), which makes the "two humps" reading defensible. State this in the text, because a reader sees unequal linear widths. Period bins are decade-based and fine.
- **Second bin width check is not reported.** The spec (robustness c) and the course guidance require that a feature (here the dip between the humps) be checked at a second bin width. The data summary shows that fine bins exist (0.1 dex radius, 0.25 dex period). The draft should say that the two humps and the 4–8 R⊕ dip persist in the fine histogram, with the counts. It should also report the sub-2 R⊕ bins (<1, 1–1.5, 1.5–2); the radius valley near 1.5–2 R⊕ is the best-known feature of this distribution and the lit review cites it, but the draft says nothing about it.
- **"Overlap little" is not supported by a joint statistic.** The abstract says the groups "overlap little in the radius-period plane", and the text says "the groups overlap little in either dimension" on the basis of KS distances of 0.53 and 0.61. A KS distance of 0.53 means the CDFs differ by at most 0.53; the marginals still overlap substantially (the p90 of radius differs only by a factor of 1.1, and giant planets appear in both groups). The planned joint table (radius bin × period bin, group shares, cell-level differences) and the overlap measure from the plan are not in the paper. Either add the joint table or soften the claim to the marginal comparison.
- **Bootstrap intervals ignore system structure.** Planets are resampled individually. Planets in the same system (Kepler multis, TRAPPIST-1, etc.) share host stars, detection conditions and often radii references, so the planet-level bootstrap understates uncertainty for quantile differences. `hostname` is loaded: a cluster bootstrap by host would be a direct check. The seed (20261013 in the spec) should also be stated in the paper.
- **Spearman for n = 20.** The interval 0.16–0.87 is correctly described as wide. Fine.
- **Medians and ratios.** 12.6/2.46 ≈ 5.1 and 358.6/7.97 ≈ 45.0 agree with the log differences (0.71 and 1.65). The group shares (79.6%, 20.1%) are correct. The ratio statements in the conclusion (the "one fifth" etc.) are fine.

## 6. Associations and interpretation

The pooled ρ of 0.30 exceeding the transit-measured within-group value of 0.08 is correctly attributed to the mix of groups. The calculated-group value (0.40) should carry an explicit caveat: a calculated radius is a function of mass, and the mass-period relation in RV samples reflects detection limits (long periods need massive planets), so the "positive radius-period association" in that group is produced by two layers of construction (relation and selection). The draft says this only partly in the Limitations.

## 7. Time and units

Units are given for radius (R⊕), period (days) and mass (M⊕), with the Jupiter conversions checked. Log10 is applied to strictly positive values (checked: no radius ≤ 0 and no period below 0.09 d). No currency or seasonality issues apply. The discovery year coverage of 1992–2026 is declared.

## 8. Integrity and replication

Strengths: raw table kept unmodified, derived table built by a script, SHA-256 of the download, row counts at each step, `% src:` links from every number to a JSON path, a figure check that re-reads each figure's values, and a documented mismatch that was found and fixed (histogram bins).

Remaining items:
- The paper should state the load date and the TAP query (or point to `data_sources.json`).
- The groups table, the radius and period statistics tables, and the associations table are `\input` files I could not verify. Spot-check that n in the associations table (1,215; 4,810; 20; 6,045; mass-radius 1,215 / 4,786) matches the text.
- The dictionary promises that limit-flag counts (5 radii, 6 periods, 7 in sample) are "counted and handled". The paper reports the sensitivity run but not the counts. Add one sentence.

## 9. Red flags check

No vague sample description, no missing summary statistics, no implausible summary statistics except the unaddressed upper tail (Section 4.5). Missing data are discussed. No round-number sample sizes. No timing problem (no treatment/outcome).

## Prioritised list of requested changes

1. Test whether the masses of the 4,786 transit-measured planets are themselves calculated (`pl_bmasse_reflink`). Drop or redefine the ρ = 0.93 benchmark accordingly. (Section 4.2)
2. Qualify the "measured" label: imaging radii are model-based, and unlabelled model-derived radii may sit in the measured group. (Section 4.1)
3. Say in the abstract and conclusion that the calculated part of the giant-planet hump reflects the plateau of the assumed relation (maximum 14.3 R⊕). (Section 4.3)
4. Add the joint radius-period table, or remove "overlap little in the radius-period plane". (Section 5)
5. Report the group-specific loss from the period restriction (322 of 1,537 calculated, 0 of 4,810) and give the sample flow sequentially. (Section 2)
6. Align the mass-radius figure sample (1,537) with the statistic sample (1,215), and reconcile 855 vs 853. (Section 2)
7. Report the second-bin-width check, the sub-2 R⊕ bins and the upper-tail radii (>25 R⊕, up to 87 R⊕), and say how they affect the quantiles. (Sections 4.5, 5)
8. State the snapshot date, the relation named by the archive, the bootstrap seed, and consider a host-clustered bootstrap. (Sections 1, 5)
9. Note that periods of imaged and some timing planets are derived, not observed. (Section 4.4)

OVERALL SCORE: 6.5/10
RECOMMENDATION: Minor Revision
