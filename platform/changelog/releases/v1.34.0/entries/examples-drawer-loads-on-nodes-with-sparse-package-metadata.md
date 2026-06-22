---
title: Examples drawer loads on nodes with sparse package metadata
type: bugfix
authors:
  - Zedoraps
  - claude
created: 2026-06-16T22:48:31.211245Z
---

The Explorer's Examples drawer no longer hangs at "Loading…" on Tenzir
Nodes that have installed packages whose examples are missing a `name`
or `description` (for instance several mappers under `microsoft/`,
`fortinet/`, `otel/`, and `zscaler/` in the Tenzir Library).
