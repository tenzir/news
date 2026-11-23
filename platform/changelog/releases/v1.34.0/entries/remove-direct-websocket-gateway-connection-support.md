---
title: Remove direct Websocket Gateway connection support
type: change
author: avaq
created: 2026-06-22T08:01:54.928Z
---

The Platform configuration variable `PUBLIC_USE_INTERNAL_WS_PROXY` no longer
has any effect. The platform now behaves as though this setting is always
enabled: All connections to the Websocket Gateway are now proxied through the
App Server ("BFF").

The `PUBLIC_WEBSOCKET_GATEWAY_ENDPOINT` variable that used to configure the
direct Gateway connection is now used as a fallback for when the
`PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT` isn't defined.
