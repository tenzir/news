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
binds it to the triggering Git diff, and validates the following properties
before any write:

- The requested entry and content hash match the triggering diff.
- Every post fits X's weighted-character limit.
- The canonical Tenzir changelog URL occurs once in the final post.
- The posts contain no mentions, em dashes, or unexpected URLs.
- The thread shape matches the changelog content.

AI threat detection is disabled for this workflow. The drafting agent is
credentialless and read-only, while the separate publisher accepts only the
typed output after deterministic validation. A second model pass would add AI
usage and latency without guarding the X credentials or write operation.

Each post links to the project's changelog on `tenzir.com`, not to its
implementation pull request. The URL uses the canonical project ID from
`changelog/config.yaml`.
For example, an entry under `skills/` links to
`https://tenzir.com/changelog/tenzir-skills/`. The project page remains stable
when an entry moves from the unreleased section into a versioned release.
The workflow explicitly allows `tenzir.com` so gh-aw's safe-output sanitizer
preserves that URL. The drafting agent has no general web tool.

Live publication uses OAuth 1.0a and retries only connection-establishment
timeouts and explicit rate limits, which are known not to have created a post.
Ambiguous timeouts and server errors stop immediately. A GitHub check-run
ledger provides deduplication and partial-thread resume, binds progress to the
exact drafted posts, and blocks another write after an ambiguous outcome.

To recover an ambiguous write, inspect `@tenzir_company`. Delete the post if X
created it, then manually dispatch the same entry with **Retry after confirming
and removing any ambiguous X post** enabled. The explicit dispatch and retry
flag provide operator confirmation before publication resumes.

#### Staged mode

Staged mode runs the model and all validation, then renders the proposed thread
in the Actions step summary without creating an X post or a GitHub check run.
The production workflow has staged mode disabled.

Only the `publish_x` job uses the `social-production` environment. It runs
after the secret-free safe-output validator, restricts publication to `main`,
and exposes the X credentials only to the publication job. The environment has
no required reviewers or wait timer, so validated feature entries publish
without human intervention. Store these secrets in that environment:

| Secret | Purpose |
| --- | --- |
| `X_API_KEY` | OAuth 1.0a consumer key for the X application. |
| `X_API_SECRET` | OAuth 1.0a consumer secret for the X application. |
| `X_ACCESS_TOKEN` | Read-and-write token for the Tenzir X account. |
| `X_ACCESS_TOKEN_SECRET` | Secret for the read-and-write access token. |

#### Run a drafting preview

Run a branch preview before merging a workflow change:

1. In the `tenzir/news` repository, open **Actions**.
2. Select **Draft changelog features for X**.
3. Click **Run workflow** and select the pull request branch.
4. Enter an existing direct feature path, such as
   `tenzir/changelog/unreleased/SLUG.md`.
5. Start the workflow.
6. Download the `agent` artifact and inspect `agent_output.json`.

The branch preview consumes Copilot credits but cannot run the main-only
publication job. A direct unreleased entry whose type isn't `feature` produces
a no-op before inference. An invalid entry path fails deterministic validation.

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

Version 0.82.10 provides a built-in `gpt-5.6` alias, but that alias can resolve
to Luna, Sol, or Terra. The workflow therefore imports its own local
`gpt-5.6-sol` alias from `workflows/shared/gpt-5.6-sol.md`; its only candidate
is `copilot/gpt-5.6-sol`. Keep that alias: it lets the pinned AWF runtime
validate an alias while still selecting Sol from the live Copilot model
catalog. The compiler also defaults to strict security: the agent and threat
detector run without `sudo` or host access. This workflow doesn't depend on
either capability and must not opt into legacy security.

#### Live publication

The production workflow has live publication enabled. These prerequisites must
remain in place:

1. Keep **Allow use of Copilot CLI billed to the organization** enabled under
   **Organization Settings → Copilot → Policies → Copilot CLI**.
2. Keep GPT-5.6 Sol enabled in the Tenzir organization's Copilot model policy.
3. Confirm that all four X secrets exist in `social-production` and represent
   `@tenzir_company` with read-and-write access.
4. Keep `social-production` restricted to `main` without required reviewers or
   a wait timer.
5. Maintain enough X API credits and an appropriate spending limit.
6. Keep `safe-outputs.staged` and `GH_AW_SAFE_OUTPUTS_STAGED` set to `false` in
   `workflows/changelog-x.md`.
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
