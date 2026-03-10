This release fixes an issue where ephemeral nodes were causing the frontend to display a 500 error message or be displayed with incorrect connection status.

## 🚀 Features

### Add experimental Insights tab to pipeline detail view

The pipeline detail modal now includes an experimental Insights tab that visualizes per-operator backpressure, helping users identify bottlenecks in their pipelines. This tab is only available for pipelines running on the experimental new executor.

*By @realllydan.*

### Add PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT environment variable

The app container now supports a `PRIVATE_WEBSOCKET_GATEWAY_ENDPOINT` environment variable that overrides the existing `PUBLIC_WEBSOCKET_GATEWAY_ENDPOINT` for calls in the app backend. This allows configuring different endpoints when the frontend and backend live in different networks.

*By @benno.*

## 🐞 Bug fixes

### Fix ephemeral nodes not showing correctly in the UI

We fixed an issue where ephemeral nodes were causing the frontend to fail to render or be displayed with incorrect connection status.

*By @benno.*
