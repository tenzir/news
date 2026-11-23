This release adds the ability to sort events by time in the Stream view, cycling between newest-first, oldest-first, and off. It also fixes the Insights tab freezing on large pipelines and upgrades dependencies to address known security vulnerabilities.

## 🚀 Features

### Right-click actions in the Explorer

You can now right-click a field name or value in the Explorer table to filter, sort, aggregate, or reshape your results. Actions like Equals, Not equals, Greater than, Contains, Starts with, Top values, Rare values, and Count values are appended to the editor as TQL, so common queries can be built by clicking instead of typing.

Timestamps get extra options for filtering around the clicked value, with windows of 5 minutes, 1 hour, and 1 day before, after, or on either side.

*By @gitryder.*

### Sort events by time in the Stream view

You can now sort events by time in the Stream view. The control cycles between newest first, oldest first, and off, and is disabled when no timestamp field is detected in the data. Your sorting preference is remembered between sessions.

*By @gitryder.*

## 🔧 Changes

### Return a dedicated error when a user key expires

When a `X-Tenzir-UserKey` has expired, the platform now returns a dedicated `403` response with the detail `User key expired`, instead of the generic `403 Invalid API Key: X-Tenzir-UserKey expired` error. This lets clients reliably detect the expired-key case and trigger a re-authentication flow.

*By @lava.*

## 🐞 Bug fixes

### Fix actions on the account, org, and invite pages failing after the page was open for 15 minutes

We fixed an issue where actions on the account, organization, and invitation pages would fail if the page had been open for more than 15 minutes. The following operations now automatically refresh the user key when needed: changing account details, updating passwords, deleting accounts, creating and updating organizations, managing organization invitations, and deleting organizations.

*By @avaq.*

### Fix duration round-trip in TQL queries

Negative multi-part durations no longer drift when copied or embedded into a TQL query. Previously a duration like `-(19min + 12.636s)` was rendered as `-19min + 12.636s`, which the parser read as `-1127.364s` instead of the original `-1152.636s` — off by twice the seconds component. The sign now distributes across every term (`-19min - 12.636s`) so the value round-trips cleanly.

Duration rendering also picks up a clearer split between display and query forms. The table cells, chart tooltips, and chart axis labels show durations in a human-readable form like `1h 30min 5.000s`. The inspector and any context that needs to round-trip the value back into a query show the TQL-valid arithmetic form like `1h + 30min + 5.000000000s`.

*By @gitryder.*

### Fix Insights tab freezing on large pipelines

We fixed an issue where the Insights tab became unresponsive and flickered on pipelines with many operators. The table now renders smoothly and stays interactive while showing live metrics.

*By @gitryder.*

### Insights tab for v6 release candidates

The Insights tab now always shows data for the release candidates of Tenzir Node v6, even if no `// neo` comment is present.

*By @jachris.*
