"""
Replication script for: The Vocabulary of Weather in English-Language Novels by Author Birth Cohort, 1770-1899
Paper ID: 4b4d6a45-97cd-4a7f-870b-173551822e97

Descriptive text analysis (no regression, no causal claim). Heteroskedasticity-robust SEs do not apply: uncertainty is an
author-clustered bootstrap (seed 20261014, 2,000 draws), as fixed in econometric_spec.md. Keyness uses Dunning G2 (token-based).

Requirements: pandas, numpy, scipy, matplotlib (sqlite3 is in the standard library)
Usage: python replication/estimation.py        (paths are resolved from this file, so any working directory works)
Inputs (workspace root): data.db (table `corpus`), corpus_design.json, stopwords.txt
Output: replication/output/ (tables as CSV, estimation_results.json, validation_sample.json, figures as PNG)
"""
import json
import math
import random
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

np.random.seed(42)  # all resampling below uses explicitly seeded generators (SEED)
SEED = 20261014
ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Load data and design ───────────────────────────────────────────────────
DESIGN = json.load(open(ROOT / "corpus_design.json", encoding="utf-8"))
PRE = DESIGN["preprocessing"]
PATTERN = re.compile(PRE["token_pattern"])
STOP = set(open(ROOT / "stopwords.txt", encoding="utf-8").read().split())
COHORTS = ["c1", "c2", "c3", "c4", "c5", "c6"]
AN = {a["id"]: a for a in DESIGN["analyses"]}
DICTS = {k: AN[k]["dictionary"]["terms"] for k in
         ["weather_all", "precipitation", "wind_words", "storm_words", "fog_words", "snow_ice_words", "sun_words", "cloud_words"]}
HEAD = AN["frequencies"]["terms"]
HEAD7 = AN["cohort_trend"]["terms"]
NODES = AN["weather_collocates"]["nodes"]
AMBIG = {"shower", "showers", "thunder", "thunders", "thundered", "thundering", "icy", "cloud", "clouds", "clouded", "cloudy",
         "wind", "winds", "sun", "suns", "storm", "storms"}
CORE = {w + s for w in HEAD for s in ("", "s")} & set(DICTS["weather_all"])
NB = 2000

con = sqlite3.connect(str(ROOT / "data.db"))
rows = con.execute("SELECT doc_id, text, author, author_birth_year, cohort FROM corpus ORDER BY doc_id").fetchall()
con.close()

# ── 2. Variable construction: tokens, per-novel counts, cohort totals ─────────
docs = {}
for did, text, author, by, coh in rows:
    t = unicodedata.normalize("NFC", text)
    low = t.lower()
    toks = []
    pos = []
    for m in PATTERN.finditer(low):
        toks.append(m.group(0))
        pos.append((m.start(), m.end()))
    docs[did] = dict(text=t, low=low, toks=toks, pos=pos, author=author, coh=coh, n=len(toks), cnt=Counter(toks),
                     same_len=len(low) == len(t))
ids = sorted(docs)
authors_of = {c: sorted({docs[d]["author"] for d in ids if docs[d]["coh"] == c}) for c in COHORTS}
coh_tokens = {c: sum(docs[d]["n"] for d in ids if docs[d]["coh"] == c) for c in COHORTS}
N_ALL = sum(coh_tokens.values())
coh_cnt = {c: sum((docs[d]["cnt"] for d in ids if docs[d]["coh"] == c), Counter()) for c in COHORTS}
all_cnt = sum(coh_cnt.values(), Counter())
types = len(all_cnt)
GROUP_TOK = dict(coh_tokens, all=N_ALL)


def per10k(c, n):
    return round(c / n * 10000, 4)


