"""The reproduction status of the studies in reproduce/studies.json (see reproduce/README.md).

The workflow .github/workflows/reproduce.yml calls this script three times:

  python -I reproduce/status.py matrix  --studies reproduce/studies.json [--only NAME]
      prints the job matrix: one entry per study, {"address", "name"}.
  python -I reproduce/status.py entry   --address URL --fetch-exit N [--reproduce-exit N]
                                        [--report report.json] [--log reproduce.log]
                                        [--fetch-log fetch.log] [--package study.e2er]
                                        --e2er-version V --run-url URL -o entry.json
      turns one study's run into one entry of reproduce-status.json.
  python -I reproduce/status.py merge   --studies reproduce/studies.json --entries DIR
                                        [--previous reproduce-status.json] --repository OWNER/REPO
                                        --run-url URL -o reproduce-status.json
      collects the entries, keeps the previous entry of a study this run did not check, and
      writes the file the release `reproduce-status` carries.

Only the standard library; Python 3.10 or later. The report of `e2er reproduce --json` is read
defensively: fields this script does not know are ignored, missing ones leave their count out.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "e2er-reproduce-status/1"
VERDICTS = ("reproduced", "not-exact", "failed", "source-changed", "source-unavailable")
ADDRESS_RE = re.compile(r"^https://e2er\.org/([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/([A-Za-z0-9._-]{1,100})$")
REPO_RE = re.compile(r"^([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/([A-Za-z0-9._-]{1,100})$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[A-Za-z0-9.+-]{0,30})$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SUMMARY_MAX = 300
#: The exit code of `timeout` when it stopped e2er reproduce.
TIMED_OUT = 124
MAX_STUDIES = 200
#: The counts an entry may carry, all whole numbers of 0 or more.
COUNT_KEYS = (
    "values", "identical", "same_at_precision", "small_difference", "differs",
    "missing_in_rerun", "only_in_rerun",
    "tables_rendered", "tables_identical", "tables_differ",
    "inputs", "inputs_differ",
)
RESULT_COUNTS = ("identical", "same_at_precision", "small_difference", "differs", "missing_in_rerun", "only_in_rerun")
ENTRY_KEYS = {"address", "checked_at", "e2er_version", "verdict", "summary", "counts", "exit_code", "package_sha256", "run_url"}
_SOURCE_CHANGED = re.compile(r"^source[-_ ]changed$")
_SOURCE_UNAVAILABLE = re.compile(r"^source[-_ ]unavailable$")


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def plain(text: object, limit: int = SUMMARY_MAX) -> str:
    """One line of plain text: no control characters, no markup brackets, at most `limit` characters."""
    s = re.sub(r"[\x00-\x1f\x7f-\x9f\u2028\u2029\u202a-\u202e\u2066-\u2069]+", " ", str(text or ""))
    s = s.replace("<", "(").replace(">", ")")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s


def run_url_ok(url: object, repository: str) -> bool:
    return isinstance(url, str) and re.fullmatch(rf"https://github\.com/{re.escape(repository)}/actions/runs/\d{{1,20}}", url) is not None


# ---------------------------------------------------------------------------------------- reading


def _int(v: object) -> int | None:
    return v if isinstance(v, int) and not isinstance(v, bool) and v >= 0 else None


def counts_of(report: dict) -> dict | None:
    """The numbers of compared values, tables and inputs the report gives; None without any."""
    out: dict[str, int] = {}
    results = report.get("results")
    if isinstance(results, list):
        sums = {k: 0 for k in RESULT_COUNTS}
        values = 0
        seen = False
        for r in results:
            if not isinstance(r, dict):
                continue
            c = r.get("counts")
            if isinstance(c, dict):
                seen = True
                for k in RESULT_COUNTS:
                    sums[k] += _int(c.get(k)) or 0
            values += _int(r.get("values")) or 0
        if seen:
            out.update(sums)
            out["values"] = values or sum(sums.values())
    tables = report.get("tables")
    if isinstance(tables, dict):
        n = lambda k: len(tables[k]) if isinstance(tables.get(k), list) else _int(tables.get(k))  # noqa: E731
        for key, field in (("tables_rendered", "rendered"), ("tables_identical", "identical"), ("tables_differ", "differ")):
            v = n(field)
            if v is not None:
                out[key] = v
    inputs = report.get("inputs")
    if isinstance(inputs, list):
        rows = [i for i in inputs if isinstance(i, dict)]
        out["inputs"] = len(rows)
        out["inputs_differ"] = sum(1 for i in rows if str(i.get("status", "")).lower() not in ("identical", "same_rows", "not_compared", ""))
    return out or None


def source_changed(report: dict) -> bool:
    """Whether the report says the data a step loaded again differ from the recorded fingerprint.

    e2er adds this category in a later release; its field names are not fixed here, so every
    likely form counts: a category/outcome field, a flag, an input's status, the verdict's words."""
    for key in ("category", "outcome", "result", "status", "kind", "verdict_category"):
        v = report.get(key)
        if isinstance(v, str) and _SOURCE_CHANGED.match(v.strip().lower()):
            return True
    if report.get("source_changed") is True:
        return True
    src = report.get("source")
    if isinstance(src, dict) and src.get("changed") is True:
        return True
    for i in report.get("inputs") or []:
        if isinstance(i, dict) and isinstance(i.get("status"), str) and _SOURCE_CHANGED.match(i["status"].strip().lower()):
            return True
    verdict = report.get("verdict")
    return isinstance(verdict, str) and bool(re.match(r"^\s*(the )?source(?: data)? (has )?changed", verdict, re.I))


def last_error(log: Path | None) -> str:
    """The last line of an e2er log that says what went wrong (`error: …`), or ''."""
    if not log or not log.is_file():
        return ""
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()[-200:]
    for line in reversed(lines):
        m = re.match(r"^\s*(?:error|Error|ERROR)\s*:\s*(.+)$", line)
        if m:
            return plain(m.group(1), 200)
    return ""


def sha256_of(path: Path | None) -> str | None:
    if not path or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_entry(*, address: str, fetch_exit: int, reproduce_exit: int | None, report: dict | None,
               log: Path | None, fetch_log: Path | None, package: Path | None,
               e2er_version: str, run_url: str, checked_at: str | None = None) -> dict:
    """One study's entry of reproduce-status.json."""
    entry = {
        "address": address,
        "checked_at": checked_at or now_utc(),
        "e2er_version": e2er_version,
        "verdict": "failed",
        "summary": "",
        "counts": None,
        "exit_code": None,
        "package_sha256": sha256_of(package) if fetch_exit == 0 else None,
        "run_url": run_url,
    }
    if fetch_exit != 0:
        why = last_error(fetch_log)
        entry["summary"] = plain("e2er fetch could not download the study package and check it against e2er.org" + (f": {why}" if why else "."))
        return entry
    entry["exit_code"] = reproduce_exit
    if not isinstance(report, dict) and reproduce_exit == TIMED_OUT:
        entry["summary"] = "e2er reproduce did not finish within the 50 minutes the workflow gives a study."
        return entry
    if not isinstance(report, dict):
        why = last_error(log)
        entry["summary"] = plain("e2er reproduce stopped before it wrote a report" + (f": {why}" if why else "."))
        return entry
    entry["counts"] = counts_of(report)
    said = plain(report.get("verdict"))
    if reproduce_exit == 0:
        entry["verdict"] = "reproduced"
    elif source_changed(report):
        entry["verdict"] = "source-changed"
    elif isinstance(report.get("category"), str) and _SOURCE_UNAVAILABLE.match(report["category"].strip().lower()):
        entry["verdict"] = "source-unavailable"
    elif reproduce_exit == 1:
        entry["verdict"] = "not-exact"
    else:
        entry["verdict"] = "failed"
    entry["summary"] = said or {
        "reproduced": "Reproduced.",
        "not-exact": "Not reproduced exactly.",
        "source-changed": "The data loaded again from the source differ from the data the study recorded.",
        "failed": "The study's code could not be run.",
        "source-unavailable": "A data source did not answer; the next run tries again.",
    }[entry["verdict"]]
    return entry


