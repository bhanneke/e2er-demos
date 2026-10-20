import json
d = json.load(open('data_dictionary.json'))
cols = {"gdp_pps_nuts2": ["value"], "nuts2_boundaries": ["nuts_id", "geometry"], "pop_nuts2": ["value"]}
for t in d["tables"]:
    t["columns"] = [{"name": c, "min_non_null": 0.9} for c in cols[t["name"]]]
json.dump(d, open('data_dictionary.json', 'w'), indent=2, ensure_ascii=False)
print("ok")
