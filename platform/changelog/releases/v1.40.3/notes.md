This release removes the compromised `emSign ECC Root CA - G3` root certificate from the trust stores of all Tenzir Platform container images. It also fixes a bug where packages installed from the Library lost their shared constants, and includes dependency upgrades from the weekly container scans.

## 🐞 Bug fixes

### Removal of the compromised eMudhra root certificate from container images

The Tenzir Platform services no longer trust certificates issued under the `emSign ECC Root CA - G3` root. In October 2026, the private keys of eight eMudhra intermediate CAs under this root were found to be compromised, which would allow forging trusted TLS certificates for any domain. Mozilla and Google have removed the root from their trust stores in response.

The platform API, gateway, UI, CLI, and SeaweedFS images now ship trust stores without this root. Connections to services that use certificates from other eMudhra roots are unaffected.

One exception remains: the database migrations that the `platform-ui` and `platform-ui-aws` images run at startup still trust this root until an upstream runtime update removes it. This only matters if your Postgres connection uses TLS and an attacker can intercept traffic between the UI container and the database.

The images also include the dependency upgrades from the weekly container scans:

- `pyjwt` 2.13.0 to 2.15.1 and `urllib3` 2.7.0 to 2.8.0 in the platform API, gateway, and CLI images
- `brace-expansion`, `devalue`, `shell-quote`, `source-map-js`, and `undici` in the UI images

*By @lava.*

### Shared constants in Library package installations

Packages installed from the Library now retain their shared constants. Operators that use these constants, including Microsoft event processing, can resolve them after installation through the Platform.
