---
title: Custom library sources
type: feature
authors:
  - gitryder
created: 2026-07-09T12:09:46.000000Z
---

Organizations can now maintain their own package libraries.

From the organization settings page, an administrator can add up to 10 library
sources — public or private Git repositories — alongside the built-in Tenzir
Library, which is always available and does not count toward the limit. A
private source authenticates with a credential you provide; it is stored
securely and used only on the server, so it is never exposed to the browser.

The Library then shows packages from every configured source together, labels
each package with the source it came from, and lets you filter the view by
source.
