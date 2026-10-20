import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ws = Path(".").resolve()
spec = json.load(open("figure_spec.json"))
fig = next(f for f in spec["figures"] if f["filename"] == "fig_cmd.pdf")
g = Counter(fig["groups"])
print("spec points by group:", dict(g), "total", len(fig["x"]))

con = sqlite3.connect("data.db")
q = lambda sql: con.execute(sql).fetchall()
print("pleiades_members rows:", q("SELECT COUNT(*) FROM pleiades_members")[0][0])
print("gaia_clean quality sample:", q("SELECT COUNT(*) FROM gaia_clean")[0][0])
print("gaia_clean Member:", q("SELECT COUNT(*) FROM gaia_clean WHERE cmd_group='Member'")[0][0])
print("gaia_clean Field:", q("SELECT COUNT(*) FROM gaia_clean WHERE cmd_group='Field'")[0][0])
print("members with bp_rp:", q("SELECT COUNT(*) FROM gaia_clean WHERE cmd_group='Member' AND bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL")[0][0])
print("field with bp_rp:", q("SELECT COUNT(*) FROM gaia_clean WHERE cmd_group='Field' AND bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL")[0][0])
print("members not in pleiades_members:", q("SELECT COUNT(*) FROM gaia_clean c WHERE c.cmd_group='Member' AND c.source_id NOT IN (SELECT source_id FROM pleiades_members)")[0][0])
print("field overlapping members:", q("SELECT COUNT(*) FROM gaia_clean c WHERE c.cmd_group='Field' AND c.source_id IN (SELECT source_id FROM pleiades_members)")[0][0])

rows = q("SELECT cmd_group, bp_rp, phot_g_mean_mag FROM gaia_clean WHERE cmd_group IN ('Member','Field') AND bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL")
db = Counter()
for grp, x, y in rows:
    db[(grp, round(x, 6), round(y, 6))] += 1
spec_pts = Counter()
for grp, x, y in zip(fig["groups"], fig["x"], fig["y"]):
    spec_pts[(grp, round(x, 6), round(y, 6))] += 1
print("db points:", len(rows), "spec points match db multiset:", db == spec_pts)
