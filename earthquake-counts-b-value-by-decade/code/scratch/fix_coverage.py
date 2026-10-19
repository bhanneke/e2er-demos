import json
d = json.load(open('data_dictionary.json'))
for t in d['tables']:
    c = t.get('coverage')
    if c and c['column'] == 'time' and 'T' not in str(c['from']):
        c['from'] = c['from'] + 'T00:00:00Z'
        c['to'] = c['to'] + 'T23:59:59Z'
        print(t['name'], c)
json.dump(d, open('data_dictionary.json', 'w'), indent=2)
