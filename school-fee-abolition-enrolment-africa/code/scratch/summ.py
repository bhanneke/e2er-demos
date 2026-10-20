import json
r = json.load(open('estimation_results.json'))
for k, v in r.items():
    if isinstance(v, dict) and 'coefficients' in v:
        c = v['coefficients']
        a = c.get('att') or list(c.values())[0]
        print(k, v.get('n_observations'), v.get('n_clusters'), round(a['estimate'], 3),
              a.get('se') and round(a['se'], 3), a.get('p_value') and round(a['p_value'], 4))
print(r['pre_trends'])
print(r['placebo'])
print(r['sensitivity'])
print(r['sample_flow'])
print([(p['relative_period'], round(p['estimate'], 1), round(p['se'], 1)) for p in r['event_study']['periods']])
print(r['leave_one_country_out']['by_dropped_country'])
print(r['h3_initial_level']['country_att'])
