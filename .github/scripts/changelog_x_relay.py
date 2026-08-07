"""Discover stable changelog releases for the X drafting relay."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import TypedDict

FULL_SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
STABLE_VERSION = re.compile(r"^v\d+\.\d+\.\d+$")
MANIFEST_PATH = re.compile(
    r"^(?P<project>[a-z0-9]+(?:-[a-z0-9]+)*)/changelog/releases/"
    r"(?P<version>v\d+\.\d+\.\d+(?:-[^/]+)?)/manifest\.yaml$"
)


class ReleasePayload(TypedDict):
    """One request accepted by the workflows Worker."""

    after: str
    project: str
    version: str
    entryPaths: list[str]
    retryAmbiguous: bool
    force: bool
    dryRun: bool


def collect_push(repo: Path, before: str, after: str) -> list[ReleasePayload]:
    """Return every stable release whose manifest was added by one push."""
    validate_sha(after)
    if not before or before == "0" * 40:
        before = git(repo, "hash-object", "-t", "tree", "/dev/null").strip()
    releases: set[tuple[str, str]] = set()
    for path in git(
        repo, "diff", "--name-only", "--diff-filter=A", before, after
    ).splitlines():
        match = MANIFEST_PATH.fullmatch(path)
        if match and STABLE_VERSION.fullmatch(match["version"]):
            releases.add((match["project"], match["version"]))
    return [
        release_payload(repo, after, project, version)
        for project, version in sorted(releases)
    ]


def collect_manual(
    repo: Path,
    after: str,
    project: str,
    version: str,
    *,
    dry_run: bool,
    retry_ambiguous: bool,
) -> list[ReleasePayload]:
    """Build one forced request for a manually selected stable release."""
    validate_sha(after)
    validate_release(project, version)
    manifest = f"{project}/changelog/releases/{version}/manifest.yaml"
    git(repo, "cat-file", "-e", f"{after}:{manifest}")
    return [
        release_payload(
            repo,
            after,
            project,
            version,
            force=True,
            dry_run=dry_run,
            retry_ambiguous=retry_ambiguous,
        )
    ]


def release_payload(
    repo: Path,
    after: str,
    project: str,
    version: str,
    *,
    force: bool = False,
    dry_run: bool = False,
    retry_ambiguous: bool = False,
) -> ReleasePayload:
    """Enumerate one release's Markdown entries at the pinned commit."""
    validate_release(project, version)
    prefix = f"{project}/changelog/releases/{version}/entries/"
    paths = []
    for path in git(
        repo, "ls-tree", "-r", "--name-only", after, "--", prefix
    ).splitlines():
        if not path.endswith(".md"):
            continue
        slug = path.removeprefix(prefix).removesuffix(".md")
        if not KEBAB_CASE.fullmatch(slug) or "/" in slug:
            raise ValueError(f"invalid release entry path: {path}")
        paths.append(path)
    return {
        "after": after.lower(),
        "project": project,
        "version": version,
        "entryPaths": sorted(paths),
        "retryAmbiguous": retry_ambiguous,
        "force": force,
        "dryRun": dry_run,
    }


def validate_sha(value: str) -> None:
    """Require the immutable commit identity accepted by the Worker."""
    if not FULL_SHA.fullmatch(value):
        raise ValueError(f"after must be a full Git commit SHA, got {value!r}")


def validate_release(project: str, version: str) -> None:
    """Require a top-level project and a stable release version."""
    if not KEBAB_CASE.fullmatch(project):
        raise ValueError(f"project must be lowercase kebab-case, got {project!r}")
    if not STABLE_VERSION.fullmatch(version):
        raise ValueError(f"version must be a stable vX.Y.Z release, got {version!r}")


def git(repo: Path, *args: str) -> str:
    """Run one read-only Git command in the news checkout."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_bool(value: str) -> bool:
    """Parse the lowercase booleans supplied by GitHub Actions."""
    if value == "true":
        return True
    if value == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse push or manual collection inputs."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    commands = parser.add_subparsers(dest="command", required=True)
    push = commands.add_parser("push")
    push.add_argument("--before", default="")
    push.add_argument("--after", required=True)
    manual = commands.add_parser("manual")
    manual.add_argument("--after", required=True)
    manual.add_argument("--project", required=True)
    manual.add_argument("--version", required=True)
    manual.add_argument("--dry-run", type=parse_bool, default=False)
    manual.add_argument("--retry-ambiguous", type=parse_bool, default=False)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Print one compact JSON request per discovered release."""
    args = parse_args(argv)
    if args.command == "push":
        payloads = collect_push(args.repo, args.before, args.after)
    else:
        payloads = collect_manual(
            args.repo,
            args.after,
            args.project,
            args.version,
            dry_run=args.dry_run,
            retry_ambiguous=args.retry_ambiguous,
        )
    for payload in payloads:
        print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
