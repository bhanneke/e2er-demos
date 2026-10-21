import json, sqlite3
s = json.load(open('summary_statistics.json'))
for f in s['sample_flow']:
    print(f)
print(s['n_observations'], s['n_units'], s['n_tokens'], s['n_types'], s['weather_dictionary'], s['front_matter_chars_cut'], s['outcome'])
for c, v in s['by_cohort'].items():
    print(c, v['n_documents'], v['n_authors'], v['n_tokens'], v['tokens_per_doc_median'], v['birth_year_min'], v['birth_year_max'], v['n_weather_dictionary_hits'])
con = sqlite3.connect('data.db')
print(con.execute("select count(*), sum(n) from weather_dictionary_hits").fetchone())
for r in con.execute("select cohort, source_id, author, substr(title,1,35) from corpus order by cohort, source_id"):
    print(r)
