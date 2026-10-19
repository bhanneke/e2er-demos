import sqlite3, json
con = sqlite3.connect("data.db")
con.execute("CREATE TABLE w_new AS SELECT window,start_year,end_year,window_type,n_total FROM eq_bvalue_windows")
con.execute("DROP TABLE eq_bvalue_windows")
con.execute("ALTER TABLE w_new RENAME TO eq_bvalue_windows")
con.commit()
print(con.execute("select * from eq_bvalue_windows").fetchall())
d = json.load(open("data_dictionary.json"))
for t in d["tables"]:
    if t["name"] == "eq_bvalue_windows":
        t["key"] = ["window"]
        t["columns"] = [c for c in t["columns"] if c["name"] not in ("mc_rule", "mc", "n_above_mc", "mean_mag_above_mc")]
        t["series"] = "decade windows for the b-value analysis (sample sizes only)"
        t["role"] = ("sample sizes per decade (1976-85, 1986-95, 1996-2005, 2006-15, 2016-25; no sliding windows). "
                     "Mc (maximum curvature +0.2, goodness-of-fit 90/95%, common threshold = largest decade Mc), n above Mc and the "
                     "b-value (Aki-Utsu MLE, dM = 0.1) are estimates and are computed in the analysis step from eq_clean_m45, not stored here.")
json.dump(d, open("data_dictionary.json", "w"), indent=2)
