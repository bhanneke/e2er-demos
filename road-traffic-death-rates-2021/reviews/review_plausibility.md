# Plausibility Review: Estimated Road Traffic Death Rates across Countries and WHO Regions, 2021

## Summary

The magnitudes are plausible. Rates of 0 to 37.4 deaths per 100,000 are in the range WHO publishes for RS_198. The high-tail and low-tail countries match what the field would expect, and the rank listings are internally consistent: the region counts in the top and bottom ten sum correctly (5 AFR, 3 EMR, 1 AMR, 1 SEAR at the top; 7 EUR, 2 WPR, 1 SEAR at the bottom), and the four countries above 30 are exactly Guinea, Libya, Haiti and Guinea-Bissau.

The problems are about reconciliation, not magnitude. The paper presents unweighted country means as regional averages without saying so, and never sets them against WHO's own regional estimates, one of which differs by 4.4 points. The membership count does not match WHO's, the raw extract has an unexplained "0.0" text value for two excluded countries, and the uncertainty bounds are entirely absent in a way that should be checked before the Limitations section is written. Items marked "own knowledge" come from my general knowledge of the field and were not verified against a source in this run.

## Findings

### 1. Membership and sample count (major)

- Location: Abstract ("195 countries"); Introduction ("for each Member State"); Section 2.2 (N = 195); Section 3.2 (region counts AFR 47, AMR 36, EMR 22, EUR 53, SEAR 9, WPR 28).
- Own knowledge, to verify: WHO has 194 Member States, with 11 in South-East Asia and 35 in the Americas. The analysed set of 195 is therefore one larger than the Member States. It includes Niue, which is an associate member, and possibly other non-members. The SEAR count of 9 is two short of the regional total, and the AMR count of 36 is one above it.
- Why it matters: the paper says the sample covers Member States. If the set includes associates and omits some Member States, the sample label and the N are both wrong.
- Check: list the 197 COUNTRY locations against the WHO Member State list. Name any associate members in the sample and any Member States absent from the extract, and give the reason for each absence (no 2021 estimate, or not in the extract). Then either correct the Member State wording or state the sample as "countries with an RS_198 estimate for 2021".

### 2. Unweighted country means presented as regional averages (major)

- Location: Abstract ("The African region averages 19.4"); Introduction ("Regional averages range from 6.7 ... to 19.4"); Section 3.2 and Table regions; Conclusion.
- The regional and national means are unweighted means across countries (estimation spec, groups and statistics). The WHO REGION rows in the data summary are the published regional estimates, and the draft never reports them.

| Region | Unweighted country mean (paper) | WHO REGION row (data summary) |
|---|---|---|
| AFR | 19.44 | 19.4 |
| AMR | 14.1 | 14.1 |
| EMR | 16.7 | 16.4 |
| EUR | 6.70 | 6.7 |
| SEAR | 15.9 | 16.1 |
| WPR | 10.8 | 15.2 |

- Two regions match to one decimal, and WPR differs by 4.4 points. The small gaps for EMR and SEAR are what one would expect from different weighting. A gap that large in WPR is not explained by the text. My own knowledge is that WPR contains very populous countries with rates well above the regional unweighted mean, which would pull a population-weighted estimate upward. This is plausible but has not been checked here.
- The global value of 15.0 is also a weighted figure, against an unweighted country mean of 13.3. The same weighting explanation applies.
- Check: (a) state in the text that the regional and national means are unweighted country means; (b) report the WHO REGION rows and the GLOBAL row next to them; (c) confirm from the GHO metadata how the REGION rows are computed, since the exact match for AFR and EUR is worth a look before the paper calls them "regional averages"; (d) explain the WPR gap, ideally with population-weighted means computed from the same data or a population source.

### 3. Zero values and the raw "0.0" text for HKG and MAC (major)

- Location: Section 2.2 ("no numeric value ... excluded"); Section 3.3 ("the only two zero values in the sample").
- Monaco and Niue are recorded as exactly 0.0. For a model-based estimate, an exact zero is unusual. A zero count is plausible for a population of about 1,600 (Niue) or about 39,000 (Monaco), but a model output of exactly zero suggests either a count-based value or a floor in the model. The paper's statement that a zero is "more plausible" in small populations is an assertion, not a check.
- The data summary says `value_text` for HKG and MAC reads "0.0", while the numeric value is null. So the raw extract has three "0.0" strings in total, and the paper mentions only the null numeric value. If the text is the published value, excluding HKG and MAC is a parsing decision that changes the zero story.
- Check: inspect the raw JSON for MCO, NIU, HKG and MAC. Confirm whether `Value` is a count, a model output, or a placeholder, and whether the `value_text` for HKG and MAC is the published value or a display string. Report the decision in Section 2.2 and state whether the two zeros are counts or model outputs.

### 4. All uncertainty bounds are null (major, to verify)

