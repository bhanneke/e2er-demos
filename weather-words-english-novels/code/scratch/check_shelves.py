import sqlite3, glob, collections
import pandas as pd

con = sqlite3.connect("data.db")
t = pd.concat([pd.read_sql(f"select id,title,authors,bookshelves,subjects from gutenberg_texts_c{i}", con) for i in range(1, 7)])
c = pd.read_sql("select source_id from corpus", con).source_id
t = t[t.id.isin(c)]
for r in t.itertuples():
    s = str(r.bookshelves) + ";" + str(r.subjects)
    sh = [x.strip() for x in str(r.bookshelves).split(";") if "Literature" in x and "British" not in x and "American" not in x]
    if sh or "ranslat" in s:
        print(r.id, r.authors, r.title[:40], sh, "TRANSL" if "ranslat" in s else "")
a = pd.concat([pd.read_csv(f) for f in glob.glob("data/gutenberg_books_c*.csv") + glob.glob("data/extra_c*.csv")]).drop_duplicates("id")
cn = collections.Counter()
for s in a.bookshelves.fillna(""):
    for x in s.split(";"):
        cn[x.strip()] += 1
print({k: v for k, v in cn.items() if "Literature" in k})
print(a.subjects.fillna("").str.contains("ranslat").sum())
