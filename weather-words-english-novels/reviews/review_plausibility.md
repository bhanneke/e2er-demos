# Plausibility Review: Vocabulary of Weather in English-Language Novels by Author Birth Cohort

Scope: whether the numbers and patterns make sense for what is measured (weather words per 10,000 tokens in a Gutenberg novel sample). Number tracing to the results files is done elsewhere. Items marked [domain] rest on my own knowledge, not on the paper or its files. The `\input` tables were not in my context, so I could not check them. I worked from the in-text numbers.

## 1. What I checked and found plausible

- **Corpus arithmetic.** The cohort token counts sum to 9,248,093. The hit counts sum to 10,540. These reproduce the pooled rates (c1 1,933/174.30 = 11.09; c2 10.81; c4 13.32; c6 11.11; corpus 11.40).
- **Spearman values.** The rho/p pairs are exact for n = 6 (0.60/.208, 0.83/.042, 0.77/.072, -0.94/.005, and others). The composite rho of 0.60 reproduces from the six pooled rates.
- **Keyness log ratios.** Those I recomputed from the counts and token shares agree: tempest c1 2.09, sunlight c1 -4.25, fog c2 -2.83, mist c4 1.01, misty c6 1.54, snow c5 1.04.
- **Document lengths.** The maximum of 320,232 tokens fits *Middlemarch* [domain]. The c2 mean length of about 170k fits the long mid-century novels in that cohort.
- **Magnitudes.** A composite rate of 11 per 10,000 (0.11%), with family rates of 0.4–3 per 10,000, is a plausible order of magnitude for narrative prose [domain]. I found no unit slip.
- **Tempest.** The decline of *tempest* as a poetic or archaic word across the nineteenth century agrees with general lexical history [domain].
- **Validation.** The validation arithmetic is consistent: 140/198 = 0.71, and the per-family fractions round correctly. The ±0.16 interval for n = 33 is right for a simple binomial.

## 2. Implausible, unexplained or over-interpreted items

### A. Orthography and tokenisation may produce the "light" and "storm" patterns (high priority)

1. **Hyphenation.** The tokenizer `[a-z]+(?:['’][a-z]+)?` splits hyphens, and the dictionary matches exact closed forms. Nineteenth-century texts, especially early ones, often write *sun-shine, sun-light, sun-beam, snow-storm, thunder-storm, sea-fog, rain-drop* [domain]. Closing-up of such compounds over the century is a well-known orthographic drift [domain].
   - Consequence 1: the finding that c1 is "relatively poor in *sunlight* (2 vs 164 occurrences, log ratio -4.25) and *sunshine*" is a 20-fold difference in a common word. That is exactly what a spelling convention produces.
   - Consequence 2: the inference that "later cohorts favour the vocabulary of light" is not safe. It may be spelling, not vocabulary.
   - Consequence 3: a hyphenated *thunder-storm* or *snow-storm* produces two dictionary hits (*thunder* + *storm*) for one event. The collocation result "thunder storm (12)" shows the split is occurring. Rates for storm and snow words are therefore inflated, and by an amount that depends on the period's hyphenation habits.
   - Check: count `sun-?light`, `sun-?shine`, `snow-?storm`, `thunder-?storm` in the raw texts by cohort. Then rerun keyness and the family rates with hyphens treated as joiners, or with hyphenated compounds counted once.
2. **Dialect and eye-dialect (recall bias that varies by cohort).** The apostrophe rule keeps *rainin'* as the token "rainin", which is not in the dictionary. Scots-heavy c1 (Hogg, Galt, Scott), Hardy's dialect in c4, and the cowboy and frontier dialect of c5–c6 (Mulford, Kyne, Connor) will lose weather hits (*snaw, rainin', blowin'*) [domain]. The paper lists missed inflections (*blew, pouring*) but not the possibility that recall differs systematically across cohorts.
   - Check: list the most frequent unmatched tokens within a character window of "weather" contexts for each cohort. Alternatively, run a lemma-based or stem-based variant, which the plan promised but the paper never ran.
3. **The word "weather" itself, *sky* and *lightning*-type items.** The head noun *weather* and *sky* are absent from the list, even though the research question is about "weather". The paper does not say why. State the reason or run the extended list from the plan.

