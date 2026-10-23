#!/usr/bin/env python3
"""Discord notification script for changelog entries and releases."""

import json
from pathlib import Path

import click
import requests
from changelog import (
    build_entry_message,
    build_release_message,
    get_changelog_entry_url,
    get_changelog_product_url,
    get_changelog_release_url,
    get_config,
    get_config_for_entry,
    get_repository,
    load_entry,
    unfold_soft_breaks,
)

# Type configuration: emoji, label, and embed color
TYPE_CONFIG = {
    "feature": ("🚀", "Feature", 0x58ACFF),  # Blue
    "change": ("🔄", "Change", 0x9B59B6),  # Purple
    "breaking": ("💥", "Breaking Change", 0xE74C3C),  # Red
    "bugfix": ("🐞", "Bug Fix", 0x2ECC71),  # Green
    "fix": ("🐞", "Bug Fix", 0x2ECC71),
}
DEFAULT_TYPE = ("📝", "Update", 0x58ACFF)


def send(webhook_url: str, message: dict) -> None:
    """Post a Components V2 message to a Discord webhook.

    Discord ignores components unless `with_components` is set. Webhooks that
    aren't owned by an application accept only non-interactive components, such
    as link buttons. The message can't carry `content` or `embeds`, so this
    uses the Discord HTTP API directly.
    """
    response = requests.post(
        webhook_url,
        params={"with_components": "true", "wait": "true"},
        json=message,
        timeout=30,
    )
    if not response.ok:
        raise click.ClickException(
            f"Discord returned {response.status_code}: {response.text}"
        )


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

    # Link the embed title to the entry on the public changelog. PR links remain
    # available in the metadata below.
    url = get_changelog_entry_url(project, file, config)

    # Build the body. A very long body is truncated by the message builder.
    description = unfold_soft_breaks(data["body"])

    # Add metadata (authors and prs are simple lists after tenzir-ship normalization)
    meta_parts = []
    if data["authors"]:
        authors_str = ", ".join(
            f"[@{a}](https://github.com/{a})" for a in data["authors"]
        )
        meta_parts.append(f"by {authors_str}")
    if data["prs"]:
        prs_str = ", ".join(
            f"[#{pr}](https://github.com/{repo}/pull/{pr})" for pr in data["prs"]
        )
        meta_parts.append(f"({prs_str})")

    message = build_entry_message(
        kicker=f"**{repo}**",
        label=f"{emoji} {label}",
        title=data["title"],
        url=url,
        body=description,
        meta=" ".join(meta_parts),
        color=color,
    )
    send(webhook_url, message)


@cli.command()
@click.argument("project")
@click.argument("release_file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url", required=False)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print the message JSON instead of sending it.",
)
def release(
    project: str, release_file: Path, webhook_url: str | None, dry_run: bool
):
    """Send a notification for a release.

    RELEASE_FILE is the output of `tenzir-ship show VERSION --release --json`.
    The notification is a Components V2 message that lists entry titles by type
    and links to the full notes in a button. With
    --dry-run, WEBHOOK_URL is optional and the payload goes to stdout, ready to
    paste into a Discord message builder.
    """
    if not dry_run and not webhook_url:
        raise click.UsageError("WEBHOOK_URL is required unless --dry-run is set.")
    config = get_config(project)
    name = config.get("name", project)

    (data,) = json.loads(release_file.read_text())
    url = get_changelog_release_url(project, data["version"], config)
    message = build_release_message(
        data,
        name=name,
        url=url,
        product_url=get_changelog_product_url(project, config),
        color=0x2ECC71,  # Green
    )
    if dry_run:
        click.echo(json.dumps(message, indent=2, ensure_ascii=False))
        return
    send(webhook_url, message)


if __name__ == "__main__":
    cli()
