---
title: OpenTelemetry tracing for the Platform frontend
type: feature
authors: [avaq, jachris]
created: 2026-06-11T09:30:56.076467Z
---

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
