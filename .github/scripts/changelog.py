"""Shared helpers for loading changelog projects and entries."""

from pathlib import Path
from typing import TypedDict

import yaml


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
