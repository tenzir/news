# Continuous integration

This document is the maintainer guide for GitHub Actions, changelog
synchronization, notifications, and deployment automation in `tenzir/news`.

## Workflow map

| Path | Purpose |
| --- | --- |
| [`actions/sync/action.yaml`](actions/sync/action.yaml) | Triggers this repository's synchronization workflow from a source repository. |
| [`workflows/sync.yaml`](workflows/sync.yaml) | Serializes changelog synchronization and sends Discord notifications. |
| [`workflows/changelog-x-relay.yaml`](workflows/changelog-x-relay.yaml) | Relays newly added changelog entries to the workflows Worker for X drafting. |
| [`workflows/changelog-check.yaml`](workflows/changelog-check.yaml) | Tests the shared changelog helpers on pull requests. |
| [`workflows/rebuild-content.yaml`](workflows/rebuild-content.yaml) | Requests a `tenzir/content` rebuild after a push to `main`. |
| [`scripts/`](scripts/) | Contains deterministic parsing and notification helpers. |

## Changelog synchronization

Source repositories trigger `workflows/sync.yaml`. The workflow clones the
source repository and synchronizes its changelog into a top-level project
directory.

### Synchronization architecture

The workflow runs in `tenzir/news` and uses `concurrency: group: "sync"` to
serialize updates. This avoids concurrent source repositories racing while
they pull and push the same target repository.

Each run performs these steps:

1. Validate that the source exists in the `tenzir` organization.
2. Clone the source repository.
3. Synchronize the primary changelog and configured module changelogs.
4. Commit and push the result to `main`.
5. Notify configured destinations about new entries and releases.
6. Dispatch a rebuild request to `tenzir/content`.

The workflow uses these organization or repository settings:

| Setting | Purpose |
| --- | --- |
| `vars.TENZIR_GITHUB_APP_ID` | Identifies the Tenzir GitHub App. |
| `secrets.TENZIR_GITHUB_APP_PRIVATE_KEY` | Creates installation tokens. |

### Add a project

Add a workflow like this to the source repository:

```yaml
name: Sync to News

on:
  push:
    branches: [main]
    paths:
      - "changelog/**"
  workflow_dispatch:

jobs:
  sync:
    name: Trigger news sync
    runs-on: ubuntu-latest

    steps:
      - name: Generate app token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.TENZIR_GITHUB_APP_ID }}
          private-key: ${{ secrets.TENZIR_GITHUB_APP_PRIVATE_KEY }}
          repositories: news

      - name: Trigger sync workflow
        uses: tenzir/news/.github/actions/sync@main
        with:
          token: ${{ steps.app-token.outputs.token }}
```

The action derives the following defaults from the source repository:

- `project`: The repository name, such as `mcp` for `tenzir/mcp`.
- `target`: The project name and target directory in `tenzir/news`.
- `path`: `changelog`.

Override the target when the synchronized directory and source repository have
different names:

```yaml
- uses: tenzir/news/.github/actions/sync@main
  with:
    token: ${{ steps.app-token.outputs.token }}
    target: platform
```

For an initial import, set `skip_notifications: true`. Remove it after the
first synchronization.

### Synchronize module changelogs

For a repository with module changelogs, add each module path to the source
workflow trigger and pass the paths through `extra_paths`:

```yaml
on:
  push:
    branches: [main]
    paths:
      - "changelog/**"
      - "plugins/*/changelog/**"

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Generate app token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.TENZIR_GITHUB_APP_ID }}
          private-key: ${{ secrets.TENZIR_GITHUB_APP_PRIVATE_KEY }}
          repositories: news

      - uses: tenzir/news/.github/actions/sync@main
        with:
          token: ${{ steps.app-token.outputs.token }}
          extra_paths: "plugins/*/changelog"
```

The `extra_paths` input accepts space-separated glob patterns. Each matching
directory remains under the target project. For example,
`plugins/foo/changelog` synchronizes to
`PROJECT/plugins/foo/changelog` in this repository.

### Trigger synchronization directly

You can also dispatch the workflow without the composite action:

```sh
gh workflow run sync.yaml \
  --repo tenzir/news \
  --field project=PROJECT \
  --field path=changelog
```

## Notifications

The synchronization workflow can notify Discord and trigger the X drafting
workflow. Setting `skip_notifications: true` adds `[skip notifications]` to the
sync commit, which suppresses both channels.

### Discord notifications

Configure these optional repository secrets:

| Secret | Purpose |
| --- | --- |
| `DISCORD_CHANGELOG_WEBHOOK` | Notifies about new unreleased entries. |
| `DISCORD_RELEASE_WEBHOOK` | Notifies about new top-level releases. |

When a secret is absent, the workflow skips the corresponding notification.
Notification failures don't fail the synchronization run.

### X automation

Every push to `main` runs `workflows/changelog-x-relay.yaml`, which collects
newly added feature entries matching `PROJECT/changelog/unreleased/SLUG.md`
and relays the commit SHA and entry paths to the `workflows` Cloudflare Worker
in [`tenzir/infra`](https://github.com/tenzir/infra) (`website/workflows/`).
Everything else — fetching and parsing the entries, drafting posts with
GPT-5.6 Sol through an AI Gateway, deterministic validation (weighted
280-character limit, canonical changelog URL exactly once in the final post,
no mentions or em dashes, thread shape matching the entry content), and
OAuth 1.0a publication to `@tenzir_company` — happens in that Worker as a
durable Cloudflare Workflow. See the Worker's README for the full design,
including the Durable Object ledger that guarantees a crash can never publish
a duplicate post.

This repository needs one Actions secret:

| Secret | Purpose |
| --- | --- |
| `WORKFLOWS_NEWS_TOKEN` | Authenticates the relay against the Worker. Mirrors the `workflows-news-token` value in the Cloudflare Secrets Store. |

To recover an ambiguous write (the Worker refused to publish because a prior
write's outcome is unknown), inspect `@tenzir_company`. Delete the post if X
created it, then manually dispatch the relay for the same entry with **Retry
after confirming and removing any ambiguous X post** enabled.

## Website rebuilds

Every push to `main` runs `workflows/rebuild-content.yaml`. It sends a
`news-updated` repository dispatch to `tenzir/content`, which rebuilds
`tenzir.com/changelog`.

The workflow uses the same Tenzir GitHub App settings as synchronization and
requests a token scoped to the `content` repository.

## Validate CI changes

Run these checks before committing changes to the notification scripts:

```sh
uv run --with-requirements .github/scripts/requirements.txt \
  python .github/scripts/test_changelog.py
uvx ruff check .github/scripts
uvx ruff format --check .github/scripts
git diff --check
```
