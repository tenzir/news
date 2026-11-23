---
title: "Return a dedicated error when a user key expires"
type: change
authors: [lava]
created: 2026-05-21T00:00:00Z
---

When a `X-Tenzir-UserKey` has expired, the platform now returns a dedicated `403` response with the detail `User key expired`, instead of the generic `403 Invalid API Key: X-Tenzir-UserKey expired` error. This lets clients reliably detect the expired-key case and trigger a re-authentication flow.
