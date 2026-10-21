"""Build the corpus from the loaded Gutenberg texts (data preparation only: no cohort comparison, no test statistics).

Reads gutenberg_texts_c1..c6 from data.db, cleans front matter, applies the 30,000-token rule, excludes non-novels,
de-duplicates by text hash, cuts every cohort to the smallest n (draw order of data/sample_ids.csv, seed 20261014),
writes the tables corpus, corpus_token_counts, weather_dictionary_hits, corpus_cohort_summary, and the files
stopwords.txt, corpus_manifest.json, summary_statistics.json, figure_spec.json.
"""
import hashlib
import json
import re
import sqlite3
import unicodedata
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

DESIGN = json.load(open("corpus_design.json", encoding="utf-8"))
PRE = DESIGN["preprocessing"]
PATTERN = re.compile(PRE["token_pattern"])
COHORTS = ["c1", "c2", "c3", "c4", "c5", "c6"]
LABEL = {"c1": "1770-1799", "c2": "1800-1819", "c3": "1820-1839", "c4": "1840-1859", "c5": "1860-1879", "c6": "1880-1899"}
MIN_TOKENS = 30000
NON_NOVELS = {
    4927: "Bulfinch, Legends of Charlemagne: retold medieval legends, not a novel",
    4926: "Bulfinch, The Age of Chivalry: mythology/legend retelling, not a novel",
    477: "Ferri, Criminal Sociology: non-fiction treatise",
    973: "Pyle, Book of Pirates: mixed collection of stories and non-fiction",
}

open("stopwords.txt", "w", encoding="utf-8").write("\n".join(sorted(ENGLISH_STOP_WORDS)) + "\n")


def tokens(text):
    t = unicodedata.normalize("NFC", text)
    if PRE["lowercase"]:
        t = t.lower()
    return PATTERN.findall(t)


def quantile(sv, q):
    pos = (len(sv) - 1) * q
    lo, hi = int(pos), min(int(pos) + 1, len(sv) - 1)
    return sv[lo] + (sv[hi] - sv[lo]) * (pos - lo)


def clean(text):
    """Remove transcriber lines, illustration markers and a leading contents block; return (text, chars_cut)."""
    t0 = unicodedata.normalize("NFC", text).replace("\r\n", "\n")
    t = t0
    t = re.sub(r"^\s*(Produced by|Transcribed from|Transcribed by|E-text prepared by|Etext prepared by|Scanned by|Proofed by)[^\n]*(\n[^\n]+)*?(?=\n\s*\n)", "", t, count=1, flags=re.I)
    t = re.sub(r"\[(Illustration|Frontispiece|Decoration|Image)[^\]]*\]", "", t, flags=re.I)
    t = re.sub(r"\n[ \t]*\[?(Transcriber|Transcriber's|Editor's|Etext|Contributor)['’s]*\s*Note[^\n]*(\n[^\n]+)*", "\n", t, flags=re.I)
    head = int(len(t) * 0.08)
    m = re.search(r"\n[ \t]*(table of )?contents\.?[ \t]*\n", t[:head], flags=re.I)
    if m:
        rest = t[m.end():head + 4000]
        gap = re.search(r"\n[ \t]*\n[ \t]*\n[ \t]*\n", rest)
        if gap:
            t = t[:m.start()] + "\n" + t[m.end() + gap.end():]
    return t, len(t0) - len(t)


con = sqlite3.connect("data.db")
frames = []
for c in COHORTS:
    d = pd.read_sql(f"select id, title, authors, author_birth_year, languages, text from gutenberg_texts_{c}", con)
    d["table_cohort"] = c
    frames.append(d)
d = pd.read_sql("select id, title, authors, author_birth_year, languages, text from gutenberg_texts_c3_refill", con)
d["table_cohort"] = "c3"
frames.append(d)
raw = pd.concat(frames, ignore_index=True)
draw = pd.read_csv("data/sample_ids_v2.csv")[["id", "draw_rank", "exclude_reason"]]
raw = raw.merge(draw, on="id", how="left", validate="m:1")
raw["exclude_reason"] = raw.exclude_reason.fillna("")
raw.loc[raw.id == 750, "exclude_reason"] = "translation of a medieval text (Sebastian Evans), not a novel"
raw_all_n = len(raw)
excl = raw[raw.exclude_reason != ""]
raw = raw[raw.exclude_reason == ""].copy()
bins = {k: tuple(map(int, v.split("-"))) for k, v in LABEL.items()}
raw["cohort"] = raw.author_birth_year.map(lambda y: next(k for k, (s, e) in bins.items() if s <= y <= e))
assert (raw.cohort == raw.table_cohort).all(), "cohort from birth year differs from the table it was loaded in"
assert raw.id.is_unique