def doc_hits(terms, drop_capitalised=False):
    """Hits per novel for a set of exact word forms; optionally drop capitalised mid-sentence hits (surnames etc.)."""
    ts = set(terms)
    out = {}
    for d in ids:
        if not drop_capitalised:
            out[d] = sum(docs[d]["cnt"][w] for w in ts)
        else:
            D = docs[d]
            k = 0
            for w, (s, e) in zip(D["toks"], D["pos"]):
                if w in ts:
                    if D["same_len"] and D["text"][s].isupper():
                        j = s - 1
                        while j >= 0 and D["text"][j] in " \t\n\r":
                            j -= 1
                        if j >= 0 and D["text"][j] not in ".!?\"“”‘'—:;(":
                            continue
                    k += 1
            out[d] = k
    return out


def cohort_stats(h):
    """h: doc -> hits. Pooled rate, equal-weight rate, author-clustered bootstrap CIs (authors resampled within cohort), dispersion."""
    rng = np.random.default_rng(SEED)
    res = {}
    for c in COHORTS + ["all"]:
        cs = COHORTS if c == "all" else [c]
        dl = [d for d in ids if docs[d]["coh"] in cs]
        byauth = defaultdict(list)
        for d in dl:
            byauth[(docs[d]["coh"], docs[d]["author"])].append(d)
        keys = sorted(byauth)
        A = np.array([[sum(h[d] for d in byauth[k]), sum(docs[d]["n"] for d in byauth[k]),
                       sum(h[d] / docs[d]["n"] for d in byauth[k]), len(byauth[k])] for k in keys], float)
        coh_of = np.array([k[0] for k in keys])
        hits, tok = A[:, 0].sum(), A[:, 1].sum()
        pooled = hits / tok * 1e4
        eq = A[:, 2].sum() / A[:, 3].sum() * 1e4
        bp, be = [], []
        groups = [np.where(coh_of == cc)[0] for cc in cs]
        for _ in range(NB):
            idx = np.concatenate([g[rng.integers(0, len(g), len(g))] for g in groups])
            S = A[idx].sum(axis=0)
            bp.append(S[0] / S[1] * 1e4)
            be.append(S[2] / S[3] * 1e4)
        nd = sum(1 for d in dl if h[d] > 0)
        na = len({docs[d]["author"] for d in dl if h[d] > 0})
        arate = A[:, 0] / A[:, 1] * 1e4
        top = int(np.argmax(A[:, 0])) if hits > 0 else 0
        res[c] = dict(hits=int(hits), n_tokens=int(tok), per_10k=round(pooled, 4), per_million=round(pooled * 100, 2),
                      ci_pooled_per_10k=[round(float(np.percentile(bp, 2.5)), 4), round(float(np.percentile(bp, 97.5)), 4)],
                      mean_doc_per_10k=round(eq, 4),
                      ci_mean_doc_per_10k=[round(float(np.percentile(be, 2.5)), 4), round(float(np.percentile(be, 97.5)), 4)],
                      n_docs=len(dl), n_docs_with_hit=nd, share_docs_with_hit=round(nd / len(dl), 4),
                      n_authors=len(keys), n_authors_with_hit=na,
                      dispersion_authors=dict(min=round(float(arate.min()), 4), p25=round(float(np.percentile(arate, 25)), 4),
                                              median=round(float(np.median(arate)), 4), p75=round(float(np.percentile(arate, 75)), 4),
                                              max=round(float(arate.max()), 4), sd=round(float(arate.std(ddof=1)), 4),
                                              cv=round(float(arate.std(ddof=1) / arate.mean()), 4) if arate.mean() > 0 else None,
                                              top_author=keys[top][1], top_author_share_of_hits=round(float(A[top, 0] / hits), 4) if hits else None))
    return res


