---
title: Robust package data handling in the Library
type: change
authors:
  - gitryder
created: 2026-07-16T10:20:33.000000Z
---

The Library now validates all package data against schemas that mirror the
node's actual output, covering every install state and configuration shape a
node can report. A single unexpected package can no longer block package
management.
