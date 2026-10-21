"""Phase 1: filter the catalogue frames and draw the ordered sample (seed 20261014). Writes data/sample_ids.csv."""
import glob
import json
import random
import re
import sqlite3
import pandas as pd

SEED = 20261014
BINS = {"c1": (1770, 1799), "c2": (1800, 1819), "c3": (1820, 1839), "c4": (1840, 1859), "c5": (1860, 1879), "c6": (1880, 1899)}

files = sorted(glob.glob("data/gutenberg_books_c*.csv") + glob.glob("data/extra_c*.csv"))
raw = pd.concat([pd.read_csv(f).assign(frame_file=f) for f in files])
flow = [{"step": "catalogue rows read (all frame files, with repeats)", "n": int(len(raw))}]
a = raw.drop_duplicates("id").copy()
flow.append({"step": "unique ebook ids", "n": int(len(a))})


def step(name, mask):
    global a
    a = a[mask(a)].copy()
    flow.append({"step": name, "n": int(len(a))})


step("language exactly en", lambda d: d.languages.astype(str).str.strip() == "en")
step("exactly one catalogue person (no ';' = no translator/editor/illustrator listed)", lambda d: ~d.authors.astype(str).str.contains(";"))
step("author birth year 1770-1899 recorded", lambda d: d.author_birth_year.between(1770, 1899))
step("plain text available, copyright not true", lambda d: (d.has_plain_text == 1) & (d.copyright.astype(str).str.lower() != "true"))
inc = re.compile(r"fiction|novel|romance|adventure|detective|historical|stories|gothic|love", re.I)
exc = re.compile(r"poetry|poems|drama|plays|short stories|essays|letters|children|juvenile|biograph|fairy|diaries|diary|autobiograph", re.I)
tag = a.subjects.fillna("") + " ; " + a.bookshelves.fillna("")
a = a[tag.str.contains(inc) & ~tag.str.contains(exc)].copy()
flow.append({"step": "fiction-type subjects/bookshelves, excluding poetry/drama/short stories/essays/letters/children's/juvenile/biography", "n": int(len(a))})
step("omnibus/collections dropped by title", lambda d: ~d.title.astype(str).str.contains(r"complete|collected|works of|tales|stories|poems|selected|volumes? [ivx0-9]+|vol\.", case=False, regex=True))
a["norm_title"] = a.title.astype(str).str.lower().str.replace(r"[^a-z0-9 ]", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
a["norm_title"] = a.norm_title.str.split(" or ").str[0].str.replace(r"^(the|a|an) ", "", regex=True)
a = a.sort_values("id").drop_duplicates(["norm_title", "authors"])
flow.append({"step": "de-duplicated by normalised title + author (lowest ebook number kept)", "n": int(len(a))})
a["author_birth_year"] = a.author_birth_year.astype(int)
a["cohort"] = a.author_birth_year.apply(lambda y: next(k for k, (s, e) in BINS.items() if s <= y <= e))
rng = random.Random(SEED)
out = []
for c in BINS:
    d = a[a.cohort == c].sort_values("id")
    ids = list(d.id)
    rng.shuffle(ids)
    per_author = {}
    rank = 0
    for i in ids:
        r = d[d.id == i].iloc[0]
        if per_author.get(r.authors, 0) >= 2:
            continue
        per_author[r.authors] = per_author.get(r.authors, 0) + 1
        rank += 1
        out.append({"cohort": c, "draw_rank": rank, "id": int(i), "title": r.title, "authors": r.authors,
                    "author_birth_year": int(r.author_birth_year), "author_death_year": r.author_death_year})
    print(c, "eligible", len(d), "authors", d.authors.nunique(), "after 2/author cap", rank)
    flow.append({"step": f"eligible {c} (after cap of 2 per author)", "n": rank})
s = pd.DataFrame(out)
s.to_csv("data/sample_ids.csv", index=False)
json.dump(flow, open("data/draw_flow.json", "w"), indent=1)
for c in BINS:
    print(c, ",".join(str(x) for x in s[(s.cohort == c) & (s.draw_rank <= 20)].id))
