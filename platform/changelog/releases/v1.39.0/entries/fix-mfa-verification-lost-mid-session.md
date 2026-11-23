---
title: "Fix MFA users losing workspace access mid-session"
type: bugfix
author: gitryder
created: 2026-08-12T13:34:00Z
---

Fixed an issue where users who signed in with multi-factor authentication
would, after some time, lose access to workspaces that require MFA and could
no longer manage their authenticators until they signed out and back in.
