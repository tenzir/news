---
title: "Fix token generation for static workspaces"
type: bugfix
author: lava
created: 2025-12-17T13:24:10Z
---

Fixed a bug that caused static workspace tokens to include stray  b'...' characters, resulting in invalid node tokens.