def trend(h):
    """Descriptive: Spearman of cohort rates vs cohort index; OLS slope of novel-level rate on cohort index (+ log length), author-cluster bootstrap."""
    rate = np.array([sum(h[d] for d in ids if docs[d]["coh"] == c) / coh_tokens[c] * 1e4 for c in COHORTS])
    rho, p = spearmanr(range(1, 7), rate)
    y = np.array([h[d] / docs[d]["n"] * 1e4 for d in ids])
    x = np.array([COHORTS.index(docs[d]["coh"]) + 1 for d in ids], float)
    ll = np.log(np.array([docs[d]["n"] for d in ids], float))
    au = np.array([docs[d]["coh"] + "|" + docs[d]["author"] for d in ids])
    X1 = np.column_stack([np.ones(len(ids)), x])
    X2 = np.column_stack([np.ones(len(ids)), x, ll - ll.mean()])
    b1 = np.linalg.lstsq(X1, y, rcond=None)[0][1]
    b2 = np.linalg.lstsq(X2, y, rcond=None)[0][1]
    rng = np.random.default_rng(SEED + 1)
    byc = {c: sorted({a for a in au if a.startswith(c + "|")}) for c in COHORTS}
    pos = defaultdict(list)
    for i, a in enumerate(au):
        pos[a].append(i)
    s1, s2 = [], []
    for _ in range(1000):
        idx = []
        for c in COHORTS:
            ks = byc[c]
            for j in rng.integers(0, len(ks), len(ks)):
                idx.extend(pos[ks[j]])
        idx = np.array(idx)
        s1.append(np.linalg.lstsq(X1[idx], y[idx], rcond=None)[0][1])
        s2.append(np.linalg.lstsq(X2[idx], y[idx], rcond=None)[0][1])
    ci = lambda s: [round(float(np.percentile(s, 2.5)), 4), round(float(np.percentile(s, 97.5)), 4)]
    return dict(cohort_rates_per_10k=[round(float(r), 4) for r in rate], spearman_rho=round(float(rho), 4),
                spearman_p=round(float(p), 4), slope_per_cohort_step=round(float(b1), 4), slope_ci95=ci(s1),
                slope_adj_log_length=round(float(b2), 4), slope_adj_ci95=ci(s2), n_docs=len(ids), n_bootstrap=1000,
                note="descriptive monotone-drift summary over six birth cohorts; not a causal estimate")


# ── 3. Summary statistics and dictionary models (composite + six categories) ──
dict_models = {}
hits_cache = {}
for k, terms in DICTS.items():
    h = doc_hits(terms)
    hits_cache[k] = h
    st = cohort_stats(h)
    by_group = [dict(group=g, hits=st[g]["hits"], n_tokens=st[g]["n_tokens"], per_10k=per10k(st[g]["hits"], st[g]["n_tokens"]),
                     **{kk: vv for kk, vv in st[g].items() if kk not in ("hits", "n_tokens", "per_10k")}) for g in COHORTS + ["all"]]
    dict_models[k] = {"method": "dictionary", "analysis": k,
                      "dictionary": {"terms": terms, "source": AN[k]["dictionary"]["source"]},
                      "outputs": {"by_group": by_group, "trend": trend(h)},
                      "validation": {"file": "text_validation.json"}}

wterms = sorted(set(DICTS["weather_all"]) | set(HEAD))
tf = {}
for g in COHORTS + ["all"]:
    cnt = all_cnt if g == "all" else coh_cnt[g]
    n = GROUP_TOK[g]
    tf[g] = {"n_tokens": n, "terms": [dict(term=w, count=cnt[w], per_10k=per10k(cnt[w], n)) for w in wterms if cnt[w] > 0]}


def tdocs(w, cs):
    dl = [d for d in ids if docs[d]["coh"] in cs]
    return sum(1 for d in dl if docs[d]["cnt"][w] > 0), len(dl)


