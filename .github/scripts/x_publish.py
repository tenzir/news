#!/usr/bin/env python3
"""Validate and publish X threads requested by the drafting agent."""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Callable, TypedDict

import requests
from requests_oauthlib import OAuth1

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)
from twitter_text import extract_urls_with_indices, parse_tweet  # noqa: E402

from changelog_x import (  # noqa: E402
    ThreadPayload,
    build_payload,
    payload_hash,
    selected_entry_paths,
)


X_POST_URL = "https://api.x.com/2/tweets"
TRANSIENT_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}
MENTION_PATTERN = re.compile(r"(?<![\w@])@[A-Za-z0-9_]+")


class SafeOutputItem(TypedDict, total=False):
    """The typed request emitted by the agent."""

    type: str
    entry: str
    post_1: str
    post_2: str
    post_3: str
    post_4: str
    post_5: str


@dataclass(frozen=True)
class ValidatedThread:
    """A safe-output request bound to a reparsed changelog entry."""

    entry: Path
    payload: ThreadPayload
    digest: str
    posts: list[str]
    weighted_lengths: list[int]


def posts_from_item(item: SafeOutputItem) -> list[str]:
    """Extract one contiguous list of one to five posts."""
    posts: list[str] = []
    found_gap = False
    for number in range(1, 6):
        value = item.get(f"post_{number}", "")
        if not isinstance(value, str):
            raise ValueError(f"post_{number} must be a string")
        if not value:
            found_gap = True
            continue
        if value != value.strip():
            raise ValueError(f"post_{number} has leading or trailing whitespace")
        if found_gap:
            raise ValueError("thread posts must be contiguous")
        posts.append(value)
    if not posts:
        raise ValueError("an X thread must contain at least one post")
    return posts


def validate_posts(payload: ThreadPayload, posts: list[str]) -> list[int]:
    """Enforce the deterministic publication policy for an X thread."""
    if len(posts) > 5:
        raise ValueError("an X thread cannot contain more than five posts")
    has_code_fence = bool(re.search(r"(?:^|\n)```", payload["body"]))
    if not has_code_fence and len(posts) != 1:
        raise ValueError("entries without fenced code must use exactly one post")

    weighted_lengths: list[int] = []
    for index, post in enumerate(posts):
        label = f"post_{index + 1}"
        if "—" in post:
            raise ValueError(f"{label} contains an em dash")
        if MENTION_PATTERN.search(post):
            raise ValueError(f"{label} contains an @mention")
        parsed = parse_tweet(post)
        if not parsed.valid:
            raise ValueError(
                f"{label} exceeds X's weighted character limit "
                f"({parsed.weightedLength}/280)"
            )
        weighted_lengths.append(parsed.weightedLength)

        urls = extract_urls_with_indices(post)
        if index < len(posts) - 1 and urls:
            raise ValueError("only the final post may contain a URL")
        if index == len(posts) - 1:
            if len(urls) != 1 or urls[0]["url"] != payload["url"]:
                raise ValueError("the final post must contain only the changelog URL")
            if post.count(payload["url"]) != 1:
                raise ValueError("the final post must contain the changelog URL once")
    return weighted_lengths


def expected_payloads(before: str, after: str, entry: str) -> dict[str, ThreadPayload]:
    """Recompute the exact set of feature entries authorized by the trigger."""
    expected: dict[str, ThreadPayload] = {}
    for path in selected_entry_paths(before, after, entry):
        payload = build_payload(path)
        if payload["type"] == "feature":
            expected[path.as_posix()] = payload
    return expected


