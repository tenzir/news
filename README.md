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
- `path`: `changelog` (path to changelog directory in source repo)

Override these by passing additional inputs to the action if needed.

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
