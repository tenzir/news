---
title: "Add security headers and CSP for standalone deployment"
type: feature
author: lava
---

The platform frontend now supports configurable response headers and Content Security Policy (CSP) for standalone deployments.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_DEFAULT=true` to enable default security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Resource-Policy). Use `TENZIR_PLATFORM_UI_RESPONSE_HEADERS_DEFAULT` with a JSON object to override with custom headers.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_HSTS=true` to enable HTTP Strict Transport Security for HTTPS deployments.

Set `TENZIR_PLATFORM_UI_ENABLE_RESPONSE_HEADERS_CSP=true` to enable Content Security Policy, which helps prevent XSS and other injection attacks.
