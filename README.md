# ✨ Tenzir News

This repository aggregates changelog entries from Tenzir repositories. Each
directory corresponds to a project and follows the
[tenzir/changelog](https://github.com/tenzir/changelog) format.

---

## 🛠️ Development

### 🔄 Adding a New Project

To sync a project's changelog to this repository, add a workflow to the source
repository:

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

The action uses sensible defaults:

- `project`: repository name (e.g., `mcp` for `tenzir/mcp`)
- `path`: `changelog` (path to changelog directory in source repo)

Override these by passing additional inputs to the action if needed.