# ------------------------------------------------------------------------------------- validating


def entry_problems(e: object, repository: str) -> list[str]:
    if not isinstance(e, dict):
        return ["an entry is not an object"]
    out = []
    unknown = set(e) - ENTRY_KEYS
    if unknown:
        out.append(f"unknown fields {sorted(unknown)}")
    if not isinstance(e.get("address"), str) or not ADDRESS_RE.match(e["address"]):
        out.append("address: https://e2er.org/<owner>/<project>")
    if not isinstance(e.get("checked_at"), str) or not TIME_RE.match(e["checked_at"]):
        out.append("checked_at: YYYY-MM-DDTHH:MM:SSZ")
    if not isinstance(e.get("e2er_version"), str) or not VERSION_RE.match(e["e2er_version"]):
        out.append("e2er_version: a version like 0.20.1")
    if e.get("verdict") not in VERDICTS:
        out.append(f"verdict: one of {', '.join(VERDICTS)}")
    s = e.get("summary")
    if not isinstance(s, str) or not s or len(s) > SUMMARY_MAX or s != plain(s):
        out.append(f"summary: one line of plain text, 1 to {SUMMARY_MAX} characters")
    c = e.get("counts")
    if c is not None and (not isinstance(c, dict) or set(c) - set(COUNT_KEYS) or any(_int(v) is None for v in c.values())):
        out.append(f"counts: null or an object of whole numbers ({', '.join(COUNT_KEYS)})")
    if e.get("exit_code") is not None and _int(e.get("exit_code")) is None:
        out.append("exit_code: null or a whole number")
    p = e.get("package_sha256")
    if p is not None and (not isinstance(p, str) or not SHA256_RE.match(p)):
        out.append("package_sha256: null or 64 hex digits")
    if not run_url_ok(e.get("run_url"), repository):
        out.append(f"run_url: https://github.com/{repository}/actions/runs/<id>")
    return out


