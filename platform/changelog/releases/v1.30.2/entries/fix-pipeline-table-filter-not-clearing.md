---
title: Fix pipeline table filter not clearing
type: bugfix
author: gitryder
created: 2026-04-07T08:08:07.608839Z
---

We fixed an issue where the pipeline table stayed filtered after viewing a pipeline's detail page and navigating away to another tab. Returning to the Pipelines page would show only the previously viewed pipeline, and clearing the search had no effect.
