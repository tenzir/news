---
title: JSON output for workspace creation
type: feature
authors:
  - lava
created: 2026-09-21T10:35:00.000000Z
---

`tenzir-platform admin create-workspace` gained a `--json` flag, so scripts can read the id of the new workspace without parsing a human-readable message:

```sh
tenzir-platform admin create-workspace team my-team --json
```
