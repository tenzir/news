---
title: Sporadic 502 errors behind load balancers
type: bugfix
authors:
  - lava
created: 2026-07-09T16:15:52.445932Z
---

The platform's HTTP servers now keep idle connections open longer than
typical load balancer idle timeouts. Previously, a load balancer could reuse
a pooled connection that the platform had already closed, causing requests to
sporadically fail with 502 errors.

In addition, when the list of connected nodes cannot be retrieved, the API
now returns the actual error reported by the websocket gateway instead of a
generic parsing failure, and requests that were aborted by the client no
longer produce error-level noise in the app server logs.
