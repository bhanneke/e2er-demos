"""Phase 1b (rerun): apply the researcher's translation / non-novel exclusions to the seeded draw order of
data/sample_ids.csv (draw ranks unchanged) and list, per cohort, which ids still have to be loaded.
Writes data/sample_ids_v2.csv (with exclusion reasons) and data/refill_ids.json."""
import glob
import json
import re
import sqlite3
import pandas as pd

TARGET = 20
cat = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("data/gutenberg_books_c*.csv") + glob.glob("data/extra_c*.csv"))]).drop_duplicates("id")
s = pd.read_csv("data/sample_ids.csv").merge(cat[["id", "bookshelves", "subjects"]], on="id", how="left", validate="1:1")
NON_ENGLISH = re.compile(r"Category: (French|German|Russian|Italian|Spanish|Scandinavian|Norwegian|Swedish|Danish|Finnish|Dutch|Portuguese|Polish|Czech|Greek|Latin|Japanese|Chinese)[^;]* Literature|Literature - Other", re.I)
MANUAL = {
    1258: "translation (Dumas)", 2759: "translation (Dumas)", 1608: "translation (Dumas)", 1235: "translation (Gautier)",
    4067: "translation (Muehlbach)", 1748: "translation (Gaboriau)", 547: "translation (Gaboriau)", 1353: "translation (Verne)",
    83: "translation (Verne)", 1290: "translation (Flaubert)",
    1051: "not a novel (Sartor Resartus)", 2496: "not a novel (Our Village, sketches)", 6112: "not a novel (Nature and Human Nature)",
    357: "not a novel (A Dream of John Ball)",
    4927: "not a novel", 4926: "not a novel", 477: "not a novel", 973: "not a novel",
}


def reason(r):
    if r.id in MANUAL:
        return MANUAL[r.id]
    if NON_ENGLISH.search(str(r.bookshelves)):
        return "bookshelf names a non-English literature"
    if re.search(r"translations? into english", str(r.subjects), re.I):
        return "subjects say Translations into English"
    return ""


s["exclude_reason"] = [reason(r) for r in s.itertuples()]
con = sqlite3.connect("data.db")
loaded = set()
for c in range(1, 7):
    loaded |= set(pd.read_sql(f"select id from gutenberg_texts_c{c}", con).id)
short = set(json.load(open("data/rejected_ids.json"))) | {581, 2695}
s["loaded"] = s.id.isin(loaded)
s["short_under_30k"] = s.id.isin(short)
s.to_csv("data/sample_ids_v2.csv", index=False)
out = {}
for c, g in s.groupby("cohort"):
    ok = g[(g.exclude_reason == "") & ~g.short_under_30k].sort_values("draw_rank")
    have = ok[ok.loaded]
    need = max(0, TARGET - len(have))
    pool = ok[~ok.loaded]
    out[c] = {"eligible_loaded": int(len(have)), "need": int(need), "pool_unloaded": int(len(pool)), "load_ids": [int(i) for i in pool.id.head(need)]}
    print(c, out[c], "excluded in draw:", g[g.exclude_reason != ""].id.tolist())
json.dump(out, open("data/refill_ids.json", "w"), indent=1)