- Location: Data dictionary (`low`, `high`); Section 2.2 and Section 4 (Limitations, second paragraph).
- The draft states that the API returns no `low` or `high` for any of the 197 rows. Own knowledge, to verify: WHO has published uncertainty intervals for road traffic death estimates in its reports, and the GHO endpoint may expose them. A total absence across 197 rows looks more like a field-name or filter problem than a fact about the series.
- Why it matters: if the bounds exist, the Limitations section is wrong, the Spearman association between value and interval width (currently null) can be computed, and the claim that "no bounds" constrains the ranking becomes an artifact of the extraction.
- Check: fetch one country record (for example GBR or NGA) and inspect every key in the raw JSON for Low and High or any similar field. If bounds exist, rerun the association and rewrite the second Limitations paragraph. If they do not, state the check and the endpoint used.

### 5. Age standardisation (major for interpretation)

- Location: Section 2.1 ("The GHO response does not state whether the series is age-standardised"); Section 4 (third scope condition).
- Own knowledge, to verify: WHO's road traffic death rate estimates are, I believe, age-standardised. If so, the paper's age-composition caveat in Section 4 is misdirected, because the standardisation already removes most of the age-structure effect.
- Why it matters: the Europe result (lowest mean, 6.7) is exactly where the age-structure question bites. The text currently treats age composition as an open confound that the data cannot separate.
- Check: read the GHO indicator metadata for RS_198. Whatever it says, the paper should state the answer and align the Limitations paragraph with it. The current position of leaving the question open is defensible only until the metadata is read.

### 6. Missing cross-check against the Global Status Report (minor to major)

- Location: Data quality section (aggregates); planned cross-check in the plan's Section 5.
- The plan called for comparing the replicated aggregates (regional and global) against the WHO Global Status Report on Road Safety 2023. The draft does not report this check, and the data summary says the aggregates are "not recomputed here".
- Own knowledge, to verify: the 2023 report presents 2021 estimates including a global rate near 15 per 100,000, which matches the GLOBAL row of 15.0.
- Check: report the comparison with the figures in the report, and state any discrepancy with its likely cause (weighting, revision, or edition).

### 7. Ties at the cut-off (minor)

- Location: Section 3.3 (top ten, "Kenya and Nepal tie at 28.2"; bottom ten, "Switzerland and the United Kingdom (both 2.4)").
- The plan requires ties at the cut-off to be listed in full. The draft lists two ties at the boundaries and does not state whether a further country shares the value.
- Check: confirm the full list at 28.2 and 2.4 and state the cut-off rule.

### 8. Interpretation sentences that say more than the numbers support (minor)

- "WHO region membership explains about 39 percent of the total variation" (Introduction) versus "accounts for" (Section 3.2). The eta-squared is a descriptive share of variance between regions, not an explanation. Use one phrase, and use the descriptive one.
- "The lower tail of the distribution depends on them" (Section 3.3). The two zeros affect the minimum and the lowest percentiles only slightly. Say that the minimum depends on them.
- "The European region is the most homogeneous" (Section 3.2). Only the EUR standard deviation (3.8) is reported in the text. A comparison across regions needs the SD for all six, or the claim should be stated for Europe alone.
- "Right-skewed" is supported, though mildly. The mean (13.3) lies above the median (12.3), and the distances from the median to the quartiles are about 5.1 below and 5.8 above. "Mildly right-skewed" is the accurate description.

### 9. Figures and tables not available for check (note)

- The tables `tables/summary.tex` and `tables/regions.tex` are referenced but were not included in the material I received. The numbers in them could not be checked against the text. The histogram bin counts are described in the text ("most countries lie between 3.7 and 18.7", "four countries exceed 30") and are consistent with the ranked values, but the bin counts themselves were not available.

### 10. Citation year and data version (minor)

- The `WHO_GHO` citation says 2026, accessed 2026-10-13, while the data version is 2024-04-15. The reference should give the release version (2024-04-15) as the data vintage, and the access date separately.

## Values checked and judged plausible

- Highest rates: Guinea 37.4, Libya 34.0, Haiti 31.3, Guinea-Bissau 30.5, Syria and Zimbabwe 29.9, Yemen 29.8, Comoros 29.0, Kenya and Nepal 28.2. The magnitudes are in the range the field would expect for these countries (own knowledge, not verified against a source here).
- Lowest rates: Maldives 1.3, Malta and Singapore 1.9, Sweden 2.1, Denmark 2.3, United Kingdom and Switzerland 2.4. The UK, Sweden and Denmark values are consistent with their order of national road deaths per head (own knowledge). Norway at 1.5 is the value I would check first against national counts, because my rough recollection of Norwegian counts would put it nearer 2 (own knowledge, low confidence).
- Median 12.3, IQR 7.3 to 18.1, p5 2.4, p95 27.9, mean 13.3, SD 7.8: internally consistent with each other and with the histogram bin width (37.4 / 10 = 3.74).
- Regional ratio: 19.44 / 6.70 = 2.9, correctly described as "nearly three times".
- Eta-squared of 0.391, reported as 39 percent: consistent with the text.

## Verdict

The numbers are plausible in magnitude and the rank listings are internally consistent. The paper needs to reconcile its sample with WHO's membership, to state and explain the weighting of its regional means against WHO's regional estimates, to check the zero values and the raw "0.0" text, and to confirm from the GHO metadata whether bounds and age standardisation exist before the Limitations section is finalised.

OVERALL SCORE: 6/10
RECOMMENDATION: Major Revision
