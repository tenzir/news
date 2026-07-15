# ✨ Tenzir News

This repository aggregates changelog entries from Tenzir repositories. Each
directory corresponds to a project and follows the
[tenzir/ship](https://github.com/tenzir/ship) format.

---

## 🛠️ Development

### 🔄 Adding a New Project

To sync a project's changelog to this repository, add a workflow to the source
repository.

<details>
<summary>Example workflow</summary>

```yaml
# .github/workflows/sync-news.yaml
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
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ vars.TENZIR_GITHUB_APP_ID }}
          private-key: ${{ secrets.TENZIR_GITHUB_APP_PRIVATE_KEY }}
          repositories: news

      - name: Trigger sync workflow
        uses: tenzir/news/.github/actions/sync@main
        with:
          token: ${{ steps.app-token.outputs.token }}
```

</details>

The action uses sensible defaults:

- `project`: repository name (e.g., `mcp` for `tenzir/mcp`)
- `target`: same as `project` (directory name in this repo)
- `path`: `changelog` (path to changelog directory in source repo)

Override these by passing additional inputs to the action if needed. For example,
to sync from `tenzir/platform-internal` to `platform/` in this repo:

```yaml
- uses: tenzir/news/.github/actions/sync@main
  with:
    token: ${{ steps.app-token.outputs.token }}
    target: platform
```

For initial imports with existing changelog entries, add `skip_notifications: true`
to avoid flooding Discord, then remove it after the first sync.

### 🧩 Projects with Modules

For projects that contain modules with their own changelogs (e.g., a monorepo
with plugins), add the module paths to both the trigger and the action.

<details>
<summary>Example workflow</summary>

```yaml
# .github/workflows/sync-news.yaml
name: Sync to News

on:
  push:
    branches: [main]
    paths:
      - "changelog/**"
      - "plugins/*/changelog/**"
  workflow_dispatch:

jobs:
  sync:
    name: Trigger news sync
    runs-on: ubuntu-latest

    steps:
      - name: Generate app token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ vars.TENZIR_GITHUB_APP_ID }}
          private-key: ${{ secrets.TENZIR_GITHUB_APP_PRIVATE_KEY }}
          repositories: news

      - name: Trigger sync workflow
        uses: tenzir/news/.github/actions/sync@main
        with:
          token: ${{ steps.app-token.outputs.token }}
          extra_paths: "plugins/*/changelog"
```

</details>

The `extra_paths` input accepts glob patterns for additional changelog
directories. Each matched directory syncs as a separate project (e.g.,
`plugins/foo/changelog` syncs to `foo/` in this repository).

### 📣 Discord Notifications

The sync workflow can send notifications to Discord when new changelog entries
or releases are detected. Configure these repository secrets to enable:

| Secret                      | Description                                  |
| --------------------------- | -------------------------------------------- |
| `DISCORD_CHANGELOG_WEBHOOK` | Webhook URL for individual changelog entries |
| `DISCORD_RELEASE_WEBHOOK`   | Webhook URL for release announcements        |

Both are optional. If not set, the corresponding notifications are skipped.

**Entry notifications** are sent for each new changelog entry file detected
during sync. They include the entry title, description, type, and author.

**Release notifications** are sent when a new release appears (detected by a new
`notes.md` file in a `releases/` directory). They include the full release notes.

### X thread automation

Every push to `main` checks for newly added feature entries that match
`PROJECT/changelog/unreleased/SLUG.md`. Deterministic Python preprocessing loads
each entry through the `tenzir-ship` API. A
[GitHub Agentic Workflow](https://github.github.com/gh-aw/) then uses GPT-5.6 Sol
to draft the post or thread. The model receives no secrets and has no write
permissions.

The model can only request the typed `publish_x_thread` safe output. A separate
Python job reparses the entry, binds it to the triggering Git diff, checks the
weighted X length and thread policy, and publishes through OAuth 1.0a. Released
entries, nested changelogs, and `changes/` directories aren't supported.
Each run processes at most 25 feature entries. If a sync exceeds that limit,
the workflow fails before inference, and you can preview each entry with the
manual dispatch input.

The workflow is currently in staged mode. It validates proposed posts and shows
them in the Actions step summary, but it does not call X or create GitHub check
runs. The main-only `social-production` environment requires approval and will
hold these environment secrets when live publication is enabled:

| Secret | Description |
| --- | --- |
| `X_API_KEY` | X application API key. |
| `X_API_SECRET` | X application API secret. |
| `X_ACCESS_TOKEN` | User access token for the Tenzir X account. |
| `X_ACCESS_TOKEN_SECRET` | User access-token secret. |

The sync workflow adds `[skip notifications]` to its commit message when you
select `skip_notifications`. The X workflow ignores those commits. You can use
the workflow's manual dispatch input to preview one explicit entry later.

The editable workflow source is `.github/workflows/changelog-x.md`; its generated
`.lock.yml` is committed. The current `gh-aw` release predates GPT-5.6 Sol and
pins an older Copilot CLI, so the lock was generated from the tested
`github/gh-aw` commit below. Until a release includes GPT-5.6 Sol, use that same
compiler revision when regenerating it. For example, from the repository root:

```sh
gh_aw_ref=89c05847be8c41c3490e371af3819dc1e1057a81
docker run --rm --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e GH_AW_REF="$gh_aw_ref" \
  -v "$PWD":/work -w /work \
  golang:1.26.3@sha256:2d6c80227255c3112a4d08e67ba98e58efd3846daf15d9d7d4c389565d881b1a \
  bash -euc '
    git clone --filter=blob:none https://github.com/github/gh-aw /tmp/gh-aw
    git -C /tmp/gh-aw checkout "$GH_AW_REF"
    (cd /tmp/gh-aw && go build -o /tmp/gh-aw-bin ./cmd/gh-aw)
    /tmp/gh-aw-bin compile changelog-x --approve --validate \
      --gh-aw-ref "$GH_AW_REF"
  '
```

Return to `gh aw compile changelog-x` after a `gh-aw` release includes GPT-5.6
Sol. The temporary `shared/gpt-5.6-sol.md` import pins the exact Sol model while
the firewall's built-in model catalog catches up; remove it only after the
firewall natively accepts `gpt-5.6-sol`. To go live after reviewing staged
output:

1. Enable GPT-5.6 Sol in the Tenzir organization's Copilot model policies.
2. Run the workflow manually for a representative entry and approve the staged
   safe-output job.
3. Review the complete thread in the run's step summary.
4. Add the four X secrets to the protected `social-production` environment.
5. Change `safe-outputs.staged` and the custom job's temporary
   `GH_AW_SAFE_OUTPUTS_STAGED` override to `false`, recompile, and send that
   change through a pull request.
6. After the first successful live post, retire the fallback Worker and close
   its infra pull request.

### 🌐 Website Rebuilds

Every push to `main` dispatches a `news-updated` event to `tenzir/content` via
`.github/workflows/rebuild-content.yaml`. The content repository receives that
event and triggers the Cloudflare Workers Builds deploy hook so
`tenzir.com/changelog` picks up new entries and releases.
