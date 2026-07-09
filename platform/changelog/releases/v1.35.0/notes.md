This release introduces optional multi-factor authentication support for the public Tenzir Platform. It also improves the performance of the pipeline Diagnostics tab and fixes several issues across the app.

## 🚀 Features

### Multi-factor authentication support

The platform now supports multi-factor authentication (MFA).

Individual users can secure their account from **Account settings**, where a new **Multi-factor authentication** section lets them enroll an authenticator app (TOTP) by scanning a QR code, remove existing methods, and generate a recovery code to regain access if they lose their device.

Organization administrators can require MFA for everyone in their organization by enabling **Require MFA** in the organization settings. Once enabled, members must complete an MFA challenge before they can access their workspaces.

MFA enforcement is driven by your identity provider, so it requires provider-side support. In particular, the identity provider must be able to add a boolean `mfa` claim to the ID token after a successful factor challenge; the platform relies on that claim to tell whether a user has completed MFA. For now this is available only on our public cloud instance which uses Auth0, and the platform must be started with `TENZIR_PLATFORM_MFA_INTEGRATION=tenzir_auth0`. On all other deployments the integration stays at its default value of `none` and MFA enforcement is unavailable.

*By @lava and @avaq.*

## 🔧 Changes

### Graceful shutdown for Docker Compose nodes

Newly downloaded Docker Compose node configurations now include the correct timeout for graceful node shutdown.

To update an existing Docker Compose file, add `stop_grace_period: 4m` to the `tenzir-node` service.

*By @zedoraps.*

### Improve performance of the diagnostics pane

We improved the performance of the pipeline Diagnostics tab, which now stays responsive even when a pipeline has accumulated a very large number of diagnostics. The detailed diagnostics list shows the most recent entries, with a link to the Explorer for accessing the complete set.

*By @lava in #251.*

### Update links to new website

With the release of the new Tenzir website, some resources (most notably our product documentation) have moved to new locations. We've updated all the links across the platform to direct users to those new locations.

*By @Avaq.*

## 🐞 Bug fixes

### Explorer shortcut runs the current selection

The Explorer now runs the current editor selection when using the keyboard shortcut.

Previously, selecting text with `Ctrl+A` and then pressing `Ctrl+Enter` while still holding `Ctrl` could run an older selection instead of the newly selected pipeline.

*By @Zedoraps and @codex.*

### Fix App-Server startup failure behavior

Fixes an issue where the App Server can sometimes start up in a broken state and respond to every request with an error until it is restarted.

Now, if the App Server encounters an error during startup that it could not recover from, it immediately shuts down again, allowing automated restarts to take place.

*By @Avaq in #241.*

### Fix node action submenus in Firefox

Node action submenus now stay open when moving the mouse into the nested Linux or Docker options. Previously, Firefox users could lose the submenu while hovering into the third level, making update and configuration download actions hard to select.

*By @zedoraps in #231.*

### Package installs with typed operator defaults

Package installation from the Library now preserves user-defined operator defaults with the correct types.

This fixes packages whose operators use floating-point defaults such as `1.0`, and avoids sending stale package metadata as install overrides.

*By @zedoraps and @codex.*

### Server-side API proxy path validation

Server-side API proxy routes now validate resource paths before forwarding requests to upstream services.

This keeps forwarded requests within the intended upstream API scope.

*By @Zedoraps, @Avaq, and @codex in #224.*
