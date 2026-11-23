This release adds machine credentials for organizations: federated credentials let workloads such as GitHub Actions runs authenticate with their own OIDC tokens instead of a stored secret, and service tokens cover automation such as the Terraform provider. Revoking either credential immediately invalidates every key issued from it.

## 🚀 Features

### Federated credentials for workload identity

Organization admins can now add federated credentials on the organization settings page. A federated credential lets an external workload, such as a GitHub Actions run, authenticate with the platform using the OIDC token its own identity provider issues, so no long-lived secret has to be stored in CI.

Each credential names a trusted issuer, a required audience, and one or more claims that must match exactly, for example `repository` and `ref` for GitHub Actions. Matching workloads act as a member of the organization with the role configured on the credential.

Exchange the external token for a short-lived user key with `POST /user/federated/authenticate`, either account-level or scoped to a workspace owned by the organization:

```json
{
  "id_token": "eyJ...",
  "organization_id": "org-abc123",
  "tenant_id": "t-abc123"
}
```

Admins can remove a credential at any time, after which workloads can no longer exchange tokens for it. Removing a credential immediately invalidates all keys issued from it.

The platform only fetches signing keys from issuers that resolve to public addresses. For self-hosted deployments with an internal identity provider, such as GitLab or Keycloak on a private network, set `TENZIR_PLATFORM_FEDERATION_PRIVATE_ISSUER_HOSTS` to a comma-separated list of the issuer hostnames to allow, for example `gitlab.internal,keycloak.corp`.

*By @lava.*

### Organization service tokens

Organization admins can now create service tokens on the organization settings page. A service token is a long-lived machine credential with an organization role and an optional expiry, intended for automation such as the Terraform provider or CI jobs.

Exchange a token for a short-lived user key with `POST /user/service-token/authenticate`, either account-level or scoped to a workspace owned by the organization. The key acts with the token's role inside the organization and never outlives the token. Admins can revoke a token at any time. Revoking a token immediately invalidates all keys issued from it.

*By @lava.*
