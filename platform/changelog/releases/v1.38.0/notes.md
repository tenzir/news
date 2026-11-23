This release makes telemetry collection opt-in: telemetry is only collected for users who have explicitly consented via their Account page. The pipeline list search box now also matches on pipeline ID, so you can paste an ID to jump straight to a pipeline. Additionally, this release fixes two MFA-related UI errors and updates all container images to resolve known vulnerabilities in their dependencies.

## 🚀 Features

### Search pipelines by ID

The pipeline list search box now matches on pipeline ID in addition to name and definition. You can paste or type a pipeline ID to jump straight to it, instead of having to look up its name first.

*By @zedoraps.*

## 🔧 Changes

### Gate telemetry collection behind user-consent

Users can now opt in explicitly to telemetry collection. This is done through the Account page. Telemetry is only collected for users who have opted in.

This applies to all Platform deployments where telemetry has been enabled. Notably, telemetry has now also been enabled on app.tenzir.com.

*By @avaq.*

## 🐞 Bug fixes

### Container image dependency security fixes

All of the platform's container images have been updated to resolve known vulnerabilities in their application-level dependencies. The changes are transparent at runtime and require no configuration or data migration.

The `tenzir-platform` image upgrades `pyjwt` from 2.12.1 to 2.13.0, resolving CVE-2026-48522, CVE-2026-48523, CVE-2026-48524, CVE-2026-48525, and CVE-2026-48526. It also picks up `setuptools` 83.0.0 for CVE-2026-59890.

The `platform-api` and `platform-gateway` images upgrade the following Python dependencies:

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

*By @lava.*

### Fix error on org page after requiring MFA

After enabling "Require MFA" on an organization, when revisiting the organization page, the user would see an error instead of being redirected to the MFA Step Up page. This has now been fixed.

*By @avaq.*

### Fix MFA enrollment error being obscured

When enrolling in MFA, if something goes wrong the error is now shown under the form, instead of in a Toast that's partially obscured by the MFA enrollment wizard.

*By @avaq.*
