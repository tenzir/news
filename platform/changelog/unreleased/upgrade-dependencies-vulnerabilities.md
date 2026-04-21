---
title: "Upgrade dependencies to fix known vulnerabilities"
type: bugfix
authors: [lava]
created: 2026-04-21T10:30:00Z
---

We upgraded frontend, backend, and CLI dependencies and bumped the tenzir-seaweed base image to address known vulnerabilities reported by our container scanner.

Notable dependency bumps:

- `drizzle-orm` to 0.45.2 (CVE-2026-39356)
- `tar` to 7.5.8 (CVE-2021-32803, CVE-2026-26960, CVE-2021-37712, CVE-2021-37713)
- `tar-fs` to 3.0.7 (CVE-2024-12905)
- `ws` to 8.17.1 (CVE-2024-37890)
- `elliptic` to 6.5.7 (CVE-2024-42461, CVE-2020-13822, CVE-2024-48949)
- `cryptography` to 46.0.7 (CVE-2026-39892)
- `rollup` to 4.59.0 (CVE-2026-27606)
- `vite` to 7.3.2 (CVE-2026-39363)
- `ajv` to 8.18.0 (CVE-2025-69873)
- `defu` to 6.1.5 (CVE-2026-35209)
- `picomatch` to 4.0.4 (CVE-2026-33671)
- `http-cache-semantics` to 4.1.1 (CVE-2022-25881)
- `glob` to 11.1.0 (CVE-2025-64756)
- `glob-parent` to 5.1.2 (CVE-2020-28469)
- `cipher-base` to 1.0.5 (CVE-2025-9287)
- `trim-newlines` to 4.0.1 (CVE-2021-33623)
- `y18n` to 5.0.5 (CVE-2020-7774)
- `kind-of` to 6.0.3 (CVE-2019-20149)
- `decode-uri-component` to 0.2.1 (CVE-2022-38900)
- `minimist` to 1.2.6 (CVE-2021-44906)
- `lodash` to 4.18.1 (CVE-2020-8203, CVE-2026-4800)
- `minimatch` to 3.0.5 (CVE-2022-3517)
- `ansi-regex` to 6.0.1 (CVE-2021-3807)
- `semver` to 7.7.1 (CVE-2022-25883)
- `normalize-url` to 6.0.1 (CVE-2021-33502)
- `ini` to 1.3.6 (CVE-2020-7788)

The tenzir-seaweed base image was bumped to 4.20 and Dockerfiles now run OS package upgrades, addressing CVE-2026-2673, CVE-2026-28388, CVE-2026-31790, CVE-2026-28390, CVE-2026-28389 (openssl), CVE-2026-40200 (musl), and CVE-2026-5201 (gdk-pixbuf).
