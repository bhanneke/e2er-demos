import json, csv
f = json.load(open("figure_spec.json"))
v = [float(r["gdp_pps"]) for r in csv.DictReader(open("spatial_units.csv"))]
f["figures"][1]["values"] = v
json.dump(f, open("figure_spec.json", "w"), indent=1)
print(len(v))
