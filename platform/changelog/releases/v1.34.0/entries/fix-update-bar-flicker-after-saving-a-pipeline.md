---
title: Fix the Update bar flickering after saving a pipeline
type: bugfix
author: gitryder
created: 2026-06-19T13:02:58.244463Z
---

Previously, after saving an edit on the pipeline detail page, the Cancel/Update bar would briefly reappear for about a second before disappearing again, even though nothing had changed. The bar now hides on a successful save and stays hidden until you make a new edit.
