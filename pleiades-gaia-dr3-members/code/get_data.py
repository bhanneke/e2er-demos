"""Load again the inputs this study does not ship, with e2er-data.

Written by e2er at export on 2026-10-15, from the loads the run recorded in
data_sources.json. ESA Gaia Data Release 3's terms allow non-commercial use only, with credit to ESA/Gaia/DPAC (CC BY-NC 3.0 IGO), so a published study may leave its data out.

An input the folder already has (the study's own copy) is kept; only a missing
one is loaded again, with the command below. A table is loaded into data.db, a
file into data/. The sources revise their data, so a reloaded input can differ
from the study's: `e2er reproduce` compares every input with the study's own
file by SHA-256 and says which differ.

Run it from the run folder (`e2er reproduce` does this for you).
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

# What the run loaded and how to load it again (e2er-data arguments).
RELOADS = [
    {
        "file": "data/gaia_dr3.csv",
        "args": [
            "gaia",
            "query",
            "--adql",
            "SELECT source_id, ra, dec, DISTANCE(POINT('ICRS', ra, dec), POINT('ICRS', 56.75, 24.12)) AS dist_deg, parallax, parallax_error, parallax_over_error, pmra, pmra_error, pmdec, pmdec_error, ruwe, astrometric_params_solved, visibility_periods_used, phot_g_mean_mag, phot_g_mean_flux_over_error, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp FROM gaiadr3.gaia_source WHERE 1 = CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 56.75, 24.12, 3)) AND parallax > 2 AND parallax_over_error > 5",
            "--save-to",
            "gaia_dr3.csv"
        ],
        "what": "Gaia Data Release 3 (ESA/Gaia/DPAC), Gaia ESA Archive, Gaia archive ADQL query: SELECT source_id, ra, dec, DISTANCE(POINT('ICRS', ra, dec), POINT('ICRS', 56.75, 24.12)) AS dist_deg, parallax, parallax_error, parallax_over_error, pmra, pmra_error, pmdec, pmdec_error, ruwe, astrometric_params_solved, visibility_periods_used, phot_g_mean_mag, phot_g_mean_flux_over_error, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp FROM gaiadr3.gaia_source WHERE 1 = CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 56.75, 24.12, 3)) AND parallax > 2 AND parallax_over_error > 5, release DR3, loaded 2026-10-13"
    }
]
# The other tables of the study's data.db: they came from elsewhere, and get_data.py cannot load them.
OTHER_TABLES = []


def e2er_data() -> str:
    found = os.environ.get("E2ER_DATA") or shutil.which("e2er-data")
    if not found:
        sys.exit("e2er-data was not found. Install e2er (pip install e2er), or run `e2er reproduce` on this folder.")
    return found


def present(here: Path, item: dict) -> bool:
    if item.get("table"):
        db = here / "data.db"
        if not db.is_file():
            return False
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            try:
                (rows,) = con.execute('SELECT COUNT(*) FROM "' + item["table"].replace('"', '""') + '"').fetchone()
            finally:
                con.close()
        except sqlite3.Error:
            return False
        return rows > 0
    return (here / item["file"]).is_file()


def main() -> int:
    here = Path.cwd().resolve()
    env = {**os.environ, "E2ER_WORKSPACE_ROOT": str(here.parent)}
    if OTHER_TABLES and not (here / "data.db").is_file():
        print(
            "data.db is not in the folder. get_data.py can load only the tables listed in it again; "
            "the study also used "
            + ", ".join(OTHER_TABLES)
            + ", which came from other sources. Put the study's data.db in the folder to run it as it ran.",
            file=sys.stderr,
        )
    failed = []
    for item in RELOADS:
        target = item.get("table") or item.get("file")
        if present(here, item):
            print(f"{target}: the study's own copy is here, not loaded again")
            continue
        cmd = [e2er_data(), "--paper-id", here.name, "--specialist", "researcher", *item["args"]]
        out = subprocess.run(cmd, env=env, capture_output=True, text=True)
        try:
            result = json.loads(out.stdout)
        except ValueError:
            result = {"error": (out.stderr or out.stdout).strip()[-300:]}
        if out.returncode != 0 or result.get("error") or not present(here, item):
            failed.append(f"{target} ({item['what']}): {result.get('error') or 'nothing was loaded'}")
            continue
        print(f"{target}: loaded again ({item['what']})")
    if failed:
        print("Could not load:", *failed, sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
