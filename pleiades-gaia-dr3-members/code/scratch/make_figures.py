"""Build figure_spec.json for the Pleiades Gaia DR3 figures from data.db.

Values are read from the gaia_dr3 table with the same quality cut the figure
source names, so the figure check re-reads the identical rows. The distance
histogram takes its bins from estimation_results.json (distributions.distance),
which the figure check re-reads from the same file. The members' CMD reads the
gaia_clean table, whose cmd_group marks the members; load_members.py writes
that table with the existing membership definition, and nothing is re-estimated here.
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUALITY = "astrometric_params_solved IN (31, 95) AND ruwe < 1.4 AND parallax_over_error > 10"
RESULTS = json.loads((ROOT / "estimation_results.json").read_text(encoding="utf-8"))

con = sqlite3.connect(ROOT / "data.db")
con.row_factory = sqlite3.Row


def points(x_col, y_col, extra=""):
    rows = con.execute(
        f"SELECT source_id, {x_col}, {y_col} FROM gaia_dr3 "
        f"WHERE {QUALITY}{extra} ORDER BY source_id"
    ).fetchall()
    return [r[x_col] for r in rows], [r[y_col] for r in rows]


vpd_x, vpd_y = points("pmra", "pmdec")
cmd_x, cmd_y = points("bp_rp", "phot_g_mean_mag", " AND bp_rp IS NOT NULL")

# members and field, from the gaia_clean table written by load_members.py
MEMBER_WHERE = "bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL"
mem_rows = con.execute(
    f"SELECT bp_rp, phot_g_mean_mag, cmd_group FROM gaia_clean WHERE {MEMBER_WHERE} ORDER BY source_id"
).fetchall()
mem_x = [r["bp_rp"] for r in mem_rows]
mem_y = [r["phot_g_mean_mag"] for r in mem_rows]
mem_groups = [r["cmd_group"] for r in mem_rows]

spec = {
    "figures": [
        {
            "filename": "fig_vpd_pm.pdf",
            "figure_type": "scatter",
            "label": "fig:vpd",
            "caption_hint": (
                "Vector-point diagram of the quality-cut Gaia DR3 sample within 3 deg of "
                "the Pleiades centre (parallax_over_error > 10, RUWE < 1.4, 5- or 6-parameter "
                "solutions). No member selection is drawn: membership has not been estimated."
            ),
            "x": vpd_x,
            "y": vpd_y,
            "x_label": "Proper motion in right ascension, pmra (mas/yr)",
            "y_label": "Proper motion in declination, pmdec (mas/yr)",
            "source": {
                "table": "gaia_dr3",
                "columns": {"x": "pmra", "y": "pmdec"},
                "where": QUALITY,
            },
        },
        {
            "filename": "fig_cmd.pdf",
            "figure_type": "scatter",
            "label": "fig:cmd",
            "caption_hint": (
                "Colour-magnitude diagram of the quality-cut Gaia DR3 sample within 3 deg of "
                "the Pleiades centre, photometry not extinction-corrected (Pleiades E(B-V) about "
                "0.04 mag). Members are not marked in this figure; the members' "
                "main-sequence locus is reported in estimation_results.json."
            ),
            "x": cmd_x,
            "y": cmd_y,
            "x_label": "Colour BP - RP (mag, not extinction-corrected)",
            "y_label": "Apparent G magnitude (mag)",
            "source": {
                "table": "gaia_dr3",
                "columns": {"x": "bp_rp", "y": "phot_g_mean_mag"},
                "where": QUALITY + " AND bp_rp IS NOT NULL",
            },
        },
        {
            "filename": "fig_cmd_members.pdf",
            "figure_type": "scatter",
            "label": "fig:cmd_members",
            "caption_hint": (
                "Colour-magnitude diagram of the quality-cut Gaia DR3 sample within 3 deg of "
                "the Pleiades centre, with the members of the parallax and proper-motion "
                "selection marked (Member, 1,095 points with BP-RP) and the other stars grey "
                "(Field, 8,768 points). Photometry not extinction-corrected (Pleiades E(B-V) "
                "about 0.04 mag). The vertical axis is G magnitude drawn with larger values "
                "higher, so the brightest stars are at the bottom of the figure."
            ),
            "x": mem_x,
            "y": mem_y,
            "groups": mem_groups,
            "x_label": "Colour BP - RP (mag, not extinction-corrected)",
            "y_label": "Apparent G magnitude (mag)",
            "source": {
                "table": "gaia_clean",
                "columns": {"x": "bp_rp", "y": "phot_g_mean_mag", "groups": "cmd_group"},
                "where": MEMBER_WHERE,
            },
        },
        {
            "filename": "fig_distance_hist.pdf",
            "figure_type": "histogram",
            "label": "fig:distance",
            "caption_hint": (
                "Distance histogram of the cluster members, 1000/parallax (pc, uncorrected "
                "for the parallax zero point), in 5 pc bins. Counts are those of "
                "estimation_results.json."
            ),
            "bins": [
                {"lower": b["lower"], "upper": b["upper"], "count": b["count"]}
                for b in RESULTS["distributions"]["distance"]["bins"]
            ],
            "x_label": "Distance from 1000/parallax (pc)",
            "y_label": "Members (count)",
            "source": {"results": "distributions.distance.bins"},
        },
    ]
}

out = ROOT / "figure_spec.json"
out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
print(f"vpd points: {len(vpd_x)}")
print(f"cmd points: {len(cmd_x)}")
print(f"wrote {out}")
