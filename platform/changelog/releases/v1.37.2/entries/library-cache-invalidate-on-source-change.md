---
title: Refresh the library after changing a source
type: bugfix
authors:
  - gitryder
created: 2026-07-20T10:58:54.000000Z
---

Adding, removing, or updating a library source now updates the packages shown
on a node's library page right away. Previously the page kept showing the old
set of packages until the cached data expired or you refreshed manually.
