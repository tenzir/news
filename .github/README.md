# Continuous integration

This document is the maintainer guide for GitHub Actions, changelog
synchronization, notifications, and deployment automation in `tenzir/news`.

Markdown files under `workflows/` aren't necessarily documentation. In
particular, `workflows/changelog-x.md` is an executable input to GitHub Agentic
Workflows and must remain at its current path.

## Workflow map

| Path | Purpose |
| --- | --- |
| [`actions/sync/action.yaml`](actions/sync/action.yaml) | Triggers this repository's synchronization workflow from a source repository. |
| [`aw/actions-lock.json`](aw/actions-lock.json) | Caches immutable action pins for reproducible agentic workflow compilation. |
| [`workflows/sync.yaml`](workflows/sync.yaml) | Serializes changelog synchronization and sends Discord notifications. |
| [`workflows/changelog-x.md`](workflows/changelog-x.md) | Defines the editable agentic workflow that drafts and processes X posts. |
| [`workflows/changelog-x.lock.yml`](workflows/changelog-x.lock.yml) | Contains the generated, executable GitHub Actions workflow. Don't edit it manually. |
| [`workflows/changelog-x-check.yaml`](workflows/changelog-x-check.yaml) | Tests changelog parsing and X automation on pull requests. |
| [`workflows/rebuild-content.yaml`](workflows/rebuild-content.yaml) | Requests a `tenzir/content` rebuild after a push to `main`. |
| [`scripts/`](scripts/) | Contains deterministic parsing, notification, validation, and publication helpers. |

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

Every push to `main` checks for newly added feature entries matching
`PROJECT/changelog/unreleased/SLUG.md`. Deterministic Python preprocessing
loads each entry through the `tenzir-ship` API. A
[GitHub Agentic Workflow](https://github.github.com/gh-aw/) uses GPT-5.6 Sol to
draft the post or thread.

The workflow doesn't support released entries, nested changelogs, or
`changes/` directories. It processes at most 25 feature entries per run and
fails before inference when a batch exceeds that limit. It serializes up to
100 pending runs in FIFO order so a burst of synchronized entries retains each
push's commit range.

The model has no credentials or write permissions. It can only request a typed
`publish_x_thread` safe output. A separate Python job reparses each entry,
binds it to the triggering Git diff, requires successful threat detection, and
validates the following properties before any write:

- The requested entry and content hash match the triggering diff.
- Every post fits X's weighted-character limit.
- The source URL occurs once in the final post.
- The posts contain no mentions, em dashes, or unexpected URLs.
- The thread shape matches the changelog content.

Live publication uses OAuth 1.0a and retries only connection-establishment
timeouts and explicit rate limits, which are known not to have created a post.
Ambiguous timeouts and server errors stop immediately. A GitHub check-run
ledger provides deduplication and partial-thread resume, binds progress to the
exact drafted posts, and blocks another write after an ambiguous outcome.

To recover an ambiguous write, inspect `@tenzir_company`. Delete the post if X
created it, then manually dispatch the same entry with **Retry after confirming
and removing any ambiguous X post** enabled. The protected environment
approval provides a second check before publication resumes.

#### Staged mode

The workflow is currently staged. It runs the model and all validation, then
renders the proposed thread in the Actions step summary without creating an X
post or a GitHub check run.

Only the `publish_x` job uses the `social-production` environment. It runs
after the secret-free safe-output validator, restricts publication to `main`,
and requires approval without delaying preprocessing or no-op runs. Store these
secrets in that environment:

| Secret | Purpose |
| --- | --- |
| `X_API_KEY` | OAuth 1.0a consumer key for the X application. |
| `X_API_SECRET` | OAuth 1.0a consumer secret for the X application. |
| `X_ACCESS_TOKEN` | Read-and-write token for the Tenzir X account. |
| `X_ACCESS_TOKEN_SECRET` | Secret for the read-and-write access token. |

#### Run a staged preview

Run a preview after the workflow exists on `main`:

1. In the `tenzir/news` repository, open **Actions**.
2. Select **Draft changelog features for X**.
3. Click **Run workflow** and select `main`.
4. Enter an existing direct feature path, such as
   `tenzir/changelog/unreleased/SLUG.md`.
5. Start the workflow.
6. When the publication job pauses, review and approve the
   `social-production` deployment.
7. In the run summary, inspect **Staged Mode: X Thread Preview**.

The preview consumes Copilot credits but doesn't call X. A direct unreleased
entry whose type isn't `feature` produces a no-op before inference. An invalid
entry path fails deterministic validation.

#### Compile the agentic workflow

Edit `workflows/changelog-x.md`, then regenerate
`workflows/changelog-x.lock.yml`. Install the exact
[gh-aw v0.82.10 release](https://github.com/github/gh-aw/releases/tag/v0.82.10)
used by the lock, then compile it. The compiler uses the immutable action SHAs
in `aw/actions-lock.json`:

```sh
gh extension remove aw
gh extension install github/gh-aw --pin v0.82.10
gh aw compile changelog-x --approve --validate
```

Version 0.82.10 provides the built-in `gpt-5.6` alias. The AWF proxy resolves
that alias against the live Copilot model catalog, where the organization model
policy exposes GPT-5.6 Sol. Keep the alias instead of a concrete 5.6 model name:
the pinned AWF runtime accepts the alias before its static concrete-model list
learns about the new model. The compiler also defaults to strict security: the
agent and threat detector run without `sudo` or host access. This workflow
doesn't depend on either capability and must not opt into legacy security.

#### Enable live publication

Complete these steps before the first live post:

1. Enable GPT-5.6 Sol in the Tenzir organization's Copilot model policy.
2. Run and approve a representative staged preview.
3. Confirm that all four X secrets exist in `social-production` and represent
   `@tenzir_company` with read-and-write access.
4. Add X API credits and configure an appropriate spending limit.
5. Change `safe-outputs.staged` and `GH_AW_SAFE_OUTPUTS_STAGED` to `false` in
   `workflows/changelog-x.md`.
6. Recompile the workflow and send the change through a pull request.
7. After the first successful post, retire the fallback Worker and close
   `tenzir/infra#307`.

## Website rebuilds

Every push to `main` runs `workflows/rebuild-content.yaml`. It sends a
`news-updated` repository dispatch to `tenzir/content`, which rebuilds
`tenzir.com/changelog`.

The workflow uses the same Tenzir GitHub App settings as synchronization and
requests a token scoped to the `content` repository.

## Validate CI changes

Run these checks before committing changes to notification scripts or the X
workflow:

```sh
uv run --with-requirements .github/scripts/requirements.txt \
  python .github/scripts/test_changelog.py
uvx ruff check .github/scripts
uvx ruff format --check .github/scripts
git diff --check
```

When you change `workflows/changelog-x.md`, compile it with the pinned gh-aw
release and commit the resulting lock file.
