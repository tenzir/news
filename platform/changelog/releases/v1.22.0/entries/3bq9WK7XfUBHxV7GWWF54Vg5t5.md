---
title: "Add optional jwks_uri configuration for OIDC issuers"
type: feature
author: lava
created: 2025-12-17T13:24:10Z
---

The new optional `jwks_uri` field for the `TENZIR_PLATFORM_OIDC_TRUSTED_AUDIENCES` configuration can be used to support for identity providers that don't publish discovery documents.

For example, when using Google IAP, a configuration value like this can be used:

```
{
    "issuer": "https://cloud.google.com/iap",
    "audiences": ["your-audience"],
    "jwks_uri": "https://www.gstatic.com/iap/verify/public_key-jwk"
}
```
