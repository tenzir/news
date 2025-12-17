---
title: "Print better error message for audience mismatch"
type: change
author: lava
created: 2025-12-17T13:24:10Z
---

The error message emitted by the platform on an audience mismatch in a supplied JWT now mentions the expected and provided audiences. (unless the provided audience contains non-url-safe characters)
