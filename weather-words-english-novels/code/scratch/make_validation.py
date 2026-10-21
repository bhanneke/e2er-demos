"""Combine the hand judgments (made by reading every passage of validation_sample.json) with the sample's own
doc_id/term/quote fields and write text_validation.json. Judgments are keyed by item position within each measure.
Also prints precision per term and cohort for text_validation.md."""
import json
from collections import defaultdict

S = json.load(open("validation_sample.json", encoding="utf-8"))

# wrong[measure][position] = reason
WRONG = {
    "weather_all": {
        0: "idiom 'jammed up in the wind' = cornered, not a wind",
        5: "'a dark cloud shaded his brow' describes a facial expression, no sky",
        7: "'misty glow' of affection/tears, not atmosphere",
        8: "'snowflake fluttering' of paper scraps: figurative use for something else",
        12: "'gusts of vapour' from boiling water/steam, not weather",
        16: "'sun-angel' is a mock-poetic compound address, not the sun",
        18: "'sunny disposition' is character, not weather",
        26: "'wind the clock': verb to wind, different word",
        28: "'stormy petrel' is a figure for a troublemaker (person), not a storm",
    },
    "precipitation": {
        0: "'warm shower' of blood: spray of liquid, not rain",
        4: "'fragrant showers' from pipes in an amphitheatre: artificial sprinkling",
        6: "'crowns rained upon them': money metaphor",
        8: "'shower of bills': mail/accounts metaphor",
        12: "'shower of tears': weeping metaphor",
        16: "'showers of notes': music metaphor",
        21: "'rain of disks' in a pyrotechnic vision: not rain",
        23: "'rained blows': blows, not rain",
    },
    "wind_words": {
        8: "'scattered to the winds': fixed idiom for discarding",
        20: "'Soft Wind' is a character's name",
        21: "'gust of rage': emotion metaphor",
        22: "'too windy': long-winded speaker",
        23: "'windy guffaws': pompous/loud talk, not weather",
    },
    "storm_words": {
        1: "'domestic hurricane': household upheaval metaphor",
        4: "'voice of thunder': loud voice idiom",
        7: "'stormy excitement': emotion metaphor",
        11: "'storms and tempests' in verse: figurative for political/ecclesiastical troubles",
        14: "'tempestuous devil': a person's temper",
        16: "'words of thunder' of a light/star image: metaphor, no weather",
        18: "'lightning-like look': speed/ferocity of a glance",
        21: "'speed of lightning': speed idiom",
        22: "'rapidity of lightning': speed idiom",
    },
    "fog_words": {
        1: "'a mist seemed to pass over her sight': faintness, not atmosphere",
        4: "'all was mist': dizziness/confusion",
        5: "'mist that dimmed her eyes': tears",
        6: "'hazy' = vague, of an idea",
        16: "'hazy, nebulous way' of thought: vagueness",
        19: "'Mist' Pat'ick': dialect for 'Mister'",
        20: "'misty fires of opalescence': glowing visionary beings, not weather",
    },
    "snow_ice_words": {
        0: "'icy bosom': coldness of manner",
        4: "'icy barrier between themselves': emotional coldness",
        8: "'icy-cold water from the well': cold drink, no winter weather",
    },
    "sun_words": {
        3: "'the sunshine is brighter indoors' introduces a damsel: figure for a woman's brightness",
        6: "pun on 'sun myself in your presence' (a king): courtly figure",
        8: "the sun as a star in an astronomical (moon-voyage) passage, not weather",
        11: "'the ghost's sunshine' is moonlight in a ballad",
        18: "'sunny-haired' housemaid: hair colour",
        20: "'gilt, stiff rayed suns' are ornamental shapes in a fantasy vision",
    },
    "cloud_words": {
        4: "'a cloud of dust': dust, not sky",
        5: "'overcast with a shade of sadness': face, not sky",
        6: "'suspicious and overcast' countenance: face",
        7: "'a sneer overcast the gravity of her face': verb for facial expression",
        16: "'her glance clouded': mood",
        20: "'pacing a cloud of dust': dust",
    },
}
# fresh weather similes or weather metaphors that still evoke the phenomenon: judged right but counted as 'figurative-right' in the strict count
SIMILE = {
    "weather_all": {9: "simile of a tree in a gale", 27: "simile: words falling like icicles"},
    "precipitation": {9: "simile: sea spattered with burning hailstones"},
    "wind_words": {2: "'gale and sunshine' as a figure for good and bad times, in a sea story with real weather", 17: "simile 'delicious as a summer breeze'"},
    "storm_words": {3: "simile 'flash of lightning through a dark vault'", 12: "'close up in thunder' (sound of a storm) in a sea-voyage image", 20: "simile 'as though a storm-cloud should turn away'"},
    "fog_words": {},
    "snow_ice_words": {9: "simile: coffee blossoms like a field of snow"},
    "sun_words": {15: "simile: smile like sudden sunshine", 22: "simile: 'distinctness of bright sunshine'"},
    "cloud_words": {},
}

