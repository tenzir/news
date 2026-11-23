---
title: "Add optional Caddy reverse proxy for seaweed S3 storage"
type: feature
author: lava
created: 2026-01-19T16:47:31Z
---

The seaweed S3 storage component now supports an optional Caddy reverse proxy that improves S3 error handling. Set `TENZIR_ENABLE_CADDY=true` to enable it. The reverse proxy intercepts 404 responses and returns proper S3-style error messages.
