---
title: Drop support for legacy session storage format
type: change
author: avaq
created: 2026-07-20T15:39:28.590Z
---

We no longer support user sessions that were created by Platform versions before 1.34.0.

⚠️ If you're updating from a version prior to 1.34.0, consider updating to 1.37.0 first and allowing users to refresh their sessions before upgrading to this version. Otherwise, users must clear their browser cache or they'll receive a server error saying "Failed to establish authenticated session".
