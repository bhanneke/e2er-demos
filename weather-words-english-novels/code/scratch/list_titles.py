import sqlite3, re
con = sqlite3.connect("data.db")
tok = re.compile(r"[a-z]+(?:['’][a-z]+)?")
for c in range(1, 7):
    for i, t, a, b, tx, sub in con.execute(f"select id,title,authors,author_birth_year,text,subjects from gutenberg_texts_c{c}"):
        n = len(tok.findall(tx.lower()))
        print(c, i, n, b, a[:25], "|", t[:50], "|", (sub or "")[:60])
