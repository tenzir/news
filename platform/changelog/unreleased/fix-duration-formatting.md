---
title: Fix duration round-trip in TQL queries
type: bugfix
author: gitryder
created: 2026-05-21T00:00:00Z
---

Negative multi-part durations no longer drift when copied or embedded into a TQL query. Previously a duration like `-(19min + 12.636s)` was rendered as `-19min + 12.636s`, which the parser read as `-1127.364s` instead of the original `-1152.636s` — off by twice the seconds component. The sign now distributes across every term (`-19min - 12.636s`) so the value round-trips cleanly.

Duration rendering also picks up a clearer split between display and query forms. The table cells, chart tooltips, and chart axis labels show durations in a human-readable form like `1h 30min 5.000s`. The inspector and any context that needs to round-trip the value back into a query show the TQL-valid arithmetic form like `1h + 30min + 5.000000000s`.
