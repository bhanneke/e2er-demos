# Paper Plan: Did Abolishing Primary-School Fees in Sub-Saharan Africa Raise Primary Enrolment?

Template: policy evaluation (staggered difference-in-differences). Stage: idea → identification/data. Author context: <redacted> (project owner).

---

## 0. Status flags the next specialists must read first

1. **Treatment-year coding is PROVISIONAL.** No source in the available data list (`worldbank`, `owid`, etc.) holds a fee-abolition date. Years in §3 are the commonly cited dates in the policy literature, written down here *as hypotheses to be verified*, not as facts. The data architect/identification strategist must confirm each against a published source (via `e2er-lit search`; candidates in §3.3) before the treatment table is built, and must record the verified citation per country in `data_dictionary.json`. Any country whose date cannot be confirmed is dropped from treated units and kept only in a "dated-uncertain" robustness set.
2. **Design caveat up front:** with WDI as the only enrolment source, pre-1999 observations are sparse, so the earliest adopters (Malawi 1994, Uganda 1997) may have few or no pre-period observations. See §5 for how to handle this (these are the main threats to the `did_design` check).
3. The unit-of-analysis is country-year; with roughly 40–45 SSA countries, inference must be small-cluster-robust (§6).

---

## 1. Phenomenon (Step 0)

Between 1994 and 2005 a wave of SSA governments abolished primary-school tuition and compulsory levies, usually under donor-backed Education for All / Fast Track pressure. Headlines were dramatic: in the best-known cases (Uganda 1997, Kenya 2003, Malawi 1994) governments reported million-plus new pupils in the first year. The puzzle:

- **Theory says** removing a price should raise demand for a normal good with elastic demand among the poor; but fees were only part of the private cost (uniforms, books, foregone child labour), and supply (classrooms, teachers) was fixed in the short run, so the net effect on *measured enrolment* could be large, small, or reversed in quality-adjusted terms.
- **Measurement puzzle:** gross enrolment ratio (GER) rises mechanically if over-age children, previously excluded, flood in or if repetition rises, without any increase in the share of *age-eligible* children in school. Reported "jumps" may therefore overstate access gains.
- **Why it matters:** fee abolition is a flagship policy of the MDG/EFA era and is the template for current free secondary and "free education" reforms (Gruijters 2024 on secondary abolition). Governments and donors (World Bank, UNICEF, FTI) decide whether to fund capitation grants and class-size mitigation based on beliefs about this elasticity.

## 2. Research question and hypotheses

**RQ.** What is the causal effect of national primary-school fee abolition on the gross primary enrolment ratio in sub-Saharan Africa, and how much of any effect is access for age-eligible children (net enrolment) versus over-age/repeater enrolment?

Pre-specified hypotheses (no revision after seeing data):

