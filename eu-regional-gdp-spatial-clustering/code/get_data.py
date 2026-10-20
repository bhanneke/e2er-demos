"""Load again the inputs this study does not ship, with e2er-data.

Written by e2er at export on 2026-10-15, from the loads the run recorded in
data_sources.json. Eurostat GISCO's terms allow non-commercial use only, with the notice '© EuroGeographics for the administrative boundaries' on every map, so a published study may leave its data out.

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
        "table": "gdp_pps_nuts2",
        "args": [
            "eurostat",
            "data",
            "--dataset",
            "nama_10r_2gdp",
            "--filter",
            "unit=PPS_EU27_2020_HAB",
            "--geo-level",
            "nuts2",
            "--start",
            "2015",
            "--end",
            "2024",
            "--table",
            "gdp_pps_nuts2"
        ],
        "what": "Eurostat database (dissemination API), European Commission, Eurostat nama_10r_2gdp: Gross domestic product (GDP) at current market prices by NUTS 2 region (unit=PPS_EU27_2020_HAB, nuts2), 2015\u20132024, release 2026-02-10T11:00:00+0100, loaded 2026-10-14"
    },
    {
        "table": "nuts2_boundaries",
        "args": [
            "gisco",
            "nuts",
            "--level",
            "2",
            "--year",
            "2024",
            "--scale",
            "20M",
            "--crs",
            "3035",
            "--table",
            "nuts2_boundaries"
        ],
        "what": "GISCO geographical data (NUTS regions, countries), Eurostat, NUTS 2 regions, NUTS 2024, 1:20 million, EPSG:3035, release NUTS 2024, loaded 2026-10-14"
    },
    {
        "table": "pop_nuts2",
        "args": [
            "eurostat",
            "data",
            "--dataset",
            "demo_r_d2jan",
            "--filter",
            "sex=T,age=TOTAL",
            "--geo-level",
            "nuts2",
            "--start",
            "2024",
            "--end",
            "2024",
            "--table",
            "pop_nuts2"
        ],
        "what": "Eurostat database (dissemination API), European Commission, Eurostat demo_r_d2jan: Population on 1 January by age, sex and NUTS 2 region (sex=T, age=TOTAL, nuts2), 2024\u20132024, release 2026-08-28T23:00:00+0200, loaded 2026-10-14"
    }
]
# The other tables of the study's data.db: they came from elsewhere, and get_data.py cannot load them.
OTHER_TABLES = ["gdp_pps_sample"]


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
