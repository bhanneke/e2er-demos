"""The workflow's supply chain, by the rules of the e2er repository (tests/test_workflow_supply_chain.py
there): read-only by default, one job that writes, actions pinned to commit SHAs, no kept credentials."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "reproduce.yml"


class Workflow(unittest.TestCase):
    text = WORKFLOW.read_text(encoding="utf-8")

    def test_read_only_except_the_publish_job(self):
        self.assertRegex(self.text, r"(?m)^permissions:\n  contents: read\n")
        writes = re.findall(r"(?m)^\s+contents: write", self.text)
        self.assertEqual(len(writes), 1)
        self.assertNotRegex(self.text, r"(?m)^\s+(actions|id-token|issues|pull-requests|packages): write")
        publish = self.text.split("\n  publish:\n", 1)[1]
        self.assertIn("contents: write", publish)

    def test_every_action_is_pinned_to_a_commit(self):
        uses = [line for line in self.text.splitlines() if re.search(r"uses:\s*\S", line)]
        self.assertTrue(uses)
        for line in uses:
            ref = re.search(r"uses:\s*(\S+)", line).group(1)
            self.assertRegex(ref, r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$", line)
            self.assertRegex(line, r"#\s*v\d+\.\d+\.\d+", line)

    def test_checkouts_keep_no_credentials(self):
        self.assertEqual(self.text.count("uses: actions/checkout@"), self.text.count("persist-credentials: false"))

    def test_timeouts(self):
        self.assertIn("timeout-minutes: 60", self.text)
        self.assertNotIn("${{ matrix", "\n".join(l for l in self.text.splitlines() if l.strip().startswith(("e2er ", "python "))))


if __name__ == "__main__":
    unittest.main()
