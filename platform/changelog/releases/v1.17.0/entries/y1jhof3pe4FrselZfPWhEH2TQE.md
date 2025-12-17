---
title: "Custom OIDC sign-in request params"
type: change
author: tobim
created: 2025-12-17T13:24:10Z
---

You can now use the environment variable `EXTRA_OIDC_REQUEST_PARAMS` to set custom query parameters with the sign-in requests that get sent to the OIDC provider. This is useful for configuring the endpoint's behavior through provider specific options.
