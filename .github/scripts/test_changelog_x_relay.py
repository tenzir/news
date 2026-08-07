"""Tests for stable release discovery in the X relay."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from changelog_x_relay import collect_manual, collect_push


class ChangelogXRelayTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.git("init", "--initial-branch=main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write("README.md", "base\n")
        self.git("add", ".")
        self.git("commit", "-m", "base")
        self.before = self.git("rev-parse", "HEAD").strip()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def release(
        self, project: str, version: str, entries: tuple[str, ...] = ()
    ) -> None:
        base = f"{project}/changelog/releases/{version}"
        self.write(f"{base}/manifest.yaml", "title: Test release\n")
        for slug in entries:
            self.write(
                f"{base}/entries/{slug}.md",
                f"---\ntitle: {slug}\ntype: feature\n---\n\nBody.\n",
            )

    def commit(self) -> str:
        self.git("add", ".")
        self.git("commit", "-m", "add releases")
        return self.git("rev-parse", "HEAD").strip()

    def test_push_fans_out_every_stable_release_and_skips_prereleases(self) -> None:
        self.release("tenzir", "v6.9.0", ("feature-b", "feature-a"))
        self.release("mcp", "v1.0.0")
        self.release("tenzir", "v7.0.0-rc.1", ("not-stable",))
        after = self.commit()

        payloads = collect_push(self.root, self.before, after)

        self.assertEqual(
            [(item["project"], item["version"]) for item in payloads],
            [("mcp", "v1.0.0"), ("tenzir", "v6.9.0")],
        )
        self.assertEqual(payloads[0]["entryPaths"], [])
        self.assertEqual(
            payloads[1]["entryPaths"],
            [
                "tenzir/changelog/releases/v6.9.0/entries/feature-a.md",
                "tenzir/changelog/releases/v6.9.0/entries/feature-b.md",
            ],
        )
        self.assertTrue(all(not item["force"] for item in payloads))

    def test_entry_enumeration_uses_the_pinned_after_tree(self) -> None:
        self.release("tenzir", "v6.9.0", ("committed",))
        after = self.commit()
        self.write(
            "tenzir/changelog/releases/v6.9.0/entries/uncommitted.md",
            "not at the pinned commit\n",
        )

        payload = collect_push(self.root, self.before, after)[0]

        self.assertEqual(
            payload["entryPaths"],
            ["tenzir/changelog/releases/v6.9.0/entries/committed.md"],
        )

    def test_initial_push_compares_against_the_empty_tree(self) -> None:
        self.release("tenzir", "v6.9.0", ("feature",))
        after = self.commit()

        payloads = collect_push(self.root, "0" * 40, after)

        self.assertEqual(
            [(item["project"], item["version"]) for item in payloads],
            [("tenzir", "v6.9.0")],
        )

    def test_manual_dispatch_forces_one_release_and_preserves_safety_flags(
        self,
    ) -> None:
        self.release("tenzir", "v6.9.0", ("feature",))
        after = self.commit()

        payload = collect_manual(
            self.root,
            after,
            "tenzir",
            "v6.9.0",
            dry_run=True,
            retry_ambiguous=True,
        )[0]

        self.assertTrue(payload["force"])
        self.assertTrue(payload["dryRun"])
        self.assertTrue(payload["retryAmbiguous"])

    def test_manual_dispatch_rejects_a_prerelease(self) -> None:
        self.release("tenzir", "v7.0.0-rc.1", ("feature",))
        after = self.commit()

        with self.assertRaisesRegex(ValueError, "stable vX.Y.Z"):
            collect_manual(
                self.root,
                after,
                "tenzir",
                "v7.0.0-rc.1",
                dry_run=False,
                retry_ambiguous=False,
            )

    def test_push_without_new_manifests_is_empty(self) -> None:
        self.write("tenzir/changelog/unreleased/feature.md", "entry\n")
        after = self.commit()
        self.assertEqual(collect_push(self.root, self.before, after), [])


if __name__ == "__main__":
    unittest.main()
