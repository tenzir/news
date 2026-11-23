---
title: Server-side API proxy path validation
type: bugfix
authors:
  - Zedoraps
  - Avaq
  - codex
prs:
  - 224
created: 2026-06-23T09:13:48.151839Z
---

Server-side API proxy routes now validate resource paths before forwarding requests to upstream services.

This keeps forwarded requests within the intended upstream API scope.
