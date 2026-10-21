"""Descriptive text analysis of weather vocabulary by author birth cohort. Writes estimation_results.json and validation_sample.json."""
import json
import math
import random
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import spearmanr

SEED = 20261014
DESIGN = json.load(open("corpus_design.json", encoding="utf-8"))
PRE = DESIGN["preprocessing"]
PATTERN = re.compile(PRE["token_pattern"])
STOP = set(open("stopwords.txt", encoding="utf-8").read().split())
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

con = sqlite3.connect("data.db")
rows = con.execute("SELECT doc_id, text, author, author_birth_year, cohort FROM corpus ORDER BY doc_id").fetchall()
con.close()

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


def hits_in(d, terms, tokfilter=None):
    ts = set(terms)
    return sum(docs[d]["cnt"][w] for w in ts)


# ---------- per-document hit matrices
def doc_hits(terms, drop_capitalised=False):
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


def cohort_stats(h, label_terms=None):
    """h: doc -> hits. Pooled rate, equal-weight rate, bootstrap CIs (authors resampled within cohort), dispersion."""
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


# ---------- dictionary models
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

# ---------- term frequencies
wterms = sorted(set(DICTS["weather_all"]) | set(HEAD))
tf = {}
for g in COHORTS + ["all"]:
    cnt = all_cnt if g == "all" else coh_cnt[g]
    n = GROUP_TOK[g]
    tf[g] = {"n_tokens": n, "terms": [dict(term=w, count=cnt[w], per_10k=per10k(cnt[w], n)) for w in wterms if cnt[w] > 0]}


def tdocs(w, cs):
    dl = [d for d in ids if docs[d]["coh"] in cs]
    return sum(1 for d in dl if docs[d]["cnt"][w] > 0), len(dl)


# ---------- cohort trend series for headline exact forms, with CIs
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

# ---------- keyness


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
dispersion_doc = {}
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

# ---------- collocations
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
    ps = sorted([p for p in pairs if p["node"] == n], key=lambda p: -p["pmi"])[:20]
    out_pairs += ps
by_count = []
for n in NODES:
    by_count += sorted([p for p in pairs if p["node"] == n], key=lambda p: -p["count"])[:10]
models["weather_collocates"] = dict(method="collocation", group="all", window=1, min_count=5, measure="pmi",
                                    nodes=NODES, outputs={"pairs": out_pairs, "pairs_by_count": by_count},
                                    note="adjacent pairs with a weather node word; partners that are stop words excluded; top 20 by PMI and top 10 by count per node")

# ---------- diachronic
models["cohort_trend"] = dict(method="diachronic", outputs={"series": series, "trend_by_term": head_trend,
                              "trend_by_category": {k: dict_models[k]["outputs"]["trend"] for k in DICTS}})

# ---------- robustness
rob = {}
variants = {
    "extended_lexicon": ("weather_all", set(DICTS["weather_all"]), False),
    "core_lexicon": (None, CORE, False),
    "unambiguous_lexicon": (None, set(DICTS["weather_all"]) - AMBIG, False),
    "extended_minus_capitalised_midsentence_hits": (None, set(DICTS["weather_all"]), True),
    "unambiguous_minus_capitalised_hits": (None, set(DICTS["weather_all"]) - AMBIG, True),
}
for name, (_, terms, dc) in variants.items():
    h = doc_hits(terms, dc)
    st = cohort_stats(h)
    rob[name] = dict(n_terms=len(terms), by_cohort={g: {k: st[g][k] for k in ("hits", "per_10k", "ci_pooled_per_10k", "mean_doc_per_10k",
                                                                            "ci_mean_doc_per_10k", "share_docs_with_hit")} for g in COHORTS + ["all"]},
                     trend=trend(h))
# post hoc (defined after the hand check): drop forms judged unusable and capitalised mid-sentence hits
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
rob["trend_without_heaviest_novel"] = None
keep = {d for d in ids if d not in {loo[c]["heaviest_novel"] for c in COHORTS}}
rate = [sum(h[d] for d in keep if docs[d]["coh"] == c) / sum(docs[d]["n"] for d in keep if docs[d]["coh"] == c) * 1e4 for c in COHORTS]
rr, pp = spearmanr(range(1, 7), rate)
rob["trend_without_heaviest_novel"] = dict(cohort_rates_per_10k=[round(r, 4) for r in rate], spearman_rho=round(float(rr), 4), spearman_p=round(float(pp), 4))