# ── 4. Main specification: headline-term cohort series and trends ─────────────
series = []
for w in HEAD:
    h = {d: docs[d]["cnt"][w] for d in ids}
    st = cohort_stats(h)
    for g in COHORTS:
        series.append(dict(group=g, term=w, count=st[g]["hits"], per_10k=per10k(st[g]["hits"], coh_tokens[g]),
                           per_million=st[g]["per_million"], ci_pooled_per_10k=st[g]["ci_pooled_per_10k"],
                           mean_doc_per_10k=st[g]["mean_doc_per_10k"], ci_mean_doc_per_10k=st[g]["ci_mean_doc_per_10k"],
                           n_docs=st[g]["n_docs"], n_docs_with_term=st[g]["n_docs_with_hit"],
                           share_docs_with_term=st[g]["share_docs_with_hit"], n_authors_with_term=st[g]["n_authors_with_hit"]))
head_trend = {w: trend({d: docs[d]["cnt"][w] for d in ids}) for w in HEAD7}


# Keyness: Dunning G2 of each cohort against the other five
def g2_row(a, b, c, d):
    E1, E2 = c * (a + b) / (c + d), d * (a + b) / (c + d)
    G2 = 2 * ((a * math.log(a / E1) if a else 0) + (b * math.log(b / E2) if b else 0))
    lr = math.log2(((a or 0.5) / c) / ((b or 0.5) / d))
    return G2, lr, math.erfc(math.sqrt(G2 / 2))


def keyness_entry(w, tc, rc, tn, rn, tg):
    a, b = tc[w], rc[w]
    G2, lr, p = g2_row(a, b, tn, rn)
    more = tg if (a / tn) > (b / rn) else "rest"
    return dict(term=w, count_target=a, count_reference=b, g2=round(G2, 4), log_ratio=round(lr, 4), p_value=p,
                more_in=(tg if more == tg else f"not_{tg}"))


models = dict(dict_models)
for c in COHORTS:
    rc = all_cnt - coh_cnt[c]
    tn, rn = coh_tokens[c], N_ALL - coh_tokens[c]
    cand = [w for w in all_cnt if w not in STOP and (coh_cnt[c][w] + rc[w]) >= 20 and len(w) > 1]
    ents = [keyness_entry(w, coh_cnt[c], rc, tn, rn, c) for w in cand]
    ents = [e for e in ents if e["g2"] > 15.13]
    ents.sort(key=lambda e: -e["g2"])
    for e in ents:
        e["docs_target"] = tdocs(e["term"], [c])[0]
        e["docs_reference"] = tdocs(e["term"], [x for x in COHORTS if x != c])[0]
    top = ents[:40]
    models[f"keyness_{c}"] = dict(method="keyness", target=c, reference=f"not_{c}",
                                  statistic="log-likelihood G2 (threshold 15.13, p<0.0001), stop words excluded; log ratio, zero count taken as 0.5",
                                  n_terms_tested=len(cand), n_terms_over_threshold=len(ents), outputs={"terms": top})
    wk = [keyness_entry(w, coh_cnt[c], rc, tn, rn, c) for w in DICTS["weather_all"] if (coh_cnt[c][w] + rc[w]) >= 10 and w not in STOP]
    wk.sort(key=lambda e: -e["g2"])
    models[f"keyness_weather_{c}"] = dict(method="keyness", target=c, reference=f"not_{c}",
                                          statistic="G2 for dictionary terms with total count >= 10; no significance threshold applied; token-based, overstates certainty",
                                          outputs={"terms": wk})

# Collocations: adjacent pairs with a weather node word, PMI
node_set = set(NODES)
big = Counter()
for d in ids:
    t = docs[d]["toks"]
    for i in range(len(t) - 1):
        if t[i] in node_set or t[i + 1] in node_set:
            big[(t[i], t[i + 1])] += 1
pairs = []
for (w1, w2), c in big.items():
    if c >= 5 and (w1 in node_set) != (w2 in node_set) or (c >= 5 and w1 in node_set and w2 in node_set):
        partner = w2 if w1 in node_set else w1
        if partner in STOP and not (w1 in node_set and w2 in node_set):
            continue
        pmi = math.log2(c * N_ALL / (all_cnt[w1] * all_cnt[w2]))
        pairs.append(dict(w1=w1, w2=w2, count=c, pmi=round(pmi, 4), node=w1 if w1 in node_set else w2))
