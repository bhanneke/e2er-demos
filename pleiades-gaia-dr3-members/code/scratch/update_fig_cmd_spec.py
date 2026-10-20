import json

spec_path = "figure_spec.json"
spec = json.load(open(spec_path))
figs = spec["figures"]

members = next(f for f in figs if f["filename"] == "fig_cmd_members.pdf")
assert len(members["x"]) == len(members["y"]) == len(members["groups"]) == 9863
assert members["groups"].count("Member") == 1095
assert members["groups"].count("Field") == 8768

new = {
    "filename": "fig_cmd.pdf",
    "figure_type": "scatter",
    "label": "fig:cmd",
    "caption_hint": (
        "Colour-magnitude diagram of the Pleiades members and the field stars of the quality-cut "
        "Gaia DR3 sample within 3 deg of the Pleiades centre (parallax_over_error > 10, RUWE < 1.4, "
        "5- or 6-parameter solutions). Member: the 1,112 members of the parallax and proper-motion "
        "selection, of which 1,095 have a BP-RP colour and are plotted; the other 17 have no BP-RP and "
        "cannot be placed in the diagram. Field: the quality-cut sample minus the 1,112 members, 8,858 "
        "stars, of which 8,768 have a BP-RP colour and are plotted. Photometry is not extinction-corrected "
        "(Pleiades E(B-V) about 0.04 mag). The vertical axis shows G with larger values higher, so the "
        "brightest members are at the bottom of the figure."
    ),
    "x": members["x"],
    "y": members["y"],
    "groups": members["groups"],
    "x_label": "Colour BP - RP (mag, not extinction-corrected)",
    "y_label": "Apparent G magnitude (mag)",
    "source": {
        "table": "gaia_clean",
        "columns": {"x": "bp_rp", "y": "phot_g_mean_mag", "groups": "cmd_group"},
        "where": "cmd_group IN ('Member', 'Field') AND bp_rp IS NOT NULL AND phot_g_mean_mag IS NOT NULL",
    },
}

idx = next(i for i, f in enumerate(figs) if f["filename"] == "fig_cmd.pdf")
figs[idx] = new
json.dump(spec, open(spec_path, "w"), indent=2)
print("fig_cmd updated at index", idx, "points", len(new["x"]))