def load_safe_output_items(output_file: Path) -> list[SafeOutputItem]:
    """Load publish requests from the gh-aw agent output artifact."""
    try:
        document = json.loads(output_file.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read GH_AW_AGENT_OUTPUT") from error
    items = document.get("items") if isinstance(document, dict) else None
    if not isinstance(items, list):
        raise ValueError("GH_AW_AGENT_OUTPUT does not contain an items list")
    return [
        item
        for item in items
        if isinstance(item, dict) and item.get("type") == "publish_x_thread"
    ]


def validate_requests(
    items: list[SafeOutputItem], expected: dict[str, ThreadPayload]
) -> list[ValidatedThread]:
    """Bind agent requests to the event and validate every proposed post."""
    if not expected:
        raise ValueError("the triggering event contains no feature entries")
    by_entry: dict[str, SafeOutputItem] = {}
    for item in items:
        entry = item.get("entry")
        if not isinstance(entry, str):
            raise ValueError("every publish request must specify an entry")
        if entry in by_entry:
            raise ValueError(f"duplicate publish request for {entry}")
        by_entry[entry] = item
    missing = sorted(set(expected) - set(by_entry))
    unexpected = sorted(set(by_entry) - set(expected))
    if missing:
        raise ValueError(f"missing publish request for: {', '.join(missing)}")
    if unexpected:
        raise ValueError(f"unexpected publish request for: {', '.join(unexpected)}")

    validated: list[ValidatedThread] = []
    for entry, payload in expected.items():
        posts = posts_from_item(by_entry[entry])
        weighted_lengths = validate_posts(payload, posts)
        validated.append(
            ValidatedThread(
                entry=Path(entry),
                payload=payload,
                digest=payload_hash(payload),
                posts=posts,
                weighted_lengths=weighted_lengths,
            )
        )
    return validated


def render_staged_preview(threads: list[ValidatedThread], summary_path: Path) -> None:
    """Render a complete preview without making any API write calls."""
    lines = [
        "## 🧪 Staged Mode: X Thread Preview",
        "",
        f"The following {len(threads)} X thread operation(s) would be performed "
        "if staged mode was disabled:",
        "",
    ]
    for thread in threads:
        lines.extend(
            [
                f"### `{thread.entry.as_posix()}`",
                "",
                f"Content hash: `{thread.digest}`",
                "",
            ]
        )
        for number, (post, length) in enumerate(
            zip(thread.posts, thread.weighted_lengths, strict=True), start=1
        ):
            lines.extend(
                [
                    f"#### Post {number} ({length}/280 weighted characters)",
                    "",
                    post,
                    "",
                ]
            )
    lines.extend(
        [
            "---",
            "**Preview Summary**: "
            f"{len(threads)} operations previewed. No GitHub or X resources were created.",
            "",
        ]
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("a") as stream:
        stream.write("\n".join(lines))


def entry_commit(entry: Path) -> str:
    """Return the commit that introduced an entry for stable check-run storage."""
    result = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%H", "-1", "--", entry.as_posix()],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or os.environ["GITHUB_SHA"]


class CheckLedger:
    """Persist publication progress in a check run on the entry's first commit."""

    def __init__(self, repository: str, token: str) -> None:
        self.base_url = f"https://api.github.com/repos/{repository}"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    def _request(self, method: str, path: str, **kwargs: object) -> dict:
        response = self.session.request(
            method, f"{self.base_url}{path}", timeout=30, **kwargs
        )
        if not response.ok:
            raise RuntimeError(
                f"GitHub Checks API returned HTTP {response.status_code}"
            )
        try:
            result = response.json()
        except requests.JSONDecodeError as error:
            raise RuntimeError("GitHub Checks API returned invalid JSON") from error
        if not isinstance(result, dict):
            raise RuntimeError("GitHub Checks API returned an invalid response")
        return result

    def previous(self, commit: str, name: str) -> dict | None:
        result = self._request(
            "GET",
            f"/commits/{commit}/check-runs",
            params={"check_name": name, "filter": "latest", "per_page": 1},
        )
        runs = result.get("check_runs", [])
        return runs[0] if isinstance(runs, list) and runs else None

    def create(self, commit: str, name: str, entry: Path, tweet_ids: list[str]) -> int:
        result = self._request(
            "POST",
            "/check-runs",
            json={
                "name": name,
                "head_sha": commit,
                "status": "in_progress",
                "started_at": datetime.now(UTC).isoformat(),
                "output": self._output(entry, tweet_ids, "Publishing X thread"),
            },
        )
        return int(result["id"])

    def update(
        self,
        check_id: int,
        entry: Path,
        tweet_ids: list[str],
        status: str,
        *,
        conclusion: str | None = None,
        message: str,
    ) -> None:
        body: dict[str, object] = {
            "status": status,
            "output": self._output(entry, tweet_ids, message),
        }
        if status == "completed":
            body["conclusion"] = conclusion
            body["completed_at"] = datetime.now(UTC).isoformat()
        self._request("PATCH", f"/check-runs/{check_id}", json=body)

    @staticmethod
    def _output(entry: Path, tweet_ids: list[str], message: str) -> dict[str, str]:
        state = json.dumps({"tweet_ids": tweet_ids}, separators=(",", ":"))
        return {
            "title": f"X publication for {entry.name}",
            "summary": message[:65535],
            "text": state,
        }


def _resume_ids(previous: dict | None) -> list[str]:
    if not previous:
        return []
    if previous.get("status") != "completed":
        created = previous.get("started_at") or previous.get("created_at")
        if isinstance(created, str):
            try:
                started = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except ValueError:
                started = datetime.now(UTC)
            if started > datetime.now(UTC) - timedelta(hours=1):
                raise RuntimeError("an X publication check is already in progress")
    output = previous.get("output")
    text = output.get("text") if isinstance(output, dict) else None
    if not isinstance(text, str):
        return []
    try:
        state = json.loads(text)
    except json.JSONDecodeError:
        return []
    tweet_ids = state.get("tweet_ids") if isinstance(state, dict) else None
    if not isinstance(tweet_ids, list) or not all(
        isinstance(item, str) for item in tweet_ids
    ):
        return []
    return tweet_ids


def _retry_delay(response: requests.Response | None, attempt: int) -> float:
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
    return float(2**attempt)


def post_one(
    session: requests.Session,
    text: str,
    reply_to: str | None,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Post one X status with bounded retries for transient failures."""
    body: dict[str, object] = {"text": text}
    if reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_to}
    last_error = "X API request failed"
    for attempt in range(4):
        response: requests.Response | None = None
        try:
            response = session.post(X_POST_URL, json=body, timeout=30)
        except requests.RequestException as error:
            last_error = "failed to reach the X API"
            if attempt == 3:
                raise RuntimeError(last_error) from error
        else:
            if response.ok:
                try:
                    result = response.json()
                    tweet_id = result["data"]["id"]
                except (KeyError, TypeError, requests.JSONDecodeError) as error:
                    raise RuntimeError("X API returned an invalid response") from error
                if not isinstance(tweet_id, str):
                    raise RuntimeError("X API returned an invalid post ID")
                return tweet_id
            last_error = f"X API returned HTTP {response.status_code}"
            if response.status_code not in TRANSIENT_STATUS_CODES or attempt == 3:
                raise RuntimeError(last_error)
        sleep(_retry_delay(response, attempt))
    raise RuntimeError(last_error)


def post_thread(
    session: requests.Session,
    posts: list[str],
    tweet_ids: list[str],
    on_post: Callable[[list[str]], None],
) -> list[str]:
    """Post or resume a reply chain, recording each successful post."""
    if len(tweet_ids) > len(posts):
        raise RuntimeError("stored X publication state is inconsistent")
    published = list(tweet_ids)
    for post in posts[len(published) :]:
        published.append(post_one(session, post, published[-1] if published else None))
        on_post(published)
    return published


def x_session_from_environment() -> requests.Session:
    """Create an OAuth 1.0a session from environment-scoped secrets."""
    names = [
        "X_API_KEY",
        "X_API_SECRET",
        "X_ACCESS_TOKEN",
        "X_ACCESS_TOKEN_SECRET",
    ]
    values = {name: os.environ.get(name, "").strip() for name in names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(f"missing X credentials: {', '.join(missing)}")
    session = requests.Session()
    session.auth = OAuth1(
        values["X_API_KEY"],
        values["X_API_SECRET"],
        values["X_ACCESS_TOKEN"],
        values["X_ACCESS_TOKEN_SECRET"],
    )
    return session


def publish_live(threads: list[ValidatedThread]) -> None:
    """Publish validated threads with check-run deduplication and progress."""
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not repository or not token:
        raise RuntimeError("GitHub check-run credentials are not configured")
    ledger = CheckLedger(repository, token)
    x_session = x_session_from_environment()

    for thread in threads:
        commit = entry_commit(thread.entry)
        name = f"changelog-x/{thread.digest}"
        previous = ledger.previous(commit, name)
        if previous and previous.get("conclusion") == "success":
            print(f"Skipping already published entry: {thread.entry}")
            continue
        tweet_ids = _resume_ids(previous)
        check_id = ledger.create(commit, name, thread.entry, tweet_ids)
        progress_ids = list(tweet_ids)

        def record_progress(ids: list[str]) -> None:
            progress_ids[:] = ids
            ledger.update(
                check_id,
                thread.entry,
                ids,
                "in_progress",
                message=f"Published {len(ids)} of {len(thread.posts)} posts",
            )

        try:
            tweet_ids = post_thread(
                x_session,
                thread.posts,
                tweet_ids,
                record_progress,
            )
        except Exception as error:
            ledger.update(
                check_id,
                thread.entry,
                progress_ids,
                "completed",
                conclusion="failure",
                message=str(error),
            )
            raise
        ledger.update(
            check_id,
            thread.entry,
            tweet_ids,
            "completed",
            conclusion="success",
            message=f"Published {len(tweet_ids)} posts to X",
        )


def main() -> None:
    """Process gh-aw custom safe-output requests."""
    output_file = os.environ.get("GH_AW_AGENT_OUTPUT", "").strip()
    if not output_file:
        raise RuntimeError("GH_AW_AGENT_OUTPUT is not configured")
    expected = expected_payloads(
        os.environ.get("BEFORE", ""),
        os.environ.get("AFTER", ""),
        os.environ.get("ENTRY", ""),
    )
    threads = validate_requests(load_safe_output_items(Path(output_file)), expected)
    if os.environ.get("GH_AW_SAFE_OUTPUTS_STAGED") == "true":
        summary = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()
        if not summary:
            raise RuntimeError("GITHUB_STEP_SUMMARY is not configured")
        render_staged_preview(threads, Path(summary))
        print(f"Previewed {len(threads)} validated X thread(s)")
        return
    publish_live(threads)


if __name__ == "__main__":
    main()
