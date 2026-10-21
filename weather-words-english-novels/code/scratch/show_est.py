import json, sys
d = json.load(open('estimation_results.json'))
maxd = int(sys.argv[1]) if len(sys.argv) > 1 else 3
start = sys.argv[2] if len(sys.argv) > 2 else ''
for part in [p for p in start.split('.') if p]:
    d = d[int(part)] if isinstance(d, list) else d[part]
def show(o, depth):
    if isinstance(o, dict):
        for k, v in list(o.items())[:16]:
            print('  ' * depth + str(k), '' if isinstance(v, (dict, list)) else repr(v)[:90])
            if depth < maxd:
                show(v, depth + 1)
        if len(o) > 16:
            print('  ' * depth + '... %d keys' % len(o))
    elif isinstance(o, list):
        print('  ' * depth + '[list %d]' % len(o), repr(o[0])[:300] if o else '')
show(d, 0)
