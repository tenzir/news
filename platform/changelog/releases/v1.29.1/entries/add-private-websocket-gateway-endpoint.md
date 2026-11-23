---
title: "Add PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT environment variable"
type: feature
authors: [lava]
created: 2026-03-10T14:00:00Z
---

The app container now supports a `PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT` environment variable that overrides the existing `PUBLIC_WEBSOCKET_GATEWAY_ENDPOINT` for calls in the app backend. This allows configuring different endpoints when the frontend and backend live in different networks.
