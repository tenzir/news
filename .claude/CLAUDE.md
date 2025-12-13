# Tenzir News

This repository aggregates changelog entries from multiple Tenzir repositories.

## Repository Structure

Each top-level directory is a [tenzir/changelog](https://github.com/tenzir/changelog)
project, synced from a source repository:

```
news/
├── tenzir/     # from tenzir/tenzir
├── docs/       # from tenzir/docs
└── ...
```

## Changelog Synchronization

Source repositories push changelog updates to this repository via GitHub Actions.
The synchronization uses a pull-based workflow to avoid race conditions.

### The Problem

A naive approach where source repos directly push to this repo has a TOCTOU
(time-of-check-time-of-use) issue: when multiple repos push simultaneously,
concurrent pulls and pushes can conflict.

### The Solution

The update workflow runs in _this_ repository, triggered by source repos:

1. Source repo triggers `.github/workflows/update.yaml` via `gh workflow run`
2. The workflow uses `concurrency: group: "update"` to serialize all updates
3. Each update gets exclusive access: clone source, sync files, commit, push

### Triggering an Update

Source repositories trigger updates with:

```bash
gh workflow run update.yaml \
  --repo tenzir/news \
  --field project=<project-name> \
  --field path=<changelog-path>  # optional, defaults to "changelog"
```

The `path` parameter allows source repos to specify where their changelog
directory is located (e.g., `changelog`, `docs/changelog`, etc.).
