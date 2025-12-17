# ✨ Tenzir News

This repository aggregates changelog entries from Tenzir repositories. Each
directory corresponds to a project and follows the
[tenzir/changelog](https://github.com/tenzir/changelog) format.

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
