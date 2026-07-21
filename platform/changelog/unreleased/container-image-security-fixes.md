---
title: Container image security fixes
type: bugfix
authors:
  - lava
created: 2026-07-21T15:25:13.744874Z
---

Two of the platform's container images have been updated to resolve known
vulnerabilities. Both changes are transparent at runtime and require no
configuration or data migration.

The AWS Lambda image (`platform-api-aws`) no longer ships the unused
`setuptools`, `pip`, and `wheel` packaging tools in its runtime, resolving
CVE-2026-23949 (in `jaraco.context`) and shrinking the image's attack surface.

The SeaweedFS image (`tenzir-seaweed`) moves from SeaweedFS 4.23 to 4.40,
rebuilding the bundled `weed` binary with an updated Go toolchain and modules.
This clears the following vulnerabilities that could not be fixed by a
platform-side dependency bump:

- Go standard library: CVE-2026-33811, CVE-2026-39822, CVE-2026-42499,
  CVE-2026-39836, CVE-2026-39820, CVE-2026-42504, CVE-2026-33814
- `golang.org/x/crypto`: CVE-2026-39833, CVE-2026-46597, CVE-2026-39835,
  CVE-2026-46595, CVE-2026-42508, CVE-2026-39829, CVE-2026-39832,
  CVE-2026-39834, CVE-2026-39831, CVE-2026-39830, CVE-2026-39828
- `golang.org/x/image`: CVE-2026-46602, CVE-2026-46601, CVE-2026-46604,
  CVE-2026-33813, CVE-2026-46599
- `golang.org/x/net`: CVE-2026-39821
- `go-git/go-billy`: CVE-2026-44973
