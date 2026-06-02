---
title: "Fix being redirected to the login page when using header-based authentication"
type: bugfix
authors: [lava]
created: 2026-06-02T12:00:00Z
---

We fixed a regression introduced in v1.33.0 where users authenticating via the
`PRIVATE_JWT_FROM_HEADER` option were redirected to the login page (showing a
"Sign In" button) when opening a workspace, even though a valid JWT was supplied
in the configured header.

The workspace loader looked for the ID token in the session data, which is empty
for header-based authentication. It now reads the token from the configured
header, which is the authoritative source in that mode, so workspaces load
correctly again.