def status_problems(doc: object) -> list[str]:
    if not isinstance(doc, dict):
        return ["not a JSON object"]
    out = []
    if doc.get("schema") != SCHEMA:
        out.append(f"schema: {SCHEMA}")
    repo = doc.get("repository")
    if not isinstance(repo, str) or not REPO_RE.match(repo):
        return out + ["repository: <owner>/<repository>"]
    if not isinstance(doc.get("generated_at"), str) or not TIME_RE.match(doc["generated_at"]):
        out.append("generated_at: YYYY-MM-DDTHH:MM:SSZ")
    if not run_url_ok(doc.get("run_url"), repo):
        out.append("run_url: the workflow run that wrote the file")
    studies = doc.get("studies")
    if not isinstance(studies, list) or len(studies) > MAX_STUDIES:
        return out + [f"studies: a list of at most {MAX_STUDIES} entries"]
    seen = set()
    for i, e in enumerate(studies):
        out += [f"studies[{i}].{p}" for p in entry_problems(e, repo)]
        a = e.get("address") if isinstance(e, dict) else None
        if a in seen:
            out.append(f"studies[{i}]: {a} is listed twice")
        seen.add(a)
    return out


# ------------------------------------------------------------------------------------------ lists


def read_studies(path: Path) -> list[str]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    addresses = [s.get("address") for s in doc.get("studies", []) if isinstance(s, dict)]
    bad = [a for a in addresses if not isinstance(a, str) or not ADDRESS_RE.match(a)]
    if bad or not addresses:
        raise SystemExit(f"{path}: every study needs an address https://e2er.org/<owner>/<project>; not: {bad}")
    if len(set(addresses)) != len(addresses) or len(addresses) > MAX_STUDIES:
        raise SystemExit(f"{path}: an address is listed twice, or more than {MAX_STUDIES} studies")
    return addresses


def matrix(addresses: list[str], only: str = "") -> list[dict]:
    rows = [{"address": a, "name": ADDRESS_RE.match(a).group(2)} for a in addresses]
    if only:
        rows = [r for r in rows if r["name"] == only or r["address"] == only]
        if not rows:
            raise SystemExit(f"no study {only!r} in the list")
    return rows


def keep_last_result(new: dict | None, old: dict | None) -> dict | None:
    """A source that did not answer says nothing about the study: keep the last real result and say so.

    Only when this run's verdict is source-unavailable and an earlier entry has another verdict; the earlier
    entry keeps its verdict, date and run, and its summary gains one sentence on the source."""
    if not new:
        return old
    if new.get("verdict") != "source-unavailable" or not old or old.get("verdict") == "source-unavailable":
        return new
    note = f" A data source did not answer when the study was rerun on {new['checked_at'][:10]}; this is the result of {old['checked_at'][:10]}."
    kept = dict(old)
    kept["summary"] = plain(old.get("summary", ""), SUMMARY_MAX - len(note)).rstrip() + note
    return kept


