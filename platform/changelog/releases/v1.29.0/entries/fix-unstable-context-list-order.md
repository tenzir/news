---
title: Fix unstable context list order
type: bugfix
author: gitryder
created: 2026-02-18T08:55:40.318063Z
---

We fixed an issue where the context list could appear in a random order when no search was active, causing items to jump around. The list now uses a stable alphabetical order so it stays consistent and easier to interact with.
