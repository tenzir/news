---
title: Prevent renaming a node to an empty string
type: bugfix
author: gitryder
created: 2026-04-01T09:52:41.229656Z
---

We fixed an issue where a node could be renamed to an empty string, causing the app to malfunction. Node names are now properly validated, so empty or whitespace-only names are no longer allowed.