out_pairs = []
for n in NODES:
    out_pairs += sorted([p for p in pairs if p["node"] == n], key=lambda p: -p["pmi"])[:20]
by_count = []
for n in NODES:
    by_count += sorted([p for p in pairs if p["node"] == n], key=lambda p: -p["count"])[:10]
models["weather_collocates"] = dict(method="collocation", group="all", window=1, min_count=5, measure="pmi",
                                    nodes=NODES, outputs={"pairs": out_pairs, "pairs_by_count": by_count},
                                    note="adjacent pairs with a weather node word; partners that are stop words excluded; top 20 by PMI and top 10 by count per node")
models["cohort_trend"] = dict(method="diachronic", outputs={"series": series, "trend_by_term": head_trend,
                              "trend_by_category": {k: dict_models[k]["outputs"]["trend"] for k in DICTS}})

# ── 5. Robustness checks ──────────────────────────────────────────────────────
rob = {}
variants = {
    "extended_lexicon": (set(DICTS["weather_all"]), False),
    "core_lexicon": (CORE, False),
    "unambiguous_lexicon": (set(DICTS["weather_all"]) - AMBIG, False),
    "extended_minus_capitalised_midsentence_hits": (set(DICTS["weather_all"]), True),
    "unambiguous_minus_capitalised_hits": (set(DICTS["weather_all"]) - AMBIG, True),
}
for name, (terms, dc) in variants.items():
    h = doc_hits(terms, dc)
    st = cohort_stats(h)
    rob[name] = dict(n_terms=len(terms), by_cohort={g: {k: st[g][k] for k in ("hits", "per_10k", "ci_pooled_per_10k", "mean_doc_per_10k",
                                                                            "ci_mean_doc_per_10k", "share_docs_with_hit")} for g in COHORTS + ["all"]},
                     trend=trend(h))
# Post hoc (defined AFTER the hand check, not in the design): drop forms judged unusable and capitalised mid-sentence hits
POSTHOC_DROP = {"thunder", "thunders", "thundered", "thundering", "hurricane", "haze", "hazy", "clouded", "cloudy", "overcast"}
ph = {}
for fam in ["weather_all", "storm_words", "fog_words", "cloud_words"]:
    terms = set(DICTS[fam]) - POSTHOC_DROP
    h = doc_hits(terms, True)
    st = cohort_stats(h)
    ph[fam] = dict(n_terms=len(terms), dropped=sorted(set(DICTS[fam]) & POSTHOC_DROP),
                   by_cohort={g: {k: st[g][k] for k in ("hits", "n_tokens", "per_10k", "ci_pooled_per_10k", "mean_doc_per_10k",
                                                       "ci_mean_doc_per_10k", "share_docs_with_hit")} for g in COHORTS + ["all"]},
                   trend=trend(h))
rob["post_hoc_reduced_lexicon"] = dict(definition="defined after the hand check (post hoc): families recomputed without thunder, thunders, thundered, thundering, hurricane, haze, hazy, clouded, cloudy, overcast and without capitalised mid-sentence hits",
                                       families=ph)
rob["core_terms"] = sorted(CORE)
rob["ambiguous_forms_dropped"] = sorted(AMBIG)
# leave-one-author-out and heaviest-novel-out for the aggregate
h = hits_cache["weather_all"]
loo = {}
for c in COHORTS:
    dl = [d for d in ids if docs[d]["coh"] == c]
    rates = []
    for a in authors_of[c]:
        rest = [d for d in dl if docs[d]["author"] != a]
        rates.append(sum(h[d] for d in rest) / sum(docs[d]["n"] for d in rest) * 1e4)
    full = sum(h[d] for d in dl) / coh_tokens[c] * 1e4
    heavy = max(dl, key=lambda d: h[d] / docs[d]["n"])
    rest = [d for d in dl if d != heavy]
    loo[c] = dict(full=round(full, 4), leave_one_author_out_min=round(min(rates), 4), leave_one_author_out_max=round(max(rates), 4),
                  heaviest_novel=heavy, heaviest_novel_rate=round(h[heavy] / docs[heavy]["n"] * 1e4, 4),
                  without_heaviest_novel=round(sum(h[d] for d in rest) / sum(docs[d]["n"] for d in rest) * 1e4, 4))
