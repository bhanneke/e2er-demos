# Hand-check of dictionary hits

## Sample and procedure

The sample is `validation_sample.json` (seed 20261014), drawn by `run_estimation.py` on the corrected corpus (84 novels, six cohorts, translations removed). It covers eight dictionary measures: `weather_all` (30 items) and `precipitation`, `wind_words`, `storm_words`, `fog_words`, `snow_ice_words`, `sun_words`, `cloud_words` (24 each), 198 items in all. The hit populations behind the measures are 787 to 10,540. The strata are the six cohorts: each has 5 items in `weather_all` and 4 in every other measure, so 33 items per cohort. Within each cohort cell the draw puts ambiguous terms first (shower, thunder, icy, cloud forms, sun, storm and similar), so they are oversampled by design. The numbers below are therefore precision in a cohort-balanced sample that is not weighted by how often each term occurs, and not corpus-weighted precision.

I read every one of the 198 passages (about 200 characters around the hit) and judged each by hand; no script judged any item, and the reason for each is in `text_validation.json`. The script that wrote the file could not be run in this session, so the JSON, its per-measure counts and every table below were written and added up by hand, and the quotes were copied from the sample.

**Criterion.** A hit is *correct* when the word, in its passage, names the weather or sky phenomenon the measure assumes. A weather image whose vehicle is the phenomenon itself and that describes a scene or what the phenomenon does (a gale one leans into, the sun lighting a dell, flatteries falling like rain) is also correct. Its reason carries the tag `[figurative-right]`; the 9 such items are the gap between lenient and strict precision. A hit is *wrong* when it is:

- a figure for a person, mood, speech or event ("storms and disappointments", "domestic hurricane", "clouded every enjoyment", "chill fog between them", "icy civility", "lightning of conscience");
- a fixed idiom of speed, force or manner ("pounced like lightning", "thundering good breakfast", "pure as snow", "under a cloud", "work in the sunshine");
- another sense of the word ("walls wind up", "hurricane lantern", "cloud of water", "standing fog" meaning dry grass in Cooper, steam, smoke or gasoline "haze", a "hazy" scarf, painted clouds, noise of surf as "thunder");
- a name ("Colonel Rutherford Snow", "Sun Dance", the newspaper "the Sun") or the sun as a cosmic body or god.

## Results by measure

| Measure | Correct / checked | Precision (lenient) | Precision (strict, literal only) |
|---|---|---|---|
| weather_all | 22 / 30 | 0.733 | 0.633 |
| precipitation | 21 / 24 | 0.875 | 0.833 |
| wind_words | 21 / 24 | 0.875 | 0.792 |
| storm_words | 10 / 24 | 0.417 | 0.375 |
| fog_words | 12 / 24 | 0.500 | 0.500 |
| snow_ice_words | 20 / 24 | 0.833 | 0.792 |
| sun_words | 20 / 24 | 0.833 | 0.792 |
| cloud_words | 14 / 24 | 0.583 | 0.583 |
| **All items** | **140 / 198** | **0.707** (Wilson 95% CI about 0.64 to 0.77) | **0.662** |

`storm_words` (0.42), `fog_words` (0.50) and `cloud_words` (0.58) are well below the 0.7 line: for these three the paper must say that between four and six in ten hits are not weather, and `weather_all` sits on the line (0.73). `precipitation`, `wind_words`, `snow_ice_words` and `sun_words` are at 0.83 to 0.88 with 24 items each, so each interval is roughly ±0.15.

## Results by term (pooled over all eight samples, so a term can appear in two measures)

Cells are small. Only the patterns carry weight, not the second decimal.

| Term (forms) | Correct / checked | Precision | Wrong hits |
|---|---|---|---|
| rain, rains, rained, rainy | 19 / 19 | 1.00 | none |
| shower, showers | 3 / 6 | 0.50 | arrows, "shower of buffets", "shower on shower of stones" |
| showery | 1 / 1 | — | |
| breeze, breezes | 11 / 11 | 1.00 | none |
| wind, winds | 7 / 8 | 0.88 | verb "wind up" |
| gale | 6 / 9 | 0.67 | "wind of praise" and "gale of spears" in verse, "a regular gale" of laughter |
| gust, zephyr | 2 / 2 | — | |
| storm, storms, stormy | 3 / 7 | 0.43 | political storm, "stormy placing", "stormy excitement", "storms and disappointments" |
| thunder, thundered, thundering | 1 / 6 | 0.17 | surf, song, music of the spheres, intensifier |
| lightning | 6 / 11 | 0.55 | speed ("like lightning"), "lightning calculation", conscience, eyes, a sudden realisation |
| hurricane | 1 / 4 | 0.25 | "domestic hurricane", "let in a hurricane" (a draught), hurricane lantern |
| squall, tempest | 3 / 3 | — | |
| fog, foggy | 4 / 8 | 0.50 | "standing fog" (grass), chill fog between people, fog in the mind, "night of fog" |
| mist, mists, misty | 7 / 13 | 0.54 | cigar smoke, vats of the stockyard, cosmology, "mist of metaphysics", obscurity, "misty blue" eyes |
| haze, hazy | 3 / 8 | 0.38 | "as in a haze", a hazy scarf, gasoline fumes, a "hazy" conclusion, "blue haze round his hair" |
| snow, snows, snowy | 12 / 14 | 0.86 | "pure as snow", the surname Snow |
| frost, frosty | 2 / 3 | — | "blighting frosts" of age |
| icy | 5 / 6 | 0.83 | "icy civility" |
| icicles, thaw | 2 / 2 | — | |
| sun | 6 / 9 | 0.67 | sun god, Sun Dance, newspaper "the Sun", cosmic suns |
| sunshine | 6 / 7 | 0.86 | "work in the sunshine" |
| sunny, sunlight, sunbeams | 12 / 13 | 0.92 | "heart into the sunlight" (mood) |
| cloud, clouds | 5 / 10 | 0.50 | steam, painted clouds, "cloud of water", "clouds of birds", "under a cloud" |
| clouded, cloudy, overcast | 1 / 5 | 0.20 | "clouded every enjoyment", an overcast brow or countenance, cloudy eyes |
| cloudless | 12 / 13 | 0.92 | "cloudless pleasure" |

