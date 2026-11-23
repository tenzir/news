---
title: Security and performance improvements
type: change
author: avaq
created: 2026-06-04T00:00:00.000000Z
---

We overhauled the frontend's login and session handling. Compared to the previous release:

- OIDC provider metadata is now discovered once at application startup instead of on every session refresh, shaving the round-trip cost off many requests.
- User keys (access tokens) are now always cached server-side in the user's session, alleviating the cost of obtaining new access tokens for many requests.
- Users of Platform deployments using header-based auth (like Google IAP) are now also granted a login session, allowing them to benefit from session based caches. This means that access tokens and user metadata is no longer fetched externally on every request, potentially saving multiple round trips worth of time with each request.
- Session IDs no longer leak to JavaScript, and are solely kept inside secure HTTP cookies.
