---
title: "Add support for passing multiple issuer URLs"
type: feature
author: lava
created: 2025-12-17T13:24:10Z
---

The Tenzir Platform can now accept JWTs from multiple independent issuers. This is useful in situations where the CLI and UI users are served by two different OIDC providers.

To configure multiple OIDC providers, set the `TENZIR_PLATFORM_OIDC_TRUSTED_AUDIENCES` environment variable in your `.env` file to a list of issuer configurations:

```dotenv
TENZIR_PLATFORM_OIDC_TRUSTED_AUDIENCES='[{"issuer": "https://accounts.google.com", "audiences": ["audience1"]}, {"issuer": "https://cloud.google.com/iap", "audiences": ["audience2", "audience3"]}]'
```

Note that the previous way of setting a single JSON object with `issuer` and `audiences` keys for this variable is still supported, so no change is required
if you only want to use a single issuer.
