"""Tests of reproduce/status.py, on reports of a real run (e2er 0.20.1, 2026-11-11, paths removed).

    python -m unittest discover -s reproduce/tests
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import status as S  # noqa: E402

FIX = HERE / "fixtures"
REPO = "bhanneke/e2er-demos"
RUN = f"https://github.com/{REPO}/actions/runs/123456"
ADDR = "https://e2er.org/bhanneke/frankfurt-temperature-trend-forecasts"


def report(name: str) -> dict:
    return json.loads((FIX / f"report-{name}.json").read_text(encoding="utf-8"))


def entry(rep: dict | None, rc: int | None, **kw) -> dict:
    args = dict(address=ADDR, fetch_exit=0, reproduce_exit=rc, report=rep, log=None, fetch_log=None,
                package=None, e2er_version="0.20.1", run_url=RUN)
    args.update(kw)
    return S.make_entry(**args)


class Entries(unittest.TestCase):
    def test_reproduced(self):
        e = entry(report("reproduced"), 0)
        self.assertEqual(e["verdict"], "reproduced")
        self.assertTrue(e["summary"].startswith("Reproduced: every compared value"))
        self.assertEqual(e["counts"]["identical"], 3479)
        self.assertEqual(e["counts"]["values"], 3539)
        self.assertEqual(e["counts"]["tables_identical"], 4)
        self.assertEqual(S.entry_problems(e, REPO), [])

    def test_not_exact_keeps_e2ers_sentence_and_counts(self):
        e = entry(report("not-exact"), 1)
        self.assertEqual(e["verdict"], "not-exact")
        self.assertIn("1332 value(s) show small differences", e["summary"])
        self.assertEqual((e["counts"]["small_difference"], e["counts"]["differs"], e["counts"]["tables_differ"]), (1332, 4, 1))
        self.assertEqual(S.entry_problems(e, REPO), [])

    def test_inputs_that_differ_are_counted(self):
        e = entry(report("inputs-differ"), 1)
        self.assertEqual(e["verdict"], "not-exact")
        self.assertEqual((e["counts"]["inputs"], e["counts"]["inputs_differ"]), (2, 2))

    def test_failed_step(self):
        e = entry(report("failed"), 2)
        self.assertEqual(e["verdict"], "failed")
        self.assertIn("python clean_rs198.py", e["summary"])
        self.assertNotIn("values", e["counts"])
        self.assertEqual(S.entry_problems(e, REPO), [])

    def test_no_report_takes_the_error_line_of_the_log(self):
        e = entry(None, 2, log=FIX / "reproduce-no-report.log")
        self.assertEqual(e["verdict"], "failed")
        self.assertIn("results/figure_spec.json is not in the folder", e["summary"])
        self.assertIsNone(e["counts"])

    def test_timed_out(self):
        e = entry(None, S.TIMED_OUT)
        self.assertEqual(e["verdict"], "failed")
        self.assertIn("did not finish within the 50 minutes", e["summary"])

    def test_fetch_failure(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "fetch.log"
            log.write_text("Downloading …\nerror: the SHA-256 of the file is not the one e2er.org records\n", encoding="utf-8")
            e = entry(None, None, fetch_exit=1, fetch_log=log)
        self.assertEqual(e["verdict"], "failed")
        self.assertTrue(e["summary"].startswith("e2er fetch could not download"))
        self.assertIn("SHA-256", e["summary"])
        self.assertIsNone(e["package_sha256"])

    def test_package_sha256(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "study.e2er"
            p.write_bytes(b"abc")
            e = entry(report("reproduced"), 0, package=p)
        self.assertEqual(e["package_sha256"], "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_source_changed_in_any_likely_form(self):
        base = report("inputs-differ")
        forms = [
            {"category": "source-changed"},
            {"outcome": "source_changed"},
            {"source_changed": True},
            {"source": {"changed": True, "recorded": "sha256:…"}},
            {"inputs": [{"path": "data/gaia_dr3.csv", "status": "source_changed"}]},
            {"verdict": "The source data changed since the study was published: data/gaia_dr3.csv."},
        ]
        for f in forms:
            with self.subTest(f=f):
                e = entry({**base, **f}, 1)
                self.assertEqual(e["verdict"], "source-changed")
                self.assertEqual(S.entry_problems(e, REPO), [])
        # A new exit code for the category is read the same way.
        self.assertEqual(entry({**base, "category": "source-changed"}, 3)["verdict"], "source-changed")
        # Exit 0 is reproduced, whatever else the report says.
        self.assertEqual(entry({**base, "category": "source-changed"}, 0)["verdict"], "reproduced")

    def test_unknown_fields_and_odd_values_do_not_break_it(self):
        rep = {**report("reproduced"), "pre_publish": {"verdict": "x"}, "results": [{"counts": {"identical": -3, "differs": "many"}}, "x"], "tables": "none"}
        e = entry(rep, 0)
        self.assertEqual(S.entry_problems(e, REPO), [])
        self.assertEqual(e["counts"]["identical"], 0)

    def test_summary_is_one_plain_line(self):
        e = entry({"verdict": "Line one\nline two <script>alert(1)</script> " + chr(0x202E) + chr(0x2028) + "x" * 400}, 1)
        self.assertNotIn("\n", e["summary"])
        self.assertNotIn("<", e["summary"])
        self.assertNotIn(chr(0x202E), e["summary"])
        self.assertNotIn(chr(0x2028), e["summary"])
        self.assertLessEqual(len(e["summary"]), S.SUMMARY_MAX)
        self.assertEqual(S.entry_problems(e, REPO), [])


class Validation(unittest.TestCase):
    def test_bad_entries(self):
        good = entry(report("reproduced"), 0)
        bad = [
            {**good, "address": "https://evil.example/x/y"},
            {**good, "verdict": "great"},
            {**good, "run_url": "https://github.com/someone/else/actions/runs/1"},
            {**good, "run_url": f"https://github.com/{REPO}/actions/runs/1?x=javascript:"},
            {**good, "summary": "<b>hi</b>"},
            {**good, "summary": ""},
            {**good, "checked_at": "yesterday"},
            {**good, "counts": {"identical": -1}},
            {**good, "package_sha256": "abc"},
            {**good, "extra": 1},
        ]
        for b in bad:
            with self.subTest(b={k: b[k] for k in b if b[k] != good.get(k)}):
                self.assertNotEqual(S.entry_problems(b, REPO), [])


class Merging(unittest.TestCase):
    studies = ["https://e2er.org/bhanneke/a", "https://e2er.org/bhanneke/b", "https://e2er.org/bhanneke/c"]

    def mk(self, addr: str, when: str, verdict: str = "reproduced") -> dict:
        return {"address": addr, "checked_at": when, "e2er_version": "0.20.1", "verdict": verdict, "summary": "Reproduced.",
                "counts": None, "exit_code": 0, "package_sha256": None, "run_url": RUN}

    def test_keeps_previous_entries_of_studies_this_run_did_not_check(self):
        prev = S.merge(self.studies, [self.mk(a, "2026-11-01T05:00:00Z") for a in self.studies], None, repository=REPO, run_url=RUN)
        doc = S.merge(self.studies[:2] + ["https://e2er.org/bhanneke/c"], [self.mk(self.studies[0], "2026-11-08T05:00:00Z", "failed")], prev,
                      repository=REPO, run_url=RUN)
        self.assertEqual(S.status_problems(doc), [])
        by = {s["address"]: s for s in doc["studies"]}
        self.assertEqual(by[self.studies[0]]["verdict"], "failed")
        self.assertEqual(by[self.studies[1]]["checked_at"], "2026-11-01T05:00:00Z")

    def test_drops_studies_no_longer_listed_and_ignores_a_bad_previous_file(self):
        prev = S.merge(self.studies, [self.mk(a, "2026-11-01T05:00:00Z") for a in self.studies], None, repository=REPO, run_url=RUN)
        doc = S.merge(self.studies[:1], [], prev, repository=REPO, run_url=RUN)
        self.assertEqual([s["address"] for s in doc["studies"]], self.studies[:1])
        doc = S.merge(self.studies, [], {"schema": "other"}, repository=REPO, run_url=RUN)
        self.assertEqual(doc["studies"], [])

    def test_the_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "studies.json").write_text(json.dumps({"studies": [{"address": ADDR}]}), encoding="utf-8")
            (d / "report.json").write_text(json.dumps(report("not-exact")), encoding="utf-8")
            rc = S.main(["entry", "--address", ADDR, "--fetch-exit", "0", "--reproduce-exit", "1", "--report", str(d / "report.json"),
                         "--e2er-version", "e2er 0.20.1", "--repository", REPO, "--run-url", RUN, "-o", str(d / "e" / "x" / "entry.json")])
            self.assertEqual(rc, 0)
            rc = S.main(["merge", "--studies", str(d / "studies.json"), "--entries", str(d / "e"), "--repository", REPO, "--run-url", RUN,
                         "-o", str(d / "out.json"), "--summary", str(d / "summary.md")])
            self.assertEqual(rc, 0)
            doc = json.loads((d / "out.json").read_text(encoding="utf-8"))
            self.assertEqual(S.status_problems(doc), [])
            self.assertEqual(doc["studies"][0]["e2er_version"], "0.20.1")
            self.assertIn("not-exact", (d / "summary.md").read_text(encoding="utf-8"))

    def test_matrix_and_the_studies_file_of_this_repository(self):
        # This repository's own list (whatever studies it names), so a copy of the folder tests its own.
        addresses = S.read_studies(HERE.parent / "studies.json")
        self.assertEqual(len(S.matrix(addresses)), len(addresses))
        name = addresses[0].rsplit("/", 1)[1]
        self.assertEqual(S.matrix(addresses, name), [{"address": addresses[0], "name": name}])
        with self.assertRaises(SystemExit):
            S.matrix(addresses, "no-such-study")


if __name__ == "__main__":
    unittest.main()


class SourceUnavailable(unittest.TestCase):
    def test_a_source_that_did_not_answer_is_its_own_verdict(self):
        report = {"category": "source_unavailable", "verdict": "Could not reproduce: WHO did not answer."}
        e = entry(report, 2)
        self.assertEqual(e["verdict"], "source-unavailable")
        self.assertEqual(e["summary"], "Could not reproduce: WHO did not answer.")

    def test_the_category_of_e2er_reports_maps_to_source_changed(self):
        self.assertEqual(entry({"category": "source_changed", "verdict": "x"}, 2)["verdict"], "source-changed")

