"""Tests for changelog notification and X publication helpers."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))

from changelog import load_entry  # noqa: E402
from changelog_x import (  # noqa: E402
    MAX_FEATURE_ENTRIES,
    added_entry_paths,
    build_payload,
    payload_hash,
    prepare_entries,
    project_for_entry,
    write_context,
    write_noop,
)
from x_publish import (  # noqa: E402
    _resume_ids,
    CheckLedger,
    ValidatedThread,
    load_safe_output_items,
    post_one,
    post_thread,
    posts_from_item,
    publish_live,
    render_staged_preview,
    validate_posts,
    validate_requests,
)


def sample_payload(*, body: str = "Feature body") -> dict:
    """Return normalized feature data for tests."""
    return {
        "project": "project",
        "repo": "tenzir/example",
        "slug": "feature",
        "type": "feature",
        "title": "A feature",
        "body": body,
        "authors": ["alice"],
        "prs": [42],
        "url": "https://github.com/tenzir/example/pull/42",
    }


class ChangelogTest(unittest.TestCase):
    def test_load_entry_uses_tenzir_ship(self) -> None:
        entry = Mock(
            title="A feature",
            type="feature",
            body="Feature body",
            metadata={"authors": ["alice"], "prs": [42]},
        )
        with patch("tenzir_ship.entries.read_entry", return_value=entry) as read:
            result = load_entry(Path("project/changelog/unreleased/feature.md"))

        read.assert_called_once_with(Path("project/changelog/unreleased/feature.md"))
        self.assertEqual(result["authors"], ["alice"])
        self.assertEqual(result["prs"], [42])

    def test_build_payload_uses_project_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entry = root / "project/changelog/unreleased/feature.md"
            entry.parent.mkdir(parents=True)
            entry.write_text("unused")
            (root / "project/changelog/config.yaml").write_text(
                "repository: tenzir/example\n"
            )
            data = {
                "title": "A feature",
                "type": "feature",
                "authors": ["alice"],
                "prs": [42],
                "body": "Feature body",
            }
            with patch("changelog_x.load_entry", return_value=data):
                previous = Path.cwd()
                try:
                    os.chdir(root)
                    payload = build_payload(
                        Path("project/changelog/unreleased/feature.md")
                    )
                finally:
                    os.chdir(previous)

        self.assertEqual(payload["project"], "project")
        self.assertEqual(payload["repo"], "tenzir/example")
        self.assertEqual(payload["slug"], "feature")
        self.assertEqual(payload["prs"], [42])
        self.assertEqual(payload["url"], "https://github.com/tenzir/example/pull/42")

    def test_accepts_only_direct_unreleased_entries(self) -> None:
        self.assertEqual(
            project_for_entry(Path("tenzir/changelog/unreleased/feature.md")),
            "tenzir",
        )
        invalid = [
            "tenzir/changelog/changes/feature.md",
            "tenzir/changelog/releases/v1.0.0/entries/feature.md",
            "tenzir/plugin/changelog/unreleased/feature.md",
            "tenzir/changelog/unreleased/nested/feature.md",
            "../changelog/unreleased/feature.md",
        ]
        for path in invalid:
            with self.subTest(path=path), self.assertRaises(ValueError):
                project_for_entry(Path(path))

    def test_added_entries_are_read_from_the_git_diff(self) -> None:
        result = Mock(stdout=b"tenzir/changelog/unreleased/feature.md\0")
        with patch("changelog_x.subprocess.run", return_value=result) as run:
            paths = added_entry_paths("1" * 40, "2" * 40)

        self.assertEqual(paths, [Path("tenzir/changelog/unreleased/feature.md")])
        self.assertIn("--diff-filter=A", run.call_args.args[0])

    def test_preparation_filters_non_features_and_records_code(self) -> None:
        paths = [
            Path("one/changelog/unreleased/feature.md"),
            Path("two/changelog/unreleased/fix.md"),
        ]
        feature = sample_payload(body="Example:\n\n```tql\nfrom x\n```")
        fix = {**sample_payload(), "project": "two", "type": "bugfix"}
        with (
            patch("changelog_x.selected_entry_paths", return_value=paths),
            patch("changelog_x.build_payload", side_effect=[feature, fix]),
        ):
            entries = prepare_entries("1" * 40, "2" * 40, "")

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["entry"], paths[0].as_posix())
        self.assertTrue(entries[0]["has_code_fence"])
        self.assertEqual(entries[0]["content_hash"], payload_hash(feature))

    def test_preparation_rejects_oversized_feature_batches(self) -> None:
        paths = [
            Path(f"project/changelog/unreleased/feature-{index}.md")
            for index in range(MAX_FEATURE_ENTRIES + 1)
        ]
        with (
            patch("changelog_x.selected_entry_paths", return_value=paths),
            patch("changelog_x.build_payload", return_value=sample_payload()),
            self.assertRaisesRegex(
                ValueError,
                rf"cannot draft more than {MAX_FEATURE_ENTRIES}",
            ),
        ):
            prepare_entries("1" * 40, "2" * 40, "")

    def test_context_and_noop_are_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = root / "agent/context.json"
            safe_outputs = root / "safe-outputs.jsonl"
            write_context([], context)
            with patch.dict(os.environ, {"GH_AW_SAFE_OUTPUTS": str(safe_outputs)}):
                write_noop("Nothing to draft")

            self.assertEqual(json.loads(context.read_text()), {"entries": []})
            self.assertEqual(
                json.loads(safe_outputs.read_text()),
                {"type": "noop", "message": "Nothing to draft"},
            )

    def test_preparation_step_exposes_safe_outputs_path(self) -> None:
        workflow = (Path(__file__).parents[1] / "workflows/changelog-x.md").read_text()

        self.assertIn(
            "GH_AW_SAFE_OUTPUTS: ${{ runner.temp }}/gh-aw/safeoutputs/outputs.jsonl",
            workflow,
        )

    def test_workflow_allows_every_bounded_publish_request(self) -> None:
        workflows = Path(__file__).parents[1] / "workflows"
        source = (workflows / "changelog-x.md").read_text()
        lock = (workflows / "changelog-x.lock.yml").read_text()

        self.assertIn(f"      max: {MAX_FEATURE_ENTRIES}\n", source)
        self.assertRegex(
            lock,
            rf'"publish-x-thread":\{{[^\n]*"max":{MAX_FEATURE_ENTRIES}',
        )

    def test_workflow_selects_gpt_5_6_sol_through_an_exact_alias(self) -> None:
        workflows = Path(__file__).parents[1] / "workflows"

        self.assertIn("model: gpt-5.6-sol", (workflows / "changelog-x.md").read_text())
        self.assertIn(
            "- copilot/gpt-5.6-sol",
            (workflows / "shared/gpt-5.6-sol.md").read_text(),
        )


class XPublicationTest(unittest.TestCase):
    def test_single_post_policy_for_plain_entries(self) -> None:
        payload = sample_payload()
        post = f"A concise feature announcement. {payload['url']}"

        lengths = validate_posts(payload, [post])

        self.assertEqual(len(lengths), 1)
        self.assertLessEqual(lengths[0], 280)
        with self.assertRaisesRegex(ValueError, "exactly one post"):
            validate_posts(payload, ["First", post])

    def test_code_entries_may_use_a_valid_thread(self) -> None:
        payload = sample_payload(body="Example:\n\n```tql\nfrom x\n```")
        posts = [
            "Fan out a TQL pipeline and merge each branch back into the stream.",
            f"See the complete example and implementation: {payload['url']}",
        ]

        self.assertEqual(len(validate_posts(payload, posts)), 2)

    def test_rejects_unsafe_or_misplaced_content(self) -> None:
        payload = sample_payload(body="```tql\nfrom x\n```")
        invalid = [
            [f"Hello @someone {payload['url']}"],
            [f"Hello — world {payload['url']}"],
            [f"Early URL {payload['url']}", f"Final {payload['url']}"],
            ["No source URL"],
            [f"Wrong https://example.com {payload['url']}"],
            ["界" * 141 + f" {payload['url']}"],
        ]
        for posts in invalid:
            with self.subTest(posts=posts), self.assertRaises(ValueError):
                validate_posts(payload, posts)

    def test_posts_must_be_contiguous(self) -> None:
        with self.assertRaisesRegex(ValueError, "contiguous"):
            posts_from_item(
                {
                    "post_1": "First",
                    "post_2": "",
                    "post_3": "Third",
                }
            )

    def test_requests_must_exactly_match_triggered_entries(self) -> None:
        entry = "project/changelog/unreleased/feature.md"
        payload = sample_payload()
        item = {
            "type": "publish_x_thread",
            "entry": entry,
            "post_1": f"A concise feature announcement. {payload['url']}",
        }

        threads = validate_requests([item], {entry: payload})

        self.assertEqual(threads[0].entry, Path(entry))
        with self.assertRaisesRegex(ValueError, "missing publish request"):
            validate_requests([], {entry: payload})
        with self.assertRaisesRegex(ValueError, "unexpected publish request"):
            validate_requests(
                [
                    item,
                    {**item, "entry": "other/changelog/unreleased/feature.md"},
                ],
                {entry: payload},
            )

    def test_multiple_requests_match_multiple_triggered_entries(self) -> None:
        first_entry = "project/changelog/unreleased/first.md"
        second_entry = "project/changelog/unreleased/second.md"
        first = sample_payload()
        second = {
            **sample_payload(),
            "slug": "second",
            "prs": [43],
            "url": "https://github.com/tenzir/example/pull/43",
        }
        items = [
            {
                "type": "publish_x_thread",
                "entry": first_entry,
                "post_1": f"First feature. {first['url']}",
            },
            {
                "type": "publish_x_thread",
                "entry": second_entry,
                "post_1": f"Second feature. {second['url']}",
            },
        ]

        threads = validate_requests(
            items,
            {first_entry: first, second_entry: second},
        )

        self.assertEqual(
            [thread.entry for thread in threads],
            [Path(first_entry), Path(second_entry)],
        )

    def test_loads_only_the_custom_safe_output_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "agent.json"
            output.write_text(
                json.dumps(
                    {
                        "items": [
                            {"type": "noop", "message": "unused"},
                            {
                                "type": "publish_x_thread",
                                "entry": "project/changelog/unreleased/feature.md",
                                "post_1": "Hello",
                            },
                        ]
                    }
                )
            )

            items = load_safe_output_items(output)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["type"], "publish_x_thread")

    def test_staged_preview_contains_every_post(self) -> None:
        payload = sample_payload(body="```tql\nfrom x\n```")
        posts = ["First post", f"Final post {payload['url']}"]
        thread = ValidatedThread(
            entry=Path("project/changelog/unreleased/feature.md"),
            payload=payload,
            digest=payload_hash(payload),
            posts=posts,
            weighted_lengths=validate_posts(payload, posts),
        )
        with tempfile.TemporaryDirectory() as directory:
            summary = Path(directory) / "summary.md"

            render_staged_preview([thread], summary)

            result = summary.read_text()
        self.assertIn("Staged Mode: X Thread Preview", result)
        self.assertIn(posts[0], result)
        self.assertIn(posts[1], result)
        self.assertIn("No GitHub or X resources were created", result)

    def test_post_one_builds_an_x_reply(self) -> None:
        response = Mock(ok=True)
        response.json.return_value = {"data": {"id": "456"}}
        session = Mock()
        session.post.return_value = response

        result = post_one(session, "Second post", "123")

        self.assertEqual(result, "456")
        session.post.assert_called_once_with(
            "https://api.x.com/2/tweets",
            json={
                "text": "Second post",
                "reply": {"in_reply_to_tweet_id": "123"},
            },
            timeout=30,
        )

    def test_post_one_retries_transient_failures(self) -> None:
        transient = Mock(ok=False, status_code=503, headers={})
        success = Mock(ok=True)
        success.json.return_value = {"data": {"id": "123"}}
        session = Mock()
        session.post.side_effect = [transient, success]
        sleep = Mock()

        result = post_one(session, "First post", None, sleep=sleep)

        self.assertEqual(result, "123")
        sleep.assert_called_once_with(1.0)

    def test_post_thread_resumes_after_recorded_posts(self) -> None:
        session = Mock()
        recorded: list[list[str]] = []
        with patch("x_publish.post_one", return_value="second") as post:
            result = post_thread(
                session,
                ["First", "Second"],
                ["first"],
                lambda ids: recorded.append(list(ids)),
            )

        self.assertEqual(result, ["first", "second"])
        post.assert_called_once_with(session, "Second", "first")
        self.assertEqual(recorded, [["first", "second"]])

    def test_check_state_resumes_failed_threads(self) -> None:
        previous = {
            "status": "completed",
            "conclusion": "failure",
            "output": {"text": '{"tweet_ids":["first"]}'},
        }

        self.assertEqual(_resume_ids(previous), ["first"])

    def test_check_state_blocks_concurrent_publication(self) -> None:
        previous = {
            "status": "in_progress",
            "started_at": datetime.now(UTC).isoformat(),
            "output": {"text": '{"tweet_ids":[]}'},
        }

        with self.assertRaisesRegex(RuntimeError, "already in progress"):
            _resume_ids(previous)

    def test_live_failure_records_partial_thread_progress(self) -> None:
        payload = sample_payload(body="```tql\nfrom x\n```")
        thread = ValidatedThread(
            entry=Path("project/changelog/unreleased/feature.md"),
            payload=payload,
            digest=payload_hash(payload),
            posts=["First", f"Final {payload['url']}"],
            weighted_lengths=[5, 52],
        )
        ledger = Mock(spec=CheckLedger)
        ledger.previous.return_value = None
        ledger.create.return_value = 99

        def fail_after_first_post(_session, _posts, _ids, on_post):
            on_post(["first"])
            raise RuntimeError("second post failed")

        environment = {
            "GITHUB_REPOSITORY": "tenzir/news",
            "GITHUB_TOKEN": "token",
        }
        with (
            patch.dict(os.environ, environment, clear=True),
            patch("x_publish.CheckLedger", return_value=ledger),
            patch("x_publish.x_session_from_environment", return_value=Mock()),
            patch("x_publish.entry_commit", return_value="1" * 40),
            patch("x_publish.post_thread", side_effect=fail_after_first_post),
            self.assertRaisesRegex(RuntimeError, "second post failed"),
        ):
            publish_live([thread])

        failure = ledger.update.call_args_list[-1]
        self.assertEqual(failure.args[2], ["first"])
        self.assertEqual(failure.kwargs["conclusion"], "failure")


if __name__ == "__main__":
    unittest.main()
