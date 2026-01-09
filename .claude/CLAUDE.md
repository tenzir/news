# Tenzir News

This repository aggregates changelog entries from multiple Tenzir repositories.

## Important: No Local Changelog

This repository does **not** have its own changelog. Do not create changelog
entries here when committing changes.

The top-level directories are synced changelog projects from other repositories.
In particular, `ship/` is **not** this project's changelog—it contains
entries synced from the `tenzir/ship` repository (the ship tool
itself). Other directories like `tenzir/` and `docs/` follow the same pattern.

## Repository Structure

Each top-level directory is a [tenzir/ship](https://github.com/tenzir/ship)
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