### B. The headline "stable composite" is not distinguishable from measurement drift in precision

4. **Precision falls across cohorts.** By cohort it runs from 0.85 (c4) to 0.55 (c6). The composite rates are flat (11.09 vs 11.11). If the c6 hits are about 55% weather and the c4 hits about 85%, the true rate of weather description is not flat, and the plausible direction is a lower c6. The paper notes that "part of a raw cohort difference can reflect figurative use" but still calls the profile "remarkably stable", and leads the abstract with "stable". Both statements cannot hold: a stable raw count with unequal precision is evidence of change, not stability.
   - Check: estimate precision-adjusted cohort rates, with precision computed per term and weighted by the corpus term mix, not by the stratified sample.
5. **The 0.71 "overall" precision is not an interpretable figure.** It pools a composite sample and seven family samples that overlap in hits. It also deliberately places ambiguous terms first in each cohort cell, so false positives are over-represented, and the paper itself says it is not corpus-weighted. It still appears in the abstract and introduction as "precision of the dictionary is 0.71 overall".
   - Check: report the term-weighted precision, with an interval, in place of 0.71, or drop the pooled figure.
6. **Cells of 4 and 6 items carry large claims.**
   - "None of four sampled fog hits in cohort 6" is 4 items. The 95% interval for 0/4 runs to about 0.60, so the data are also compatible with most c6 fog hits being weather.
   - "Thunder forms were judged correct in only one of six" is 6 items. Literal thunder is the dominant sense in most fiction [domain], and the adventure-era thunder of guns and hooves does not make it so for the whole field.
   - The reduced lexicon then deletes every thunder form on that basis, which also deletes literal thunder.
   - Check: hand-code all c6 fog and mist hits (about 180 by my arithmetic from 1.53 per 10,000 × 119 ten-thousands of tokens) and all thunder hits. Both are small enough.
7. **Coding rule for "sun".** Sun judged "wrong" when it is a god or a cosmic body (SF such as *Gulliver of Mars* or *The Moon Pool*, and myth in c1) treats the sun as non-weather in some contexts. Sun-as-light is normally counted as weather vocabulary. State the rule and check how many sun "errors" come from it.

### C. Corpus selection that plausibly produces the cohort profile

8. **Cohort 6 is truncated by copyright.** Authors born 1880–1890 enter only through works published before about 1930 (US public-domain cut), so c6 consists of early-career output, whereas c1 and c2 include whole careers [domain]. The age-at-writing confound is therefore not just "unseparable" but one-sided. No author born 1891–1899 qualified (the paper notes max 1890). The advertised "1880–1899" cohort is a 1880–1890 cohort of about 9 authors.
   - The plan's hypothesis (c) (a modernist retreat from set-piece weather) cannot be tested with a c6 made of westerns (Mulford), detective and SF pulp (Christie, Rohmer, Merritt), and Lewis. Woolf, Joyce and Lawrence-type authors [domain] are not in it.
9. **Genre and setting drive the families.**
   - The c5 snow peak (snow 1.32 per 10,000, above rain 0.87) coincides with northern and logging settings in the cohort list (Curwood, Connor, White, Sinclair) [domain].
   - c1's storm and tempest excess coincides with the sea novels (Cooper's *The Pilot*, *Tom Cringle's Log*).
   - These are setting effects, not "cohort vocabulary". Attributing them to cohort needs a genre or setting control, which the plan listed but the paper does not provide.
   - The snow-and-ice Spearman of 0.83 (p = .042) depends on one cohort peak. The leave-one-author-out and heaviest-novel checks are run only for the composite. They should be run for the snow family. Report the per-novel counts for *snow* in c5.
10. **The popularity frame is not verifiable and contradicts the data summary.**
    - The paper says the frame is sorted by download count and that eligibility required "not under copyright". The data summary says `copyright` and `download_count` are empty in the extract and "not used".
    - So the ordering and the copyright filter cannot be evidenced from the catalogue table, and the "favours popular books" statement has no data behind it.
    - Check: state the source of the ordering (Gutendex default) and of the public-domain status.
