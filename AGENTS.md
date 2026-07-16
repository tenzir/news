# Tenzir News

This repository aggregates changelog entries from multiple Tenzir repositories.

## Important: No local changelog

This repository does **not** have its own changelog. Do not create changelog
entries here when committing changes.

The top-level directories are synchronized changelog projects from other
repositories. In particular, `ship/` is not this project's changelog. It
contains entries synchronized from the `tenzir/ship` repository.

## Repository structure

Each top-level directory is a [tenzir/ship](https://github.com/tenzir/ship)
project synchronized from a source repository:

```text
news/
├── tenzir/     # from tenzir/tenzir
├── platform/   # from tenzir/platform-internal
└── ...
```

## CI documentation

Before changing actions, workflows, scripts, credentials, environments, or
notification behavior, read the [CI maintainer guide](.github/README.md). Treat
it as the source of truth for CI architecture and operations.

Markdown files under `.github/workflows/` can be executable GitHub Agentic
Workflow sources. Do not move or rename them as documentation files.
