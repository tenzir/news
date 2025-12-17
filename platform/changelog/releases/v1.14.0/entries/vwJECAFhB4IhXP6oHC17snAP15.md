---
title: "Secret data type display"
type: feature
author: dit7ya
created: 2025-12-17T13:24:10Z
---

Secret data types now display as `<secret>` in the platform, for example,
in the explorer table. A tooltip explains that secret values are not transported
to the platform for security reasons.

In TQL exports (such as copy to clipboard), secrets are copied as `null`.
