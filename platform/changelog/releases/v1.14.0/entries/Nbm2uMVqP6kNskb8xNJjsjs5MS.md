---
title: "Fix false 'deployed pipeline failed' toasts"
type: bugfix
created: 2025-12-17T13:24:10Z
---

We no longer show 'deployed pipeline failed' toasts for pipelines that
weren't actually deployed, but were running via the Explorer,
Dashboard, or other sources like that.