rob["leave_one_out_weather_all"] = loo
keep = {d for d in ids if d not in {loo[c]["heaviest_novel"] for c in COHORTS}}
rate = [sum(h[d] for d in keep if docs[d]["coh"] == c) / sum(docs[d]["n"] for d in keep if docs[d]["coh"] == c) * 1e4 for c in COHORTS]
rr, pp = spearmanr(range(1, 7), rate)
rob["trend_without_heaviest_novel"] = dict(cohort_rates_per_10k=[round(r, 4) for r in rate], spearman_rho=round(float(rr), 4), spearman_p=round(float(pp), 4))

# Validation sample for the hand check (seeded, stratified, ambiguous forms oversampled)
rngv = random.Random(SEED)
sample = {}
for k, terms in DICTS.items():
    ts = set(terms)
    hl = []
    for d in ids:
        D = docs[d]
        if not D["same_len"]:
            continue
        for w, (s, e) in zip(D["toks"], D["pos"]):
            if w in ts:
                hl.append((d, w, s, e))
    nper = 5 if k == "weather_all" else 4
    namb = 2 if k == "weather_all" else 1
    chosen = []
    for c in COHORTS:
        hc = [x for x in hl if docs[x[0]]["coh"] == c]
        am = [x for x in hc if x[1] in AMBIG]
        ot = [x for x in hc if x[1] not in AMBIG]
        pick = rngv.sample(am, min(namb, len(am)))
        pick += rngv.sample(ot, min(nper - len(pick), len(ot)))
        rest = [x for x in hc if x not in pick]
        pick += rngv.sample(rest, min(nper - len(pick), len(rest)))
        chosen += pick
    items = []
    for d, w, s, e in chosen:
        T = docs[d]["text"]
        items.append(dict(doc_id=d, term=w, quote=T[max(0, s - 100):e + 100], cohort=docs[d]["coh"]))
    sample[k] = dict(seed=SEED, n_hits_total=len(hl), items=items)
