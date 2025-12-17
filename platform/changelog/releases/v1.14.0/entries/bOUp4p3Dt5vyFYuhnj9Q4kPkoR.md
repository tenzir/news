---
title: "Support using different blob storage URLs for UI and Nodes"
type: feature
author: lava
created: 2025-12-17T13:24:10Z
---

The Tenzir Platform now supports the `BLOB_STORAGE__NODES_PUBLIC_ENDPOINT_URL` environment variable that allows overriding the URL used by the nodes to reach the configured S3-compatible blob storage.
This is useful if the Tenzir Nodes run in a separate network from the Tenzir UI, and the blob storage is exposed under different domains in both networks.
