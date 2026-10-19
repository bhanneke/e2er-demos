import json, sqlite3
d = json.load(open('figure_spec.json'))
ss = json.load(open('summary_statistics.json'))
con = sqlite3.connect('data.db')
bad = 0

def walk(f):
    yield f
    for p in f.get('panels', []):
        yield p

for top in d['figures']:
    for f in walk(top):
        s = f.get('source')
        if not s:
            continue
        if 'table' in s:
            c = s['columns']
            cols = [c[k] for k in ('x', 'y', 'groups') if k in c]
            rows = con.execute(f"SELECT {','.join(cols)} FROM {s['table']} WHERE {s['where']}").fetchall()
            for i, k in enumerate([k for k in ('x', 'y', 'groups') if k in c]):
                a = sorted(map(str, [round(r[i], 6) if isinstance(r[i], float) else r[i] for r in rows]))
                b = sorted(map(str, [round(v, 6) if isinstance(v, float) else v for v in f[k]]))
                ok = len(a) == len(b) and all(x == y or abs(float(x) - float(y)) < 1e-4 * max(1, abs(float(x))) for x, y in zip(a, b)) if k != 'groups' else a == b
                if not ok:
                    bad += 1
                print(top['filename'], k, len(rows), len(f[k]), 'OK' if ok else 'MISMATCH')
        else:
            node = ss
            for part in s['results'].split('.'):
                node = node[part]
            ok = [(b['lower'], b['upper'], b['count']) for b in node] == [(b['lower'], b['upper'], b['count']) for b in f['bins']]
            n = sum(b['count'] for b in f['bins'])
            print(top['filename'], s['results'], 'sum', n, 'OK' if ok else 'MISMATCH')
            bad += not ok
print('mismatches', bad)
