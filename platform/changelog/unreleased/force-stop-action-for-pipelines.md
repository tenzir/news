---
title: Force stop action for pipelines
type: feature
authors:
  - aljazerzen
  - claude
created: 2026-07-13T08:43:45.694243Z
---

The pipeline menu now offers a **Force stop** action that terminates a running,
paused, or stopping pipeline immediately instead of waiting for it to drain
in-flight data.

Use **Force stop** when a pipeline is taking too long to stop — for instance,
when it is stuck in the `stopping` state. The action appears only for nodes that
support it.
