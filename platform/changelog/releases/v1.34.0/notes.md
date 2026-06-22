This release introduces OpenTelemetry tracing for the Platform frontend, giving operators end-to-end visibility into the requests its backend handles. It also adds dedicated columns for common fields like timestamps in the Stream view, overhauls login and session handling for better performance, and fixes a range of loading and navigation issues across the app.

## 🚀 Features

### Common fields now appear as columns

We improved the Stream view by displaying fields that are shared across all schemas in dedicated columns. Timestamps are the first supported field, making it easier to scan and compare at a glance while still allowing you to expand rows to view the full event. When no shared timestamp field is available, Stream view continues to use the existing layout.

*By @gitryder.*

### OpenTelemetry tracing for the Platform frontend

The Platform frontend can now export OpenTelemetry traces over OTLP, giving operators end-to-end visibility into the requests its backend handles.

Enable tracing and point it at your OTLP collector:

```sh
PUBLIC_ENABLE_TRACING=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

Traces are sent to `${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces` by default. Set `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` to override the traces endpoint directly.

When exporting to a collector that requires authentication, supply headers as comma-separated `key=value` pairs:

```sh
OTEL_EXPORTER_OTLP_HEADERS="authorization=Bearer <token>,x-tenant=acme"
```

*By @avaq and @jachris.*

## 🔧 Changes

### Remove direct Websocket Gateway connection support

The Platform configuration variable `PUBLIC_USE_INTERNAL_WS_PROXY` no longer has any effect. The platform now behaves as though this setting is always enabled: All connections to the Websocket Gateway are now proxied through the App Server ("BFF").

The `PUBLIC_WEBSOCKET_GATEWAY_ENDPOINT` variable that used to configure the direct Gateway connection is now used as a fallback for when the `PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT` isn't defined.

*By @avaq.*

### Security and performance improvements

We overhauled the frontend's login and session handling. Compared to the previous release:

- OIDC provider metadata is now discovered once at application startup instead of on every session refresh, shaving the round-trip cost off many requests.
- User keys (access tokens) are now always cached server-side in the user's session, alleviating the cost of obtaining new access tokens for many requests.
- Users of Platform deployments using header-based auth (like Google IAP) are now also granted a login session, allowing them to benefit from session based caches. This means that access tokens and user metadata is no longer fetched externally on every request, potentially saving multiple round trips worth of time with each request.
- Session IDs no longer leak to JavaScript, and are solely kept inside secure HTTP cookies.

*By @avaq.*

## 🐞 Bug fixes

### Delete dashboards when removing a static workspace

Previously, when a workspace was removed from the static configuration file, dashboards that users had created within that workspace were left behind as orphaned records in the database. These could resurface if a new workspace later reused the same workspace ID. Removing a static workspace now also deletes these user-created dashboards.

*By @gitryder.*

### Examples drawer loads on nodes with sparse package metadata

The Explorer's Examples drawer no longer hangs at "Loading…" on Tenzir Nodes that have installed packages whose examples are missing a `name` or `description` (for instance several mappers under `microsoft/`, `fortinet/`, `otel/`, and `zscaler/` in the Tenzir Library).

*By @Zedoraps and @claude.*

### Explorer downloads on nodes using the legacy execution engine

Downloading results from the Explorer now works on Tenzir Nodes v6+ that are configured to run pipelines on the legacy execution engine (`tenzir.neo: false`). Previously, preparing the download failed on such nodes because the pipeline that uploads the results relied on functionality that is only available in the new execution engine. The download pipeline now always runs on the new execution engine, regardless of the node's configuration.

*By @tobim and @claude in #184.*

### Fix docs not loading

The documentation panel should now show the documentation website again, instead of a white page.

*By @avaq.*

### Fix main menu links on some pages in the app

The main menu links (Pipelines, Explorer, Contexts, and Library) now navigate correctly from all pages in the app. Previously, some pages would always link to the Pipelines page, even when clicking one of the other items.

*By @avaq.*

### Fix stuck loading on pipeline details

We fixed an issue where the pipeline detail page could get stuck on loading skeletons when a node disconnected. The page now stays open and keeps showing the pipeline's definition along with a notice that the node is disconnected, and recovers automatically once the node reconnects.

*By @gitryder.*

### Fix the Update bar flickering after saving a pipeline

Previously, after saving an edit on the pipeline detail page, the Cancel/Update bar would briefly reappear for about a second before disappearing again, even though nothing had changed. The bar now hides on a successful save and stays hidden until you make a new edit.

*By @gitryder.*

### Library tab no longer hangs after interrupted load

The Library tab now loads reliably after a previous attempt was interrupted by a page reload or navigation. Previously the tab could get stuck at "Loading…" indefinitely until the browser session was cleared.

*By @Zedoraps and @claude.*
