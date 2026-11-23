---
title: "Replace tenant_manager/ path with platform_api/ in example configs"
type: change
author: lava
created: 2025-12-16T11:27:38Z
---

We switched the docker images used by our example setups from one combined `tenzir/platform` image for both the Tenzir Platform API and the Tenzir Gateway to use separate images `tenzir/platform-api` and `tenzir/platform-gateway`.

⚠️ **NOTE**: We continue building and uploading the combined `tenzir/platform` image, although we recommend switching to the new images. Due to an internal CI issue, for versions `v1.24.0` and `v1.25.0` it is necessary to change the configured command from `tenant_manager/*` to `platform_api/*`, for example `tenant_manager/rest/server/local.py` becomes `platform_api/rest/server/local.py`. We recommend skipping these versions if possible.
