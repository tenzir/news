---
title: Fix stuck loading on pipeline details
type: bugfix
author: gitryder
created: 2026-06-09T08:45:03.150844Z
---

We fixed an issue where the pipeline detail page could get stuck on loading skeletons when a node disconnected. The page now stays open and keeps showing the pipeline's definition along with a notice that the node is disconnected, and recovers automatically once the node reconnects.
