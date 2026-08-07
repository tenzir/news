---
title: Container image dependency security fixes
type: bugfix
authors:
  - lava
created: 2026-08-06T12:54:42.282732Z
---

All of the platform's container images have been updated to resolve known
vulnerabilities in their application-level dependencies. The changes are
transparent at runtime and require no configuration or data migration.

The `tenzir-platform` image upgrades `pyjwt` from 2.12.1 to 2.13.0, resolving
CVE-2026-48522, CVE-2026-48523, CVE-2026-48524, CVE-2026-48525, and
CVE-2026-48526. It also picks up `setuptools` 83.0.0 for CVE-2026-59890.

The `platform-api` and `platform-gateway` images upgrade the following Python
dependencies:

- `pynacl` 1.6.1 to 1.6.2: CVE-2025-69277
- `requests` 2.32.5 to 2.34.2: CVE-2026-25645
- `python-dotenv` 1.2.1 to 1.2.2: CVE-2026-28684
- `ecdsa` 0.19.1 to 0.19.2: CVE-2026-33936
- `jwcrypto` 1.5.6 to 1.5.8: CVE-2026-39373
- `idna` 3.11 to 3.18: CVE-2026-45409
- `pydantic-settings` 2.12.0 to 2.14.2: GHSA-4xgf-cpjx-pc3j

The `platform-ui` images upgrade these JavaScript dependencies:

- `@sveltejs/kit` 2.69.0 to 2.70.2: GHSA-866w-xmhq-wj7x, GHSA-wqjv-9729-c5q2
- `cookie` 0.6.0 to 0.7.2: CVE-2024-47764
- `tar` 7.5.19 to 7.5.22: GHSA-r292-9mhp-454m
- `@opentelemetry/core`, no longer resolving to the affected 2.7.1: CVE-2026-54285
