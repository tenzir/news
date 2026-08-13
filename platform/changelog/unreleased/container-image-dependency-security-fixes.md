---
title: Container image dependency security fixes
type: bugfix
authors:
  - lava
created: 2026-08-13T09:35:15.041823Z
---

The platform's container images have been updated to resolve vulnerabilities
found in the weekly container scan. The changes are transparent at runtime and
require no configuration or data migration.

The `platform-api` and `platform-gateway` images upgrade the following Python
dependencies:

- `aiohttp` 3.14.1 to 3.14.3: CVE-2026-69244
- `cryptography` 49.0.0 to 50.0.0: CVE-2026-69247

The `tenzir-platform` image also picks up `cryptography` 50.0.0.

The `tenzir-seaweed` image moves to the upstream `seaweedfs` 4.41 base image,
which is built against a `google.golang.org/grpc` release that resolves
GHSA-hrxh-6v49-42gf.
