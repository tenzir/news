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
    get_package_config,
    get_package_release_url,
    get_package_url,
    get_repository,
    get_source_file_url,
    load_entry,
    unfold_soft_breaks,
)

# Type configuration: emoji, label, and embed color
TYPE_CONFIG = {
    "feature": ("🚀", "feature", 0x58ACFF),  # Blue
    "change": ("🔄", "change", 0x9B59B6),  # Purple
    "breaking": ("💥", "breaking change", 0xE74C3C),  # Red
    "bugfix": ("🐞", "bug fix", 0x2ECC71),  # Green
    "fix": ("🐞", "bug fix", 0x2ECC71),
}
DEFAULT_TYPE = ("📝", "update", 0x58ACFF)


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


def entry_message(file: Path, *, kicker: str, url: str, repo: str) -> dict:
    """Render a changelog entry with its type, authors, and PR links."""
    data = load_entry(file)
    emoji, label, color = TYPE_CONFIG.get(data["type"], DEFAULT_TYPE)

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

    # A very long body is truncated by the message builder.
    return build_entry_message(
        kicker=kicker,
        label=f"{emoji} {label}",
        title=data["title"],
        url=url,
        body=unfold_soft_breaks(data["body"]),
        meta=" ".join(meta_parts),
        color=color,
    )


def load_release(release_file: Path) -> dict:
    """Load the output of `tenzir-ship show VERSION --release --json`."""
    (data,) = json.loads(release_file.read_text())
    return data


def release_message(data: dict, *, name: str, url: str, product_url: str) -> dict:
    """Render a release that lists its entry titles by type."""
    return build_release_message(
        data,
        name=name,
        url=url,
        product_url=product_url,
        color=0x2ECC71,  # Green
    )


def deliver(message: dict, webhook_url: str | None, dry_run: bool) -> None:
    """Send a message, or print it with --dry-run."""
    if dry_run:
        click.echo(json.dumps(message, indent=2, ensure_ascii=False))
        return
    if not webhook_url:
        raise click.UsageError("WEBHOOK_URL is required unless --dry-run is set.")
    send(webhook_url, message)


dry_run_option = click.option(
    "--dry-run",
    is_flag=True,
    help="Print the message JSON instead of sending it.",
)


@cli.command()
@click.argument("project")
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url", required=False)
@dry_run_option
def entry(project: str, file: Path, webhook_url: str | None, dry_run: bool):
    """Send a notification for a changelog entry."""
    config = get_config_for_entry(file)
    repo = get_repository(project, config)
    # Link the title to the entry on the public changelog. PR links remain
    # available in the byline.
    message = entry_message(
        file,
        kicker=f"**{repo}**",
        url=get_changelog_entry_url(project, file, config),
        repo=repo,
    )
    deliver(message, webhook_url, dry_run)


@cli.command("package-entry")
@click.argument("package", type=click.Path(exists=True, path_type=Path))
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url", required=False)
@click.option("--repository", required=True, help="Source repository, OWNER/NAME.")
@click.option("--ref", required=True, help="Source commit of the entry.")
@dry_run_option
def package_entry(
    package: Path,
    file: Path,
    webhook_url: str | None,
    repository: str,
    ref: str,
    dry_run: bool,
):
    """Send a notification for a package changelog entry.

    PACKAGE is the synchronized package directory, such as `library/zeek`.
    The website shows released package notes only, so the title links to the
    entry in the source repository at commit REF.
    """
    config = get_package_config(package)
    source_path = file.relative_to(package.parent)
    message = entry_message(
        file,
        kicker=f"**{config['name']}**",
        url=get_source_file_url(repository, ref, source_path),
        repo=repository,
    )
    deliver(message, webhook_url, dry_run)


@cli.command()
@click.argument("project")
@click.argument("release_file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url", required=False)
@dry_run_option
def release(project: str, release_file: Path, webhook_url: str | None, dry_run: bool):
    """Send a notification for a release.

    RELEASE_FILE is the output of `tenzir-ship show VERSION --release --json`.
    The notification is a Components V2 message that lists entry titles by type
    and links to the full notes in a button. With
    --dry-run, WEBHOOK_URL is optional and the payload goes to stdout, ready to
    paste into a Discord message builder.
    """
    config = get_config(project)
    data = load_release(release_file)
    message = release_message(
        data,
        name=config.get("name", project),
        url=get_changelog_release_url(project, data["version"], config),
        product_url=get_changelog_product_url(project, config),
    )
    deliver(message, webhook_url, dry_run)


@cli.command("package-release")
@click.argument("package", type=click.Path(exists=True, path_type=Path))
@click.argument("release_file", type=click.Path(exists=True, path_type=Path))
@click.argument("webhook_url", required=False)
@dry_run_option
def package_release(
    package: Path, release_file: Path, webhook_url: str | None, dry_run: bool
):
    """Send a notification for a package release.

    PACKAGE is the synchronized package directory, such as `library/zeek`, and
    RELEASE_FILE is the output of
    `tenzir-ship --root PACKAGE show VERSION --release --json`. The buttons
    link to the package page, which lists the release notes.
    """
    config = get_package_config(package)
    message = release_message(
        load_release(release_file),
        name=config["name"],
        url=get_package_release_url(config),
        product_url=get_package_url(config),
    )
    deliver(message, webhook_url, dry_run)


if __name__ == "__main__":
    cli()
