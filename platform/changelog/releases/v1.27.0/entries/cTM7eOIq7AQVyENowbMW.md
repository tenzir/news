---
title: "Store authentication tokens server-side"
type: feature
author: lava
created: 2026-01-20T12:08:58Z
---

Authentication tokens (idToken and userKey) are now stored in the server-side session database instead of browser cookies. This improves security by keeping sensitive tokens accessible only via the session cookie identifier, preventing direct client-side access to authentication credentials.
