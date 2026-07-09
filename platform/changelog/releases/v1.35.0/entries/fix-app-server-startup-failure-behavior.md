---
title: Fix App-Server startup failure behavior
type: bugfix
author: Avaq
prs:
  - 241
created: 2026-07-02T14:11:24.953Z
---

Fixes an issue where the App Server can sometimes start up in a broken state
and respond to every request with an error until it is restarted.

Now, if the App Server encounters an error during startup that it could not
recover from, it immediately shuts down again, allowing automated restarts to
take place.
