# Literature Review: Estimated Road Traffic Mortality and Its Measurement

Status: INCOMPLETE. No citable source in `literature.bib` covers the WHO estimation methodology, the Global Status Report on Road Safety series, or estimated-versus-official comparisons.

## What the library returned

`e2er-lit search` was run with three queries:

1. "WHO global status report on road safety road traffic deaths estimation"
2. "estimating road traffic deaths underreporting vital registration WHO"
3. "official versus estimated road traffic fatalities comparison countries"

Each query returned the same five local-library hits. None is a methods source for RS_198 or for the WHO estimation model:

- `ahanhanzo2018disability` (Benin, disability among accident victims, facility-based survey). Not relevant to mortality estimation.
- `phiri2018impact` (bus stickers on road traffic crashes). Not relevant to measurement.
- `nutbeam2025spinal` (spinal cord injury after motor vehicle collisions, retrospective ecological analysis). Not relevant to national mortality estimates.
- `katw2026validation` (road traffic noise along a Hungarian highway). Not relevant.
- `goodarzi2025the` (child road injury burden in Iran, from national estimates). Tangentially related to burden estimation, but it is a single-country application. It does not describe the WHO method and should not be cited for it.

## Methods-relevant gap

The paper needs citations for three things. None is in the library yet:

1. **WHO estimation methodology for RS_198.** The model draws on vital registration and survey data, and corrects for underreporting. The method source is the WHO technical documentation for the road traffic deaths estimates. It is not in `literature.bib`.
2. **Global Status Report on Road Safety series.** The paper needs the edition(s) that report the 2021 estimates. It also needs the edition that introduced the current estimation approach. Neither is in `literature.bib`.
3. **Estimated versus officially reported road deaths.** The paper needs a source that compares WHO estimates with police or official counts and explains the gap. None of the hits covers this.

I did not add these from memory. The citation rules say to cite only keys that resolve.

## Recommended next steps (for a human or a later run)

- Verify the exact WHO report titles, editions, and DOIs or URLs, then record each with `e2er-lit save <DOI-or-BibTeX>`. The save command needs a DOI or a full BibTeX entry, which requires access to the source.
- Allow WebSearch (currently denied in this session) or supply the WHO PDFs. With either, the three gaps can be closed.
- Once recorded, add the method sources to the methods section: the WHO estimation documentation for the indicator's construction, and the Global Status Report for the official-versus-estimated comparison.

## Known limitations to describe once sources are in place (not yet cited)

These are standard concerns in the field. They are listed here as items to source, not as established citations:

- Estimates are model-based, so cross-country differences partly reflect modelling choices, not only true mortality.
- Official counts depend on national police or registration systems, which vary in coverage and in the definition of a road death (for example, a 24-hour versus 30-day cutoff).
- Underreporting is corrected in the WHO model, so estimated rates for countries with weak registration depend heavily on the correction.
- Estimates for a given year are revised as new data arrive, so the 2021 values should be checked against the edition used.

## Sources & References

- No entries from `literature.bib` are used as methods sources. The five library hits above were reviewed and excluded.
