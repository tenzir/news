#!/usr/bin/env python3
"""Discord notification script for changelog entries and releases."""

import re
from pathlib import Path

import click
from discord_webhook import DiscordEmbed, DiscordWebhook

from changelog import get_config_for_entry, get_repository, load_entry


# Type configuration: emoji, label, and embed color
TYPE_CONFIG = {
    "feature": ("🚀", "Feature", 0x58ACFF),  # Blue
    "change": ("🔄", "Change", 0x9B59B6),  # Purple
    "breaking": ("💥", "Breaking Change", 0xE74C3C),  # Red
    "bugfix": ("🐞", "Bug Fix", 0x2ECC71),  # Green
    "fix": ("🐞", "Bug Fix", 0x2ECC71),
}
DEFAULT_TYPE = ("📝", "Update", 0x58ACFF)


def strip_leading_heading(text: str) -> str:
    """Remove the leading # heading from text (embed title already serves this purpose)."""
    lines = text.lstrip().split("\n", 1)
    if lines and lines[0].startswith("# "):
        return lines[1].lstrip() if len(lines) > 1 else ""
    return text


def demote_headers(text: str) -> str:
    """Demote ## headers to ### for better visual hierarchy in Discord.

    Discord renders ## headers very prominently, often larger than the embed
    title. Demoting to ### keeps section structure while respecting hierarchy.
    """
    return re.sub(r"^## ", "### ", text, flags=re.MULTILINE)


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
    data = load_entry(file)

    emoji, label, color = TYPE_CONFIG.get(data["type"], DEFAULT_TYPE)

    # Build URL - prefer PR link, fall back to repo
    if data["prs"]:
        url = f"https://github.com/{repo}/pull/{data['prs'][0]}"
    else:
        url = f"https://github.com/{repo}"

    # Build description
    description = truncate(data["body"], 3800)

    # Add metadata (authors and prs are simple lists after tenzir-ship normalization)
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
    notes = strip_leading_heading(notes)
    notes = demote_headers(notes)
    notes = truncate(notes, 3800)

    url = f"https://github.com/{repo}/releases/tag/{version}"

    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(
        title=f"{title} {version}",
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
