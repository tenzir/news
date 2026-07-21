This release rebuilds the platform's AWS Lambda and SeaweedFS container images to clear a broad set of known CVEs, and fixes unexpected logouts when KeyCloak is the identity provider on the Sovereign Edition. The Library also refreshes its package view immediately after source changes and surfaces install errors inline.

## 🔧 Changes

### Drop support for legacy session storage format

We no longer support user sessions that were created by Platform versions before 1.34.0.

⚠️ If you're updating from a version prior to 1.34.0, consider updating to 1.37.0 first and allowing users to refresh their sessions before upgrading to this version. Otherwise, users must clear their browser cache or they'll receive a server error saying "Failed to establish authenticated session".

*By @avaq.*

### Marketplace template moves off App Runner

The AWS Marketplace CloudFormation template now deploys the platform UI as an ECS Fargate service behind the existing gateway load balancer, using host-based routing for `ui.<domain>`. Previously the UI ran on AWS App Runner, which is closed to new customers since April 2026 and caused deployments into fresh AWS accounts to fail.

Existing stacks are unaffected; the change applies to new deployments of the template. The UI's security group is also tightened to only accept traffic from the load balancer instead of the whole VPC.

*By @lava.*

### Robust package data handling in the Library

The Library now validates all package data against schemas that mirror the node's actual output, covering every install state and configuration shape a node can report. A single unexpected package can no longer block package management.

*By @gitryder.*

## 🐞 Bug fixes

### Container image security fixes

Two of the platform's container images have been updated to resolve known vulnerabilities. Both changes are transparent at runtime and require no configuration or data migration.

The AWS Lambda image (`platform-api-aws`) no longer ships the unused `setuptools`, `pip`, and `wheel` packaging tools in its runtime, resolving CVE-2026-23949 (in `jaraco.context`) and shrinking the image's attack surface.

The SeaweedFS image (`tenzir-seaweed`) moves from SeaweedFS 4.23 to 4.40, rebuilding the bundled `weed` binary with an updated Go toolchain and modules. This clears the following vulnerabilities that could not be fixed by a platform-side dependency bump:

- Go standard library: CVE-2026-33811, CVE-2026-39822, CVE-2026-42499, CVE-2026-39836, CVE-2026-39820, CVE-2026-42504, CVE-2026-33814
- `golang.org/x/crypto`: CVE-2026-39833, CVE-2026-46597, CVE-2026-39835, CVE-2026-46595, CVE-2026-42508, CVE-2026-39829, CVE-2026-39832, CVE-2026-39834, CVE-2026-39831, CVE-2026-39830, CVE-2026-39828
- `golang.org/x/image`: CVE-2026-46602, CVE-2026-46601, CVE-2026-46604, CVE-2026-33813, CVE-2026-46599
- `golang.org/x/net`: CVE-2026-39821
- `go-git/go-billy`: CVE-2026-44973

*By @lava.*

### Fix unexpected logouts under KeyCloak

We fixed an issue where user sessions would end unexpectedly when KeyCloak was the configured identity provider for the Sovereign Edition of the Platform.

*By @avaq.*

### Refresh the library after changing a source

Adding, removing, or updating a library source now updates the packages shown on a node's library page right away. Previously the page kept showing the old set of packages until the cached data expired or you refreshed manually.

*By @gitryder.*

### Show package install errors inline

When installing a library package fails, the install dialog now shows the actual errors and warnings inline, so you can see them at a glance instead of vague toasts.

*By @gitryder.*
