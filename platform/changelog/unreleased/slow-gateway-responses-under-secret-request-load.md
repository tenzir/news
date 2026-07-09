---
title: Slow gateway responses under secret request load
type: bugfix
authors:
  - lava
created: 2026-07-09T18:58:10Z
---

The websocket gateway is now significantly faster in deployments with
many secret requests. Previously, heavy secret request traffic could slow
down all gateway responses by several seconds.