## Results by cohort (all measures pooled, 33 items per cohort)

| Cohort | Correct / checked | Precision |
|---|---|---|
| c1 | 24 / 33 | 0.73 |
| c2 | 22 / 33 | 0.67 |
| c3 | 23 / 33 | 0.70 |
| c4 | 28 / 33 | 0.85 |
| c5 | 25 / 33 | 0.76 |
| c6 | 18 / 33 | 0.55 |

By measure and cohort (correct of 4, `weather_all` of 5):

| Measure | c1 | c2 | c3 | c4 | c5 | c6 |
|---|---|---|---|---|---|---|
| weather_all | 5/5 | 4/5 | 4/5 | 4/5 | 3/5 | 2/5 |
| precipitation | 3 | 4 | 4 | 3 | 3 | 4 |
| wind_words | 3 | 4 | 2 | 4 | 4 | 4 |
| storm_words | 1 | 2 | 0 | 2 | 4 | 1 |
| fog_words | 3 | 1 | 3 | 3 | 2 | 0 |
| snow_ice_words | 3 | 3 | 3 | 4 | 4 | 3 |
| sun_words | 4 | 3 | 4 | 4 | 3 | 2 |
| cloud_words | 2 | 1 | 3 | 4 | 2 | 2 |

Each cohort cell has 4 or 5 items, and a cohort total has an interval of about ±0.16. Only the contrast between the ends carries weight: c6 (0.55) against c4 (0.85), and nothing else. The low c6 rate comes from fog (0 / 4: "blue haze round his hair", "cleared the fog from my mind", gasoline haze, a "mist" of obscurity, plus "night of fog"), storm words (idiom of speed and the intensifier "thundering", a hurricane lantern), "sun" as the newspaper and as a figure for openness, and cosmological "mists" and "thunder of the spheres" in a speculative novel (pg765). Terms of weather are used more often for states of mind and for speed in the later cohorts' prose, but the sample cannot say how much more. If the false-positive share differs by cohort like this, part of a raw cohort difference in dictionary frequency is figurative or non-weather use, not weather description.

## Terms to drop or disambiguate

The recommendations rest on 3 to 19 items per term and are for the researcher to weigh. A term judged "drop" has a precision below 0.5 here and, in the passages read, no weather sense that a simple rule would rescue.

- **Drop from the weather measures:** thunder, thunders, thundered, thundering (1 / 6; the weather sense is rare and the intensifier and "thunder of" sound are common); hurricane (1 / 4); haze, hazy (3 / 8); clouded, cloudy, overcast (1 / 5, used for faces, moods and eyes); and `cloudy` and `clouded` in particular.
- **Disambiguate or report separately:** storm, stormy (3 / 7): count only with a weather context word within a few tokens (rain, wind, sea, night), or report the term apart from `storm_words`; lightning (6 / 11): exclude "like lightning", "lightning calculation" and "flash"; shower, showers (3 / 6): exclude "shower of"; fog and mist (4 / 8 and 7 / 13): the weather senses are mostly literal in land and sea scenes and figurative for confusion; cloud, clouds (5 / 10): exclude "cloud of" and "under a cloud"; gale (6 / 9); sun (6 / 9): exclude a capitalised "Sun" (names, newspaper) and "sun god"; snow: exclude a capitalised "Snow" after a first name or title (the surname); icy and frost: figurative in about one hit in five or six.
- **Keep:** rain forms (19 / 19), breeze forms (11 / 11), wind (7 / 8), cloudless (12 / 13), sunny, sunshine, sunlight (17 / 19), snow, snowy, snows (12 / 14), thaw, icicles.

A proper-name rule is easy to add because the surname and title cases are capitalised in mid-sentence ("Colonel Rutherford Snow", "the Sun Dance", "the Sun"); the other cases need context.

## What this means for the measures

- The composite `weather_all` (0.73 lenient, 0.63 strict) is acceptable but mixes terms of very different quality: the noise comes from storm, thunder, fog-and-haze and cloud words, while rain, wind, breeze, snow and sun words are clean. Cohort comparisons should be shown for the clean families first (`precipitation`, `wind_words`, `snow_ice_words`, `sun_words`) and for `weather_all` without the dropped terms as a robustness check.
- A rise or fall in `storm_words`, `fog_words` or `cloud_words` across cohorts cannot be read as weather change without this caveat: at 0.42 to 0.58 precision, a change in figurative use alone could move the count.
- Precision says nothing about recall. Weather described without any of the listed forms (a "downpour" is listed, "pouring", "drenched", "chilly", "blew", "dark skies" are not) is missed, and the dictionary is written for this study, not published.
- The sample is small and not corpus-weighted. The Wilson intervals show that differences of a few hundredths between terms or cohorts are not distinguishable.

## Corpus caveat

The sample was drawn after the corpus was corrected: translations were excluded (the earlier sample, which had translated texts, is superseded). All 198 passages come from English-language works in the 84-novel corpus, so figurative uses by translators are no longer in the sample. Verse and songs inside novels (Hogg, Scott, MacDonald, Haggard, Melville) produce a few of the wrong hits ("gale of spears' breath", "wind of praise"); they are part of the text as analysed.
