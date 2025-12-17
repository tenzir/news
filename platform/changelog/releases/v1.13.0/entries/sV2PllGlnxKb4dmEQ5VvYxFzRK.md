---
title: "Better error handling in the Tenzir Platform CLI"
type: feature
author: lava
created: 2025-12-17T13:24:10Z
pr: 107
---

When encountering authentication errors, the Tenzir Platform CLI now exits with a nice error message instead of printing a raw stacktrace:

```sh
$ TENZIR_PLATFORM_CLI_ID_TOKEN=xxxx tenzir-platform workspace list
Error: Invalid JWT
  while validating TENZIR_PLATFORM_CLI_ID_TOKEN
(hint) upstream error: Not enough segments
```
