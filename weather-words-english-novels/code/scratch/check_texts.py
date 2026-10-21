import sqlite3, re, json
con = sqlite3.connect("data.db")
tok = re.compile(r"[a-z]+(?:['’][a-z]+)?")
rej = set(json.load(open("data/rejected_ids.json")))
for c in range(1, 7):
    rows = con.execute(f"select id,authors,words,text from gutenberg_texts_c{c}").fetchall()
    n = [len(tok.findall(r[3].lower())) for r in rows]
    print(c, "ok", sum(x >= 30000 for x in n), "short", [r[0] for r, x in zip(rows, n) if x < 30000],
          "in rejected", len(set(r[0] for r in rows) & rej))