- **H1 (main):** Abolition raises GER; effect is positive on impact (year 0–1) and persistent for ≥5 years.
- **H2 (over-age):** The GER effect exceeds the NER effect (ΔGER − ΔNER > 0), i.e., part of the surge is over-age enrolment.
- **H3 (initial level):** Effects are larger where pre-reform GER was low (more room to grow, more fee-constrained households). Expect negative interaction with baseline GER.
- **H4 (gender):** Girls' GER rises by more than boys' (higher price sensitivity of girls' schooling), shrinking the gender gap.
- **H5 (capitation grants):** Effects are larger and more persistent where abolition was accompanied by a per-pupil capitation grant that replaced fee revenue; without compensation, schools reintroduced informal charges and the effect fades.
- **H6 (quality dilution):** Pupil–teacher ratios rise and primary completion / survival rises by less than enrolment (mechanism check, not main outcome).

## 3. Treatment definition and coding

### 3.1 Definition
Treated from year *g* if the national government formally abolished tuition fees (and, where stated, compulsory levies) for public primary school nationwide. Year of first implementation in the school year concerned. **Coding rule for school-year ambiguity:** WDI enrolment refers to the school year starting in the calendar year *t* (UIS convention); the treatment year *g* is the calendar year in which the first affected school year *begins*. Policies announced mid-year for the next January intake (Uganda 1997, Kenya Jan 2003, Tanzania Jan 2002 enrolment after Nov 2001 announcement) are coded to the calendar year of the first affected intake. This rule is applied before looking at outcomes; alternative ±1 year coding is an explicit robustness check.

### 3.2 Provisional coding table (TO BE VERIFIED, see flag 1)

| Country | Provisional g | Capitation / compensating grant at adoption (provisional) | Notes / ambiguity |
|---|---|---|---|
| Malawi | 1994 | No formal grant initially | Pre-period essentially absent in WDI (see §5) |
| Uganda | 1997 | Yes (per-pupil grant) | Initially capped at 4 children per family; universal 2003 coding variant |
| Tanzania | 2001 (intake 2002) | Yes (capitation grant, PEDP) | Code 2002 for enrolment; variant 2001 |
| Kenya | 2003 | Partial (FPE grant per pupil) | Jan 2003 intake |
| Ghana | 2005 | Yes (capitation grant) | FCUBE 1996 stated fee-free intent but ineffective; code 2005 as main, 1996 variant |
| Ethiopia | ~2002–03 | Block grants | Date ambiguity high; verify |
| Cameroon | ~2000 | Limited | Verify; parents' association levies persisted |
| Mozambique, Zambia, Rwanda, Burundi, Lesotho, Madagascar, Benin, Senegal, Ghana, etc. | to be determined | to be determined | Include only if verified; many have 2000–2008 dates |

The data architect should extend to all SSA countries with a documented abolition date and drop the rest from treated units. Countries with no abolition in-sample are the never-treated comparison group (and not-yet-treated for estimators that use them).

### 3.3 Candidate published sources to locate and cite (do not cite from memory)
- Nishimura (2009) comparative UPE policy analysis of Ghana, Kenya, Malawi, Uganda (`nishimura2009a` in literature.bib) — useful for four countries' dates and grant design.
- Morgan, Petrosino & Fronius (2014) systematic review of fee elimination (`morgan2014eliminating`).
- Kan & Klasen (2020) on Uganda UPE (`kan2020evaluating`); Valente (2015) on Tanzania (`valente2015primary`); Oseifosu (2011) on Ghana capitation grant (`oseifosu2011evaluating`); Wang (2009) on Malawi and Ghana (`wang2009the`).
- Fermah et al. (2026) meta-analysis of free primary education and capitation grants (`fermah2026effect`, `fermah2026school`) — likely contains a full country-date table; first source to check.
- World Bank/UNICEF "Abolishing School Fees in Africa" (2009) and Kattan & Burnett (2004) World Bank user-fee paper: to be searched and added to the bib before use.

Each country's row in the final treatment table carries: year, source key, whether source is primary (legal/ministerial) or secondary, capitation flag, and confidence (high/medium/low).

## 4. Outcomes (WDI via `worldbank` source)

Primary outcome
- **Gross enrolment ratio, primary, total** — `SE.PRM.ENRR` (enrolment of any age ÷ official primary-age population ×100; can exceed 100). Main spec uses log(GER) for semi-elasticity interpretation, and levels (percentage points) as a second display. Also report an alternative that handles >100 values: GER winsorized at the 99th percentile; and a Poisson/PPML spec on levels.

Robustness/secondary outcomes
- **Net enrolment rate, primary** — `SE.PRM.NENR` (share of age-eligible children enrolled; capped at 100 by construction). **Very sparse before 2000 in WDI**; plan assumes NER is available only for a subset of country-years. Report the NER sample explicitly and re-estimate the GER on the identical NER-available sample to avoid composition artefacts.
- **Over-age proxy:** GER − NER (where both observed); or `SE.PRM.UNER` (out-of-school children) as a cross-check.
- **Gender:** `SE.PRM.ENRR.FE`, `SE.PRM.ENRR.MA`; gender parity index `SE.ENR.PRIM.FM.ZS`.
- **Quality/dilution mechanisms:** pupil–teacher ratio `SE.PRM.ENRL.TC.ZS`; repetition `SE.PRM.REPT.ZS` if available; primary completion rate `SE.PRM.CMPT.ZS`; persistence to last grade `SE.PRM.PRSL.ZS`.
- Raw-count enrolment `SE.PRM.ENRL` (as a check against population denominator problems: GER is sensitive to UN population-estimate revisions).

Controls (time-varying, only pre-determined or plausibly exogenous): log GDP per capita (`NY.GDP.PCAP.KD`), school-age population share (`SP.POP.0014.TO.ZS`), under-5 mortality (`SH.DYN.MORT`), urban share (`SP.URB.TOTL.IN.ZS`), aid (`DT.ODA.ODAT.PC.ZS`). Controls potentially affected by the policy are kept out of the baseline (bad-control concern); they enter only in an augmented specification.

## 5. Identification strategy and design threats

### 5.1 Estimand
Average treatment effect on the treated (ATT) by event time, aggregated to a single post-adoption ATT, for countries first treated in *g*.

### 5.2 Estimators
1. **Baseline TWFE** (country and year FE) — reported only as a benchmark; decomposed with Goodman-Bacon (2021) to show weights on already-treated-as-control comparisons.
2. **Heterogeneity-robust estimators (headline):** Callaway & Sant'Anna (2021) with not-yet-treated and never-treated controls; Sun & Abraham (2021) interaction-weighted event study; Borusyak, Jaravel & Spiess (2024) imputation; de Chaisemartin & D'Haultfœuille (2020) as a cross-check. All keys exist in `literature.bib`.
3. **Event study** from −6 to +8 years, reference −1, with binned endpoints; HonestDiD-style sensitivity (Rambachan–Roth) for parallel-trends violations; Roth (2022) pretest caution is acknowledged (power of pretest).

### 5.3 Identifying assumption
Absent abolition, GER in adopting countries would have evolved as in not-yet/never-treated countries, conditional on country and year FE (and, in a stronger spec, region×year FE and baseline-GER×year trends).

### 5.4 Threats (honest assessment)
- **Policy endogeneity / anticipation.** Fee abolition was typically adopted by newly elected or reform-minded governments, often right after democratic transitions or in response to donor programmes (HIPC debt relief, FTI), and often when enrolment was already trending up or stagnant. *Direction of bias:* if adoption follows stagnation, ATT biased downward (mean reversion); if it follows a booming economy/aid inflow, biased upward. Mitigation: event-study pre-trends; control for aid per capita and GDP growth; region×year FE; anticipation window (drop g−1); placebo outcomes (e.g., secondary GER should respond only later).
- **Contemporaneous shocks.** The EFA/MDG push (Dakar 2000), HIPC relief (1999–2006), and the end of civil conflicts (Uganda, Mozambique, Rwanda, Sierra Leone, Liberia) coincide with adoption and affect comparison countries too. Because nearly all SSA countries received these shocks, the comparison group is partly "treated" by the broader trend; the DiD identifies the *incremental* effect of abolition, which will be a lower bound if control countries also reduced fees de facto (spillovers/contamination). Mitigation: code de facto fee reductions where documented; show results using only never-adopters through 2008 vs. not-yet-treated.
- **Sparse pre-period for early adopters.** WDI primary-enrolment series for many SSA countries start in the early 1990s and have gaps. Malawi (1994) and Uganda (1997) have 0–4 pre-observations. Plan: (a) require ≥3 pre-treatment observations for inclusion in the headline sample; (b) report results with and without Malawi/Uganda; (c) never impute enrolment with interpolation in the main sample (interpolation only in a flagged robustness).
- **Measurement error in GER.** Denominator = UN population estimates, which are revised and extrapolated between censuses; administrative enrolment is subject to inflation by schools (capitation grants create an incentive to over-report enrolment — a **mechanical positive bias post-policy** where the grant is tied to enrolment counts). Mitigation: NER and household-survey (DHS) attendance as a check if a data source is accessible; otherwise state as a limitation.
- **Unbalanced panel / selection into data availability.** Missingness is correlated with conflict and low state capacity. Report balance of observation counts by treatment status; run balanced-panel estimates.
- **Heterogeneous treatment timing in a small sample.** With ~15–25 eventual treated countries and a handful of cohorts, cohort-specific ATTs are noisy; report cohort-aggregated and calendar-time aggregates.
- **Variation in treatment intensity.** "Abolition" differs: some states abolished only tuition, others also uniforms/levies; some capped (Uganda 4 kids/family initially). Main spec is binary; intensity (capitation flag, pre-reform fee burden) enters via heterogeneity only.

## 6. Inference
Cluster at the country level (the level of treatment assignment). With ≈40 clusters and ≈20 treated, report wild cluster bootstrap p-values (Webb weights) alongside CR1/CR2 standard errors; for CS estimator use the multiplier bootstrap, clustered by country. Report randomization-inference p-values (permuting adoption years across countries) as a small-sample check.

## 7. Heterogeneity (pre-specified)
1. **Gender:** separate regressions for female and male GER; and GPI as outcome. Test equality of coefficients (stacked regression with interaction, clustered).
2. **Initial enrolment level:** split countries at the median of pre-reform GER (average over g−5…g−2) and also continuous interaction with baseline GER (observed, pre-treatment; not post-treatment). Beware regression to the mean: with measurement error in GER, low baseline GER correlates mechanically with later growth. Mitigation: use baseline from two prior years and instrument/average; present nonparametrically in bins.
3. **Capitation grants:** treated countries split by whether a per-pupil compensating grant started at adoption (coded in §3.2, with source). Small-cell caveat: this is a between-country comparison of only a few cohorts and is **descriptive/suggestive**, not causal (grant adoption is endogenous to state capacity and donor presence).
4. **Time since adoption:** dynamic profile to distinguish a one-off level jump from sustained growth, and fading (informal fee reintroduction).
5. **Region/income group** (East vs West/Central Africa; francophone vs anglophone as a lens on colonial education systems).

## 8. Mechanisms and how each is observed with the available data

| Mechanism | Prediction | WDI indicator | Test |
|---|---|---|---|
| Demand-side cost removal | GER↑ and NER↑ jointly, larger where baseline low and for girls | GER, NER, female GER | H1, H3, H4 |
| Over-age enrolment / catch-up | GER↑ > NER↑; transitory GER overshoot then convergence as cohorts age through | GER − NER; GER dynamics | H2; event study shape |
| Reduced repetition/dropout vs. inflow | Persistence to last grade, completion | `SE.PRM.PRSL.ZS`, `SE.PRM.CMPT.ZS` | H6 |
| Quality dilution (supply constraint) | PTR↑ after adoption, completion lags enrolment | `SE.PRM.ENRL.TC.ZS` | H6 |
| Reporting incentives (grants tied to counts) | Post-adoption GER jump larger in capitation countries without matching NER jump | GER vs NER by capitation | H5 (flagged as alternative explanation) |
| Substitution to private schools | Public enrolment↑, private share↑ in urban areas | `SE.PRM.PRIV.ZS` (sparse) | Descriptive only |

## 9. Robustness checklist (every main result)
1. Alternative estimators (§5.2) and not-yet vs never-treated controls.
2. NER as outcome on NER-observed sample; GER on same sample.
3. Treatment-year ±1 coding; drop ambiguous-date countries; drop earliest adopters (Malawi, Uganda) for pre-period sparsity.
4. Drop country-years in active conflict (UCDP/GMD-free coding: only if a source in the list provides it; else skip) and drop one country at a time (leave-one-out).
5. Region×year FE and country-specific linear trends estimated on pre-period only (Wolfers critique noted); HonestDiD bounds.
6. Outcome transformations: log GER, GER levels, winsorized, PPML, capped at 100.
7. Placebo: secondary-school GER (`SE.SEC.ENRR`) (expected null at short horizon); placebo adoption dates (permutation).
8. Balanced panel only; no interpolation.

## 10. Data plan (sources available only)

- `worldbank` (WDI): all outcomes and controls in §4, annual, SSA countries (World Bank region code SSF), 1985–2015. Time window: outcomes 1990–2015; post-period capped so that late (post-2005) policy waves and the "free secondary" wave do not contaminate (headline window to 2012; sensitivity to 2015).
- `owid`: cross-check series for primary enrolment and out-of-school children (OWID re-publishes UIS/WB series; use for validation and gap-checking only).
- `who_gho`: under-5 mortality / health covariates if wanted.
- Not available and flagged for `data_dictionary.json` `unavailable`: household surveys (DHS/MICS) for attendance by age; UIS administrative microdata by grade/age; conflict datasets (UCDP); a fee-abolition date database. The treatment table must therefore be hand-built from published sources (§3.3).
- Deliverable data tables: (i) `panel_country_year` (outcomes, controls, treatment dummy, event time, cohort g, capitation flag); (ii) `treatment_dates` (country, g, variant dates, source key, confidence); (iii) missingness map.

## 11. Contribution and positioning

Closest prior work (from `literature.bib`; all to be read before claims are final):
- **Morgan, Petrosino & Fronius (2014)** — systematic review of fee elimination in low-income countries; synthesises mostly single-country evaluations; limitation: heterogeneous designs, no common cross-country panel.
- **Fermah et al. (2026)** — systematic review/meta-analysis of FPE and capitation-grant policies on enrolment (OSF-registered); aggregates study estimates rather than estimating one consistent design on a common outcome.
- **Kan & Klasen (2020)** — Uganda UPE, within-country DiD on household data; credible but single-country; cannot speak to cross-country heterogeneity.
- **Nishimura (2009)**, **Wang (2009)**, **Valente (2015)**, **Oseifosu (2011)** — country case comparisons / single-country evaluations (qualitative or descriptive for the multi-country work).
- **Gruijters (2024)** — secondary-fee abolition evidence: the later-wave analogue.

| Dimension | This paper | Kan & Klasen 2020 | Morgan et al. 2014 / Fermah et al. 2026 | Nishimura 2009 |
|---|---|---|---|---|
| Question | Cross-country effect of fee abolition on GER; GER vs NER decomposition | Uganda UPE effect on schooling | Pooled effect from literature | Comparative UPE design lessons |
| Data | WDI country-year panel, SSA | Household surveys | Published studies | Case documents |
| Method | Staggered DiD with robust estimators | Cohort DiD | Meta-analysis | Qualitative |
| Key output | Common-design ATT, dynamics, heterogeneity by baseline/gender/grant | Within-country effect | Pooled estimate | Narrative |
| Mechanism | Over-age vs net access; dilution | Years of schooling | Limited | Capacity/implementation |

**Honest assessment of novelty.** This is not a "first study" claim; fee abolition is widely studied. The contribution is an *aggregate, common-design* estimate with modern staggered-DiD tools, and the **GER–NER decomposition** which speaks to the measurement puzzle (do headline surges reflect access for the age-eligible?). It is a **quantification + new setting/measurement** contribution. Outlet realism: a good field journal (World Development, Journal of Development Economics as stretch, Economics of Education Review, Journal of African Economies). Weaknesses: coarse aggregate data, few treated clusters, treatment-date uncertainty. The strength of the paper rests on (a) careful, sourced treatment coding, and (b) honest uncertainty quantification. A possible "reverse insight": if the GER effect is concentrated where capitation grants are tied to head-counts and NER does not move, the headline enrolment gains partly reflect reporting incentives — which would reframe the policy's evaluation.

## 12. Idea scoring (1–5)
Data availability 3 (outcomes yes; treatment dates need hand-building; NER sparse) · Identification 3 (staggered adoption, but endogenous adoption and common shocks) · Novelty 2–3 · Importance 4 · Feasibility 4. Verdict: proceed, conditional on the `did_design` gate passing (≥3 pre-periods for headline treated units, verified dates, ≥10 treated countries with data).

## 13. Handoffs and gating checks

- **identification_strategist:** confirm treatment dates and coding rule; decide headline sample (§5.4 pre-period rule); lock estimand and pre-specified hypotheses H1–H6 before outcomes are examined.
- **data_architect:** build tables per §10; use only listed sources; write `treatment_dates` with source keys; record unavailable items; report GER/NER coverage by country-year and pre-period counts for each treated country.
- **data_analyst:** descriptive facts: GER trends of treated vs control by event time, coverage, values >100, missingness.
- **econometrics_specialist:** implement §5.2/§6/§9; produce event-study figure and cohort ATT table; Bacon decomposition.
- **`did_design` check will fail if:** fewer than ~10 treated countries have ≥3 pre-observations, or treatment dates are unsourced.
- **`did_results` check (pre-trends/event study):** joint pre-trend test, HonestDiD bounds, and dynamic profile must be reported; paper_drafter is not dispatched until this passes. Because `paper_drafter` reads the identification, data, descriptive and econometrics outputs, **all four of those specialists must run** (plus a robustness/heterogeneity pass inside the econometrics specialist's output, so that §7 and §9 results exist before drafting).
- **Writing notes:** frame as a puzzle (headline enrolment surges vs. what they measure), not as a literature gap; report null or small effects plainly; state external validity (national-level, 1994–2012 SSA, countries with data and verified dates).
