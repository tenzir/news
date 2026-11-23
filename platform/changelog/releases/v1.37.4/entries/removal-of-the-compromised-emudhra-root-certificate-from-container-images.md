---
title: Removal of the compromised eMudhra root certificate from container images
type: bugfix
authors:
  - lava
created: 2026-10-29T14:29:09.793623Z
---

The Tenzir Platform services no longer trust certificates issued under the
`emSign ECC Root CA - G3` root. In October 2026, the private keys of eight
eMudhra intermediate CAs under this root were found to be compromised, which
would allow forging trusted TLS certificates for any domain. Mozilla and Google
have removed the root from their trust stores in response.

The platform API, gateway, UI, CLI, and SeaweedFS images now ship trust stores
without this root. Connections to services that use certificates from other
eMudhra roots are unaffected.

The images also include the dependency upgrades from the weekly container
scans:

- `pyjwt` to 2.15.1 and `urllib3` to 2.8.0 in the platform API, gateway, and
  CLI images
- `brace-expansion`, `devalue`, `shell-quote`, and `source-map-js` in the UI
  images
