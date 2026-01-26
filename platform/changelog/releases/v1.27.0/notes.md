This release improves the pipeline detail view with faster loading and a convenient close button for quick navigation. Error messages are now cleaner with collapsible technical details, and we fixed issues where the UI could hang or become unresponsive. This release also includes security hardening for standalone deployments, including server-side token storage, configurable security headers, and Content Security Policy support.

## 🚀 Features

### Add optional Caddy reverse proxy for seaweed S3 storage

The seaweed S3 storage component now supports an optional Caddy reverse proxy that improves S3 error handling. Set `TENZIR_ENABLE_CADDY=true` to enable it. The reverse proxy intercepts 404 responses and returns proper S3-style error messages.

*By @lava.*

### Add security headers and CSP for standalone deployment

The platform frontend now supports configurable response headers and Content Security Policy (CSP) for standalone deployments.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_DEFAULT=true` to enable default security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Resource-Policy). Use `TENZIR_PLATFORM_UI_RESPONSE_HEADERS_DEFAULT` with a JSON object to override with custom headers.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_HSTS=true` to enable HTTP Strict Transport Security for HTTPS deployments.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_CSP=true` to enable Content Security Policy, which helps prevent XSS and other injection attacks.

*By @lava.*

### Faster pipeline detail view

We improved how pipeline details load, making the view faster than before when navigating between pipelines. We also added a close button next to the overflow menu on the right so you can quickly exit a pipeline while browsing pipeline details.

*By @gitryder in #19.*

### Store authentication tokens server-side

Authentication tokens (idToken and userKey) are now stored in the server-side session database instead of browser cookies. This improves security by keeping sensitive tokens accessible only via the session cookie identifier, preventing direct client-side access to authentication credentials.

*By @lava.*

## 🔧 Changes

### Cleaner error messages

We now hide technical error details in error messages. You can click "Show error details" to expand them anytime, and use the copy button to share with support.

*By @gitryder in #37.*

## 🐞 Bug fixes

### Fix hangup in UI

Fixed a potential infinite hang in the Tenzir UI that could be triggered by a rare race condition where the Tenzir Node returned duplicate pipeline ids.

*By @lava.*

### Fixed pipeline deletion

We fixed an issue where deleting a pipeline could cause the interface to become unresponsive.

*By @gitryder in #19.*
