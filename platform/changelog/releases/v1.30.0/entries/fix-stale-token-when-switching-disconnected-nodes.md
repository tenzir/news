---
title: 'Fix stale token when switching disconnected nodes'
type: bugfix
author: gitryder
created: 2026-04-01T09:46:47.136479Z
---

We fixed an issue where the connection token shown in the "Connect node" dialog did not update when switching between different disconnected nodes. The token now correctly refreshes for the selected node.
