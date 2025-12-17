---
title: "Fix pages reloading or resetting out of nowhere"
type: bugfix
author: avaq
created: 2025-12-17T13:24:10Z
---

We addressed a bug that caused many components in the app to reset or reload
whenever the user session was automatically extended in the background
(primarily affecting sovereign edition users with short session lifespans).
