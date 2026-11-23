---
title: Container image dependency security fixes
type: bugfix
authors:
  - lava
created: 2026-09-08T12:46:18.368258Z
---

The `platform-ui` and `platform-ui-aws` container images have been updated to
resolve vulnerabilities found in the weekly container scan. The changes are
transparent at runtime and require no configuration or data migration.

The frontend upgrades the following Node dependencies:

- `fast-uri` 4.1.2 to 4.1.4: CVE-2026-75899, CVE-2026-75931, CVE-2026-76172,
  CVE-2026-75975
- `postcss` 8.5.26 to 8.5.28, which moves its nested `nanoid` copy from
  3.3.17 to 3.3.18: CVE-2026-67213