def merge(addresses: list[str], entries: list[dict], previous: dict | None, *, repository: str, run_url: str,
          generated_at: str | None = None) -> dict:
    """The status file: this run's entries, and the previous entry of each listed study this run did not check."""
    fresh = {e["address"]: e for e in entries if e.get("address") in addresses}
    old = {}
    if isinstance(previous, dict) and not status_problems(previous) and previous.get("repository") == repository:
        old = {e["address"]: e for e in previous["studies"]}
    studies = [keep_last_result(fresh.get(a), old.get(a)) for a in addresses]
    return {
        "schema": SCHEMA,
        "repository": repository,
        "generated_at": generated_at or now_utc(),
        "run_url": run_url,
        "studies": [s for s in studies if s],
    }


# -------------------------------------------------------------------------------------------- CLI


def _load_json(path: Path | None) -> object:
    if not path or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("matrix")
    m.add_argument("--studies", type=Path, required=True)
    m.add_argument("--only", default="")
    e = sub.add_parser("entry")
    e.add_argument("--address", required=True)
    e.add_argument("--fetch-exit", type=int, required=True)
    e.add_argument("--reproduce-exit", type=int)
    e.add_argument("--report", type=Path)
    e.add_argument("--log", type=Path)
    e.add_argument("--fetch-log", type=Path)
    e.add_argument("--package", type=Path)
    e.add_argument("--e2er-version", required=True)
    e.add_argument("--repository", required=True)
    e.add_argument("--run-url", required=True)
    e.add_argument("-o", "--output", type=Path, required=True)
    g = sub.add_parser("merge")
    g.add_argument("--studies", type=Path, required=True)
    g.add_argument("--entries", type=Path, required=True, help="a folder; every entry.json below it is read")
    g.add_argument("--previous", type=Path)
    g.add_argument("--repository", required=True)
    g.add_argument("--run-url", required=True)
    g.add_argument("-o", "--output", type=Path, required=True)
    g.add_argument("--summary", type=Path, help="also write a Markdown table (the workflow's job summary)")
    a = ap.parse_args(argv)

    if a.cmd == "matrix":
        print(json.dumps(matrix(read_studies(a.studies), a.only.strip())))
        return 0

    if a.cmd == "entry":
        version = re.sub(r"^e2er\s+", "", a.e2er_version.strip())
        entry = make_entry(
            address=a.address, fetch_exit=a.fetch_exit, reproduce_exit=a.reproduce_exit,
            report=_load_json(a.report), log=a.log, fetch_log=a.fetch_log, package=a.package,
            e2er_version=version, run_url=a.run_url,
        )
        problems = entry_problems(entry, a.repository)
        if problems:
            print("the entry is not valid: " + "; ".join(problems), file=sys.stderr)
            return 1
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{entry['address']}: {entry['verdict']} — {entry['summary']}")
        return 0

    addresses = read_studies(a.studies)
    entries = []
    for p in sorted(a.entries.rglob("entry.json")):
        x = _load_json(p)
        problems = entry_problems(x, a.repository)
        if problems:
            print(f"{p}: left out: {'; '.join(problems)}", file=sys.stderr)
            continue
        entries.append(x)
    previous = _load_json(a.previous)
    doc = merge(addresses, entries, previous if isinstance(previous, dict) else None, repository=a.repository, run_url=a.run_url)
    problems = status_problems(doc)
    if problems:
        print("the status file is not valid: " + "; ".join(problems), file=sys.stderr)
        return 1
    a.output.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fresh = {x["address"] for x in entries}
    if a.summary:
        rows = ["| Study | Verdict | Checked | Summary |", "|---|---|---|---|"]
        for s in doc["studies"]:
            when = s["checked_at"][:10] + ("" if s["address"] in fresh else " (earlier run)")
            rows.append(f"| {s['address'].split('/', 3)[-1]} | {s['verdict']} | {when} | {s['summary'].replace('|', '/')} |")
        missing = [x for x in addresses if x not in {s['address'] for s in doc['studies']}]
        rows += ["", *(f"No result for {x}." for x in missing)]
        a.summary.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{len(doc['studies'])} studies, {len(fresh)} checked in this run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
