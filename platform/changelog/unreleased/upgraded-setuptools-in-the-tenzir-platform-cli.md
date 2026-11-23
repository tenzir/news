---
title: Upgraded setuptools in the Tenzir Platform CLI
type: bugfix
authors:
  - lava
created: 2026-10-26T15:53:33.459298Z
---

The Tenzir Platform CLI now requires `setuptools` 84.1.0 or later, which fixes a low-severity path traversal on Windows during legacy wheel installation (GHSA-xmj3-9gf7-h52w).
