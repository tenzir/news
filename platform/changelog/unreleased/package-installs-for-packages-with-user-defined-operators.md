---
title: Package installs for packages with user-defined operators
type: bugfix
author: gitryder
created: 2026-03-17T13:59:38.745596Z
---

Packages containing user-defined operators can again be installed through the
platform. Previously, installing such packages failed because the operator
arguments were serialized incorrectly. This only affected installs through the
platform UI—command-line package installs were not impacted.
