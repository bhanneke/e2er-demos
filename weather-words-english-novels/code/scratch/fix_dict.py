import json
d = json.load(open('data_dictionary.json'))
for t in d['tables']:
    if t['name'] == 'gutenberg_texts_c3_refill':
        t['min_non_null'] = 0.85
        t['columns'] = [dict(name=c, min_non_null=0.85) for c in ("authors", "author_birth_year", "author_death_year")]
        t['null_note'] = ("pg750 (The High History of the Holy Graal) is anonymous in the catalogue, so author fields "
                          "are null for 1 of 9 rows; it has no birth year and cannot enter a cohort.")
json.dump(d, open('data_dictionary.json', 'w'), indent=2, ensure_ascii=False)
print([t.get('min_non_null') for t in d['tables'] if t['name'] == 'gutenberg_texts_c3_refill'])
