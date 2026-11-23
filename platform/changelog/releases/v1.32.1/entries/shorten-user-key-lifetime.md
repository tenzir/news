---
title: "Shorten default user key lifetime"
type: change
authors: [lava]
created: 2026-05-13T12:00:00Z
---

We reduced the default lifetime of user keys from one week to 15 minutes. Sessions transparently refresh, so this is invisible in normal use, but shortens the window in which a leaked key could be reused.
