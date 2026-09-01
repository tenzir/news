"""Tests for the shared changelog helpers used by Discord notifications."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from changelog import (
    campaign_identity_errors,
    get_changelog_entry_url,
    get_config,
    get_config_for_entry,
    get_repository,
    load_entry,
    unfold_soft_breaks,
)

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

    def test_changelog_entry_url_uses_config_id_and_file_slug(self) -> None:
        entry = self.write(
            "tenzir/changelog/unreleased/read-and-parse-raw-avro.md", ENTRY
        )
        self.assertEqual(
            get_changelog_entry_url("tenzir", entry, {"id": "tenzir"}),
            "https://tenzir.com/changelog/tenzir/unreleased/#read-and-parse-raw-avro",
        )

    def test_changelog_entry_url_falls_back_to_project(self) -> None:
        entry = self.write("mcp/changelog/unreleased/add-tool.md", ENTRY)
        self.assertEqual(
            get_changelog_entry_url("mcp", entry, {}),
            "https://tenzir.com/changelog/mcp/unreleased/#add-tool",
        )

    def test_load_entry_normalizes_fields(self) -> None:
        entry = self.write("tenzir/changelog/unreleased/foo.md", ENTRY)
        data = load_entry(entry)
        self.assertEqual(data["type"], "feature")
        self.assertEqual(data["title"], "Batching to ClickHouse")
        self.assertEqual(data["authors"], ["somebody"])
        self.assertEqual(data["prs"], [6445])
        self.assertIn("re-batches", data["body"])

    def test_unfold_soft_breaks_joins_wrapped_markdown(self) -> None:
        markdown = """\
Three new functions close the
rendering gap:

- `autocorrelation(xs)` computes normalized
  [autocorrelation](https://example.com)
  coefficients.
- `periodogram(xs)` computes spectral power.
"""
        self.assertEqual(
            unfold_soft_breaks(markdown),
            "Three new functions close the rendering gap:\n\n"
            "- `autocorrelation(xs)` computes normalized "
            "[autocorrelation](https://example.com) coefficients.\n"
            "- `periodogram(xs)` computes spectral power.\n",
        )

    def test_unfold_soft_breaks_preserves_markdown_blocks(self) -> None:
        markdown = (
            "### Example\n\n"
            "First line  \nsecond line\n\n"
            "| A | B |\n| - | - |\n\n"
            "```tql\nfrom {x: 1}\n\nwhere x == 1\n```\n"
        )
        self.assertEqual(unfold_soft_breaks(markdown), markdown)

    def test_campaign_identities_accept_kebab_case(self) -> None:
        self.write("tenzir/changelog/config.yaml", CONFIG)
        self.write("tenzir/changelog/unreleased/add-clickhouse.md", ENTRY)
        self.assertEqual(campaign_identity_errors([self.root / "tenzir"]), [])

    def test_campaign_identities_reject_invalid_config_id(self) -> None:
        config = self.write("tenzir/changelog/config.yaml", "id: Tenzir_Node\n")
        errors = campaign_identity_errors([self.root / "tenzir"])
        self.assertEqual(
            errors,
            [f"{config}: id must be lowercase kebab-case, got 'Tenzir_Node'"],
        )

    def test_campaign_identities_reject_missing_or_non_mapping_config(self) -> None:
        cases = {
            "missing": (None, "changelog config is missing"),
            "empty": ("", "changelog config must be a mapping"),
            "false": ("false\n", "changelog config must be a mapping"),
            "list": ("[]\n", "changelog config must be a mapping"),
        }
        for project_name, (contents, message) in cases.items():
            with self.subTest(project=project_name):
                project = self.root / project_name
                config = project / "changelog/config.yaml"
                if contents is not None:
                    self.write(f"{project_name}/changelog/config.yaml", contents)
                self.assertEqual(
                    campaign_identity_errors([project]),
                    [f"{config}: {message}"],
                )

    def test_campaign_identities_reject_invalid_entry_slug(self) -> None:
        self.write("tenzir/changelog/config.yaml", CONFIG)
        entry = self.write("tenzir/changelog/unreleased/add-to_clickhouse.md", ENTRY)
        errors = campaign_identity_errors([self.root / "tenzir"])
        self.assertEqual(
            errors,
            [f"{entry}: filename stem must be lowercase kebab-case"],
        )

    def test_campaign_identities_validate_project_fallback(self) -> None:
        self.write("Not_Kebab/changelog/config.yaml", "name: Example\n")
        config = self.root / "Not_Kebab/changelog/config.yaml"
        errors = campaign_identity_errors([self.root / "Not_Kebab"])
        self.assertEqual(
            errors,
            [f"{config}: id must be lowercase kebab-case, got 'Not_Kebab'"],
        )


if __name__ == "__main__":
    unittest.main()
