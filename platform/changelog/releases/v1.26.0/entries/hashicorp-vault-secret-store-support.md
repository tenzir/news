---
title: HashiCorp Vault secret store support
type: feature
authors:
  - lava
  - mavam
created: 2025-12-23T13:01:17.76542Z
---

You can now use HashiCorp Vault as an external secret store for your workspaces.
The integration supports token and AppRole authentication methods, and works
with the KV v2 secrets engine. Add a Vault secret store via the CLI:

```bash
tenzir-platform secret store add vault \
  --address=https://vault.example.com \
  --mount=secret \
  --token=<token>
```

Or with AppRole authentication (recommended for production):

```bash
tenzir-platform secret store add vault \
  --address=https://vault.example.com \
  --mount=secret \
  --role-id=<id> --secret-id=<id>
```

The `--mount` option specifies the path to a KV v2 secrets engine. For Vault
Enterprise, use `--namespace` to specify the namespace. Vault secrets are
returned as JSON by default. Append a `:key` suffix to retrieve a specific field
as a string, for example, `secret("database:password")`.
