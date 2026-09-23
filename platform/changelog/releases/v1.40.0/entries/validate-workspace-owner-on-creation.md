---
title: Workspace creation validates the owner
type: bugfix
authors:
  - lava
created: 2026-09-21T10:30:00.000000Z
---

`tenzir-platform admin create-workspace` now rejects an owner that the platform cannot resolve, instead of creating a workspace that fails to open later. The `organization` namespace requires an organization that exists in the platform, with an `org-xxxxxxxx` id; use `team` for a free-form owner id. `admin update-workspace` already applied this check.

Opening a workspace whose owning organization no longer exists now fails with a 409 that names the problem, rather than an opaque 500. Repair it by reassigning the owner:

```sh
tenzir-platform admin update-workspace <workspace-id> --owner-namespace=team --owner-id=<owner-id>
```