11. **The size of c2 (14) comes from the search design, not from scarcity.**
    - The data summary says the c2 pool was "exhausted". Project Gutenberg holds far more than 14 English novels by authors born 1800–1819 (Trollope, Dickens, Thackeray, Kingsley, Disraeli, Poe, Gaskell, and others) [domain].
    - The 320-row popularity cap per search, applied to a window of authors alive 1800–1880, crowds out the cohort with later-born authors.
    - This matters because the equal-n cut then discards 21 eligible novels, and the 14 per cohort are the most popular survivors of a truncated list.
    - Check: report, per cohort, how many catalogue rows in the frame fell inside the birth-year window.
12. **Fog and the Dickens expectation.**
    - c2 has 9 fog tokens in 2.39 million tokens, although the cohort includes Dickens (born 1812), the Brontës, Eliot and Thackeray. The paper uses Dickens's fog to motivate the study, then reports c2 as having the least fog.
    - The sampled Dickens is *Barnaby Rudge* [domain: a historical novel set in 1780, not the London-fog novels *Bleak House* or *Our Mutual Friend*].
    - The paper does not say that the sampling of one title per author is why the known Dickensian fog is not in the data. It should say so and report fog counts per author.
    - Check: list fog and mist hits by novel for c2–c4.

### D. Interpretations that exceed the numbers

13. **"Stable" versus "unresolvable".**
    - The c2 interval is 7.01–15.32 and the c4 interval 10.87–15.71, so the data cannot exclude shifts of 30–40% in either direction. "Stable" or "remarkably stable" is stronger than "no cohort difference is detectable at 9–14 authors per cohort".
    - "Differences between authors are larger than differences between cohorts" compares the range of 69 author rates (2.10–31.35) with the range of six pooled cohort rates. These are different kinds of quantity. A variance decomposition (between-cohort versus within-cohort variance of author rates) is the appropriate comparison.
14. **Leave-one-author-out claim.** "No single author reverses a cohort's position" is contradicted by the paper's own numbers. c1 ranges from 9.42 to 12.29, a span that covers the whole range of cohort rates (10.81–13.32), and c1, c2, c3 and c6 differ by only 0.3. Their order is not meaningful.
15. **Keyness readings.** "The sky in motion (tempests, gales, clouds)" is drawn from *clouds*, a family with 0.58 precision and no term-level check. "Mist and its relatives are more frequent in cohorts 4 and 6" and the key term *misty* (c6) are fog-family items. The fog family is the one the hand check found to be non-weather (smoke, steam, "misty eyes" [domain: a common sentimental idiom]). No caveat is attached to these in the keyness section.
16. **Minor numerical point.** For *tempest* the paper says the reference is "five times as large". From the token counts it is 4.3 times (7.50 million versus 1.74 million).
17. **Multiplicity.** The count of "15 profiles" covers neither the post-hoc variants nor the keyness lists. The expectation of "one" false positive is 15 × 0.05 = 0.75 on independent tests; the profiles are correlated (snow term and snow family count as two). The post-hoc storm p = .005 is chosen from a list defined after seeing the data, and the removal of forms by a validator whose sample was drawn from the same outcome cannot be treated as a test. The paper states most of this, which is appropriate. The abstract should still keep the storm "fall" out of the findings.

## 3. Checks that would settle the main issues

1. Hyphen-sensitive recount: sun-light, sun-shine, snow-storm, thunder-storm and similar compounds by cohort (item A1).
2. Precision by term, weighted by term frequency, and precision-adjusted cohort rates (B4, B5).
3. Hand-coding of all c6 fog and mist hits and all thunder hits (B6).
4. Per-novel and per-author breakdown for snow (c5), fog (c2–c4) and storm (c1), plus leave-one-out for each family (C9, C12).
5. Variance decomposition between cohorts and authors, and a genre or setting tag (sea, frontier, northern) as a covariate (C9, D13).
6. Frame depth by cohort and the reason c2 was "exhausted" (C11).
7. Dialect and elided-form recall check (A2).

## 4. Overall judgement

The arithmetic is clean and the paper is honest about most of its limits. The weak points are measurement and selection. Orthographic and dialect effects can shift the dictionary counts differently by cohort. The precision gradient undermines the "stable" headline. c6 is a copyright-truncated early-career slice, and setting and genre are not separated from cohort. Several interpretive sentences go further than the hand-check supports.

OVERALL SCORE: 5.5/10
RECOMMENDATION: Major Revision
