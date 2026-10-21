"""Load again the inputs this study does not ship, with e2er-data.

Written by e2er at export on 2026-10-21, from the loads the run recorded in
data_sources.json. 

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
import time
from pathlib import Path

# What the run loaded and how to load it again (e2er-data arguments; "rows": how many rows the run's load
# wrote into the table, when it recorded that).
RELOADS = [
    {
        "table": "gutenberg_texts_c1",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "2276,7987,1384,7087,601,6450,7974,161,2496,6490,6086,1296,4927,105,1051,792,84,7281,4926,6112",
            "--table",
            "gutenberg_texts_c1"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 2276, 7987, 1384, 7087, 601, 6450, 7974, 161, 2496, 6490, 6086, 1296, 4927, 105, 1051, 792, 84, 7281, 4926, 6112 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 20
    },
    {
        "table": "gutenberg_texts_c2",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "917,203,1366,1235,1258,77,599,619,4590,4067,1028,4631,2472,2759,145,768,1565,422,15",
            "--table",
            "gutenberg_texts_c2"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 917, 203, 1366, 1235, 1258, 77, 599, 619, 4590, 4067, 1028, 4631, 2472, 2759, 145, 768, 1565, 422, 15 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 19
    },
    {
        "table": "gutenberg_texts_c3",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "1627,4957,1608,1748,1353,335,83,4795,357,1290,287,154,325,155,169,3365,2601,2695,547,581",
            "--table",
            "gutenberg_texts_c3"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 1627, 4957, 1608, 1748, 1353, 335, 83, 4795, 357, 1290, 287, 154, 325, 155, 169, 3365, 2601, 2695, 547, 581 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 20
    },
    {
        "table": "gutenberg_texts_c5",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "321,3427,140,2687,78,3413,5626,1908,5349,3247,1878,4284,5009,5610,1881,1976,4747,1269,330,1386",
            "--table",
            "gutenberg_texts_c5"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 321, 3427, 140, 2687, 78, 3413, 5626, 1908, 5349, 3247, 1878, 4284, 5009, 5610, 1881, 1976, 4747, 1269, 330, 1386 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 20
    },
    {
        "table": "gutenberg_texts_c4",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "493,1690,3044,174,367,2721,4393,6008,122,4982,176,903,973,491,372,1851,604,133,3823,477",
            "--table",
            "gutenberg_texts_c4"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 493, 1690, 3044, 174, 367, 2721, 4393, 6008, 122, 4982, 176, 903, 973, 491, 372, 1851, 604, 133, 3823, 477 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 20
    },
    {
        "table": "gutenberg_texts_c6",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "2546,4922,1155,6115,2126,5738,1402,172,1602,1182,765,543,546,1156,3264,859,3479,3676,1747,748",
            "--table",
            "gutenberg_texts_c6"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 2546, 4922, 1155, 6115, 2126, 5738, 1402, 172, 1602, 1182, 765, 543, 546, 1156, 3264, 859, 3479, 3676, 1747, 748 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 20
    },
    {
        "table": "gutenberg_texts_c3_refill",
        "args": [
            "gutenberg",
            "text",
            "--ids",
            "993,6102,750,1684,6113,2374,840,5700,693",
            "--table",
            "gutenberg_texts_c3_refill"
        ],
        "what": "Project Gutenberg ebooks (catalogue via Gutendex; texts from Project Gutenberg's mirror), Project Gutenberg texts 993, 6102, 750, 1684, 6113, 2374, 840, 5700, 693 (header, footer and licence removed), release 2026-10-14, loaded 2026-10-14",
        "rows": 9
    }
]
# A source that does not answer in time (Gutendex answers a query it has not seen in a minute, then from its
# cache) is asked again: this many times in all, this many seconds apart.
ATTEMPTS = 3
PAUSE_SECONDS = 30
# The other tables of the study's data.db: they came from elsewhere, and get_data.py cannot load them.
OTHER_TABLES = []


def e2er_data() -> str:
    found = os.environ.get("E2ER_DATA") or shutil.which("e2er-data")
    if not found:
        sys.exit("e2er-data was not found. Install e2er (pip install e2er), or run `e2er reproduce` on this folder.")
    return found


def count(here: Path, item: dict) -> int:
    """The rows of the item's table in the folder's data.db (0 without it)."""
    db = here / "data.db"
    if not db.is_file():
        return 0
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            (rows,) = con.execute('SELECT COUNT(*) FROM "' + item["table"].replace('"', '""') + '"').fetchone()
        finally:
            con.close()
    except sqlite3.Error:
        return 0
    return int(rows)


def present(here: Path, item: dict) -> bool:
    if item.get("table"):
        return count(here, item) > 0
    return (here / item["file"]).is_file()


def load(here: Path, env: dict, item: dict) -> str:
    """Load one item again; an empty string when it worked, else why not."""
    cmd = [e2er_data(), "--paper-id", here.name, "--specialist", "researcher", *item["args"]]
    out = subprocess.run(cmd, env=env, capture_output=True, text=True)
    try:
        result = json.loads(out.stdout)
    except ValueError:
        result = {"error": (out.stderr or out.stdout).strip()[-300:]}
    if out.returncode != 0 or result.get("error") or not present(here, item):
        return str(result.get("error") or "nothing was loaded")
    return ""


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
        why = ""
        for attempt in range(1, ATTEMPTS + 1):
            why = load(here, env, item)
            if not why or present(here, item):
                break
            if attempt < ATTEMPTS:
                print(f"{target}: not loaded ({why}); trying again in {PAUSE_SECONDS} s", file=sys.stderr)
                time.sleep(PAUSE_SECONDS)
        if why:
            failed.append(f"{target} ({item['what']}): {why}")
            continue
        if item.get("table") and isinstance(item.get("rows"), int) and count(here, item) < item["rows"]:
            # A load that stopped early (a source's time limit) has only some of the rows the run loaded.
            failed.append(
                f"{target} ({item['what']}): loaded {count(here, item)} of the "
                f"{item['rows']} rows the run loaded"
            )
            continue
        print(f"{target}: loaded again ({item['what']})")
    if failed:
        print("Could not load:", *failed, sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