flow = []
def log(step, n, extra=None):
    prev = flow[-1]["n"] if flow else n
    row = {"step": step, "n": int(n), "dropped": int(prev - n) if flow else 0}
    if extra:
        row.update(extra)
    flow.append(row)

log("full texts loaded in gutenberg_texts_c1..c6 and gutenberg_texts_c3_refill", raw_all_n)
log("drop translations, books on non-English-literature bookshelves and non-novels (ids " + ", ".join(map(str, sorted(excl.id))) + ")", len(raw))
rows = []
for r in raw.itertuples():
    txt, cut = clean(r.text)
    toks = tokens(txt)
    rows.append({"doc_id": f"pg{r.id}", "source_id": int(r.id), "title": r.title, "author": r.authors,
                 "author_birth_year": int(r.author_birth_year), "cohort": r.cohort, "language": r.languages,
                 "draw_rank": int(r.draw_rank), "text": txt, "chars_cut": int(cut), "toks": toks, "n_tokens": len(toks)})
df = pd.DataFrame(rows)

short = df[df.n_tokens < MIN_TOKENS]
df = df[df.n_tokens >= MIN_TOKENS]
log(f"drop novels under {MIN_TOKENS:,} tokens after cleaning (ids {sorted(short.source_id.tolist())})", len(df))
nn = df[df.source_id.isin(NON_NOVELS)]
df = df[~df.source_id.isin(NON_NOVELS)]
log("drop non-novels found on reading titles/subjects (ids " + ", ".join(map(str, sorted(nn.source_id))) + ")", len(df))
df["sha256"] = df.text.map(lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest())
df = df.sort_values(["cohort", "draw_rank"])
df = df.drop_duplicates("sha256")
log("de-duplicate by text SHA-256", len(df))
df["norm_title"] = df.title.str.lower().str.replace(r"[^a-z0-9 ]", " ", regex=True).str.split(" or ").str[0].str.strip()
df = df.drop_duplicates(["norm_title", "author"])
log("de-duplicate by normalised title + author", len(df))
assert (df.groupby(["cohort", "author"]).size() <= 2).all()
counts_before = df.groupby("cohort").size().reindex(COHORTS).to_dict()
nmin = int(min(counts_before.values()))
df = df.groupby("cohort", group_keys=False).apply(lambda g: g.sort_values("draw_rank").head(nmin)).sort_values(["cohort", "draw_rank"])
log(f"cut every cohort to the smallest n ({nmin}), lowest draw ranks kept", len(df))
log("final corpus", len(df))
print("cohort sizes before cut:", counts_before, "-> n per cohort", nmin)

# ---- tables
corpus = df[["doc_id", "text", "title", "author", "author_birth_year", "cohort", "language", "source_id"]]
tc = df[["doc_id", "cohort", "n_tokens"]].copy()
dict_terms = {}
for a in DESIGN["analyses"]:
    if a["method"] == "dictionary" and a["id"] != "weather_all":
        for t in a["dictionary"]["terms"]:
            dict_terms[t] = a["id"]
all_terms = set(next(a for a in DESIGN["analyses"] if a["id"] == "weather_all")["dictionary"]["terms"])
assert all_terms == set(dict_terms), all_terms ^ set(dict_terms)
hits = []
for r in df.itertuples():
    cnt = Counter(w for w in r.toks if w in dict_terms)
    for w, n in sorted(cnt.items()):
        hits.append({"doc_id": r.doc_id, "cohort": r.cohort, "term": w, "category": dict_terms[w], "n": n})
hits = pd.DataFrame(hits)
summ = df.groupby("cohort").agg(n_docs=("doc_id", "count"), n_authors=("author", "nunique"), n_tokens=("n_tokens", "sum"),
                                birth_year_min=("author_birth_year", "min"), birth_year_max=("author_birth_year", "max")).reindex(COHORTS).reset_index()
for name, t in [("corpus", corpus), ("corpus_token_counts", tc), ("weather_dictionary_hits", hits), ("corpus_cohort_summary", summ)]:
    t.to_sql(name, con, if_exists="replace", index=False)
con.commit()

# ---- manifest
docs = []
for r in df.itertuples():
    docs.append({"doc_id": r.doc_id, "source": f"Project Gutenberg ebook {r.source_id} (gutenberg.pglaf.org mirror; header/footer/licence removed by the connector)",
                 "licence": "not restricted by copyright in the USA; Project Gutenberg licence removed", "sha256": r.sha256,
                 "n_tokens": int(r.n_tokens), "title": r.title, "author": r.author, "author_birth_year": int(r.author_birth_year),
                 "cohort": r.cohort, "chars_cut_front_matter": int(r.chars_cut)})
lens = sorted(df.n_tokens.tolist())
vocab = set()
for tk in df.toks:
    vocab.update(tk)