# ---------- validation sample
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
json.dump(sample, open("validation_sample.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- figures (each drawn from the results)
cohort_summary = []
for c in COHORTS:
    lens = sorted(docs[d]["n"] for d in ids if docs[d]["coh"] == c)
    cohort_summary.append(dict(cohort=c, n_tokens=coh_tokens[c], median_tokens=float(np.median(lens))))
figs = [
    {"filename": "fig_corpus_tokens_by_cohort.pdf", "figure_type": "bar", "label": "fig:corpus_tokens",
     "caption_hint": "Tokens in the analysed corpus by author birth cohort (c1 = born 1770-1799 ... c6 = born 1880-1899; equal number of novels per cohort).",
     "categories": [r["cohort"] for r in cohort_summary], "values": [float(r["n_tokens"]) for r in cohort_summary],
     "y_label": "Tokens (all novels of the cohort)", "x_label": "Author birth cohort (c1 = 1770-1799 ... c6 = 1880-1899)",
     "source": {"results": "corpus.cohort_summary", "fields": {"categories": "cohort", "values": "n_tokens"}}},
    {"filename": "fig_corpus_median_length_by_cohort.pdf", "figure_type": "bar", "label": "fig:corpus_length",
     "caption_hint": "Median novel length in tokens by author birth cohort (c1 = born 1770-1799 ... c6 = born 1880-1899).",
     "categories": [r["cohort"] for r in cohort_summary], "values": [r["median_tokens"] for r in cohort_summary],
     "y_label": "Median tokens per novel", "x_label": "Author birth cohort (c1 = 1770-1799 ... c6 = 1880-1899)",
     "source": {"results": "corpus.cohort_summary", "fields": {"categories": "cohort", "values": "median_tokens"}}},
]
LABELS = {"c1": "1770-1799", "c2": "1800-1819", "c3": "1820-1839", "c4": "1840-1859", "c5": "1860-1879", "c6": "1880-1899"}
for c in COHORTS:
    for pre, what in (("keyness", "Key terms"), ("keyness_weather", "Key weather terms")):
        mid = f"{pre}_{c}"
        terms = models[mid]["outputs"]["terms"]
        figs.append({
            "filename": f"fig_{mid}.pdf", "figure_type": "bar", "label": f"fig:{mid}",
            "caption_hint": f"{what} of cohort {LABELS[c]} against the other five cohorts (log ratio, base 2; positive = more frequent in this cohort).",
            "categories": [t["term"] for t in terms], "values": [t["log_ratio"] for t in terms],
            "x_label": "Term", "y_label": "Log ratio (base 2)",
            "source": {"results": f"models.{mid}.outputs.terms", "fields": {"categories": "term", "values": "log_ratio"}}})
trend_terms = [t for t in ["rain", "wind", "storm", "fog", "snow", "sun", "cloud"] if any(s["term"] == t for s in series)]
ser_figs = []
for t in trend_terms:
    pts = [s for s in series if s["term"] == t]
    ser_figs.append({"label": t, "x": [s["group"] for s in pts], "y": [s["per_10k"] for s in pts],
                     "source": {"results": "models.cohort_trend.outputs.series", "fields": {"x": "group", "y": "per_10k"},
                                "where": f"term = '{t}'"}})
figs.append({"filename": "fig_cohort_trend.pdf", "figure_type": "time_series", "label": "fig:cohort_trend",
             "caption_hint": "Frequency per 10,000 tokens of headline weather words by author birth cohort.",
             "series": ser_figs, "x_label": "Author birth cohort (c1 = 1770-1799, c2 = 1800-1819, c3 = 1820-1839, c4 = 1840-1859, c5 = 1860-1879, c6 = 1880-1899)", "y_label": "Occurrences per 10,000 tokens"})
json.dump({"figures": figs}, open("figure_spec.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- write
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
    "figures": [f["filename"] for f in figs],
    "bootstrap": dict(seed=SEED, draws=NB, scheme="authors resampled with replacement within cohort; all sampled novels of a drawn author kept; 95% percentile interval"),
    "limits": dict(sampling_bias=DESIGN["limits"]["sampling_bias"], frame=DESIGN["limits"]["frame"],
                   interpretation=f"descriptive patterns of word counts in {len(ids)} popular, digitised novels; cohort is birth-year based and overlaps in publication years; no causal claim"),
}
json.dump(res, open("estimation_results.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("docs", len(ids), "tokens", N_ALL, "types", types)
for k in DICTS:
    print(k, [(g["group"], g["per_10k"]) for g in dict_models[k]["outputs"]["by_group"]])
print({c: dict_models["weather_all"]["outputs"]["trend"][x] for c in ["x"] for x in ["spearman_rho", "slope_per_cohort_step", "slope_ci95"]})
print("samples", {k: len(v["items"]) for k, v in sample.items()})
