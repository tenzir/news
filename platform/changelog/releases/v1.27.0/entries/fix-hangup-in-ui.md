---
title: Fix hangup in UI
type: bugfix
author: lava
created: 2026-01-26T12:11:04.746925Z
---

Fixed a potential infinite hang in the Tenzir UI that could
be triggered by a rare race condition where the Tenzir Node
returned duplicate pipeline ids.
