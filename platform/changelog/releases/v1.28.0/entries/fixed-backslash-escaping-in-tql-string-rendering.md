---
title: Fixed backslash escaping in TQL string rendering
type: bugfix
author: lava
created: 2026-02-09T11:17:06.230703Z
---

We fixed a bug in the Inspector where strings containing backslashes were not displayed correctly. Backslashes were not being escaped in TQL string rendering. For example, a string like `Hello \World\` was previously rendered as `"Hello \World\"` instead of `"Hello \\World\\"`. The fix ensures backslashes are properly escaped when displayed.
