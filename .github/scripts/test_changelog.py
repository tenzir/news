"""Tests for the shared changelog helpers used by Discord notifications."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from changelog import get_config, get_config_for_entry, get_repository, load_entry


CONFIG = """\
id: tenzir
name: Tenzir Node
repository: tenzir/tenzir
"""

ENTRY = """\
---
title: Batching to ClickHouse
type: feature
authors:
  - somebody
prs:
  - 6445
---

The operator now re-batches events internally.
"""


class ChangelogHelpersTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_config_for_entry_finds_nearest_config(self) -> None:
        self.write("tenzir/changelog/config.yaml", CONFIG)
        entry = self.write("tenzir/changelog/unreleased/foo.md", ENTRY)
        config = get_config_for_entry(entry)
        self.assertEqual(config["id"], "tenzir")

    def test_config_for_entry_prefers_the_closest_config(self) -> None:
        self.write("tenzir/changelog/config.yaml", CONFIG)
        self.write("tenzir/plugins/foo/changelog/config.yaml", "id: tenzir-foo\n")
        entry = self.write("tenzir/plugins/foo/changelog/unreleased/bar.md", ENTRY)
        self.assertEqual(get_config_for_entry(entry)["id"], "tenzir-foo")

    def test_config_for_entry_returns_empty_without_config(self) -> None:
        entry = self.write("orphan/changelog/unreleased/foo.md", ENTRY)
        self.assertEqual(get_config_for_entry(entry), {})

    def test_get_config_reads_the_project_config(self) -> None:
        self.write("tenzir/changelog/config.yaml", CONFIG)
        cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        self.assertEqual(get_config("tenzir")["name"], "Tenzir Node")
        self.assertEqual(get_config("missing"), {})

    def test_get_repository_falls_back_to_convention(self) -> None:
        self.assertEqual(
            get_repository("tenzir", {"repository": "tenzir/tenzir"}),
            "tenzir/tenzir",
        )
        self.assertEqual(get_repository("mcp", {}), "tenzir/mcp")

    def test_load_entry_normalizes_fields(self) -> None:
        entry = self.write("tenzir/changelog/unreleased/foo.md", ENTRY)
        data = load_entry(entry)
        self.assertEqual(data["type"], "feature")
        self.assertEqual(data["title"], "Batching to ClickHouse")
        self.assertEqual(data["authors"], ["somebody"])
        self.assertEqual(data["prs"], [6445])
        self.assertIn("re-batches", data["body"])


if __name__ == "__main__":
    unittest.main()
