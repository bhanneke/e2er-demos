"""Reload planning: keep loaded novels with >= 30,000 words, fill the table to 20 ids with the next reserves of
data/sample_ids.csv (draw order). Rejected ids are remembered in data/rejected_ids.json."""
import json
import os
import re
import sqlite3
import pandas as pd

s = pd.read_csv("data/sample_ids.csv")
rej = json.load(open("data/rejected_ids.json")) if os.path.exists("data/rejected_ids.json") else []
con = sqlite3.connect("data.db")
tok = re.compile(r"[a-z]+(?:['’][a-z]+)?")
for c in ["c1", "c2", "c3", "c4", "c5", "c6"]:
    d = pd.read_sql(f"select id, text from gutenberg_texts_{c}", con)
    d["n"] = d.text.str.lower().map(lambda t: len(tok.findall(t)))
    keep = [int(i) for i in d[d.n >= 30000].id]
    rej += [int(i) for i in d[d.n < 30000].id]
    seen = set(rej) | set(keep)
    pool = [int(i) for i in s[s.cohort == c].sort_values("draw_rank").id if int(i) not in seen]
    new = keep + pool[: 20 - len(keep)]
    print(c, "kept", len(keep), "short", int((d.n < 30000).sum()), "pool left", len(pool), "ids", ",".join(map(str, new)))
json.dump(sorted(set(rej)), open("data/rejected_ids.json", "w"))