out = {}
rows = []  # (measure, doc, term, cohort, correct, strict)
for m, v in S.items():
    items = []
    for i, it in enumerate(v["items"]):
        ok = i not in WRONG[m]
        if ok:
            reason = ("[figurative-right] " + SIMILE[m][i]) if i in SIMILE[m] else f"[literal] '{it['term']}' names the weather or sky phenomenon in a weather scene or description"
        else:
            reason = WRONG[m][i]
        items.append({"doc_id": it["doc_id"], "term": it["term"], "quote": it["quote"], "correct": ok, "reason": reason})
        rows.append((m, it["doc_id"], it["term"], it["cohort"], ok, ok and i not in SIMILE[m], it["quote"]))
    nc = sum(x["correct"] for x in items)
    out[m] = {"items": items, "precision": round(nc / len(items), 4), "n_checked": len(items), "n_correct": nc}
json.dump(out, open("text_validation.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("per measure:")
for m, v in out.items():
    strict = sum(1 for r in rows if r[0] == m and r[5])
    print(m, v["n_correct"], "/", v["n_checked"], round(v["precision"], 3), "strict", strict, round(strict / v["n_checked"], 3))
tot = len(rows)
print("all", sum(r[4] for r in rows), tot, sum(r[4] for r in rows) / tot, "strict", sum(r[5] for r in rows) / tot)

# pooled, de-duplicated across measures (weather_all vs sub-dictionaries may draw the same hit)
seen = {}
for r in rows:
    seen.setdefault((r[1], r[2], r[6]), r)
pool = list(seen.values())
print("pooled unique", len(pool), "of", tot)


def table(keyf, label):
    d = defaultdict(lambda: [0, 0])
    for r in pool:
        k = keyf(r)
        d[k][1] += 1
        d[k][0] += r[4]
    print(label)
    for k in sorted(d):
        print(" ", k, d[k][0], "/", d[k][1], round(d[k][0] / d[k][1], 2))


table(lambda r: r[3], "by cohort")
table(lambda r: r[2], "by term")
table(lambda r: (r[3]), "by cohort (again)")
amb = ["sun", "sunny", "sunshine", "storm", "stormy", "cloud", "clouds", "fog", "snow", "wind", "windy", "shower", "showers", "rained", "mist", "misty", "hazy", "icy", "lightning", "thunder", "overcast", "gusts", "gust", "tempestuous"]
d = defaultdict(lambda: [0, 0])
for r in pool:
    if r[2] in amb:
        d[(r[2], r[3])][1] += 1
        d[(r[2], r[3])][0] += r[4]
print("ambiguous terms by cohort:")
for k in sorted(d):
    print(" ", k, d[k])
print("translation docs in sample:", sorted({r[1] for r in pool if r[1] in {"pg1258", "pg2759", "pg1608", "pg1235", "pg4067", "pg1748", "pg547", "pg1353", "pg83", "pg1290"}}))
print("non-novel docs in sample:", sorted({r[1] for r in pool if r[1] in {"pg1051", "pg2496", "pg6112", "pg357"}}))
