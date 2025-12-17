---
title: "Update the secret store CLI interface to align with the Platform API"
type: bugfix
author: lava
created: 2025-12-17T13:24:10Z
pr: 131
---

The Tenzir Platform CLI was calling an outdated version of the secret store API, leading to unintended 404 errors. The CLI has been updated to use the latest version now.
