# Literature Review: Primary-School Fee Abolition in Sub-Saharan Africa and Modern Staggered DiD

Stage: idea. Produced by the Literature Scanner. Only `\cite{}` keys listed in section 6 resolve in `literature.bib`. Works named in plain "Author (year)" form are NOT yet in the bib. They come from memory and must be verified, and then added with `e2er-lit search`, before they are cited in the paper.

## 1. Key Findings (what the literature says)

### 1.1 Country evidence on fee abolition
- **Uganda (UPE, 1997).** Deininger (2003, *Economics of Education Review*) uses household surveys from before and after UPE. He reports large enrolment gains, concentrated among the poor, girls and rural children, and a narrowing of the enrolment gap by income. He also finds that quality came under strain. Not yet in the bib; verify the details. Grogan (2009, *Journal of African Economies*) finds that UPE reduced delayed school entry and increased on-time entry. Not yet in the bib. Related work in the bib: \cite{kan2020evaluating} (school-fee abolition and educational outcomes in Uganda), \cite{moyi2011delayed} (delayed entry), \cite{lamichhane2017impact} (out-of-school children), \cite{nishimura2007internal} (internal efficiency), \cite{nakabugo2008universal} (large classes). \cite{behrman2014the} uses UPE in Uganda and FPE in Malawi to study adult women's HIV status.
- **Malawi (FPE, 1994).** Al-Samarrai and Zaman (2007, *Education Economics*) study fee abolition, access and equity. They find enrolment rose sharply, with improved equity but pressure on quality and high repetition and dropout. Not yet in the bib; verify.
- **Kenya (FPE, January 2003).** Lucas and Mbiti (2012, *AEJ: Applied*) find that FPE raised entry and completion, especially for the poor. They also find sorting out of public schools and no gain in test scores. Not yet in the bib. The work order says "Lucas and McEwan"; the Kenya paper I can recall is Lucas and Mbiti, so the intended citation needs checking. \cite{wallstrom2017is} studies private schooling after Kenya's FPE.
- **Tanzania (fee abolition and PEDP, around 2001).** \cite{valente2015primary} studies primary education expansion and quality in Tanzania.
- **Ghana.** The capitation grant started in 2005. I found no paper on it in the search so far; one is needed.
- **Multi-country synthesis and policy reports.** Avenstrup, Liang and Nellemann (2004, World Bank), on Kenya, Lesotho, Malawi and Uganda, find big enrolment jumps followed by capacity and quality strains. Not yet in the bib. Other World Bank and UNESCO material (EFA Global Monitoring Reports, the World Bank/UNICEF School Fee Abolition Initiative) is not yet searched. \cite{evans2020education} is a general review of education research in Africa.

### 1.2 Common empirical pattern
- All country studies report a large jump in gross enrolment (GER) at or soon after abolition. The jump is larger for poorer children and for girls.
- Concerns recur about congestion, quality, delayed entry and over-age enrolment (which mechanically inflates GER), and substitution toward private schools.
- Most studies are single-country, use household surveys or simple before/after designs, and have no clean control group. Some use age-cohort exposure designs.

### 1.3 Modern staggered-DiD methods (all in the bib)
- \cite{goodmanbacon2021difference}: the two-way fixed effects (TWFE) estimate is a weighted average of 2x2 comparisons. Already-treated units act as controls, so heterogeneous effects over time can bias it.
- \cite{dechaisemartin2020twoway}: TWFE weights can be negative under heterogeneous effects. The paper proposes a robust estimator.
- \cite{callaway2021difference}: group-time ATTs aggregated with not-yet-treated or never-treated controls. It supports conditional parallel trends.
- \cite{sun2021estimating}: an interaction-weighted event-study estimator that avoids contamination from other leads and lags.
- \cite{borusyak2024revisiting}: an imputation estimator, efficient under homogeneous-trend assumptions.
- \cite{roth2023trending}: a synthesis of the recent DiD literature.
- \cite{roth2022pretest}: pretests for parallel trends have low power and cause selection bias.
- \cite{rambachan2023credible}: sensitivity analysis (HonestDiD) that bounds the violation of parallel trends.

## 2. Gap

- No cross-country study of SSA fee abolition uses heterogeneity-robust staggered DiD with not-yet-treated comparisons. Existing work is mostly single-country, pre/post, or uses TWFE. I have not searched exhaustively, so this claim must be checked with more searches before it goes into the paper.
- The contribution is a pooled, multi-country ATT on GER with dynamic event-study effects. It would use \cite{callaway2021difference} and \cite{sun2021estimating} as the main estimators, \cite{borusyak2024revisiting} as a check, and a TWFE benchmark decomposed with \cite{goodmanbacon2021difference}. Inference on pre-trends follows \cite{roth2022pretest} and \cite{rambachan2023credible}.

## 3. Methodological Notes for the Design
- Staggered adoption mid-1990s to mid-2000s is the setting these estimators were built for. The mid-2000s adopters and the not-yet-treated pool serve as controls.
- Treatment dating is a risk. "Abolition" differs across countries: formal law versus implementation, and partial versus full abolition (Uganda started with four children per family). Coding rules must be documented with sources.
- Fee abolition coincided with other policies: HIPC debt relief, the Education for All and Fast Track Initiative funding, and the Millennium Development Goals. These are possible confounders and drive anticipation and selection into early adoption.
- GER outcomes: GER can exceed 100%, is affected by over-age entry, and relies on administrative population denominators (World Bank/UIS). Net enrolment would be a useful complement, but its coverage is thinner.
- Missing data in the 1990s is likely, so the panel may be unbalanced.

## 4. Gaps and Open Questions
- Verify all non-bib references (Deininger 2003, Grogan 2009, Al-Samarrai and Zaman 2007, Lucas and Mbiti 2012, Avenstrup et al. 2004) and add them to the bib. Clarify the "Lucas and McEwan" reference.
- Confirm adoption years per country (Malawi 1994, Uganda 1997, Tanzania around 2001, Kenya 2003, Ghana 2005 capitation grant). The other adopters in the sample (Lesotho, Cameroon, Mozambique, Rwanda, Ethiopia and others) are unchecked.
- No search yet for World Bank/UNESCO reports, and no review of other multi-country or panel evidence.
- No quantitative effect sizes were extracted from the cited studies; they were not read for this review.

## 5. Handoff
- The identification_strategist should define the treatment dating and the control pool.
- The data_architect should check GER coverage by country-year from 1990 onward.
- The paper_drafter should cite only keys in section 6 until the other works are added.

## 6. Citable Keys (in literature.bib)
Methods: callaway2021difference, goodmanbacon2021difference, sun2021estimating, dechaisemartin2020twoway, borusyak2024revisiting, roth2023trending, roth2022pretest, rambachan2023credible.
Topic (found via search; relevance judged from titles only, not read): kan2020evaluating, moyi2011delayed, lamichhane2017impact, nishimura2007internal, nakabugo2008universal, behrman2014the, wallstrom2017is, valente2015primary, evans2020education.
