"""Shared helpers for loading and validating changelog projects and entries."""

import argparse
import re
import sys
from pathlib import Path
from typing import TypedDict

import yaml

KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
BLOCK_START = re.compile(
    r"^ {0,3}(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|>\s?|`{3,}|~{3,}|"
    r"(?:-{3,}|\*{3,}|_{3,})\s*$)"
)
BLOCK_END = re.compile(r"^ {0,3}(?:#{1,6}\s|(?:-{3,}|\*{3,}|_{3,})\s*$)")


class EntryData(TypedDict):
    """Normalized changelog entry fields used by notifications."""

    title: str
    type: str
    authors: list[str]
    prs: list[int]
    body: str


def get_config_for_entry(entry_path: Path) -> dict:
    """Load the nearest changelog configuration for an entry."""
    current = entry_path.parent
    while current != current.parent:
        config_path = current / "config.yaml"
        if config_path.exists():
            return yaml.safe_load(config_path.read_text()) or {}
        current = current.parent
    return {}


def get_config(project: str) -> dict:
    """Load the top-level changelog configuration for a project."""
    config_path = Path(project) / "changelog" / "config.yaml"
    if config_path.exists():
        return yaml.safe_load(config_path.read_text()) or {}
    return {}


def get_repository(project: str, config: dict | None = None) -> str:
    """Return the configured repository or the conventional fallback."""
    if config is None:
        config = get_config(project)
    return config.get("repository", f"tenzir/{project}")


def load_entry(file_path: Path) -> EntryData:
    """Load and normalize a changelog entry through tenzir-ship."""
    from tenzir_ship.entries import read_entry

    entry = read_entry(file_path)
    return {
        "title": entry.title,
        "type": entry.type,
        "authors": list(entry.metadata.get("authors", [])),
        "prs": list(entry.metadata.get("prs", [])),
        "body": entry.body,
    }


def unfold_soft_breaks(text: str) -> str:
    """Replace Markdown soft line breaks with spaces for Discord embeds.

    Discord can drop a soft break next to an inline Markdown element instead of
    rendering it as a space. Preserve block boundaries, hard breaks, tables,
    and fenced or indented code while joining wrapped prose and list items.
    """
    lines = text.splitlines()
    if not lines:
        return text
    trailing_newline = text.endswith("\n")
    unfolded: list[str] = []
    current = lines[0]
    fence_marker: str | None = None
    for next_line in lines[1:]:
        fence = FENCE.match(current)
        was_in_fence = fence_marker is not None
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                fence_marker = None
        preserve = (
            was_in_fence
            or fence is not None
            or not current.strip()
            or not next_line.strip()
            or current.endswith(("  ", "\\"))
            or BLOCK_END.match(current) is not None
            or BLOCK_START.match(next_line) is not None
            or current.startswith("    ")
            or next_line.startswith("    ")
            or current.lstrip().startswith("|")
            or next_line.lstrip().startswith("|")
        )
        if preserve:
            unfolded.append(current)
            current = next_line
        else:
            current = f"{current.rstrip()} {next_line.lstrip()}"
    unfolded.append(current)
    result = "\n".join(unfolded)
    return result + "\n" if trailing_newline else result


def campaign_identity_errors(projects: list[Path]) -> list[str]:
    """Return campaign identity errors for top-level changelog entries."""
    errors: list[str] = []
    for project in projects:
        changelog = project / "changelog"
        config_path = changelog / "config.yaml"
        if not config_path.exists():
            errors.append(f"{config_path}: changelog config is missing")
        else:
            try:
                config = yaml.safe_load(config_path.read_text())
            except yaml.YAMLError as error:
                errors.append(f"{config_path}: invalid YAML: {error}")
            else:
                if not isinstance(config, dict):
                    errors.append(f"{config_path}: changelog config must be a mapping")
                else:
                    campaign_id = config.get("id", project.name)
                    if not isinstance(campaign_id, str) or not KEBAB_CASE.fullmatch(
                        campaign_id
                    ):
                        errors.append(
                            f"{config_path}: id must be lowercase kebab-case, "
                            f"got {campaign_id!r}"
                        )
        for entry in sorted((changelog / "unreleased").glob("*.md")):
            if not KEBAB_CASE.fullmatch(entry.stem):
                errors.append(f"{entry}: filename stem must be lowercase kebab-case")
    return errors


def main(argv: list[str] | None = None) -> int:
    """Validate identities used to derive changelog attribution campaigns."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "projects",
        nargs="*",
        type=Path,
        help="project directories to validate (defaults to all top-level projects)",
    )
    args = parser.parse_args(argv)
    projects = args.projects or sorted(
        path for path in Path(".").iterdir() if (path / "changelog").is_dir()
    )
    errors = campaign_identity_errors(projects)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
