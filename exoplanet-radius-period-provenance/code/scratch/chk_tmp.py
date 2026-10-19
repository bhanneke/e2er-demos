import json
fs=json.load(open('figure_spec.json'))
er=json.load(open('estimation_results.json'))
D=er['distributions']
m={'radius_calculated':'log10_radius_fine_calculated','radius_measured_transiting':'log10_radius_fine_measured_transiting','period_calculated':'log10_period_fine_calculated','period_measured_transiting':'log10_period_fine_measured_transiting'}
for g in fs['figures']:
    if g['filename']!='fig_marginals_by_group.pdf': continue
    for p in g['panels']:
        old=p['source']['results'].split('.')[1]
        ek=m[old]
        p['bins']=[dict(lower=round(b['lower'],6),upper=round(b['upper'],6),count=b['count']) for b in D[ek]['bins']]
        p['source']={'results':'distributions.%s.bins'%ek}
        p['x_label']=('log10 planet radius (log10 Earth radii)' if old.startswith('radius') else 'log10 orbital period (log10 days)')
        p['y_label']='Planets'
        print(old,'->',ek,sum(b['count'] for b in p['bins']),p.get('title'))
json.dump(fs,open('figure_spec.json','w'))
