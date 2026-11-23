---
title: Azure managed identity for Key Vault secret stores
type: feature
authors:
  - tobim
created: 2026-08-13T12:35:50.613529Z
---

Azure Key Vault secret stores can now authenticate with a managed identity instead of a client secret:

```sh
tenzir-platform secret store add azure \
  --vault-url=https://example.vault.azure.net \
  --managed-identity \
  --workspace=t-example1
```

Platform administrators can use `--managed-identity-client-id` to select a user-assigned identity. Requiring administrator access prevents workspace members from binding arbitrary deployment identities to their workspace while avoiding a long-lived service-principal secret in the workspace configuration.
