Azure Key Vault secret stores can now authenticate with a managed identity, which removes the need to keep a long-lived client secret in the workspace configuration. This release also adds a new flag for JSON output to the workspace creation CLI.

## 🚀 Features

### Azure managed identity for Key Vault secret stores

Azure Key Vault secret stores can now authenticate with a managed identity instead of a client secret:

```sh
tenzir-platform secret store add azure \
  --vault-url=https://example.vault.azure.net \
  --managed-identity \
  --workspace=t-example1
```

Platform administrators can use `--managed-identity-client-id` to select a user-assigned identity. Requiring administrator access prevents workspace members from binding arbitrary deployment identities to their workspace while avoiding a long-lived service-principal secret in the workspace configuration.

*By @tobim.*

### JSON output for workspace creation

`tenzir-platform admin create-workspace` gained a `--json` flag, so scripts can read the id of the new workspace without parsing a human-readable message:

```sh
tenzir-platform admin create-workspace team my-team --json
```

*By @lava.*

## 🔧 Changes

### Force stopping Explorer pipelines

Explorer now force stops running pipelines when supported.

*By @aljazerzen.*

## 🐞 Bug fixes

### Workspace creation validates the owner

`tenzir-platform admin create-workspace` now rejects an owner that the platform cannot resolve, instead of creating a workspace that fails to open later. The `organization` namespace requires an organization that exists in the platform, with an `org-xxxxxxxx` id; use `team` for a free-form owner id. `admin update-workspace` already applied this check.

Opening a workspace whose owning organization no longer exists now fails with a 409 that names the problem, rather than an opaque 500. Repair it by reassigning the owner:

```sh
tenzir-platform admin update-workspace <workspace-id> --owner-namespace=team --owner-id=<owner-id>
```

*By @lava.*
