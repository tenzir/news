---
title: Library tab no longer hangs after interrupted load
type: bugfix
authors:
  - Zedoraps
  - claude
created: 2026-06-16T22:48:35.092604Z
---

The Library tab now loads reliably after a previous attempt was
interrupted by a page reload or navigation. Previously the tab could
get stuck at "Loading…" indefinitely until the browser session was
cleared.
