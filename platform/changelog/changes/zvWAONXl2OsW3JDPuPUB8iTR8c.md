---
title: "Make log level configurable through environment"
type: feature
authors: lava
---

The log level of the Tenzir Platform API and the Tenzir Gateway can now be configured with the `TENZIR_PLATFORM_LOG_LEVEL` environment variable.

Possible values are `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. If not set, it defaults to `DEBUG` for backward compatibility.