json.dump(sample, open(OUTPUT_DIR / "validation_sample.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ── 6. Export results ─────────────────────────────────────────────────────────
cohort_summary = []
for c in COHORTS:
    lens = sorted(docs[d]["n"] for d in ids if docs[d]["coh"] == c)
    cohort_summary.append(dict(cohort=c, n_tokens=coh_tokens[c], median_tokens=float(np.median(lens))))
res = {
    "result_kind": "text",
    "corpus": dict(n_documents=len(ids), n_tokens=N_ALL, n_types=types,
                   cohort_summary=cohort_summary,
                   n_documents_by_cohort={c: sum(1 for d in ids if docs[d]["coh"] == c) for c in COHORTS},
                   n_authors_by_cohort={c: len(authors_of[c]) for c in COHORTS},
                   preprocessing=dict(token_pattern=PRE["token_pattern"], lowercase=PRE["lowercase"],
                                      stopwords={"file": PRE["stopwords"]["file"], "source": PRE["stopwords"]["source"]},
                                      lemmatisation="none", ngrams=PRE["ngrams"])),
    "term_frequencies": tf,
    "models": models,
    "robustness": rob,
    "bootstrap": dict(seed=SEED, draws=NB, scheme="authors resampled with replacement within cohort; all sampled novels of a drawn author kept; 95% percentile interval"),
    "limits": dict(sampling_bias=DESIGN["limits"]["sampling_bias"], frame=DESIGN["limits"]["frame"],
                   interpretation=f"descriptive patterns of word counts in {len(ids)} popular, digitised novels; cohort is birth-year based and overlaps in publication years; no causal claim"),
}
json.dump(res, open(OUTPUT_DIR / "estimation_results.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)  # full results (all tables)

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Table 1: corpus summary by cohort (documents, authors, tokens, median length)
pd.DataFrame([dict(cohort=r["cohort"], n_docs=res["corpus"]["n_documents_by_cohort"][r["cohort"]],
                   n_authors=res["corpus"]["n_authors_by_cohort"][r["cohort"]], n_tokens=r["n_tokens"],
                   median_tokens=r["median_tokens"]) for r in cohort_summary]).to_csv(OUTPUT_DIR / "table1_corpus_summary.csv", index=False)  # Table 1

# Table 2: weather dictionary rates per 10,000 tokens by cohort (composite and categories), bootstrap CIs
rows2 = []
for k in DICTS:
    for g in dict_models[k]["outputs"]["by_group"]:
        rows2.append(dict(dictionary=k, group=g["group"], hits=g["hits"], n_tokens=g["n_tokens"], per_10k=g["per_10k"],
                          ci_lo=g["ci_pooled_per_10k"][0], ci_hi=g["ci_pooled_per_10k"][1], mean_doc_per_10k=g["mean_doc_per_10k"],
                          share_docs_with_hit=g["share_docs_with_hit"], n_authors_with_hit=g["n_authors_with_hit"]))
pd.DataFrame(rows2).to_csv(OUTPUT_DIR / "table2_dictionary_rates_by_cohort.csv", index=False)  # Table 2

# Table 3: headline-term rates by cohort
pd.DataFrame([dict(s, ci_lo=s["ci_pooled_per_10k"][0], ci_hi=s["ci_pooled_per_10k"][1]) for s in series]
             ).drop(columns=["ci_pooled_per_10k", "ci_mean_doc_per_10k"]).to_csv(OUTPUT_DIR / "table3_headline_terms_by_cohort.csv", index=False)  # Table 3

# Table 4: descriptive trend summaries (Spearman, OLS slope on cohort index, author-clustered bootstrap CI)
drop = ("cohort_rates_per_10k", "note")
tr = [dict(kind="category", name=k, **{x: v for x, v in dict_models[k]["outputs"]["trend"].items() if x not in drop}) for k in DICTS]
tr += [dict(kind="term", name=w, **{x: v for x, v in t.items() if x not in drop}) for w, t in head_trend.items()]
pd.DataFrame(tr).to_csv(OUTPUT_DIR / "table4_cohort_trends.csv", index=False)  # Table 4

# Table 5: author dispersion of the composite weather rate by cohort
pd.DataFrame([dict(group=g["group"], **g["dispersion_authors"]) for g in dict_models["weather_all"]["outputs"]["by_group"]]
             ).to_csv(OUTPUT_DIR / "table5_author_dispersion.csv", index=False)  # Table 5

# Table 6: keyness per cohort against the other five (top 40 unigrams; weather terms with total count >= 10)
for c in COHORTS:
    pd.DataFrame(models[f"keyness_{c}"]["outputs"]["terms"]).to_csv(OUTPUT_DIR / f"table6_keyness_{c}.csv", index=False)  # Table 6 (all vocabulary)
    pd.DataFrame(models[f"keyness_weather_{c}"]["outputs"]["terms"]).to_csv(OUTPUT_DIR / f"table6_keyness_weather_{c}.csv", index=False)  # Table 6 (weather terms)

# Table 7: adjacent collocates (PMI)
pd.DataFrame(models["weather_collocates"]["outputs"]["pairs"]).to_csv(OUTPUT_DIR / "table7_collocates_pmi.csv", index=False)  # Table 7

# Table 8: robustness lexicon variants (incl. post-hoc reduced lexicon, defined after the hand check)
rb = []
for name in ["extended_lexicon", "core_lexicon", "unambiguous_lexicon", "extended_minus_capitalised_midsentence_hits", "unambiguous_minus_capitalised_hits"]:
    for g, v in rob[name]["by_cohort"].items():
        rb.append(dict(variant=name, group=g, hits=v["hits"], per_10k=v["per_10k"], ci_lo=v["ci_pooled_per_10k"][0],
                       ci_hi=v["ci_pooled_per_10k"][1], spearman_rho=rob[name]["trend"]["spearman_rho"], spearman_p=rob[name]["trend"]["spearman_p"]))
for fam, v in rob["post_hoc_reduced_lexicon"]["families"].items():
    for g, x in v["by_cohort"].items():
        rb.append(dict(variant=f"post_hoc_reduced_{fam}", group=g, hits=x["hits"], per_10k=x["per_10k"], ci_lo=x["ci_pooled_per_10k"][0],
                       ci_hi=x["ci_pooled_per_10k"][1], spearman_rho=v["trend"]["spearman_rho"], spearman_p=v["trend"]["spearman_p"]))
pd.DataFrame(rb).to_csv(OUTPUT_DIR / "table8_robustness_lexicons.csv", index=False)  # Table 8

# Table 9: leave-one-author-out and heaviest-novel-out checks
pd.DataFrame.from_dict(rob["leave_one_out_weather_all"], orient="index").rename_axis("cohort").to_csv(OUTPUT_DIR / "table9_leave_one_out.csv")  # Table 9

# Appendix table: term frequencies per cohort and pooled
pd.DataFrame([dict(group=g, **t) for g in tf for t in tf[g]["terms"]]).to_csv(OUTPUT_DIR / "tableA1_term_frequencies.csv", index=False)  # Appendix A1

# Figures 1-2: corpus tokens and median novel length by cohort
for fn, key, yl in (("fig_corpus_tokens_by_cohort.png", "n_tokens", "Tokens"), ("fig_corpus_median_length_by_cohort.png", "median_tokens", "Median tokens per novel")):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar([r["cohort"] for r in cohort_summary], [r[key] for r in cohort_summary], color="#4c72b0")
    ax.set_xlabel("Author birth cohort (c1 = 1770-1799 ... c6 = 1880-1899)")
    ax.set_ylabel(yl)
    fig.tight_layout(); fig.savefig(OUTPUT_DIR / fn, dpi=200); plt.close(fig)  # Figures 1-2

# Figure 3: headline weather words per 10,000 tokens by cohort (x values are the cohort ids c1..c6)
fig, ax = plt.subplots(figsize=(7, 4))
for t in ["rain", "wind", "storm", "fog", "snow", "sun", "cloud"]:
    pts = [s for s in series if s["term"] == t]
    if pts:
        ax.plot([s["group"] for s in pts], [s["per_10k"] for s in pts], marker="o", label=t)
ax.set_xlabel("Author birth cohort (c1 = 1770-1799 ... c6 = 1880-1899)")
ax.set_ylabel("Occurrences per 10,000 tokens")
ax.legend(ncol=2, fontsize=8)
fig.tight_layout(); fig.savefig(OUTPUT_DIR / "fig_cohort_trend.png", dpi=200); plt.close(fig)  # Figure 3

# Keyness bars (log ratio, base 2) per cohort, all vocabulary and weather terms
for c in COHORTS:
    for pre in ("keyness", "keyness_weather"):
        ts = models[f"{pre}_{c}"]["outputs"]["terms"]
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar([t["term"] for t in ts], [t["log_ratio"] for t in ts], color="#55a868")
        ax.set_ylabel("Log ratio (base 2)")
        ax.set_xlabel("Term")
        plt.setp(ax.get_xticklabels(), rotation=90, fontsize=7)
        fig.tight_layout(); fig.savefig(OUTPUT_DIR / f"fig_{pre}_{c}.png", dpi=200); plt.close(fig)  # keyness figures
print("docs", len(ids), "tokens", N_ALL, "types", types)
print("outputs written to", OUTPUT_DIR)
