---
title: Python 3.13 for the platform container images
type: change
authors:
  - lava
created: 2026-08-13T09:17:52.195023Z
---

The AWS Lambda container image for the platform API has moved from the
`python:3.10` base image to `python:3.13`. The 3.10 image is built on Amazon
Linux 2, which is discontinued and no longer receives security updates; the
3.13 image is built on Amazon Linux 2023. This also removes `setuptools` from
the image entirely, since the Amazon Linux 2023 images no longer preinstall it.

The `platform-api` and `platform-gateway` images move from Python 3.10 to
Python 3.13 as well, ahead of Python 3.10 reaching end of life upstream in
October 2026. Both remain based on Debian 13.

The `tenzir-platform` CLI image moves from Python 3.11 to Python 3.13, so all
of the platform's Python images are now on the same version. Because the Debian
slim images stopped preinstalling `setuptools` after 3.11, this also resolves
CVE-2026-23949, which was reported against the `jaraco.context` copy vendored
into the base image's `setuptools`.

These changes are transparent at runtime and require no configuration or data
migration.
