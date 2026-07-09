---
title: Multi-factor authentication support
type: feature
authors:
  - lava
  - avaq
created: 2026-07-08T08:55:36.811287Z
---

The platform now supports multi-factor authentication (MFA).

Individual users can secure their account from **Account settings**, where a new
**Multi-factor authentication** section lets them enroll an authenticator app
(TOTP) by scanning a QR code, remove existing methods, and generate a recovery
code to regain access if they lose their device.

Organization administrators can require MFA for everyone in their organization
by enabling **Require MFA** in the organization settings. Once enabled, members
must complete an MFA challenge before they can access their workspaces.

MFA enforcement is driven by your identity provider, so it requires
provider-side support. In particular, the identity provider must be able to add
a boolean `mfa` claim to the ID token after a successful factor challenge; the
platform relies on that claim to tell whether a user has completed MFA. For now
this is available only on our public cloud instance which uses Auth0, and the
platform must be started with
`TENZIR_PLATFORM_MFA_INTEGRATION=tenzir_auth0`. On all other deployments the
integration stays at its default value of `none` and MFA enforcement is
unavailable.
