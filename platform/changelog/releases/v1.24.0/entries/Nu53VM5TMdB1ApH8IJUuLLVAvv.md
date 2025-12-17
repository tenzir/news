---
title: "Add option to require client certificates for the Tenzir Gateway"
type: feature
author: lava
created: 2025-12-17T13:24:10Z
---

Add a new TENZIR_PLATFORM_REQUIRE_CLIENT_CERTS environment variable that, when set to true, requires connecting clients to present a valid certificate signed by one of the CAs specified in TLS_CAFILE.
