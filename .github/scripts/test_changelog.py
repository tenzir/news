"""Tests for the shared changelog helpers used by Discord notifications."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from changelog import (
    build_release_message,
    campaign_identity_errors,
    get_changelog_entry_url,
    get_changelog_release_url,
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


def message_texts(message: dict) -> list[dict]:
    """Collect the text displays of a Components V2 message in order."""
    texts = []
    for child in message["components"][0]["components"]:
        if child["type"] == 10:
            texts.append(child)
        elif child["type"] == 9:
            texts += [c for c in child["components"] if c["type"] == 10]
    return texts


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

    def test_changelog_release_url_uses_config_id(self) -> None:
        self.assertEqual(
            get_changelog_release_url(
                "helm-charts", "v1.2.0", {"id": "tenzir-helm-charts"}
            ),
            "https://tenzir.com/changelog/tenzir-helm-charts/v1.2.0/",
        )
        self.assertEqual(
            get_changelog_release_url("mcp", "v0.3.0", {}),
            "https://tenzir.com/changelog/mcp/v0.3.0/",
        )

    def test_release_message_groups_titles_by_type(self) -> None:
        release = {
            "version": "v1.0.0",
            "title": "A big release",
            "intro": "This release\nadds things.",
            "entries": [
                {"type": "bugfix", "title": "Fixed a crash", "body": "Long body."},
                {"type": "feature", "title": "New operator", "body": "Long body."},
                {"type": "breaking", "title": "Removed X", "body": "Long body."},
                {"type": "feature", "title": "New function", "body": "Long body."},
            ],
        }
        url = "https://example.com/"
        message = build_release_message(
            release,
            name="Tenzir",
            url=url,
            product_url="https://example.com/product/",
            color=0x2ECC71,
        )
        self.assertEqual(message["flags"], 1 << 15)
        self.assertNotIn("content", message)
        self.assertNotIn("embeds", message)
        (container,) = message["components"]
        self.assertEqual(container["type"], 17)
        self.assertEqual(container["accent_color"], 0x2ECC71)
        children = container["components"]
        header = children[0]
        self.assertEqual(header["type"], 9)
        self.assertEqual(
            header["accessory"],
            {
                "type": 2,
                "style": 5,
                "label": "Tenzir",
                "url": "https://example.com/product/",
            },
        )
        self.assertEqual(
            [c["content"] for c in message_texts(message)],
            [
                "# A big release",
                "This release adds things.",
                "### 💥 Breaking changes\n- Removed X\n"
                "### 🚀 Features\n- New operator\n- New function\n"
                "### 🐞 Bug fixes\n- Fixed a crash",
            ],
        )
        row = children[-1]
        self.assertEqual(row["type"], 1)
        self.assertEqual(
            row["components"],
            [
                {
                    "type": 2,
                    "style": 5,
                    "label": "View v1.0.0 release notes",
                    "url": url,
                }
            ],
        )

    def test_release_message_truncates_with_a_count(self) -> None:
        release = {
            "version": "v1.0.0",
            "entries": [
                {"type": "feature", "title": f"Feature number {i}"} for i in range(50)
            ],
        }
        url = "https://example.com/"
        message = build_release_message(
            release,
            name="Tenzir",
            url=url,
            product_url="https://example.com/product/",
            color=0,
            max_length=300,
        )
        texts = [c["content"] for c in message_texts(message)]
        self.assertLessEqual(sum(len(t) for t in texts), 300)
        shown = texts[-1].count("\n- ")
        self.assertGreater(shown, 0)
        self.assertTrue(
            texts[-1].endswith(
                f"-# …and {50 - shown} more in the [release notes]({url})."
            )
        )
        # The button stays even when titles are dropped.
        self.assertEqual(message["components"][0]["components"][-1]["type"], 1)

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
