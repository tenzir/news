#!/usr/bin/env python3
"""Prepare changelog feature entries for the X drafting agent."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import TypedDict

from changelog import get_config_for_entry, get_repository, load_entry


PROJECT_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
COMMIT_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
ZERO_COMMIT = "0" * 40


class ThreadPayload(TypedDict):
    """Normalized changelog data given to the drafting agent."""

    project: str
    repo: str
    slug: str
    type: str
    title: str
    body: str
    authors: list[str]
    prs: list[int]
    url: str


class PreparedEntry(TypedDict):
    """One validated feature entry in the agent context file."""

    entry: str
    content_hash: str
    has_code_fence: bool
    changelog: ThreadPayload


def project_for_entry(file_path: Path) -> str:
    """Validate a direct unreleased entry path and return its project."""
    if file_path.is_absolute():
        raise ValueError("entry path must be relative to the repository root")
    parts = file_path.parts
    if (
        len(parts) != 4
        or parts[1:3] != ("changelog", "unreleased")
        or file_path.suffix != ".md"
        or not PROJECT_PATTERN.fullmatch(parts[0])
    ):
        raise ValueError("entry path must match PROJECT/changelog/unreleased/SLUG.md")
    return parts[0]


def build_payload(file_path: Path) -> ThreadPayload:
    """Parse one direct unreleased entry through tenzir-ship."""
    project = project_for_entry(file_path)
    entry = load_entry(file_path)
    repo = get_repository(project, get_config_for_entry(file_path))
    url = (
        f"https://github.com/{repo}/pull/{entry['prs'][0]}"
        if entry["prs"]
        else f"https://github.com/{repo}"
    )
    return {
        "project": project,
        "repo": repo,
        "slug": file_path.stem,
        "type": entry["type"],
        "title": entry["title"],
        "body": entry["body"],
        "authors": entry["authors"],
        "prs": entry["prs"],
        "url": url,
    }


def payload_hash(payload: ThreadPayload) -> str:
    """Return a stable digest for a normalized changelog entry."""
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _validate_commit(commit: str, name: str) -> None:
    if not COMMIT_PATTERN.fullmatch(commit):
        raise ValueError(f"{name} must be a full Git commit SHA")


def empty_tree() -> str:
    """Return Git's empty tree object ID."""
    result = subprocess.run(
        ["git", "hash-object", "-t", "tree", "/dev/null"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def added_entry_paths(before: str, after: str) -> list[Path]:
    """Return direct unreleased entries added between two commits."""
    _validate_commit(before, "before")
    _validate_commit(after, "after")
    if before == ZERO_COMMIT:
        before = empty_tree()
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=A",
            "-z",
            before,
            after,
            "--",
            "*/changelog/unreleased/*.md",
        ],
        check=True,
        capture_output=True,
    )
    paths = [Path(os.fsdecode(item)) for item in result.stdout.split(b"\0") if item]
    # Git pathspecs can match more broadly than our supported layout. Keep the
    # boundary explicit and fail closed if that ever happens.
    for path in paths:
        project_for_entry(path)
    return paths


def selected_entry_paths(before: str, after: str, entry: str) -> list[Path]:
    """Select either one manual entry or entries added by the triggering push."""
    if entry.strip():
        path = Path(entry.strip())
        project_for_entry(path)
        return [path]
    if not before or not after:
        raise ValueError("manual runs must specify an entry")
    return added_entry_paths(before, after)


def prepare_entries(before: str, after: str, entry: str) -> list[PreparedEntry]:
    """Build the feature-only agent context for a push or manual run."""
    prepared: list[PreparedEntry] = []
    seen: set[Path] = set()
    for path in selected_entry_paths(before, after, entry):
        if path in seen:
            continue
        seen.add(path)
        payload = build_payload(path)
        if payload["type"] != "feature":
            continue
        prepared.append(
            {
                "entry": path.as_posix(),
                "content_hash": payload_hash(payload),
                "has_code_fence": bool(re.search(r"(?:^|\n)```", payload["body"])),
                "changelog": payload,
            }
        )
    return prepared


def write_context(entries: list[PreparedEntry], output: Path) -> None:
    """Write the deterministic context consumed by the drafting agent."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"entries": entries}, ensure_ascii=False, indent=2) + "\n"
    )


def write_noop(message: str) -> None:
    """Skip inference when preprocessing found nothing to draft."""
    safe_outputs = os.environ.get("GH_AW_SAFE_OUTPUTS", "").strip()
    if not safe_outputs:
        return
    with Path(safe_outputs).open("a") as stream:
        stream.write(json.dumps({"type": "noop", "message": message}) + "\n")


def main() -> None:
    """Prepare the agent context file from GitHub event inputs."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="")
    parser.add_argument("--entry", default="")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        entries = prepare_entries(args.before, args.after, args.entry)
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        parser.error(str(error))
    write_context(entries, args.output)
    if not entries:
        write_noop("No newly added changelog feature entries to draft for X")
    print(
        f"Prepared {len(entries)} changelog feature entr{'y' if len(entries) == 1 else 'ies'}"
    )


if __name__ == "__main__":
    main()