length = {"min": float(lens[0]), "p25": round(float(quantile(lens, .25)), 2), "median": round(float(quantile(lens, .5)), 2),
          "p75": round(float(quantile(lens, .75)), 2), "max": float(lens[-1]), "mean": round(float(np.mean(lens)), 2)}
corp = {"n_documents": int(len(df)), "n_tokens": int(df.n_tokens.sum()), "n_types": len(vocab), "length": length}
json.dump({"documents": docs, "corpus": corp}, open("corpus_manifest.json", "w"), indent=1, ensure_ascii=False)

# ---- summary statistics (descriptive only)
by = {}
for c in COHORTS:
    g = df[df.cohort == c]
    l = sorted(g.n_tokens.tolist())
    by[c] = {"n_documents": int(len(g)), "n_authors": int(g.author.nunique()), "n_tokens": int(g.n_tokens.sum()),
             "tokens_per_doc_mean": round(float(np.mean(l)), 2), "tokens_per_doc_median": round(float(quantile(l, .5)), 2),
             "tokens_per_doc_min": int(l[0]), "tokens_per_doc_max": int(l[-1]),
             "birth_year_min": int(g.author_birth_year.min()), "birth_year_max": int(g.author_birth_year.max()),
             "birth_year_mean": round(float(g.author_birth_year.mean()), 2), "n_weather_dictionary_hits": int(hits[hits.cohort == c].n.sum())}
stats = {
    "n_observations": int(len(df)), "n_units": int(df.author.nunique()),
    "n_tokens": corp["n_tokens"], "n_types": corp["n_types"],
    "time_coverage": {"start_iso": "1770", "end_iso": "1899", "n_periods": 6, "note": "author birth years in six cohorts; no publication year used"},
    "outcome": {"tokens_per_document": {"mean": length["mean"], "sd": round(float(np.std(lens, ddof=1)), 2), "min": length["min"], "p25": length["p25"],
                                          "median": length["median"], "p75": length["p75"], "max": length["max"]}},
    "author_birth_year": {"min": int(df.author_birth_year.min()), "max": int(df.author_birth_year.max()), "mean": round(float(df.author_birth_year.mean()), 2)},
    "by_cohort": by,
    "n_per_cohort_before_cut": {k: int(v) for k, v in counts_before.items()},
    "weather_dictionary": {"n_terms": len(dict_terms), "n_hits_total": int(hits.n.sum()), "n_distinct_terms_observed": int(hits.term.nunique())},
    "sample_flow": [{"step": "catalogue rows read (6 frames + 7 extra searches, with repeats)", "n": 4160, "dropped": 0},
                    {"step": "unique ebook ids", "n": 1409, "dropped": 2751},
                    {"step": "language en, one catalogue person, birth year 1770-1899, plain text, not copyrighted, fiction-type, non-novel forms and collections removed, title+author de-duplication (catalogue-eligible books)", "n": 632, "dropped": 777},
                    {"step": "random draw (seed 20261014), at most 2 per author per cohort: first 20 per cohort drawn for text loading", "n": 120, "dropped": 512}]
                   + [dict(flow[0], dropped=0)] + [dict(f) for f in flow[1:]],
    "missingness": {"title_pct_missing": 0.0, "author_birth_year_pct_missing": 0.0, "language_pct_missing": 0.0,
                    "note": "books without a recorded birth year, or with several catalogue persons, were dropped at the catalogue stage, not coded as zero"},
    "front_matter_chars_cut": {"total": int(df.chars_cut.sum()), "max_doc": int(df.chars_cut.max())},
}
json.dump(stats, open("summary_statistics.json", "w"), indent=1)

fig = {"figures": [
    {"filename": "fig_corpus_tokens_by_cohort.pdf", "figure_type": "bar", "label": "fig:corpus_tokens",
     "caption_hint": "Tokens in the analysed corpus by author birth cohort (equal number of novels per cohort).",
     "categories": [LABEL[c] for c in COHORTS], "values": [float(by[c]["n_tokens"]) for c in COHORTS],
     "y_label": "Tokens (all novels of the cohort)", "x_label": "Author birth cohort"},
    {"filename": "fig_corpus_median_length_by_cohort.pdf", "figure_type": "bar", "label": "fig:corpus_length",
     "caption_hint": "Median novel length in tokens by author birth cohort.",
     "categories": [LABEL[c] for c in COHORTS], "values": [float(by[c]["tokens_per_doc_median"]) for c in COHORTS],
     "y_label": "Median tokens per novel", "x_label": "Author birth cohort"}]}
json.dump(fig, open("figure_spec.json", "w"), indent=1)
print(json.dumps({"corpus": corp, "by_cohort": by, "flow": flow}, indent=1))
