---
title: Package installs with typed operator defaults
type: bugfix
authors:
  - zedoraps
  - codex
created: 2026-06-30T07:42:04.965784Z
---

Package installation from the Library now preserves user-defined operator defaults with the correct types.

This fixes packages whose operators use floating-point defaults such as `1.0`, and avoids sending stale package metadata as install overrides.
