---
title: Graceful shutdown for Docker Compose nodes
type: change
authors:
  - zedoraps
created: 2026-07-01T13:31:45.141605Z
---

Newly downloaded Docker Compose node configurations now include the correct timeout for graceful node shutdown.

To update an existing Docker Compose file, add `stop_grace_period: 4m` to the `tenzir-node` service.
