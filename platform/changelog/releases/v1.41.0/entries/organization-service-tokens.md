---
title: Organization service tokens
type: feature
authors:
  - lava
created: 2026-10-05T12:56:46.984067Z
---

Organization admins can now create service tokens on the organization settings
page. A service token is a long-lived machine credential with an organization
role and an optional expiry, intended for automation such as the Terraform
provider or CI jobs.

Exchange a token for a short-lived user key with
`POST /user/service-token/authenticate`, either account-level or scoped to a
workspace owned by the organization. The key acts with the token's role inside
the organization and never outlives the token. Admins can revoke a token at any
time. Revoking a token immediately invalidates all keys issued from it.
