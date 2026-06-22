---
title: Explorer downloads on nodes using the legacy execution engine
type: bugfix
authors:
  - tobim
  - claude
prs:
  - 184
created: 2026-06-03T09:06:58.674152Z
---

Downloading results from the Explorer now works on Tenzir Nodes v6+ that are
configured to run pipelines on the legacy execution engine (`tenzir.neo:
false`). Previously, preparing the download failed on such nodes because the
pipeline that uploads the results relied on functionality that is only
available in the new execution engine. The download pipeline now always runs
on the new execution engine, regardless of the node's configuration.
