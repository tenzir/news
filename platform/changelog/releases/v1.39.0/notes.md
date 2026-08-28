This release makes working with data in the Explorer easier: browse stored schemas, use field actions in more places, preview value frequencies, plus new view options in the Stream view and custom time field selection. It also ships various fixes and security updates under the hood.

## 🚀 Features

### Display options for the Explorer Stream view

You can now tailor the Explorer's Stream view to the fields you need. Open **Fields** to show or hide fields across all schema variants, or Shift-click a field to show it exclusively.

The Stream toolbar also includes controls to wrap long values and hide field names, making dense events easier to scan. Field selections affect only the collapsed overview; expanded events always show the complete event with field names. Field selections reset with each pipeline run, while line wrapping and field-name visibility persist.

*By @zedoraps.*

### Field actions and cached value insights in the Explorer

You can now right-click fields and values in collapsed or expanded Explorer Stream events, as well as in the Table and Inspector views, to build filters and field operations without writing them manually. Available actions depend on the field and value, including equality and comparison filters, string matching, timestamp windows, field selection, and field removal. You can also hide or show a non-timestamp field in the collapsed Stream overview and the Table view.

Hover over **Top values**, **Rare values**, or **Count values** to preview value frequencies from the current Explorer cache without replacing your pipeline. The preview respects the active result schema or Stream schema filters and becomes available once the run has finished; while a run still streams, the menu offers actions that add the equivalent step to your pipeline instead. Select **Open as query** to continue the analysis as a standalone query.

*By @zedoraps.*

### Node schema browsing in the Explorer

You can now browse stored schemas and their fields from the Explorer's **Stored data** tab, even before you run a pipeline. Each schema shows the number of stored events, its schema variants, and its available fields. Search by a schema or field name, add an `@name` filter to the current pipeline, or open the stored events for a schema directly.

The data pane keeps node-wide stored schemas separate from the schemas in your current results. When you run a pipeline, the pane switches to **Results** automatically.

*By @zedoraps.*

### Timestamp field selection for Explorer time ranges

The Explorer time picker now lets you choose the timestamp field used for time ranges. Select `_ts`, `ts`, `timestamp`, or `time`, or enter a custom field name. Quick presets and custom relative or absolute ranges then update the matching field in your pipeline while preserving unrelated predicates.

*By @zedoraps.*

## 🔧 Changes

### Python 3.13 for the platform container images

The AWS Lambda container image for the platform API has moved from the `python:3.10` base image to `python:3.13`. The 3.10 image is built on Amazon Linux 2, which is discontinued and no longer receives security updates; the 3.13 image is built on Amazon Linux 2023. This also removes `setuptools` from the image entirely, since the Amazon Linux 2023 images no longer preinstall it.

The `platform-api` and `platform-gateway` images move from Python 3.10 to Python 3.13 as well, ahead of Python 3.10 reaching end of life upstream in October 2026. Both remain based on Debian 13.

The `tenzir-platform` CLI image moves from Python 3.11 to Python 3.13, so all of the platform's Python images are now on the same version. Because the Debian slim images stopped preinstalling `setuptools` after 3.11, this also resolves CVE-2026-23949, which was reported against the `jaraco.context` copy vendored into the base image's `setuptools`.

These changes are transparent at runtime and require no configuration or data migration.

*By @lava.*

## 🐞 Bug fixes

### Container image dependency security fixes

The platform's container images have been updated to resolve vulnerabilities found in the weekly container scan. The changes are transparent at runtime and require no configuration or data migration.

The `platform-api` and `platform-gateway` images upgrade the following Python dependencies:

- `aiohttp` 3.14.1 to 3.14.3: CVE-2026-69244
- `cryptography` 49.0.0 to 50.0.0: CVE-2026-69247

The `tenzir-platform` image also picks up `cryptography` 50.0.0.

The `tenzir-seaweed` image moves to the upstream `seaweedfs` 4.41 base image, which is built against a `google.golang.org/grpc` release that resolves GHSA-hrxh-6v49-42gf.

*By @lava.*

### Fix MFA users losing workspace access mid-session

Fixed an issue where users who signed in with multi-factor authentication would, after some time, lose access to workspaces that require MFA and could no longer manage their authenticators until they signed out and back in.

*By @gitryder.*
