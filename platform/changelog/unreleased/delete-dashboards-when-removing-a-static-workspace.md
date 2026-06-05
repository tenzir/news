---
title: Delete dashboards when removing a static workspace
type: bugfix
author: gitryder
created: 2026-06-04T09:57:07.537451Z
---

Previously, when a workspace was removed from the static configuration file, dashboards that users had created within that workspace were left behind as orphaned records in the database. These could resurface if a new workspace later reused the same workspace ID. Removing a static workspace now also deletes these user-created dashboards.
