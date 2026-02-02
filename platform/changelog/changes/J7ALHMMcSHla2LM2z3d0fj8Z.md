---
title: "User key expiration handling"
type: bugfix
authors: lava
---

Fixed a bug that could leave users with a stale user key in their session, causing authentication failures. The platform now proactively checks for expired user keys and refreshes them automatically.
