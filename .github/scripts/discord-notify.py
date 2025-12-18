#!/usr/bin/env python3
"""Discord notification script for changelog entries and releases."""

from pathlib import Path

import click
import yaml
from discord_webhook import DiscordEmbed, DiscordWebhook


def get_config_for_entry(entry_path: Path) -> dict:
    """Get config from config.yaml relative to an entry file.

    Entries can be in:
    - <project>/changelog/unreleased/<entry>.md
    - <project>/changelog/releases/<version>/entries/<entry>.md
    - <project>/<subdir>/changelog/unreleased/<entry>.md (nested)

    In all cases, we find config.yaml in the changelog root (parent of unreleased/
    or releases/).
    """
    # Walk up to find the changelog root (contains config.yaml, unreleased/, releases/)
    current = entry_path.parent
    while current != current.parent:
        config_path = current / "config.yaml"
        if config_path.exists():
            return yaml.safe_load(config_path.read_text()) or {}
        current = current.parent
    return {}


def get_config(project: str) -> dict:
    """Get config from top-level config.yaml for a project."""
    config_path = Path(project) / "changelog" / "config.yaml"
    if config_path.exists():
        return yaml.safe_load(config_path.read_text()) or {}
    return {}


def get_repository(project: str, config: dict | None = None) -> str:
    """Get repository from config, falling back to tenzir/{project}."""
    if config is None:
        config = get_config(project)
    return config.get("repository", f"tenzir/{project}")


# Type configuration: emoji, label, and embed color
TYPE_CONFIG = {
    "feature": ("🚀", "Feature", 0x58ACFF),  # Blue
    "change": ("🔄", "Change", 0x9B59B6),  # Purple
    "breaking": ("💥", "Breaking Change", 0xE74C3C),  # Red
    "bugfix": ("🐞", "Bug Fix", 0x2ECC71),  # Green
    "fix": ("🐞", "Bug Fix", 0x2ECC71),
}
DEFAULT_TYPE = ("📝", "Update", 0x58ACFF)


def parse_entry(file_path: Path) -> dict:
    """Parse a changelog entry file with YAML frontmatter."""
    content = file_path.read_text()

    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"title": file_path.stem, "type": "change", "body": content}

    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()

    # Normalize singular/plural fields
    authors = frontmatter.get("authors") or []
    if not authors and "author" in frontmatter:
        authors = [frontmatter["author"]]

    prs = frontmatter.get("prs") or []
    if not prs and "pr" in frontmatter:
        prs = [frontmatter["pr"]]

    return {
        "title": frontmatter.get("title", file_path.stem),
        "type": frontmatter.get("type", "change"),
        "authors": authors,
        "prs": prs,
        "body": body,
    }


def truncate(text: str, max_length: int = 4000) -> str:
    """Truncate text to fit Discord's embed limits."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 20] + "\n\n*[Truncated]*"


@click.group()
def cli():
    """Send Discord notifications for changelog updates."""


@cli.command()
@click.argument("project")
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url")
def entry(project: str, file: Path, webhook_url: str):
    """Send a notification for a changelog entry."""
    config = get_config_for_entry(file)
    repo = get_repository(project, config)
    data = parse_entry(file)

    emoji, label, color = TYPE_CONFIG.get(data["type"], DEFAULT_TYPE)

    # Build URL - prefer PR link, fall back to repo
    if data["prs"]:
        url = f"https://github.com/{repo}/pull/{data['prs'][0]}"
    else:
        url = f"https://github.com/{repo}"

    # Build description
    description = truncate(data["body"], 3800)

    # Add metadata
    meta_parts = []
    if data["authors"]:
        authors_str = ", ".join(
            f"[@{a}](https://github.com/{a})" for a in data["authors"]
        )
        meta_parts.append(f"By {authors_str}")
    if data["prs"]:
        prs_str = ", ".join(
            f"[#{pr}](https://github.com/{repo}/pull/{pr})" for pr in data["prs"]
        )
        meta_parts.append(prs_str)

    if meta_parts:
        description += f"\n\n*{' · '.join(meta_parts)}*"

    # Create and send embed
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=data["title"],
        description=description,
        color=color,
        url=url,
    )
    embed.set_author(
        name=repo,
        url=f"https://github.com/{repo}",
    )
    embed.set_footer(text=f"{emoji} {label}")
    webhook.add_embed(embed)
    webhook.execute()


@cli.command()
@click.argument("project")
@click.argument("version")
@click.argument("notes_file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url")
def release(project: str, version: str, notes_file: Path, webhook_url: str):
    """Send a notification for a release."""
    config = get_config_for_entry(notes_file)
    repo = get_repository(project, config)
    title = config.get("name", project)

    notes = notes_file.read_text()
    notes = truncate(notes, 3800)

    url = f"https://github.com/{repo}/releases/tag/{version}"

    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=f"**{title}** {version}",
        description=notes,
        color=0x2ECC71,  # Green
        url=url,
    )
    embed.set_author(
        name=repo,
        url=f"https://github.com/{repo}",
    )
    webhook.add_embed(embed)
    webhook.execute()


if __name__ == "__main__":
    cli()
