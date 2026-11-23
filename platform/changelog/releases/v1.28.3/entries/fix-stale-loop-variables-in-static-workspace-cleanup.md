---
title: Fix stale loop variables in static workspace cleanup
type: bugfix
author: lava
created: 2026-02-17T15:15:11Z
---

Fixed a bug where the static workspace synchronization used stale loop
variables during cleanup, causing stale workspaces to persist and the last
configured workspace to be incorrectly deleted.
